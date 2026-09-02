---
name: elementor-container-should-render-is-fake
description: "elementor/frontend/container/should_render is NOT a real Elementor hook — it never fires; use a shortcode returning '' to conditionally render page sections"
metadata:
  type: reference
---

**`elementor/frontend/container/should_render` does not exist.** Verified against
Elementor 4.2.3 on 2026-09-01. A callback added to it **never fires**, silently.

Confirmed two ways:
1. Instrumented the filter and rendered a template — **0 calls**.
2. Grepped Elementor core for `apply_filters('*should_render*')` — the only match
   in the whole plugin is `elementor/element/should_render_shortcode`.

This bit twice in one session: an existing snippet already used it for
`rf-gallery-section` and `rf-steps-media`, so it looked like a proven pattern. It
is dead code, and always has been. Nobody noticed because all six Riverside
services happen to have both a gallery and a `how_it_plays_image`, so the
conditions it guards are always true. Copying it made an "optional" section
render on all six services with its fallback heading.

**The working pattern is a shortcode that returns `''`:**

```php
add_shortcode( 'rf_service_extra', function () {
    $body = trim( (string) get_post_meta( get_the_ID(), 'extra_body', true ) );
    if ( '' === $body ) { return ''; }
    return '<section class="rf-extra">…</section>';
} );
```

Put a `shortcode` widget in the template. The whole section — wrapper, heading,
spacing — lives in the shortcode, so nothing is left behind when it returns ''.
Do **not** wrap it in a styled container: an Elementor container renders its box
and margins even when its children output nothing.

Key on the **content field, not the heading** — headings usually carry a
`fallback` in the dynamic tag and are therefore never empty.

Related: [[rf-service-template-fields]], [[wpengine-cache-before-verifying]]
