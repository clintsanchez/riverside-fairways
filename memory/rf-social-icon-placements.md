---
name: rf-social-icon-placements
description: "Riverside Fairways social links live in exactly 3 places — Elementor footer 1457, Team Member Card 5900, and SEOPress seopress_social_accounts_extra"
metadata: 
  node_type: memory
  type: project
  originSessionId: 226937ca-282b-4c2d-93b8-b18d79f2194e
  modified: 2026-09-10T19:21:26.827Z
---

A new social profile for Riverside Fairways has to land in **three** places or
it will look done and be half-wired:

1. **Footer template 1457** — `social_icon_list` in `_elementor_data`
2. **Team Member Card 5900** — same widget, same array (easy to miss; the
   founders' cards each render their own copy)
3. **SEOPress** — `seopress_social_option_name['seopress_social_accounts_extra']`,
   one URL per line. SEOPress has **no TikTok field**, so anything outside
   facebook/twitter/instagram/youtube/linkedin/pinterest goes in `extra`.

Then record it on the [Trello card](https://trello.com/c/W6Uw6BKy) and in
`aib/profile.md`.

Current set (2026-09-10): **Facebook, Instagram, TikTok** — Christy asked for
only these three "for now". Medium was removed from footer + team card but is
still in SEOPress `sameAs` (schema only, not a button).

**Instagram is `@riversidefairways` (plural).** The singular `riversidefairway`
was marked "client-supplied and confirmed" on 2026-08-31 but was a dead profile
until 2026-09-10. Check a handle with Playwright (logged-out curl and the
profile API can't tell real from fake: every handle returns the same generic
page / 401). A dead profile's page title is "Profile isn't available".

**Verification gotcha.** Elementor renders these as **inline SVG**, not
`<i class="fab fa-tiktok">`. Grepping live markup for `fa-tiktok` returns
nothing and reads exactly like a failed write. Grep for **`e-fab-tiktok`**
instead. On the homepage each icon should appear **3×** (footer + two team
cards). Font Awesome 5.15.3 is bundled and does ship the TikTok glyph.

**Do not "tidy" the Twitter leftovers.** Templates 1397, 1405, 1444, 1612 and
5894 (`RFSTG = Home`) still contain `fab fa-twitter`, but none of them holds a
theme-builder condition, so none renders anywhere. They are unused template-kit
remnants, not live pages. Clint has pushed back before on uninstructed cleanup
([[rf-scope-stick-to-the-ask]]).

Related: [[markup-io-resolve-api]], [[wpengine-cache-before-verifying]]
