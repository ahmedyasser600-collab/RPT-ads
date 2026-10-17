<?php
/**
 * Template Name: Contact
 */

$form_sent = false; $form_error = false; $submission_result = null;
if (!function_exists('tolx_contact_topics')) {
    function tolx_contact_topics() {
        return [
            'crm'             => 'Orders & follow-ups',
            'revenue-assets'  => 'Stock & sales',
            'einvoicing'      => 'E-invoicing & VAT',
            'workflows'       => 'Team tasks & approvals',
            'reporting'       => 'Reports & dashboards',
            'marketing'       => 'Website & marketing',
            'not-sure'        => 'Not sure yet',
        ];
    }
}
if (($_SERVER['REQUEST_METHOD'] ?? '') === 'POST') {
    if (!wp_verify_nonce(tolx_input('tolx_contact_nonce'), 'tolx_contact_form')) {
        $form_error = 'Security check failed. Refresh this page and try again.';
    } elseif (tolx_input('contact_website')) {
        $form_error = 'Submission rejected.';
    } else {
        $data = [];
        // 'name' is a reserved WordPress query var; posting it makes WP return a 404 before this template runs.
        foreach (['name' => 'tolx_name', 'company' => 'company', 'email' => 'email', 'phone' => 'phone', 'message' => 'message', 'source' => 'source'] as $key => $field) $data[$key] = tolx_input($field, $key === 'message' ? 5000 : 200);
        // Topics: chips post improve[]; keep only known values, stored as readable labels.
        $picked = array_intersect(array_keys(tolx_contact_topics()), array_map('sanitize_key', (array) ($_POST['improve'] ?? [])));
        $data['industry'] = implode(', ', array_map(function ($k) { return tolx_contact_topics()[$k]; }, $picked));
        $data['tracking'] = tolx_input('tracking', 500);
        $data['consent'] = tolx_input('privacy_consent', 10) === 'yes' ? 'Agreed to the privacy policy (' . gmdate('Y-m-d H:i') . ' UTC)' : '';
        if (!$data['name'] || !is_email($data['email'])) $form_error = 'Please add your name and a valid email address.';
        elseif (!$data['consent']) $form_error = 'Please tick the box to agree to our privacy policy, so we can reply to you.';
        else {
            $submission_result = tolx_save_submission('contact', $data);
            if (is_wp_error($submission_result)) $form_error = $submission_result->get_error_message();
            else $form_sent = true;
        }
    }
}

get_header(); ?>
<?php if ($form_sent && !$submission_result['duplicate']) : ?><script>window.addEventListener('load', function () { if (window.tolxMeasure) window.tolxMeasure('enquiry_saved'); if (typeof window.gtag === 'function') window.gtag('event', 'generate_lead', { form: 'contact' }); });</script><?php endif; ?>

<section class="contact-v2">
  <div class="container contact-v2-grid">

    <div class="contact-v2-intro">
      <div class="contact-v2-crumbs"><?php tolx_render_breadcrumbs(); ?></div>
      <h1 class="contact-v2-title">Tell us what's hard to track.</h1>
      <p class="contact-v2-lead">Two minutes here. A reply within one business day. Then a 30-minute call to map how your business runs, before we propose anything.</p>
    </div>

    <div class="contact-v2-panel" id="enquiry">
      <div class="contact-v2-panel-head">
        <h2>Book your discovery call</h2>
        <p>Takes two minutes. We reply within one business day.</p>
      </div>
      <div class="contact-v2-panel-body">
      <?php if ($form_sent) : ?>
        <div class="cform-done" role="status">
          <span class="cform-done-mark" aria-hidden="true"><?php tolx_icon('check', 28); ?></span>
          <h2>Thanks, <?php echo esc_html(strtok($data['name'], ' ')); ?>. We've got it.</h2>
          <p>We'll reply within one business day. A confirmation is on its way to your inbox.</p>
          <p class="cform-done-alt">Need an answer sooner? <a href="https://wa.me/971509860063" target="_blank" rel="noopener">Message us on WhatsApp</a></p>
        </div>
      <?php else : ?>
        <form method="POST" action="#enquiry" class="cform" novalidate>
          <?php wp_nonce_field('tolx_contact_form', 'tolx_contact_nonce'); ?>
          <div style="position:absolute;left:-9999px" aria-hidden="true"><input name="contact_website" tabindex="-1" autocomplete="off"></div>
          <input type="hidden" name="tracking" value="<?php echo esc_attr(tolx_input('tracking', 500)); ?>">
          <input type="hidden" name="source" value="<?php echo esc_attr(tolx_input('source', 200)); ?>">

          <?php if ($form_error) : ?>
            <p class="cform-error" role="alert"><?php echo esc_html($form_error); ?></p>
          <?php endif; ?>

          <fieldset class="cform-topics">
            <legend>What should we look at first? <span class="cform-opt">Pick any that apply</span></legend>
            <div class="cform-tiles">
              <?php
              $picked_now = array_map('sanitize_key', (array) ($_POST['improve'] ?? []));
              $topic_icons = ['crm' => 'order', 'revenue-assets' => 'inventory', 'einvoicing' => 'billing', 'workflows' => 'project', 'reporting' => 'dashboard', 'marketing' => 'growth', 'not-sure' => 'chat'];
              foreach (tolx_contact_topics() as $key => $label) : ?>
                <label class="cform-tile<?php echo $key === 'not-sure' ? ' cform-tile--wide' : ''; ?>">
                  <input type="checkbox" name="improve[]" value="<?php echo esc_attr($key); ?>" <?php checked(in_array($key, $picked_now, true)); ?>>
                  <span class="cform-tile-icon" aria-hidden="true"><?php tolx_icon($topic_icons[$key], 20); ?></span>
                  <span class="cform-tile-text"><?php echo esc_html($label); ?></span>
                </label>
              <?php endforeach; ?>
            </div>
          </fieldset>

          <div class="cform-row">
            <div class="cform-field">
              <label for="name">Your name</label>
              <input type="text" id="name" name="tolx_name" autocomplete="name" required value="<?php echo esc_attr(tolx_input('tolx_name', 200)); ?>">
            </div>
            <div class="cform-field">
              <label for="company">Company <span class="cform-opt">optional</span></label>
              <input type="text" id="company" name="company" autocomplete="organization" value="<?php echo esc_attr(tolx_input('company', 200)); ?>">
            </div>
          </div>

          <div class="cform-row">
            <div class="cform-field">
              <label for="email">Work email</label>
              <input type="email" id="email" name="email" autocomplete="email" inputmode="email" required value="<?php echo esc_attr(tolx_input('email', 200)); ?>">
            </div>
            <div class="cform-field">
              <label for="phone">Phone or WhatsApp <span class="cform-opt">optional</span></label>
              <input type="tel" id="phone" name="phone" autocomplete="tel" inputmode="tel" placeholder="+971" value="<?php echo esc_attr(tolx_input('phone', 200)); ?>">
            </div>
          </div>

          <div class="cform-field">
            <label for="message">Anything we should know? <span class="cform-opt">optional</span></label>
            <textarea id="message" name="message" rows="2" placeholder="For example: we take about 40 orders a day on WhatsApp and lose track of follow-ups."><?php echo esc_textarea(tolx_input('message', 5000)); ?></textarea>
          </div>

          <div class="cform-consent-wrap">
            <label class="cform-consent">
              <input type="checkbox" id="privacy_consent" name="privacy_consent" value="yes" required <?php checked(tolx_input('privacy_consent', 10), 'yes'); ?>>
              <span class="cform-consent-box" aria-hidden="true"></span>
              <span class="cform-consent-text">I agree to the <a href="<?php echo home_url('/privacy-policy/'); ?>" target="_blank" rel="noopener">privacy policy</a> and to TOLX contacting me about my enquiry.</span>
            </label>
          </div>

          <button type="submit" class="cform-submit">Request my discovery call</button>
        </form>
      <?php endif; ?>
      </div>
    </div>

    <div class="contact-v2-after">
      <h2 class="contact-v2-h2">What happens next</h2>
      <ol class="contact-v2-steps">
        <li><strong>We reply within one business day,</strong> by email or WhatsApp, whichever you prefer.</li>
        <li><strong>A 30-minute discovery call.</strong> You walk us through how orders, stock and tasks move today.</li>
        <li><strong>A clear proposal.</strong> We map your operation first, then show how Odoo would run it.</li>
      </ol>

      <h2 class="contact-v2-h2">Rather talk now?</h2>
      <ul class="contact-v2-direct">
        <li><a href="https://wa.me/971509860063" target="_blank" rel="noopener"><?php tolx_icon('chat', 20); ?><span>WhatsApp us</span><span class="contact-v2-direct-sub">Replies the same day</span></a></li>
        <li><a href="tel:+971509860063"><?php tolx_icon('phone', 20); ?><span>+971 50 986 0063</span><span class="contact-v2-direct-sub">Call us</span></a></li>
        <li><a href="mailto:sales@tolx.ae"><?php tolx_icon('mail', 20); ?><span>sales@tolx.ae</span><span class="contact-v2-direct-sub">Email</span></a></li>
      </ul>

      <a href="<?php echo home_url('/about/odoo-partnership/'); ?>" class="contact-v2-partner">
        <span class="contact-v2-partner-badge"><img src="<?php echo get_template_directory_uri(); ?>/assets/img/odoo_ready_partners_rgb.svg" alt="Odoo Ready Partner badge" width="120" height="60" loading="lazy"></span>
        <span>Certified Odoo Ready Partner, based in Dubai.</span>
      </a>
    </div>

  </div>
</section>

<?php
// Contact page has its own footer (no CTA block — visitor is already converting here)
?>
</main>

<footer class="footer">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-brand">
        <a href="<?php echo home_url(); ?>" class="nav-logo">
          <?php tolx_helm(28); ?>
          <span class="nav-wordmark">TOLX<span>.</span></span>
        </a>
        <p>A UAE software house and business systems partner. We build systems around the assets, workflows, data, and digital channels that generate revenue. As an Odoo Ready Partner, we implement Odoo around how each business works.</p>
        <a href="<?php echo home_url('/about/odoo-partnership/'); ?>" class="footer-badge" aria-label="Odoo Ready Partner">
          <span class="odoo-badge-chip odoo-badge-chip--sm">
            <img src="<?php echo get_template_directory_uri(); ?>/assets/img/odoo_ready_partners_rgb.svg" alt="Odoo Ready Partner badge" width="68" height="34" loading="lazy">
          </span>
        </a>
      </div>
      <div>
        <h3>Systems</h3>
        <ul class="footer-links">
          <li><a href="<?php echo home_url('/solutions/'); ?>">Revenue Asset Systems</a></li>
          <li><a href="<?php echo home_url('/solutions/'); ?>">Workflow Automation</a></li>
          <li><a href="<?php echo home_url('/solutions/'); ?>">CRM &amp; Sales Operations</a></li>
          <li><a href="<?php echo home_url('/solutions/'); ?>">Dashboards &amp; Reporting</a></li>
          <li><a href="<?php echo home_url('/odoo/'); ?>">Odoo Configuration</a></li>
        </ul>
      </div>
      <div>
        <h3>Growth Systems</h3>
        <ul class="footer-links">
          <li><a href="<?php echo home_url('/growth-systems/'); ?>">Web Development</a></li>
          <li><a href="<?php echo home_url('/growth-systems/'); ?>">Marketing Systems</a></li>
          <li><a href="<?php echo home_url('/growth-systems/'); ?>">SEO &amp; Content</a></li>
          <li><a href="<?php echo home_url('/growth-systems/'); ?>">CRM &amp; Automation</a></li>
          <li><a href="<?php echo home_url('/growth-systems/'); ?>">Analytics &amp; Reporting</a></li>
        </ul>
      </div>
      <div>
        <h3>Company</h3>
        <ul class="footer-links">
          <li><a href="<?php echo home_url('/about/'); ?>">About</a></li>
          <li><a href="<?php echo home_url('/software-house-dubai/'); ?>">Software House Dubai</a></li>
          <li><a href="<?php echo home_url('/about/our-approach/'); ?>">Our Approach</a></li>
          <li><a href="<?php echo home_url('/blog/'); ?>">Blog</a></li>
        </ul>
      </div>
      <div>
        <h3>Get in Touch</h3>
        <ul class="footer-links">
          <li><a href="https://wa.me/971509860063" target="_blank" rel="noopener">WhatsApp</a></li>
          <li><a href="tel:+971509860063">+971 50 986 0063</a></li>
          <li><a href="mailto:sales@tolx.ae">sales@tolx.ae</a></li>
          <li><a href="https://www.linkedin.com/company/tolx1" target="_blank" rel="noopener">LinkedIn</a></li>
          <li>Dubai, UAE</li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <p>&copy; <?php echo date('Y'); ?> Tolx. All rights reserved.</p>
      <div class="footer-bottom-links">
        <a href="<?php echo home_url('/privacy-policy/'); ?>">Privacy Policy</a>
        <a href="<?php echo home_url('/terms-of-service/'); ?>">Terms of Service</a>
      </div>
    </div>
  </div>
</footer>

<?php wp_footer(); ?>
</body>
</html>
