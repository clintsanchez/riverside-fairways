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

## The API tells you WHICH element was pinned — don't diff screenshots

`markup.py open <board> --all --json` returns `elements[0].path`, a CSS selector
for the exact element the client clicked:

```
 18  :nth-child(9) > img                                   # 9th gallery image
 26  .kk-sgallery > :nth-child(3) > img
 33  :nth-child(5) > .kk-acc__panel > p                    # 5th FAQ answer
 45  #kk-ppane-homes > .kk-pricing-grid > :nth-child(1) > .kk-pricing-item__img > img
```

That resolves every vague "remove this one" / "use this picture here" exactly.
The **JSON export has no coordinates at all**, so working from the export alone
you are guessing.

🩸 On Klutter Krewe (2026-09-02) I resolved 14 vague comments by diffing the
markup screenshots against each other — markup leaves a faint four-corner marker
on the pinned element, so an 8-pixel diff between two shots of the same viewport
reveals the box. It worked, and it agreed with the API on every image. But it
took most of an hour, and it got **two of them wrong**: comment 33 read like a
process paragraph so I put it in the detail block when the selector said the
fifth FAQ answer, and comment 1's pin was a home service card, not the blog card
I inferred. Pull the selectors first; keep the screenshot trick only for boards
where the API is unavailable.

Verify a fix landed by querying the same selector in Playwright — it is the
client's own definition of the target.

Related: [[wpengine-cache-before-verifying]]
