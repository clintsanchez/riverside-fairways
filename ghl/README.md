# Riverside Fairways — GoHighLevel CRM

The client's live CRM build: pipeline, workflows, documents, billing, forms.
Moved here from `ghl-toolkit` on 2026-09-08 with its git history intact.

**Sub-account `Riverside Fairways` = `8Dc5dXota6CblTBsNy2k`**, created 2026-09-04
from snapshot `Mobile Event Rental v1`. Target slug `riverside`
(`GHL_LOCATION_ID_RIVERSIDE` + `GHL_PIT_RIVERSIDE`).

## Files

| Path | What it is |
|---|---|
| `DEPLOYMENT.md` | **Read first.** Full build log, test results, defects found and fixed, open items. |
| `client-email-2026-09-04.md` | Client status email — the five outstanding asks. |
| `billing-ids.json` | Product / price / invoice-template ids in their account. |
| `billing-workflows.json` | Generated spec for workflows 31–34 (quote → deposit → balance). |
| `docs-workflows.json` | Generated spec for workflows 35–38 (waiver, venue sheet, COI, receipt). |
| `products.json` | Packages and add-ons with prices. |
| `users.json` | Account users (workflow task assignees). |
| `guest-waiver-qr.png` | QR code for the on-site waiver sign. |
| `build/` | Copies of the builder scripts — see the warning below. |

## Running the builders

Credentials come from a local `.env` (never committed). Every script takes
`--target riverside` and **refuses to write without `--live`** — dry run is the
default.

```bash
python3 ghl/build/patch_workflows.py --target riverside --fixes <fixes.json>
python3 ghl/build/build_workflows.py --target riverside --live
```

`extract_workflows.py` additionally needs `GHL_TOKEN_ID`, a Firebase token from a
logged-in browser session (`--token-help`); it lasts about an hour.

## ⚠️ build/ is a COPY, not the source of truth

These scripts are maintained in **`ghl-toolkit/build/`** and shared across every
client. They are duplicated here so this repo can be worked on standalone.

**A fix made here does not reach other clients, and vice versa.** Before relying
on one for anything that matters, diff it against ghl-toolkit:

```bash
diff -r ghl/build ~/Documents/Claude/Projects/GHL/build
```

This bit before: `fix_templates.py` had rules that *introduced*
`{{location.email}}` / `{{location.name}}` into email templates — merge fields
that render blank in a cloned sub-account. Fixed in ghl-toolkit 2026-09-07. A
stale copy would have reinstated it.

## The template this came from

The reusable snapshot lives in `ghl-toolkit/snapshots/event-rental/` —
`Mobile Event Rental v18 (2026-09)` = `dT317DkPHCLJxyp3CdqA`. **Riverside is
still on the v1 lineage** and has not been re-based onto v18.
