# Placeholder figures — DO NOT LAUNCH WITHOUT REPLACING

Created 2026-08-03. Every value below was **invented by Claude at Clint's
request** so the service-page layout could be designed and reviewed. None of it
came from Christy or Jase, and none of it has been verified.

This conflicts with the accuracy guardrail in `.claude/CLAUDE.md` for as long as
it stays on the site. It is safe only because the site is still on the WP Engine
staging URL and has not launched.

## How to spot them on the page

Placeholder values render with a **dotted amber underline**. That marker lives
in one rule at the end of section 12 of the stylesheet (WPCodeBox snippet 2,
`website/rf-stylesheet.css`), commented as such. Delete that rule once the real
figures are in and the underline disappears everywhere at once.

## What needs confirming

All of these live on the **Options page** (Settings → Global Settings), so each
one is a single edit that updates all six service pages.

| Field | Placeholder now | What to ask |
| --- | --- | --- |
| `spec_1_value` | `From $495` | Real starting price. Every competitor publishes one — WeGo $2,500, PopCaddie $1,000, Lynks $450/2hr, NextGen $295/hr. |
| `spec_1_label` | `2 hours, fully staffed` | What does the starting price actually buy — how many hours, staffed or not? |
| `spec_2_value` | `15 ft × 15 ft` | Real floor footprint of the enclosure. |
| `spec_3_value` | `10 ft` | Real minimum ceiling clearance. This is the single most common reason a booking falls through. |
| `spec_4_value` | `Fully insured` | **Are they actually insured?** If not, this must come off the site entirely, not be reworded. |
| `spec_4_label` | `COI available on request` | Can they produce a certificate of insurance? Corporate and wedding venues usually require one before load-in. |
| `service_cities` | 14 Louisiana / MS towns | Which towns do they genuinely cover without a travel surcharge? The list drives local SEO, so it should be honest about the no-fee radius. |

Also still unconfirmed, from the earlier pass and unrelated to this file's
fields:

- Deposit amount and balance-due terms — still `[[PLACEHOLDER]]` in the
  **Booking & Cancellation Policy** (post 1628, still a draft).
- Travel-fee radius and rate — same policy.
- Whether clubs are available for **left-handed** players. This claim is
  already published in service-page copy and has no source.
- Whether **Sarah Mitchell** (Home page, "Lead Technician & Setup Specialist")
  is a real person. The intake lists two equal partners and company size "to be
  determined".

## Also placeholder-adjacent

The **power requirement** is stated in body copy as "access to electricity"
rather than a spec. Competitors say "one standard outlet". Worth pinning down
whether a single 110v circuit is genuinely enough, or whether a dedicated
circuit is needed for larger setups — it changes what venues they can accept.

---

## Update — 2026-08-31: two invented figures removed

The site went live on riversidefairways.com on 2026-08-29, which voided the
"staging only" assumption this file was written under. Two of the four spec-band
tiles were replaced with statements that are actually true rather than blanked,
so the band stays balanced:

| Tile | Was (invented) | Now (true) |
| --- | --- | --- |
| 1 | `From $495` / `2 hours, fully staffed` | `Quoted per event` / `Tell us your date and venue` |
| 4 | `Fully insured` / `COI available on request` | `Fully staffed` / `We set up, run it, pack out` |

"Quoted per event" matches what the pricing page already says. "Fully staffed"
is taken from the What's Included copy on every service page.

**Still invented and still live:** `15 ft x 15 ft` (tile 2) and `10 ft`
(tile 3). Both still carry the amber dotted underline. The original values are
backed up in the WordPress option `rf_spec_backup_20260831`.

Note: blanking a tile does NOT hide it — Elementor renders an empty bordered box
with a lone icon. The field description claiming otherwise is wrong. To remove a
tile properly, delete the widget from template 1669.

---

## RESOLVED — 2026-09-01: Christy confirmed the real figures

Client markup export (`client-feedback/riversidefairways-com-export-2026-09-01.json`,
61 comments) supplied the facts this file was waiting on. **Two of my three
invented figures were wrong.**

| Fact | I had | Christy (#11,#12,#10) | Status |
| --- | --- | --- | --- |
| Floor space | 15 ft x 15 ft | **15 ft x 20 ft** | live |
| Ceiling clearance | 10 ft | **12 ft** | live |
| Corporate price | From $495 | **From $2,100**, customised, fully staffed, call for quote | pending (#10) |
| Insurance | "Fully insured" | never confirmed | removed, replaced with "Fully staffed" |

Measurements are now in 17 places: the spec band plus the venue list on all six
service pages and five FAQ answers, which previously said only "adequate ceiling
height".

### A claim of mine that was flat wrong

I had written across five service pages and two FAQs that the equipment **is not
weatherproof** and that outdoor setups **require** a tent or pavilion. Christy
(#21,#28,#36,#37,#47,#54): the gear is "fairly weatherproof", cover is **not
required but preferred**, and heavy rain or wind can pause or end an event if
there is nowhere to move under. Corrected in 10 fields.

Her own photo of 2026-08-23 shows the enclosure on open grass with no cover —
the site was contradicting the client's own evidence.

### Manufacturer branding removed (#23,#27,#29,#46,#58)

Four photos showed a hexagon logo (crossed clubs) belonging to the **simulator
manufacturer**, not Riverside Fairways — from the manufacturer's private group,
which Christy had flagged by text on 2026-08-21. Removed from 11 placements.
A fifth photo I had suspected turned out to be an ordinary **Vice** ball
wordmark and was kept.

### Still outstanding

- Travel radius / fee: "can travel further for an additional travel fee, call
  for quote" (#22) — no distance or rate given.
- Deposit, balance-due and payment terms: still `[[PLACEHOLDER]]` in the draft
  Booking & Cancellation Policy.
- Left-handed clubs: still unverified, still published.
