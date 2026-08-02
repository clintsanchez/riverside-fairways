repo: clintsanchez/riverside-fairways
branch: main

## Last sync
date: 2026-08-01T14:24:00Z

### Updated in this project
- Built the full token set from `brand-style-guide.md` (the upstream `css-tokens.css` still holds `#______` placeholders).
- Extracted reversed, ivory, black and flag-icon variants from the single supplied logo PNG.
- Authored the seven components named in `DESIGN.md` plus a `Logo` wrapper.
- Recreated the marketing site described in `DESIGN.md` as a five-screen UI kit.

## Screen map

| Project file | Built from |
|---|---|
| `tokens/colors.css` | `brand-style-guide.md` §Color Palette, `website/css-tokens.css` |
| `tokens/typography.css` | `brand-style-guide.md` §Typography, `DESIGN.md` §Typography |
| `tokens/spacing.css`, `tokens/radius.css` | `website/css-tokens.css`, `DESIGN.md` §Spacing & Layout |
| `assets/*` | `brand/riverside-fairways-logo.png` |
| `components/core/*`, `components/layout/*` | `DESIGN.md` §Components |
| `guidelines/*.card.html` | `brand-style-guide.md` / `brand-style-guide.html` |
| `ui_kits/website/*` | `DESIGN.md`, `.agents/product-marketing.md`, `00-Client-Brief.md` |
| `readme.md` §Content fundamentals | `brand-style-guide.md` §4, §7, `aib/brand-voice.md` |
