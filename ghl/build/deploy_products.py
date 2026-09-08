#!/usr/bin/env python3
"""Create GHL Products + one-time Prices from a JSON spec (location PIT).

  POST /products/                 {name, locationId, productType, description, availableInStore}
  POST /products/{id}/prices      {name, type: "one_time", currency, amount, locationId}
Idempotent by product name (existing product: prices are added only if none
match the amount). Dry run by default.

  python build/deploy_products.py --target riverside --spec snapshots/event-rental/clients/riverside-products.json [--live]
"""
from __future__ import annotations
import argparse, json, sys
import requests
from ghl_target import add_target_args, resolve

BASE = "https://services.leadconnectorhq.com"
G, Y, R, B, X = "\033[32m", "\033[33m", "\033[31m", "\033[1m", "\033[0m"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    add_target_args(ap); ap.add_argument("--spec", required=True)
    args = ap.parse_args(); t = resolve(args); loc = t.location_id
    H = {"Authorization": f"Bearer {t.token}", "Version": "2021-07-28", "Content-Type": "application/json"}
    spec = json.load(open(args.spec))
    r = requests.get(f"{BASE}/products/", headers=H, params={"locationId": loc, "limit": 100}, timeout=45)
    existing = {p["name"].strip().lower(): p for p in (r.json().get("products", []) if r.ok else [])}
    print(f"{B}{len(spec)} products in spec, {len(existing)} in {t.label}{X}  ({'LIVE' if t.live else 'dry run'})\n")
    for s in spec:
        key = s["name"].strip().lower(); p = existing.get(key)
        if p:
            pr = requests.get(f"{BASE}/products/{p['_id']}/price", headers=H, params={"locationId": loc}, timeout=45)
            prices = pr.json().get("prices", []) if pr.ok else []
            if any(abs(float(x.get("amount", 0)) - s["amount"]) < 0.01 for x in prices):
                print(G + f"  = {s['name']:34} ${s['amount']:>8,.2f} exists" + X); continue
            print(Y + f"  ~ {s['name']:34} ${s['amount']:>8,.2f} product exists, add price" + X)
            if t.live:
                q = requests.post(f"{BASE}/products/{p['_id']}/price", headers=H, data=json.dumps({"name": s["name"], "type": "one_time", "currency": "USD", "amount": s["amount"], "locationId": loc}), timeout=45)
                print(("    " + G + f"price {q.status_code}" + X) if q.ok else ("    " + R + f"price {q.status_code} {q.text[:200]}" + X))
            continue
        print(Y + f"  + {s['name']:34} ${s['amount']:>8,.2f} CREATE" + X)
        if not t.live: continue
        c = requests.post(f"{BASE}/products/", headers=H, data=json.dumps({"name": s["name"], "locationId": loc, "productType": s.get("type", "SERVICE"), "description": s.get("description", ""), "availableInStore": False}), timeout=45)
        if not c.ok: print("    " + R + f"product {c.status_code} {c.text[:200]}" + X); continue
        pid = c.json().get("_id") or c.json().get("id")
        q = requests.post(f"{BASE}/products/{pid}/price", headers=H, data=json.dumps({"name": s["name"], "type": "one_time", "currency": "USD", "amount": s["amount"], "locationId": loc}), timeout=45)
        print(("    " + G + f"product {pid} price {q.status_code}" + X) if q.ok else ("    " + R + f"product {pid} price {q.status_code} {q.text[:200]}" + X))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
