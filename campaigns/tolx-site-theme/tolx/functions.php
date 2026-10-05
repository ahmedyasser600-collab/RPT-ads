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
    // Fonts are self-hosted (assets/fonts) and declared inline in tolx_font_faces(),
    // so there is no render-blocking request to Google Fonts.
    $ver = wp_get_theme()->get('Version');
    $dir = get_template_directory();

    // Serve style.min.css when it is at least as new as style.css (build.sh makes it).
    // If someone edits style.css without rebuilding, the stale minified file is skipped.
    $min = $dir . '/style.min.css';
    if (file_exists($min) && filemtime($min) >= filemtime($dir . '/style.css')) {
        wp_enqueue_style('tolx-style', get_template_directory_uri() . '/style.min.css', array(), $ver . '.' . filemtime($min));
    } else {
        wp_enqueue_style('tolx-style', get_stylesheet_uri(), array(), $ver);
    }

    // Main JS, deferred
    wp_enqueue_script('tolx-main', get_template_directory_uri() . '/js/main.js', array(), $ver, array('in_footer' => true, 'strategy' => 'defer'));
}
add_action('wp_enqueue_scripts', 'tolx_scripts');

// Self-hosted brand fonts: preload the two weights the first screen needs
// (300 = hero paragraph, 700 = headline) and declare all faces inline.
function tolx_font_faces() {
    $base = get_template_directory_uri() . '/assets/fonts/';
    foreach (array('chakra-petch-latin-700-normal', 'chakra-petch-latin-300-normal') as $f) {
        echo '<link rel="preload" href="' . esc_url($base . $f . '.woff2') . '" as="font" type="font/woff2" crossorigin>' . "\n";
    }
    $css = '';
    foreach (array(300, 400, 500, 600, 700) as $w) {
        $css .= "@font-face{font-family:'Chakra Petch';font-style:normal;font-weight:$w;font-display:swap;src:url({$base}chakra-petch-latin-$w-normal.woff2) format('woff2')}";
    }
    $css .= "@font-face{font-family:'Share Tech Mono';font-style:normal;font-weight:400;font-display:swap;src:url({$base}share-tech-mono-latin-400-normal.woff2) format('woff2')}";
    echo '<style id="tolx-fonts">' . $css . "</style>\n";
}
add_action('wp_head', 'tolx_font_faces', 1);

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
