<?php
/**
 * Tolx Theme Functions
 */

// Icon library
require_once get_template_directory() . '/partials/icons.php';

// Helm logo SVG
require_once get_template_directory() . '/partials/helm.php';

// SEO module — meta tags, OG, Twitter Cards, JSON-LD schema, breadcrumbs
require_once get_template_directory() . '/partials/seo.php';

// Customizer — image slots with drag-and-drop upload + per-image treatment
require_once get_template_directory() . '/partials/customizer.php';

// Theme Setup
function tolx_setup() {
    add_theme_support('title-tag');
    add_theme_support('post-thumbnails');
    add_theme_support('html5', array('search-form', 'comment-form', 'comment-list', 'gallery', 'caption'));
    add_theme_support('custom-logo');

    register_nav_menus(array(
        'primary' => __('Primary Navigation', 'tolx'),
        'footer-solutions' => __('Footer Solutions', 'tolx'),
        'footer-company' => __('Footer Company', 'tolx'),
        'footer-contact' => __('Footer Contact', 'tolx'),
    ));
}
add_action('after_setup_theme', 'tolx_setup');

// Enqueue Styles & Scripts
function tolx_scripts() {
    // Google Fonts
    wp_enqueue_style('tolx-fonts', 'https://fonts.googleapis.com/css2?family=Chakra+Petch:wght@300;400;500;600;700&family=Share+Tech+Mono&display=swap', array(), null);

    // Main stylesheet
    wp_enqueue_style('tolx-style', get_stylesheet_uri(), array('tolx-fonts'), wp_get_theme()->get('Version'));

    // Main JS
    wp_enqueue_script('tolx-main', get_template_directory_uri() . '/js/main.js', array(), wp_get_theme()->get('Version'), true);
}
add_action('wp_enqueue_scripts', 'tolx_scripts');

// Remove WordPress emoji scripts
remove_action('wp_head', 'print_emoji_detection_script', 7);
remove_action('wp_print_styles', 'print_emoji_styles');

// Custom excerpt length
function tolx_excerpt_length($length) {
    return 20;
}
add_filter('excerpt_length', 'tolx_excerpt_length');

// Custom excerpt more
function tolx_excerpt_more($more) {
    return '...';
}
add_filter('excerpt_more', 'tolx_excerpt_more');

// Add page slug to body class
function tolx_body_classes($classes) {
    if (is_page()) {
        global $post;
        $classes[] = 'page-' . $post->post_name;
    }
    return $classes;
}
add_filter('body_class', 'tolx_body_classes');

require_once get_template_directory() . '/partials/leads.php';
require_once get_template_directory() . '/partials/editorial.php';

/* ============================================================
   RETIRED PAGE REDIRECTS
   ------------------------------------------------------------
   The Odoo pricing page was removed (positioning: no public
   pricing). 301 its old URL to the Odoo hub so link equity and
   any inbound links are preserved instead of 404ing.
   ============================================================ */
if (!function_exists('tolx_retired_redirects')) {
    function tolx_retired_redirects() {
        $path = strtolower(rtrim(parse_url($_SERVER['REQUEST_URI'] ?? '', PHP_URL_PATH) ?: '', '/'));
        $map = array(
            '/odoo/pricing-uae' => '/odoo/',
            '/pricing-uae'      => '/odoo/',
        );
        if (isset($map[$path])) {
            wp_redirect(home_url($map[$path]), 301);
            exit;
        }
    }
}
add_action('template_redirect', 'tolx_retired_redirects', 1);
