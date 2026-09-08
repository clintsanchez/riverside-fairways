# Mobile Event Rental — GHL Snapshot Template

A reusable GoHighLevel snapshot for **single-asset, date-based mobile event
rental**: mobile golf simulators, photo booths, 360 booths, mobile bars, axe
throwing trailers, arcade/game trailers, inflatables.

Built in `ZZ-TEMPLATE Mobile Event Rental` (`SdgdulZOPTsu8bEZYnzN`), seeded from
client **Riverside Fairways** (mobile golf simulator, Denham Springs LA).

Build log, API findings and decisions: **[PROJECT.md](PROJECT.md)**
Trade research (534 lines, ~90 sources): **[research/trade-research.md](research/trade-research.md)**

---

## What ships in the snapshot

| Asset | Count | Notes |
|---|---:|---|
| Custom fields | 34 (41 w/ base) | event, venue/logistics, quote/booking, source |
| Custom values | 59 (68 w/ base) | **all empty** — the client-swappable brand layer |
| Tags | 60 (72 w/ base) | `book-` `risk-` `qual-` `src-` `ops-` `event-` `pkg-` prefixes |
| Calendars | 4 | 3 consult + 1 **internal-only** unit booking calendar |
| Equipment resource | 1 | qty = units owned; **this is the double-booking guard** |
| Knowledge base | 39 FAQs | 10 categories, every operator fact a merge field |
| Conversation AI | 1 agent | suggestive mode, SMS, 39 hard NEVER rules |
| Pipeline | 12 stages | spec only — no write API |
| Workflows | 14 | spec only — no write API |

## Two structural decisions

**1. Double-booking is prevented by a calendar equipment resource, not workflow logic.**
`POST /calendars/resources/equipments` with `quantity` = units owned, bound to a
`service_booking` calendar. GHL then refuses the overlapping booking natively. A
single-asset operator has *no recovery* from a double-book — there is no second
unit to send.

**2. Operator-controlled booking. Customers cannot self-book the event date.**
Leads *request* a date, the operator confirms against the unit calendar, and only
then does the deposit invoice go out. This is the template default, per the
client's explicit requirement (2026-09-02) and because availability depends on
travel time and setup windows a booking widget cannot judge.

The consult calendars *are* customer-bookable — a 20-minute call costs the
operator nothing physical.

## The three-state hold

The most important thing this template gets right, straight from the research:

```
Quote Sent  →  Agreement Signed  →  Deposit Paid
   ↓                 ↓                    ↓
not held         not held           DATE HELD
```

Operators routinely believe a date is held at stage 1 or 2. Each is its own
pipeline stage so an unsigned agreement cannot hide inside "follow-up".

## Layout

```
config/           JSON specs for everything deployed via API
deploy.py         fields + values + tags (dry-run by default, --apply to write)
deploy_calendars.py  calendars + the equipment resource
deploy_kb.py      knowledge base + 39 FAQs
deploy_agent.py   Conversation AI agent
research/         sourced trade research + the 39-item MUST-NOT-STATE list
```

## Running the deployers

Credentials come from `../../.env` — never hardcoded, never committed. All
deployers are idempotent and guarded by a hardcoded `LOCK_LOCATION`; they abort
if the env location doesn't match.

```bash
python3 deploy.py                 # dry run
python3 deploy.py --apply         # write
python3 deploy_calendars.py --apply
python3 deploy_kb.py --apply
python3 deploy_agent.py --apply
```

## Known API limits (tested, not assumed)

| Asset | Writable? |
|---|---|
| Custom fields / values / tags | ✅ |
| Calendars + **equipment resources** | ✅ |
| Knowledge base + FAQs | ✅ |
| Conversation AI agent | ✅ |
| Contact custom-field **folders** | ❌ `/custom-fields/folder` is custom-object shaped |
| **Workflows** | ❌ read-only |
| **Pipelines** | ❌ no endpoints at all |
| **Funnels / forms / surveys** | ❌ |
| **Snapshots** | ❌ create is UI-only; API has share-link only |

Gotchas that each cost a failed apply:
- Tags reject a `locationId` in the body (422)
- `MONETARY` is spelled **`MONETORY`** in GHL's enum
- API-created sub-accounts have **zero users**, and a calendar with no team
  member is rejected `"No team member found"`
- GHL derives custom-value `fieldKey`s itself and they don't always match the
  name — `Add-On Package Name` → `addon_package_name`. **Validate before
  shipping copy that depends on them.**
- `POST /conversation-ai/agents` requires `personality` and `goal` as separate
  fields and rejects any unknown property

## Deploying to a client

1. Push the snapshot into the new sub-account
2. **Fill the REQUIRED custom values** (marked `_req` in `config/custom_values.json`).
   Blank fields degrade the AI to handoffs — safe, but useless.
3. Set the equipment resource `quantity` to the units they actually own
4. **Verify the EVENT - Unit Booking widget is unpublished** — a stranger taking
   a Saturday in October is the failure mode
5. Assign users to all four calendars, set real working hours
6. Rename the Package Interest field options to their actual package names
7. Build the 14 workflows in the UI (see `config/workflows.json`, build order at
   the bottom)
8. Rename pipeline stages per `config/pipeline.json`; delete the Solar pipeline
9. Run the KB website crawler against **that client's** URL — never in the template
10. Connect payments; confirm whether balance capture is manual (it usually is)

## Caveats

- **The AI ships in suggestive mode.** It discusses dates, money, insurance and
  weather on behalf of an operator whose year is ~50 Saturdays. Move it to
  auto-pilot only after weeks of reviewed drafts.
- **Do not run the KB crawler in the template account.** Crawling one client's
  site bakes that business into every future deployment.
- The seasonality month-model in the research is an explicit **hypothesis** —
  validate against the operator's own booking history.
- Deposit/cancellation figures in the research are `[operator-sampled]`, not
  standards. Nothing is hard-coded as a default.
