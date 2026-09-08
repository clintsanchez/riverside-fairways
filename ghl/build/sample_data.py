#!/usr/bin/env python3
"""Sample data pack: realistic demo contacts + opportunities across every pipeline stage so a fresh
account's dashboard, pipeline and contact views look alive on first login. Everything is tagged
`sample-data`; `--cleanup` deletes exactly those contacts (opportunities go with them).
Public API only (location PIT). Workflows do fire on the demo contacts (stage triggers), so the
emails/SMS in the pack use example.com addresses and no phone numbers.

  python build/sample_data.py --target riverside [--live] [--cleanup]
"""
from __future__ import annotations
import argparse, datetime as dt, json, random
import requests
from ghl_target import add_target_args, resolve

BASE = "https://services.leadconnectorhq.com"
G, Y, R, B, X = "\033[32m", "\033[33m", "\033[31m", "\033[1m", "\033[0m"
PEOPLE = [("Maya", "Thompson", "Corporate / Team Building", "Tier 3 - Premium", 60, "Indoor", "Bayou Logistics HQ"),
          ("Derek", "Landry", "Kids Birthday Party", "Tier 1 - Entry", 18, "Outdoor", "Backyard, Denham Springs"),
          ("Priya", "Nair", "Charity / Fundraiser", "Tier 4 - Full Day", 120, "Indoor", "St. Alphonsus Parish Hall"),
          ("Cole", "Bergeron", "Graduation", "Tier 2 - Mid", 35, "Outdoor", "Pavilion, Watson"),
          ("Renee", "Fontenot", "Private Party / Celebration", "Tier 2 - Mid", 30, "Indoor", "The Barn at Oak Ridge"),
          ("Marcus", "Hebert", "Corporate / Team Building", "Corporate / Custom", 90, "Indoor", "Amite Office Park"),
          ("Lauren", "Guidry", "Wedding / Reception", "Tier 3 - Premium", 80, "Indoor", "White Oak Estate"),
          ("Tyler", "Broussard", "Church / School Event", "Tier 2 - Mid", 45, "Indoor", "Live Oak Middle gym"),
          ("Simone", "Duplantis", "Casual Get-Together", "Tier 1 - Entry", 15, "Outdoor", "Backyard, Walker"),
          ("Andre", "Boudreaux", "Corporate / Team Building", "Tier 4 - Full Day", 110, "Indoor", "Plant 2 break hall")]
# (stage name prefix, days from today for the event, quoted amount, extra tags)
STAGES = [("New Inquiry", 21, 495, []), ("Qualified", 28, 1300, ["book-date-available"]), ("Consult Scheduled", 35, 1600, []),
          ("Quote Sent", 40, 900, ["book-quote-sent"]), ("Agreement Sent", 33, 900, ["book-quote-accepted"]), ("Signed", 26, 2100, ["book-agreement-signed"]),
          ("Deposit Paid", 18, 1300, ["book-deposit-paid", "customer"]), ("Booked", 12, 900, ["book-deposit-paid", "book-confirmed", "customer"]),
          ("Event Delivered", -6, 495, ["book-completed", "type-past-client"]), ("Post-Event", -20, 1600, ["book-completed", "review-positive", "type-past-client"])]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    add_target_args(ap); ap.add_argument("--cleanup", action="store_true")
    a = ap.parse_args(); t = resolve(a); loc = t.location_id
    H = {"Authorization": f"Bearer {t.token}", "Version": "2021-07-28", "Content-Type": "application/json"}
    if a.cleanup:
        r = requests.post(f"{BASE}/contacts/search", headers=H, data=json.dumps({"locationId": loc, "pageLimit": 100, "filters": [{"field": "tags", "operator": "contains", "value": ["sample-data"]}]}), timeout=45)
        ids = [c["id"] for c in r.json().get("contacts", [])] if r.ok else []
        print(f"{B}{t.label}{X}: {len(ids)} sample contacts" + ("" if t.live else "  (dry run)"))
        for i in ids:
            if t.live: print("  delete", i, requests.delete(f"{BASE}/contacts/{i}", headers=H, timeout=45).status_code)
        return 0
    fields = {f["name"]: f["id"] for f in requests.get(f"{BASE}/locations/{loc}/customFields", headers=H, timeout=45).json()["customFields"]}
    pipe = requests.get(f"{BASE}/opportunities/pipelines", headers=H, params={"locationId": loc}, timeout=45).json()["pipelines"][0]
    stage = {s["name"]: s["id"] for s in pipe["stages"]}
    print(f"{B}{t.label}{X}: {len(PEOPLE)} demo hosts across {len(STAGES)} stages  ({'LIVE' if t.live else 'dry run'})")
    for (first, last, etype, tier, guests, io, venue), (sname, days, amount, tags) in zip(PEOPLE, STAGES):
        sid = [v for k, v in stage.items() if k.startswith(sname)][0]
        date = (dt.date.today() + dt.timedelta(days=days)).isoformat()
        print(f"  {first} {last:11} {sname:16} {date} ${amount:>6,} {tier}")
        if not t.live: continue
        body = {"locationId": loc, "firstName": first, "lastName": last, "email": f"{first.lower()}.{last.lower()}@example.com", "source": random.choice(["Google", "Facebook", "Referral", "Website"]),
                "tags": ["sample-data", "type-lead"] + tags,
                "customFields": [{"id": fields["Event Date"], "value": date}, {"id": fields["Event Type"], "value": etype}, {"id": fields["Package Interest"], "value": tier}, {"id": fields["Guest Count"], "value": str(guests)},
                                 {"id": fields["Indoor or Outdoor"], "value": io}, {"id": fields["Venue Name"], "value": venue}, {"id": fields["Quoted Amount"], "value": str(amount)}, {"id": fields["How Did You Hear About Us?"], "value": random.choice(["Google", "Facebook", "Friend or family", "Saw you at an event"])}]}
        r = requests.post(f"{BASE}/contacts/", headers=H, data=json.dumps(body), timeout=45)
        if not r.ok: print("   " + R + f"contact {r.status_code} {r.text[:120]}" + X); continue
        cid = r.json()["contact"]["id"]
        o = requests.post(f"{BASE}/opportunities/", headers=H, data=json.dumps({"pipelineId": pipe["id"], "locationId": loc, "name": f"{first} {last} - {etype}", "pipelineStageId": sid, "status": "won" if sname in ("Event Delivered", "Post-Event") else "open", "contactId": cid, "monetaryValue": amount}), timeout=45)
        print("   " + (G if o.ok else R) + f"contact {cid} opportunity {o.status_code}" + X)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
