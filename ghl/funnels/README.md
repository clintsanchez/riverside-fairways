# Funnel — Date Request

Matches riversidefairways.com's design system (DM Sans + Bad Script, deep green
on ivory, pill buttons, 22–28px radii, soft shadows) while staying
**client-agnostic**: every business fact is a `{{custom_values.*}}` merge field
and the two brand colours come from the six Global Custom Colors (`config/brand_colors.json`), read in a script and applied as CSS variables.
For Riverside, fill the values and it *is* their site. For the next client, it's
a colour + logo swap.

Pushed as data with `build/build_funnel_page.py` (autosave endpoint, see BROWSER-RECIPES) into the Date Request funnel in the template and every client copy.

## Pages

| # | Page | File | Purpose |
|---|---|---|---|
| 1 | Request Your Date | `01-request-date.html` | THE landing page: hero, how it works, packages, why us, request form, review proof strip, FAQ, service area. Form feeds workflow 1. |
| 2 | Got It | `02-thank-you.html` | Sets the expectation: no date is held yet; a person confirms. |

Both pages deliberately **do not** embed the `EVENT - Unit Booking` calendar. The
only calendar link anywhere is `{{custom_values.booking_page_url}}`, which the
operator points at the **Discovery Call** widget.

## Design tokens (from the live site's `--rf-*` block)

| Token | Value | Snapshot mapping |
|---|---|---|
| primary green | `#306553` | `{{ brandboards.brand_primary }}` |
| dark | `#111111` | `{{ brandboards.brand_secondary }}` |
| green bright | `#9CC4AD` | `{{ brandboards.brand_accent }}` |
| bone / charcoal | `#FBFAF8` / `#242424` | `brand_background` / `brand_text` |
| green light / bright | `#7BA691` / `#9CC4AD` | derived |
| green deep / hover | `#24503F` / `#3C7A64` | derived |
| cream / bone | `#F5EFE5` / `#FBFAF8` | fixed |
| charcoal / graphite | `#242424` / `#1A1A1A` | fixed |
| font | DM Sans | fixed |
| script accent | Bad Script | fixed |
| radii | sm 12 · md 22 · lg 28 · pill 999 | fixed |

`Color 1` / `Color 2` are base custom values already present in the template, so
the funnel picks up brand colour with no new values.

## Form fields (build in GHL Forms, embed in page 1)

The form must **collect, not just acknowledge** — research finding #3. Each maps
to a custom field that already exists.

| Form field | Custom field | Required |
|---|---|---|
| First name / Last name / Email / Phone | standard | ✅ |
| Event date | `Event Date` | ✅ |
| Is that date flexible? | `Event Date Flexible?` | ✅ |
| What kind of event? | `Event Type` | ✅ |
| Roughly how many guests? | `Guest Count` | ✅ |
| Venue name | `Venue Name` | |
| Venue address or city | `Venue Address` | ✅ |
| Indoors or outdoors? | `Indoor or Outdoor` | ✅ |
| Preferred start time | `Event Start Time` | |
| Is there a standard outlet nearby? | `Power Access Confirmed?` | |
| Anything we should know about access? | `Access Notes` | |
| How did you hear about us? | `How Did You Hear About Us?` | |
| SMS consent | `B-018-COI. SMS Optin` | ✅ |

Submit → tag `book-date-requested` → workflow 1 fires → redirect to page 2.

## Images

The live site's photography is Riverside's own (poolside event, clubhouse lawn
at sunset, patio dinner party). **Do not ship those in the snapshot** — they're
client-specific and hosted under Riverside's WordPress. The HTML uses a neutral
gradient hero with an image slot; drop the client's photos in at deployment.
