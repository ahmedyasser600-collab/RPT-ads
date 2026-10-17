<?php
// Gmail login for enquiry emails. Keep the real app password OUT of the theme: put
//   define('TOLX_SMTP_PASS', 'xxxx xxxx xxxx xxxx');
// in wp-config.php (above "That's all, stop editing"). wp-config.php values win, and theme updates never overwrite them.
if (!defined('TOLX_SMTP_USER')) define('TOLX_SMTP_USER', 'tolxodoo@gmail.com');
if (!defined('TOLX_SMTP_PASS')) define('TOLX_SMTP_PASS', 'PASTE_APP_PASSWORD_HERE');
// Who is notified of each enquiry: one or more addresses, separated by commas. Visitor replies go to the first.
if (!defined('TOLX_LEAD_EMAIL')) define('TOLX_LEAD_EMAIL', 'sales@tolx.ae, tolxodoo@gmail.com');
// Company profile sent to people who use the contact form. Upload the PDF in Media > Add New, copy its
// "File URL" and paste it below. Leave it empty to send the confirmation email without a PDF.
if (!defined('TOLX_PROFILE_PDF_URL')) define('TOLX_PROFILE_PDF_URL', 'https://tolx.ae/wp-content/uploads/2026/10/Tolx_brochure.pdf');
/** Private submission storage: saved before any notification. */
function tolx_assessment_questions() {
    return json_decode(file_get_contents(get_template_directory() . '/partials/assessment.json'), true);
}
function tolx_input($key, $limit = 200) {
    $value = $_POST[$key] ?? '';
    if (!is_string($value) || strlen($value) > $limit * 4) return '';
    $clean = sanitize_textarea_field(wp_unslash($value));
    return function_exists('mb_substr') ? mb_substr($clean, 0, $limit) : substr($clean, 0, $limit);
}
function tolx_assessment_summary($answers) {
    $questions = tolx_assessment_questions();
    if (!is_string($answers) || !preg_match('/^[0-3](,[0-3]){5}$/D', $answers)) return new WP_Error('answers', 'Please answer all six questions.');
    $lines = [];
    foreach (explode(',', $answers) as $i => $answer) {
        $q = $questions[$i]; $option = $q['opts'][(int) $answer];
        $lines[] = $q['q'] . "\nYour answer: " . $option['t'] . "\n" . (!empty($option['gap']) ? 'Consider: ' . $option['opp']['text'] : 'Maintain this process and review it as your needs change.');
    }
    return implode("\n\n", $lines) . "\n\nThese are starting points based on your answers, not a verified business diagnosis. Tool selection, integrations and automation depend on discovery and agreed scope. Odoo is one option; a spreadsheet or focused tool may be sufficient.";
}
add_action('init', function () {
    register_post_type('tolx_submission', ['label' => 'TOLX enquiries', 'public' => false, 'show_ui' => true, 'show_in_menu' => true, 'supports' => ['title'], 'capabilities' => ['edit_posts' => 'manage_options', 'edit_post' => 'manage_options', 'read_post' => 'manage_options', 'delete_post' => 'manage_options', 'publish_posts' => 'manage_options', 'read_private_posts' => 'manage_options', 'delete_posts' => 'manage_options', 'edit_others_posts' => 'manage_options', 'create_posts' => 'do_not_allow'], 'map_meta_cap' => false]);
});
add_action('add_meta_boxes', function () {
    add_meta_box('tolx_record', 'Saved enquiry and notification status', function ($post) {
        if (!current_user_can('manage_options')) return;
        echo '<pre style="white-space:pre-wrap">' . esc_html($post->post_content) . "\n\n" . esc_html(wp_json_encode(get_post_meta($post->ID, '_tolx_notifications', true))) . '</pre>';
    }, 'tolx_submission');
});
/**
 * Lead notifications. If TOLX_SMTP_USER and TOLX_SMTP_PASS are defined in wp-config.php, mail goes straight
 * to that SMTP account (Gmail by default) and bypasses wp_mail and any mail plugin. Otherwise wp_mail is used.
 * Optional: TOLX_SMTP_HOST, TOLX_SMTP_PORT (587 STARTTLS / 465 SSL), TOLX_LEAD_EMAIL (who receives enquiries).
 * Returns true, or a short error message (never the password).
 */
function tolx_send_mail($to, $subject, $body, $reply_to = '', $attachments = []) {
    if (!defined('TOLX_SMTP_USER') || !defined('TOLX_SMTP_PASS') || !TOLX_SMTP_USER || !TOLX_SMTP_PASS || TOLX_SMTP_PASS === 'PASTE_APP_PASSWORD_HERE') {
        $headers = ['Content-Type: text/plain; charset=UTF-8'];
        if ($reply_to && is_email($reply_to)) $headers[] = 'Reply-To: ' . $reply_to;
        return wp_mail($to, $subject, $body, $headers, $attachments) ? true : 'wp_mail returned false';
    }
    require_once ABSPATH . WPINC . '/PHPMailer/PHPMailer.php';
    require_once ABSPATH . WPINC . '/PHPMailer/SMTP.php';
    require_once ABSPATH . WPINC . '/PHPMailer/Exception.php';
    $mail = new PHPMailer\PHPMailer\PHPMailer(true);
    try {
        $port = defined('TOLX_SMTP_PORT') ? (int) TOLX_SMTP_PORT : 587;
        $mail->isSMTP();
        $mail->Host = defined('TOLX_SMTP_HOST') ? TOLX_SMTP_HOST : 'smtp.gmail.com';
        $mail->Port = $port;
        $mail->SMTPSecure = $port === 465 ? PHPMailer\PHPMailer\PHPMailer::ENCRYPTION_SMTPS : PHPMailer\PHPMailer\PHPMailer::ENCRYPTION_STARTTLS;
        $mail->SMTPAuth = true;
        $mail->Username = TOLX_SMTP_USER;
        $mail->Password = str_replace(' ', '', TOLX_SMTP_PASS);
        $mail->Timeout = 15;
        $mail->CharSet = 'UTF-8';
        $mail->setFrom(TOLX_SMTP_USER, 'TOLX Website');
        foreach ((array) $to as $address) $mail->addAddress($address);
        if ($reply_to && is_email($reply_to)) $mail->addReplyTo($reply_to);
        $mail->Subject = $subject;
        $mail->Body = $body;
        foreach ($attachments as $file) $mail->addAttachment($file);
        $mail->send();
        return true;
    } catch (\Exception $e) {
        $error = 'SMTP: ' . substr((string) $mail->ErrorInfo, 0, 200);
        error_log('TOLX lead mail failed. ' . $error);
        return $error;
    }
}
/** Enquiry notification addresses (array), from TOLX_LEAD_EMAIL or the site's TOLX_EMAIL. */
function tolx_lead_recipients() {
    $list = defined('TOLX_LEAD_EMAIL') ? array_values(array_filter(array_map('trim', explode(',', TOLX_LEAD_EMAIL)), 'is_email')) : [];
    return $list ?: [TOLX_EMAIL];
}
/** Local path of the company profile PDF in the Media Library, or '' if it is not set or not found. */
function tolx_profile_pdf_path() {
    if (!TOLX_PROFILE_PDF_URL) return '';
    $id = attachment_url_to_postid(TOLX_PROFILE_PDF_URL);
    $path = $id ? get_attached_file($id) : '';
    return $path && file_exists($path) ? $path : '';
}
function tolx_contact_confirmation_body($data, $has_pdf) {
    $lines = [
        'Hi ' . $data['name'] . ',',
        '',
        'Thank you for contacting TOLX. We have received your enquiry and will reply within 1 business day.',
    ];
    if ($has_pdf) array_push($lines, '', 'Our company profile is attached, so you can see how we work in the meantime.');
    elseif (TOLX_PROFILE_PDF_URL) array_push($lines, '', 'Our company profile: ' . TOLX_PROFILE_PDF_URL);
    if (!empty($data['message'])) array_push($lines, '', 'Your message:', $data['message']);
    array_push($lines, '', 'If it is urgent, message us on WhatsApp: https://wa.me/971509860063 or call +971 50 986 0063.', '', 'TOLX', 'tolx.ae');
    return implode("\n", $lines);
}
function tolx_lead_subject($kind, $data, $id) {
    $who = $data['name'] . (!empty($data['company']) ? ' (' . $data['company'] . ')' : '');
    return ($kind === 'assessment' ? 'New scorecard lead: ' : 'New enquiry: ') . $who . ' #' . $id;
}
function tolx_lead_email_body($kind, $data, $summary, $id) {
    $labels = ['name' => 'Name', 'company' => 'Company', 'email' => 'Email', 'phone' => 'Phone', 'industry' => 'Wants to improve', 'source' => 'Heard about us', 'sector' => 'Sector', 'role' => 'Role', 'consent' => 'Consent'];
    $lines = ['New ' . $kind . ' from tolx.ae', ''];
    foreach ($labels as $key => $label) {
        if (isset($data[$key]) && $data[$key] !== '') $lines[] = $label . ': ' . $data[$key];
    }
    if (!empty($data['message'])) array_push($lines, '', 'Message:', $data['message']);
    if ($summary) array_push($lines, '', 'Assessment summary:', $summary);
    array_push($lines, '', 'Reply to this email to answer ' . $data['name'] . ' directly.', 'Saved in WordPress: ' . admin_url('post.php?post=' . (int) $id . '&action=edit'));
    return implode("\n", $lines);
}
function tolx_save_submission($kind, $data, $summary = '') {
    $fingerprint = hash_hmac('sha256', $kind . wp_json_encode($data), wp_salt('nonce'));
    $lock = 'tolx_lead_' . $fingerprint;
    $existing = get_option($lock);
    if ($existing && time() - $existing['time'] < 900) {
        if (!empty($existing['id'])) return ['id' => $existing['id'], 'duplicate' => true, 'message' => 'This submission is already saved.', 'summary' => $summary];
        return new WP_Error('busy', 'This submission is being processed. Please wait and retry.');
    }
    if ($existing) delete_option($lock);
    $ip = hash_hmac('sha256', $_SERVER['REMOTE_ADDR'] ?? 'unknown', wp_salt('nonce'));
    $rate = 'tolx_rate_' . $ip; $count = (int) get_transient($rate);
    if ($count >= 5) return new WP_Error('limit', 'Too many requests. Please wait an hour or contact us directly.');
    if (!add_option($lock, ['time' => time(), 'id' => 0], '', false)) return new WP_Error('busy', 'Please wait and retry.');
    set_transient($rate, $count + 1, HOUR_IN_SECONDS);
    $body = $kind . "\n" . wp_json_encode($data, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE) . "\n\n" . $summary;
    $id = wp_insert_post(['post_type' => 'tolx_submission', 'post_status' => 'private', 'post_title' => $kind . ' — ' . $data['name'], 'post_content' => wp_slash($body)], true);
    if (is_wp_error($id) || !$id) { delete_option($lock); return new WP_Error('storage', 'We could not save your enquiry. Your details remain on this page; please retry or contact us directly.'); }
    update_option($lock, ['time' => time(), 'id' => $id], false);
    $status = ['team' => 'pending', 'visitor' => 'not_requested', 'webhook' => 'disabled'];
    update_post_meta($id, '_tolx_notifications', $status);
    $sent = tolx_send_mail(tolx_lead_recipients(), tolx_lead_subject($kind, $data, $id), tolx_lead_email_body($kind, $data, $summary, $id), $data['email']);
    $status['team'] = $sent === true ? 'accepted_by_mailer' : 'failed';
    if ($sent !== true) $status['team_error'] = $sent;
    if ($kind === 'contact') {
        $pdf = tolx_profile_pdf_path();
        $sent = tolx_send_mail($data['email'], 'We received your enquiry - TOLX', tolx_contact_confirmation_body($data, (bool) $pdf), tolx_lead_recipients()[0], $pdf ? [$pdf] : []);
        $status['visitor'] = $sent === true ? 'accepted_by_mailer' : 'failed';
        if ($sent !== true) $status['visitor_error'] = $sent;
    }
    if ($kind === 'assessment') {
        $sent = tolx_send_mail($data['email'], 'Your TOLX operations summary', "Hi " . $data['name'] . ",\n\n" . $summary . "\n\nDiscuss your workflow: " . home_url('/contact/'));
        $status['visitor'] = $sent === true ? 'accepted_by_mailer' : 'failed';
        if ($sent !== true) $status['visitor_error'] = $sent;
        if (defined('TOLX_SCORECARD_SHEET_WEBHOOK') && TOLX_SCORECARD_SHEET_WEBHOOK) {
            $result = wp_remote_post(TOLX_SCORECARD_SHEET_WEBHOOK, ['timeout' => 8, 'headers' => ['Content-Type' => 'application/json'], 'body' => wp_json_encode(['id' => $id, 'submission' => $data, 'summary' => $summary])]);
            $status['webhook'] = !is_wp_error($result) && wp_remote_retrieve_response_code($result) >= 200 && wp_remote_retrieve_response_code($result) < 300 ? 'http_accepted' : 'failed';
        }
    }
    update_post_meta($id, '_tolx_notifications', $status);
    return ['id' => $id, 'duplicate' => false, 'summary' => $summary, 'message' => 'Your enquiry is saved.' . ($status['visitor'] === 'failed' ? ' Email could not be sent; copy your summary below.' : ($kind === 'assessment' ? ' Your summary was accepted by the mail service; inbox delivery is not confirmed.' : ($status['visitor'] === 'accepted_by_mailer' ? ' We have emailed you a confirmation.' : ''))) . ($status['team'] === 'failed' ? ' Team notification failed; your saved enquiry is available to administrators.' : '')];
}
function tolx_handle_scorecard_lead() {
    if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST' || !wp_verify_nonce(tolx_input('sc_nonce'), 'tolx_scorecard')) wp_send_json_error(['message' => 'Security check failed. Refresh and retry.'], 403);
    if (tolx_input('sc_website')) wp_send_json_error(['message' => 'Submission rejected.'], 400);
    $data = [];
    foreach (['name', 'email', 'company', 'sector', 'role', 'consent', 'answers'] as $key) $data[$key] = tolx_input($key);
    if (!$data['name'] || !$data['company'] || !$data['sector'] || !$data['role'] || !is_email($data['email']) || $data['consent'] !== 'yes') wp_send_json_error(['message' => 'Complete all fields, provide a valid email and confirm consent.'], 400);
    $allowed = json_decode(file_get_contents(get_template_directory() . '/partials/assessment-fields.json'), true);
    if (!in_array($data['sector'], $allowed['sector'], true) || !in_array($data['role'], $allowed['role'], true)) wp_send_json_error(['message' => 'Select a valid sector and role.'], 400);
    $summary = tolx_assessment_summary($data['answers']);
    if (is_wp_error($summary)) wp_send_json_error(['message' => $summary->get_error_message()], 400);
    $result = tolx_save_submission('assessment', $data, $summary);
    if (is_wp_error($result)) wp_send_json_error(['message' => $result->get_error_message()], 503);
    wp_send_json_success($result);
}
add_action('wp_ajax_tolx_scorecard_lead', 'tolx_handle_scorecard_lead');
add_action('wp_ajax_nopriv_tolx_scorecard_lead', 'tolx_handle_scorecard_lead');
add_action('wp_footer', function () {
    if (is_page('scorecard') || is_page_template('page-scorecard.php')) echo '<script>window.TOLX_SC=' . wp_json_encode(['ajaxUrl' => admin_url('admin-ajax.php'), 'nonce' => wp_create_nonce('tolx_scorecard')], JSON_HEX_TAG | JSON_HEX_AMP | JSON_HEX_APOS | JSON_HEX_QUOT) . ';</script>';
}, 5);
function tolx_published_destination($slug, $fallback = '/solutions/') {
    $page = get_page_by_path($slug);
    return $page && get_post_status($page) === 'publish' ? get_permalink($page) : home_url($fallback);
}

// Expire duplicate-lock hashes; enquiry records require the administrator's retention review.
add_action('init', function () {
    if (!wp_next_scheduled('tolx_lead_cleanup')) wp_schedule_event(time() + HOUR_IN_SECONDS, 'daily', 'tolx_lead_cleanup');
});
add_action('tolx_lead_cleanup', function () {
    global $wpdb;
    $names = $wpdb->get_col($wpdb->prepare("SELECT option_name FROM {$wpdb->options} WHERE option_name LIKE %s", $wpdb->esc_like('tolx_lead_') . '%'));
    foreach ($names as $name) {
        $entry = get_option($name);
        if (is_array($entry) && !empty($entry['time']) && time() - $entry['time'] > DAY_IN_SECONDS) delete_option($name);
    }
});
add_action('switch_theme', function () { wp_clear_scheduled_hook('tolx_lead_cleanup'); });
