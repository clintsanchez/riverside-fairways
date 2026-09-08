# Riverside Fairways — deployment sheet

Mobile golf simulator rental, Denham Springs LA. The client this template was
seeded from.

**Sub-account: `Riverside Fairways` = `8Dc5dXota6CblTBsNy2k`** — created
2026-09-04 via `POST /locations/` from snapshot `kc48mDlFyozpHoW38ukG`
(Mobile Event Rental v1, refreshed to v4 with all 17 workflows). Target slug
`riverside` (`GHL_LOCATION_ID_RIVERSIDE` + `GHL_PIT_RIVERSIDE` in `.env`; Private
Integration `ghl-toolkit`, all scopes, created 2026-09-04).

## End-to-end test (2026-09-04) — PASSED after fixes

Test contact submitted the live site form → contact + fields + tag → workflow 1
(email, Jase SMS, follow-up SMS with booking link) and workflow 2 (internal
SMS/email, task) → stage moves/tags drove 3, 4, 5, 6, 12, 2b, 16 → unit
calendar booked, double-booking guard verified (overlaps + 90-min buffer
rejected, gap accepted). Test data deleted; client notification values restored.

Fixed during the test (all applied to Riverside; template where it applies):
- Task steps had no assignee → GHL silently skipped them. Assigned to Jase (`build/assign_tasks.py`).
- All 4 calendars arrived **inactive** with no hours; activated, hours set.
- Owners' weekly schedules defaulted to weekdays → no weekend slots. Unit calendar: 7 days 8 AM–11 PM for Jase + Christy; default schedules (consult calendars): Mon–Sat 8 AM–8 PM.
- "2. Call Confirmation" fired on unit bookings → trigger now limited to the 3 consult calendars.
- Workflow 6 had a duplicate stage trigger → removed.
- Workflow 13 missed-call filter added. Booking Page URL filled (links were blank).

Still open from the test:
- **No phone number** — SMS went out from a shared +1 289 number and later `failed`. Clint holding until the client decides (buy 225 LC number / port / A2P).
- Payment Link empty → "Pay here:" SMS has no link until the processor is chosen.
- Do not book the unit with "ignore availability" — it bypasses the equipment guard.

## Agreement (2026-09-04)

`Event Rental Agreement` Documents & Contracts template, built as data from
`config/agreement.md` (`build/build_document.py`). Riverside copy
`6a9adadf3a5753990282661f`; template copy `6a9ad8483a575399028211bd` (in snapshot v7).
Terms per Clint: deposit non-refundable; balance refundable 7+ days out, full
total due inside 7 days; free reschedule 7+ days out, $175 fee inside, deposit
credited 12 months. Host signature + date + printed name fields; business
countersignature not included (add in UI if Jase wants to countersign).
Verified rendered on sendlink.co with Riverside's values.

Wiring: workflow 3 step `3b - Document` sends it from Jase right after the quote
email; workflow 5 now also triggers on **document status SIGNED for this
template** (in addition to the `book-agreement-signed` tag), so signing starts
the deposit sequence automatically.

## Deployment log (2026-09-04)

| Done | Item |
|---|---|
| x | 34 workflows published (snapshot v8 pushed add-only 2026-09-04: guardrails 17-25, contact type 26a-c, engagement 27, monthly event ideas 28, review gate 29a/b) all on Riverside's own ids |
| x | Post-Event Experience Survey (own copy) + `Review Survey Link` set; workflow 9 sends the survey, happy answers redirect to Google |
| x | Pipeline `Event Bookings` (12 stages); GHL's default `Marketing Pipeline` deleted |
| x | 4 calendars incl. `EVENT - Unit Booking (INTERNAL)` = `jsmbQKFnzGwyt1hBlBEs` |
| x | Equipment resource `Primary Rental Unit`, **qty 1**, bound to the unit calendar |
| x | Form `Date Request` + funnel `Date Request` (2 pages); base junk forms/funnels removed |
| x | 47 custom values filled — sheet below plus verbatim FAQ wording for Weather Policy Summary, Payment Methods Accepted, Booking Lead Time; Facebook/Instagram URLs |
| x | Workflow 13 trigger now filters Call Status = no-answer (template + Riverside, snapshot v5) |
| x | Clint's agency user attached |
| x | Users: Jase (jase@) and Christy (info@) created as account admins (`build/add_users.py`, invites emailed); both on every calendar |
| | Knowledge-base crawl of riversidefairways.com inside *this* account |
| | Custom values still empty and why: **Cancellation / Reschedule Policy Summary** — the site's Booking & Cancellation Policy (post 1628) is a DRAFT with `[[REFUND TERMS]]` placeholders, so the client has not decided these; Google Review Link (GBP pending); Insurance Statement; Setup Time Required; Years In Business; Peak Season Note; Logo URL; Colors; Payment Link; Agreement / Contract Link; Booking Page URL; Referral / Repeat offers |
| | Note: policy draft says equipment is *not* weatherproof; the live FAQ says *fairly* weatherproof. Loaded the FAQ (published) wording; client should reconcile |
| | `Internal Notification Email` set to **info@riversidefairways.com** pending Jase-vs-info confirmation |
| ~ | WordPress embeds were live for the test, then **reverted 2026-09-04 on Clint's instruction** (`/forms/availability/` back to `[ws_form id="6"]`, `/forms/consultation/` back to original). Reason: this sub-account is the source for the snapshot; the client gets a duplicate later, and the site will be wired to *that* account's form/calendar ids. Embed code pattern is in the recipes. WS Form 6 actions (re-checked, earlier note was wrong): notification email from no-reply@riversidefairways.com to **info@ and jase@** (reply-to = submitter), a **confirmation email to the submitter** from no-reply@, Show Message, Save Submission, redirect to `/confirmation/availability/`. Updated 2026-09-04 as data via the WS Form PHP API and republished. |
| | Funnel domain (client side) before `/request-a-date` is public |
| | **DNS: add SPF** at GoDaddy for riversidefairways.com (no SPF today, DMARC is `p=quarantine`, MX is Google). TXT @ = `v=spf1 include:_spf.google.com include:_spf.wpengine.com ~all`. Test mail from the WP Engine server reached Clint's inbox on 2026-09-04, but without SPF that is luck, not policy. |

Sources: [riversidefairways.com](https://riversidefairways.com), their pricing,
FAQ and event-safety pages, and the Christy/Jase text thread (Jul 31 – Sep 2 2026).

---

## Business facts

| | |
|---|---|
| Business | Riverside Fairways |
| Owners | Jase and Christy Browning |
| Phone | (225) 335-8279 |
| Email | info@riversidefairways.com · jase@riversidefairways.com (Workspace) |
| Mailing | 7061 Hunters Way, Denham Springs, LA 70726 |
| Hours | 6am–9pm |
| Service area | Baton Rouge, New Orleans, the Northshore; LA + MS Gulf Coast |
| Socials | Facebook, Instagram, TikTok ([@riversidefairways](https://www.tiktok.com/@riversidefairways)) |
| GBP | verification video submitted 2026-08-31, up to 5 days |
| Unit count | **1** ← the equipment resource quantity |

## Packages (from the pricing page)

| Tier | Name | Price | Duration |
|---|---|---|---|
| 1 | Birdie | $495 | 2 hrs |
| 2 | Eagle | $900 | 4 hrs |
| 3 | Champion | $1,300 | 6 hrs |
| 4 | All Day | $1,600 | 8 hrs |
| — | Corporate | $2,100+ | custom |

Add-ons (from /pricing-packages/): **Feral Experience $250 flat** (14+ games on any package), additional
hour **$175**, speaker/music **$75**, generator **$100**. Minimum booking 2 hours.

**GHL Products (2026-09-04):** all 10 of the above exist as Products with one-time prices in the Riverside sub-account (`clients/riverside-products.json`, `build/deploy_products.py`). Products are not a snapshot asset, so every client gets its own catalog. Quotes, invoices, the agreement's pricing table and opportunity values can all pull from these.

**Travel:** 50-mile radius free; **$75** for 51–100 mi; quote beyond 100 mi.

The Feral Package maps to `Add-On Package Name`; it is the answer to "will my
guests use it" for mixed-age and kid-heavy groups.

## Requirements (from the FAQ)

- **Space:** 15 ft × 20 ft floor
- **Height:** 12 ft ceiling clearance
- **Power:** reliable electricity (standard outlet)
- WiFi a plus, not required
- Outdoor OK — equipment is fairly weatherproof, cover preferred
- Setup/teardown happen outside billed event time
- Clubs and balls supplied; left-handed clubs on request at booking
- Team stays on site to set up, run play and pack out

## Balance timing — RESOLVED 2026-09-03

**48 hours before the event.** Confirmed by Clint 2026-09-03. Site patched the
same day via the Novamira MCP (`novamira-riversidefairway`): FAQ item 6322
("What payment methods do you accept?"), the Pricing & Packages page 5839, and
the draft Booking & Cancellation Policy 1628. Zero residual "7 days" in the DB.

## Payments — current state (as of 2026-09-02)

- Square, Venmo and PayPal accounts all set up by the client
- Stripe was floated; client told to hold ("Sit tight on configuring all the
  stripe things")
- **Undecided.** Last exchange: "Stripe or square?" → "I'm partial to stripe. I
  think my CRM is going to be able to take care of all the calendar/booking/
  payment stuff."
- Client accepted that **balance capture is manual** — the customer clicks pay
  on the reminder, or the operator charges the card on file. Do not let any copy
  promise automatic charging.

## The booking requirement (drove the template design)

> "the biggest part of that is we want to own our calendar and not let people do
> self booking. Is there a way that we can do that and just have the deposit
> invoice auto send to the customer once we book the date ourselves?"
> — 2026-09-02

They currently block their email calendar by hand and don't want to long-term.
This is exactly what the internal-only `EVENT - Unit Booking` calendar plus the
equipment resource solves.

## Deadline

Two October inquiries pending; pre-booking for October was opening the week of
2026-08-27. Current bookings are charity events with no payment needed.

---

## Custom value fill-in

```
Business Name                     Riverside Fairways
Business Phone                    (225) 335-8279
Business Email                    info@riversidefairways.com
Business Website                  https://riversidefairways.com
Owner First Name                  Jase
Primary City                      Denham Springs
State                             LA
Service Area List                 Baton Rouge, New Orleans and the Northshore
Base Travel Radius Miles          50
Travel Fee Policy                 Travel within 50 miles is included; 51-100
                                  miles is a flat $75; beyond 100 miles we
                                  quote it with your address.
Rental Asset Name                 mobile golf simulator
Unit Count                        1
Package 1 Name / Price / Duration Birdie / $495 / 2 hours
Package 2 Name / Price / Duration Eagle / $900 / 4 hours
Package 3 Name / Price / Duration Champion / $1,300 / 6 hours
Package 4 Name / Price / Duration All Day / $1,600 / 8 hours
Corporate Package Name / Price    Corporate / $2,100+
Add-On Package Name               Feral Package
Add-On Package Description        14 additional simulator games on top of golf
Pricing Page URL                  https://riversidefairways.com/pricing-plans/
Deposit Percent                   50%
Balance Due Days Before Event     2
Payment Methods Accepted          ⚠️ PENDING — Square/PayPal/Venmo decision
Space Requirement Footprint       15 ft x 20 ft
Space Requirement Height          12 ft of ceiling clearance
Power Requirement                 reliable access to electricity
Indoor Outdoor Capability         Yes — the equipment is fairly weatherproof, so
                                  cover is not required, though it is preferred.
What Is Included                  The simulator, screen and hitting area, clubs
                                  and balls, and our team on site to set up, run
                                  play and pack out.
Staffing Included                 Yes. We arrive early, set up, run the session
                                  and pack out.
Google Review Link                ⚠️ PENDING GBP verification
Internal Notification Email       ⚠️ CONFIRM — jase@ or info@
Internal Notification Phone       (225) 335-8279
Referral Offer                    LEAVE BLANK unless they actually have one
Repeat Customer Offer             LEAVE BLANK unless they actually have one
```

**Weather / Cancellation / Reschedule policy summaries:** pull verbatim from
their own pages. Do not paraphrase — the AI quotes these word for word, and
refund-vs-rain-check is an *opposite* default across this industry.

Their FAQ weather wording: *"rain, high wind, extreme heat, and lightning can
damage the equipment and create a safety risk"* → they contact you quickly to
reschedule or refund. Confirm this is still accurate before loading it.

## Notes

- Riverside's own site says outdoor is fine — unusual for this trade and a
  genuine selling point. The `Indoor Outdoor Capability` value carries it.
- Their competition is not mobile ("The good thing for us is that they're not
  mobile like we are" — 2026-08-21). Mobility is the differentiator.
- Event-safety page has real liability terms including a one-swing-at-a-time
  rule and host supervision duty. The AI must never paraphrase any of it.

## 2026-09-04 (later) — pass 3 applied directly to Riverside

- Survey `aqEtq5FqBoaNqU0GlJ6i`: rules re-pointed at field id `2VkInhWkcpySwRw1FXti`; both branches tested live. Redirect URL is a **placeholder** (`https://g.page/r/REPLACE-WITH-GOOGLE-REVIEW-LINK/review`) until the Google review link is known - the `Google Review Link` custom value is also still empty, so the 29a SMS sends without a link. Not on their website; needs the client.
- Workflow `30. Live Chat - AI Answers First` built with Riverside bot `MgAYjdgrMj1uguQuNbBk` (Event Booking Assistant); 26c refreshed. 35 workflows now.
- Chat widget `Event Booking Chat` `6a9b061d86066d429fe0372b` created with literal business name/website. Not embedded on the site yet (account is still the build copy).
- Internal Notification Phone/Email restored to `(225) 335-8279` / `info@riversidefairways.com`. All survey test contacts deleted.
- UI layer applied directly (dashboard rebuilt inside default `6a9a41c007fde41c6586f99a`, 5 field folders, contact view). Verified rendering, no widget errors.
- Brand palette created (neutral defaults, not their colors yet) and the form/survey buttons pointed at it. Riverside's real colors still need setting, then one re-run of `apply_brand_tags.py`.
- Funnel pages re-pushed on the brand palette (their green/dark defaults) with FAQ + review strip. Not published: no domain attached yet; `Average Rating` / `Review Count` / `Google Review Link` / `Logo URL` still empty.
- Billing set deployed: 12 templates (quote/deposit/balance x 4 tiers), workflows 31-34 (sender Jase), workflow 7 adds `book-balance-due` at 7 days, workflows 3 and 5 patched. Not exercised in Riverside yet; payment processor still not connected.
- Documents set deployed: Guest Waiver form `ut9QJ12Uuw0kKym0xfId` (QR: `clients/riverside-guest-waiver-qr.png`), Venue Requirements Sheet, COI Request, Event Day Confirmation, corporate quote template; workflows 35-36 built, workflow 7 patched (and its template field ids remapped).
- Branding pass applied: Logo URL = riverside-fairways-logo.svg, Color 1 #306553, Color 2 #111111; documents and forms rebuilt. Still-empty custom values that show as blanks in documents: Setup Time Required, Insurance Statement, Cancellation/Reschedule Policy Summary, Peak Season Note, Years In Business, Average Rating, Review Count, Google Review Link, Referral/Repeat offers (leave blank unless real).
- Documents part 2 deployed (proposal, date held, reschedule, receipt) with workflows 37-38, the corporate branch on 31 and the Date Held step in 6. Owner action tags to know: `book-rescheduled`, `book-balance-paid`.
- 2026-09-04: Google Business Profile still in verification with Google; review link cannot exist yet. Survey redirect and 29a SMS stay on the placeholder until it does.
- DNS: Clint is doing it. SPF for riversidefairways.com: `v=spf1 include:_spf.google.com include:_spf.wpengine.com ~all` (plus the LeadConnector sending-domain records once the sub-account's dedicated domain is set up under Settings > Email Services).


## Email logo fixed (2026-09-07)

Every Riverside email was rendering a broken logo. Two causes, neither obvious:

1. **Business profile `logoUrl` was blank.** All 15 email templates pull the
   header image from `{{location.logo_url}}`. (`{{location.name}}` and
   `{{location.email}}` were fine — the profile has those — so the sender-field
   defect that hits a *fresh clone* does not apply here.)
2. **The `Logo URL` custom value pointed at something unusable in email.**
   `riversidefairways.com/.../riverside-fairways-logo.svg` returns **403 to any
   request without a browser User-Agent** — which is how email clients and
   Gmail's image proxy fetch — and is an **SVG**, which Gmail, Outlook and Apple
   Mail do not render in email at all. No PNG/JPG existed on their site.

Fix: rendered the SVG to a 1200x648 transparent PNG and uploaded it to GHL media.

```
https://assets.cdn.filesafe.space/8Dc5dXota6CblTBsNy2k/media/cd3e3846-77cc-4e5f-a75e-78e570f17b5d.png
```

Verified it returns 200 with **no** User-Agent, unlike the WordPress URL. Set in
both places: the `Logo URL` custom value and the business profile `logoUrl`.
Profile PUT needs the **agency** token — the location PIT returns 401 "not
authorized for this scope".

**Lesson for every client:** do not point `Logo URL` at the client's own site.
Host it in GHL media. Client sites block bots and serve SVG; both fail silently
in email. Check the URL with a plain no-UA request before trusting it.
