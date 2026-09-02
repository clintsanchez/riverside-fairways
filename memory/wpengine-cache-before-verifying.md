---
name: wpengine-cache-before-verifying
description: "Purge WP Engine page cache before verifying Elementor changes with Playwright, or you read stale HTML and misdiagnose"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: ad14a3f9-2842-47f1-bcab-f7d39732352c
  modified: 2026-08-02T22:07:16.105Z
---

On riversidefair.wpenginepowered.com, always purge the WP Engine page cache
after writing `_elementor_data` and before verifying the result in Playwright.

```php
do_action( 'wpe_purge_varnish_cache_all' );
WpeCommon::purge_varnish_cache();
WpeCommon::purge_memcached();
\Elementor\Plugin::$instance->files_manager->clear_cache();
```

Adding a cache-busting query param (`?cb=1`) also works for a quick check.

**Why:** Clearing only Elementor's file cache is not enough. A verified-correct
database write plus a correct server-side `WP_Query` still rendered the *old*
markup on the live page, which reads exactly like a broken query and sends you
looking for a bug that isn't there.

**How to apply:** Purge, then verify. If live output contradicts a write you
already confirmed in the database, suspect cache before suspecting the code.

Related: [[elementor-loop-taxonomy-filter]]
