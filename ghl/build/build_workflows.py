#!/usr/bin/env python3
"""Create whole workflows as data through the builder's own endpoints.

Discovered 2026-09-03 by capturing the GHL workflow builder:
  POST /workflow/{loc}                      -> {id}            create an empty shell
  POST /workflow/{loc}/trigger              -> {id}            create a trigger (needs workflowId, status: draft)
  PUT  /workflow/{loc}/{id}                 -> document        write steps; triggersChanged + newTriggers attaches triggers
  GET  /workflow/{loc}/trigger?workflowId=  -> [triggers]
Auth: browser session `authorization: Bearer <jwt>` + channel: APP + source: WEB_USER.

Spec: a JSON file with a list of workflows, each:
  { "name": "...", "settings": {...optional doc overrides...},
    "triggers": [ {trigger doc without ids} ],
    "steps":    [ {"name": "...", "type": "sms", "attributes": {...}}, ... ]   # linear chain
  }
Steps are chained in order (next = following step's id; last next = ""). Branching
(if_else) steps carry their own `branches` in attributes; put branch children after
the if_else with `"parent": "<if_else name>", "branch": "<branch name>"` and they
are wired into that branch (linear within the branch).

  export GHL_BEARER=...
  python build/build_workflows.py --target template-event --spec snapshots/event-rental/config/workflow_build.json
  python build/build_workflows.py --target template-event --spec ... --only "5. ..." --live
Idempotent by name: an existing workflow with the same name is UPDATED (steps
replaced, triggers reconciled) rather than duplicated.
"""
from __future__ import annotations

import argparse, json, os, sys, time, uuid
import requests
from ghl_target import add_target_args, resolve

BACKEND = "https://backend.leadconnectorhq.com"
G, Y, R, D, B, X = "\033[32m", "\033[33m", "\033[31m", "\033[2m", "\033[1m", "\033[0m"
COMPANY = "e2kBZzx6fPOIPYPlu3ci"


def hdrs():
    tok = os.getenv("GHL_BEARER", "").strip()
    if not tok: sys.exit(R + "GHL_BEARER not set" + X)
    return {"authorization": f"Bearer {tok}", "channel": "APP", "source": "WEB_USER",
            "accept": "application/json", "content-type": "application/json"}


def norm(s): return " ".join(str(s).split()).strip().lower()


def build_templates(steps):
    """Turn the spec's step list into GHL templates with ids + next wiring.

    Linear chains: next/parentKey. Branching (if_else) follows the current builder
    model captured 2026-09-04: the condition node carries `attributes.branches[]`
    and `next` = [branch ids]; every branch (and the implicit "None" else-branch)
    is its own `if_else` node whose id == branches[i].id, with `parent` = the
    condition node, `sibling` = the other branch ids and `next` = its first child.
    Children of a branch carry `parent` = branch id and chain with parentKey.
    Spec: a step with "parent": "<if_else name>", "branch": "<branch name>|None".
    """
    tpl = []
    for i, s in enumerate(steps):
        node = {"id": str(uuid.uuid4()), "order": i, "name": s["name"], "type": s["type"],
                "attributes": json.loads(json.dumps(s.get("attributes", {}))), "next": "",
                "_parent": s.get("parent"), "_branch": s.get("branch")}
        if s.get("workflowsActionType"): node["workflowsActionType"] = s["workflowsActionType"]   # INTERNAL actions (documents, conversation AI) need this or "corrupted type"
        tpl.append(node)
    by_name = {t["name"]: t for t in tpl}
    # 1) materialise branch nodes for every if_else condition node
    extra = []
    for t in tpl:
        if t["type"] != "if_else" or t["_parent"] is not None and t["attributes"].get("else"): continue
        if t["type"] == "if_else" and not t["attributes"].get("branches") and not t["attributes"].get("else"): continue
        if t["type"] != "if_else": continue
        a = t["attributes"]; a.setdefault("currentRecipeType", "CUSTOM"); a.setdefault("operator", "and"); a.setdefault("if", True); a.setdefault("version", 2); a.setdefault("noneBranchName", "None")
        t["cat"] = "conditions"; t["nodeType"] = "condition-node"
        branch_nodes = []
        for br in a["branches"]:
            br.setdefault("id", str(uuid.uuid4()))
            for seg in br.get("segments", []):
                seg.setdefault("__segmentId", str(uuid.uuid4()))
                for c in seg.get("conditions", []): c.setdefault("__conditionId", str(uuid.uuid4())); c.setdefault("ifElseNodeId", ""); c.setdefault("isWait", False)
            branch_nodes.append({"id": br["id"], "parent": t["id"], "order": 1, "name": br["name"], "type": "if_else", "cat": "conditions", "nodeType": "branch-yes",
                                 "attributes": {"if": False, "conditionName": "Condition", "operator": "and", "branches": []}, "next": "", "_parent": None, "_branch": None, "_isBranch": t["name"]})
        none = {"id": str(uuid.uuid4()), "parent": t["id"], "order": 1, "name": "None", "type": "if_else", "cat": "conditions", "nodeType": "branch-no",
                "attributes": {"else": True}, "_parent": None, "_branch": None, "_isBranch": t["name"]}
        branch_nodes.append(none)
        ids = [b["id"] for b in branch_nodes]
        for b in branch_nodes: b["sibling"] = [x for x in ids if x != b["id"]]; b["parentKey"] = t["id"]
        t["next"] = ids
        extra.extend(branch_nodes)
    tpl.extend(extra)
    # 2) chains: top level, and per (if_else name, branch name)
    chains = {}
    for t in tpl:
        if t.get("_isBranch"): continue
        chains.setdefault((t["_parent"], t["_branch"]), []).append(t)
    for key, chain in chains.items():
        for a, b in zip(chain, chain[1:]):
            a["next"] = b["id"]; b["parentKey"] = a["id"]
        parent, branch = key
        if parent:
            cond = by_name[parent]
            bnode = next((x for x in tpl if x.get("_isBranch") == parent and x["name"] == branch), None)
            if bnode is None: raise SystemExit(f"branch '{branch}' not found on if_else '{parent}'")
            bnode["next"] = chain[0]["id"]
            chain[0]["parentKey"] = bnode["id"]
            for c in chain: c["parent"] = bnode["id"]
    for t in tpl:
        for k in ("_parent", "_branch", "_isBranch"): t.pop(k, None)
        if t["type"] == "if_else" and t.get("nodeType") in ("branch-yes", "branch-no") and not t.get("next"): t.pop("next", None)
    return tpl


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    add_target_args(ap)
    ap.add_argument("--spec", required=True)
    ap.add_argument("--only")
    args = ap.parse_args()
    t = resolve(args); H = hdrs(); loc = t.location_id
    spec = json.load(open(args.spec))
    wfs = spec["workflows"] if isinstance(spec, dict) else spec

    r = requests.get(f"{BACKEND}/workflow/{loc}/list", headers=H, params={"limit": 200, "offset": 0}, timeout=45)
    r.raise_for_status()
    existing = {norm(x["name"]): (x.get("_id") or x.get("id")) for x in r.json().get("rows", []) if x.get("type") != "directory"}
    print(f"{B}{len(wfs)} workflows in spec, {len(existing)} in account{X}  ({'LIVE' if t.live else 'dry run'})\n")

    # pass 1: make sure every spec workflow has a shell so {{wf:Name}} can resolve
    if t.live:
        for w in wfs:
            if existing.get(norm(w["name"])): continue
            body = {"name": w["name"], "status": "draft", "parentId": w.get("parentId"), "updatedBy": None, "modifiedSteps": [],
                    "workflowData": {"templates": []}, "deletedSteps": [], "createdSteps": [], "senderAddress": {},
                    "stopOnResponse": w.get("settings", {}).get("stopOnResponse", False), "allowMultiple": True,
                    "allowMultipleOpportunity": True, "autoMarkAsRead": False, "eventStartDate": "", "timezone": "",
                    "triggersChanged": False, "company_id": COMPANY, "company_age": 5}
            c = requests.post(f"{BACKEND}/workflow/{loc}", headers=H, data=json.dumps(body), timeout=45)
            if c.ok: existing[norm(w["name"])] = c.json()["id"]; print(G + f"  shell created: {w['name']} -> {c.json()['id']}" + X); time.sleep(0.4)
            else: print(R + f"  shell failed: {w['name']} {c.status_code} {c.text[:160]}" + X)

    def resolve_refs(obj):
        if isinstance(obj, dict):
            for k, v in obj.items(): obj[k] = resolve_refs(v)
            return obj
        if isinstance(obj, list): return [resolve_refs(v) for v in obj]
        if isinstance(obj, str) and obj.startswith("{{wf:") and obj.endswith("}}"):
            ref = obj[5:-2]; rid = existing.get(norm(ref))
            if not rid: print(Y + f"      unresolved workflow ref: {ref}" + X); return obj
            return rid
        return obj

    for w in wfs:
        name = w["name"]
        if args.only and norm(name) != norm(args.only): continue
        tpl = resolve_refs(build_templates(w["steps"]))
        wid = existing.get(norm(name))
        print(f"{B}  {name}{X}  {len(tpl)} steps, {len(w.get('triggers', []))} triggers  {'(update)' if wid else '(create)'}")
        for s in tpl: print(f"      {D}{s['type']:22}{X} {s['name'][:60]}")
        for tr in w.get("triggers", []): print(f"      {Y}trigger{X} {tr['type']:24} {tr.get('name','')[:50]}")
        if not t.live: continue

        if not wid:
            body = {"name": name, "status": "draft", "parentId": w.get("parentId"), "updatedBy": None, "modifiedSteps": [],
                    "workflowData": {"templates": []}, "deletedSteps": [], "createdSteps": [], "senderAddress": {},
                    "stopOnResponse": w.get("settings", {}).get("stopOnResponse", False), "allowMultiple": True,
                    "allowMultipleOpportunity": True, "autoMarkAsRead": False, "eventStartDate": "", "timezone": "",
                    "triggersChanged": False, "company_id": COMPANY, "company_age": 5}
            c = requests.post(f"{BACKEND}/workflow/{loc}", headers=H, data=json.dumps(body), timeout=45)
            if not c.ok: print(R + f"      create failed {c.status_code} {c.text[:200]}" + X); continue
            wid = c.json()["id"]; print(G + f"      created {wid}" + X)
            time.sleep(0.5)

        # triggers: create any not already present (by name)
        g = requests.get(f"{BACKEND}/workflow/{loc}/trigger", headers=H, params={"workflowId": wid}, timeout=45)
        old = g.json() if g.ok else []
        old = old if isinstance(old, list) else old.get("triggers", [])
        have = {norm(x.get("name")) for x in old}
        new = list(old)
        for tr in w.get("triggers", []):
            if norm(tr.get("name")) in have: continue
            body = {**tr, "status": "draft", "workflowId": wid, "schedule_config": tr.get("schedule_config", {}),
                    "masterType": tr.get("masterType", "highlevel"), "actions": [{"workflow_id": wid, "type": "add_to_workflow"}],
                    "active": True, "triggersChanged": True, "location_id": loc, "company_id": COMPANY, "company_age": 5}
            p = requests.post(f"{BACKEND}/workflow/{loc}/trigger", headers=H, data=json.dumps(body), timeout=45)
            if not p.ok: print(R + f"      trigger failed {p.status_code} {p.text[:200]}" + X); continue
            tid = p.json()["id"]; print(G + f"      trigger {tr['type']} -> {tid}" + X)
            att = {k: v for k, v in body.items() if k not in ("triggersChanged", "company_id", "company_age")}; att["id"] = tid
            new.append(att)

        # steps + attach triggers
        d = requests.get(f"{BACKEND}/workflow/{loc}/{wid}", headers=H, params={"includeScheduledPauseInfo": "true"}, timeout=45).json()
        prev_ids = [s["id"] for s in d.get("workflowData", {}).get("templates", [])]
        d["name"] = name
        d["workflowData"] = {"templates": tpl}
        for k, v in w.get("settings", {}).items(): d[k] = v
        d.update({"modifiedSteps": [], "createdSteps": [s["id"] for s in tpl], "deletedSteps": prev_ids,
                  "triggersChanged": True, "oldTriggers": old, "newTriggers": new,
                  "permissionMeta": {"canRead": True, "canWrite": True}, "scheduledPauseDates": d.get("scheduledPauseDates", [])})
        p = requests.put(f"{BACKEND}/workflow/{loc}/{wid}", headers=H, data=json.dumps(d), timeout=60)
        if p.ok: print(G + f"      PUT {p.status_code} version {p.json().get('version')}  status={p.json().get('status')}" + X)
        else: print(R + f"      PUT {p.status_code} {p.text[:300]}" + X)
        time.sleep(0.6)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
