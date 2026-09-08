#!/usr/bin/env python3
"""Patch workflow steps as data through the builder's own save endpoint.

The workflow builder persists with
  PUT https://backend.leadconnectorhq.com/workflow/{loc}/{wfId}
carrying the whole document (GET the same URL returns it, including
workflowData.templates = the step tree). Auth is the browser session's
`authorization: Bearer <jwt>` (NOT the Firebase token-id) plus
`channel: APP`, `source: WEB_USER`. Captured 2026-09-03 from a real save.

Fixes come from snapshots/<name>/config/workflow_fixes.json:
  global_field_swaps        - string replacements applied to every attribute
  workflows[<name>][<step>] - replacement body/subject/name per step

  export GHL_BEARER=...              # from a captured builder request
  python build/patch_workflows.py --target template-event --fixes snapshots/event-rental/config/workflow_fixes.json
  python build/patch_workflows.py --target template-event --fixes ... --only "4. Got Estimate / Follow-Up" --live
"""
from __future__ import annotations

import argparse, json, os, re, sys, time
import requests
from ghl_target import add_target_args, resolve

BACKEND = "https://backend.leadconnectorhq.com"
G, Y, R, D, B, X = "\033[32m", "\033[33m", "\033[31m", "\033[2m", "\033[1m", "\033[0m"
TEXT_KEYS = ("body", "subject", "whisper_message", "from_name", "from_email", "to", "message", "html")


def hdrs():
    tok = os.getenv("GHL_BEARER", "").strip()
    if not tok:
        sys.exit(R + "GHL_BEARER not set - capture the builder's `authorization` header from a save." + X)
    return {"authorization": f"Bearer {tok}", "channel": "APP", "source": "WEB_USER",
            "accept": "application/json", "content-type": "application/json"}


def swap_strings(obj, swaps):
    """Apply global string swaps to every string in attributes; return changed flag."""
    changed = False
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(v, str):
                nv = v
                for a, b in swaps.items():
                    nv = nv.replace("{{" + a + "}}", "{{" + b + "}}").replace("{{ " + a + " }}", "{{" + b + "}}").replace(a, b) if not a.startswith("custom_values.") else nv.replace(a, b)
                if nv != v:
                    obj[k] = nv; changed = True
            elif isinstance(v, (dict, list)):
                changed = swap_strings(v, swaps) or changed
    elif isinstance(obj, list):
        for v in obj:
            changed = swap_strings(v, swaps) or changed
    return changed


def parse_fix(fx):
    """A fix string may be 'SUBJECT: ... | FROM NAME: ... | FROM: ... | TO: ...' or a plain SMS body or 'WHISPER: ...'."""
    out = {}
    if fx.startswith("SUBJECT:") or " | FROM" in fx:
        for part in fx.split(" | "):
            k, _, v = part.partition(":")
            k = k.strip().upper(); v = v.strip()
            if k == "SUBJECT": out["subject"] = v
            elif k == "FROM NAME": out["from_name"] = v
            elif k == "FROM": out["from_email"] = v
            elif k == "TO": out["to"] = v
        return out
    if fx.startswith("WHISPER:"):
        return {"whisper_message": fx[len("WHISPER:"):].strip()}
    if fx.startswith("Rename step:"):
        v = fx.split(":", 1)[1].split(". Stage:")[0].strip().strip("'\"")
        return {"_name": v}
    if fx.startswith("Rename condition:"):
        return {"conditionName": fx.split(":", 1)[1].strip()}
    if fx.startswith("Change tag to:"):
        return {"tags": [x.strip() for x in fx.split(":", 1)[1].split(",")]}
    if fx.startswith("Add tags:"):
        return {"tags": [x.strip() for x in fx.split(":", 1)[1].split("(")[0].split(",") if x.strip()]}
    if fx.startswith(("Stage:", "REPLACE with", "WAIT TYPE", "monetary_value", "PER-STEP")):
        return {"_manual": fx}
    return {"body": fx}


def apply_fixes(doc, wf_fix, swaps, log):
    tpl = doc["workflowData"]["templates"]
    modified = []
    by_order = wf_fix.get("_sms_by_order", {}); subj_by_order = wf_fix.get("_email_subject_by_order", {})
    rn_steps = wf_fix.get("_rename_steps", {}); rn_conds = wf_fix.get("_rename_conditions", {})
    for seq, st in enumerate(tpl, 1):
        before = json.dumps(st, sort_keys=True)
        a = st.setdefault("attributes", {})
        if st.get("name") in rn_steps: st["name"] = rn_steps[st["name"]]
        # GHL's current validator rejects create_opportunity steps without a `fields` array
        # ("Fields is required") - the Skool base never had it. Normalise so UI saves pass.
        if st.get("type") == "create_opportunity" and "fields" not in a: a["fields"] = []
        if a.get("conditionName") in rn_conds: a["conditionName"] = rn_conds[a["conditionName"]]
        # per-step replacement
        fx = None
        if st.get("type") == "sms" and str(st.get("order")) in by_order: fx = by_order[str(st["order"])]
        elif st.get("type") == "email" and str(st.get("order")) in subj_by_order: fx = "SUBJECT: " + subj_by_order[str(st["order"])]
        elif st.get("name") in wf_fix and not st["name"].startswith("_"): fx = wf_fix[st["name"]]
        if fx:
            parsed = parse_fix(fx)
            if "_manual" in parsed:
                log.append((st["name"], "MANUAL", parsed["_manual"][:90]))
            else:
                if "_name" in parsed:
                    st["name"] = parsed.pop("_name")
                for k, v in parsed.items():
                    tgt = a
                    if k in ("from_name", "from_email", "subject", "to") and isinstance(a.get("email"), dict): tgt = a["email"]
                    if k == "to" and isinstance(a.get("sms"), dict): tgt = a["sms"]
                    tgt[k] = v
                kind = {"sms": "SMS", "email": "Email", "call": "Call", "internal_notification": "Internal"}.get(st.get("type"))
                if kind and ("body" in parsed or "subject" in parsed or "whisper_message" in parsed) and not re.match(r"^\d+[a-z]? - ", st["name"]):
                    src = parsed.get("subject") or parsed.get("whisper_message") or parsed.get("body") or ""
                    slug = re.sub(r"\{\{[^}]*\}\}", "", src); slug = re.sub(r"[^A-Za-z0-9 '-]", " ", slug)
                    words = [w for w in slug.split() if w.lower() not in ("hi", "hey", "hello", "thanks", "a", "the", "-", "again")]
                    slug = " ".join(words[:5]).rstrip("- ")
                    st["name"] = f"{seq} - {kind}: {slug}"
        # global merge-field swaps everywhere
        swap_strings(a, swaps)
        if json.dumps(st, sort_keys=True) != before:
            modified.append(st["id"]); log.append((st["name"], "PATCH", ", ".join(k for k in (parse_fix(fx) if fx else {}) if k != "_manual") or "field swaps"))
    return modified


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    add_target_args(ap)
    ap.add_argument("--fixes", required=True)
    ap.add_argument("--only", help="workflow name to restrict to")
    args = ap.parse_args()
    t = resolve(args)
    H = hdrs()
    FIX = json.load(open(args.fixes))
    swaps = FIX.get("global_field_swaps", {})

    r = requests.get(f"{BACKEND}/workflow/{t.location_id}/list", headers=H, params={"limit": 200, "offset": 0}, timeout=45)
    r.raise_for_status()
    rows = [x for x in r.json().get("rows", []) if x.get("type") != "directory"]
    print(f"{B}{len(rows)} workflows{X}  ({'LIVE' if t.live else 'dry run'})\n")
    for w in rows:
        name = w.get("name")
        norm = lambda x: " ".join(str(x).split()).strip().lower()
        if args.only and norm(name) != norm(args.only): continue
        wf_fix = next((v for k, v in FIX["workflows"].items() if norm(k) == norm(name)), {})
        g = requests.get(f"{BACKEND}/workflow/{t.location_id}/{w['_id'] if '_id' in w else w['id']}", headers=H, params={"includeScheduledPauseInfo": "true"}, timeout=45)
        if not g.ok: print(R + f"  ! {name}: GET {g.status_code}" + X); continue
        doc = g.json()
        if "workflowData" not in doc: print(Y + f"  - {name}: no workflowData (draft/empty)" + X); continue
        log = []
        modified = apply_fixes(doc, wf_fix, swaps, log)
        rename = wf_fix.get("_rename_to")
        if rename and doc.get("name") != rename: doc["name"] = rename; log.append(("<workflow>", "RENAME", rename))
        print(f"{B}  {name}{X}  {len(modified)} steps modified" + (f"  -> {rename}" if rename else ""))
        for n, kind, what in log:
            col = G if kind == "PATCH" else (Y if kind == "MANUAL" else B)
            print(f"      {col}{kind:6}{X} {n[:40]:40} {D}{what}{X}")
        if not t.live or not (modified or rename): continue
        body = dict(doc)
        body.update({"modifiedSteps": modified, "deletedSteps": [], "createdSteps": [], "triggersChanged": False,
                     "permissionMeta": {"canRead": True, "canWrite": True}, "scheduledPauseDates": doc.get("scheduledPauseDates", [])})
        p = requests.put(f"{BACKEND}/workflow/{t.location_id}/{doc['_id']}", headers=H, data=json.dumps(body), timeout=60)
        print(("      " + G + f"PUT {p.status_code} version {p.json().get('version') if p.ok else ''}" + X) if p.ok else ("      " + R + f"PUT {p.status_code} {p.text[:200]}" + X))
        time.sleep(0.5)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
