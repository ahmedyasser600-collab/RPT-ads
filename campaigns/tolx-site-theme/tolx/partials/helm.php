<?php
/**
 * Tolx Helm Logo
 *
 * Renders the ship's helm SVG. Used in preloader, nav, and footer.
 *
 * @param int    $size   Pixel size. Default 32.
 * @param string $extra  Extra class(es) for the <svg>.
 */
if (!function_exists('tolx_helm')) {
    function tolx_helm($size = 32, $extra = '') {
        $cls = trim('tolx-helm ' . $extra);
        ?>
<svg width="<?php echo intval($size); ?>" height="<?php echo intval($size); ?>" viewBox="0 0 80 80" fill="none" xmlns="http://www.w3.org/2000/svg" class="<?php echo esc_attr($cls); ?>" aria-hidden="true">
  <circle cx="40" cy="40" r="30" stroke="#D4A843" stroke-width="5" fill="none"/>
  <circle cx="40" cy="40" r="7" stroke="#D4A843" stroke-width="4" fill="none"/>
  <line x1="40" y1="10" x2="40" y2="33" stroke="#D4A843" stroke-width="3.5"/>
  <line x1="40" y1="47" x2="40" y2="70" stroke="#D4A843" stroke-width="3.5"/>
  <line x1="10" y1="40" x2="33" y2="40" stroke="#D4A843" stroke-width="3.5"/>
  <line x1="47" y1="40" x2="70" y2="40" stroke="#D4A843" stroke-width="3.5"/>
  <line x1="18.8" y1="18.8" x2="35.1" y2="35.1" stroke="#D4A843" stroke-width="3"/>
  <line x1="44.9" y1="44.9" x2="61.2" y2="61.2" stroke="#D4A843" stroke-width="3"/>
  <line x1="61.2" y1="18.8" x2="44.9" y2="35.1" stroke="#D4A843" stroke-width="3"/>
  <line x1="35.1" y1="44.9" x2="18.8" y2="61.2" stroke="#D4A843" stroke-width="3"/>
  <ellipse cx="40" cy="3" rx="3.5" ry="5" fill="#D4A843"/>
  <ellipse cx="40" cy="77" rx="3.5" ry="5" fill="#D4A843"/>
  <ellipse cx="3" cy="40" rx="5" ry="3.5" fill="#D4A843"/>
  <ellipse cx="77" cy="40" rx="5" ry="3.5" fill="#D4A843"/>
  <ellipse cx="66" cy="14" rx="3.2" ry="4.5" transform="rotate(-45 66 14)" fill="#D4A843"/>
  <ellipse cx="14" cy="14" rx="3.2" ry="4.5" transform="rotate(45 14 14)" fill="#D4A843"/>
  <ellipse cx="66" cy="66" rx="3.2" ry="4.5" transform="rotate(45 66 66)" fill="#D4A843"/>
  <ellipse cx="14" cy="66" rx="3.2" ry="4.5" transform="rotate(-45 14 66)" fill="#D4A843"/>
</svg>
        <?php
    }
}
