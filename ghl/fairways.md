# Riverside Fairways — deployment sheet

Mobile golf simulator rental, Denham Springs LA. The client this template was
seeded from. **Sub-account not yet created** — this is the fill-in sheet for
when the snapshot is pushed.

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

Add-ons: **Feral Package** (14 additional simulator games), extended play time,
premium audio, power backup / generator.

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

## ⚠️ Conflict to resolve with the client

Their **pricing page** says *50% non-refundable deposit, balance due 48 hours
before the event*. Their **FAQ page** says *50% deposit, remaining balance due
7 days before the event*.

These contradict each other and both are public. Ask which is correct before
filling `Balance Due Days Before Event` — the workflow timing keys off it.

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
Balance Due Days Before Event     ⚠️ RESOLVE CONFLICT FIRST (2 or 7)
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
