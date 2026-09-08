# Email template renames — DONE 2026-09-07

**All 12 renamed by hand in the UI and verified via API: 12/12, zero issues.**
The three unreferenced templates were correctly left alone; still 15 templates
total; all 12 workflow bindings resolve; all bodies still free of `location.*`.
The table below is kept as the record of what maps to what.

The 12 live email templates still carry the **inherited base names**, while the
bodies are rewritten event-rental copy. That mismatch already caused one wrong
call: matching by name said all 15 were orphaned and safe to delete, when in
fact workflows bind them **by id** and deleting would have broken 5 workflows.

Rename them so the name says what the template is.

**There is no rename API.** Probed 2026-09-07 on both APIs:

| Attempt | Result |
|---|---|
| `POST /emails/builder/data` with `name` | 201, HTML written, **name silently ignored** |
| `PUT/PATCH /emails/builder/{id}` (public) | 404 |
| `PUT/PATCH /emails/builder/{loc}/{id}` (internal) | 404 |
| `PUT .../name`, `POST .../rename` (internal) | 404 |

So this is a UI pass: **Marketing → Emails → Templates**, ⋮ → Rename.

## The map

| Current name | Rename to | Used by |
|---|---|---|
| New Lead Confirmation | `1 - New Inquiry: request received` | 1. New Inquiry - Fast Five :: step 4 |
| Nurture Campaign: Email #1 | `15 - Nurture 1: three things to check` | 15. Nurture - Long Tail :: step 4 |
| Nurture Campaign: Email #2 | `15 - Nurture 2: how a date gets held` | 15. Nurture - Long Tail :: step 8 |
| Nurture Campaign: Email #3 | `15 - Nurture 3: indoors or outdoors` | 15. Nurture - Long Tail :: step 12 |
| Nurture Campaign: Email #4 | `15 - Nurture 4: if half your guests` | 15. Nurture - Long Tail :: step 16 |
| Nurture Campaign: Email #5 | `15 - Nurture 5: company or organization` | 15. Nurture - Long Tail :: step 20 |
| Nurture Campaign: Email #6 | `15 - Nurture 6: last one from us` | 15. Nurture - Long Tail :: step 24 |
| Appointment Confirmation Email | `2 - Call confirmed` | 2. Call Confirmation :: step 1 |
| 24 Hour Appointment Reminder | `2 - Call reminder: tomorrow` | 2. Call Confirmation :: step 3 |
| 1 Hour Before Appointment Reminder | `2 - Call reminder: 1 hour` | 2. Call Confirmation :: step 6 |
| No Show Appointment | `2b - Call no-show follow-up` | 2b. Call No-Show :: step 6 |
| Got Estimate / Follow-Up | `3 - Quote sent` | 3. Date Available :: step 3 |

Unreferenced, leave as-is (or delete): `New Lead Notification`,
`New Appointment Notification`, `Appointment Follow-Up`.

**Renaming is safe** — workflows bind by id, not name, so the bindings survive.
Confirmed by writing to an unreferenced template and re-reading: same id, 15
templates, HTML unchanged.

## Playwright cannot do this either (tried 2026-09-07)

Automated a logged-in persistent Chromium (`.pw-profile`, cookies saved, correct
sub-account). Navigation works — Marketing → Emails reaches
`/v2/location/{loc}/marketing/emails/templates` (note: **`/marketing/emails/`**,
not `/emails/`, which renders a blank page).

The template list lives in a cross-origin iframe, `name="emails-home"` on
`email-home-prod.leadconnectorhq.com`. Playwright reads into that frame fine —
per BROWSER-RECIPES that is exactly why Playwright beats extension drivers — but
**the app never initializes** in the automated browser. It mounts an empty
`<div id="app">` shell and stops. Console shows the cause:

```
GET https://backend.leadconnectorhq.com/locations/undefined/customFields   <- no location context
422  Error fetching users by location
firestore.googleapis.com .../Listen/channel   FAILED (x4)
```

The location id never reaches the iframe app, so it renders nothing to click.
Not a selector or timing problem — waited 30s+, reloaded, same result.

**So the renames are a manual UI pass.** Marketing → Emails → Templates, ⋮ →
Rename, per the map above. Roughly five minutes for all 12.
