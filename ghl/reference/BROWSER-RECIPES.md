# Driving the GHL UI

Hard-won notes from building a survey and a workflow by automation. Most of the
time here went into discovering these; none of it is guessable.

## Use Playwright, not a browser extension

Extension-based drivers (BrowserMCP and friends) are sandboxed out of
cross-origin iframes. Every interesting GHL builder lives in one, so the
accessibility tree comes back with three useless nodes and clicks time out.

Playwright drives Chrome over the DevTools Protocol and reads inside those
frames. It is the difference between "cannot see the page" and "can address
every control".

```
claude mcp add playwright -s user -- npx @playwright/mcp@latest
```

It launches its own browser, so you log into GHL once inside it. Restart the
session afterwards — MCP tools load at startup.

## Frame names

| Surface | Frame | URL |
|---|---|---|
| Survey / form builder | `survey-builder-app` | `/v2/location/{loc}/survey-builder-v2/{id}` |
| Workflow list + builder | `workflow-builder` | `/automation/workflow/{id}` — **singular**, the list uses `/workflows/` |

The workflow builder will not load from a direct `/workflows/{id}` link. Open
the list, then click through.

## Prefer capturing the save payload over clicking

The single most useful trick. Most GHL builders serialize their whole document
into one request on Save. Capture it, rewrite the JSON, POST it back — far
faster and far more reliable than driving the UI.

The survey builder posts everything to `POST /surveys/{id}` with a `token-id`
header. Its `formData.slides[].slideData[]` holds every question, each carrying
`Id` (the custom field id), `label`, and `required`. Rewriting that array moved
22 fields across 5 slides, set every label and every required flag, in one call
— after an hour of failing to do it by dragging.

```js
let body = null;
page.on('request', r => {
  if (r.method() === 'POST' && /\/surveys\/ID/.test(r.url())) body = r.postData();
});
await frame.getByRole('button', { name: 'Save' }).click();
// ...edit JSON, then replay with the captured headers:
await page.request.post(url, { headers: captured.headers, data: JSON.stringify(edited) });
```

Replay from `page.request`, not `page.evaluate` — a fetch from the page origin
is blocked by CORS.

## Target custom fields by id, never by name

An account can hold 200+ custom fields with near-identical names. In the
field-picker each row is:

```html
<div class="cf-row-wrap" data-field-id="euB0HeK5b0HyIJcc739h">
  <div class="n-checkbox" role="checkbox" aria-checked="false">
```

So select by the id you read from the API, and assert `aria-checked` flipped:

```js
await frame.evaluate((id) => {
  const row = document.querySelector(`.cf-row-wrap[data-field-id="${id}"]`);
  row.querySelector('.n-checkbox[role=checkbox]').click();
}, fieldId);
```

This is the difference between a mapping you can trust and one that silently
binds the wrong field. A wrong mapping does not error — GHL saves it, the
client fills the form, and the answer is discarded with no log.

Two gotchas: the picker only renders rows for **expanded** groups, so click any
`.n-collapse-item:not(.n-collapse-item--active) .n-collapse-item__header` first;
and long search terms miss — search 2–3 words, not a whole question.

## Drag needs real mouse movement

Palette items use pointer-event drag (`standard-draggable-container`,
`draggable="false"`), not HTML5 DnD. Playwright's `dragTo` does nothing. Press,
move in several steps, pause, release:

```js
await m.move(x1, y1); await m.down();
await m.move(400, 600, { steps: 10 });
await m.move(x2, y2, { steps: 10 });
await page.waitForTimeout(300); await m.up();
```

## Element toolbars float

The gear / duplicate / trash icons appear at the selected element's top-right
and move with it. Read the element's bounding box and click relative to it —
a fixed coordinate hits duplicate instead of delete, which is how you end up
with a "(copy)" of a field.

Opening a properties panel shifts the canvas left, moving those icons again.

## Verify with the API, never the UI

A "published" banner is not proof. One publish click in this project silently
flipped a workflow back to draft; only the REST API showed it. After any build:

```
GET /workflows/?locationId={loc}          → status
GET /surveys/?locationId={loc}            → exists
GET /locations/{loc}/customFields         → mappings
```

## Known API oddities

- `POST /proposals/templates/send` wants **`templateId`**, plus `contactId` and
  `userId`. Its 422 complains that `documentId` is missing — that name belongs
  to a different validator and sending it fails identically.
- Workflow steps and triggers are not in the workflow document. They live in
  Firebase Storage behind `fileUrl` / `triggersFilePath`; `fileUrl` is fetchable,
  the triggers file needs a signed URL.
- Custom field names may carry leading spaces. Normalize before matching or a
  field that exists reads as missing — and creating it then fails on a taken
  fieldKey.
- The internal API (`backend.leadconnectorhq.com`, `token-id` + `channel: APP`)
  can create a workflow shell via `POST /workflow/{loc}`, but the step-writing
  endpoints from public write-ups return 404. Build steps in the UI.

## Reading workflows as data

`build/extract_workflows.py` dumps every workflow in a sub-account — including
the full step tree — to JSON. The public API returns only metadata, so this uses
the internal API plus a browser Firebase token.

```
export GHL_TOKEN_ID="..."          # python build/extract_workflows.py --token-help
python build/extract_workflows.py --target grow --out snapshots/grow/workflows.json
```

Each step carries its real config: `add_contact_tag` has its tags,
`internal_update_opportunity` its pipeline and stage, `email` its subject and
body, and `transition` marks branch arms ("Opportunity Found" / "Not Found").
That is enough to read a snapshot you did not build, diff two accounts, or use a
working workflow as the spec for rebuilding it elsewhere.

Two notes: the token is scoped per user/location — the script refuses if it does
not cover the target, because otherwise it silently returns the wrong account's
data. And a workflow with no step tree is normally just empty or draft.

## Pipelines: the UI's own save is a public-shaped PUT

The pipeline stage editor (`/opportunities/pipeline/{id}?tab=stages`) saves with
`PUT https://services.leadconnectorhq.com/opportunities/pipelines/{id}` carrying
the whole `{name, stages[], showInFunnel, showInPieChart, useOpportunityProbability}`
document, authenticated with the browser `token-id` + `channel: APP` +
`source: WEB_USER` (a PIT does not work here - the public API has no pipeline
write). Replaying it from `page.request` with extra stages (fresh v4 UUID `id`,
no `originId`) and rewritten `position`s adds and reorders stages in one call.
`DELETE` on the same route removes a pipeline. Verified 2026-09-03 building the
Event Bookings pipeline: 7 renames + 5 inserts + 1 delete, then confirmed via
`GET /opportunities/pipelines` with the location PIT.

## Workflow builder: never send page-level keyboard shortcuts

`page.keyboard.press('ControlOrMeta+A')` + `Backspace` intended for a TipTap
message editor landed on the canvas instead, selected every node, and opened
"Are you sure you want to delete 11 selected nodes?" (10 actions + 1 trigger).
Nothing persists until the workflow is saved, but a later scripted "Save" would
have committed it. Rules:
- Type only via frame-scoped locators (`frame.locator(...).fill()/type()`),
  never `page.keyboard`.
- Before every click, check `frame.locator('.hr-modal-mask').count()`; a mask
  means a modal is up. Read `.hr-modal-container` text and choose Cancel unless
  the modal is the thing you meant to trigger.
- Typing `{{` in the message editor opens the custom-values picker
  (`.cv-slash-suggestion-popup`) which intercepts clicks; Escape closes it but
  also reverts the edit. Merge fields are stored as raw `{{...}}` text - edit
  them via the save payload, not the editor.

## Workflows: steps ARE writable - through the builder's own PUT

The step-writing endpoints from public write-ups 404, but the builder itself
persists with `PUT https://backend.leadconnectorhq.com/workflow/{loc}/{wfId}`
carrying the whole document; `GET` on the same URL returns it including
`workflowData.templates` (the step tree). Auth is the session's
`authorization: Bearer <jwt>` (a different token from the Firebase `token-id`)
plus `channel: APP`, `source: WEB_USER`. Add `modifiedSteps: [ids]`,
`deletedSteps: []`, `createdSteps: []`, `triggersChanged: false`. Merge fields
are stored as raw `{{...}}` text. `build/patch_workflows.py` does this from a
fixes JSON; 2026-09-03 it rewrote 53 steps across 8 workflows in one run, the
builder reloaded them cleanly, and the public API still reported `published`.
"Save action" in the UI only calls `/validate-assets` + `/validate-workflows`;
only the header Save writes.

## Workflows: creating them whole, as data (2026-09-03)

`build/build_workflows.py` builds workflows from a JSON spec. Endpoints, all on
`backend.leadconnectorhq.com` with the session bearer + `channel: APP` +
`source: WEB_USER`:

- `POST /workflow/{loc}` with `{name, status:"draft", workflowData:{templates:[]}, ...}` -> `{id}`
- `POST /workflow/{loc}/trigger` with `{type, name, conditions, workflowId, status:"draft",
  masterType:"highlevel", actions:[{type:"add_to_workflow", workflow_id}], active:true}` -> `{id}`.
  Omit `workflowId` and the trigger is created orphaned and unreachable.
- `PUT /workflow/{loc}/{id}` with the full doc, `createdSteps:[ids]`, `triggersChanged:true`,
  `newTriggers:[...with ids]`. Last step's `next` must be `""` (not null - 400).
- `DELETE /workflow/{loc}/{id}` works.

Shapes that bit: task `dueDate.unit` accepts `days`, not `hours`; wait
`{type:"appointment", appointmentCondition:"skip", appointmentStartAfter:{when, type:"day"|"hour", value}}`
anchors to the enrolling appointment; the Custom Date Reminder trigger has **no**
before/after offset (it fires on the date, `offsetDays` is ignored) - anchor
T-minus logic to an appointment instead. Internal SMS notification bodies live at
`attributes.sms.body`, not `attributes.body`. `create_opportunity` needs `fields: []`.
GHL names can contain non-breaking spaces (`5.\xa0Closed Sale`) - normalise before
matching. And never name a zsh loop variable `path`.

## Forms: create via POST /forms/, save via POST /forms/{id} (2026-09-03)

The v2 form builder creates with `POST https://services.leadconnectorhq.com/forms/`
`{locationId, productType:"form", source:"landing_page"}` and saves the whole
document with `POST /forms/{id}` `{name, formData:{form:{fields:[...], formAction,
style, ...}}}` - auth is the browser Firebase `token-id` + `channel: APP` +
`source: WEB_USER` + `Version: 2021-07-28` (a PIT gets 401). Standard fields are
`{label, tag, type, standard:true, required, ...}`; custom fields embed the full
custom-field record (`Id`, `fieldKey`, `dataType`, `picklistOptions`...) plus
`type = dataType.lower()`, `tag = Id`, `hiddenFieldQueryKey = fieldKey tail`.
`build/build_form.py` rewrites a captured base document from a spec. The read
right after a save can lag a few seconds - reads on both hosts caught up on retry.

## Funnels: shell + step are plain POSTs; page content is the hard part (2026-09-03)

`POST https://backend.leadconnectorhq.com/funnels/funnel/create` `{locationId, name, type:"funnel"}`
-> `{id}`, then `POST /funnels/funnel/create-step` `{step:{id:<uuid>, name, url:"<path>",
pages:[], type:"optin_funnel_page", split:false, control_traffic:100}, funnelId}` -> creates the
funnel_pages document too. Both use the Firebase `token-id`. The page editor
(`page-builder.leadconnectorhq.com`, frame `funnel-builder`) has no Save button when
autosave is off; Publish is blocked until a domain exists; palette elements are
drag-only. Content-as-data was not cracked in this session - the pages are pasted
in the UI (funnels/*.html) or hosted on the client's WordPress instead.

## Funnel page content: POST /funnels/builder/autosave/{pageId} (2026-09-03)

The page builder persists the whole page with
`POST https://backend.leadconnectorhq.com/funnels/builder/autosave/{pageId}`
`{funnelId, pageData:{sections, settings, general, pageStyles, trackingCode, popups, ...}, pageVersion, pageType:"draft", manualSave, integrations}`
(Firebase `token-id`). Read it back with `GET /funnels/builder/page/data?pageId=`.
A section > 1-column row > column > element `{meta:"custom-code", tagName:"c-custom-code",
extra.customCode.value:"<html>"}` renders arbitrary HTML. `build/build_funnel_page.py`
re-ids a captured base tree and injects a file. Gotchas: an empty `pageData` is
rejected (422) so the tree must contain at least one section; the page palette
defines `--primary`/`--secondary`, so custom CSS must not reuse those names; the
`</>` toolbar panel is page-level Tracking Code (`pageData.trackingCode.headerCode`
/ `footerCode`) and its textareas are header-first. The Quick Add palette opened
from the canvas "+" is click-to-insert (the side palette is drag-only).

## Snapshot create (agency UI, captured 2026-09-03)

Snapshot *creation* has no public endpoint, but the agency UI posts:

```
POST https://backend.leadconnectorhq.com/snapshots-appengine/v2/snapshots?companyId={companyId}
authorization: Bearer <agency session JWT>   channel: APP   source: WEB_USER   version: 2021-07-28
{
  "name": "Mobile Event Rental v1 (2026-09)",
  "location_id": "<source sub-account>",
  "company_id": "<companyId>",
  "exemptClone": ["google_ad_campaigns", ... asset types with nothing selected ...],
  "selectedAssets": { "calendars": ["<id>", ...], "teams": [...], "workflow": [...], ... }
}
```

Response (200) is the snapshot record with `type: "own"` and
`dehydrationStatus: {state: "processing", completed, total}` — poll
`python3 ghl_snapshots.py list` until it settles. The UI's select-all
checkbox only covers the *visible* page of each category; verify with the
search box per category (n/n) before clicking Create. Toast:
"Snapshot creation initiated successfully".

## Deleting base-snapshot junk as data (captured 2026-09-04)

All take the Firebase `token-id` + `channel: APP` + `source: WEB_USER`.

```
DELETE https://services.leadconnectorhq.com/forms/{formId}?locationId={loc}      (Version: 2021-07-28)
DELETE https://services.leadconnectorhq.com/surveys/{surveyId}?locationId={loc}  (Version: 2021-07-28)
POST   https://backend.leadconnectorhq.com/funnels/funnel/folder/delete
       {"id": "<folderId>", "locationId": "<loc>", "userId": "<userId>"}
       -> deletes the folder AND every funnel/website inside it
```

There is no `DELETE /funnels/funnel/{id}` on either host (404). Folder ids
come from `GET /snapshots/v2/preFetchAssets/{loc}?companyId=&assetType=funnels`
(entries with `type: "directory"`) or the funnels list.

## Snapshot asset inventory (agency, bearer)

```
GET https://backend.leadconnectorhq.com/snapshots/v2/preFetchAssets/{loc}?companyId={co}&assetType=<type>
GET https://backend.leadconnectorhq.com/snapshots/assets/asset-names?locationId={loc}&companyId={co}   # list of types
GET https://backend.leadconnectorhq.com/snapshots-appengine/snapshot/{snapshotId}/get_assets?type=own&companyId={co}  # what a snapshot holds
```
`preFetchAssets` is what the create/refresh modal uses; iterate the types from
`asset-names` and you have every selectable id, which is how to build a truly
complete `selectedAssets` instead of trusting the modal's select-all.

## Snapshot silently drops imported workflows (found 2026-09-04)

A workflow whose document has `originType: "snapshot"` (it came in through an
*imported* snapshot such as the Skool Home Services pack) is **never** written
into a snapshot you create from that sub-account. The asset shows as selected,
the create/refresh request returns 200, `dehydrationStatus` completes, and the
workflow just isn't in `get_assets` or on the pushed sub-account. Nothing in
the UI says so. `originType`/`originId` are ignored by the builder's PUT, so
the only fix is `build/clone_workflows.py`: recreate each one as a user-origin
workflow (new shell → copy triggers → PUT steps with fresh ids), rewrite every
`add_to_workflow`/`remove_from_workflow` reference, then delete the originals.

Validator rules the clone script had to satisfy on *new* steps that the
originals got away with: every referenced node needs `parentKey` (and legacy
docs carry `parent`, which must not be null — set it to the referencing node,
or drop it on the root); leaf `next` must be `""` not null; `create_opportunity`
needs `fields: []`; a trigger whose `conditions` name a form/survey that no
longer exists fails the whole PUT ("Referenced asset(s) missing") — strip the
dead ids from `value` (list or scalar) first.

Trigger endpoints: `GET /workflow/{loc}/trigger?workflowId=` returns the full
trigger incl. `conditions`; `DELETE /workflow/{loc}/trigger/{triggerId}` works.
Pipelines, custom values, tags, calendars and email templates from the imported
base were NOT dropped — only workflows carry this restriction (so far).

Snapshot refresh as data:
```
POST https://backend.leadconnectorhq.com/snapshots-appengine/v2/snapshots/{snapshotId}/refresh?companyId={co}
{"extras": {"exemptClone": [<types with nothing selected>], "selectedAssets": {<type>: [ids]}}}
```
Bearer + channel/source/version headers. `python3 ghl_snapshots.py load <snap> <loc> --override`
then re-pushes (it prompts for the location id on stdin).

## Private Integration token by Playwright (2026-09-04)

`/v2/location/{loc}/settings/private-integrations` → "Create new integration" →
name + description → Next → `#scopes-select` is a multi-select whose options
are `.hr-base-select-option` (virtualised; click each unselected one and
scroll `.hr-virtual-list`) → Create → confirm the "sensitive scopes" dialog.
The token appears once in the page text (`pit-…`) and in the 201 response of
`POST /marketplace/private-integration/location/{loc}` (`activeToken`).

## Trigger update as data

`PUT /workflow/{loc}/trigger/{triggerId}` with the full trigger record (from
the GET list) plus `workflowId`, `location_id`, `company_id`, `company_age`,
`triggersChanged: true`. Used to add `message.status == no-answer` to the
Missed Call Text Back `call_status` trigger without opening the builder.

## Calendars after a snapshot push (Riverside test, 2026-09-04)

What the snapshot does NOT carry, so every client deploy must redo it:
- `isActive` comes through **false** — `PUT /calendars/{id} {"isActive": true}`
  (public API, location PIT). Booking against an inactive calendar returns
  "Calendar is inactive".
- `openHours` comes through empty. Format that the public API accepts is ONE
  DAY PER ENTRY: `[{"daysOfTheWeek":[0],"hours":[{"openHour":6,"openMinute":0,"closeHour":23,"closeMinute":0}]}, ...]`
  (a multi-day `daysOfTheWeek` list → 422 "must be a valid day of week").
- `teamMembers` are gone — add users, then per-user **schedules**. Free slots
  = calendar hours ∩ each staff member's weekly schedule, and new users default
  to weekdays only, so weekend events show *no slots* even with 7-day hours.
  The UI (Calendar > Availability > Bulk edit > Edit hours) saves
  ```
  PUT https://backend.leadconnectorhq.com/calendars/schedules/{scheduleId}   (token-id)
  {"rules":[{"day":"sunday","type":"wday","intervals":[{"from":"8:0","to":"23:0"}]}, ...],
   "name":"<scheduleId>","timezone":"America/Chicago","calendarIds":["<calendarId>"]}
  ```
  one schedule per user per calendar; `GET /calendars/schedules/{id}` reads it.
- Equipment resources are not snapshot assets — recreate (`POST /calendars/resources/equipments`).

Booking guard behaviour (verified with real POSTs): overlaps against a
*confirmed* appointment are rejected ("slot no longer available"), the
`slotBuffer` (90 min) is enforced, a gap booking is accepted. BUT
`ignoreFreeSlotValidation: true` skips the equipment guard entirely and a
no-show/cancelled appointment frees its slot. Operators must not use
"ignore availability" when booking the unit.

## Workflow findings from the same test
- `task-notification` with `assignedTo: ""` creates nothing, silently → `build/assign_tasks.py`.
- An `appointment` trigger without a `calendar.id` condition fires for EVERY
  calendar — the base "Call Confirmation" emailed "your call is confirmed" when
  the unit was booked. Fixed with `calendar.id is-any-of [consult calendars]`.
- Internal-notification emails to a custom address make GHL auto-create a
  contact for that address (source NOTIFICATION).
- Shared/trial LC number: SMS went `queued` for the first few, then `failed`.

### User schedules, resolved (2026-09-04)
`GET /calendars/schedules/search?locationId=&isDefault=true` lists each user's
default weekly schedule; `...&calendarId=` lists calendar-specific overrides.
A schedule only applies to the calendars in its `calendarIds`. A calendar with
no schedule covering a user falls back to Mon–Fri — that is why consult
calendars showed no Saturday slots even after the default rules gained
Saturday. Fix as data: `PUT /calendars/schedules/{id}` with
`{"rules": [...], "name", "timezone", "calendarIds": [<all calendars the user
works>]}` — no `userId`/`locationId` in the body (422). New users' defaults
must be extended per client; do it right after `add_users.py`.

## Documents & Contracts templates as data (2026-09-04)

`build/build_document.py`. Endpoints (Firebase `token-id` + channel/source +
`Version: 2021-07-28`; the location PIT is rejected on the single-template GET/PUT):
```
POST /proposals/templates                {name, type:"proposal", locationId, isPublicDocument:false}
GET  /proposals/templates/{id}?locationId=
PUT  /proposals/templates/{id}           full body — strip _id/__v/createdAt/updatedAt/type/version/
                                         isPublicDocument/versionHistory/…; `timezone` must be an object
```
Pages are 816×1056 with 48 margins; elements are absolutely positioned in
page-relative px. A single Text element per page holding the section HTML works
(h1/h3/p/ul/strong render; `<table>` is stripped, use label/value paragraphs).
Fillable fields = Signature / DateField / TextField elements (recipient
`assignedContact`) plus matching `fillableFields` entries.

Merge tags render at send time: `{{contact.<field_key>}}` (custom contact
fields, dates prettified, money as $900.00) and `{{custom_values.<key>}}` —
verified on the public sendlink.co page. Sending as data (location PIT works):
`POST /proposals/templates/send {locationId, templateId, contactId, userId, sendDocument:true}`
→ `links[0].referenceId` → `https://sendlink.co/documents/v1/<referenceId>`.
`DELETE /proposals/document/{id}?locationId=` removes a sent document.
`documents_contracts` is a snapshot asset type.

## Documents in workflows (captured 2026-09-04)

Action step (insert as data in the workflow PUT; `workflowsActionType` is
required or the validator says "corrupted type"):
```json
{"type":"proposals_estimates_send_document","workflowsActionType":"INTERNAL","name":"3b - Document: Event Rental Agreement",
 "attributes":{"userId":"<sender user>","templateId":"<documents template id>","sendDocument":"true","medium":"email","type":"proposals_estimates_send_document"}}
```
Trigger (POST /workflow/{loc}/trigger): `type: "proposal_estimate_update"`,
`masterType: "internal"`, `workflowsTriggerType: "INTERNAL"`, conditions
`status == SIGNED` (values: SENT / VIEWED / SIGNED / COMPLETED / DECLINED) and
`documentCreatedByTemplateId == <template id>`. The UI filter list shows
"Status" (document) *and* the contact custom field "Agreement Status" — pick the
first.

## Importing a shared snapshot (2026-09-04)

Vendor "import" links are tracking redirects to
`https://affiliates.gohighlevel.com/?fp_ref=…&share=<shareId>` → the app opens
`/snapshots/imported?share_id=<shareId>` with an "Import snapshot" modal. Confirming posts
`POST https://backend.leadconnectorhq.com/snapshots/share/v2/redeem/<shareId>?companyId=<co>`
`{"snapshotName": "..."}` (bearer). Bare `app.gohighlevel.com/?share=<id>` just lands on the
agency dashboard — use the affiliates URL form. Resolve a tracking link with
`curl -sL -o /dev/null -w '%{url_effective}'` (HEAD returns 405).

## Survey conditional logic: reference fields by ID, redirect to a literal (2026-09-04)

Rules in `formData.form.conditionalLogic[].conditions[].selectedField` must be
the element's **id** (the custom field id, e.g. `2VkInhWkcpySwRw1FXti`), not
its `hiddenFieldQueryKey`. Query-keyed rules save fine and never evaluate:
show/hide does nothing and `disqualifyLead` never fires, so the "disqualified"
trigger branch is dead. Because the id differs per sub-account, every pushed
copy of a survey needs its rules re-pointed at the local field id (the
snapshot does not remap them).

`disqualifyLead` with `disqualifyAction: openUrl` needs a **literal URL** in
`outcome.value`; a `{{custom_values.*}}` tag is not rendered and the widget
just reloads itself. Verified: literal → browser navigates after submit and
the submission record carries `disqualified: true`. Test surveys from a
fresh page with localStorage cleared, otherwise the widget resumes the
previous session.

## Chat widget as data (captured 2026-09-04)

All `token-id` + `channel: APP` + `source: WEB_USER` + `Version: 2021-07-28`.

```
GET  /chat-widget/list?locationId=&limit=&offset=       (settings here are partial)
GET  /chat-widget/data/{loc}/{widgetId}                 full record incl. settings
POST /chat-widget/   {locationId, name, chatType:"liveChat", version:2, default:true, settings}
     -> 201, but settings are ignored on create; follow with
PUT  /chat-widget/data/{loc}/{widgetId}  {settings:{...}, updatedBy:<userId>}   (rename: {name:...})
```

`GET /chat-widget/{id}` is 403 and `PUT /chat-widget/{id}` is 404. Merge
tags inside settings are not rendered by the widget: keep them in the
template copy (`config/chat_widget.json`) and substitute literals per client.
`chat_widget` is a snapshot asset type.

## Snapshot refresh auth (2026-09-04)

`POST /snapshots-appengine/v2/snapshots/{id}/refresh?companyId=` returns 401
on `services.` with `token-id`; use `backend.leadconnectorhq.com` with the
agency session `authorization: Bearer` (same as create). Body
`{"extras":{"exemptClone":[...],"selectedAssets":{type:[ids]}}}`.

## Dashboards as data (captured 2026-09-04)

The dashboard editor talks to `backend.leadconnectorhq.com/reporting/…` with the
agency session bearer **plus** `token-id`, `x-reporting-api-version: 3` and
`version: 2021-04-15`. Without `x-reporting-api-version` every write is
`409 dashboard_version_error` no matter what version you send.

```
GET  /reporting/dashboards?locationId=                 defaultDashboardId, dashboard[] (mine), sharedDashboards[]
GET  /reporting/dashboards/{id}?locationId=            dashboard{__v}, widgets[], dashboardWidgets[{widgetId, layout}]
GET  /reporting/dashboards/widgets-definitions          catalog: definitions[module][], layoutProperties, groups, dateProperty…
POST /reporting/dashboards            {title, locationId, isPrivate:false}
POST /reporting/dashboards/{id}/permissions  {locationId, permission:[{role, permission}], isPrivate}
PUT  /reporting/dashboards/{id}       {title, activityBuffer:{create:[{<widgetId>: doc}], delete:[widgetId…]},
                                       layout:[{id:<dashboardWidgetId>, x,y,w,h,minW,minH,noResize,cellHeight:"54px"}],
                                       themeConfig, version:<dashboard.__v>}
DELETE /reporting/dashboards/{id}     body {locationId, version}
POST /reporting/dashboards/{id}/set-default  -> 403 set_default_dashboard_role_view_error for agency users, UI included.
```

Widget and placement ids are client-generated 24-hex ObjectIds. Data widgets:
`options.aggregations:[{operator, field}]`, `filters:[{group:"OR", filters:[{group:"AND", filters:[…]}]}]`
(an empty top-level list is "Invalid filters format"), `dateProperty` (custom date
fields as `custom_fields.<id>`), `dateRangeOverride:{operator}`,
`groupBy:{fields:["custom_fields.<id>.raw"], limit, orderBy}` — strings, the
front end wraps them — and tables need `tableProperties:{columns:[…], order,
orderBy, limit}` or every data call is a bare 400. Custom-field columns are
`customFields.<id>`. Because set-default is closed, rebuild **inside** the
location's default dashboard (`build_dashboard.py --into default`); the
snapshot then carries it as the default. `dashboards` is a snapshot asset.

## Custom-field folders and the contact detail view (2026-09-04)

```
POST /locations/{loc}/customFields/            {name, documentType:"folder", model:"contact"}  -> customFieldFolder.id
PUT  /locations/{loc}/customFields/bulk/parent {fieldIds:[…], parentId}
DELETE /locations/{loc}/customFields/{folderId}   (400 on stock folders or non-empty ones)
GET   services /contacts/views?locationId=  /contacts/views/{id}     id = default-view-{loc}
PATCH backend  /contacts/views/{id}   {schema}
```

Folders never appear in the field list; they are the distinct `parentId`
values (GET the id for the name). `schema.leftSection.topCard.customFields`
= field ids pinned under the contact name; `tabs.allFields.folders` = folder
order. `contact_detail_views` is a snapshot asset. The Opportunities board's
card fields are a per-user preference, not a location setting — not buildable.

## Global Custom Colors: brand palette as merge tags (2026-09-04)

Brand Boards > Global settings > Custom colors. Each color becomes a merge tag
`{{ brandboards.<key> }}` that builders store instead of a hex.

```
GET  services /brand-boards/custom-colors/{loc}?offset=0&limit=100&includeDeleted=false   -> customColors[{_id, name, key, rawKey, value}]
POST services /brand-boards/custom-colors/        {locationId, name, value:"#rrggbbaa", key}
PUT  services /brand-boards/custom-colors/{loc}/{id}  {name, value}
```
token-id + channel APP + source WEB_USER. `brand_custom_color` is a snapshot asset.

What actually happens with the tag, verified on the public survey and form:
- Forms: the submit element's `bgColor` / `color` hold the tag and the public
  form resolves it at render. Change the palette, the button changes.
- Surveys: `form.footerStyle.buttonStyle.*` holds the tag, but the public page
  paints from `form.footerStyle.computedStyles.styles` (and the mobile twin),
  a hex cache the builder writes on save. A palette change does not reach a
  survey until that cache is regenerated. `apply_brand_tags.py` writes the tag
  and the resolved hex together, so re-running it is the refresh.
- On save the builder links any color whose hex equals a palette value to that
  tag. Two palette entries with the same hex get cross-linked (Primary became
  `brand_secondary` when both were green). Keep values unique.
- Design Kit (the Brand Board itself) is a picker convenience only; its colors
  are copied as hex.

## Brand tags in funnel pages (2026-09-04)

`{{ brandboards.<key> }}` is substituted at render on `sites.leadconnectorhq.com`
pages (preview and published) in page text and inside `<script>` strings, but
**not inside `<style>` blocks** — a tag in a CSS rule comes through verbatim.
So the funnel pages read the tags in a small script and apply them as CSS
variables (`--rf-primary` etc.), guarded by a hex regex so an unresolved tag
leaves the stylesheet defaults. Values arrive as 8-digit hex (`#306553ff`),
which CSS accepts. Custom values render the same way, so the pages need no
per-client edits: palette + custom values = the client's site.

## Billing as data: estimate/invoice templates, workflow steps, estimate trigger (2026-09-04)

Public Invoices API (location PIT, `Version: 2021-07-28`):
```
POST /invoices/template            {altId, altType:"location", name, currency, businessDetails{name,...}, items[{name, currency, amount, qty}], discount:{type:"percentage", value:0}, termsNotes}
POST /invoices/estimate/template   same + title, items[].type:"one_time" (productId/priceId optional)
GET  /invoices/template | /invoices/estimate/template   ?altId&altType&limit&offset -> data[]
DELETE /invoices/estimate/template/{id}   body {altId, altType}   (query params alone -> 422)
```
`discount` is mandatory even when zero. No deposit/partial-payment field on templates:
deposits are separate templates. Workflow steps (`workflowsActionType: INTERNAL`):
```
{"type":"payments_create_invoice",  "attributes":{"userId","templateId","liveMode":"true","action":"sms_and_email"}}
{"type":"payments_create_estimate", "attributes":{"userId","templateId","liveMode":"true","sendMode":"sendDirectly","action":"sms_and_email"}}
```
The Send Invoice / Send Estimate actions take only user, template, mode and channel:
amounts always come from the template, so per-package templates + an if/else on
the package field is the way to vary the amount. Trigger:
```
{"type":"estimate_update","masterType":"internal","workflowsTriggerType":"INTERNAL",
 "conditions":[{"operator":"==","field":"status","value":"accepted","title":"Estimate Status","type":"select","id":"status"}]}
```
Estimate status values: accepted, declined, invoiced, sent, viewed.

Estimate trigger filter on a specific template (captured 2026-09-04):
`{"operator":"==","field":"documentCreatedByTemplateId","value":"<estimate template id>","title":"Template","type":"select","id":"documentCreatedByTemplateId"}`.
If/else on a contact custom field (validated by the builder, displays as
`If "Package Interest" is "Tier 1 - Entry"`):
`{"conditionType":"contact_detail","conditionSubType":"<custom field id>","conditionOperator":"==","conditionValue":"Tier 1 - Entry","__customFieldType__":"custom"}`
inside `branches[].segments[].conditions[]` with `attributes.currentRecipeType:"CUSTOM"` and `conditionName`.
Correction (tested 2026-09-04): a custom-field condition must carry `__customFieldType__: "standard"`
(what the UI writes) — with `"custom"` the runtime resolves the field to '' and no branch runs.
The condition node also gets `version: 2` and `noneBranchName: "None"`; `build_workflows.py` sets both.
Verified live: two contacts with different Package Interest values took different branches.

## Documents set, waiver form, corporate quote (2026-09-04)

- Custom field `dataType: "SIGNATURE"` exists (`POST /locations/{loc}/customFields`); embedded in a
  form it renders a signature canvas on the public widget. Allowed dataTypes: TEXT, LARGE_TEXT,
  NUMERICAL, PHONE, MONETORY, CHECKBOX, SINGLE_OPTIONS, MULTIPLE_OPTIONS, FLOAT, TIME, DATE,
  TEXTBOX_LIST, FILE_UPLOAD, SIGNATURE, RADIO.
- The standalone form widget does NOT render `{{custom_values.*}}` inside the consent text — the
  waiver spec is fed a per-client copy with Business Name substituted.
- `POST /forms/` returns 201 with no id; find the new shell as the newest "Form 1".
- `GET /proposals/templates?locationId=&limit=20&skip=` — limit must be 21 or less, `offset` is refused.
- Task step `dueDate` = `{"duration": n, "unit": "days", "skipWeekends": false}`.
- Estimate template items: `qty` must be at least 0.1 (no zero-quantity "pick list" lines).
- Sent invoices: `POST /invoices/{id}/void` (delete is 400); estimates delete with body `{altId, altType}`.
- A workflow rebuilt from the template spec into a client keeps the TEMPLATE's custom-field ids and
  only fails later ("Referenced asset(s) missing"); remap ids by field name before any client PUT.

## Branding documents and forms (2026-09-04)

Documents & Contracts render Text elements through a sanitizer: `<div>`/`<span>` backgrounds,
`<img>`, `<table>` and paragraph-level `color:` are dropped, and `{{custom_values.*}}` inside a
style attribute is not resolved. What survives: `color:` on `<h1>`–`<h4>`, `<span>` and `<b>`;
bold/italic; lists. Elements have a native `responsiveStyles.large.backgroundColor` and there
is a native Image element (`src` must be a literal URL). Elements FLOW top to bottom in array
order; `position.top/left` is ignored. So `build_document.py` now builds a brand chrome from the
location's custom values at build time: Image (Logo URL) → Text band (Color 2 background,
white `<h2>` title, `<h4>` subtitle) → thin Color 1 band → body (headings recolored to Color 1)
→ footer band (business name/phone/email/website). Rebuild the documents when a client's logo
or colors change (`--template-id` keeps the id, so workflows stay wired).

Forms: `build_form.py` takes `header` (logo URL + title + subtitle rendered as an HTML header
element — the public widget does render `<img>` here, but not custom values, so the logo URL
and business name are substituted per client) and `style` (radius, button colors as brand
tags). Field borders, label fonts, padding and the pill button come from the same block.

## Interpreter note (2026-09-04)

When a shell starts with a bare PATH, `python3` resolves to Apple's 3.9 without `requests`/`dotenv`; the build scripts need `/usr/local/bin/python3` (`export PATH=/usr/local/bin:$PATH`).

