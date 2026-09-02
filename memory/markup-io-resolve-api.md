---
name: markup-io-resolve-api
description: "markup.io comments are resolved via ~/bin/markup.py resolve — the Public API IS enabled; POST /threads/<id>/resolve, and it rate-limits at ~40 writes"
metadata:
  type: reference
---

Marking client review comments complete is scriptable — no browser automation,
no clicking. `~/bin/markup.py` (workspace key at `~/.config/markup/api-key`)
now has a `resolve` subcommand I added 2026-09-01:

```
markup.py boards --all                       # board id + open count
markup.py resolve <board> "1,3,5-17,56"      # comment NUMBERS, not thread ids
markup.py resolve <board> "4" --unresolve    # reversible
markup.py resolve <board> "..." --dry-run
```

**The Public API is enabled on the BlakSheep workspace.** The older Tiger Town
note saying it 403s `"Public API is not enabled"` is stale (June 2026) — it cost
me a wrong answer to Clint this session. Verify before repeating it.

Endpoint shape, found by probing:
- `POST /api/v2/threads/<id>/resolve` → 200. Also `/unresolve`.
- `PATCH` and `PUT` on `/threads/<id>` both **404** — markup.io uses bare POSTs
  to action sub-paths, not resource updates.

**It rate-limits writes.** ~40 rapid POSTs earns `429 TOO_MANY_REQUESTS`, and
the limiter stays hot for ~a minute afterward — a plain retry immediately 429s
again. `post()` now backs off exponentially and the batch loop sleeps 0.4s
between writes. Backup of the pre-patch script: `~/bin/markup.py.bak-*`.

Comment `number` in the JSON export maps 1:1 to the thread `id` from the API, so
an export and a live thread list can be cross-referenced by number safely.

Related: [[wpengine-cache-before-verifying]]
