#!/usr/bin/env python3
"""Assign every task-notification step in a sub-account's workflows to a user.

Finding 2026-09-04 (Riverside test): a task step with `assignedTo: ""` is silently
skipped - no task is created and nothing is logged. The template ships tasks
unassigned because it cannot know the client's users, so run this right after
provisioning users (build/add_users.py).

  export GHL_BEARER=...   # browser session JWT (see BROWSER-RECIPES.md)
  python build/assign_tasks.py --target riverside --user OCw93AQjlkxWAo1MbOj5 [--live]
"""
from __future__ import annotations
import argparse, json, os, sys, time
import requests
from ghl_target import add_target_args, resolve

BACKEND = "https://backend.leadconnectorhq.com"
G, Y, R, B, X = "\033[32m", "\033[33m", "\033[31m", "\033[1m", "\033[0m"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    add_target_args(ap); ap.add_argument("--user", required=True, help="GHL user id to assign tasks to")
    ap.add_argument("--force", action="store_true", help="reassign even if already assigned to someone")
    args = ap.parse_args(); t = resolve(args); loc = t.location_id
    tok = os.getenv("GHL_BEARER", "").strip()
    if not tok: sys.exit(R + "GHL_BEARER not set" + X)
    H = {"authorization": f"Bearer {tok}", "channel": "APP", "source": "WEB_USER", "content-type": "application/json"}
    rows = [x for x in requests.get(f"{BACKEND}/workflow/{loc}/list", headers=H, params={"limit": 200, "offset": 0}, timeout=45).json()["rows"] if x.get("type") != "directory"]
    total = 0
    for w in rows:
        wid = w.get("_id") or w.get("id")
        d = requests.get(f"{BACKEND}/workflow/{loc}/{wid}", headers=H, params={"includeScheduledPauseInfo": "true"}, timeout=45).json()
        mod = []
        for s in d.get("workflowData", {}).get("templates", []):
            if s["type"] != "task-notification": continue
            a = s.setdefault("attributes", {})
            if a.get("assignedTo") and not args.force: continue
            a["assignedTo"] = args.user; mod.append(s["id"]); print(f"  {w['name'][:34]:34} {s['name'][:40]}")
        if not mod: continue
        total += len(mod)
        if not t.live: continue
        d.update({"modifiedSteps": mod, "createdSteps": [], "deletedSteps": [], "triggersChanged": False, "permissionMeta": {"canRead": True, "canWrite": True}, "scheduledPauseDates": d.get("scheduledPauseDates", [])})
        p = requests.put(f"{BACKEND}/workflow/{loc}/{wid}", headers=H, data=json.dumps(d), timeout=60)
        print((G if p.ok else R) + f"      PUT {p.status_code} {'' if p.ok else p.text[:200]}" + X); time.sleep(0.4)
    print(f"\n{B}{total} task steps {'assigned' if t.live else 'would be assigned'} to {args.user}{X}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
