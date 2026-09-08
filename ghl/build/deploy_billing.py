#!/usr/bin/env python3
"""Create the quote / deposit / balance templates per package tier (public Invoices API, location PIT).

  GET  /products/?locationId=                          products (+ /products/{id}/price for amounts)
  POST /invoices/estimate/template  {altId, altType, name, title, currency, businessDetails, items[{name, currency, amount, qty, type:"one_time", productId?, priceId?}], discount, termsNotes}
  POST /invoices/template           {altId, altType, name, currency, businessDetails, items[...], discount, termsNotes}
  GET  /invoices/template | /invoices/estimate/template   (idempotent by name)
Deposit percent comes from the Deposit Percent custom value ("50%"). Writes snapshots/event-rental/clients/<slug>-billing-ids.json.

  python build/deploy_billing.py --target riverside --spec snapshots/event-rental/config/billing.json [--live]
"""
from __future__ import annotations
import argparse, json, re
import requests
from ghl_target import add_target_args, resolve

BASE = "https://services.leadconnectorhq.com"
G, Y, R, B, X = "\033[32m", "\033[33m", "\033[31m", "\033[1m", "\033[0m"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    add_target_args(ap); ap.add_argument("--spec", required=True)
    a = ap.parse_args(); t = resolve(a); loc = t.location_id
    H = {"Authorization": f"Bearer {t.token}", "Version": "2021-07-28", "Content-Type": "application/json"}
    spec = json.load(open(a.spec)); q = {"altId": loc, "altType": "location"}
    cvs = requests.get(f"{BASE}/locations/{loc}/customValues", headers=H, timeout=45).json()["customValues"]
    cv = {v["fieldKey"].replace("{{ custom_values.", "").rstrip(" }"): (v.get("value") or "") for v in cvs}
    pct = float(re.sub(r"[^0-9.]", "", cv.get("deposit_percent") or "50") or 50)
    biz = {"name": cv.get("business_name") or t.label, "phoneNo": cv.get("business_phone", ""), "website": cv.get("business_website", "")}
    prods = requests.get(f"{BASE}/products/", headers=H, params={"locationId": loc, "limit": 100}, timeout=45).json().get("products", [])
    byname = {p["name"].strip().lower(): p for p in prods}
    est_ex = {e["name"]: e["_id"] for e in requests.get(f"{BASE}/invoices/estimate/template", headers=H, params={**q, "limit": 100, "offset": 0}, timeout=45).json().get("data", [])}
    inv_ex = {e["name"]: e["_id"] for e in requests.get(f"{BASE}/invoices/template", headers=H, params={**q, "limit": 100, "offset": 0}, timeout=45).json().get("data", [])}
    print(f"{B}{t.label}{X}: {len(prods)} products, deposit {pct:g}%, {len(est_ex)} estimate + {len(inv_ex)} invoice templates exist  ({'LIVE' if t.live else 'dry run'})")
    out = {"location_id": loc, "deposit_percent": pct, "tiers": {}}
    for tier in spec["tiers"]:
        p = byname.get(tier["product"].strip().lower())
        if not p: print(R + f"  product missing: {tier['product']}" + X); continue
        pr = requests.get(f"{BASE}/products/{p['_id']}/price", headers=H, params={"locationId": loc}, timeout=45).json().get("prices", [])
        if not pr: print(R + f"  no price on {tier['product']}" + X); continue
        amount = float(pr[0]["amount"]); dep = round(amount * pct / 100, 2); bal = round(amount - dep, 2)
        label = tier["label"]; ids = {}
        docs = {
            "estimate": (f"{BASE}/invoices/estimate/template", est_ex, {"name": spec["estimate"]["name"].format(label=label), "title": spec["estimate"]["title"], "items": [{"name": p["name"], "description": p.get("description", ""), "currency": "USD", "amount": amount, "qty": 1, "type": "one_time", "productId": p["_id"], "priceId": pr[0]["_id"]}], "termsNotes": spec["estimate"]["terms"]}),
            "deposit": (f"{BASE}/invoices/template", inv_ex, {"name": spec["deposit"]["name"].format(label=label), "items": [{"name": spec["deposit"]["item_name"].format(label=label, percent=f"{pct:g}"), "currency": "USD", "amount": dep, "qty": 1}], "termsNotes": spec["deposit"]["terms"]}),
            "balance": (f"{BASE}/invoices/template", inv_ex, {"name": spec["balance"]["name"].format(label=label), "items": [{"name": spec["balance"]["item_name"].format(label=label), "currency": "USD", "amount": bal, "qty": 1}], "termsNotes": spec["balance"]["terms"]}),
        }
        for kind, (url, existing, body) in docs.items():
            if body["name"] in existing:
                ids[kind] = existing[body["name"]]; print(G + f"  = {body['name']:28} ${body['items'][0]['amount']:>9,.2f}" + X); continue
            print(Y + f"  + {body['name']:28} ${body['items'][0]['amount']:>9,.2f}" + X)
            if not t.live: continue
            r = requests.post(url, headers=H, data=json.dumps({**q, "currency": "USD", "businessDetails": biz, "discount": {"type": "percentage", "value": 0}, **body}), timeout=45)
            if r.ok: ids[kind] = r.json()["_id"]
            else: print("    " + R + f"{r.status_code} {r.text[:200]}" + X)
        out["tiers"][tier["key"]] = {"package_interest": tier["package_interest"], "label": label, "amount": amount, "deposit": dep, "balance": bal, **ids}
    for ex in spec.get("extra_estimates", []):
        items = []
        for pname in ex["products"]:
            p = byname.get(pname.strip().lower())
            if not p: print(Y + f"  extra: product missing {pname}" + X); continue
            pr = requests.get(f"{BASE}/products/{p['_id']}/price", headers=H, params={"locationId": loc}, timeout=45).json().get("prices", [])
            if pr: items.append({"name": p["name"], "description": p.get("description", ""), "currency": "USD", "amount": float(pr[0]["amount"]), "qty": 1, "type": "one_time", "productId": p["_id"], "priceId": pr[0]["_id"]})
        if ex["name"] in est_ex: out.setdefault("extra", {})[ex["name"]] = est_ex[ex["name"]]; print(G + f"  = {ex['name']:28} {len(items)} lines" + X); continue
        print(Y + f"  + {ex['name']:28} {len(items)} lines" + X)
        if t.live and items:
            r = requests.post(f"{BASE}/invoices/estimate/template", headers=H, data=json.dumps({**q, "currency": "USD", "businessDetails": biz, "discount": {"type": "percentage", "value": 0}, "name": ex["name"], "title": ex["title"], "items": items, "termsNotes": ex["terms"]}), timeout=45)
            if r.ok: out.setdefault("extra", {})[ex["name"]] = r.json()["_id"]
            else: print("    " + R + f"{r.status_code} {r.text[:200]}" + X)
    if t.live:
        path = f"snapshots/event-rental/clients/{a.target}-billing-ids.json"
        json.dump(out, open(path, "w"), indent=1); print(f"\n  ids -> {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
