# Riverside Fairways Brand Guidelines

**Document Version:** 2.0  
**Last Updated:** August 1, 2026  
**Brand Contact:** Christy Browning, Riverside Fairways  

> **What changed in 2.0.** Version 1.0 described a light theme that the live site
> never used. This version documents what is actually deployed: a dark theme
> built on Elementor kit 1368, with the green sampled directly from the logo
> file. Every contrast figure below has been measured, not estimated. Two
> figures in v1.0 were wrong and are corrected here. See §12 for the full list.

---

## 1. Brand Overview

### Mission
Riverside Fairways brings the fairway to you. We are a fully mobile golf simulator company that delivers premium entertainment experiences to corporate events, celebrations, weddings, and parties throughout Louisiana and beyond.

### Brand Essence
**Mobile. Sophisticated. Accessible.**

Riverside Fairways combines luxury golf experience with the convenience of mobility. We're sophisticated without being stuffy, and approachable without being casual.

### Brand Promise
"We bring the fairway to you." Premium golf entertainment, anywhere, anytime.

### Core Brand Values
- **Mobile-First:** We set up anywhere with electricity
- **Luxury:** Premium experience, professional service
- **Accessible:** No golf experience required, fun for all skill levels
- **Sophisticated:** Elegant, quality-focused experience
- **Community-Oriented:** Perfect for corporate team building, celebrations, and gatherings

### Target Audiences
- **Corporate Events:** Team building, client entertainment, holiday parties
- **Event Planners:** Wedding ceremonies and receptions, milestone celebrations
- **Families & Social:** Casual parties, birthday celebrations, social gatherings
- **Golf Enthusiasts:** Practice facility, tournament alternatives

---

## 2. Visual Identity

### Logo

#### Logo Mark
The Riverside Fairways logo features an elegant script wordmark with an integrated golf flag icon. The design conveys sophistication through graceful letterforms and subtle movement.

#### Primary Logo
- **File:** `brand/riverside-fairways-logo.png`
- **Color:** Fairway Green (#5D7D72), sampled directly from the logo artwork
- **Use:** All primary applications, digital and print

The supplied logo is a single flat colour throughout: `#5D7D72`. Earlier drafts
listed `#5A8F7B`, which does not appear anywhere in the file. Always sample from
the artwork rather than trusting a written value.

#### Logo Variations

**Horizontal Lockup** (Preferred for most uses)
- Logo with "BRINGING THE FAIRWAY TO YOU" tagline
- Maintains full brand personality and messaging

**Icon Only** (Apps, avatars, favicons)
- Golf flag icon in isolation
- Minimum size: 120px digital, 0.5" print
- Use for social media profile pictures, app icons, favicons

**Monochrome (Black)**
- Use on white or very light backgrounds
- Professional reports, black & white printing

**Reversed (Cream)**
- Use on Deep Green, near-black, or photographic backgrounds
- This is the primary web variant, since the site is a dark theme
- Use Cream (#F5EFE5) rather than pure white so it matches site type

#### Clear Space
Maintain clear space equal to the height of the golf flag on all sides. No other design elements should intrude on this space.

#### Minimum Size
- **Digital:** 120 pixels wide
- **Print:** 0.75 inches wide

#### Logo Don'ts
- ❌ Never stretch, compress, or distort the logo
- ❌ Never rotate the logo (except 180° for reversed applications)
- ❌ Never change the colors without approval
- ❌ Never add effects (shadows, gradients, outlines)
- ❌ Never place on busy or patterned backgrounds
- ❌ Never remove or alter the tagline when using full lockup
- ❌ Never place on backgrounds with insufficient contrast

---

### Color Palette

The palette below is the live source of truth. Each colour maps to a variable in
the Elementor kit (Site Settings > Global Colors) and to a token in
`website/css-tokens.css`. Change a colour in Elementor and the site follows.

#### The site is a dark theme

Riverside Fairways renders as cream and green type on near-black. This is
deliberate: it makes the simulator photography and screen imagery the brightest
thing on the page. Light backgrounds are reserved for print, email, and the
occasional highlight panel.

#### Core Colors

**Near-Black** (page background)
- **Hex:** #111111 · **RGB:** 17, 17, 17
- **Elementor:** Secondary · **Token:** `--rf-secondary`
- **Usage:** Site background, dark bands, signage backgrounds

**Card Surface**
- **Hex:** #1A1A1A · **RGB:** 26, 26, 26
- **Elementor:** Overlay 3 · **Token:** `--rf-graphite`
- **Usage:** Cards, callout boxes, panels that sit on the page background

**Cream** (headings and bright type)
- **Hex:** #F5EFE5 · **RGB:** 245, 239, 229
- **Elementor:** Primary · **Token:** `--rf-cream`
- **Usage:** Headings, reversed logo, light panels, print backgrounds

**Body Cream** (running text)
- **Hex:** #EDE7DC · **RGB:** 237, 231, 220
- **Elementor:** Text · **Token:** `--rf-text`
- **Usage:** Body copy on dark surfaces

#### Greens

**Fairway Green** (the logo colour)
- **Hex:** #5D7D72 · **RGB:** 93, 125, 114
- **Elementor:** Overlay 1 · **Token:** `--rf-accent`
- **Usage:** The logo, borders, photographic overlays, large display type
- ⚠ **4.17:1 on near-black.** Large text and graphics only, never body copy.

**Deep Green** (buttons and fills)
- **Hex:** #306553 · **RGB:** 48, 101, 83
- **Elementor:** Accent · **Token:** `--rf-primary`
- **Usage:** Button fills, rules, left borders on callout boxes
- ⚠ **2.80:1 on near-black.** This is a FILL colour. Never set text in it on a
  dark background. It is safe as a background behind white or cream text.

**Light Green** (type and links on dark)
- **Hex:** #7BA691 · **RGB:** 123, 166, 145
- **Token:** `--rf-green-light`
- **Usage:** Links, eyebrow labels, small green type on dark surfaces
- This is the only green that clears AA at body and label sizes on near-black.
  It is a derived shade, not present in the Elementor kit.

#### Supporting Neutral

**Warm Neutral**
- **Hex:** #D4C5B9 · **RGB:** 212, 197, 185
- **Usage:** Decorative borders and quiet accents. Not a text colour.

#### Accessibility Compliance

Every figure below was measured against the deployed colours. Target is WCAG AA:
4.5:1 for normal text, 3:1 for large text and graphics.

| Combination | Ratio | Normal text | Large text |
|---|---|---|---|
| Body Cream on Near-Black | 15.34:1 | ✓ AAA | ✓ AAA |
| Cream on Near-Black | 16.51:1 | ✓ AAA | ✓ AAA |
| Body Cream on Card Surface | 14.14:1 | ✓ AAA | ✓ AAA |
| Light Green on Near-Black | 6.93:1 | ✓ AA | ✓ AAA |
| Light Green on Card Surface | 6.39:1 | ✓ AA | ✓ AAA |
| White on Deep Green (buttons) | 6.75:1 | ✓ AA | ✓ AAA |
| Cream on Deep Green (buttons) | 5.90:1 | ✓ AA | ✓ AAA |
| Near-Black on Cream (print) | 16.51:1 | ✓ AAA | ✓ AAA |
| Deep Green on Cream (print) | 5.90:1 | ✓ AA | ✓ AAA |
| Fairway Green on Near-Black | 4.17:1 | ✗ FAIL | ✓ AA |
| Fairway Green on Cream | 3.96:1 | ✗ FAIL | ✓ AA |
| Deep Green on Near-Black | 2.80:1 | ✗ FAIL | ✗ FAIL |

**The two rules that matter:**

1. Deep Green is a background, never dark-on-dark text.
2. Fairway Green is for the logo, borders, and large type. For small green text
   on a dark surface, use Light Green.

**Color Blindness Consideration:** Avoid green plus red combinations in
information displays. Pair colour with an icon, label, or pattern whenever it
carries meaning.

---

### Typography

Both typefaces are already loaded by the site through the Elementor kit. Do not
introduce a third family without approval.

#### Primary Typeface: DM Sans

**Usage:** Headings, body text, UI, buttons  
**Weights in use:** Regular (400), Medium (500), Semibold (600), Bold (700)  
**Licensing:** Google Fonts, free for commercial use

```
font-family: "DM Sans", system-ui, sans-serif;
```

#### Accent Typeface: Bad Script

**Usage:** Short decorative flourishes only. Pull quotes, a single line of
scripted emphasis, occasional social graphics.  
**Weight:** 500  
**Licensing:** Google Fonts, free for commercial use

Bad Script echoes the script "Riverside" in the logo. Use it sparingly. Never
set a heading, a paragraph, a button, or anything longer than one line in it,
and never use it at small sizes.

#### Monospace: Courier New

**Usage:** Code samples, technical specifications, colour codes

#### Type Hierarchy

Sizes below are the live Elementor kit values. Headings are set in DM Sans Bold
with `line-height: 1.1` and capitalised.

| Level | Size | Weight | Notes |
|---|---|---|---|
| Display | 5rem (80px) | 700 | Hero statements only |
| H1 | 3rem (48px) | 700 | Page titles |
| H2 | 2rem (32px) | 700 | Section headers |
| H3 | 1.563rem (25px) | 700 | Subsections |
| H4 | 1.375rem (22px) | 700 | Minor headings |
| Lede | 1.5rem (24px) | 400 | Intro paragraph, line-height 1.3 |
| Body | 1.1rem (17.6px) | 400 | Running text, line-height 1.6 |
| Accent | 1.15rem (18.4px) | 500 | Buttons and UI labels |
| Small | 0.875rem (14px) | 400 | Captions and metadata |

**Optimal line length:** 50 to 75 characters. The site caps body text at 68
characters via the `--measure` token.

#### Typography Do's and Don'ts

✓ **Do:**
- Use the specified hierarchy and let the Elementor kit drive sizing
- Keep body text at 1rem or larger
- Left align body text
- Maintain line-height between 1.4 and 1.8 for running text
- Check contrast against the dark background, not against white

✗ **Don't:**
- Set body copy, headings, or buttons in Bad Script
- Set text smaller than 14px
- Use all caps for extended body text. Reserve caps for short eyebrow labels
- Justify text alignment
- Stretch, compress, or distort text

---

## 3. Photography & Imagery Style

### Photography Direction

**Style:** Professional, polished, sophisticated  
**Mood:** Upscale leisure, approachable luxury, community connection  
**Subjects:** Golf simulator action, group experiences, celebration moments

**Note on the dark theme.** Photography is the brightest element on the page, so
images carry the energy. Favour well-lit subjects against darker surroundings,
which is how a simulator setup genuinely looks in a venue. The screen glow, the
ball in flight, and lit faces should be the focal points.

#### Composition Guidelines
- **Framing:** Close-up action shots or medium group shots. Avoid distant wide angles
- **Lighting:** Subjects clearly lit, with faces and expressions readable
- **Backgrounds:** Controlled. Darker surroundings suit the site and look natural
- **People:** Always include people. Show genuine enjoyment and engagement
- **Edges:** Images sit on a near-black page, so avoid bright blown-out borders
  that create a hard rectangle against the background

#### Color Treatment
- Warm, inviting tones aligned with brand colors
- Avoid over-saturation; maintain natural appearance
- Slight warm color cast encouraged (enhances approachability)

#### Prohibited Imagery
- ❌ Generic, overly staged stock photos
- ❌ Underexposed images where faces are unreadable
- ❌ Cluttered or busy backgrounds
- ❌ Very wide or distant shots with small people
- ❌ Images with competing brand elements
- ❌ Bright white studio backdrops, which fight the dark page

### Graphic Elements

**Accent Shapes:** Subtle geometric elements using brand colors  
**Icons:** Simple, clean line-based icons (14px–48px)  
**Illustrations:** Limited use; when used, employ simple line art style aligned with brand colors

---

## 4. Brand Voice & Tone

### Brand Voice Characteristics

Riverside Fairways' voice is:

**Friendly / Approachable**
- Conversational and personable
- Avoids stiff corporate jargon
- Warm and welcoming

**Luxury / Sophisticated**
- Professional and polished
- High-quality language and presentation
- Confident and authoritative

**Casual / Conversational**
- Uses contractions ("we're," "it's")
- Direct address (you/we)
- Relaxed but professional

### Voice Principles

1. **Write for Your Audience:** Corporate clients want professionalism; party planners want fun and ease
2. **Use Active Voice:** "We'll set up your simulator" not "Your simulator will be set up by us"
3. **Be Specific:** "Premium golf simulator with 14 additional games" not "Fun entertainment"
4. **Show Benefits:** Focus on what the audience gains ("impress your clients," "create unforgettable moments")
5. **Maintain Authenticity:** Stay true to "fully mobile" and "luxury" positioning

### Tone by Context

**Marketing Materials**
- **Tone:** Enthusiastic, aspirational
- **Example:** "Transform your event into an unforgettable experience. Our mobile golf simulator brings championship-level entertainment to your venue."

**Website Copy**
- **Tone:** Informative, professional
- **Example:** "Riverside Fairways sets up anywhere with access to electricity. In just a few hours, we create a premium golf experience your guests will remember."

**Social Media**
- **Tone:** Friendly, engaging, visual-first
- **Example:** "Who said golf needs a course? ⛳ Check out this corporate team building moment with our mobile simulator!"

**Customer Support**
- **Tone:** Helpful, solution-oriented
- **Example:** "We'd love to help make your event perfect. Here's what we can do..."

**Internal Communications**
- **Tone:** Collaborative, clear
- **Example:** "Team update: New booking protocol to improve setup times."

### Voice Don'ts

❌ **Avoid:**
- Corporate jargon ("leverage," "synergize," "paradigm shift")
- Passive voice ("errors were made")
- All caps for emphasis (use bold instead)
- Exclamation points in excess
- Assumptions about golf knowledge
- Negative framing ("Don't worry...")

---

## 5. Key Messages & Messaging Framework

### Elevator Pitch (30 seconds)
"Riverside Fairways brings championship-quality golf simulation to your event. Fully mobile and set up anywhere with electricity, our premium simulator creates unforgettable moments for corporate events, weddings, and celebrations throughout Louisiana."

### Primary Messages

1. **Fully Mobile**
   - We set up anywhere you need us
   - No golf course required
   - Flexibility your event deserves

2. **Premium Experience**
   - Championship-quality simulator
   - Professional, polished service
   - Luxury entertainment

3. **Perfect for Any Event**
   - Corporate team building
   - Wedding entertainment
   - Casual celebrations
   - Birthday parties

4. **No Golf Experience Required**
   - Inclusive and accessible
   - Fun for all skill levels
   - Creates connection and laughter

### Supporting Messages

- 14 additional games beyond golf
- Professional setup and breakdown
- Engaging for groups of all sizes
- Creates shareable moments
- Impressive conversation starter

### Calls to Action

**Book Your Event:**
- "Reserve your simulator today"
- "Plan your perfect event"
- "Get a quote now"
- "Schedule a demo"

**Share & Engage:**
- "Tag us in your event photos"
- "Share your high score"
- "Tell us about your experience"

---

## 6. Brand Applications

### Digital Applications

**Website** (dark theme)
- Background: Near-Black (#111111) sitewide
- Header: Logo in Cream, navigation in Cream with Light Green active state
- Hero: Photography with a Fairway Green scrim so type stays readable
- CTA buttons: Deep Green (#306553) fill with white or cream text
- Body text: Body Cream (#EDE7DC) on Near-Black
- Headings: Cream (#F5EFE5)
- Links and eyebrow labels: Light Green (#7BA691)
- Cards and callouts: Card Surface (#1A1A1A) with a Deep Green left border

**Email Marketing** (light, for deliverability and client inboxes)
- Header: Logo on Cream background
- Primary CTA button: Deep Green fill with white text
- Signature colour: Deep Green accent bar
- Links: Underlined Deep Green. Do not use Fairway Green for link text on cream,
  it measures 3.96:1

**Social Media**
- Profile colour: Fairway Green
- Story and post overlays: Semi-transparent Fairway Green gradient
- Text: Cream over a scrim rather than a drop shadow
- Hashtag: #RiversideFairways (branded in bio)

**Mobile App** (if developed)
- Status bar: Near-Black
- Navigation: Light Green highlights
- Primary buttons: Deep Green fill with white text
- Backgrounds: Near-Black with Card Surface panels

### Print Applications

**Business Cards**
- Layout: Logo on left, Cream background, Deep Green border accent
- Text: Near-Black and Deep Green for hierarchy
- Paper: Heavyweight matte cardstock
- A reversed variant on Near-Black with a Cream logo matches the website

**Brochures**
- Cover: Hero photography with a Fairway Green overlay
- Interior: Cream background with Deep Green section dividers
- Typography: Maintain hierarchy per the type guidelines
- Paper: Matte cardstock

**Signage**
- Logo: Minimum 2" wide
- Background: Cream or Near-Black
- Text: High contrast. Near-Black on Cream, or Cream on Near-Black
- Maintain clear space around the logo

**Promotional Materials**
- Branded colour: Fairway Green throughout
- Logo placement: Top or centre-left
- Contact information: Easy to read
- Call to action: Prominent and clear

---

## 7. Tone & Grammar Standards

### Writing Style

**Contractions:** Use freely ("we're," "it's," "you'll")  
**Second Person:** Address audience as "you"  
**Active Voice:** Preferred over passive  
**Exclamation Points:** Use sparingly for genuine enthusiasm  
**Lists:** Use bullet points for scanability  
**Paragraphs:** Keep short (3–4 sentences max)

### Grammar & Punctuation

- **Oxford Comma:** Use consistently (A, B, and C)
- **Em Dashes:** Do not use them. Rewrite with a comma, a full stop, or
  parentheses. Em dashes are a strong tell of AI-generated copy and the blog
  house standard forbids them, so the rule is the same everywhere
- **Semicolons:** Use to connect related independent clauses
- **Capitalization:** Headline case for headers, sentence case for body
- **Numbers:** Spell out numbers one through nine, use numerals for 10+

### Brand-Specific Terminology

| Term | Usage |
|------|-------|
| Golf simulator | ✓ Correct (our specific offering) |
| Golf simulation platform | ✓ Acceptable alternative |
| Golf game / golf video game | ✗ Avoid (too casual/inaccurate) |
| Bringing the fairway to you | ✓ Our tagline (brand promise) |
| Mobile simulator | ✓ Emphasizes mobility |
| Event entertainment | ✓ Broad context |

---

## 8. Dos and Don'ts Summary

### Logo
✓ Use approved logo files  
✓ Maintain clear space  
✗ Never distort or stretch  
✗ Never change colors  

### Color
✓ Use exact hex values  
✓ Test contrast for accessibility  
✗ Never approximate colors  
✗ Never use unauthorized color combinations  

### Typography
✓ Follow type hierarchy  
✓ Maintain readability (min 12px body text)  
✗ Never use unapproved fonts  
✗ Never stretch or compress text  

### Voice
✓ Be friendly and professional  
✓ Use active voice  
✗ Never use corporate jargon  
✗ Never be condescending  

### Photography
✓ Feature people and genuine moments  
✓ Use professional, well-lit imagery  
✗ Never use generic stock photos  
✗ Never use dark, moody lighting  

---

## 9. Brand Evolution & Approval Process

### When Changes Are Needed
Contact the brand owner (Christy Browning, Riverside Fairways) with:
- Description of proposed change
- Rationale for change
- Visual mockups or examples
- Implementation timeline

### Approval Workflow
1. Submit request to brand owner
2. Approval review (1–2 business days)
3. Implementation with approved assets
4. Guideline updates if change is approved

### Quarterly Brand Audits
Review all materials for compliance, document brand usage, and suggest refinements based on market response.

---

## 10. Resources & Asset Management

### Logo Files

**Currently supplied:**
- `brand/riverside-fairways-logo.png`: full lockup with tagline, Fairway Green,
  3600 x 1942, transparent background

**Still needed.** These are referenced throughout this guide but do not exist yet:
- Reversed / Cream version (the primary web variant on a dark site)
- Icon only (golf flag) for favicons, avatars, and app icons
- Monochrome black for single-colour print
- Vector source (SVG, AI, or EPS). Only a raster PNG has been supplied, which
  limits large-format print and clean scaling

### Brand Color Swatches
- **Live source of truth:** Elementor > Site Settings > Global Colors (kit 1368)
- **CSS tokens:** `website/css-tokens.css`, mirrored from `website/rf-stylesheet.css`
- Pantone matches: not yet specified. Needed before any large print run
- Digital swatches (Adobe, Figma): not yet produced

### Typography
- DM Sans and Bad Script, both from Google Fonts, already loaded by the site
- Type hierarchy specifications (see §2)
- Web font embed handled by the Elementor kit, no manual embed needed

### Templates
- Website template (HTML/CSS)
- Email template
- Presentation template (PowerPoint)
- Social media templates (1200×628, 1080×1080, 1080×1920)

### Brand Asset Library
Location: [To be provided]  
Access: [To be determined]  
Update Frequency: Quarterly  

---

## 11. Contact & Support

**Brand Owner:** Christy Browning  
**Title:** Riverside Fairways  
**Email:** jase@riversidefairways.com  
**Phone:** +1 (225) 978-2363

**Questions or clarifications about brand usage?** Contact Christy directly.

---

## 12. Changelog

### Version 2.0, August 1, 2026

Version 1.0 documented a light theme with a palette that the live site never
used. This version was reconciled against the deployed Elementor kit (id 1368)
and the supplied logo artwork.

**Corrections:**

| Item | v1.0 said | Verified reality |
|---|---|---|
| Logo green | #5A8F7B | **#5D7D72**, sampled from the logo file. #5A8F7B appears nowhere in the artwork |
| Theme | Light, white and ivory backgrounds | **Dark.** Live site background is #111111 |
| Primary typeface | Segoe UI / Helvetica Neue | **DM Sans**, plus Bad Script for accents |
| Green on Ivory contrast | "5.2:1 — WCAG AA compliant" | **3.30:1, fails AA for normal text.** The claim was wrong |
| CTA buttons | Primary Green with white text | White on #5A8F7B is only **3.72:1**. Buttons now use Deep Green #306553 at 6.75:1 |
| Em dashes | "Use for emphasis or pause" | **Do not use.** Now matches the blog house standard |
| Body text | Charcoal on white | Body Cream #EDE7DC on near-black |

**Still outstanding:**

- Vector logo source and the reversed, icon, and monochrome variants
- Pantone matches for print
- Confirmation of the 14 games in the Feral package. The three blog posts
  originally named cornhole, basketball, and darts, which could not be verified
  against any supplied document

---

## Appendix: Quick Reference Checklist

Use this checklist when creating branded materials:

- [ ] Logo properly sized with adequate clear space
- [ ] Colors match exact hex values, taken from the Elementor kit
- [ ] Typography follows hierarchy guidelines
- [ ] Voice is friendly, not corporate jargon
- [ ] Copy uses active voice and contractions
- [ ] Photography is professional and people-focused
- [ ] Imagery is well-lit and reads correctly on a dark background
- [ ] Tagline/messaging aligns with key messages
- [ ] All text meets accessibility contrast requirements
- [ ] Design reflects luxury and approachability
- [ ] Material is reviewed against these guidelines
- [ ] Brand owner approval obtained before publication

---

---

**End of Brand Guidelines Document**

*Version 2.0 | August 1, 2026 | Next Review: November 1, 2026*
