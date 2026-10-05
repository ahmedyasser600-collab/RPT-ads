<?php // Reusable CTA Block — V2 command panel ?>
<section class="cta-section">
  <div class="container">
    <div class="cta-cmd fade-in">
      <div class="cta-cmd-tag">Next stop</div>
      <h2>Ready to replace spreadsheets with systems built around how your business runs?</h2>
      <p>Tell us what is hard to track: orders, stock, follow-ups or team updates. We help you choose and implement a suitable system, using Odoo when it fits.</p>
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
        <p>A Dubai software and business-systems company helping UAE SMEs organise orders, stock, customer follow-ups and team tasks. Suitable software, practical implementation and support for adoption, with Odoo as one possible foundation.</p>
        <a href="<?php echo home_url('/about/odoo-partnership/'); ?>" class="footer-badge" aria-label="Odoo Ready Partner">
          <span class="odoo-badge-chip odoo-badge-chip--sm">
            <img src="<?php echo get_template_directory_uri(); ?>/assets/img/odoo_ready_partners_rgb.svg" alt="Odoo Ready Partner badge" width="68" height="34" loading="lazy">
          </span>
        </a>
      </div>
      <div>
        <h4>Systems</h4>
        <ul class="footer-links">
          <li><a href="<?php echo esc_url(tolx_published_destination('stock-sales-management')); ?>">Stock &amp; Sales</a></li>
          <li><a href="<?php echo esc_url(tolx_published_destination('team-tasks-approvals')); ?>">Team Tasks &amp; Approvals</a></li>
          <li><a href="<?php echo esc_url(tolx_published_destination('order-tracking-customer-follow-up')); ?>">Orders &amp; Customer Follow-up</a></li>
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
          <li><a href="<?php echo home_url('/about/our-approach/'); ?>">Our Approach</a></li>
          <li><a href="<?php echo home_url('/software-house-dubai/'); ?>">Software House Dubai</a></li>
          <li><a href="<?php echo home_url('/blog/'); ?>">Blog</a></li>
        </ul>
      </div>
      <div>
        <h4>Get in Touch</h4>
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

<?php wp_footer(); ?>
</body>
</html>
