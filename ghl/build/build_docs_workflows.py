#!/usr/bin/env python3
"""Generate the document workflows spec (build_workflows.py input) for a location, resolving ids by name.

  35. Guest Waiver Signed        form "Guest Waiver" submitted -> tags guest + waiver-signed, contact type lead stays; no messages
  36. Qualified - Venue Sheet    stage "Qualified - Date Checked" -> send Venue Requirements Sheet; if COI Requested? is Yes -> send COI Request + task
Also patches 7. Pre-Event Readiness in place: a "Document: Event Day Confirmation" step right after "7 - Wait until 2 days before event".

  python build/build_docs_workflows.py --target riverside --user <userId> --out snapshots/event-rental/clients/riverside-docs-workflows.json [--live]
"""
from __future__ import annotations
import argparse, json, os, uuid
import requests
from ghl_target import add_target_args, resolve

SVC, BACK = "https://services.leadconnectorhq.com", "https://backend.leadconnectorhq.com"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    add_target_args(ap); ap.add_argument("--user", required=True); ap.add_argument("--out", required=True)
    a = ap.parse_args(); t = resolve(a); loc = t.location_id
    tok = os.environ.get("GHL_TOKEN_ID"); bearer = os.environ.get("GHL_BEARER")
    HT = {"token-id": tok, "channel": "APP", "source": "WEB_USER", "Version": "2021-07-28", "Content-Type": "application/json"}
    HB = {"authorization": f"Bearer {bearer}", "channel": "APP", "source": "WEB_USER", "version": "2021-07-28", "Content-Type": "application/json"}
    docs = {}
    skip = 0
    while True:
        r = requests.get(f"{SVC}/proposals/templates", headers=HT, params={"locationId": loc, "limit": 20, "skip": skip}, timeout=45).json()
        page = r.get("data", r.get("templates", [])) if isinstance(r, dict) else r
        for d in page: docs[d.get("name")] = d.get("_id") or d.get("id")
        if len(page) < 20: break
        skip += 20
    forms = {f["name"]: (f.get("id") or f.get("_id")) for f in requests.get(f"{SVC}/forms/", headers=HT, params={"locationId": loc, "limit": 50}, timeout=45).json()["forms"]}
    fields = {f["name"]: f["id"] for f in requests.get(f"{SVC}/locations/{loc}/customFields", headers=HT, timeout=45).json()["customFields"]}
    pipe = requests.get(f"{SVC}/opportunities/pipelines", headers=HT, params={"locationId": loc}, timeout=45).json()["pipelines"][0]
    qualified = [s["id"] for s in pipe["stages"] if s["name"].startswith("Qualified")][0]
    need = ["Venue Requirements Sheet", "Certificate of Insurance Request", "Event Day Confirmation", "Date Held Confirmation", "Reschedule Confirmation", "Paid in Full Receipt"]
    missing = [n for n in need if n not in docs] + ([] if "Guest Waiver" in forms else ["form Guest Waiver"])
    if missing: raise SystemExit(f"missing in {t.label}: {missing}")
    doc = lambda name: {"type": "proposals_estimates_send_document", "workflowsActionType": "INTERNAL", "attributes": {"userId": a.user, "templateId": docs[name], "sendDocument": "true", "medium": "email", "type": "proposals_estimates_send_document"}}
    wfs = [
        {"name": "35. Guest Waiver Signed", "settings": {"status": "published", "allowMultiple": True},
         "triggers": [{"type": "form_submission", "masterType": "highlevel", "name": "Guest Waiver submitted", "schedule_config": {}, "conditions": [{"operator": "is-any-of", "field": "form.id", "value": [forms["Guest Waiver"]], "title": "Form is", "type": "select"}]}],
         "steps": [{"name": "1 - Tags: guest, waiver-signed", "type": "add_contact_tag", "attributes": {"tags": ["guest", "waiver-signed"]}},
                   {"name": "2 - Remove from nurture (guests are not leads)", "type": "remove_from_workflow", "attributes": {"type": "remove_from_workflow", "includeCurrent": False}}]},
        {"name": "36. Qualified - Venue Sheet + COI", "settings": {"status": "published"},
         "triggers": [{"type": "pipeline_stage_updated", "masterType": "highlevel", "name": "Stage: Qualified - Date Checked", "schedule_config": {}, "conditions": [{"operator": "==", "field": "opportunity.pipelineId", "value": pipe["id"], "title": "Pipeline", "type": "select"}, {"operator": "==", "field": "opportunity.pipelineStageId", "value": qualified, "title": "Stage", "type": "select"}]}],
         "steps": [{"name": "1 - Document: Venue Requirements Sheet", **doc("Venue Requirements Sheet")},
                   {"name": "2 - SMS: venue sheet sent", "type": "sms", "attributes": {"type": "sms", "body": "{{contact.first_name}}, just emailed you a one-page venue sheet (space, power, access). Forward it to the venue and we're set."}},
                   {"name": "3 - COI requested?", "type": "if_else", "attributes": {"currentRecipeType": "CUSTOM", "conditionName": "COI requested", "branches": [{"name": "Yes", "segments": [{"operator": "or", "conditions": [{"conditionType": "contact_detail", "conditionSubType": fields["COI Requested?"], "conditionOperator": "==", "conditionValue": "Yes", "__customFieldType__": "standard"}]}]}]}},
                   {"name": "4 - Document: COI Request", "parent": "3 - COI requested?", "branch": "Yes", **doc("Certificate of Insurance Request")},
                   {"name": "5 - Task: attach the certificate", "parent": "3 - COI requested?", "branch": "Yes", "type": "task-notification", "attributes": {"type": "task_notification", "title": "COI for {{contact.venue_name}} - {{contact.name}} {{contact.event_date}}", "body": "<p>The venue wants a certificate of insurance. The COI Request document went to the host; get the certificate from the carrier naming {{contact.venue_name}} and email it to {{contact.email}} and the venue.</p>", "assignedTo": a.user, "dueDate": {"duration": 3, "unit": "days", "skipWeekends": False}}}]},
    ]
    wfs += [
        {"name": "37. Rescheduled - New Date Confirmation", "settings": {"status": "published", "allowMultiple": True},
         "triggers": [{"type": "contact_tag", "masterType": "highlevel", "name": "Tag added: book-rescheduled", "schedule_config": {}, "conditions": [{"operator": "index-of-true", "field": "tagsAdded", "value": "book-rescheduled", "title": "Tag Added", "type": "select", "id": "tag-added"}]}],
         "steps": [{"name": "1 - Document: Reschedule Confirmation", **doc("Reschedule Confirmation")},
                   {"name": "2 - SMS: new date confirmed", "type": "sms", "attributes": {"type": "sms", "body": "{{contact.first_name}}, your event is now on {{contact.event_date}}. Deposit carried over, everything else unchanged. Confirmation is in your email."}},
                   {"name": "3 - Remove tag: book-rescheduled", "type": "remove_contact_tag", "attributes": {"tags": ["book-rescheduled"]}},
                   {"name": "4 - Task: move the unit calendar block", "type": "task-notification", "attributes": {"type": "task_notification", "title": "Move unit calendar block to {{contact.event_date}} - {{contact.name}}", "body": "<p>Rescheduled. Move the EVENT - Unit Booking block to the new date and update the balance invoice due date if one is out.</p>", "assignedTo": a.user, "dueDate": {"duration": 1, "unit": "days", "skipWeekends": False}}}]},
        {"name": "38. Balance Paid - Receipt", "settings": {"status": "published", "allowMultiple": True},
         "triggers": [{"type": "contact_tag", "masterType": "highlevel", "name": "Tag added: book-balance-paid", "schedule_config": {}, "conditions": [{"operator": "index-of-true", "field": "tagsAdded", "value": "book-balance-paid", "title": "Tag Added", "type": "select", "id": "tag-added"}]}],
         "steps": [{"name": "1 - Field: Balance Status = Paid", "type": "update_contact_field", "attributes": {"type": "update_contact_field", "actionType": "update_field_data", "fields": [{"field": fields["Balance Status"], "value": "Paid", "title": "Balance Status", "type": "select", "date": ""}]}},
                   {"name": "2 - Document: Paid in Full Receipt", **doc("Paid in Full Receipt")},
                   {"name": "3 - SMS: paid in full", "type": "sms", "attributes": {"type": "sms", "body": "All set, {{contact.first_name}} - {{contact.event_date}} is paid in full. Your receipt is in your email. See you there."}}]},
    ]
    json.dump({"_source": f"Generated by build/build_docs_workflows.py for {a.target}; regenerate, do not edit.", "workflows": wfs}, open(a.out, "w"), indent=1)
    print(f"wrote {a.out}: docs {docs}, form {forms['Guest Waiver']}")
    # patch 7. Pre-Event Readiness in place
    r = requests.get(f"{BACK}/workflow/{loc}", headers=HB, params={"limit": 100}, timeout=45).json(); items = r if isinstance(r, list) else r.get("workflows", [])
    for wf_prefix, anchor_prefix, step_name, doc_name in (("7. Pre-Event", "7 - Wait until 2 days", "7b - Document: Event Day Confirmation", "Event Day Confirmation"),
                                                         ("6. Deposit Paid", "5 - SMS: date reserved", "5b - Document: Date Held Confirmation", "Date Held Confirmation")):
        w = [x for x in items if x["name"].startswith(wf_prefix)]
        if not w: print("no workflow", wf_prefix); continue
        d = requests.get(f"{BACK}/workflow/{loc}/{w[0]['id']}", headers=HB, timeout=45).json(); steps = d.get("workflowData", d)["templates"]
        if any(x.get("name", "").startswith(step_name) for x in steps): print(wf_prefix, "already has", step_name); continue
        anchor = [x for x in steps if x.get("name", "").startswith(anchor_prefix)][0]
        new = {"id": str(uuid.uuid4()), "order": anchor["order"] + 1, "name": step_name, "type": "proposals_estimates_send_document", "workflowsActionType": "INTERNAL", "next": anchor.get("next", ""), "parentKey": anchor["id"], "attributes": doc(doc_name)["attributes"]}
        for x in steps:
            if x.get("parentKey") == anchor["id"] and x["id"] != new["id"]: x["parentKey"] = new["id"]
        anchor["next"] = new["id"]; steps.insert(steps.index(anchor) + 1, new)
        if not t.live: print("dry run: would add", step_name); continue
        pr = requests.put(f"{BACK}/workflow/{loc}/{w[0]['id']}", headers=HB, data=json.dumps({"workflowData": {"templates": steps}, "status": d.get("status", "published"), "version": d.get("version"), "name": w[0]["name"], "triggersChanged": False}), timeout=60)
        print(wf_prefix, "patched:", pr.status_code, pr.text[:120] if not pr.ok else "")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
