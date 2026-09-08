---
name: ghl-logo-url-never-client-site
description: Host email logos in GHL media, never the client's own site — theirs 403s bots and serves SVG, both fail silently in email
metadata:
  type: project
---

Riverside's `Logo URL` custom value pointed at
`riversidefairways.com/.../riverside-fairways-logo.svg`. Every GHL email
rendered a broken logo. Two independent causes:

1. **403 without a browser User-Agent.** WordPress (or a security plugin)
   blocks bot-like requests. Email clients and Gmail's image proxy fetch exactly
   that way. It loads fine in a browser, so it looks healthy.
2. **SVG does not render in email.** Gmail, Outlook and Apple Mail all refuse
   it. Even a 200 would have shown broken.

Fix: render to PNG, upload via `POST /medias/upload-file`, set the URL in both
the `Logo URL` custom value **and** the business-profile `logoUrl` (templates
read `{{location.logo_url}}` from the profile, not the custom value).

**Why:** the failure is invisible from inside GHL — the value is filled, the URL
opens in your browser, and nothing errors. Only a plain no-UA fetch reveals it.

**How to apply:** before trusting any image URL in GHL email, fetch it with no
User-Agent and confirm 200 plus a raster content-type. Prefer GHL media
(`assets.cdn.filesafe.space`) over any client-hosted asset.

Related: [[ghl-profile-write-needs-agency-token]]
