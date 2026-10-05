<?php
/** Editable editorial metadata and an explicit, administrator-only local draft importer. */
function tolx_editorial_manifest() {
    $items = require get_template_directory() . '/content/editorial-drafts.php';
    return is_array($items) ? $items : [];
}
function tolx_editorial_fields() {
    return ['_tolx_seo_title' => 'SEO title', '_tolx_seo_description' => 'Meta description'];
}
add_action('add_meta_boxes', function () {
    foreach (['post', 'page'] as $type) {
        add_meta_box('tolx_editorial_seo', 'TOLX search metadata', function ($post) {
            wp_nonce_field('tolx_editorial_save', 'tolx_editorial_nonce');
            echo '<p>Editable title and description for theme-managed SEO. With an SEO plugin active, edit its own fields; it remains the output owner.</p>';
            foreach (tolx_editorial_fields() as $key => $label) {
                echo '<p><label>' . esc_html($label) . '<br><textarea name="' . esc_attr($key) . '" rows="2" style="width:100%">' . esc_textarea(get_post_meta($post->ID, $key, true)) . '</textarea></label></p>';
            }
        }, $type, 'normal');
    }
});
add_action('save_post', function ($id) {
    if (wp_is_post_revision($id) || (defined('DOING_AUTOSAVE') && DOING_AUTOSAVE) || !current_user_can('edit_post', $id)) return;
    $nonce = $_POST['tolx_editorial_nonce'] ?? '';
    if (!is_string($nonce) || !wp_verify_nonce($nonce, 'tolx_editorial_save')) return;
    foreach (tolx_editorial_fields() as $key => $label) {
        if (isset($_POST[$key]) && is_string($_POST[$key])) update_post_meta($id, $key, sanitize_text_field(wp_unslash($_POST[$key])));
    }
});
function tolx_editorial_apply_missing($id, $item) {
    if (get_post_status($id) !== 'draft') return new WP_Error('status', 'Existing non-draft content was skipped.');
    $fields = [
        '_tolx_content_key' => $item['slug'],
        '_tolx_seo_title' => $item['seo_title'], '_tolx_seo_description' => $item['seo_description'],
        '_yoast_wpseo_title' => $item['seo_title'], '_yoast_wpseo_metadesc' => $item['seo_description'],
        'rank_math_title' => $item['seo_title'], 'rank_math_description' => $item['seo_description'],
        '_seopress_titles_title' => $item['seo_title'], '_seopress_titles_desc' => $item['seo_description'],
    ];
    foreach ($fields as $key => $value) {
        if (get_post_meta($id, $key, true) === '') {
            update_post_meta($id, $key, $value);
            if (get_post_meta($id, $key, true) !== $value) return new WP_Error('metadata', 'The draft is saved but some search metadata could not be saved. Retry after checking database health.');
        }
    }
    if (!get_post_field('post_excerpt', $id)) {
        $updated = wp_update_post(['ID' => $id, 'post_excerpt' => wp_slash($item['excerpt'])], true);
        if (is_wp_error($updated)) return $updated;
    }
    if (has_post_thumbnail($id)) return $id;
    $source = get_template_directory() . '/assets/editorial/' . basename($item['image']);
    if (!is_file($source)) return new WP_Error('image', 'The draft is saved but its bundled image is missing.');
    $attachments = get_posts(['post_type' => 'attachment', 'post_status' => 'inherit', 'post_parent' => $id, 'meta_key' => '_tolx_editorial_image_key', 'meta_value' => $item['image'], 'numberposts' => 1]);
    if ($attachments) $attachment_id = $attachments[0]->ID;
    else {
        // A temporary copy is needed because media_handle_sideload moves its input file.
        $temporary = wp_tempnam($item['image']);
        if (!$temporary || !copy($source, $temporary)) {
            if ($temporary) wp_delete_file($temporary);
            return new WP_Error('image_copy', 'The draft is saved but its image could not be copied. Retry after checking uploads permissions.');
        }
        $attachment_id = media_handle_sideload(['name' => basename($item['image']), 'tmp_name' => $temporary], $id, $item['image_title'], ['post_title' => $item['image_title'], 'post_excerpt' => $item['image_caption'], 'post_content' => $item['image_caption']]);
        if (is_wp_error($attachment_id)) { wp_delete_file($temporary); return $attachment_id; }
        update_post_meta($attachment_id, '_tolx_editorial_image_key', $item['image']);
        update_post_meta($attachment_id, '_wp_attachment_image_alt', $item['image_alt']);
    }
    if (!set_post_thumbnail($id, $attachment_id) && (int) get_post_thumbnail_id($id) !== (int) $attachment_id) return new WP_Error('thumbnail', 'Image was uploaded but not attached as featured image. Retry or assign it manually.');
    return $id;
}
function tolx_import_editorial_drafts() {
    $report = [];
    foreach (tolx_editorial_manifest() as $item) {
        $existing = get_page_by_path($item['slug'], OBJECT, $item['type']);
        if ($existing && $existing->post_status !== 'draft') {
            $report[] = $item['title'] . ': skipped existing non-draft content.'; continue;
        }
        if ($existing) $id = $existing->ID;
        else {
            // Resolve existing-page links for sites installed in a subdirectory.
            $body = preg_replace_callback('#href="(/[^"\s]*)"#', function ($m) { return 'href="' . esc_url(home_url($m[1])) . '"'; }, $item['content']);
            $id = wp_insert_post(['post_type' => $item['type'], 'post_status' => 'draft', 'post_title' => $item['title'], 'post_name' => $item['slug'], 'post_content' => wp_slash($body), 'post_excerpt' => wp_slash($item['excerpt']), 'comment_status' => 'closed', 'ping_status' => 'closed'], true);
            if (is_wp_error($id) || !$id) { $report[] = $item['title'] . ': draft could not be saved.'; continue; }
        }
        $result = tolx_editorial_apply_missing($id, $item);
        $report[] = $item['title'] . ': ' . (is_wp_error($result) ? $result->get_error_message() : 'draft ready with metadata and featured image.');
    }
    return $report;
}
add_action('admin_menu', function () {
    add_management_page('TOLX editorial drafts', 'TOLX editorial drafts', 'manage_options', 'tolx-editorial', function () {
        if (!current_user_can('manage_options')) return;
        echo '<div class="wrap"><h1>TOLX editorial drafts</h1><p>Import one article and three service pages as drafts, with local photos, excerpts and search metadata. Existing matching drafts receive only missing metadata/images; their body text and existing images are preserved. Existing published or other non-draft content is skipped.</p><p>Nothing is imported by theme installation or activation. This action uploads images to the Media Library, where files can be publicly accessible even while their parent content is a draft.</p>';
        $report = get_transient('tolx_editorial_report_' . get_current_user_id());
        if (is_array($report)) { echo '<ul>'; foreach ($report as $line) echo '<li>' . esc_html($line) . '</li>'; echo '</ul>'; }
        echo '<form method="post" action="' . esc_url(admin_url('admin-post.php')) . '"><input type="hidden" name="action" value="tolx_import_editorial">';
        wp_nonce_field('tolx_import_editorial');
        submit_button('Import or complete the four drafts'); echo '</form></div>';
    });
});
add_action('admin_post_tolx_import_editorial', function () {
    if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST' || !current_user_can('manage_options') || !current_user_can('upload_files') || !current_user_can('edit_posts') || !current_user_can('edit_pages')) wp_die('Administrator permissions are required.', '', ['response' => 403]);
    check_admin_referer('tolx_import_editorial');
    $key = 'tolx_editorial_import_lock'; $previous = (int) get_option($key);
    if ($previous && time() - $previous > 600) delete_option($key);
    if (!add_option($key, time(), '', false)) wp_die('An import is already in progress. Please wait and retry.');
    require_once ABSPATH . 'wp-admin/includes/file.php';
    require_once ABSPATH . 'wp-admin/includes/media.php';
    require_once ABSPATH . 'wp-admin/includes/image.php';
    try { $report = tolx_import_editorial_drafts(); }
    finally { delete_option($key); }
    set_transient('tolx_editorial_report_' . get_current_user_id(), $report, HOUR_IN_SECONDS);
    wp_safe_redirect(admin_url('tools.php?page=tolx-editorial')); exit;
});
