# Client markup — progress

Source: `riversidefairways-com-export-2026-09-01.json` (61 comments, all from
Christy, captured 2026-08-30 on markup.io).

**51 done · 1 partial · 9 remaining** as of 2026-09-01.

## Done

| Comments | What |
| --- | --- |
| #11,12,19,20,24,25,33,34,39,40 | Measurements corrected to **15 ft x 20 ft** and **12 ft**. Two of my three placeholder figures were wrong. Applied to the spec band plus six venue lists and five FAQ answers that had only said "adequate ceiling height". |
| #21,28,36,37,47,54 | Cover policy. The site claimed the gear is **not** weatherproof and that outdoor setups **require** a tent. Christy: fairly weatherproof, cover **not required but preferred**, heavy rain or wind can pause or end an event. 10 fields rewritten. |
| #23,27,29,46,58 | Removed 4 photos carrying the **simulator manufacturer's** hexagon logo from 11 placements. A fifth suspect was an ordinary Vice ball wordmark and was kept. Galleries refilled from her RF-branded 30 Aug shots. |
| #2,18,32,55 | Fabricated reviews. Sections hidden via Elementor's responsive controls **and** the 18 review posts drafted, because hiding alone leaves the invented text in the page source. Testimonials page drafted, 301'd, out of nav and sitemap. |
| #3,56 | Landscaping leftovers. Three live templates (Single Post, Single Policy, Single Confirmation) carried the Turfgarden sidebar. Replaced with the real services loop. |
| #7,17 | Home street address removed from the Options page and all seven policy documents. The Google Maps link pinned their house and now points at the town. |
| #10 | Corporate price **From $2,100**. Made per-service first: the spec band is global, so the literal change would have priced kids' parties at $2,100. |
| #5,6,8 | Social icons. Team-card icons restored and wired to the real profiles (she wanted them working, not removed). Footer set is Facebook / Instagram / Medium. |
| #9 | Membership removed from the footer. |

## Partial

**#4** — Twitter is gone, but TikTok cannot be added: **the URL has never been
supplied**, despite being asked for three times.

## Remaining (26)

**Pricing page — #49,50,51,52,53.** Corporate tier at $2,100, package contents,
"Feral Package" header. Unblocked; highest commercial value left.

**Charity — #26,30,31,59,60.** Background photo + "Let's Connect", a copy tweak,
a new live/silent auction section, two photo decisions.

**Kids — #41,43,44,45,61.** Feral is an **add-on, not included**; a link to the
Feral showcase; removals.

**Contact — #13,14,15,16.** Duplicate email field, heading change, removals.

**Feral showcase — #42,44.** New "Geaux Feral" section. Needs a decision on
whether it is a page or a section.

**Also:** #1 (remove "confirmed clients"), #22 (travel fee wording), #35, #38,
#48 (repeats of #26).

**#57 merch** — prices supplied (Hats $30, T-shirts $25, Towel $20, Koozies $10,
Full Package $75) but product photos are still coming.

## Still waiting on the client

- TikTok URL
- RF-logo replacement photos
- Merch photos
- Real reviews
- Travel-fee distance and rate
- Deposit / balance / payment terms for the Booking policy (still a draft)
- Whether left-handed clubs exist (claim is published, unverified)

---

## Session 2 additions

| Comments | What |
| --- | --- |
| #26,38,41,48 | Sidebar CTA card. Background was `girl-gardener-dressed-in-apron-is-pruning-plants.jpg`, another Turfgarden leftover, which is why she asked for "a golf background photo". Now a real Riverside shot with a dark scrim; heading is "Let's Connect". One shared component across service, blog, policy and confirmation templates. |
| #13,14,15,16 | Contact page. Removed the duplicate "Our Email" card and a lorem ipsum paragraph, changed the heading (it also read "Let's **Became** One Of Us"), and made the email and phone cards clickable — they displayed the details but were not links. |
| #49,50,51,52,53 | Pricing. Added the Corporate tier at $2,100, corrected the Feral wording on three cards, renamed the "14 Extra Games" add-on to "Feral Package". |
| #1 | "250+ Happy Client" badge removed from the homepage — the last instance of that fabricated stat. |
| #22 | Travel-fee line appended to the global service-area copy, so it shows on all six service pages. |
| #30 | "that work hardest" → "that work the best". |
| #43 | Kids page now states Feral is an add-on, not included — in both the intro and the How It Plays list. |

### Notes for next time

- Elementor writes backgrounds to an **external** `post-<id>.css`, not inline. Grepping page HTML for a background image gives false negatives.
- A container can carry **two** backgrounds: `background_image` and a separate
  `background_overlay_image` on `::before`. Changing only the first leaves the old
  image visible on top.
- The sidebar is `position: sticky`, which breaks Playwright element screenshots.
  Set `position: static` before capturing.
- Passing strings with apostrophes through Python into PHP stores a literal
  backslash. Use base64.

## Board synced — 2026-09-01

Resolved **42** of 61 comments directly on the markup.io board via
`markup.py resolve riversidefairways.com "1,3,5-17,19-22,24-26,28,30,33,34,36-41,43,47-54,56"`.
Board `40030c5b-0ea4-452f-84cd-3f1d30ed1f3e` · verified 42 resolved / 19 open.

Bar chosen by Clint: **replacement delivered**, not merely *problem removed*. So
the nine "fixed but nothing in its place" items stay OPEN on the board on
purpose, and the board itself tracks the missing assets:

| Open because no replacement yet | Comments |
| --- | --- |
| Manufacturer-branded photos removed, none supplied | 23, 27, 29, 46, 58 |
| Fabricated testimonials removed, no real reviews yet | 2, 18, 32, 55 |

Still open for their original reasons: 4 (TikTok URL), 31 (auction section),
35/45/59/60/61 (bare "remove" with no pin data), 42/44 (Feral showcase — blocked
on pricing, raccoon mascot art, multisport photos), 57 (merch photos).

**19 open total.** Reopen anything with `markup.py resolve <board> <n> --unresolve`.

### #4 closed — 2026-09-01

Christy: *"Removed Twitter quick button, replace with TikTok across all pages where shown."*
TikTok URL supplied by Clint: `https://www.tiktok.com/@riversidefairways`.

Twitter was already gone from both **live** templates — it only survived in
unused template-kit leftovers (1397, 1405, 1444, 1612, 5894), none of which are
assigned a theme-builder condition. Left them alone. So the remaining work was
adding TikTok:

| Where | Change |
| --- | --- |
| Footer **1457** | TikTok inserted between Instagram and Medium |
| Team Member Card **5900** | same |
| SEOPress `sameAs` | appended to `seopress_social_accounts_extra` |

Verified live: `e-fab-tiktok` renders 3× on the homepage (footer + two team
cards), `sameAs` carries all four profiles. FA 5.15.3 ships `fa-tiktok`, so the
glyph is real — Elementor outputs inline SVG, not `<i class="fab">`.

**18 open.**

### #23 closed — 2026-09-01 (Christy's own photos)

Christy texted 8 photos (Jase shot them) at 18:30: *"You don't have to use all of
these, just whatever looks good with the page in your opinion."* Two subjects —
the **RF monogram** ball and the **Feral raccoon mascot** ball.

#23 was *"this is not our logo, we can provide you with some different photos
that have our logo on the golf balls."* The offender was attachment **6163**
(`riverside-fairways-branded-golf-ball-on-a-tee.webp`) — the one I had earlier
judged an ordinary Vice wordmark and **kept**. It was in **all six** service
galleries, not just the page she pinned.

Replaced everywhere:

| Service | Now |
| --- | --- |
| 1654 Corporate | 6314 RF monogram, turf |
| 1655 Charity | 6321 RF monogram, grass |
| 1656 Weddings | 6314 RF monogram, turf |
| 1657 Kids' Birthday | 6318 Feral mascot, tee close-up |
| 1658 Private Parties | 6321 RF monogram, grass |
| 1659 Casual | 6321 RF monogram, grass |

All 8 uploaded as WebP under 200 KB (ids 6314–6321), alt text set, originals in
`01-Brand-Assets/service-photos/_originals/`. Verified live after purge.

**The raccoon mascot is no longer a blocker for #42/#44** — it exists and is
on-brand. Still missing there: multisport action photos, and Christy's pricing
choice.

**8 open:** 2, 18, 31, 32, 42, 44, 55, 57.

### #57 partial — Swag prices live 2026-09-01

Christy's list from #57: Hats $30 · T-Shirts $25 · Golf Towel $20 · Koozies $10 ·
Full Package $75. The page had **six** template-kit items and **no prices**.

Rebuilt to her five (page 5993, backup in option `rf_swag_backup_20260901`):

| Card | Was | Image |
| --- | --- | --- |
| Hats — $30 | Logo Cap | 6014 kept (matches) |
| T-Shirts — $25 | Tournament Tee | 6019 kept (matches) |
| Golf Towel — $20 | Golf Towel | 6017 kept (matches) |
| Koozies — $10 | Polo Shirt | **image cleared** — a polo render is not a koozie |
| Full Package — $75 | Performance Glove | **image cleared** |
| _deleted_ | Golf Marker Set | — |

Buttons changed **"Add to Cart" → "Ask About Swag"**: there is no cart on this
site, so the old label promised checkout that does not exist.

SEO title/description/social/excerpt still advertised "polo shirts, gloves, ball
markers" — rewritten to the real lineup.

**#57 stays open** — she is sending real product photos, and the three surviving
images are AI-generated renders, not the actual merch.

**8 open:** 2, 18, 31, 32, 42, 44, 55, 57.
