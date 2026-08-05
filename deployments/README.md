# Deployment Files for Riverside Fairways

These files fix the black background issue on the homepage (post ID 1204).

## Files

1. **00-rf-fix-black-bg.php** — Standalone fix (original, comprehensive logging)
2. **01-rf-rest-fix-handler.php** — REST API endpoint wrapper
3. **02-functions-snippet.php** — Code snippet for theme functions.php

## Quick Deploy

**Via WP Engine Dashboard:**
1. Upload `00-rf-fix-black-bg.php` to `wp-content/mu-plugins/`
2. Refresh the homepage
3. Optionally delete the file after fix

**Full Instructions:**
See `DEPLOYMENT-BLACK-BG-FIX.md` in the parent directory

## Testing

After deployment, verify no black backgrounds appear on:
https://riversidefair.wpenginepowered.com/
