---
name: rf-social-icon-placements
description: "Riverside Fairways social links live in exactly 3 places — Elementor footer 1457, Team Member Card 5900, and SEOPress seopress_social_accounts_extra"
metadata:
  type: project
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

Current set (2026-09-01): Facebook, Instagram, TikTok, Medium — in that order,
Medium last because it is the blog rather than a social profile.

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
