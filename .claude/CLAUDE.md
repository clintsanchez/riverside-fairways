# Riverside Fairways — Project Instructions for Claude Code

This is the working repo for **Riverside Fairways**, a BlakSheep Creative client. Build
their website and marketing collateral here. Onboarded 2026-08-01 from the GHL
BSC Onboarding Survey.

## Who this is
- **Contact:** Christy Browning · +12259782363 · jase@riversidefairways.com
- **Website:** _not provided_ · **Facebook:** https://www.facebook.com/riversidefairways
- **What they do:** We are a mobile golf simulator; great for corporate events, casual events, weddings, parties, etc. We also offer a “Feral” package that includes a variety of 14 additional simulator games; greats for kids parties.
- **Differentiator (lead with this):** We are fully mobile and can set up anywhere we have access to electricity (access to wifi is a plus but not required).
- **GHL contact (source of truth):** `ZDpvIwxxH3Ow40GOomEa`

## Source of truth
Read these first; keep them current as the engagement evolves:
- `../.agents/product-marketing.md` — positioning, ICP, voice. **The canonical doc.**
- `../00-Client-Brief.md` — full intake brief.
- `HANDOFF.md` — current status + open confirmations. **Read when resuming.**
- `../aib/` — Agency-in-a-BOX client files (also synced to the AiB vault).

## Brand
- **Colors (client-described):** primary Moody green, secondary Ivory, accent _not captured_ — **sample exact hex from the logo in `../brand/` before using.**
- **Voice:** Friendly / Approachable, Luxury / Sophisticated, Casual / Conversational
- **Do NOT mention:** No politics please
- Design system spec: `../DESIGN.md` (Stitch) · tokens: `../website/css-tokens.css` · guide: `../brand-style-guide.md`. Keep all three in lockstep.
- **For brand work, use the `brand-guidelines` skill** — sample hex from the logo
  in `../brand/`, then run it to produce the full brand guideline (accessibility-
  checked colors, type hierarchy, logo rules, voice samples, compliance
  checklist). Write its output to `../brand-style-guide.md`; keep `../DESIGN.md` +
  `../website/css-tokens.css` in sync with its palette.

## APIs / connections
- **WordPress:** fill `../.env` from `../.env.example`; client helpers in `../tools/wp/` (`python3 ../tools/wp/wp.py ping` to test). WP MCP block in `../.mcp.json`.
- **GHL:** this client's contact id is in `../.env` (`GHL_CONTACT_ID`); shared PIT/location creds live in the ghl-toolkit `.env`.
- **Credentials:** hosting/domain logins from onboarding are in `../CREDENTIALS.local.md` (gitignored, 0600). **Move them to a password manager and delete the file.**

## 🚨 Accuracy guardrail (do not skip)
Before publishing ANY public claim, verify against authoritative records (see
`../06-Reports/records-check.md`): license status/class, years in business
(Less than 1 year), and registered address vs. service area. Never fabricate
reviews, credentials, or experience claims. Safe fallback for unconfirmed
numbers: "decades of combined experience."

## 🚨 Writing `_elementor_data` — read this BEFORE touching Elementor JSON

`_elementor_data` is one big **escaped-JSON string** in `postmeta`. Corrupting it makes the
page render header + footer only, with no body and no error. These rules are not optional.

**Read / write the raw bytes.**
- Read with `$wpdb->get_var("SELECT meta_value FROM {$wpdb->postmeta} WHERE post_id=%d AND meta_key='_elementor_data'")`.
  **Never `get_post_meta()`** — it unslashes and you lose the escaping.
- Write with `$wpdb->update`/`$wpdb->insert`. **Never `update_post_meta()`** — it runs
  `wp_slash()` and re-escapes what is already escaped.
- **Never `json_decode` → modify → `json_encode`.** Round-tripping rewrites the escaping of
  the entire document. Treat it as a string and `str_replace` on it.
- Validate with `json_decode($raw) !== null` (PHP) or `json.loads()` (Python) **before**
  writing back. That check is the whole safety net.
- Pass payloads into PHP as **base64(json)** to sidestep shell/Python→PHP quoting entirely.

**The four things that silently corrupt it:**
1. ⚠️ **Raw newlines.** A literal `\n` or `\r` byte inside a JSON string value is an illegal
   control character. `json_decode` returns null and Elementor's
   `get_builder_content_for_display()` returns `""`. When injecting multi-paragraph HTML,
   join with `</p><p>` and **zero newlines** — never `"</p>\n<p>"`.
2. **Unescaped forward slashes.** Escape `/` → `\/` in injected HTML to match how Elementor
   stores it. But check first: this data mixes plain `</p>` and escaped `<\/p>`. Count both
   (`raw.count('</p>')` vs `raw.count('<\\/p>')`) before building a string anchor, or your
   insert lands at offset 0 — valid JSON, but inside no widget, so it renders nothing.
3. **Literal double quotes** in injected text. Use none.
4. **Assuming spacing.** Values are stored with spaces after colons
   (`"background_overlay_image": {"id": 123,`). A regex without `\s*` matches nothing and
   fails silently.

**After ANY raw write, bust all four caches or you will verify stale output:**
```php
delete_post_meta($pid, '_elementor_element_cache');   // ← the one everyone forgets
delete_post_meta($pid, '_elementor_page_assets');
delete_post_meta($pid, '_elementor_css');
wp_cache_delete($pid, 'post_meta'); clean_post_cache($pid);
(new \Elementor\Core\Files\CSS\Post($pid))->update();
```
Editing `_elementor_data` does **not** invalidate `_elementor_element_cache`. The old widget
HTML stays cached and a perfectly correct edit renders stale — even when the element-cache
experiment reads as `inactive`, because the meta still exists and is still served.

**Then purge WP Engine** (`riversidefair.wpenginepowered.com`) before verifying anything:
```php
do_action('wpe_purge_varnish_cache_all');
WpeCommon::purge_varnish_cache(); WpeCommon::purge_memcached();
\Elementor\Plugin::$instance->files_manager->clear_cache();
```
A verified-correct DB write plus a correct `WP_Query` will still serve the *old* markup
otherwise, which reads exactly like a broken query. Suspect cache before suspecting code.
Do **one** cache clear at the end of a batch, not one per item — rapid back-to-back flushes
saturate WPE's PHP workers and produce a site-wide 500 that self-recovers in minutes.

**Loop-grid taxonomy filters** need *both* controls, keyed by **`term_taxonomy_id`** (not
`term_id` — they match on fresh terms and diverge later):
```php
"post_query_include"          => ["terms"],
"post_query_include_term_ids" => [ $term->term_taxonomy_id ],
```
There is no `post_query_<taxonomy>_ids` control; guessing that name renders every post
instead of erroring. Introspect rather than guess:
`\Elementor\Plugin::$instance->widgets_manager->get_widget_types('loop-grid')->get_controls()`.

**Backgrounds:** Elementor builds section-background CSS from the attachment **`id`**, not
the `url` string. Swapping only the URL changes nothing on the rendered page. Verify by
reading `uploads/elementor/css/post-<id>.css` **on disk** — an HTTP fetch hits the CDN cache.

**Fixing an already-broken page:** `str_replace(["\r\n","\n","\r"], '', $raw)` — clean
Elementor JSON contains no raw newlines, so stripping all of them is safe. Confirm
`json_decode !== null`, write back, then run the cache-bust block above.

## Next steps
1. Move credentials to a password manager; delete `../CREDENTIALS.local.md`.
2. Collect/sample brand assets → fill `../DESIGN.md` / `../website/css-tokens.css` / `../brand-style-guide.md`.
3. Run the public-records check.
4. Create the design system in Stitch from `../DESIGN.md`.
5. SEO suite → homepage → priority pages.
