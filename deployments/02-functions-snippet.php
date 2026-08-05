// Add this to wp-content/themes/[theme]/functions.php or child theme

// Inline fix that runs on admin init
add_action('admin_init', function() {
    if (!current_user_can('manage_options')) {
        return;
    }
    
    // Check if fix was already applied
    if (get_transient('rf_black_bg_fixed')) {
        return;
    }
    
    $post_id = 1204;
    $json = get_post_meta($post_id, '_elementor_data', true);
    
    if (!empty($json)) {
        $data = json_decode($json, true);
        $fixed = false;
        
        function rf_fix_black_bg(&$elements) {
            global $fixed;
            foreach ($elements as &$element) {
                if (isset($element['settings']['background_color'])) {
                    $color = strtoupper($element['settings']['background_color']);
                    if (in_array($color, array('#000000', '#000', '000000', '000'))) {
                        $element['settings']['background_color'] = '';
                        $fixed = true;
                    }
                }
                if (isset($element['elements']) && is_array($element['elements'])) {
                    rf_fix_black_bg($element['elements']);
                }
            }
        }
        
        rf_fix_black_bg($data);
        
        if ($fixed) {
            update_post_meta($post_id, '_elementor_data', json_encode($data));
            delete_transient('elementor_' . $post_id . '_css');
            wp_cache_delete('elementor_post_' . $post_id);
            do_action('elementor_clear_cache');
            set_transient('rf_black_bg_fixed', true, 24 * HOUR_IN_SECONDS);
        }
    }
});
