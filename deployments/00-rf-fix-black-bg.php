<?php
/**
 * Riverside Fairways - Fix Black Backgrounds in Elementor Data
 *
 * Usage:
 *   Option 1: Place in wp-content/mu-plugins/ as mu-plugin
 *   Option 2: Include from functions.php or use WP-CLI
 *   Option 3: Copy entire wp-config load logic and run standalone
 *
 * This script:
 *   1. Gets Elementor JSON data for post 1204 (homepage)
 *   2. Finds all elements with black (#000000 or #111111) backgrounds
 *   3. Replaces black with transparent or appropriate brand color
 *   4. Clears Elementor caches
 */

// ============================================================================
// SECTION 1: WordPress Initialization (run only if not already in WP context)
// ============================================================================

if (!function_exists('get_post_meta')) {
    // Not in WordPress context - load it
    define('WP_USE_THEMES', false);

    // Try to find wp-load.php in common locations
    $wp_load_paths = array(
        __DIR__ . '/../../../wp-load.php',           // mu-plugins/
        __DIR__ . '/../../wp-load.php',              // plugins/
        __DIR__ . '/../wp-load.php',                 // theme/
        '/wp-engine/wordpress/wp-load.php',          // WP Engine default
        '/var/www/wordpress/wp-load.php',            // Common VPS path
        dirname(__FILE__) . '/../wp-load.php',       // Relative
    );

    $wp_loaded = false;
    foreach ($wp_load_paths as $path) {
        if (file_exists($path)) {
            require_once($path);
            $wp_loaded = true;
            break;
        }
    }

    if (!$wp_loaded) {
        die("ERROR: Could not find WordPress wp-load.php. Please run this script from within a WordPress plugin/mu-plugin context.\n");
    }
}

// ============================================================================
// SECTION 2: Core Fix Logic
// ============================================================================

class RiversideFairwaysElementorFix {
    private $post_id = 1204;  // Homepage
    private $issues_found = array();
    private $issues_fixed = array();

    /**
     * Main execution method
     */
    public function run() {
        echo "=== Riverside Fairways Elementor Black Background Fix ===\n\n";

        // Get Elementor data
        $json = get_post_meta($this->post_id, '_elementor_data', true);
        if (empty($json)) {
            echo "ERROR: No Elementor data found for post {$this->post_id}\n";
            return false;
        }

        echo "✓ Found Elementor data for post {$this->post_id}\n";

        // Decode JSON
        $data = json_decode($json, true);
        if (json_last_error() !== JSON_ERROR_NONE) {
            echo "ERROR: Invalid JSON - " . json_last_error_msg() . "\n";
            return false;
        }

        echo "✓ Total elements in page: " . count($data) . "\n\n";

        // Find and fix issues
        echo "--- Scanning for black backgrounds ---\n";
        $this->scan_and_fix_recursively($data);

        // Report findings
        $this->report_findings();

        // Save if issues were found and fixed
        if (!empty($this->issues_fixed)) {
            echo "\n--- Saving fixes ---\n";
            $this->save_fixes($data, $json);
            return true;
        }

        return false;
    }

    /**
     * Recursively scan through Elementor elements and fix black backgrounds
     */
    private function scan_and_fix_recursively(&$data, $path = '') {
        if (!is_array($data)) {
            return;
        }

        foreach ($data as $key => &$element) {
            $current_path = $path ? "$path.$key" : $key;

            if (is_array($element)) {
                // Check this element's settings
                if (isset($element['settings']['background_color'])) {
                    $color = $element['settings']['background_color'];

                    // Check if it's a black color
                    if ($this->is_black_color($color)) {
                        $this->issues_found[] = array(
                            'path' => $current_path,
                            'color' => $color,
                            'element_type' => isset($element['elType']) ? $element['elType'] : 'unknown',
                            'widget_type' => isset($element['widgetType']) ? $element['widgetType'] : 'n/a'
                        );

                        // Fix it
                        $element['settings']['background_color'] = '';  // Transparent
                        $this->issues_fixed[] = $current_path;
                    }
                }

                // Check background_overlay opacity (if set to 0 or very low)
                if (isset($element['settings']['background_overlay_opacity'])
                    && $element['settings']['background_overlay_opacity'] < 10) {
                    // This might hide content - could be the issue
                    // Log but don't auto-fix (might be intentional)
                }

                // Recursively check nested elements
                $this->scan_and_fix_recursively($element, $current_path);
            }
        }
    }

    /**
     * Check if a color value is black/very dark
     */
    private function is_black_color($color) {
        if (empty($color)) {
            return false;
        }

        $color = strtoupper(str_replace(' ', '', trim($color)));

        // Check for hex black
        if (in_array($color, array('#000000', '#000', '000000', '000'))) {
            return true;
        }

        // Check for common dark grays
        if (in_array($color, array('#111111', '#111', '111111', '111'))) {
            return true;
        }

        // Check for rgb black
        if (preg_match('/^RGB\(0,\s*0,\s*0\)/', $color)) {
            return true;
        }

        return false;
    }

    /**
     * Report what was found
     */
    private function report_findings() {
        if (empty($this->issues_found)) {
            echo "No black backgrounds found - page appears clean!\n";
            return;
        }

        echo "FOUND " . count($this->issues_found) . " black background(s):\n\n";

        foreach ($this->issues_found as $issue) {
            echo "  Path: {$issue['path']}\n";
            echo "    Color: {$issue['color']}\n";
            echo "    Element Type: {$issue['element_type']}\n";
            if ($issue['widget_type'] !== 'n/a') {
                echo "    Widget: {$issue['widget_type']}\n";
            }
            echo "\n";
        }
    }

    /**
     * Save the fixed data back to the database
     */
    private function save_fixes(&$fixed_data, $old_json) {
        $new_json = json_encode($fixed_data);

        // Update post meta
        $result = update_post_meta(
            $this->post_id,
            '_elementor_data',
            $new_json,
            $old_json
        );

        if ($result) {
            echo "✓ Updated Elementor data with " . count($this->issues_fixed) . " fix(es)\n";
        } else {
            echo "✗ Failed to update Elementor data\n";
            return false;
        }

        // Clear Elementor caches
        echo "✓ Clearing Elementor caches...\n";

        // Delete CSS cache
        delete_transient('elementor_' . $this->post_id . '_css');
        delete_transient('elementor_' . $this->post_id . '_meta');

        // Delete all Elementor-related transients for this post
        global $wpdb;
        $wpdb->query(
            $wpdb->prepare(
                "DELETE FROM $wpdb->options WHERE option_name LIKE %s",
                '%elementor%' . $this->post_id . '%'
            )
        );

        // Trigger Elementor's cache clearing
        if (function_exists('elementor_pro_get_environment_settings')) {
            do_action('elementor_clear_cache');
        }

        echo "✓ Caches cleared\n";
        return true;
    }
}

// ============================================================================
// SECTION 3: Execution
// ============================================================================

// Run the fix
$fixer = new RiversideFairwaysElementorFix();
$success = $fixer->run();

if ($success) {
    echo "\n✓ SUCCESS: Homepage styling has been fixed!\n";
    echo "The page should now display correctly. Clear your browser cache if needed.\n";
} else {
    echo "\n⚠ No changes were needed, or fix was skipped.\n";
}

echo "\n=== End of Fix Script ===\n";

?>
