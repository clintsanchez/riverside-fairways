# Riverside Fairways — Design System

**Riverside Fairways** is a fully mobile golf simulator based in Denham Springs,
Louisiana, serving all of Louisiana and the Mississippi Gulf Coast. They bring a
championship-quality simulator to corporate events, weddings, parties and charity
tournaments — anywhere with an electrical outlet. A second offering, the **Feral
pack**, adds 14 non-golf simulator games for kids and casual crowds.

- **Tagline / brand promise:** *Bringing the fairway to you.*
- **Brand essence:** Mobile · Sophisticated · Accessible
- **Owners:** Christy Browning and Jase — a two-person operation, under a year old.
- **Contact:** (225) 978-2363 · jase@riversidefairways.com · [Facebook](https://www.facebook.com/riversidefairways)
- **Pricing model:** tiered packages with add-ons, quoted per event (no public rate card).

## Products & surfaces

There is **one** product surface described in the source material: a **marketing
website** (not yet built or launched). No app, dashboard, docs site or slide
template exists anywhere in the sources, so none has been invented here. The
brand guide additionally anticipates email marketing, social templates and print
collateral; those are documented but not built.

## Sources

Everything here is derived from one repository:

- **GitHub:** https://github.com/clintsanchez/riverside-fairways (branch `main`)
  - `brand-style-guide.md` / `brand-style-guide.html` — the authoritative brand guide (colors, type, voice, logo rules, applications)
  - `DESIGN.md` — the component inventory and scale spec
  - `website/css-tokens.css` — token scaffold (spacing, radius, container, status colors)
  - `00-Client-Brief.md`, `.agents/product-marketing.md`, `aib/*.md` — positioning, ICP, voice, goals
  - `brand/riverside-fairways-logo.png` — the only supplied visual asset

Read that repo for deeper context before extending this system. See `github.md`
for the sync record.

---

## CONTENT FUNDAMENTALS

**The voice is three things at once:** friendly/approachable, luxury/sophisticated,
and casual/conversational. In practice that means polished sentences delivered
like a person talking, not a brochure. "Sophisticated without being stuffy."

**Person.** Second person for the reader, first-person plural for the company —
"you" and "we," never "the client" or "Riverside Fairways provides." Contractions
are used freely: *we're, it's, you'll, that's*.

**Voice.** Active, always. "We'll set up your simulator" — not "your simulator
will be set up by us." Lead with the differentiator in almost every opening:
*fully mobile, anywhere with electricity*.

**Casing.** Headline case for headers, sentence case for body. Uppercase is a
*typographic* device (eyebrows, nav, lockups) — never an emphasis device. Bold
carries emphasis; ALL CAPS in a sentence is off-brand.

**Punctuation & grammar.** Oxford comma, always. Em dashes for pause and emphasis.
Semicolons for linked clauses. Numbers one through nine spelled out; 10+ as
numerals. Exclamation points are rationed to genuine enthusiasm — roughly one per
page, if that.

**Length.** Paragraphs cap at three or four sentences. Bulleted lists for anything
scannable. Body copy sits at a 50–75 character measure.

**Specificity beats adjectives.** "Premium golf simulator with 14 additional games"
rather than "fun entertainment." Benefits over features: *impress your clients*,
*create unforgettable moments*.

**Tone shifts by context:**
- *Marketing* — enthusiastic, aspirational: "Transform your event into an unforgettable experience."
- *Website* — informative, professional: "Riverside Fairways sets up anywhere with access to electricity."
- *Social* — friendly, visual-first, playful: "Who said golf needs a course? ⛳"
- *Support* — helpful and solution-led: "We'd love to help make your event perfect. Here's what we can do…"

**Emoji.** Effectively banned on the website, in email and in print. The single
sanctioned exception is social media, where a golf-flag ⛳ occasionally appears in
a caption. Never use emoji as UI iconography.

**Banned.** Corporate jargon ("leverage," "synergize," "paradigm shift"), passive
voice, negative framing ("Don't worry…"), assumptions about golf knowledge, any
political content, and any unverified claim about licensing, reviews, or years in
business (the business is under a year old — never imply otherwise).

**Terminology.** "Golf simulator" ✓ · "golf simulation platform" ✓ · "mobile
simulator" ✓ · "golf video game" ✗. The tagline is written *Bringing the fairway
to you* and never reworded.

**Sample lines in voice:**
> "We're fully mobile — we set up anywhere you've got electricity."
> "No golf experience required. That's half the fun."
> "Tell us the date and the venue. We'll handle the rest."

---

## VISUAL FOUNDATIONS

**Palette.** A moody sage green over ivory. Primary Green `#5A8F7B` is the brand
color — logo, buttons, links, key UI. Secondary Ivory `#F5F1EB` is the workhorse
background for sections and large content areas. Light Green `#7BA691` is
*exclusively* for hover and subtle highlight; Dark Green `#3D5D52` carries weight
— headings, dark bands, the footer. Warm Neutral `#D4C5B9` is decorative only:
borders, dividers, image wells. Neutrals run White → Off-White `#F9F8F6` → Light
Gray `#EEEEEE` → Medium Gray `#999999` → Charcoal `#333333` (body text). Status
colors (`#22A06B` / `#E8A33D` / `#D9534F`) are for forms and system feedback only
— never decoration. **At most two background colors per layout**: white plus
ivory, or ivory plus one dark-green band.

**Type.** The body/UI face is the system stack
(`-apple-system, BlinkMacSystemFont, "Segoe UI", "Helvetica Neue", sans-serif`) at
16px/1.6 — the brand guide specifies system fonts and ships no binaries. The
display face is **Cormorant Garamond** (Google Fonts), chosen to match the
high-contrast serif of "FAIRWAYS" in the logo lockup — see *Substitutions* below.
Hierarchy: H1 42px weight 300 with 2px tracking (light and airy, never bold);
H2 28px weight 600 with 1px tracking; H3 20px weight 600; body 16px; captions
12px in Medium Gray. Never below 12px. Left-aligned, never justified.

**The signature typographic move is letterspacing.** Uppercase eyebrows at 12px /
.18em, and the tagline lockup at .32em, echoing the spaced `F A I R W A Y S` in
the logo. Use it for kickers, nav, and small labels — never for a paragraph.

**Spacing.** Everything is a multiple of 8: 8 / 16 / 32 / 64 / 96 / 128. Sections
breathe at 96px vertical (64px tight). Container is 1200px; prose narrows to
760px. Minimum tap target 44px.

**Corners & borders.** 6px on controls, 12px on cards, 20px on large panels,
pill for filter chips. Borders are hairline: 1px Light Gray on white surfaces,
1px Warm Neutral on ivory. Headings in long-form documents sit above a 3px
Primary Green rule — a device lifted straight from the brand guide.

**Cards.** White or ivory fill, 12px radius, 1px hairline border, and a very soft
shadow (`0 2px 10px rgba(61,93,82,.08)`) — green-tinted, never black. Cards never
match their section background. The featured card in a set gets a 2px green
border, not a bigger shadow. No colored left-border accents.

**Shadows.** Three steps only: swatch (`0 2px 4px rgba(0,0,0,.10)`), card, and
raised (`0 8px 24px rgba(61,93,82,.12)`). No inner shadows anywhere in the system.

**Backgrounds & imagery.** Flat color is the default — no textures, no patterns,
no illustration system. The one gradient in the brand is
`linear-gradient(135deg,#5A8F7B,#3D5D52)`, used on title cards and hero areas
without photography. Photography is bright, warm, and people-forward: close-up
action or medium group shots, even lighting on faces, controlled backgrounds,
natural saturation with a slight warm cast. Never dark, moody, wide, or obviously
staged stock. **Any photograph carrying text gets the Primary Green 40% overlay
plus a bottom scrim** — that green wash is the brand's most recognizable
composition. No photography was supplied with the brand package; every image well
in this system renders a labelled placeholder.

**Transparency & blur.** Used sparingly and only over photography: the 40% green
overlay, the bottom scrim, and a hairline `rgba(255,255,255,.18)` rule under a
transparent header. No frosted-glass panels, no blurred backdrops.

**Motion.** Restrained. 200ms color and background transitions on the standard
ease (`cubic-bezier(.4,0,.2,1)`); 120ms for small controls. Fades and color
changes only — no bounce, no spring, no parallax, no entrance animations.

**Interaction states.** Hover *lightens*: filled buttons go Primary → Light Green;
outline buttons fill with Primary Green and flip their label to white; links
darken to Dark Green. Press states darken to Dark Green — nothing scales or
shrinks. Focus is a 3px `rgba(90,143,123,.35)` ring, never removed. Disabled is
Light Gray fill with Medium Gray text.

**Layout rules.** One hero per page, at the very top. Sections alternate white and
ivory down the page; at most one dark-green band before the footer. The footer is
always dark green with the ivory logo. Headers may be transparent over a hero,
solid white everywhere else. Grids are 3- or 4-up on desktop, gap 32px.

---

## ICONOGRAPHY

**There is no icon system in the source material.** The brand guide asks for
"simple, clean line-based icons (14px–48px)" but ships none, and the repository
contains exactly one image file — the logo PNG.

What this system does instead:

- **The golf flag from the logo is the brand's only real glyph.** It has been
  extracted from the logo artwork into `assets/icon-flag.png` and
  `assets/icon-flag-reversed.png` and is used as a list bullet, an avatar mark,
  and an empty-state / placeholder mark. It is not drawn — it is cropped from the
  supplied logo file.
- **No hand-drawn SVGs.** Nothing in this project draws an icon from scratch.
- **No icon font, no sprite sheet, no CDN icon set is linked.** If a UI genuinely
  needs a utility icon set (menu, close, chevron, phone), use **Lucide** at 1.5px
  stroke via CDN — it matches the brand's "simple, clean, line-based" description.
  **This would be a substitution, not a brand asset — flag it with the client.**
- **Emoji are not iconography.** The ⛳ that appears in social captions is copy,
  not UI. Never use emoji in an interface.
- **Unicode as icons:** only the "→" in text links ("Ask about weddings →"), which
  the brand guide's own materials use. Nothing else.

---

## Substitutions & flags — please review

1. **Display serif is a substitution.** The brand guide names only system fonts
   (Segoe UI / Helvetica Neue), which cannot express the elegance of the logo. The
   logo's "FAIRWAYS" wordmark is a high-contrast serif, so **Cormorant Garamond**
   (Google Fonts) is used for headings and display type. *If you have the real
   licensed font files from the logo designer, send them and this swaps out in one
   file (`tokens/fonts.css`).*
2. **No photography exists.** Every image is a labelled placeholder.
3. **No pricing or package names exist.** "The Fairway / The Clubhouse / The Open"
   in the UI kit are illustrative scaffolding, clearly marked as such.
4. **Only one logo file was supplied** (the full color lockup). The reversed,
   ivory, black and icon variants in `assets/` were generated by recoloring and
   cropping that exact artwork — no mark was redrawn. Horizontal and stacked
   lockups referenced in the brand guide were not supplied.
5. **No icon set.** See ICONOGRAPHY above.

## Intentional additions

- **`Logo`** — a thin wrapper around the approved PNG files. Added so no consumer
  is ever tempted to set the wordmark in type. Not a component in the source spec.

---

## Index

| Path | What it is |
|---|---|
| `styles.css` | Global entry point — link this one file. `@import`s only. |
| `tokens/` | `colors` · `typography` · `spacing` · `radius` · `elevation` · `motion` · `fonts` · `base` |
| `assets/` | Logo lockups (primary, reversed, ivory, black) and the flag icon |
| `brand/` | The original supplied logo artwork, untouched |
| `components/core/` | `Button` · `Card` · `Logo` |
| `components/layout/` | `Section` · `Hero` · `SiteHeader` · `SiteFooter` |
| `guidelines/` | 19 specimen cards — colors, type, spacing, brand |
| `ui_kits/website/` | Marketing site recreation (5 screens, click-through) |
| `github.md` | Source-repo association and sync record |
| `SKILL.md` | Agent Skills entry point |

### Components

- **Button** — primary, outline, ghost, reversed; sm/md/lg; disabled; full-width.
- **Card** — default, surface, elevated, inverse; media well, eyebrow, footer, `featured`.
- **Logo** — approved lockups and the flag icon at any height.
- **Section** — page band with background skin, container, eyebrow/heading/lead.
- **Hero** — photo hero with green overlay, CTA pair and trust strip.
- **SiteHeader** — logo, uppercase nav, click-to-call, quote CTA; transparent mode.
- **SiteFooter** — dark green footer with ivory logo, link columns, contact row.

Each component directory carries `<Name>.d.ts` (props contract),
`<Name>.prompt.md` (when and how to use it) and one `@dsCard` HTML.

### UI kits

- **`ui_kits/website/`** — Home, Packages, Events, About & service area, Get a quote.
