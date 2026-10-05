<?php
/**
 * Tolx SEO Module
 *
 * Per-page meta tags, Open Graph, Twitter Cards, canonical URLs, and JSON-LD schema.
 * All output emitted via wp_head hooks.
 *
 * Page metadata is determined by:
 *  1. Per-page custom values from the meta map (tolx_get_page_meta())
 *  2. WordPress yoast/seo plugin if present (we yield to it cleanly)
 *  3. Sensible fallbacks for any page without explicit meta
 */

/* ==========================================================
   CONFIGURATION
   ========================================================== */

if (!defined('TOLX_SITE_NAME'))     define('TOLX_SITE_NAME', 'Tolx');
if (!defined('TOLX_LEGAL_NAME'))    define('TOLX_LEGAL_NAME', 'Tolx');
if (!defined('TOLX_TAGLINE'))       define('TOLX_TAGLINE', 'Steer your operations with precision.');
if (!defined('TOLX_PHONE'))         define('TOLX_PHONE', '+971509860063');
if (!defined('TOLX_EMAIL'))         define('TOLX_EMAIL', 'sales@tolx.ae');
if (!defined('TOLX_WHATSAPP'))      define('TOLX_WHATSAPP', 'https://wa.me/971509860063');
if (!defined('TOLX_LINKEDIN'))      define('TOLX_LINKEDIN', 'https://www.linkedin.com/company/tolx1');
if (!defined('TOLX_LOCALITY'))      define('TOLX_LOCALITY', 'Dubai');
if (!defined('TOLX_REGION'))        define('TOLX_REGION', 'Dubai');
if (!defined('TOLX_COUNTRY'))       define('TOLX_COUNTRY', 'AE');
if (!defined('TOLX_DEFAULT_DESC')) {
    define('TOLX_DEFAULT_DESC', 'A Dubai software and business-systems company helping UAE SMEs organise orders, stock, customer follow-ups and team tasks. Odoo Ready Partner: Odoo implemented around your operation, with practical support for adoption.');
}

/* ==========================================================
   PAGE META MAP
   --
   Per-slug overrides for title/description. If not listed,
   falls back to the page's own title + a generic description.
   ========================================================== */

if (!function_exists('tolx_get_page_meta_map')) {
    function tolx_get_page_meta_map() {
        return [

            // Homepage
            'home' => [
                'title' => 'Software for UAE SMEs | Orders, Stock & Team Tasks · Tolx',
                'description' => 'Odoo Ready Partner in Dubai. Tolx helps UAE SMEs organise orders, stock, follow-ups and team tasks with Odoo implemented around how they work, plus adoption support.',
            ],

            // Solutions hub
            'solutions' => [
                'title' => 'Business Software Solutions for UAE SMEs · Tolx',
                'description' => 'Practical systems for stock, sales, customer follow-ups, tasks and reporting. Tolx implements Odoo for UAE SMEs, configured around how each business works.',
            ],

            // Growth Systems department
            'growth-systems' => [
                'title' => 'Growth Systems Dubai | Web, Marketing, CRM & Automation | Tolx',
                'description' => 'Tolx builds growth systems for UAE businesses: web development, marketing infrastructure, CRM, automation, analytics, dashboards, and business analysis.',
            ],

            // Solution pages
            'ev-charger-operator-system' => [
                'title' => 'EV Charger Operator System — Odoo for UAE EV Operators · Tolx',
                'description' => 'Site survey to invoice in one system. Asset register, project management, field service, contracts, and CPO revenue — built for UAE EV operators and DEWA-approved installers.',
            ],
            'fleet-management-system' => [
                'title' => 'Fleet Management System — Odoo for UAE Fleets · Tolx',
                'description' => 'Vehicle register, maintenance, fuel tracking, driver compliance, and total cost of ownership. Built on Odoo for UAE fleets running 10 to 500 vehicles.',
            ],
            'logistics-last-mile-system' => [
                'title' => 'Logistics & Last-Mile System — Odoo for UAE Delivery · Tolx',
                'description' => 'Order intake, route planning, proof of delivery, returns, COD reconciliation, and a real-time client portal — built on Odoo for UAE last-mile operations.',
            ],
            'cpo-revenue-module' => [
                'title' => 'CPO Revenue Module — Per-Charger Margin Tracking · Tolx',
                'description' => 'kWh delivered, session revenue, energy cost, and gross margin tracked per charger. An add-on for EV operators generating per-session revenue in the UAE.',
            ],

            // Trust pages
            'about' => [
                'title' => 'About Tolx — UAE Software House & Business Systems Partner',
                'description' => 'A Dubai software house and business systems partner. We map how revenue moves through your business, then build the systems around it: software, automation, CRM, dashboards, web, and Odoo.',
            ],
            'odoo-partnership' => [
                'title' => 'Certified Odoo Ready Partner in Dubai & UAE · Tolx',
                'description' => 'Tolx is a certified Odoo Ready Partner serving the UAE. Learn what working with a certified Odoo partner means for your operation.',
            ],
            'our-approach' => [
                'title' => 'Our Approach — Operation First, Then the System · Tolx',
                'description' => 'We map how revenue moves through your business, define clear scope, then build, configure, connect, or automate. How Tolx delivers systems for UAE businesses.',
            ],

            // === ODOO SEO HUB (Phase 4.6) ===
            'odoo' => [
                'title' => 'What is Odoo? A Practical Guide for UAE Businesses · Tolx',
                'description' => 'Odoo for UAE businesses — what it is, how it works, modules, licensing, and when it fits. Written by a Dubai software house and Odoo partner.',
            ],
            'uae-implementation' => [
                'title' => 'Odoo Implementation in the UAE — From Discovery to Go-Live · Tolx',
                'description' => 'Odoo implementation in Dubai and across the UAE. Scope-led delivery by a software house that builds the system around your operation.',
            ],
            'odoo-partner-dubai' => [
                'title' => 'Odoo Partner in Dubai — Implementation for UAE Businesses · Tolx',
                'description' => 'Tolx is an Odoo partner in Dubai. Scope-led Odoo implementation, configured around how UAE businesses actually work.',
            ],
            'software-house-dubai' => [
                'title' => 'Software House in Dubai — Business Systems for UAE Companies · Tolx',
                'description' => 'Tolx is a Dubai software house building systems around the assets, workflows, and data that generate revenue. Custom software, automation, CRM, web, and Odoo.',
            ],

            // Contact
            'contact' => [
                'title' => 'Contact Tolx — Book a Discovery Call · UAE Software House',
                'description' => 'Discuss orders, stock, customer follow-ups or team tasks with Tolx in Dubai. Tell us your business problem by enquiry form, WhatsApp, phone or email.',
            ],

            // Legal
            'privacy-policy' => [
                'title' => 'Privacy Policy · Tolx',
                'description' => 'How Tolx collects, uses, and protects your information — in line with the UAE Personal Data Protection Law.',
            ],
            'terms-of-service' => [
                'title' => 'Terms of Service · Tolx',
                'description' => 'Terms governing the use of the Tolx website and services.',
            ],

        ];
    }
}

/* ==========================================================
   META RESOLVER
   ========================================================== */

if (!function_exists('tolx_resolve_meta')) {
    function tolx_resolve_meta() {
        global $post;
        $map = tolx_get_page_meta_map();

        $title = '';
        $description = '';
        $type = 'website';
        $url = '';

        if (is_front_page()) {
            $m = $map['home'] ?? [];
            $title = $m['title'] ?? get_bloginfo('name');
            $description = $m['description'] ?? get_bloginfo('description');
            $url = home_url('/');
        } elseif (is_singular('post')) {
            $type = 'article';
            $title = get_the_title() . ' · Tolx Blog';
            $description = wp_trim_words(strip_tags(get_the_excerpt() ?: get_the_content()), 30, '…');
            if (!$description) $description = TOLX_DEFAULT_DESC;
            $url = get_permalink();
        } elseif (is_page()) {
            $slug = $post ? $post->post_name : '';
            if (isset($map[$slug])) {
                $title = $map[$slug]['title'];
                $description = $map[$slug]['description'];
            } else {
                $title = get_the_title() . ' · Tolx';
                $description = wp_trim_words(strip_tags(get_the_excerpt() ?: get_the_content()), 30, '…');
                if (!$description) $description = TOLX_DEFAULT_DESC;
            }
            $url = get_permalink();
        } elseif (is_home()) {
            $title = 'Blog — Insights for UAE Businesses · Tolx';
            $description = 'Practical guides to orders, stock, customer follow-ups, team tasks and Odoo for UAE small businesses.';
            $url = home_url('/blog/');
        } elseif (is_category()) {
            $cat = single_cat_title('', false);
            $title = $cat . ' · Tolx Blog';
            $description = 'Articles in the ' . $cat . ' category.';
            $url = get_category_link(get_queried_object_id());
        } elseif (is_404()) {
            $title = '404 — Page Not Found · Tolx';
            $description = TOLX_DEFAULT_DESC;
            $url = home_url(wp_parse_url($_SERVER['REQUEST_URI'] ?? '/', PHP_URL_PATH) ?: '/');
        } else {
            $title = is_search() ? 'Search results · Tolx' : (is_archive() ? wp_strip_all_tags(get_the_archive_title()) . ' · Tolx' : 'Tolx');
            $description = TOLX_DEFAULT_DESC;
            $url = home_url(wp_parse_url($_SERVER['REQUEST_URI'] ?? '/', PHP_URL_PATH) ?: '/');
        }

        if (is_singular()) {
            $custom_title = get_post_meta(get_queried_object_id(), '_tolx_seo_title', true);
            $custom_description = get_post_meta(get_queried_object_id(), '_tolx_seo_description', true);
            if ($custom_title) $title = $custom_title;
            if ($custom_description) $description = $custom_description;
        }
        $paged = max(1, (int) get_query_var('paged'), (int) get_query_var('page'));
        if ($paged > 1) {
            $url = get_pagenum_link($paged, false);
            $title .= ' · Page ' . $paged;
        }
        return [
            'title'       => $title,
            'description' => $description,
            'type'        => $type,
            'url'         => $url,
        ];
    }
}

/* ==========================================================
   YOAST / RANKMATH DETECTION
   --
   If a major SEO plugin is active, we step out of the way
   for titles, metadata, canonicals, robots and schema.
   ========================================================== */

if (!function_exists('tolx_seo_plugin_active')) {
    function tolx_seo_plugin_active() {
        return defined('WPSEO_VERSION')
            || defined('RANK_MATH_VERSION')
            || defined('AIOSEO_VERSION') || class_exists('All_in_One_SEO_Pack')
            || defined('SEOPRESS_VERSION') || defined('THE_SEO_FRAMEWORK_VERSION')
            || (bool) apply_filters('tolx_external_seo_owner', false);
    }
}

/* ==========================================================
   FAQ SCHEMA INJECTION
   --
   Pages that contain FAQ content can register their Q&A pairs
   via tolx_register_faq() before get_header() is called.
   The registered FAQs are then emitted as a FAQPage schema
   inside the JSON-LD graph.
   ========================================================== */

if (!isset($GLOBALS['tolx_faq_buffer'])) {
    $GLOBALS['tolx_faq_buffer'] = [];
}

if (!function_exists('tolx_register_faq')) {
    /**
     * Register one or more FAQ Q&A pairs for the current page.
     *
     * Accepts two forms:
     *   1. Array of [Q, A] pairs (preferred for multiple FAQs)
     *      tolx_register_faq([['Q1','A1'], ['Q2','A2']]);
     *   2. Two scalar args
     *      tolx_register_faq('Question', 'Answer');
     *
     * Call this from a page template before get_header().
     */
    function tolx_register_faq($question_or_pairs, $answer = null) {
        if (is_array($question_or_pairs) && $answer === null) {
            // Form 1 — array of pairs
            foreach ($question_or_pairs as $pair) {
                if (is_array($pair) && count($pair) >= 2) {
                    $GLOBALS['tolx_faq_buffer'][] = [
                        'q' => trim((string) $pair[0]),
                        'a' => trim(strip_tags((string) $pair[1])),
                    ];
                }
            }
        } elseif (is_string($question_or_pairs) && is_string($answer)) {
            // Form 2 — two scalar args
            $GLOBALS['tolx_faq_buffer'][] = [
                'q' => trim($question_or_pairs),
                'a' => trim(strip_tags($answer)),
            ];
        }
    }
}

if (!function_exists('tolx_get_faq_schema_node')) {
    function tolx_get_faq_schema_node() {
        if (empty($GLOBALS['tolx_faq_buffer'])) return null;

        $items = [];
        foreach ($GLOBALS['tolx_faq_buffer'] as $faq) {
            $items[] = [
                '@type' => 'Question',
                'name' => $faq['q'],
                'acceptedAnswer' => [
                    '@type' => 'Answer',
                    'text'  => $faq['a'],
                ],
            ];
        }

        return [
            '@type' => 'FAQPage',
            '@id'   => get_permalink() . '#faq',
            'mainEntity' => $items,
        ];
    }
}

/* ==========================================================
   META TAG OUTPUT (wp_head)
   ========================================================== */

if (!function_exists('tolx_emit_meta_tags')) {
    function tolx_emit_meta_tags() {

        // Active supported SEO plugins own all SEO head output.
        if (tolx_seo_plugin_active()) {
            return;
        }

        $meta = tolx_resolve_meta();

        echo "\n<!-- Tolx SEO Module -->\n";

        // Standard meta description
        echo '<meta name="description" content="' . esc_attr($meta['description']) . '">' . "\n";

        // Canonical URL
        if (!is_404() && !is_search()) echo '<link rel="canonical" href="' . esc_url($meta['url']) . '">' . "\n";

        // Open Graph
        echo '<meta property="og:type" content="' . esc_attr($meta['type']) . '">' . "\n";
        echo '<meta property="og:title" content="' . esc_attr($meta['title']) . '">' . "\n";
        echo '<meta property="og:description" content="' . esc_attr($meta['description']) . '">' . "\n";
        echo '<meta property="og:url" content="' . esc_url($meta['url']) . '">' . "\n";
        echo '<meta property="og:site_name" content="' . esc_attr(TOLX_SITE_NAME) . '">' . "\n";
        echo '<meta property="og:locale" content="en_AE">' . "\n";

        // OG image — featured image for posts/pages, fallback to a site OG asset
        $og_image = '';
        $candidate = get_template_directory() . '/social-card-business-systems-2026.png';
        if (is_singular() && has_post_thumbnail()) {
            $og_image = get_the_post_thumbnail_url(get_the_ID(), 'large');
        }
        if (!$og_image) {
            // Fallback: a static social card asset shipped with the theme.
            // A dated filename is used so LinkedIn/Facebook do not keep the old cached image.
            $candidate = get_template_directory() . '/social-card-business-systems-2026.png';
            if (file_exists($candidate)) {
                $og_image = get_template_directory_uri() . '/social-card-business-systems-2026.png?v=20260716';
            } elseif (file_exists(get_template_directory() . '/social-card.png')) {
                // Compatibility fallback.
                $og_image = get_template_directory_uri() . '/social-card.png?v=20260716';
            }
        }
        if ($og_image) {
            echo '<meta property="og:image" content="' . esc_url($og_image) . '">' . "\n";
            echo '<meta property="og:image:secure_url" content="' . esc_url($og_image) . '">' . "\n";
            $info = is_singular() && has_post_thumbnail() ? wp_get_attachment_image_src(get_post_thumbnail_id(), 'large') : null;
            if ($info) {
                $mime = get_post_mime_type(get_post_thumbnail_id());
                echo '<meta property="og:image:type" content="' . esc_attr($mime) . '">' . "\n";
                echo '<meta property="og:image:width" content="' . (int) $info[1] . '">' . "\n";
                echo '<meta property="og:image:height" content="' . (int) $info[2] . '">' . "\n";
            } else {
                $size = getimagesize(file_exists($candidate) ? $candidate : get_template_directory() . '/social-card.png');
                if ($size) echo '<meta property="og:image:type" content="' . esc_attr($size['mime']) . '"><meta property="og:image:width" content="' . (int) $size[0] . '"><meta property="og:image:height" content="' . (int) $size[1] . '">';
            }
            echo '<meta property="og:image:alt" content="' . esc_attr(is_singular() && has_post_thumbnail() ? (get_post_meta(get_post_thumbnail_id(), '_wp_attachment_image_alt', true) ?: $meta['title']) : $meta['title']) . '">' . "\n";
        }

        // Twitter Cards
        echo '<meta name="twitter:card" content="' . ($og_image ? 'summary_large_image' : 'summary') . '">' . "\n";
        echo '<meta name="twitter:title" content="' . esc_attr($meta['title']) . '">' . "\n";
        echo '<meta name="twitter:description" content="' . esc_attr($meta['description']) . '">' . "\n";
        if ($og_image) {
            echo '<meta name="twitter:image" content="' . esc_url($og_image) . '">' . "\n";
        }

        // Article-specific tags
        if (is_singular('post')) {
            $author = get_the_author();
            $published = get_the_date('c');
            $modified  = get_the_modified_date('c');
            echo '<meta property="article:published_time" content="' . esc_attr($published) . '">' . "\n";
            echo '<meta property="article:modified_time" content="' . esc_attr($modified) . '">' . "\n";
            if ($author) echo '<meta property="article:author" content="' . esc_attr($author) . '">' . "\n";
            $cats = get_the_category();
            if (!empty($cats)) echo '<meta property="article:section" content="' . esc_attr($cats[0]->name) . '">' . "\n";
        }

        // JSON-LD
        tolx_emit_jsonld();

        echo "<!-- /Tolx SEO Module -->\n\n";
    }
}

/* ==========================================================
   TITLE TAG FILTER
   --
   WordPress emits the title via wp_title() / document_title_parts.
   We filter it so our custom titles win — but only when no SEO
   plugin is active.
   ========================================================== */

if (!function_exists('tolx_filter_document_title')) {
    function tolx_filter_document_title($parts) {
        if (tolx_seo_plugin_active()) return $parts;
        $meta = tolx_resolve_meta();
        if (!empty($meta['title'])) {
            // Reduce to a single 'title' value — most themes respect this.
            return ['title' => $meta['title']];
        }
        return $parts;
    }
}

/* ==========================================================
   JSON-LD SCHEMA
   ========================================================== */

if (!function_exists('tolx_emit_jsonld')) {
    function tolx_emit_jsonld() {
        $graph = [];

        // 1) Organization (always)
        $org = [
            '@type'    => 'Organization',
            '@id'      => home_url('/#organization'),
            'name'     => TOLX_SITE_NAME,
            'legalName'=> TOLX_LEGAL_NAME,
            'url'      => home_url('/'),
            'slogan'   => TOLX_TAGLINE,
            'description' => TOLX_DEFAULT_DESC,
            'logo'     => [
                '@type' => 'ImageObject',
                'url'   => get_template_directory_uri() . '/android-chrome-512x512.png',
                'width' => 512,
                'height'=> 512,
            ],
            'sameAs'   => array_filter([
                TOLX_LINKEDIN,
            ]),
            'contactPoint' => [
                '@type' => 'ContactPoint',
                'telephone'   => TOLX_PHONE,
                'email'       => TOLX_EMAIL,
                'contactType' => 'sales',
                'areaServed'  => ['AE'],
                'availableLanguage' => ['en'],
            ],
            'address'  => [
                '@type' => 'PostalAddress',
                'addressLocality' => TOLX_LOCALITY,
                'addressRegion'   => TOLX_REGION,
                'addressCountry'  => TOLX_COUNTRY,
            ],
        ];
        $graph[] = $org;

        // 2) ProfessionalService — describes the actual service offering
        $service = [
            '@type'    => 'Service',
            '@id'      => home_url('/#service'),
            'name'     => 'Tolx — Business Systems, Software & Odoo',
            'url'      => home_url('/'),
            'description' => 'A UAE software house building systems around the assets, workflows, data, and digital channels that generate revenue — custom software, automation, CRM, dashboards, web, marketing systems, and Odoo configuration.',
            'provider' => ['@id' => home_url('/#organization')],
            'areaServed' => [
                ['@type' => 'Country', 'name' => 'United Arab Emirates'],
            ],
            'serviceType' => 'Business Systems, Software Development & Odoo Implementation',
            'hasOfferCatalog' => [
                '@type' => 'OfferCatalog',
                'name'  => 'Tolx Systems',
                'itemListElement' => [
                    [
                        '@type' => 'Offer',
                        'itemOffered' => [
                            '@type' => 'Service',
                            'name'  => 'Stock & Sales Systems',
                            'url'   => home_url('/solutions/'),
                            'description' => 'Systems that give visibility and control over the assets, capacity, locations, contracts, teams, and workflows that generate revenue.',
                        ],
                    ],
                    [
                        '@type' => 'Offer',
                        'itemOffered' => [
                            '@type' => 'Service',
                            'name'  => 'Workflow & Automation Systems',
                            'url'   => home_url('/solutions/'),
                            'description' => 'Reduce manual work, approvals, double entry, and disconnected handoffs across the operation.',
                        ],
                    ],
                    [
                        '@type' => 'Offer',
                        'itemOffered' => [
                            '@type' => 'Service',
                            'name'  => 'CRM & Commercial Operations',
                            'url'   => home_url('/solutions/'),
                            'description' => 'Structure leads, follow-ups, quotes, pipelines, client records, and revenue visibility.',
                        ],
                    ],
                    [
                        '@type' => 'Offer',
                        'itemOffered' => [
                            '@type' => 'Service',
                            'name'  => 'Dashboards & Decision Systems',
                            'url'   => home_url('/solutions/'),
                            'description' => 'Turn scattered data into real-time operational and commercial decisions.',
                        ],
                    ],
                    [
                        '@type' => 'Offer',
                        'itemOffered' => [
                            '@type' => 'Service',
                            'name'  => 'Odoo Configuration',
                            'url'   => home_url('/odoo/'),
                            'description' => 'Tolx implements and configures Odoo around your workflows, from discovery to go-live.',
                        ],
                    ],
                    [
                        '@type' => 'Offer',
                        'itemOffered' => [
                            '@type' => 'Service',
                            'name'  => 'Growth Systems',
                            'url'   => home_url('/growth-systems/'),
                            'description' => 'Web development, marketing systems, SEO, analytics, CRM, and automation that connect growth activity to the rest of the business.',
                        ],
                    ],
                ],
            ],
        ];
        $graph[] = $service;

        // 3) WebSite (with SearchAction)
        $graph[] = [
            '@type' => 'WebSite',
            '@id'   => home_url('/#website'),
            'url'   => home_url('/'),
            'name'  => TOLX_SITE_NAME,
            'publisher' => ['@id' => home_url('/#organization')],
            'inLanguage' => 'en-AE',
        ];

        // 4) WebPage / Article — context-specific
        $meta = tolx_resolve_meta();
        if (is_singular()) {
            $page_id = is_front_page() ? home_url('/#webpage') : (get_permalink() . '#webpage');

            if (is_singular('post')) {
                $article = [
                    '@type'    => 'BlogPosting',
                    '@id'      => get_permalink() . '#article',
                    'mainEntityOfPage' => ['@id' => $page_id],
                    'headline' => get_the_title(),
                    'description' => $meta['description'],
                    'url'      => get_permalink(),
                    'datePublished' => get_the_date('c'),
                    'dateModified'  => get_the_modified_date('c'),
                    'author'   => [
                        '@type' => 'Person',
                        'name'  => get_the_author(),
                    ],
                    'publisher'=> ['@id' => home_url('/#organization')],
                    'isPartOf' => ['@id' => home_url('/#website')],
                ];
                if (has_post_thumbnail()) {
                    $article['image'] = get_the_post_thumbnail_url(get_the_ID(), 'large');
                }
                $cats = get_the_category();
                if (!empty($cats)) {
                    $article['articleSection'] = $cats[0]->name;
                }
                $graph[] = ['@type' => 'WebPage', '@id' => $page_id, 'url' => get_permalink(), 'name' => get_the_title(), 'isPartOf' => ['@id' => home_url('/#website')]];
                $graph[] = $article;
            } else {
                $graph[] = [
                    '@type' => 'WebPage',
                    '@id'   => $page_id,
                    'url'   => $meta['url'],
                    'name'  => $meta['title'],
                    'description' => $meta['description'],
                    'isPartOf' => ['@id' => home_url('/#website')],
                    'about'    => ['@id' => home_url('/#service')],
                    'inLanguage' => 'en-AE',
                ];
            }

            // Breadcrumbs (skip on home)
            if (!is_front_page()) {
                $crumbs = tolx_build_breadcrumbs();
                if (!empty($crumbs)) {
                    $items = [];
                    $pos = 1;
                    foreach ($crumbs as $c) {
                        $items[] = [
                            '@type' => 'ListItem',
                            'position' => $pos++,
                            'name' => $c['name'],
                            'item' => $c['url'],
                        ];
                    }
                    $graph[] = [
                        '@type' => 'BreadcrumbList',
                        '@id'   => $meta['url'] . '#breadcrumb',
                        'itemListElement' => $items,
                    ];
                }
            }

            // FAQ schema if registered by the page template
            $faq_node = tolx_get_faq_schema_node();
            if ($faq_node) {
                $graph[] = $faq_node;
            }
        }

        $payload = [
            '@context' => 'https://schema.org',
            '@graph'   => $graph,
        ];

        // Use JSON_UNESCAPED_SLASHES so URLs render cleanly.
        $json = wp_json_encode($payload, JSON_HEX_TAG | JSON_HEX_AMP | JSON_HEX_APOS | JSON_HEX_QUOT | JSON_UNESCAPED_UNICODE);
        if ($json === false) return;

        echo '<script type="application/ld+json">' . "\n" . $json . "\n</script>\n";
    }
}

/* ==========================================================
   BREADCRUMB BUILDER
   ========================================================== */

if (!function_exists('tolx_build_breadcrumbs')) {
    function tolx_build_breadcrumbs() {
        $crumbs = [['name' => 'Home', 'url' => home_url('/')]];

        if (is_singular('post')) {
            $crumbs[] = ['name' => 'Blog', 'url' => home_url('/blog/')];
            $cats = get_the_category();
            if (!empty($cats)) {
                $crumbs[] = [
                    'name' => $cats[0]->name,
                    'url'  => get_category_link($cats[0]->term_id),
                ];
            }
            $crumbs[] = ['name' => get_the_title(), 'url' => get_permalink()];
        } elseif (is_page()) {
            global $post;
            $ancestors = $post ? array_reverse(get_post_ancestors($post)) : [];
            foreach ($ancestors as $aid) {
                $crumbs[] = ['name' => get_the_title($aid), 'url' => get_permalink($aid)];
            }
            $crumbs[] = ['name' => get_the_title(), 'url' => get_permalink()];
        } elseif (is_home()) {
            $crumbs[] = ['name' => 'Blog', 'url' => home_url('/blog/')];
        } elseif (is_category()) {
            $crumbs[] = ['name' => 'Blog', 'url' => home_url('/blog/')];
            $crumbs[] = ['name' => single_cat_title('', false), 'url' => get_category_link(get_queried_object_id())];
        }

        return $crumbs;
    }
}

/* ==========================================================
   VISIBLE BREADCRUMB COMPONENT
   --
   Optional helper template tag for displaying breadcrumbs
   inline on a page. Call `tolx_render_breadcrumbs();` inside
   any template — typically below the page hero.
   ========================================================== */

if (!function_exists('tolx_render_breadcrumbs')) {
    function tolx_render_breadcrumbs() {
        if (is_front_page()) return;
        $crumbs = tolx_build_breadcrumbs();
        if (count($crumbs) < 2) return;
        ?>
<nav class="tolx-breadcrumbs" aria-label="Breadcrumb">
  <ol class="tolx-breadcrumb-list">
    <?php $last = count($crumbs) - 1; foreach ($crumbs as $i => $c): ?>
      <li class="tolx-breadcrumb-item">
        <?php if ($i < $last): ?>
          <a href="<?php echo esc_url($c['url']); ?>"><?php echo esc_html($c['name']); ?></a>
        <?php else: ?>
          <span aria-current="page"><?php echo esc_html($c['name']); ?></span>
        <?php endif; ?>
      </li>
    <?php endforeach; ?>
  </ol>
</nav>
        <?php
    }
}

/* ==========================================================
   HOOKS
   ========================================================== */

add_action('wp_head', 'tolx_emit_meta_tags', 1);
add_filter('document_title_parts', 'tolx_filter_document_title', 100);

/* ==========================================================
   ROBOTS.TXT — Append a sane sitemap reference
   ========================================================== */

if (!function_exists('tolx_robots_txt')) {
    function tolx_robots_txt($output, $public) {
        // Core or the active SEO plugin owns robots and sitemap references.
        return $output;
    }
}
add_filter('robots_txt', 'tolx_robots_txt', 10, 2);

/* ==========================================================
   WP CORE SITEMAP — make sure it's enabled (WP 5.5+)
   --
   WordPress now ships a default XML sitemap at /wp-sitemap.xml.
   We forward /sitemap.xml requests to it for friendliness.
   ========================================================== */

if (!function_exists('tolx_sitemap_redirect')) {
    function tolx_sitemap_redirect() {
        if (tolx_seo_plugin_active() || !get_option('blog_public') || !function_exists('wp_sitemaps_get_server') || !wp_sitemaps_get_server()->sitemaps_enabled()) return;
        $req = $_SERVER['REQUEST_URI'] ?? '';
        if (strtolower(rtrim(parse_url($req, PHP_URL_PATH) ?: '', '/')) === '/sitemap.xml') {
            // Only redirect if a real sitemap.xml file isn't being served by something else.
            if (!file_exists(ABSPATH . 'sitemap.xml')) {
                wp_redirect(home_url('/wp-sitemap.xml'), 301);
                exit;
            }
        }
    }
}
add_action('template_redirect', 'tolx_sitemap_redirect', 1);

add_action('wp', function () {
    if (!tolx_seo_plugin_active()) remove_action('wp_head', 'rel_canonical');
});
add_filter('wp_robots', function ($robots) {
    if (!tolx_seo_plugin_active() && (is_search() || is_404() || is_preview() || is_attachment() || (is_singular() && post_password_required()))) {
        unset($robots['index']); $robots['noindex'] = true;
    }
    return $robots;
});

/* ==========================================================
   SEO PLUGIN GAP-FILL
   --
   When Yoast, Rank Math or All in One SEO owns the head, the
   module above steps aside. If that plugin has no description or
   social image for a page (common with a default install), fill
   the gap from this theme so search results keep a description and
   shared links keep the TOLX social card. Values the plugin does
   have are never overwritten.
   ========================================================== */

if (!function_exists('tolx_social_card_url')) {
    function tolx_social_card_url() {
        if (is_singular() && has_post_thumbnail()) {
            $img = get_the_post_thumbnail_url(get_queried_object_id(), 'full');
            if ($img) return $img;
        }
        foreach (array('social-card-business-systems-2026.png', 'social-card.png') as $f) {
            if (file_exists(get_template_directory() . '/' . $f)) {
                return get_template_directory_uri() . '/' . $f . '?v=20260716';
            }
        }
        return '';
    }
}

if (!function_exists('tolx_fallback_description')) {
    function tolx_fallback_description() {
        $meta = tolx_resolve_meta();
        return !empty($meta['description']) ? $meta['description'] : TOLX_DEFAULT_DESC;
    }
}

// Yoast SEO
add_filter('wpseo_metadesc', function ($d) { return trim((string) $d) !== '' ? $d : tolx_fallback_description(); }, 20);
add_filter('wpseo_opengraph_desc', function ($d) { return trim((string) $d) !== '' ? $d : tolx_fallback_description(); }, 20);
add_action('wpseo_add_opengraph_images', function ($images) {
    if (is_object($images) && method_exists($images, 'has_images') && !$images->has_images()) {
        $url = tolx_social_card_url();
        if ($url) $images->add_image(array('url' => $url, 'width' => 1200, 'height' => 630));
    }
});

// Rank Math
add_filter('rank_math/frontend/description', function ($d) { return trim((string) $d) !== '' ? $d : tolx_fallback_description(); }, 20);
add_filter('rank_math/opengraph/facebook/image', function ($img) { return $img ? $img : tolx_social_card_url(); }, 20);
add_filter('rank_math/opengraph/twitter/image', function ($img) { return $img ? $img : tolx_social_card_url(); }, 20);

// All in One SEO
add_filter('aioseo_description', function ($d) { return trim((string) $d) !== '' ? $d : tolx_fallback_description(); }, 20);
add_filter('aioseo_facebook_tags', function ($tags) {
    if (!is_array($tags)) return $tags;
    if (empty($tags['og:description'])) $tags['og:description'] = tolx_fallback_description();
    if (empty($tags['og:image'])) {
        $url = tolx_social_card_url();
        if ($url) {
            $tags['og:image'] = $url;
            $tags['og:image:secure_url'] = $url;
            $tags['og:image:width'] = 1200;
            $tags['og:image:height'] = 630;
        }
    }
    return $tags;
}, 20);
add_filter('aioseo_twitter_tags', function ($tags) {
    if (!is_array($tags)) return $tags;
    if (empty($tags['twitter:image'])) {
        $url = tolx_social_card_url();
        if ($url) $tags['twitter:image'] = $url;
    }
    if (empty($tags['twitter:card'])) $tags['twitter:card'] = 'summary_large_image';
    return $tags;
}, 20);

