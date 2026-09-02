---
name: elementor-loop-taxonomy-filter
description: "Elementor Pro loop-grid taxonomy filter uses post_query_include + post_query_include_term_ids, keyed by term_taxonomy_id"
metadata: 
  node_type: memory
  type: reference
  originSessionId: ad14a3f9-2842-47f1-bcab-f7d39732352c
  modified: 2026-08-02T22:07:25.216Z
---

To filter an Elementor Pro `loop-grid` by taxonomy when writing `_elementor_data`
directly, set **both**:

```php
"post_query_include"          => ["terms"],
"post_query_include_term_ids" => [ $term->term_taxonomy_id ],
```

Two traps:

- There is **no** `post_query_<taxonomy>_ids` control. Guessing that name fails
  silently — the grid renders every post instead of erroring.
- The value is **term_taxonomy_id**, not term_id. Elementor resolves it with
  `get_term_by( 'term_taxonomy_id', ... )`. They happen to be equal on fresh
  terms, so a wrong assumption can pass by luck and break later.

Confirm control names by introspecting rather than guessing:

```php
$w = \Elementor\Plugin::$instance->widgets_manager->get_widget_types( 'loop-grid' );
$w->get_controls();   // grep for term/tax/include
```

Relationship filtering (MB Relationships) has no native equivalent — that needs
`post_query_query_id` plus an `elementor/query/<id>` PHP hook.

Related: [[wpengine-cache-before-verifying]]
