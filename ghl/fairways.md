# Riverside Fairways — deployment sheet

Mobile golf simulator rental, Denham Springs LA. The client this template was
seeded from.

**Sub-account: `Riverside Fairways` = `8Dc5dXota6CblTBsNy2k`** — created
2026-09-04 via `POST /locations/` from snapshot `kc48mDlFyozpHoW38ukG`
(Mobile Event Rental v1, refreshed to v4 with all 17 workflows). Target slug
`riverside` (`GHL_LOCATION_ID_RIVERSIDE` + `GHL_PIT_RIVERSIDE` in `.env`; Private
Integration `ghl-toolkit`, all scopes, created 2026-09-04).

## Deployment log (2026-09-04)

| Done | Item |
|---|---|
| x | 17 workflows published, all referencing Riverside's own pipeline/calendar ids (verified, 0 stale template ids) |
| x | Pipeline `Event Bookings` (12 stages); GHL's default `Marketing Pipeline` deleted |
| x | 4 calendars incl. `EVENT - Unit Booking (INTERNAL)` = `jsmbQKFnzGwyt1hBlBEs` |
| x | Equipment resource `Primary Rental Unit`, **qty 1**, bound to the unit calendar |
| x | Form `Date Request` + funnel `Date Request` (2 pages); base junk forms/funnels removed |
| x | 47 custom values filled — sheet below plus verbatim FAQ wording for Weather Policy Summary, Payment Methods Accepted, Booking Lead Time; Facebook/Instagram URLs |
| x | Workflow 13 trigger now filters Call Status = no-answer (template + Riverside, snapshot v5) |
| x | Clint's agency user attached |
| | Client users (Jase, Christy) — invite from Settings > Team (sends them email; left for Clint) |
| | Knowledge-base crawl of riversidefairways.com inside *this* account |
| | Custom values still empty and why: **Cancellation / Reschedule Policy Summary** — the site's Booking & Cancellation Policy (post 1628) is a DRAFT with `[[REFUND TERMS]]` placeholders, so the client has not decided these; Google Review Link (GBP pending); Insurance Statement; Setup Time Required; Years In Business; Peak Season Note; Logo URL; Colors; Payment Link; Agreement / Contract Link; Booking Page URL; Referral / Repeat offers |
| | Note: policy draft says equipment is *not* weatherproof; the live FAQ says *fairly* weatherproof. Loaded the FAQ (published) wording; client should reconcile |
| | `Internal Notification Email` set to **info@riversidefairways.com** pending Jase-vs-info confirmation |
| x | WordPress: `/forms/availability/` (post 6334, the header "Book Your Event" target) now embeds GHL form `MDbnBPt0usnkrNvXehLB` in place of `[ws_form id="6"]` (original saved in post meta `_rf_ws_form_backup`; WS Form 6 had no actions configured, so its submissions went nowhere). `/forms/consultation/` (post 38) embeds the Discovery Call calendar `n955fquCtCCiNx5xlTiF` (original in `_rf_content_backup`). WP Engine cache purged. |
| | Funnel domain (client side) before `/request-a-date` is public |

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

Add-ons (from /pricing-packages/): **Feral Package** (14+ games), additional
hour **$175**, speaker/music **$75**, generator **$100**. Minimum booking 2 hours.

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
