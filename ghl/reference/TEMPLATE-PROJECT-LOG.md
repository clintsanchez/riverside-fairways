# GHL Snapshot Builder — Mobile Event Rental Template

## Goal
A reusable GHL snapshot for single-asset, date-based mobile event rental,
seeded from client Riverside Fairways (mobile golf simulator, Denham Springs LA).

## Scratch sub-account
- Name: `ZZ-TEMPLATE Mobile Event Rental`
- Location ID: `SdgdulZOPTsu8bEZYnzN`
- Base snapshot: `Hw09k7a4AYnbUeyfb9w1` (Home Services Snapshot - Skool [v0])
- Created: 2026-09-03 via `POST /locations/` with `snapshotId`

## Auth
`../../.env` → `GHL_AGENCY_PIT` + `GHL_COMPANY_ID` (agency-level, for snapshots
and sub-account create) and `GHL_PIT_TEMPLATE_EVENT` (location PIT, for
everything inside the account). Base `https://services.leadconnectorhq.com`,
header `Version: 2021-07-28`.

The agency PIT **cannot** write assets inside a sub-account — every
`/locations/{id}/*` call returns 401 `"token is not authorized for this scope"`.
A location PIT is mandatory for the deploy layer.

## Scope decision
The brief asked for a bounce-house / spacewalk party rental snapshot. Riverside
Fairways is a **mobile golf simulator** business — one unit, tiered time
packages, no inflatables catalog. Scoped to **Mobile Event Rental** (single
asset delivered to a venue) so the template genuinely fits the client while
staying reusable across photo booths, 360 booths, mobile bars, axe throwing and
inflatables. The catalog layer became packages + add-ons rather than an
inventory list.

## Base snapshot inventory (verified 2026-09-03)
Push completed, zero pending. Identical to what the patio-gutter build found.

KEEP (cannot be rebuilt via API — this is why we clone):
- Pipeline "Sales Pipeline" `zXP0R6qnjGEskUroY9M6`: Lead → Hot Lead → Scheduled
  Appointment → No Show → Got Estimate & Follow-Up → Sale → Request Review
- Workflows 1-8 plus 2 Facebook Conversion API workflows, all published

DELETE (wrong trade):
- Pipeline "Solar Leads or Plumbers" `HmV7LgblqAkDxsxSV7m9` (13 solar stages)
- Calendars "ABC Solar", "ABC HVAC"

REBUILD: 7 generic custom fields, 9 empty custom values, 12 generic tags.

## Two structural decisions

**1. Equipment resource = the double-booking guard.**
`POST /calendars/resources/equipments` with `quantity` = units owned, bound via
`calendarIds` to a `service_booking` calendar. GHL refuses the overlapping
booking natively. Deployed and verified: `Primary Rental Unit`, qty 1, bound to
`mpanAhWgmY607yOLYEii`.

Per the spec, one equipment maps to exactly **one** service calendar; multi-unit
operators raise `quantity` rather than creating more resources.

**2. Operator-controlled booking (template default).**
The event calendar is internal-only. Customers request a date; the operator
confirms; the deposit invoice then auto-sends. Driven by the client requirement
(2026-09-02: *"we want to own our calendar and not let people do self booking…
just have the deposit invoice auto send to the customer once we book the date
ourselves"*) and independently supported by the research — availability depends
on soft holds, travel time and setup windows a booking widget cannot judge.

The 20-minute consult calendars remain customer-bookable.

## Research → design (research/trade-research.md, ~90 sources)

| Finding | What changed |
|---|---|
| "Held" is three states, not one | Quote Sent / Agreement Signed / Deposit Paid are three separate pipeline stages. Only the last holds a date. |
| Book the footprint, not the event hours | 90-min buffer on the booking calendar covering setup + teardown + travel |
| Inquiry season ≠ event season | Workflow 14 schedules outbound to *inquiry* season — Dec corporate work sells Aug-Oct |
| Sub-5-min response must *qualify* | Workflow 1 and the AI both collect date/venue/guests/indoor-outdoor/power/COI, not just acknowledge |
| Cadence forks by event type | Event Type field + `event-*` tags drive separate nurture |
| Weather needs its own state | "Weather Hold / At Risk" stage + workflow 8 at T-72h / T-24h / event morning |
| COI has carrier lead time | `COI Requested?` field + `risk-coi-pending` tag chased at T-10 days |
| Anniversary rebooking at T+8mo | Workflow 10, driven by `src-annual-event` + `Annual Event Month` |
| Refund vs rain-check are *opposite* industry defaults | The AI quotes the operator's stored policy verbatim and never paraphrases |

## Verified API capability

DEPLOYED VIA API (all live, zero errors):
- 34 custom fields, 59 custom values (all empty), 60 tags
- 4 calendars + 1 equipment resource
- Knowledge base `Mw89g44WZkNJVfsPiiE9` + 39 FAQs
- Conversation AI agent `zK8w7PhMbVugsYu8eKRh`

NOT DEPLOYABLE (manual UI work, specs written):
- Workflows — GET only, zero writes → `config/workflows.json` (14 specs)
- Pipelines — no endpoints at all → `config/pipeline.json` (12 stages)
- Funnels, forms, surveys — read only
- Contact custom-field **folders** — see below
- Snapshots — create is UI-only

## API findings (each cost a failed apply)

1. **Tags reject `locationId` in the body.** 422 `"property locationId should
   not exist"`. The location is already in the path.
2. **`MONETARY` is spelled `MONETORY`** in GHL's dataType enum. Not a typo on
   our side — it is their enum.
3. **Contact custom-field folders are not API-creatable.**
   `POST /locations/{id}/customFields` has no `parentId`, and
   `POST /custom-fields/folder` is custom-object shaped (needs `objectKey` like
   `custom_object.pet`). All fields land in the default folder; grouping is UI work.
4. **API-created sub-accounts have ZERO users.** `POST /calendars/` then fails
   with `"No team member found"`. Fix: `PUT /users/{id}` adding the location to
   `locationIds` — and that PUT requires `companyId` in the body or it 422s.
   `GET /users/?locationId=` is eventually consistent; check the user record instead.
5. **GHL derives custom-value `fieldKey`s itself and they don't always match the
   name.** `Add-On Package Name` → `addon_package_name`, not `add_on_package_name`.
   Validate every merge field against live `fieldKey`s before shipping copy —
   2 of 22 FAQ merge fields were wrong on first write.
6. **`POST /conversation-ai/agents` requires `personality` and `goal`** as
   separate fields alongside `instructions`, and rejects any unknown property —
   so `_`-prefixed documentation keys must be stripped before POST.

## Template vs per-deployment layers (IMPORTANT)

SHIPS IN SNAPSHOT: 34 trade fields, 60 tags, 4 calendars + equipment resource,
39 client-agnostic FAQs, AI agent with 39 guardrails, 12-stage pipeline spec,
14 workflow specs, **empty** custom values.

PER DEPLOYMENT: fill the REQUIRED custom values; set equipment quantity; verify
the booking widget is unpublished; assign calendar users; rename Package
Interest options; run the KB crawler against **that client's** URL.

Do NOT train the KB crawler in the template account — a crawl of one client's
site would bake their business into every future deployment. (The patio build
caught this mid-crawl.)

## Guardrails
39 MUST-NOT-STATE rules in `research/trade-research.md`, encoded verbatim as
NEVER rules in the AI agent and baked into all 39 FAQ answers. The empirical
case: published axe-throwing minimum ages range **8 to 18** across operators,
and space requirements within one asset class range 30×30 ft to a 45-ft rig. An
AI answering from general knowledge will be confidently wrong.

Meta-rule: **every number in the agent's mouth is a merge field or it doesn't
get said.** A blank merge field degrades to a handoff, never to an invented figure.

## Status

- [x] Create scratch sub-account with base snapshot
- [x] Inspect base inventory
- [x] Trade research + MUST-NOT-STATE list
- [x] Deploy fields / values / tags
- [x] Deploy calendars + equipment resource
- [x] Deploy knowledge base + 39 FAQs
- [x] Deploy Conversation AI agent
- [x] Rename pipeline + stages, delete Solar pipeline (browser + replayed PUT)
- [x] Delete ABC Solar / ABC HVAC calendars (API)
- [x] Workflow layer manual items closed as data (wait types/60-day replaced in the rebuild; workflow 13 call-status filter via trigger PUT). Unit calendar keeps an auto-generated widgetSlug but is not linked anywhere.
- [x] Audit + rewrite 15 inherited email templates (API)
- [x] Repoint 4 trigger links off vendor domain (API)
- [x] Audit + rewrite the 8 inherited workflows via build/patch_workflows.py (53 steps, 0 flags on re-extract)
- [x] Build workflows 2,4,5,6,7,8,9,10,11,12,13 as data (build/build_workflows.py); 1/3/15 are the patched base; 14 is a campaign
- [x] Funnel pages written (funnels/)
- [x] Template cleanup 2026-09-04: base junk deleted as data — 5 forms, 2 surveys, 16 funnels (two folder deletes), 3 calendars (ABC Contractors, Book an Appointment, "Calendar "), 2 Facebook CAPI workflows, the empty "Home Services Workflows" folder
- [x] Re-homed the 8 base-inherited workflows as user-origin copies (`build/clone_workflows.py`) — see "Snapshot finding" below
- [x] Snapshot `Mobile Event Rental v1 (2026-09)` = `kc48mDlFyozpHoW38ukG` (created 2026-09-04 in the agency UI, refreshed as data to v4: 17 workflows, 4 calendars, 1 form, 1 funnel, 81 custom-field entries, 59 custom values, 63 tags, 19 email-template entries, pipeline, AI agent, 2 knowledge bases, dashboard, review settings, contact view)
- [x] Riverside Fairways sub-account `8Dc5dXota6CblTBsNy2k` created from the snapshot via `POST /locations/` (2026-09-04); Clint's user attached; target slug `riverside`
- [x] Riverside: second push (override) delivered all 17 workflows; junk forms/funnels + default Marketing Pipeline removed; equipment qty 1 bound to `jsmbQKFnzGwyt1hBlBEs`; 42 custom values filled
- [x] Riverside: location PIT (`ghl-toolkit`), WordPress embeds live (availability form + Discovery Call calendar), 47 custom values, workflow 13 missed-call filter (snapshot v5)
- [x] Riverside: users, task assignment, calendars activated + owner schedules, end-to-end test PASSED (see the client repo: `riverside-fairways/ghl/DEPLOYMENT.md`)
- [x] Event Rental Agreement (Documents & Contracts) built as data in template + Riverside; sent from workflow 3; workflow 5 triggers on document SIGNED (snapshot v7)
- [ ] Riverside: phone number decision (client), Payment Link, KB crawl; site embeds reverted until the client's own duplicate account exists

## Defects found in the Riverside test — status in the TEMPLATE (snapshot v6)

| Defect | Template fix |
|---|---|
| Task steps unassigned → silently skipped | All 7 task steps assigned to Clint's agency user (present in every sub-account), so tasks are always created; `build/assign_tasks.py --user <owner>` re-points them per client |
| Calendars inactive / no hours after push | Template calendars now active with per-day hours (unit: 7 days 6–23; consults Mon–Sat 8–20). Whether a push carries them is unverified — checklist step 3 still runs |
| Weekend slots missing (user schedules) | Per user, cannot ship in a snapshot — checklist step 3 |
| Call Confirmation fired for unit bookings | Trigger limited to the 3 consult calendars in the template |
| Duplicate stage trigger on workflow 6 | Removed in the template |
| Blank booking link | `Booking Page URL` is a client value — checklist step 4 |
| `ignoreFreeSlotValidation` bypasses guard | GHL behaviour; documented for operators |

## Ported from the Cleaning Services Snapshot (2026-09-04) — snapshot v8

Evaluation: `research/cleaning-snapshot-eval.md`. Built as data, user-origin, our naming:

| # | Workflow | Trigger | Does |
|---|---|---|---|
| 17 | Inbound Message - Notify Operator | any customer reply (SMS, email, FB, GBM, IG, WhatsApp, live chat) | internal SMS with the message; one per contact per day |
| 18 | Opt-Out - STOP or Wrong Number | SMS containing STOP/unsubscribe/wrong number | remove from all workflows, DND all channels, tag `dnd-all`, opportunity lost, alert |
| 19 | Email Bounce or Unsubscribe - DND Email | mailgun unsubscribed / complained / failed | tag `email-undeliverable`, DND email only, alert |
| 20 | SMS Delivery Errors - Alert | carrier error 30003-30034 | tag `sms-error`, alert with plain-English code meaning |
| 21 | Bad or Landline Number - Tag | number validation not_valid / sms_incapable | tag, DND SMS |
| 22 | Consult Cancelled - Reschedule Nudge | consult calendar appointment cancelled | 2 SMS with the booking page |
| 23 | Payment Received | payment succeeded | tag `payment-received` + `book-deposit-paid` (kicks off 6), alert |
| 24 | Payment Failed - Alert | payment failed | retry SMS with payment link, alert, task |
| 25 | Invoice Sent - Awaiting Payment | invoice sent | tag, 2-day nudge to operator |
| 26a-c | Contact Type | contact created / deposit paid / event delivered | contact.type lead→customer, tags `type-lead/-client/-past-client` |
| 27, 27b | Email Engagement | mailgun opened / clicked | tags `email-opened` / `email-clicked` |
| 28 | Past Clients - Monthly Event Ideas | tag `type-past-client` | 5 emails over 12 months (next event, corporate, holidays book early, fundraisers, same date next year) |
| 29a/b | Review Gate | Post-Event Experience Survey happy / unhappy | happy → Google review SMS; unhappy → alert + task, never a public link |

Also: **Post-Event Experience Survey** (`documents`… no: `surveys`, built as data from the source survey: 4-option rating on the new `Event Experience Rating` field, comment on `Your Feedback`, conditional logic, happy path redirects to `Google Review Link`). Workflow 9 now sends `Review Survey Link` instead of the Google link directly. New custom value `Review Survey Link` (per client: `https://api.leadconnectorhq.com/widget/survey/<id>`).

Deferred to pass 3 (UI-only or needs a number): chat widget backed by the booking AI (config not reachable as data), AI voice caller tags/stages, live-chat AI shift.

Builder finding: `if_else` steps need branch nodes as their own `if_else` entries (nodeType branch-yes/None) with the condition node's `next` = list of branch ids. `build_workflows.py` does not do that yet — split logic into trigger-specific workflows instead.

## Post-snapshot checklist (learned from the Riverside test)
1. `build/add_users.py` — create the client's users.
2. `build/assign_tasks.py --user <id>` — task steps are skipped when unassigned.
3. Activate calendars, set `openHours` (one day per entry), recreate the equipment resource, add users to calendars, set user schedules (`PUT /calendars/schedules/{id}`; default schedules are weekdays only).
4. Fill custom values incl. Booking Page URL and Payment Link.
4b. `build/deploy_products.py --spec clients/<client>-products.json` — packages and add-ons as Products with prices (not a snapshot asset).
4c. Set `Review Survey Link` to the client's copy of the Post-Event Experience Survey (`/widget/survey/<id>`).
4d. Open the client's survey copy as data and (i) re-point every rule's `selectedField` at the local `Event Experience Rating` field id, (ii) put the client's literal Google review URL in the `disqualifyLead` rule value and `formAction.disqualifiedUrl`. Query-keyed rules and merge-tag URLs silently do nothing (see BROWSER-RECIPES).
4e. Chat widget: snapshot carries `Event Booking Chat`; PUT `/chat-widget/data/{loc}/{id}` with `config/chat_widget.json` settings, business name/website substituted as literals. Embed code goes on the client's site only once the account is theirs.
4f. Workflow 30 (Live Chat - AI Answers First) references the Conversation AI bot by id; after the push, re-point both `update_conversation_ai_status` steps at the local bot id (`preFetchAssets?assetType=conversation_ai`).
5. Restrict any `appointment` trigger to the right calendars.
6. Run the form → pipeline test with internal notifications pointed at yourself.

## Snapshot finding (2026-09-04) — imported workflows are silently excluded

Any workflow whose document carries `originType: "snapshot"` (it arrived via an
*imported* snapshot — here the Skool Home Services base) is dropped when you
create or refresh your own snapshot. Selection succeeds, the request returns
200, dehydration "completes", and the workflow is simply absent from
`get_assets` and from every sub-account the snapshot is pushed to. The first
push to Riverside delivered 9 of 19 workflows for exactly this reason.
`originType` cannot be changed through the builder PUT. Fix: recreate as
user-origin (`build/clone_workflows.py`), which also repairs the legacy
`parent`/`parentKey`/`next` wiring and strips triggers pointing at deleted
forms. Pipelines, tags, custom values, calendars and email templates from the
base were NOT affected. Full notes: `build/BROWSER-RECIPES.md`.

Consequence for future template builds: start from the imported base for the
*non-workflow* assets, but treat every base workflow as something to rebuild
or clone before the snapshot is cut.

## Open questions for the client
1. ~~Balance due 48 hours or 7 days?~~ **Resolved 2026-09-03: 48 hours.**
   Site patched via Novamira MCP same day (FAQ 6322, page 5839, draft 1628).
2. Payment processor — Square, PayPal or Stripe? All three accounts exist; the
   decision was left open on 2026-09-02.
3. Internal notification address — `jase@` or `info@`?

## Pass 3 additions (2026-09-04) — snapshot v9

- `build_workflows.py` now materialises real if/else branches (condition node + branch-yes/branch-no nodes, `parentKey`/`sibling` wiring) and passes `workflowsActionType: INTERNAL` through for document and Conversation-AI steps.
- Workflow 30 `Live Chat - AI Answers First`: live-chat reply → existing client (tag `type-client`) gets AI off + internal SMS; everyone else gets the Event Booking Assistant switched on, 24 h later handed back.
- Review gate verified end to end in Riverside (happy → `review-positive` + redirect; unhappy → `review-negative` + task) after fixing the survey rules (field id, literal URL). Survey saved as data in `config/review_survey.json`.
- Chat widget `Event Booking Chat` built as data (`config/chat_widget.json`) and included in the snapshot.

## UI layer (2026-09-04) — snapshot v10

- **Owner Dashboard** (`config/dashboard.json`, `build/build_dashboard.py --into default`): 13 widgets — inquiries / booked / won / unread this month, booking funnel, stage distribution, events this month and next month (tables keyed on the Event Date custom field), how people find us, event types, post-event ratings, open pipeline value, tasks. Replaces the stock dashboard's ad reports, GA charts and example tasks in place, so it stays the location default.
- **Custom-field folders** (`config/field_folders.json`, `build/organize_fields.py`): Event Details, Venue & Logistics, Booking & Payment, Post-Event & Feedback, Sales Notes.
- **Contact detail view** (`config/contact_view.json`, `build/apply_contact_view.py`): Event Date, Event Type, Venue, Guest Count, Package, Quoted Amount pinned under the name; folders in the order above; opportunities and appointments first in the side panel.
- All three reference fields, folders and stages by name and are safe to re-run on any client copy. Post-snapshot: run the three scripts against the client (ids are remapped by the snapshot but the dashboard widgets reference them by id, so rebuild rather than trust the copy).

## Brand palette (2026-09-04) — snapshot v11

Six Global Custom Colors (`config/brand_colors.json`, `build/apply_brand_colors.py`): Brand Primary, Brand Secondary, Brand Accent, Text on Primary, Brand Background, Brand Text. They are merge tags (`{{ brandboards.brand_primary }}`) and ship in the snapshot. The Date Request form and the Post-Event survey buttons reference them (`config/brand_tags.json`, `build/apply_brand_tags.py`). Funnels and emails should use the same tags when built (render-time, untested yet).

Post-snapshot: 4g. Set the client's colors in Brand Boards > Global settings (or edit `brand_colors.json` and run the applier with `--force`), then run `apply_brand_tags.py` once so the survey's cached styles pick up the new hex. Keep the six values distinct from each other.

## Funnel pages on the palette (2026-09-04) — snapshot v12

Both Date Request pages now take their colors from the Global Custom Colors (script-applied CSS variables; tags do not resolve inside style blocks) and page 1 gained a review-proof strip (`Average Rating`, `Review Count`, `Google Review Link`) and a six-question FAQ fed by the policy custom values. Pushed to the template and Riverside; verified on the preview URLs. Still per client: domain + publish, logo URL, hero photo, the rating/review-count values.

## Quote-to-deposit billing (2026-09-04) — snapshot v13

Per package tier the account holds an estimate template (the quote), a deposit invoice template (Deposit Percent of the package) and a balance invoice template (`config/billing.json`, `build/deploy_billing.py`, ids in `clients/<slug>-billing-ids.json`). Four generated workflows (`build/build_billing_workflows.py` -> `clients/<slug>-billing-workflows.json`, built with `build_workflows.py`):

| # | Trigger | Does |
|---|---|---|
| 31 | Opportunity enters *Quote Sent / Follow-Up* | if/else on Package Interest -> sends that tier's estimate; None branch texts the owner |
| 32 | Estimate accepted | tag `book-quote-accepted`, stage Agreement Sent, SMS, sends the Event Rental Agreement |
| 33 | Tag `book-agreement-signed` (from 5.) | if/else on Package Interest -> sends the deposit invoice |
| 34 | Tag `book-balance-due` (added by 7. at 7 days out) | if/else on Package Interest -> sends the balance invoice |

Workflow 3 no longer sends the agreement at quote time (32 does, after acceptance); workflow 5's SMS now points at the invoice instead of a payment link. Verified in the template: stage move -> quote #1 ($495); signed tag -> Deposit invoice $247.50; balance tag -> Balance invoice $247.50, all to the right package. Invoices need a payment processor connected on the client account before anyone can pay them.

Post-snapshot: 4h. `deploy_products.py` -> `deploy_billing.py` -> `build_billing_workflows.py --user <owner>` -> `build_workflows.py` on the generated spec. Invoice/estimate templates are not snapshot assets, so this step is required per client. Corporate / custom quotes stay manual (the None branch tells the owner).

Caveats: invoice templates carry no relative due date, so every invoice is due the day after it is sent (deposit: fine; balance: it is sent 7 days out and reads as overdue after a day even though the policy says 2 days before). Template Send Invoice actions also test-verified end to end: stage move -> quote -> Accept -> `book-quote-accepted` + agreement + stage; signed tag -> deposit invoice; balance tag -> balance invoice. Sent invoices can only be voided (`POST /invoices/{id}/void`), never deleted; estimates delete with the body `{altId, altType}`.

## Documents set (2026-09-04) — snapshot v14

| Document | Built by | Sent by |
|---|---|---|
| Guest Waiver (form, signature field, QR code) | `config/waiver_form_spec.json` + `build_form.py`; QR in `clients/<slug>-guest-waiver-qr.png` | guests scan at the setup; **35. Guest Waiver Signed** tags `guest` + `waiver-signed` and pulls them out of lead nurture |
| Venue Requirements Sheet | `config/venue_sheet.json` + `build_document.py` | **36. Qualified - Venue Sheet + COI** on entering Qualified |
| Certificate of Insurance Request | `config/coi_request.json` | 36, only when COI Requested? = Yes, plus a 3-day task for the owner to attach the certificate |
| Event Day Confirmation | `config/event_confirmation.json` | 7. Pre-Event Readiness, right after the 2-days-out wait |
| Quote - Corporate (custom) | `config/billing.json` extra_estimates | manual: owner trims the add-on lines and sends from the contact |

Workflows 35/36 and the workflow-7 patch come from `build/build_docs_workflows.py` (ids resolved by name per location). Verified in the template: waiver submission -> tags; Qualified stage -> COI task created and documents sent. Post-snapshot 4i: build the three documents, the waiver form (with Business Name substituted), run `build_docs_workflows.py --live` then `build_workflows.py` on its output, print the QR.

## Branding pass (2026-09-04) — snapshot v15

All four documents carry a brand header (logo, Color 2 title band, Color 1 rule), brand-colored headings and a footer band with the business contact line, generated from custom values at build time. Both forms carry a logo + title header, rounded fields, Inter labels and a pill button in Brand Primary. Custom values that drive the look: `Logo URL` (use a horizontal logo, SVG is fine), `Color 1`, `Color 2`. Post-snapshot 4j: after setting those three values, rebuild the four documents (`build_document.py --template-id <id>`) and the two forms; the funnel pages and palette already follow.

Polish (later 2026-09-04): section headings carry a 26px top gap, list rows 9px, paragraphs 12px at 1.6 line height; 26px under the logo and a spacer under the title band. New custom value `Owner Photo URL` (Riverside: the team photo of Jase and Christy) renders as a photo sign-off with `Owner Full Name` on the venue sheet, COI request and confirmation. Snapshot v16.

## Documents set, part 2 (2026-09-04) — snapshot v17

| Document | Sent by |
|---|---|
| Corporate Event Proposal (`config/corporate_proposal.json`) | 31, new *Corporate / Custom* branch: proposal goes out on entering Quote Sent, plus a 1-day task to send the trimmed corporate estimate |
| Date Held Confirmation (`config/date_held.json`) | 6. Deposit Paid, right after the "date reserved" text |
| Reschedule Confirmation (`config/reschedule_confirmation.json`) | **37. Rescheduled** on tag `book-rescheduled` (owner adds it after changing Event Date): document, text, tag removed, task to move the unit-calendar block |
| Paid in Full Receipt (`config/paid_receipt.json`) | **38. Balance Paid** on tag `book-balance-paid` (owner adds it, or a future processor flow): Balance Status = Paid, receipt, text |

All eight documents share the brand chrome and the owner-photo sign-off. Riverside's duplicate agreement template (from the v8 add-only push) is deleted; every workflow points at the branded one.

## Sample data pack (2026-09-04)

`build/sample_data.py --target <slug> --live` loads ten demo hosts, one per pipeline stage (New Inquiry through Post-Event), with event dates spread over the next six weeks, realistic venues, packages, guest counts, quoted amounts and lead sources, each with an opportunity. All tagged `sample-data`; `--cleanup` removes them. Loaded in the template so the dashboard, funnel and pipeline read as a working business; not loaded in Riverside (real account). Stage triggers do fire on demo contacts (the addresses are example.com and there are no phones, so nothing reaches a real person).

Knowledge base: both accounts hold the 39-FAQ `Mobile Event Rental Knowledge Base`; the empty "Existing knowledge base" leftovers were deleted. Riverside's site FAQ confirms service area (Louisiana and the Mississippi Gulf Coast), payment methods (cards, Venmo, PayPal) and the 15 x 20 / 12 ft / power requirements already in custom values; it does not state setup time or insurance, so those two values stay blank until the client answers.

Voice AI receptionist: not started. It needs the builder's internal API (browser session), which was unavailable at the end of this session.


## Pre-freeze verification (2026-09-07) — full step-tree scan

Fresh extract of the template account via `build/extract_workflows.py`: **43
workflows, 321 steps**, all published. Supersedes the 2026-09-03 extract, which
held only 10 workflows and could not see 17–38.

| Check | Result |
|---|---|
| `{{location.*}}` merge fields | **7 steps** — see below |
| Base email templates still referenced | none — the 15 inherited Skool templates are orphaned |
| Stale `custom_values.company_*` / `lead_value` / `twillio_*` | 0 |
| Vendor leakage (HomeService.co, Skool, vendor names) | clean |
| Wrong-trade copy (home / roof / solar / HVAC) | clean |
| Phantom offers, fake scarcity | clean |
| Task steps missing an assignee | none |
| Draft / unpublished workflows | none |

**The one real defect.** `{{location.name}}` and `{{location.email}}` appear in
7 email steps. The business profile does **not** travel in a snapshot, so these
render blank in a cloned sub-account — silently, and `15. Nurture - Long Tail`
runs unattended for months.

- `1. New Inquiry - Fast Five` — step *4 - Email: Got your request here's what*
- `15. Nurture - Long Tail` — steps 4, 8, 12, 16, 20, 24 (every email in the sequence)

These were the **`from_name` / `from_email`** sender fields, not body copy — so
in a clone those emails send with a blank From name and a blank From address.

**APPLIED 2026-09-07.** `build/patch_workflows.py --target template-event
--fixes config/workflow_fixes.json --live` — dry run first (7 steps, 2
workflows, nothing else), then live: both PUTs returned 200. Re-extracted
afterwards to verify independently rather than trusting the write:
**zero `location.*` remain across all 43 workflows**, and all 7 steps now read
`{{custom_values.business_name}}` / `{{custom_values.business_email}}`.

Use `patch_workflows.py` for this class of fix, not `build_workflows.py` — the
latter replaces every step from a spec file and would rebuild both workflows
wholesale, risking drift from what is live and tested.

Two housekeeping items before the freeze: delete the 15 orphaned base email
templates, and run `build/sample_data.py --target template-event --cleanup
--live` so the ten demo hosts do not clone into a paying account.

## Email templates: the name-match test was wrong (2026-09-07)

The earlier conclusion that the 15 inherited email templates were "orphaned,
safe to delete" was **wrong, and deleting them would have broken five
workflows.** That conclusion came from matching template *names* against the
workflow step trees. Workflows bind templates by **id**, not name, and the
bodies were rewritten without ever renaming the templates — so the old base
labels survive on live assets.

Cross-referencing ids: **12 of the 15 are actively referenced.**

| Template (old base name) | Actually used by |
|---|---|
| New Lead Confirmation | 1. New Inquiry — *Got your request here's what* |
| Nurture Campaign: Email #1–6 | 15. Nurture - Long Tail — all six emails |
| Appointment Confirmation Email | 2. Call Confirmation — *Your call is confirmed* |
| 24 Hour Appointment Reminder | 2. Call Confirmation — *Your call is tomorrow* |
| 1 Hour Before Appointment Reminder | 2. Call Confirmation — *Your call is in 1 hour* |
| No Show Appointment | 2b. Call No-Show — *We missed each other* |
| Got Estimate / Follow-Up | 3. Date Available — *Your quote for…* |

Genuinely unreferenced: `New Lead Notification`, `New Appointment
Notification`, `Appointment Follow-Up`. Harmless; leave them.

**Rename these 12 to match their workflow step** before the next deployment.
The stale names are what made them look disposable, and will again.

### Open defect: location.* inside the template HTML

The workflow-step fix (sender fields) did **not** reach the template bodies.
All 12 live templates still carry three `location.*` refs each, in the same
three places:

1. header logo — `<img src="{{location.logo_url}}">` → broken image
2. sign-off — `Thanks, {{owner_first_name}}` / `{{location.name}}` → blank line
3. footer — copyright `{{location.name}}`, mailing address `{{location.email}}`

The business profile does not travel in a snapshot, so in a clone every one of
these renders blank or broken. Swap to `custom_values.logo_url`,
`custom_values.business_name`, `custom_values.business_email` (all REQUIRED,
all validated to resolve).

**FIXED 2026-09-07.** The write path already existed: `fix_templates.py` posts
to `POST /emails/builder/data` on the **public** API (PIT auth, no browser
token) — the same call that rewrote these bodies on 09-03.

Root cause was in that script. Its `GLOBAL` rules *introduced* the problem:
`support@homeservice.co -> {{location.email}}`, and several `PER` replacement
strings hard-coded `{{location.name}}`. So re-running it would have reinstated
the defect. Both are now corrected, and three `location.* -> custom_values.*`
rules added to `GLOBAL`.

Applied to all 15 templates (53 occurrences), every one HTTP 201. Re-fetched
the live HTML afterwards to verify rather than trust the writes:
**zero `location.*` across all 15.**

Note the ~83 "MISS" lines in that script's output are expected and harmless —
the `PER` literals matched the original base copy and already ran on 09-03, so
those strings no longer exist. Only the `GLOBAL` rules still find anything.

## The two MANUAL wait-step flags are a false alarm (2026-09-07)

`patch_workflows.py` prints MANUAL against `24 Hours before The appointment` and
`1 Hour before the appointment` in **2. Call Confirmation**. Verified against the
live step tree: **both are already correct.**

```
"type": "appointment",
"appointmentStartAfter": { "when": "before", "type": "hour", "value": 24 }   # and value: 1
```

That is exactly *Until a scheduled date/time > Appointment > Before*. A duration
wait would carry `"type": "minutes"` with no appointment type and no
`when: "before"` — the way `Wait 2hr after` correctly uses `when: "after"`.

The flag is a static `_manual` string in `workflow_fixes.json`, printed
unconditionally as a build-time instruction for whoever assembles the workflow
in the UI. It does not inspect live config, so it will print on every run
forever. Do not re-investigate; do not "fix" these steps.

## Email templates renamed (2026-09-07)

The 12 live templates now carry names that say which workflow step they serve
(map + verification in `config/template_renames.md`). Done by hand in the UI —
there is no rename API, and Playwright could not drive the page either.

Verified after: 12/12 renamed, 3 unreferenced ones untouched, still 15
templates, **all 12 workflow bindings resolve**, and every body is still free of
`location.*`. Renaming is safe precisely because workflows bind by id — the same
fact that made the earlier name-matching test wrong.

## Snapshot v18 frozen (2026-09-07)

**`Mobile Event Rental v18 (2026-09)` = `dT317DkPHCLJxyp3CdqA`**, cut from
`ZZ-TEMPLATE Mobile Event Rental` (`SdgdulZOPTsu8bEZYnzN`). This is the first
snapshot intended to be reusable for a *second* same-vertical client; v1
(`kc48mDlFyozpHoW38ukG`) is what Riverside was built from and stays as its
provenance record.

Note the snapshot list is eventually consistent — v18 did not appear in
`GET /snapshots/` for several minutes after the UI reported it created. Poll,
do not assume the create failed.

What changed since v17:

| | |
|---|---|
| `location.*` in workflow sender fields | 7 steps in workflows 1 and 15 — every email in the long-tail nurture was sending with a blank From name and From address |
| `location.*` in template bodies | 53 occurrences across all 15 templates — header logo, sign-off, footer |
| `fix_templates.py` | its own rules were *introducing* `{{location.email}}` / `{{location.name}}`; corrected so a re-run cannot reinstate the defect |
| Demo data | 15 contacts removed — the 10 tagged `sample-data` plus 5 GHL `(Example)` contacts the cleanup script does not know about |
| Email templates | the 12 live ones renamed to name their workflow step |
| `build_guide.py` | client-agnostic; section 7 is now freeze + generic client-deploy runbook |
| Wait steps | verified already correct — the MANUAL flag is a static note, not a defect |

Riverside (`8Dc5dXota6CblTBsNy2k`) was not touched by any of this work. It still
runs on the v1 lineage and has **not** received the `location.*` fixes.


## Riverside moved out of this repo (2026-09-08)

The client-specific half of the Riverside build now lives in the client's own
repo, **`clintsanchez/riverside-fairways`**, under `ghl/` — deployment log,
client email, billing/docs workflow specs, products, users, waiver QR. Moved
with `git filter-branch` so the 25 commits of history came along.

This repo keeps the **reusable** side: the `ZZ-TEMPLATE Mobile Event Rental`
account, its config, and snapshot `Mobile Event Rental v18 (2026-09)` =
`dT317DkPHCLJxyp3CdqA`.

`clients/` still holds the `template-event-*` files — those describe the
template account, not a client. The builder scripts in `build/` stay here as the
shared source of truth; the client repo vendors copies and its README says to
diff them.
