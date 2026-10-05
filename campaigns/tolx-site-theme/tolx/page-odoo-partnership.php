<?php
/**
 * Template Name: Odoo Partnership
 */
get_header(); ?>

<div class="container"><?php tolx_render_breadcrumbs(); ?></div>

<section class="page-hero">
  <div class="container">
    <div class="fade-in">
      <div class="section-tag mono">Odoo Partnership</div>
      <h1>Built on Odoo. <em>One of several foundations.</em></h1>
      <p>Tolx is a UAE software house and a certified Odoo Ready Partner. Here's why <a href="<?php echo home_url('/odoo/'); ?>" style="color:inherit;border-bottom:1px solid var(--gold);text-decoration:none;">Odoo</a> is our most established foundation, one of several, and what working with a certified partner means for your project.</p>
    </div>
  </div>
</section>

<!-- ============================================
     READY PARTNER FEATURE BANNER (Phase 5.2)
     Blog-feature-scale badge treatment
     ============================================ -->
<section class="section-sm">
  <div class="container">
    <div class="odoo-badge-feature fade-in">
      <img src="<?php echo get_template_directory_uri(); ?>/assets/img/odoo_ready_partners_rgb.svg" alt="Odoo Ready Partner badge" width="600" height="300" loading="lazy">
    </div>
  </div>
</section>

<!-- ============================================
     WHY ODOO + COMPARISON
     ============================================ -->
<section class="section">
  <div class="container">
    <div class="hero-grid">

      <div class="fade-in">
        <div class="section-tag mono">Why Odoo</div>
        <h2 class="section-title">An open-source ERP foundation, configured for your operation.</h2>
        <p style="font-size:16px;color:var(--text-sec);line-height:1.7;margin-bottom:16px;">Odoo is a modular open-source ERP that covers every business function — from accounting and inventory to field service and project management. It's proven across thousands of operators globally and supported by an active development ecosystem.</p>
        <p style="font-size:16px;color:var(--text-sec);line-height:1.7;margin-bottom:16px;">For UAE businesses that have outgrown spreadsheets, Odoo offers enterprise-grade capability without the enterprise overhead. It's a strong platform for companies that need integrated operations but don't need SAP or Oracle.</p>
        <p style="font-size:16px;color:var(--text-sec);line-height:1.7;">When Odoo is the right foundation, it gives us the flexibility to build deep configurations around how the operation actually runs. Something that would be prohibitively expensive on rigid enterprise platforms.</p>
      </div>

      <div class="fade-in" data-stagger="1">
        <div class="section-tag mono">Foundation properties</div>
        <h2 class="section-title">What Odoo gives you.</h2>
        <div class="op-grid" style="grid-template-columns:1fr;margin-top:8px;">
          <div class="op-block">
            <div class="op-block-icon"><?php tolx_icon('open-source', 18); ?></div>
            <div>
              <h4>Open Source</h4>
              <p>You own the system and your data. No vendor lock-in, no licence trap.</p>
            </div>
          </div>
          <div class="op-block">
            <div class="op-block-icon"><?php tolx_icon('module', 18); ?></div>
            <div>
              <h4>Modular Architecture</h4>
              <p>Start with the modules you need. Add more as the operation grows. No big-bang migrations.</p>
            </div>
          </div>
          <div class="op-block">
            <div class="op-block-icon"><?php tolx_icon('shield', 18); ?></div>
            <div>
              <h4>UAE Compliance Ready</h4>
              <p>VAT-aware, DEWA-compatible, RTA-friendly, Arabic-capable — configured, not bolted on.</p>
            </div>
          </div>
          <div class="op-block">
            <div class="op-block-icon"><?php tolx_icon('settings', 18); ?></div>
            <div>
              <h4>Configurable, Not Custom</h4>
              <p>Most needs are met through configuration. Custom code is the exception, not the default.</p>
            </div>
          </div>
        </div>
      </div>

    </div>
  </div>
</section>

<!-- ============================================
     ODOO vs ALTERNATIVES
     ============================================ -->
<section class="section">
  <div class="container">
    <div class="section-head fade-in">
      <div>
        <div class="section-tag mono">Odoo vs alternatives</div>
        <h2 class="section-title">Where Odoo fits in the ERP landscape.</h2>
      </div>
    </div>

    <div class="compare-grid fade-in">
      <div class="compare-col compare-col--neg">
        <div class="compare-col-head">
          <span class="compare-col-tag">SAP / Oracle</span>
        </div>
        <ul class="compare-list">
          <li>Enterprise budget required</li>
          <li>Long implementation cycles</li>
          <li>Rigid module structure</li>
          <li>Vendor lock-in</li>
          <li>Global configuration, local adjustments</li>
        </ul>
      </div>
      <div class="compare-col compare-col--pos">
        <div class="compare-col-head">
          <span class="compare-col-tag">Odoo (configured by Tolx)</span>
        </div>
        <ul class="compare-list">
          <li>SME-friendly licensing</li>
          <li>4–8 week go-live cycles</li>
          <li>Fully modular and configurable</li>
          <li>Open source — you own it</li>
          <li>UAE compliance configured into the system</li>
        </ul>
      </div>
    </div>
  </div>
</section>

<!-- ============================================
     READY PARTNER STATUS (Phase 5.2)
     ============================================ -->
<section class="section-sm">
  <div class="container">
    <div class="partner-strip fade-in">
      <div class="odoo-badge-chip">
        <img src="<?php echo get_template_directory_uri(); ?>/assets/img/odoo_ready_partners_rgb.svg" alt="Odoo Ready Partner badge" width="144" height="72" loading="lazy">
      </div>
      <div class="partner-strip-copy">
        <div class="section-tag mono">Partner status</div>
        <p style="margin-bottom:10px;">Certified Odoo Ready Partner. Local implementation, UAE compliance built in.</p>
        <p style="font-size:14.5px;color:var(--text-sec);line-height:1.65;">Ready Partner is an official certification tier issued by Odoo. It confirms certified consultants, verified delivery, and a listing in Odoo's partner directory. The badge is issued and verified by Odoo, not self-declared.</p>
      </div>
      <a href="<?php echo home_url('/operations-readiness-scorecard/'); ?>" class="partner-strip-link">Check your operations readiness →</a>
    </div>
  </div>
</section>

<!-- ============================================
     WHAT BEING A PARTNER MEANS
     ============================================ -->
<section class="section">
  <div class="container">
    <div class="section-head fade-in">
      <div>
        <div class="section-tag mono">What it means for you</div>
        <h2 class="section-title">Working with a certified partner.</h2>
      </div>
    </div>
    <div class="diag-grid">
      <div class="diag-card fade-in" data-stagger="1">
        <div class="diag-card-tag">01 · Benefit</div>
        <h3>Certified Consultants</h3>
        <p>Our team holds Odoo functional certifications. We know the platform's modules, workflows, and limitations.</p>
      </div>
      <div class="diag-card fade-in" data-stagger="2">
        <div class="diag-card-tag">02 · Benefit</div>
        <h3>Direct Odoo Support</h3>
        <p>As a partner, we escalate directly to Odoo's technical team when an edge case requires platform-level support.</p>
      </div>
      <div class="diag-card fade-in" data-stagger="3">
        <div class="diag-card-tag">03 · Benefit</div>
        <h3>Partner Tools</h3>
        <p>Development environments, staging servers, and migration tools available only to certified partners.</p>
      </div>
      <div class="diag-card fade-in" data-stagger="4">
        <div class="diag-card-tag">04 · Benefit</div>
        <h3>Listed on Odoo.com</h3>
        <p>Verified by Odoo as a qualified implementation partner — listed in the official partner directory.</p>
      </div>
    </div>
  </div>
</section>

<!-- ============================================
     ODOO CLUSTER LINKS
     ============================================ -->
<section class="section">
  <div class="container">
    <div class="section-head fade-in">
      <div>
        <div class="section-tag mono">More on Odoo</div>
        <h2 class="section-title">Continue exploring.</h2>
      </div>
    </div>
    <div class="op-grid op-grid--modules">
      <a href="<?php echo home_url('/odoo/'); ?>" class="op-block fade-in" data-stagger="1" style="text-decoration: none; color: inherit;">
        <div class="op-block-icon"><?php tolx_icon('module', 18); ?></div>
        <div>
          <h4>What is Odoo?</h4>
          <p>The full UAE operator's guide to what Odoo is, what's in the toolbox, and where it fits.</p>
        </div>
      </a>
      <a href="<?php echo home_url('/odoo/uae-implementation/'); ?>" class="op-block fade-in" data-stagger="2" style="text-decoration: none; color: inherit;">
        <div class="op-block-icon"><?php tolx_icon('settings', 18); ?></div>
        <div>
          <h4>Odoo Implementation in the UAE</h4>
          <p>What a real Odoo implementation looks like with a Dubai-based partner.</p>
        </div>
      </a>
      <a href="<?php echo home_url('/solutions/'); ?>" class="op-block fade-in" data-stagger="3" style="text-decoration: none; color: inherit;">
        <div class="op-block-icon"><?php tolx_icon('module', 18); ?></div>
        <div>
          <h4>Systems Beyond Odoo</h4>
          <p>Where Odoo fits alongside custom software, automation, web, CRM, and dashboards.</p>
        </div>
      </a>
      <a href="<?php echo home_url('/odoo-partner-dubai/'); ?>" class="op-block fade-in" data-stagger="4" style="text-decoration: none; color: inherit;">
        <div class="op-block-icon"><?php tolx_icon('shield', 18); ?></div>
        <div>
          <h4>Odoo Partner in Dubai</h4>
          <p>How to choose an Odoo partner in Dubai, and what working with Tolx looks like.</p>
        </div>
      </a>
    </div>
  </div>
</section>

<?php get_footer(); ?>
