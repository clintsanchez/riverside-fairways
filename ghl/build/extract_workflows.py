#!/usr/bin/env python3
"""
Extract every workflow in a sub-account to JSON — including the step tree.

Why this exists: the public API lists workflows but returns only metadata
(id, name, status). The steps live in Firebase Storage behind the workflow
document's `fileUrl`, reachable through GHL's internal API. Without this, a
snapshot's workflows can only be read by clicking through the UI, which is why
they are the one asset the deploy system still rebuilds by hand.

Read-only. Writes nothing to GHL.

  # 1. get a token (see --token-help)
  export GHL_TOKEN_ID="..."
  # 2. extract
  python build/extract_workflows.py --target grow --out snapshots/grow/workflows.json
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import sys
import time
from pathlib import Path
from urllib.parse import quote

import requests

from ghl_target import add_target_args, resolve

INTERNAL = "https://backend.leadconnectorhq.com"
G, Y, R, D, B, X = "\033[32m", "\033[33m", "\033[31m", "\033[2m", "\033[1m", "\033[0m"

TOKEN_HELP = f"""
{B}  Get an internal-API token{X}

  The step tree is not on the public API. It needs the Firebase token from a
  logged-in browser session, which lasts about an hour.

  1. Open {B}app.gohighlevel.com{X} in Chrome, logged into the right sub-account
  2. DevTools (⌥⌘I) → Console
  3. Paste:

{G}     copy(await new Promise(r=>{{const q=indexedDB.open("firebaseLocalStorageDb");q.onsuccess=()=>{{const s=q.result.transaction("firebaseLocalStorage","readonly").objectStore("firebaseLocalStorage").getAll();s.onsuccess=()=>r(s.result.map(x=>x?.value?.stsTokenManager?.accessToken).find(Boolean)??null)}};q.onerror=()=>r(null)}}))\033[0m

  4. {G}export GHL_TOKEN_ID="<paste>"{X}

  Nothing is stored on disk; the token lives only in that shell.
"""


def token_info(tok: str) -> dict:
    try:
        payload = tok.split(".")[1]
        payload += "=" * (-len(payload) % 4)
        p = json.loads(base64.urlsafe_b64decode(payload))
        return {
            "user": p.get("user_id"),
            "expires_in": int(p.get("exp", 0) - time.time()),
            "locations": p.get("locations", []),
        }
    except Exception:
        return {}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    add_target_args(ap)
    ap.add_argument("--out", help="Write JSON here (default: stdout summary only)")
    ap.add_argument("--token-help", action="store_true", help="How to get GHL_TOKEN_ID")
    ap.add_argument("--limit", type=int, default=200)
    args, _ = ap.parse_known_args()

    if "--token-help" in sys.argv:
        print(TOKEN_HELP)
        return 0

    args = ap.parse_args()
    t = resolve(args)

    tok = os.getenv("GHL_TOKEN_ID", "").strip()
    if not tok:
        print(R + "  GHL_TOKEN_ID is not set." + X)
        print(TOKEN_HELP)
        return 1

    info = token_info(tok)
    if info.get("expires_in", 0) <= 0:
        print(R + "  Token is expired — get a fresh one (--token-help).\n" + X)
        return 1
    if info.get("locations") and t.location_id not in info["locations"]:
        # The token is scoped per user/location; using it against another
        # sub-account silently returns that user's own data instead.
        print(R + f"  This token does not cover {t.location_id}." + X)
        print(D + f"  It covers: {', '.join(info['locations'][:4])}\n" + X)
        return 1

    H = {"token-id": tok, "channel": "APP", "Accept": "application/json"}
    print(D + f"  token ok, {info.get('expires_in',0)//60} min left\n" + X)

    r = requests.get(f"{INTERNAL}/workflow/{t.location_id}/list",
                     headers=H, params={"limit": args.limit, "offset": 0}, timeout=45)
    if not r.ok:
        print(R + f"  list failed: {r.status_code} {r.text[:160]}\n" + X)
        return 1
    rows = [x for x in r.json().get("rows", []) if x.get("type") != "directory"]
    print(f"{B}  {len(rows)} workflows{X}\n")

    out, no_steps = [], 0
    for row in rows:
        wid = row.get("_id") or row.get("id")
        meta = requests.get(f"{INTERNAL}/workflow/{t.location_id}/{wid}", headers=H, timeout=45)
        if not meta.ok:
            print(f"    {R}✗{X} {row.get('name','?')[:52]} {D}{meta.status_code}{X}")
            continue
        m = meta.json()

        steps = None
        if m.get("fileUrl"):
            try:
                fr = requests.get(m["fileUrl"], timeout=45)
                if fr.ok:
                    steps = fr.json().get("templates")
            except Exception:
                steps = None

        if steps is None:
            no_steps += 1
        n = len(steps or [])
        mark = G + "✓" + X if steps is not None else Y + "!" + X
        print(f"    {mark} {m.get('name','?')[:52]:<54} {D}{m.get('status','?'):<10} {n} steps{X}")

        out.append({
            "id": wid,
            "name": m.get("name"),
            "status": m.get("status"),
            "version": m.get("version"),
            "stopOnResponse": m.get("stopOnResponse"),
            "allowMultiple": m.get("allowMultiple"),
            "timezone": m.get("timezone"),
            "window": m.get("window"),
            "steps": steps or [],
        })

    print()
    if no_steps:
        print(Y + f"  {no_steps} workflow(s) returned no step tree — usually an empty or draft workflow.\n" + X)

    if args.out:
        p = Path(args.out)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps({
            "locationId": t.location_id,
            "target": t.slug,
            "extractedAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "workflows": out,
        }, indent=1, ensure_ascii=False))
        total = sum(len(w["steps"]) for w in out)
        print(G + f"  wrote {p}  ({len(out)} workflows, {total} steps)\n" + X)
    return 0


if __name__ == "__main__":
    sys.exit(main())
