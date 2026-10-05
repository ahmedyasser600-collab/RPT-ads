</main>

<?php // Reusable CTA Block — V2 command panel ?>
<section class="cta-section">
  <div class="container">
    <div class="cta-cmd fade-in">
      <div class="cta-cmd-tag">Next stop</div>
      <h2>Ready to replace spreadsheets with systems built around how your business runs?</h2>
      <p>Tell us what is hard to track: orders, stock, follow-ups or team updates. We implement Odoo around how you work and help your team adopt it.</p>
      <div class="cta-cmd-actions">
        <a href="<?php echo home_url('/contact/'); ?>" class="btn-primary">Book a Discovery Call <span>→</span></a>
        <a href="https://wa.me/971509860063" target="_blank" rel="noopener" class="btn-ghost">WhatsApp us</a>
      </div>
      <div class="cta-cmd-meta">30-minute discovery call · We map the operation before we propose anything</div>
    </div>
  </div>
</section>

<footer class="footer">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-brand">
        <a href="<?php echo home_url(); ?>" class="nav-logo">
          <?php tolx_helm(28); ?>
          <span class="nav-wordmark">TOLX<span>.</span></span>
        </a>
        <p>A Dubai software and business-systems company helping UAE SMEs organise orders, stock, customer follow-ups and team tasks. As an Odoo Ready Partner, we implement Odoo around your operation and support your team through adoption.</p>
        <a href="<?php echo home_url('/about/odoo-partnership/'); ?>" class="footer-badge" aria-label="Odoo Ready Partner">
          <span class="odoo-badge-chip odoo-badge-chip--sm">
            <img src="<?php echo get_template_directory_uri(); ?>/assets/img/odoo_ready_partners_rgb.svg" alt="Odoo Ready Partner badge" width="68" height="34" loading="lazy">
          </span>
        </a>
      </div>
      <div>
        <h3>Systems</h3>
        <ul class="footer-links">
          <li><a href="<?php echo esc_url(tolx_published_destination('stock-sales-management')); ?>">Stock &amp; Sales</a></li>
          <li><a href="<?php echo esc_url(tolx_published_destination('team-tasks-approvals')); ?>">Team Tasks &amp; Approvals</a></li>
          <li><a href="<?php echo esc_url(tolx_published_destination('order-tracking-customer-follow-up')); ?>">Orders &amp; Customer Follow-up</a></li>
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
          <li><a href="<?php echo home_url('/about/our-approach/'); ?>">Our Approach</a></li>
          <li><a href="<?php echo home_url('/software-house-dubai/'); ?>">Software House Dubai</a></li>
          <li><a href="<?php echo home_url('/blog/'); ?>">Blog</a></li>
        </ul>
      </div>
      <div>
        <h3>Get in Touch</h3>
        <ul class="footer-links">
          <li><a href="<?php echo home_url('/contact/'); ?>">Contact Us</a></li>
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

<a href="https://wa.me/971509860063" class="wa-float" target="_blank" rel="noopener" aria-label="Chat with Tolx on WhatsApp">
  <svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2.2A9.8 9.8 0 0 0 3.6 17l-1.4 4.8 4.9-1.3A9.8 9.8 0 1 0 12 2.2zm0 17.8a8 8 0 0 1-4.1-1.1l-.3-.2-2.9.8.8-2.8-.2-.3A8 8 0 1 1 12 20zm4.4-6c-.2-.1-1.4-.7-1.7-.8-.2-.1-.4-.1-.5.1l-.8 1c-.1.2-.3.2-.5.1a6.6 6.6 0 0 1-3.3-2.9c-.2-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.5-.4h-.5a.9.9 0 0 0-.7.3 2.8 2.8 0 0 0-.9 2.1 4.9 4.9 0 0 0 1 2.6 11.2 11.2 0 0 0 4.3 3.8c1.6.7 2.2.7 3 .6.5-.1 1.4-.6 1.6-1.1.2-.6.2-1 .1-1.1l-.5-.3z"/></svg>
  <span>WhatsApp us</span>
</a>

<?php wp_footer(); ?>
</body>
</html>
