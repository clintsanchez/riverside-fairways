---
name: ghl-profile-write-needs-agency-token
description: PUT /locations/{id} needs the agency PIT — a location token returns 401 "not authorized for this scope"
metadata:
  type: reference
---

Writing a sub-account's business profile (`PUT /locations/{id}` — name, address,
`logoUrl`) is refused by that location's own Private Integration token:

```
401 {"statusCode":401,"message":"The token is not authorized for this scope."}
```

It succeeds with `GHL_PIT_AGENCY`. Send `companyId` and `name` in the body along
with whatever field is changing.

**Why:** the location PIT reads the profile fine, so the failure only shows on
write and reads like a bad request rather than a scope problem.

**How to apply:** reach for the agency token for anything under `/locations/`
itself. Location PITs cover the resources *inside* a sub-account (contacts,
workflows, custom values, media), not the sub-account record.

Related: [[ghl-logo-url-never-client-site]]
