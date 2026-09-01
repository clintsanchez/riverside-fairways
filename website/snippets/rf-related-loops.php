<?php
/**
 * Riverside Fairways — related content on the Single Service template.
 *
 * Elementor loop widgets cannot filter by a Meta Box relationship, so these
 * hooks do it. Set a loop widget's Query ID to one of the names below and it
 * will show only the items connected to the service being viewed.
 *
 *   service_faqs     -> faqs connected via faq_to_service
 *   service_reviews  -> reviews connected via review_to_service
 *
 * Both fail closed: a service with nothing linked shows nothing, rather than
 * falling back to every FAQ or review on the site.
 *
 * NOTE: Elementor's element cache must stay disabled. With it on, one service's
 * rendered output is cached against the template and served to all the others.
 */
if ( ! function_exists( 'rf_related_ids' ) ) {
	function rf_related_ids( $type, $service_id ) {
		global $wpdb;
		if ( ! $service_id ) {
			return array();
		}
		return $wpdb->get_col(
			$wpdb->prepare(
				"SELECT `from` FROM {$wpdb->prefix}mb_relationships WHERE type = %s AND `to` = %d",
				$type,
				$service_id
			)
		);
	}
}

if ( ! function_exists( 'rf_filter_related_loop' ) ) {
	function rf_filter_related_loop( $query, $relationship ) {
		$ids = rf_related_ids( $relationship, get_queried_object_id() );
		$query->set( 'post__in', $ids ? array_map( 'intval', $ids ) : array( 0 ) );
		$query->set( 'orderby', 'post__in' );
		$query->set( 'ignore_sticky_posts', true );
	}
}

add_action( 'elementor/query/service_faqs', function ( $query ) {
	rf_filter_related_loop( $query, 'faq_to_service' );
} );

add_action( 'elementor/query/service_reviews', function ( $query ) {
	rf_filter_related_loop( $query, 'review_to_service' );
} );

/**
 * Each FAQ is its own loop item, so every accordion renders collapsed and
 * nothing would be open on load. Open the first one only.
 *
 * Elementor's nested-accordion initialises after DOMContentLoaded and resets
 * the state, so this waits for its own element_ready hook and clicks the
 * summary rather than setting .open directly, which keeps Elementor's internal
 * state and aria-expanded in sync.
 */
add_action( 'wp_footer', function () {
	if ( ! is_singular( 'services' ) ) {
		return;
	}
	?>
	<script>
	( function () {
		function openFirstFaq() {
			// :first-child fails here, the loop container has a preceding node
			var all = document.querySelectorAll( '.rf-faq-loop .e-loop-item details' );
			var first = all.length ? all[0] : null;
			if ( ! first || first.open ) { return; }
			var summary = first.querySelector( 'summary' );
			if ( summary ) { summary.click(); } else { first.open = true; }
		}
		window.addEventListener( 'elementor/frontend/init', function () {
			if ( window.elementorFrontend && elementorFrontend.hooks ) {
				elementorFrontend.hooks.addAction(
					'frontend/element_ready/nested-accordion.default',
					function () { setTimeout( openFirstFaq, 0 ); }
				);
			}
		} );
		window.addEventListener( 'load', function () { setTimeout( openFirstFaq, 150 ); } );
	} )();
	</script>
	<?php
}, 99 );


/**
 * FAQPage structured data for the FAQ hub.
 *
 * Deliberately NOT the nested-accordion's built-in faq_schema switch: each FAQ
 * is its own loop item, so that would emit four separate FAQPage blocks (one
 * per category grid) instead of one page with eleven questions. This builds a
 * single block from the categorised FAQs.
 */
add_action( 'wp_head', function () {
	if ( ! is_page( 1678 ) ) {
		return;
	}

	$faqs = get_posts( array(
		'post_type'      => 'faqs',
		'posts_per_page' => -1,
		'post_status'    => 'publish',
		'tax_query'      => array(
			array(
				'taxonomy' => 'faq-categories',
				'operator' => 'EXISTS',
			),
		),
	) );

	$entities = array();
	foreach ( $faqs as $faq ) {
		$answer = get_post_meta( $faq->ID, 'answer', true );
		if ( ! $answer ) {
			continue;
		}
		$entities[] = array(
			'@type'          => 'Question',
			'name'           => wp_strip_all_tags( $faq->post_title ),
			'acceptedAnswer' => array(
				'@type' => 'Answer',
				'text'  => wp_strip_all_tags( $answer ),
			),
		);
	}

	if ( ! $entities ) {
		return;
	}

	echo '<script type="application/ld+json">'
		. wp_json_encode( array(
			'@context'   => 'https://schema.org',
			'@type'      => 'FAQPage',
			'mainEntity' => $entities,
		), JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE )
		. '</script>' . "\n";
}, 5 );


/**
 * [rf_service_gallery] — photo grid for the current service.
 *
 * Elementor has no Meta Box gallery dynamic tag and the core gallery widget is
 * not registered on this install, so the grid is rendered here from the
 * service_gallery image_advanced field. One field, any number of photos, and
 * the whole section removes itself when the field is empty.
 */
add_shortcode( 'rf_service_gallery', function () {
	$ids = get_post_meta( get_the_ID(), 'service_gallery', true );
	if ( ! $ids || ! is_array( $ids ) ) {
		return '';
	}

	$out = '<div class="rf-gallery">';
	foreach ( $ids as $id ) {
		$src = wp_get_attachment_image_url( (int) $id, 'large' );
		if ( ! $src ) {
			continue;
		}
		$alt = get_post_meta( (int) $id, '_wp_attachment_image_alt', true );
		$out .= sprintf(
			'<figure class="rf-gallery__item">%s</figure>',
			wp_get_attachment_image( (int) $id, 'large', false, [
				'alt'     => $alt,
				'loading' => 'lazy',
			] )
		);
	}
	return $out . '</div>';
} );

/**
 * Hide the gallery heading/section when a service has no photos, so an empty
 * field never leaves an orphaned heading behind.
 */
add_filter( 'elementor/frontend/container/should_render', function ( $should, $element ) {
	if ( ! $should || ! is_singular( 'services' ) ) {
		return $should;
	}
	$class = $element->get_settings( 'css_classes' ) ?: '';

	if ( 'rf-gallery-section' === $class ) {
		$ids = get_post_meta( get_the_ID(), 'service_gallery', true );
		return ! empty( $ids ) && is_array( $ids );
	}

	// no photo for this service -> drop the media column so the numbered list
	// goes full width instead of sitting next to an empty gap
	if ( 'rf-steps-media' === $class ) {
		return (bool) get_post_meta( get_the_ID(), 'how_it_plays_image', true );
	}

	return $should;
}, 10, 2 );

/**
 * Explicit 301s.
 *
 * SEOPress's own redirect records were not firing for programmatically created
 * entries (the one built through its UI works, an identical one created via
 * wp_insert_post does not), and its global "redirect every 404 to the homepage"
 * option has been turned off because it turns missing pages into soft 404s.
 * These are handled here instead: deterministic, and version-controlled.
 */
add_action( 'template_redirect', function () {
	if ( ! is_404() ) {
		return;
	}

	$map = [
		'/policies/terms-and-conditions/' => '/policies/terms-conditions/',
		'/terms-and-conditions/'          => '/policies/terms-conditions/',
		'/terms-conditions/'              => '/policies/terms-conditions/',
		'/testimonials/'                  => '/',
	];

	$path = strtok( $_SERVER['REQUEST_URI'] ?? '', '?' );
	$path = '/' . trim( (string) $path, '/' ) . '/';

	if ( isset( $map[ $path ] ) ) {
		wp_safe_redirect( home_url( $map[ $path ] ), 301 );
		exit;
	}
} );
