<?php
/**
 * Tolx Icon Library
 *
 * Sharp technical / schematic icon set. Two-layer construction:
 *   - Primary stroke: 1.4px, square caps, square joins
 *   - Hairline detail: 0.6px, used for status pips, register lines, tracking marks
 *
 * Usage:
 *   <?php tolx_icon('charger'); ?>
 *   <?php tolx_icon('charger', 24); ?>            // custom size
 *   <?php tolx_icon('charger', 24, 'gold'); ?>    // 'gold' or 'current' (default current)
 *
 * All icons render as SVG with stroke="currentColor" so the icon picks up
 * its colour from the parent. Container colour rules:
 *   - .sol-card-icon, .op-block-icon, .card-icon → gold
 *   - .cmd-row-icon, .hero-cmd-module svg → gold
 *   - inline body text → currentColor
 */

if (!function_exists('tolx_icon_svg')) {
    function tolx_icon_svg($name) {
        $icons = [

            /* ============================================================
               OPERATIONAL / FIELD ICONS
               ============================================================ */

            // CHARGER — vertical CCS connector schematic with tip pip
            'charger' => '<g><rect x="9" y="3" width="6" height="14" /><line x1="11" y1="6" x2="11" y2="9" /><line x1="13" y1="6" x2="13" y2="9" /><line x1="11" y1="12" x2="13" y2="12" /><path d="M9 17 L7 21 L17 21 L15 17" /><circle cx="12" cy="2.5" r="0.6" fill="currentColor" stroke="none"/></g>',

            // FLEET — vehicle plan-view with directional indicator
            'fleet' => '<g><rect x="4" y="3" width="16" height="18" rx="1" /><line x1="8" y1="3" x2="8" y2="6" /><line x1="16" y1="3" x2="16" y2="6" /><line x1="8" y1="18" x2="8" y2="21" /><line x1="16" y1="18" x2="16" y2="21" /><line x1="4" y1="11" x2="20" y2="11" /><path d="M10 14 L12 16 L14 14" stroke-width="0.7"/></g>',

            // VEHICLE / CAR — three-quarter schematic
            'vehicle' => '<g><path d="M3 14 L4 10 L20 10 L21 14 L21 17 L3 17 Z" /><circle cx="7.5" cy="17" r="1.5" /><circle cx="16.5" cy="17" r="1.5" /><line x1="6" y1="10" x2="7" y2="7" stroke-width="0.7"/><line x1="18" y1="10" x2="17" y2="7" stroke-width="0.7"/></g>',

            // ROUTE — waypoint + route line + endpoint
            'route' => '<g><circle cx="6" cy="6" r="2" /><circle cx="18" cy="18" r="2" /><path d="M6 8 L6 14 L18 14 L18 16" stroke-dasharray="2 1.5"/><line x1="3" y1="6" x2="9" y2="6" stroke-width="0.6"/><line x1="15" y1="18" x2="21" y2="18" stroke-width="0.6"/></g>',

            // DELIVERY / PACKAGE — schematic box with corner notch
            'delivery' => '<g><path d="M3 7 L12 3 L21 7 L21 17 L12 21 L3 17 Z" /><line x1="3" y1="7" x2="12" y2="11" /><line x1="21" y1="7" x2="12" y2="11" /><line x1="12" y1="11" x2="12" y2="21" /><line x1="7.5" y1="5" x2="16.5" y2="9" stroke-width="0.6"/></g>',

            // ASSET / TRACKING — corner brackets + central node
            'asset' => '<g><path d="M3 7 L3 3 L7 3" /><path d="M17 3 L21 3 L21 7" /><path d="M21 17 L21 21 L17 21" /><path d="M7 21 L3 21 L3 17" /><circle cx="12" cy="12" r="2.5" /><circle cx="12" cy="12" r="0.7" fill="currentColor" stroke="none"/></g>',

            // INVENTORY — stacked register
            'inventory' => '<g><rect x="3" y="4" width="18" height="4" /><rect x="3" y="10" width="18" height="4" /><rect x="3" y="16" width="18" height="4" /><line x1="6" y1="6" x2="9" y2="6" stroke-width="0.7"/><line x1="6" y1="12" x2="9" y2="12" stroke-width="0.7"/><line x1="6" y1="18" x2="9" y2="18" stroke-width="0.7"/><circle cx="18" cy="6" r="0.7" fill="currentColor" stroke="none"/><circle cx="18" cy="12" r="0.7" fill="currentColor" stroke="none"/></g>',

            // FIELD SERVICE / WRENCH — schematic tool with pivot point
            'field-service' => '<g><path d="M14 4 a4 4 0 1 0 4 4 L21 5 L19 3 L16 6 a3 3 0 0 1 -2 0 L14 4 Z" /><line x1="13" y1="11" x2="4" y2="20" /><circle cx="4" cy="20" r="1.2" /><circle cx="14" cy="8" r="0.6" fill="currentColor" stroke="none"/></g>',

            // MAINTENANCE / GEAR — technical schematic gear
            'maintenance' => '<g><circle cx="12" cy="12" r="3" /><line x1="12" y1="3" x2="12" y2="6" /><line x1="12" y1="18" x2="12" y2="21" /><line x1="3" y1="12" x2="6" y2="12" /><line x1="18" y1="12" x2="21" y2="12" /><line x1="5.6" y1="5.6" x2="7.7" y2="7.7" /><line x1="16.3" y1="16.3" x2="18.4" y2="18.4" /><line x1="5.6" y1="18.4" x2="7.7" y2="16.3" /><line x1="16.3" y1="7.7" x2="18.4" y2="5.6" /><circle cx="12" cy="12" r="0.7" fill="currentColor" stroke="none"/></g>',

            // SITE SURVEY / SURVEY — crosshair on plan
            'survey' => '<g><rect x="3" y="3" width="18" height="18" /><line x1="12" y1="3" x2="12" y2="21" stroke-width="0.6"/><line x1="3" y1="12" x2="21" y2="12" stroke-width="0.6"/><circle cx="12" cy="12" r="3" /><line x1="12" y1="9" x2="12" y2="15" stroke-width="0.7"/><line x1="9" y1="12" x2="15" y2="12" stroke-width="0.7"/></g>',

            // PROJECT / TASK — task list with progress markers
            'project' => '<g><rect x="3" y="4" width="18" height="16" /><line x1="6" y1="9" x2="14" y2="9" /><line x1="6" y1="13" x2="12" y2="13" /><line x1="6" y1="17" x2="10" y2="17" /><circle cx="17" cy="9" r="0.7" fill="currentColor" stroke="none"/><circle cx="15" cy="13" r="0.7" fill="currentColor" stroke="none"/></g>',

            // CONTRACT / DOCUMENT — folded doc with signature line
            'contract' => '<g><path d="M5 3 L15 3 L19 7 L19 21 L5 21 Z" /><polyline points="15 3 15 7 19 7" /><line x1="8" y1="12" x2="16" y2="12" stroke-width="0.7"/><line x1="8" y1="15" x2="14" y2="15" stroke-width="0.7"/><line x1="8" y1="18" x2="12" y2="18" /></g>',

            // BILLING / INVOICE — receipt with running total
            'billing' => '<g><path d="M5 3 L19 3 L19 21 L17 19 L15 21 L13 19 L11 21 L9 19 L7 21 L5 19 Z" /><line x1="8" y1="8" x2="16" y2="8" stroke-width="0.7"/><line x1="8" y1="11" x2="16" y2="11" stroke-width="0.7"/><line x1="8" y1="14" x2="13" y2="14" stroke-width="0.7"/><circle cx="16" cy="14" r="0.7" fill="currentColor" stroke="none"/></g>',

            // REVENUE / CURRENCY — abstract currency stream
            'revenue' => '<g><path d="M16 5 H10 a3 3 0 0 0 0 6 h4 a3 3 0 0 1 0 6 H8" /><line x1="12" y1="2" x2="12" y2="5" /><line x1="12" y1="17" x2="12" y2="20" /><circle cx="20" cy="9" r="0.7" fill="currentColor" stroke="none"/><circle cx="4" cy="15" r="0.7" fill="currentColor" stroke="none"/></g>',

            // KWH / ENERGY — bolt + measurement bracket
            'kwh' => '<g><path d="M13 3 L5 13 L11 13 L10 21 L18 11 L12 11 L13 3 Z" /><line x1="20" y1="3" x2="22" y2="3" stroke-width="0.6"/><line x1="20" y1="21" x2="22" y2="21" stroke-width="0.6"/><line x1="21" y1="3" x2="21" y2="21" stroke-width="0.6"/></g>',

            // SESSION / TIMER — clock with sweep arc
            'session' => '<g><circle cx="12" cy="12" r="9" /><polyline points="12 7 12 12 16 14" /><line x1="12" y1="3" x2="12" y2="4.5" stroke-width="0.6"/><line x1="12" y1="19.5" x2="12" y2="21" stroke-width="0.6"/><line x1="3" y1="12" x2="4.5" y2="12" stroke-width="0.6"/><line x1="19.5" y1="12" x2="21" y2="12" stroke-width="0.6"/></g>',

            // DASHBOARD — radial gauge + ticks
            'dashboard' => '<g><path d="M3 18 a9 9 0 0 1 18 0" /><line x1="3" y1="18" x2="5.5" y2="18" stroke-width="0.7"/><line x1="21" y1="18" x2="18.5" y2="18" stroke-width="0.7"/><line x1="6.4" y1="11" x2="8.2" y2="12.5" stroke-width="0.7"/><line x1="17.6" y1="11" x2="15.8" y2="12.5" stroke-width="0.7"/><line x1="12" y1="6" x2="12" y2="8.5" stroke-width="0.7"/><line x1="12" y1="18" x2="16" y2="11" /><circle cx="12" cy="18" r="1.2" fill="currentColor" stroke="none"/></g>',

            /* ============================================================
               PEOPLE / ORG ICONS
               ============================================================ */

            // DRIVER / OPERATOR — person with badge marker
            'driver' => '<g><circle cx="12" cy="7" r="3.5" /><path d="M5 21 v-1.5 a4 4 0 0 1 4 -4 h6 a4 4 0 0 1 4 4 V21" /><line x1="14" y1="6" x2="16" y2="6" stroke-width="0.6"/></g>',

            // OPERATOR / OPERATIONS PERSON — same as driver but with headset hint
            'operator' => '<g><circle cx="12" cy="8" r="3" /><path d="M5 21 v-2 a4 4 0 0 1 4 -4 h6 a4 4 0 0 1 4 4 V21" /><path d="M7 8 a5 5 0 0 1 10 0" stroke-width="0.6"/><circle cx="7" cy="9" r="0.8" fill="currentColor" stroke="none"/><circle cx="17" cy="9" r="0.8" fill="currentColor" stroke="none"/></g>',

            // INSTALLER / FIELD TECH — hard hat profile
            'installer' => '<g><path d="M4 17 a8 8 0 0 1 16 0" /><line x1="3" y1="17" x2="21" y2="17" /><line x1="3" y1="20" x2="21" y2="20" /><line x1="12" y1="9" x2="12" y2="11" stroke-width="0.6"/><circle cx="12" cy="8" r="0.7" fill="currentColor" stroke="none"/></g>',

            // CLIENT / BUILDING — operator company
            'company' => '<g><rect x="4" y="3" width="16" height="18" /><line x1="8" y1="7" x2="10" y2="7" stroke-width="0.7"/><line x1="14" y1="7" x2="16" y2="7" stroke-width="0.7"/><line x1="8" y1="11" x2="10" y2="11" stroke-width="0.7"/><line x1="14" y1="11" x2="16" y2="11" stroke-width="0.7"/><line x1="8" y1="15" x2="10" y2="15" stroke-width="0.7"/><line x1="14" y1="15" x2="16" y2="15" stroke-width="0.7"/><rect x="10" y="18" width="4" height="3" /></g>',

            /* ============================================================
               STRUCTURAL / SYSTEM ICONS
               ============================================================ */

            // MODULE / GRID — 2x2 module map with connection lines
            'module' => '<g><rect x="3" y="3" width="7" height="7" /><rect x="14" y="3" width="7" height="7" /><rect x="3" y="14" width="7" height="7" /><rect x="14" y="14" width="7" height="7" /><line x1="10" y1="6.5" x2="14" y2="6.5" stroke-width="0.6"/><line x1="10" y1="17.5" x2="14" y2="17.5" stroke-width="0.6"/><line x1="6.5" y1="10" x2="6.5" y2="14" stroke-width="0.6"/><line x1="17.5" y1="10" x2="17.5" y2="14" stroke-width="0.6"/></g>',

            // OPEN-SOURCE / NODE — hub with three branches
            'open-source' => '<g><circle cx="12" cy="6" r="2" /><circle cx="6" cy="18" r="2" /><circle cx="18" cy="18" r="2" /><line x1="12" y1="8" x2="12" y2="14" /><line x1="12" y1="14" x2="6" y2="16.5" /><line x1="12" y1="14" x2="18" y2="16.5" /><circle cx="12" cy="14" r="0.8" fill="currentColor" stroke="none"/></g>',

            // SHIELD / COMPLIANCE — UAE compliant marker
            'shield' => '<g><path d="M12 3 L20 6 V12 a9 9 0 0 1 -8 9 a9 9 0 0 1 -8 -9 V6 Z" /><polyline points="9 12 11.5 14.5 16 10" stroke-width="1.6"/></g>',

            // LIGHTNING / SPEED — sharp diagonal bolt
            'lightning' => '<g><path d="M14 3 L5 13 L11 13 L10 21 L19 11 L13 11 L14 3 Z" /></g>',

            // CHECK / VERIFIED — check inside corner brackets
            'check' => '<g><polyline points="5 12 10 17 19 7" stroke-width="1.6"/><path d="M3 6 V3 H6" stroke-width="0.6"/><path d="M21 18 V21 H18" stroke-width="0.6"/></g>',

            // ARROW / NAV — arrow with reference axis
            'arrow' => '<g><line x1="4" y1="12" x2="19" y2="12" /><polyline points="14 7 19 12 14 17" /><line x1="2" y1="9" x2="2" y2="15" stroke-width="0.6"/></g>',

            // MAIL / ENVELOPE — schematic envelope
            'mail' => '<g><rect x="3" y="5" width="18" height="14" /><polyline points="3 5 12 13 21 5" /><line x1="3" y1="19" x2="9" y2="13" stroke-width="0.6"/><line x1="21" y1="19" x2="15" y2="13" stroke-width="0.6"/></g>',

            // PHONE — receiver with signal pip
            'phone' => '<g><path d="M5 3 H8 L10 8 L7.5 10 a12 12 0 0 0 6.5 6.5 L16 14 L21 16 V19 a2 2 0 0 1 -2 2 a17 17 0 0 1 -16 -16 a2 2 0 0 1 2 -2 Z" /><circle cx="19" cy="5" r="0.8" fill="currentColor" stroke="none"/></g>',

            // CHAT / WHATSAPP-LIKE — speech bubble with hairline tail
            'chat' => '<g><path d="M3 6 a3 3 0 0 1 3 -3 h12 a3 3 0 0 1 3 3 v9 a3 3 0 0 1 -3 3 H10 L5 22 V18 H6 a3 3 0 0 1 -3 -3 Z" /><line x1="8" y1="9" x2="16" y2="9" stroke-width="0.6"/><line x1="8" y1="13" x2="14" y2="13" stroke-width="0.6"/></g>',

            // PIN / LOCATION
            'pin' => '<g><path d="M12 22 s-7 -7 -7 -12 a7 7 0 0 1 14 0 c0 5 -7 12 -7 12 Z" /><circle cx="12" cy="10" r="2.5" /><circle cx="12" cy="10" r="0.7" fill="currentColor" stroke="none"/></g>',

            // CALENDAR
            'calendar' => '<g><rect x="3" y="5" width="18" height="16" /><line x1="3" y1="10" x2="21" y2="10" /><line x1="8" y1="3" x2="8" y2="7" /><line x1="16" y1="3" x2="16" y2="7" /><circle cx="8" cy="14" r="0.8" fill="currentColor" stroke="none"/><circle cx="12" cy="14" r="0.8" fill="currentColor" stroke="none"/><circle cx="16" cy="14" r="0.8" fill="currentColor" stroke="none"/></g>',

            // BUILDING / GROWTH — bar trend up
            'growth' => '<g><polyline points="3 18 9 12 13 16 21 6" /><polyline points="15 6 21 6 21 12" /><line x1="3" y1="21" x2="21" y2="21" stroke-width="0.6"/></g>',

            // CLIENT / USERS — multiple operators
            'users' => '<g><circle cx="9" cy="8" r="2.5" /><circle cx="17" cy="9" r="2" /><path d="M3 19 v-1 a4 4 0 0 1 4 -4 h4 a4 4 0 0 1 4 4 v1" /><path d="M15 14 a3 3 0 0 1 3 -1 h0 a3 3 0 0 1 3 3 v1" /></g>',

            // FUEL / DROP — fuel droplet with measurement
            'fuel' => '<g><path d="M12 3 C8 9 6 12 6 15 a6 6 0 0 0 12 0 c0 -3 -2 -6 -6 -12 Z" /><line x1="9" y1="15" x2="11" y2="15" stroke-width="0.7"/><circle cx="14" cy="15" r="0.7" fill="currentColor" stroke="none"/></g>',

            // SETTINGS / CONFIGURE
            'settings' => '<g><line x1="4" y1="6" x2="20" y2="6" /><line x1="4" y1="12" x2="20" y2="12" /><line x1="4" y1="18" x2="20" y2="18" /><circle cx="9" cy="6" r="1.6" fill="var(--bg, #09090B)"/><circle cx="9" cy="6" r="1.6" /><circle cx="15" cy="12" r="1.6" fill="var(--bg, #09090B)"/><circle cx="15" cy="12" r="1.6" /><circle cx="9" cy="18" r="1.6" fill="var(--bg, #09090B)"/><circle cx="9" cy="18" r="1.6" /></g>',

            // PORTAL / SCREEN — client portal device
            'portal' => '<g><rect x="3" y="4" width="18" height="13" rx="1" /><line x1="9" y1="20" x2="15" y2="20" /><line x1="12" y1="17" x2="12" y2="20" stroke-width="0.6"/><line x1="6" y1="8" x2="14" y2="8" stroke-width="0.7"/><line x1="6" y1="11" x2="11" y2="11" stroke-width="0.7"/><circle cx="17" cy="13" r="0.8" fill="currentColor" stroke="none"/></g>',

            // RETURN / REVERSE — return arrow with axis
            'return' => '<g><polyline points="9 8 4 12 9 16" /><path d="M4 12 H14 a6 6 0 0 1 6 6 V21" /><line x1="2" y1="9" x2="2" y2="15" stroke-width="0.6"/></g>',

            // ORDER / CART — abstract order schematic
            'order' => '<g><polyline points="3 4 6 4 8 16 18 16 20 8 8 8" /><circle cx="9" cy="20" r="1.4" /><circle cx="17" cy="20" r="1.4" /><line x1="11" y1="11" x2="17" y2="11" stroke-width="0.6"/></g>',

            // MONEY / DIRHAM (using currency symbol-like) — for COD
            'cash' => '<g><rect x="3" y="6" width="18" height="12" /><circle cx="12" cy="12" r="2.5" /><circle cx="6" cy="12" r="0.7" fill="currentColor" stroke="none"/><circle cx="18" cy="12" r="0.7" fill="currentColor" stroke="none"/></g>',

            // LIVE-DATA / TRANSMISSION — radar pulse
            'live' => '<g><circle cx="12" cy="12" r="2" fill="currentColor" stroke="none"/><circle cx="12" cy="12" r="5" /><path d="M5 12 a7 7 0 0 1 14 0" stroke-width="0.6"/><path d="M2 12 a10 10 0 0 1 20 0" stroke-width="0.6" stroke-dasharray="2 2"/></g>',

            // SCALE / SME — tiered blocks
            'scale' => '<g><rect x="3" y="14" width="6" height="7" /><rect x="9" y="9" width="6" height="12" /><rect x="15" y="4" width="6" height="17" /><line x1="6" y1="17" x2="6" y2="18" stroke-width="0.6"/><line x1="12" y1="13" x2="12" y2="14" stroke-width="0.6"/><line x1="18" y1="9" x2="18" y2="10" stroke-width="0.6"/></g>',

            // LINKEDIN — minimal stylised
            'linkedin' => '<g><rect x="3" y="3" width="18" height="18" /><rect x="6" y="10" width="2.5" height="8" fill="currentColor" stroke="none"/><circle cx="7.25" cy="7" r="1.5" fill="currentColor" stroke="none"/><path d="M11 18 V10 H13.5 V11.5 a3 3 0 0 1 5.5 1.5 V18 H16.5 V14 a1.5 1.5 0 0 0 -3 0 V18 Z" fill="currentColor" stroke="none"/></g>',

        ];

        return $icons[$name] ?? null;
    }
}

if (!function_exists('tolx_icon')) {
    /**
     * Render an icon. Echoes the SVG.
     *
     * @param string $name   Icon name (see library above).
     * @param int    $size   Pixel size (square). Default 24.
     * @param string $extra  Extra class(es) for the <svg>.
     */
    function tolx_icon($name, $size = 24, $extra = '') {
        $body = tolx_icon_svg($name);
        if (!$body) {
            // Unknown icon — render a small placeholder square so missing icons are obvious in dev
            echo '<svg width="' . intval($size) . '" height="' . intval($size) . '" viewBox="0 0 24 24" class="tolx-icon tolx-icon-missing ' . esc_attr($extra) . '" fill="none" stroke="currentColor" stroke-width="1.4"><rect x="3" y="3" width="18" height="18"/><line x1="3" y1="3" x2="21" y2="21" stroke-width="0.6"/></svg>';
            return;
        }
        $cls = trim('tolx-icon tolx-icon-' . preg_replace('/[^a-z0-9\-]/', '', $name) . ' ' . $extra);
        echo '<svg width="' . intval($size) . '" height="' . intval($size) . '" viewBox="0 0 24 24" class="' . esc_attr($cls) . '" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="square" stroke-linejoin="miter">' . $body . '</svg>';
    }
}
