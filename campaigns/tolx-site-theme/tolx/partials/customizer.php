<?php
/**
 * Tolx Customizer — Image Slots
 *
 * Registers a "Tolx Visuals" panel in Appearance → Customize.
 * Each slot consists of:
 *   - An image upload control (WP_Customize_Image_Control)
 *   - A treatment selector (none | subtle | duotone)
 *
 * Templates render images via tolx_image_slot($key, $fallback_callback).
 * If no image is uploaded, the fallback (typically the existing CSS
 * placeholder) is rendered instead.
 *
 * Slot keys are documented in TOLX_IMAGE_SLOTS below — add a new one
 * here, register the controls in tolx_customize_register(), and call
 * tolx_image_slot() from the template.
 */

/* ==========================================================
   SLOT REGISTRY
   --
   Single source of truth. Adding a slot here drives both the
   Customizer registration and the template helper.
   ========================================================== */

if (!function_exists('tolx_image_slots')) {
    function tolx_image_slots() {
        return [

            // -------- Solution heroes (4 slots) --------
            'ev_hero' => [
                'label'         => 'EV Charger Operator System — hero image',
                'description'   => 'Replaces the field-operations placeholder on the EV solution page. Recommended: landscape, ~1200×900px, EV charger in operation or technician on site.',
                'section'       => 'tolx_visuals_solutions',
            ],
            'fleet_hero' => [
                'label'         => 'Fleet Management System — hero image',
                'description'   => 'Replaces the depot placeholder on the Fleet solution page. Recommended: landscape, ~1200×900px, vehicle yard or fleet in motion.',
                'section'       => 'tolx_visuals_solutions',
            ],
            'logistics_hero' => [
                'label'         => 'Logistics & Last-Mile — hero image',
                'description'   => 'Replaces the dispatch placeholder on the Logistics solution page. Recommended: landscape, ~1200×900px, delivery van or POD scene.',
                'section'       => 'tolx_visuals_solutions',
            ],
            'cpo_hero' => [
                'label'         => 'CPO Revenue Module — hero image',
                'description'   => 'Replaces the revenue-layer placeholder on the CPO solution page. Recommended: landscape, ~1200×900px, charging session or kWh dashboard.',
                'section'       => 'tolx_visuals_solutions',
            ],

            // -------- About + trust pages (2 slots) --------
            'about_founder' => [
                'label'         => 'About — founder photo (optional)',
                'description'   => 'If set, displays in the About page below the founder story. Recommended: portrait, ~800×1000px, professional headshot or working scene.',
                'section'       => 'tolx_visuals_trust',
            ],
            'about_team' => [
                'label'         => 'About — team or office photo (optional)',
                'description'   => 'If set, displays as a wide visual on the About page. Recommended: landscape, ~1600×900px.',
                'section'       => 'tolx_visuals_trust',
            ],

            // -------- Contact + homepage (2 slots) --------
            'contact_hero' => [
                'label'         => 'Contact page — side image (optional)',
                'description'   => 'If set, displays beside the contact form. Recommended: portrait, ~900×1200px.',
                'section'       => 'tolx_visuals_marketing',
            ],
            'homepage_hero_bg' => [
                'label'         => 'Homepage — hero background (optional)',
                'description'   => 'If set, displays as a faded background behind the homepage hero. The image is heavily darkened to keep text readable. Recommended: very wide, ~2400×1200px, atmospheric not subject-heavy.',
                'section'       => 'tolx_visuals_marketing',
            ],

            // -------- Solutions hub (1 slot) --------
            'solutions_hub_hero' => [
                'label'         => 'Solutions hub — hero visual (optional)',
                'description'   => 'If set, displays beside the Solutions page hero. Recommended: landscape, ~1200×900px, mix of operational scenes.',
                'section'       => 'tolx_visuals_marketing',
            ],
        ];
    }
}

/* ==========================================================
   CUSTOMIZER REGISTRATION
   ========================================================== */

if (!function_exists('tolx_customize_register')) {
    function tolx_customize_register($wp_customize) {

        // ---- Top-level panel ----
        $wp_customize->add_panel('tolx_visuals', [
            'title'       => 'Tolx Visuals',
            'description' => 'Drag-and-drop image slots for the Tolx site. Each slot has an optional brand treatment (subtle / duotone / none). Empty slots fall back to the default placeholder visual.',
            'priority'    => 30,
        ]);

        // ---- Sections within the panel ----
        $wp_customize->add_section('tolx_visuals_solutions', [
            'title'       => 'Solution Heroes',
            'panel'       => 'tolx_visuals',
            'description' => 'Hero images for each of the four solution pages.',
            'priority'    => 10,
        ]);

        $wp_customize->add_section('tolx_visuals_trust', [
            'title'       => 'About & Trust',
            'panel'       => 'tolx_visuals',
            'description' => 'Optional founder photo and team imagery for the About page.',
            'priority'    => 20,
        ]);

        $wp_customize->add_section('tolx_visuals_marketing', [
            'title'       => 'Marketing Surfaces',
            'panel'       => 'tolx_visuals',
            'description' => 'Optional images for the homepage, Solutions hub, and Contact page.',
            'priority'    => 30,
        ]);

        // ---- Per-slot controls ----
        foreach (tolx_image_slots() as $key => $slot) {
            // Image upload control
            $img_setting_id = "tolx_img_{$key}";
            $wp_customize->add_setting($img_setting_id, [
                'default'           => '',
                'transport'         => 'refresh',
                'sanitize_callback' => 'esc_url_raw',
                'capability'        => 'edit_theme_options',
            ]);
            $wp_customize->add_control(new WP_Customize_Image_Control($wp_customize, $img_setting_id, [
                'label'       => $slot['label'],
                'description' => $slot['description'],
                'section'     => $slot['section'],
                'priority'    => 10,
            ]));

            // Treatment selector
            $tx_setting_id = "tolx_img_{$key}_treatment";
            $wp_customize->add_setting($tx_setting_id, [
                'default'           => 'subtle',
                'transport'         => 'refresh',
                'sanitize_callback' => 'tolx_sanitize_treatment',
                'capability'        => 'edit_theme_options',
            ]);
            $wp_customize->add_control($tx_setting_id, [
                'label'    => 'Treatment',
                'section'  => $slot['section'],
                'type'     => 'select',
                'choices'  => [
                    'none'    => 'None — raw photo',
                    'subtle'  => 'Subtle — slight desaturation + gold tint',
                    'duotone' => 'Duotone — heavy brand treatment',
                ],
                'priority' => 11,
            ]);
        }
    }
}
add_action('customize_register', 'tolx_customize_register');

/* ==========================================================
   SANITIZER
   ========================================================== */

if (!function_exists('tolx_sanitize_treatment')) {
    function tolx_sanitize_treatment($value) {
        $allowed = ['none', 'subtle', 'duotone'];
        return in_array($value, $allowed, true) ? $value : 'subtle';
    }
}

/* ==========================================================
   TEMPLATE HELPER
   --
   Renders an image slot. If no image is set, calls the fallback
   callback (typically the existing CSS placeholder).
   ========================================================== */

if (!function_exists('tolx_image_slot')) {
    /**
     * Render an image slot.
     *
     * @param string   $key       The slot key (matches tolx_image_slots()).
     * @param callable $fallback  Callable that echoes the placeholder fallback.
     * @param array    $args      Optional. Supported: 'class', 'alt', 'wrapper_class'.
     */
    function tolx_image_slot($key, $fallback = null, $args = []) {
        $img_url   = get_theme_mod("tolx_img_{$key}", '');
        $treatment = get_theme_mod("tolx_img_{$key}_treatment", 'subtle');

        $args = wp_parse_args($args, [
            'class'         => '',
            'alt'           => '',
            'wrapper_class' => '',
        ]);

        if (empty($img_url)) {
            // No image set — render fallback
            if (is_callable($fallback)) {
                call_user_func($fallback);
            }
            return;
        }

        $tx_class = 'tolx-img-tx-' . esc_attr($treatment);
        $cls = trim('tolx-img ' . $tx_class . ' ' . esc_attr($args['class']));
        $wrapper_cls = trim('tolx-img-wrap ' . esc_attr($args['wrapper_class']));
        $alt = !empty($args['alt']) ? esc_attr($args['alt']) : '';

        echo '<div class="' . $wrapper_cls . '">';
        echo '<img src="' . esc_url($img_url) . '" alt="' . $alt . '" class="' . $cls . '" loading="lazy" decoding="async" />';
        echo '</div>';
    }
}

/* ==========================================================
   HOMEPAGE BG HELPER
   --
   The homepage hero background needs special treatment: it sits
   behind content as a darkened atmospheric layer. Helper renders
   inline style only when an image is set.
   ========================================================== */

if (!function_exists('tolx_homepage_hero_bg_style')) {
    function tolx_homepage_hero_bg_style() {
        $img = get_theme_mod('tolx_img_homepage_hero_bg', '');
        if (empty($img)) return '';
        return ' style="background-image: linear-gradient(rgba(9,9,11,0.85), rgba(9,9,11,0.95)), url(' . esc_url($img) . '); background-size: cover; background-position: center;"';
    }
}
