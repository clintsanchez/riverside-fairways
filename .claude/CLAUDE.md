# Riverside Fairways — Project Instructions for Claude Code

This is the working repo for **Riverside Fairways**, a BlakSheep Creative client. Build
their website and marketing collateral here. Onboarded 2026-08-01 from the GHL
BSC Onboarding Survey.

## Who this is
- **Contact:** Christy Browning · +12259782363 · jase@riversidefairways.com
- **Website:** _not provided_ · **Facebook:** https://www.facebook.com/riversidefairways
- **What they do:** We are a mobile golf simulator; great for corporate events, casual events, weddings, parties, etc. We also offer a “Feral” package that includes a variety of 14 additional simulator games; greats for kids parties.
- **Differentiator (lead with this):** We are fully mobile and can set up anywhere we have access to electricity (access to wifi is a plus but not required).
- **GHL contact (source of truth):** `ZDpvIwxxH3Ow40GOomEa`

## Source of truth
Read these first; keep them current as the engagement evolves:
- `../.agents/product-marketing.md` — positioning, ICP, voice. **The canonical doc.**
- `../00-Client-Brief.md` — full intake brief.
- `HANDOFF.md` — current status + open confirmations. **Read when resuming.**
- `../aib/` — Agency-in-a-BOX client files (also synced to the AiB vault).

## Brand
- **Colors (client-described):** primary Moody green, secondary Ivory, accent _not captured_ — **sample exact hex from the logo in `../brand/` before using.**
- **Voice:** Friendly / Approachable, Luxury / Sophisticated, Casual / Conversational
- **Do NOT mention:** No politics please
- Design system spec: `../DESIGN.md` (Stitch) · tokens: `../website/css-tokens.css` · guide: `../brand-style-guide.md`. Keep all three in lockstep.
- **For brand work, use the `brand-guidelines` skill** — sample hex from the logo
  in `../brand/`, then run it to produce the full brand guideline (accessibility-
  checked colors, type hierarchy, logo rules, voice samples, compliance
  checklist). Write its output to `../brand-style-guide.md`; keep `../DESIGN.md` +
  `../website/css-tokens.css` in sync with its palette.

## APIs / connections
- **WordPress:** fill `../.env` from `../.env.example`; client helpers in `../tools/wp/` (`python3 ../tools/wp/wp.py ping` to test). WP MCP block in `../.mcp.json`.
- **GHL:** this client's contact id is in `../.env` (`GHL_CONTACT_ID`); shared PIT/location creds live in the ghl-toolkit `.env`.
- **Credentials:** hosting/domain logins from onboarding are in `../CREDENTIALS.local.md` (gitignored, 0600). **Move them to a password manager and delete the file.**

## 🚨 Accuracy guardrail (do not skip)
Before publishing ANY public claim, verify against authoritative records (see
`../06-Reports/records-check.md`): license status/class, years in business
(Less than 1 year), and registered address vs. service area. Never fabricate
reviews, credentials, or experience claims. Safe fallback for unconfirmed
numbers: "decades of combined experience."

## Next steps
1. Move credentials to a password manager; delete `../CREDENTIALS.local.md`.
2. Collect/sample brand assets → fill `../DESIGN.md` / `../website/css-tokens.css` / `../brand-style-guide.md`.
3. Run the public-records check.
4. Create the design system in Stitch from `../DESIGN.md`.
5. SEO suite → homepage → priority pages.
