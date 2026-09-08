# Riverside Fairways — Project Handoff

**Updated**: 2026-09-08
**Status**: Website live · GoHighLevel CRM built and tested · waiting on five client answers

---

## Read this first

Two tracks run in this repo:

| Track | Where | State |
|---|---|---|
| **Website / brand** | `website/`, `brand/`, `01-Brand-Assets/`, `deployments/` | Live. The August black-background fix is below. |
| **GoHighLevel CRM** | `ghl/` — start with `ghl/DEPLOYMENT.md` | Built, tested end to end, in the client's hands. |

---

## GoHighLevel CRM

**Sub-account `Riverside Fairways` = `8Dc5dXota6CblTBsNy2k`**, built 2026-09-04
from the `Mobile Event Rental` snapshot. Full build log, test results and every
defect found: **`ghl/DEPLOYMENT.md`**.

What it does: a date request (site form, text or call) triggers an auto-reply,
an owner alert and a task to check the unit calendar. Operator confirms the date
→ quote → agreement → signature → deposit invoice → **date held**. Balance goes
out a week ahead, an event-day sheet two days ahead, and a review-gated survey
after. Eight branded documents, a QR guest waiver, missed-call text-back, an AI
chat responder and an owner dashboard.

### Blocked on the client — five answers

These are in the email drafted at `ghl/client-email-2026-09-04.md` (a Gmail
draft is queued; **not yet sent**):

1. **Google review link** — the happy-customer path is built and idle without it.
   Needs their Business Profile to finish verification.
2. **Phone number** — new local number, or port the existing one.
3. **Payments** — Stripe (or the built-in processor) must be connected before any
   deposit or balance invoice can actually be paid.
4. **Setup time** — documents currently read "about ___ before your start time."
5. **Insurance statement** — one line for venues that ask.

Nine further custom values are blank but lower stakes: cancellation and
reschedule policy summaries, average rating, review count, years in business,
peak season note, referral and repeat-customer offers, lead email.

### Fixed 2026-09-07

**Broken logo in every email.** The business profile `logoUrl` was empty and the
`Logo URL` custom value pointed at an SVG on their WordPress that returns 403 to
any request without a browser User-Agent — which is how email clients and
Gmail's image proxy fetch. SVG also does not render in email at all. Rendered a
PNG, hosted it in GHL media, set both fields. Detail in `ghl/DEPLOYMENT.md`.

**Rule that came out of it:** never point `Logo URL` at the client's own site.

### Open, not blocked

- **Workflow email steps not yet checked for `{{location.*}}`.** The template had
  7 such steps; the fix is not applied here. Riverside's profile has name and
  email, so those resolve — likely cosmetic, but unverified. Needs a Firebase
  browser token (`ghl/build/extract_workflows.py --token-help`).
- **Riverside is on the v1 snapshot lineage.** The reusable template has since
  moved to `Mobile Event Rental v18 (2026-09)` = `dT317DkPHCLJxyp3CdqA` in
  ghl-toolkit. Re-basing is a decision, not a task.

---

## Black Background Fix — Status

**Issue**: Homepage (post ID 1204) displays unintended black (#000000) backgrounds in Elementor containers/sections.

**Root Cause**: Elementor post meta `_elementor_data` contains black background colors in element settings that need to be replaced or cleared.

**Solution**: Four deployment options available (see DEPLOYMENT-BLACK-BG-FIX.md):

1. **Option 1 - WP Engine Dashboard** (EASIEST)
   - Upload `00-rf-fix-black-bg.php` to `wp-content/mu-plugins/`
   - Script auto-executes on load
   - No coding required

2. **Option 2 - WP-CLI via SSH** (FASTEST)
   - Requires SSH access to WP Engine server
   - Run: `wp eval-file /path/to/fix-elementor-black-bg.php`

3. **Option 3 - Theme Functions** (PERMANENT)
   - Add snippet from `02-functions-snippet.php` to theme `functions.php`
   - Runs automatically on admin init
   - Prevents future occurrences

4. **Option 4 - REST API Endpoint** (AUTOMATED)
   - Upload `01-rf-rest-fix-handler.php` as mu-plugin
   - Access via: `https://riversidefair.wpenginepowered.com/wp-json/rf-fix/v1/black-bg`

**Files Ready for Deployment**: `/deployments/`
- `00-rf-fix-black-bg.php` — Standalone fix script
- `01-rf-rest-fix-handler.php` — REST API wrapper
- `02-functions-snippet.php` — Theme hook snippet
- `README.md` — Quick reference

**Next Action**: Choose a deployment method and execute one of the four options above.

---

## Novamira MCP Connection Status

**Issue**: Attempted direct execution via Novamira WordPress MCP endpoint, but encountered:
- Missing MCP-Session-Id header (requires active session from Novamira client)
- Upload endpoint requires authentication token
- Cannot establish direct PHP execution without proper MCP session context

**Workaround**: Deployment scripts created for manual/UI-based deployment instead.

---

## Project File Locations

| File/Folder | Purpose |
|------------|---------|
| `00-Client-Brief.md` | Full client intake documentation |
| `DESIGN.md` | Stitch design system spec (TOKENS, colors, typography) |
| `brand-style-guide.md` | Brand guidelines (colors, voice, usage rules) |
| `website/css-tokens.css` | CSS custom properties (brand colors, fonts, sizing) |
| `website/` | Website source files (HTML, assets, etc.) |
| `deployments/` | **← Black background fix scripts (ready to deploy)** |
| `DEPLOYMENT-BLACK-BG-FIX.md` | Full deployment instructions |
| `01-Brand-Assets/` | Logos, colors, imagery |
| `tools/` | WordPress utilities and scripts |

---

## Contact & Credentials

**Client**:
- Contact: Christy Browning
- Phone: +1 225-978-2363
- Email: jase@riversidefairways.com
- Facebook: https://www.facebook.com/riversidefairways

**BlakSheep Account Manager**:
- Clint Sanchez (clint@blaksheepcreative.com)

**WordPress Site**:
- URL: https://riversidefair.wpenginepowered.com
- Host: WP Engine
- Admin: WP-admin via username/password in CREDENTIALS.local.md or password manager

---

## Next Steps Checklist

### Immediate (This Week)
- [ ] Deploy black background fix using one of the 4 options
- [ ] Verify homepage displays correctly post-fix
- [ ] Test responsive design on mobile/tablet
- [ ] Clear browser and Elementor caches

### Short-term (Next Week)
- [ ] Complete public records verification
- [ ] Optimize remaining homepage sections
- [ ] Set up analytics (Google Analytics, FB Pixel)
- [ ] Create SEO metadata (meta descriptions, OG tags)

### Medium-term (2-3 Weeks)
- [ ] Build priority pages (Services, Pricing, Contact)
- [ ] Create blog/news section (if applicable)
- [ ] Set up email subscription/lead capture
- [ ] Schedule social media content

### Before Launch
- [ ] Full QA testing (desktop, mobile, browsers)
- [ ] Performance optimization (images, CSS, JS)
- [ ] Security audit (SSL, form submissions, backups)
- [ ] Client sign-off and approval

---

## Notes for Next Agent/Session

1. **Black Background Fix** is NOT yet deployed — check if it has been done since 2026-08-05
2. **Deployment files are ready** in `/deployments/` — just need to execute one of the 4 options
3. **Novamira MCP connection works for queries** but direct PHP execution requires proper session context
4. **All brand/design assets are prepared** — refer to DESIGN.md for tokens/colors
5. **Client contact method**: Email (jase@riversidefairways.com) or phone +1 225-978-2363

---

## Document Version History

| Date | Changes | Status |
|------|---------|--------|
| 2026-08-05 | Initial handoff created; black background fix prepared; deployment guide written | READY FOR DEPLOYMENT |

---

**URGENT**: Deploy black background fix using Option 1 (WP Engine Dashboard) if not yet completed.
