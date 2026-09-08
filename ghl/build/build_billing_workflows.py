#!/usr/bin/env python3
"""Generate the billing workflows spec (for build_workflows.py) from a client's billing ids.

Reads snapshots/event-rental/clients/<slug>-billing-ids.json (from deploy_billing.py) plus the location's
Package Interest field id, sender user and pipeline stage ids, and writes a build_workflows spec with:
  31. Quote Sent - Send Estimate by Package     stage -> "Quote Sent / Follow-Up": branch on Package Interest, send the tier's estimate
  32. Quote Accepted - Agreement                estimate accepted (any quote template): tag + send agreement + stage Agreement Sent
  33. Agreement Signed - Deposit Invoice        tag book-agreement-signed: branch on Package Interest, send the tier's deposit invoice
  34. Balance Invoice - 7 Days Out              tag book-balance-due (added by 7. Pre-Event Readiness at 7 days): branch, send balance invoice
Every branch has a "None" fallback that sends an internal SMS so nothing is silently skipped.

  python build/build_billing_workflows.py --target riverside --user <userId> --out snapshots/event-rental/clients/riverside-billing-workflows.json
"""
from __future__ import annotations
import argparse, json, os
import requests
from ghl_target import add_target_args, resolve

SVC = "https://services.leadconnectorhq.com"


def cf_condition(field_id, value):
    return {"conditionType": "contact_detail", "conditionSubType": field_id, "conditionOperator": "==", "conditionValue": value, "__customFieldType__": "standard"}


def branches(tiers, field_id, cond_name):
    return {"currentRecipeType": "CUSTOM", "conditionName": cond_name, "branches": [
        {"name": t["label"], "segments": [{"operator": "or", "conditions": [cf_condition(field_id, t["package_interest"])]}]} for t in tiers.values()]}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    add_target_args(ap); ap.add_argument("--user", required=True, help="sender user id (owner)"); ap.add_argument("--out", required=True)
    a = ap.parse_args(); t = resolve(a); loc = t.location_id
    H = {"Authorization": f"Bearer {t.token}", "Version": "2021-07-28"}
    ids = json.load(open(f"snapshots/event-rental/clients/{a.target}-billing-ids.json")); tiers = ids["tiers"]
    fields = requests.get(f"{SVC}/locations/{loc}/customFields", headers=H, timeout=45).json()["customFields"]
    pkg = [f["id"] for f in fields if f["name"] == "Package Interest"][0]
    pipe = requests.get(f"{SVC}/opportunities/pipelines", headers=H, params={"locationId": loc}, timeout=45).json()["pipelines"][0]
    stage = {s["name"]: s["id"] for s in pipe["stages"]}
    quote_stage = [v for k, v in stage.items() if k.startswith("Quote Sent")][0]
    agree_stage = [v for k, v in stage.items() if k.startswith("Agreement Sent")][0]
    doc_tpl = requests.get(f"{SVC}/proposals/templates", headers={**H}, params={"locationId": loc}, timeout=45)
    agreement = None
    if doc_tpl.ok:
        for d in doc_tpl.json().get("data", doc_tpl.json().get("templates", [])):
            if "Agreement" in d.get("name", ""): agreement = d.get("_id") or d.get("id")
    docs = {}; skip = 0
    HT = {"token-id": os.environ.get("GHL_TOKEN_ID", ""), "channel": "APP", "source": "WEB_USER", "Version": "2021-07-28"}
    while True:
        r = requests.get(f"{SVC}/proposals/templates", headers=HT, params={"locationId": loc, "limit": 20, "skip": skip}, timeout=45).json()
        pg = r.get("data", []) if isinstance(r, dict) else r
        for d in pg: docs[d.get("name")] = d.get("_id")
        if len(pg) < 20: break
        skip += 20
    proposal = docs.get("Corporate Event Proposal")
    inv = lambda tpl: {"type": "payments_create_invoice", "workflowsActionType": "INTERNAL", "attributes": {"userId": a.user, "templateId": tpl, "liveMode": "true", "action": "sms_and_email", "type": "payments_create_invoice"}}
    est = lambda tpl: {"type": "payments_create_estimate", "workflowsActionType": "INTERNAL", "attributes": {"userId": a.user, "templateId": tpl, "liveMode": "true", "sendMode": "sendDirectly", "action": "sms_and_email", "type": "payments_create_estimate"}}
    sms_internal = lambda body: {"type": "internal_notification", "attributes": {"type": "sms", "sms": {"userType": "custom_sms", "body": body, "to": "{{custom_values.internal_notification_phone}}", "attachments": []}}}
    def branched(name, cond_name, maker, kind):
        steps = [{"name": "1 - Which package?", "type": "if_else", "attributes": branches(tiers, pkg, cond_name)}]
        for key, tr in tiers.items():
            steps.append({"name": f"2 - {kind}: {tr['label']}", "parent": "1 - Which package?", "branch": tr["label"], **maker(tr[kind if kind != "quote" else "estimate"])})
        if kind == "quote" and proposal:
            steps[0]["attributes"]["branches"].append({"name": "Corporate / Custom", "segments": [{"operator": "or", "conditions": [cf_condition(pkg, "Corporate / Custom")]}]})
            steps.append({"name": "2 - Document: Corporate Event Proposal", "parent": "1 - Which package?", "branch": "Corporate / Custom", "type": "proposals_estimates_send_document", "workflowsActionType": "INTERNAL", "attributes": {"userId": a.user, "templateId": proposal, "sendDocument": "true", "medium": "email", "type": "proposals_estimates_send_document"}})
            steps.append({"name": "3 - Task: build the corporate quote", "parent": "1 - Which package?", "branch": "Corporate / Custom", "type": "task-notification", "attributes": {"type": "task_notification", "title": "Corporate quote - {{contact.name}} {{contact.event_date}}", "body": "<p>The proposal went out automatically. Open the contact, send the 'Quote - Corporate (custom)' estimate after trimming the add-on lines to what they asked for.</p>", "assignedTo": a.user, "dueDate": {"duration": 1, "unit": "days", "skipWeekends": False}}})
        steps.append({"name": "2 - Package not set: tell the owner", "parent": "1 - Which package?", "branch": "None", **sms_internal(f"{{{{contact.name}}}}: Package Interest is blank, so no {kind} was sent automatically. Send it by hand from the contact.")})
        return steps
    wfs = [
        {"name": "31. Quote Sent - Send Estimate by Package", "settings": {"status": "published"},
         "triggers": [{"type": "pipeline_stage_updated", "masterType": "highlevel", "name": "Stage: Quote Sent / Follow-Up", "schedule_config": {}, "conditions": [{"operator": "==", "field": "opportunity.pipelineId", "value": pipe["id"], "title": "Pipeline", "type": "select"}, {"operator": "==", "field": "opportunity.pipelineStageId", "value": quote_stage, "title": "Stage", "type": "select"}]}],
         "steps": branched("31", "Which package", est, "quote")},
        {"name": "32. Quote Accepted - Agreement", "settings": {"status": "published"},
         "triggers": [{"type": "estimate_update", "masterType": "internal", "workflowsTriggerType": "INTERNAL", "name": "Estimate accepted", "schedule_config": {}, "conditions": [{"operator": "==", "field": "status", "value": "accepted", "title": "Estimate Status", "type": "select", "id": "status"}]}],
         "steps": [{"name": "1 - Tag: book-quote-accepted", "type": "add_contact_tag", "attributes": {"tags": ["book-quote-accepted"]}},
                   {"name": "2 - Stage: Agreement Sent", "type": "create_opportunity", "attributes": {"type": "create_opportunity", "pipeline_id": pipe["id"], "opportunity_name": "{{contact.name}}", "opportunity_source": "{{contact.source}}", "monetary_value": "{{contact.quoted_amount}}", "pipeline_stage_id": agree_stage, "opportunity_status": "open", "fields": []}},
                   {"name": "3 - SMS: quote accepted, agreement coming", "type": "sms", "attributes": {"type": "sms", "body": "Great news, {{contact.first_name}} - your quote for {{contact.event_date}} is accepted. The agreement is on its way; once it's signed we'll send the deposit invoice and lock in the date."}}]
                  + ([{"name": "4 - Document: Event Rental Agreement", "type": "proposals_estimates_send_document", "workflowsActionType": "INTERNAL", "attributes": {"userId": a.user, "templateId": agreement, "sendDocument": "true", "medium": "email", "type": "proposals_estimates_send_document"}}] if agreement else [])},
        {"name": "33. Agreement Signed - Deposit Invoice by Package", "settings": {"status": "published"},
         "triggers": [{"type": "contact_tag", "masterType": "highlevel", "name": "Tag added: book-agreement-signed", "schedule_config": {}, "conditions": [{"operator": "index-of-true", "field": "tagsAdded", "value": "book-agreement-signed", "title": "Tag Added", "type": "select", "id": "tag-added"}]}],
         "steps": branched("33", "Which package", inv, "deposit")},
        {"name": "34. Balance Invoice - 7 Days Out", "settings": {"status": "published"},
         "triggers": [{"type": "contact_tag", "masterType": "highlevel", "name": "Tag added: book-balance-due", "schedule_config": {}, "conditions": [{"operator": "index-of-true", "field": "tagsAdded", "value": "book-balance-due", "title": "Tag Added", "type": "select", "id": "tag-added"}]}],
         "steps": branched("34", "Which package", inv, "balance")},
    ]
    json.dump({"_source": f"Generated by build/build_billing_workflows.py for {a.target}; do not edit, regenerate.", "workflows": wfs}, open(a.out, "w"), indent=1)
    print(f"wrote {a.out}: {len(wfs)} workflows, agreement template {agreement}, package field {pkg}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
