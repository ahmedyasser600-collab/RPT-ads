<?php
/**
 * Template Name: Contact
 */

$form_sent = false; $form_error = false; $submission_result = null;
if (($_SERVER['REQUEST_METHOD'] ?? '') === 'POST') {
    if (!wp_verify_nonce(tolx_input('tolx_contact_nonce'), 'tolx_contact_form')) {
        $form_error = 'Security check failed. Refresh this page and try again.';
    } elseif (tolx_input('contact_website')) {
        $form_error = 'Submission rejected.';
    } else {
        $data = [];
        foreach (['name', 'company', 'email', 'phone', 'industry', 'message', 'source'] as $key) $data[$key] = tolx_input($key, $key === 'message' ? 5000 : 200);
        if (!$data['name'] || !is_email($data['email']) || !$data['message']) $form_error = 'Enter your name, a valid email and your message.';
        else {
            $submission_result = tolx_save_submission('contact', $data);
            if (is_wp_error($submission_result)) $form_error = $submission_result->get_error_message();
            else $form_sent = true;
        }
    }
}

get_header(); ?>
<?php if ($form_sent && !$submission_result['duplicate']) : ?><script>window.addEventListener('load', function () { if (window.tolxMeasure) window.tolxMeasure('enquiry_saved'); });</script><?php endif; ?>

<div class="container"><?php tolx_render_breadcrumbs(); ?></div>

<section class="page-hero">
  <div class="container">
    <div class="fade-in">
      <div class="section-tag mono">Get in Touch</div>
      <h1>Let's find the right <em>starting point.</em></h1>
      <p>Tell us where orders, stock, quotations, follow-ups or team updates become hard to track. We help UAE SMEs choose suitable tools, connect information and put a practical process in place.</p>
    </div>
  </div>
</section>

<!-- ============================================
     EXPECTATION PANEL
     ============================================ -->
<section class="section-sm">
  <div class="container">
    <div class="cmd-panel fade-in" style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:24px;padding:32px 36px;">
      <div style="display:flex;align-items:center;gap:14px;">
        <span class="cmd-panel-dot"></span>
        <div>
          <div class="cmd-panel-title" style="margin-bottom:4px;">What to Expect</div>
          <div style="font-size:15px;color:var(--text);">30-minute discovery call · We map the operation before we propose anything</div>
        </div>
      </div>
      <div style="font-family:'Share Tech Mono',monospace;font-size:11px;letter-spacing:1.5px;text-transform:uppercase;color:var(--text-sec);">Reply within 1 business day</div>
    </div>
  </div>
</section>

<!-- ============================================
     CONTACT GRID
     ============================================ -->
<section class="section-sm" style="padding-top:0;">
  <div class="container">

    <?php
    // Optional contact-page hero image — renders only if uploaded
    $contact_img = get_theme_mod('tolx_img_contact_hero', '');
    if (!empty($contact_img)):
    ?>
    <div class="fade-in" style="margin-bottom: 48px;">
      <?php
      tolx_image_slot('contact_hero', null, [
          'alt'           => 'Tolx — Dubai software house and business systems partner',
          'wrapper_class' => 'tolx-img-wrap--wide',
      ]);
      ?>
    </div>
    <?php endif; ?>

    <div class="hero-grid">

      <!-- LEFT — FORM -->
      <div class="fade-in">
        <h2 style="font-size:24px;font-weight:600;margin-bottom:24px;letter-spacing:-0.4px;">Send us a message</h2>

        <?php if ($form_sent) : ?>
          <div class="cmd-panel" style="padding:48px 32px;text-align:center;">
            <div class="card-icon" style="margin:0 auto 18px;">
              <?php tolx_icon('check', 24); ?>
            </div>
            <h3 style="font-size:20px;font-weight:600;margin-bottom:8px;">Enquiry saved.</h3>
            <p style="font-size:15px;color:var(--text-sec);"><?php echo esc_html($submission_result['message']); ?></p>
          </div>
        <?php else : ?>

          <?php if ($form_error) : ?>
            <div style="background:var(--status-alert-soft);border:1px solid rgba(220,60,60,0.2);border-radius:8px;padding:16px 20px;margin-bottom:24px;">
              <p style="font-size:14px;color:var(--text);margin:0;"><?php echo esc_html($form_error); ?></p>
            </div>
          <?php endif; ?>

          <form method="POST" action="">
            <?php wp_nonce_field('tolx_contact_form', 'tolx_contact_nonce'); ?>
            <div style="position:absolute;left:-9999px" aria-hidden="true"><input name="contact_website" tabindex="-1" autocomplete="off"></div>

            <div class="form-group">
              <label class="form-label" for="name">Your Name *</label>
              <input type="text" id="name" name="name" class="form-input" placeholder="Full name" required value="<?php echo esc_attr(tolx_input('name', 5000)); ?>">
            </div>
            <div class="form-group">
              <label class="form-label" for="company">Company</label>
              <input type="text" id="company" name="company" class="form-input" placeholder="Company name" value="<?php echo esc_attr(tolx_input('company', 5000)); ?>">
            </div>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">
              <div class="form-group">
                <label class="form-label" for="email">Email *</label>
                <input type="email" id="email" name="email" class="form-input" placeholder="you@company.com" required value="<?php echo esc_attr(tolx_input('email', 5000)); ?>">
              </div>
              <div class="form-group">
                <label class="form-label" for="phone">Phone</label>
                <input type="tel" id="phone" name="phone" class="form-input" placeholder="+971 5X XXX XXXX" value="<?php echo esc_attr(tolx_input('phone', 5000)); ?>">
              </div>
            </div>
            <div class="form-group">
              <label class="form-label" for="industry">What do you want to improve?</label>
              <select id="industry" name="industry" class="form-select">
                <option value="">Select what you'd like to improve</option>
                <option value="workflows" <?php selected(tolx_input('industry', 5000), 'workflows'); ?>>Team tasks and approvals</option>
                <option value="revenue-assets" <?php selected(tolx_input('industry', 5000), 'revenue-assets'); ?>>Stock and sales</option>
                <option value="website" <?php selected(tolx_input('industry', 5000), 'website'); ?>>Website / digital presence</option>
                <option value="marketing" <?php selected(tolx_input('industry', 5000), 'marketing'); ?>>Marketing and lead generation</option>
                <option value="crm" <?php selected(tolx_input('industry', 5000), 'crm'); ?>>Order tracking and customer follow-up</option>
                <option value="automation" <?php selected(tolx_input('industry', 5000), 'automation'); ?>>Automation / integrations</option>
                <option value="reporting" <?php selected(tolx_input('industry', 5000), 'reporting'); ?>>Reporting / dashboards</option>
                <option value="odoo" <?php selected(tolx_input('industry', 5000), 'odoo'); ?>>Odoo configuration</option>
                <option value="not-sure" <?php selected(tolx_input('industry', 5000), 'not-sure'); ?>>Not sure yet</option>
              </select>
            </div>
            <div class="form-group">
              <label class="form-label" for="message">Message *</label>
              <textarea id="message" name="message" class="form-textarea" placeholder="Tell us about your operation and what you're looking for..." required><?php echo esc_textarea(tolx_input('message', 5000)); ?></textarea>
            </div>
            <div class="form-group">
              <label class="form-label" for="source">How did you hear about us?</label>
              <select id="source" name="source" class="form-select">
                <option value="">Select one</option>
                <option value="google" <?php selected(tolx_input('source', 5000), 'google'); ?>>Google Search</option>
                <option value="linkedin" <?php selected(tolx_input('source', 5000), 'linkedin'); ?>>LinkedIn</option>
                <option value="referral" <?php selected(tolx_input('source', 5000), 'referral'); ?>>Referral</option>
                <option value="odoo" <?php selected(tolx_input('source', 5000), 'odoo'); ?>>Odoo.com</option>
                <option value="event" <?php selected(tolx_input('source', 5000), 'event'); ?>>Event / Conference</option>
                <option value="other" <?php selected(tolx_input('source', 5000), 'other'); ?>>Other</option>
              </select>
            </div>
            <button type="submit" class="btn-primary" style="width:100%;justify-content:center;margin-top:8px;">Send Message <span>→</span></button>
          </form>
          <p style="font-size:13px;color:var(--text-sec);margin-top:14px;text-align:center;">We respond to all enquiries within 1 business day.</p>
        <?php endif; ?>
      </div>

      <!-- RIGHT — CONTACT CHANNELS -->
      <div class="fade-in" data-stagger="1">
        <h2 style="font-size:24px;font-weight:600;margin-bottom:24px;letter-spacing:-0.4px;">Other ways to reach us</h2>

        <div class="op-grid" style="grid-template-columns:1fr;gap:14px;">

          <a href="tel:+971509860063" class="op-block" style="text-decoration:none;color:inherit;">
            <div class="op-block-icon"><?php tolx_icon('phone', 18); ?></div>
            <div>
              <h4>Call Us</h4>
              <p style="font-family:'Share Tech Mono',monospace;color:var(--gold);letter-spacing:0.5px;">+971 50 986 0063</p>
            </div>
          </a>

          <a href="https://wa.me/971509860063" target="_blank" rel="noopener" class="op-block" style="text-decoration:none;color:inherit;">
            <div class="op-block-icon"><?php tolx_icon('chat', 18); ?></div>
            <div>
              <h4>WhatsApp</h4>
              <p>Message us directly. Replies same day.</p>
            </div>
          </a>

          <a href="mailto:sales@tolx.ae" class="op-block" style="text-decoration:none;color:inherit;">
            <div class="op-block-icon"><?php tolx_icon('mail', 18); ?></div>
            <div>
              <h4>Email</h4>
              <p style="font-family:'Share Tech Mono',monospace;color:var(--gold);letter-spacing:0.5px;font-size:13px;">sales@tolx.ae</p>
            </div>
          </a>

          <a href="https://www.linkedin.com/company/tolx1" target="_blank" rel="noopener" class="op-block" style="text-decoration:none;color:inherit;">
            <div class="op-block-icon"><?php tolx_icon('linkedin', 18); ?></div>
            <div>
              <h4>LinkedIn</h4>
              <p>Follow for industry insights and updates.</p>
            </div>
          </a>

          <div class="op-block">
            <div class="op-block-icon"><?php tolx_icon('pin', 18); ?></div>
            <div>
              <h4>Office</h4>
              <p>Dubai, United Arab Emirates</p>
            </div>
          </div>

        </div>
      </div>

    </div>
  </div>
</section>

<?php
// Contact page has its own footer (no CTA block — visitor is already converting here)
?>
<footer class="footer">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-brand">
        <a href="<?php echo home_url(); ?>" class="nav-logo">
          <?php tolx_helm(28); ?>
          <span class="nav-wordmark">TOLX<span>.</span></span>
        </a>
        <p>A UAE software house and business systems partner. We build systems around the assets, workflows, data, and digital channels that generate revenue. Odoo is our most established foundation, and one of several.</p>
        <a href="<?php echo home_url('/about/odoo-partnership/'); ?>" class="footer-badge" aria-label="Odoo Ready Partner">
          <span class="odoo-badge-chip odoo-badge-chip--sm">
            <img src="<?php echo get_template_directory_uri(); ?>/assets/img/odoo_ready_partners_rgb.svg" alt="Odoo Ready Partner badge" width="68" height="34" loading="lazy">
          </span>
        </a>
      </div>
      <div>
        <h4>Systems</h4>
        <ul class="footer-links">
          <li><a href="<?php echo home_url('/solutions/'); ?>">Revenue Asset Systems</a></li>
          <li><a href="<?php echo home_url('/solutions/'); ?>">Workflow Automation</a></li>
          <li><a href="<?php echo home_url('/solutions/'); ?>">CRM &amp; Sales Operations</a></li>
          <li><a href="<?php echo home_url('/solutions/'); ?>">Dashboards &amp; Reporting</a></li>
          <li><a href="<?php echo home_url('/odoo/'); ?>">Odoo Configuration</a></li>
        </ul>
      </div>
      <div>
        <h4>Growth Systems</h4>
        <ul class="footer-links">
          <li><a href="<?php echo home_url('/growth-systems/'); ?>">Web Development</a></li>
          <li><a href="<?php echo home_url('/growth-systems/'); ?>">Marketing Systems</a></li>
          <li><a href="<?php echo home_url('/growth-systems/'); ?>">SEO &amp; Content</a></li>
          <li><a href="<?php echo home_url('/growth-systems/'); ?>">CRM &amp; Automation</a></li>
          <li><a href="<?php echo home_url('/growth-systems/'); ?>">Analytics &amp; Reporting</a></li>
        </ul>
      </div>
      <div>
        <h4>Company</h4>
        <ul class="footer-links">
          <li><a href="<?php echo home_url('/about/'); ?>">About</a></li>
          <li><a href="<?php echo home_url('/software-house-dubai/'); ?>">Software House Dubai</a></li>
          <li><a href="<?php echo home_url('/about/our-approach/'); ?>">Our Approach</a></li>
          <li><a href="<?php echo home_url('/blog/'); ?>">Blog</a></li>
        </ul>
      </div>
      <div>
        <h4>Get in Touch</h4>
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
