# UI kit — Riverside Fairways marketing site

A click-through recreation of the marketing site described in `DESIGN.md` in the
source repo (hero + section + card + header/footer inventory). **No live site
exists yet** — this kit is the design-system reading of that spec, not a copy of
a shipped product.

## Screens
| File | Screen | Notes |
|---|---|---|
| `HomeScreen.jsx` | Home | Photo hero, what-we-do split, event grid, stat row, quote band |
| `PackagesScreen.jsx` | Packages | Three tiers, featured middle card, add-ons |
| `EventsScreen.jsx` | Events | Alternating media/text rows for the four event types |
| `AboutScreen.jsx` | About & service area | Narrow measure prose, dark-green contact band |
| `BookScreen.jsx` | Get a quote | Form, package chips, success state |

`shared.jsx` pulls the components off the bundle and holds the shared data
(`PACKAGES`, `EVENTS`, `NAV`) plus the `Photo` placeholder.

## Known gaps
- **No photography was supplied.** Every image well renders a labelled warm-neutral
  placeholder. Drop real event photos in and swap `<Photo>` for `<img>`.
- **No pricing.** The source says "tiered packages with available add ons" but
  names no tiers or rates. Package names and inclusions here are illustrative
  scaffolding — confirm with the client before publishing.
- Only one product surface exists (marketing site). No app, docs or dashboard
  is described anywhere in the source repo, so none is invented here.
