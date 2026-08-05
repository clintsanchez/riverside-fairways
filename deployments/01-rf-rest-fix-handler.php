<?php
/**
 * REST Handler for Black Background Fix
 * Place in wp-content/mu-plugins/ or load via hook
 */

add_action('rest_api_init', function() {
    register_rest_route('rf-fix/v1', '/black-bg', array(
        'methods' => array('POST', 'GET'),
        'permission_callback' => '__return_true', // WARNING: Open endpoint for demo only
        'callback' => function() {
            $post_id = 1204;
            $json = get_post_meta($post_id, '_elementor_data', true);
            $fixed_count = 0;
            
            if (!empty($json)) {
                $data = json_decode($json, true);
                
                function fix_recursively(&$elements) {
                    global $fixed_count;
                    foreach ($elements as &$element) {
                        if (isset($element['settings']['background_color'])) {
                            $color = strtoupper($element['settings']['background_color']);
                            if (in_array($color, array('#000000', '#000', '000000', '000'))) {
                                $element['settings']['background_color'] = '';
                                $fixed_count++;
                            }
                        }
                        if (isset($element['elements'])) {
                            fix_recursively($element['elements']);
                        }
                    }
                }
                
                fix_recursively($data);
                
                if ($fixed_count > 0) {
                    update_post_meta($post_id, '_elementor_data', json_encode($data));
                    delete_transient('elementor_' . $post_id . '_css');
                    do_action('elementor_clear_cache');
                }
            }
            
            return new WP_REST_Response(array(
                'success' => true,
                'fixed_count' => $fixed_count,
                'message' => "Fixed $fixed_count black background(s) on page $post_id"
            ), 200);
        }
    ));
});
?>
