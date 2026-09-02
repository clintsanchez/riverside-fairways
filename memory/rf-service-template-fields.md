---
name: rf-service-template-fields
description: "Riverside Fairways service pages: one template (1669) + Meta Box group 1756 drives all six; Meta Box stores TWO copies and both must be written"
metadata:
  type: project
---

All six Riverside Fairways service pages render from **one** Elementor template,
**1669 Single Service** (condition `include/singular/services`). Per-service
difference comes from Meta Box fields, never from separate templates — Clint's
stated intent is that the client edits fields, not layouts.

- **Field group 1756 "Service Content"** — 20 flat fields (no repeaters).
- Services: 1654 Corporate · 1655 Charity · 1656 Weddings · 1657 Kids' Birthday ·
  1658 Private Parties · 1659 Casual.
- Bound with the `meta-box-text` dynamic tag, settings URL-encoded:
  `{"key":"services:venue_needs_heading","fallback":"…"}`.

**Meta Box keeps TWO copies of the field list and you must write both:**

| postmeta key | used by |
| --- | --- |
| `fields` | the MB Builder UI |
| `meta_box` | the **runtime** — this is what resolves dynamic tags |

Writing only `fields` makes the field appear in wp-admin and resolve to **empty**
on the front end. That is what once blanked every service H1 via `hero_h1`.

**Optional sections** use `extra_heading` + `extra_body` rendered by
`[rf_service_extra]` — keyed on the body. See
[[elementor-container-should-render-is-fake]] for why it is a shortcode and not a
container filter.

`service_gallery` is an `image_advanced` array of attachment IDs, rendered by
`[rf_service_gallery]`. To swap a photo everywhere, check **all six** galleries —
a single bad image was in all of them even though the client only pinned one page.

Related: [[markup-io-resolve-api]], [[rf-scope-stick-to-the-ask]]
