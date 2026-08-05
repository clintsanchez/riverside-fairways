# Riverside Fairways — Black Background Fix Deployment

**Issue**: Homepage (post ID 1204) displays unintended black (#000000) backgrounds in Elementor sections/containers.

**Status**: Fix scripts created and ready for deployment.

**Timeline**: 2026-08-05

---

## Quick Fix Options

### Option 1: Via WP Engine Dashboard (RECOMMENDED)

1. **Log into WP Engine** → Select the Riverside Fairways site
2. **Access WP Admin** → Themes or mu-plugins area
3. **Upload as mu-plugin**:
   - Go to wp-content/mu-plugins/ (create folder if missing)
   - Upload: `00-rf-fix-black-bg.php`
   - Refresh the homepage in browser
   - The script auto-executes and fixes all black backgrounds
   - Delete the file after running (optional, safe to leave)

### Option 2: Via WP-CLI (If You Have SSH Access)

```bash
# SSH into WP Engine server
ssh [your-wpe-account]@[site-id].wpenginepowered.com

# Navigate to WordPress root
cd wordpress

# Run the fix
wp eval-file /path/to/fix-elementor-black-bg.php
```

### Option 3: Add to Theme Functions (If You Have Theme Access)

1. Connect to WP Engine via SFTP or wp-admin editor
2. Edit wp-content/themes/[your-theme]/functions.php (or child theme)
3. Add the code from `02-functions-snippet.php` at the end
4. Save the file
5. Visit wp-admin to trigger the hook

### Option 4: Use REST Endpoint (If Custom Plugin Is Active)

1. Upload `01-rf-rest-fix-handler.php` as a mu-plugin
2. Visit this URL: `https://riversidefair.wpenginepowered.com/wp-json/rf-fix/v1/black-bg`
3. You should see: `{"success":true,"fixed_count":N,"message":"Fixed N black background(s)..."}"`

---

## What Each Fix Does

| File | Method | Deployment | Best For |
|------|--------|-----------|----------|
| **00-rf-fix-black-bg.php** | Standalone script with auto-detection | mu-plugin upload | One-time fix, detailed logging |
| **01-rf-rest-fix-handler.php** | REST API endpoint | mu-plugin upload | Integration with automation |
| **02-functions-snippet.php** | Theme hook (admin_init) | Theme functions.php | Always-on protection, runs once |

---

## How It Works

1. **Retrieves** Elementor JSON data from post 1204 meta (`_elementor_data`)
2. **Scans** all elements recursively for black color values (#000000, #000, rgb(0,0,0))
3. **Replaces** black backgrounds with empty string (transparent)
4. **Clears** Elementor caches:
   - Transients: `elementor_1204_css`, `elementor_1204_meta`
   - Post cache: `elementor_post_1204`
   - Global Elementor cache
5. **Reports** number of fixes applied

---

## Verification

After deployment:

1. Visit `https://riversidefair.wpenginepowered.com/` (homepage)
2. Open browser DevTools → Elements/Inspector
3. Search for `background.*#000` or `background-color: #000`
4. Should find **zero** matches (or expected background-color values only)
5. Check page appears visually correct (no black overlays)

---

## Safety Notes

- **Non-destructive**: Replaces black with transparent (no design loss)
- **Post-specific**: Only affects post ID 1204 (homepage)
- **Idempotent**: Safe to run multiple times (only fixes if needed)
- **Cache-aware**: Clears all relevant caches after fix
- **Reverts easily**: Just restore from DB backup if needed

---

## If Issues Occur

### "No black backgrounds found"
- Homepage may already be fixed
- Issue may be CSS-based, not Elementor JSON
- Check page display visually anyway

### "Fix ran but page still looks black"
- Clear browser cache: `Ctrl+Shift+Del` (hard refresh)
- Clear Elementor cache: wp-admin → Elementor → Settings → Clear Cache
- Check CSS files for hardcoded black backgrounds outside Elementor
- May be a different element/section with the issue

### "Cannot upload file to WP Engine"
- Contact WP Engine support to enable file upload
- Use SSH + WP-CLI method instead
- Try different mu-plugin filename (00-, 01-, etc.)

---

## Deployment Checklist

- [ ] Back up WordPress database (WP Engine Dashboard → Backups)
- [ ] Choose deployment method (Options 1-4 above)
- [ ] Download appropriate fix file from this directory
- [ ] Deploy/upload file following chosen method
- [ ] Verify homepage displays correctly
- [ ] Confirm no black backgrounds appear
- [ ] (Optional) Delete temporary fix file if using mu-plugin
- [ ] Clear browser cache if needed

---

## Files Included

- **00-rf-fix-black-bg.php** — Standalone fix script (original from tools/)
- **01-rf-rest-fix-handler.php** — REST API endpoint wrapper
- **02-functions-snippet.php** — Theme hook snippet for functions.php
- **This file** — Deployment guide

---

## Contact

For questions or issues:
- Client Contact: Christy Browning (+1 225-978-2363 or jase@riversidefairways.com)
- BlakSheep Creative: Clint Sanchez (clint@blaksheepcreative.com)

---

**Last Updated**: 2026-08-05
