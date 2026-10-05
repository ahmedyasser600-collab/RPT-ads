<?php
/**
 * Template Name: Home
 * The front page template
 */
get_header(); ?>

<!-- ============================================
     HERO — split layout
     ============================================ -->
<section class="hero"<?php echo tolx_homepage_hero_bg_style(); ?>>
  <div class="hero-fx" aria-hidden="true">
    <div class="hero-fx-aurora"></div>
    <div class="hero-fx-floor"></div>
    <div class="hero-fx-horizon"></div>
    <?php foreach (array(6, 14, 23, 31, 42, 55, 63, 71, 79, 88, 94) as $i => $x) : ?>
      <span class="hero-fx-p" style="--x:<?php echo $x; ?>%;--d:<?php echo 7 + ($i % 4) * 2; ?>s;--t:<?php echo ($i * 0.9) % 7; ?>s"></span>
    <?php endforeach; ?>
  </div>
  <div class="container">
    <div class="hero-grid">

      <div class="hero-content fade-in">
        <div class="hero-tag mono section-tag">UAE Software House · Business Systems Partner</div>
        <h1>
          <span class="line">Keep track of</span>
          <span class="line">your
            <span class="flip-wrapper">
              <span class="flip-sizer">workflows</span>
              <span class="flip-clip">
                <span class="flip-word">orders</span>
                <span class="flip-word">workflows</span>
              </span>
            </span>
          </span>
          <span class="line">as your business grows.</span>
        </h1>
        <p class="hero-sub">Orders in WhatsApp, stock in Excel, follow-ups in email? Tolx helps UAE SMEs organise sales, stock and team tasks. As an Odoo Ready Partner we implement Odoo around how you work, or another solution when Odoo isn't the right fit, and support your team as they adopt it.</p>
        <div class="hero-actions">
          <a href="<?php echo home_url('/contact/'); ?>" class="btn-primary">Book a Discovery Call <span>→</span></a>
          <a href="<?php echo home_url('/solutions/'); ?>" class="btn-ghost">See Our Systems</a>
        </div>
        <p class="hero-alt">Prefer WhatsApp? <a href="https://wa.me/971509860063" target="_blank" rel="noopener">Message us on +971 50 986 0063</a></p>
      </div>

      <!-- Operational command visual (right side) -->
      <div class="hero-cmd" aria-hidden="true">
        <div class="cmd-panel">
          <div class="cmd-scan"></div>
          <div class="cmd-panel-head">
            <div class="cmd-panel-title">Tolx · Operations Layer</div>
            <div class="cmd-panel-meta"><span class="cmd-panel-dot"></span> Live</div>
          </div>

          <div class="cmd-row">
            <div class="cmd-row-icon"><?php tolx_icon('asset', 18); ?></div>
            <div class="cmd-row-label">Revenue Assets</div>
            <div class="cmd-row-tag">Visibility</div>
          </div>

          <div class="cmd-row">
            <div class="cmd-row-icon"><?php tolx_icon('route', 18); ?></div>
            <div class="cmd-row-label">Workflows</div>
            <div class="cmd-row-tag">Automation</div>
          </div>

          <div class="cmd-row">
            <div class="cmd-row-icon"><?php tolx_icon('revenue', 18); ?></div>
            <div class="cmd-row-label">Pipeline &amp; CRM</div>
            <div class="cmd-row-tag">Sales Ops</div>
          </div>

          <!-- Module grid -->
          <div class="hero-cmd-modules">
            <div class="hero-cmd-module is-live">
              <span class="hero-cmd-module-status"></span>
              <?php tolx_icon('asset', 18); ?>
              <div class="hero-cmd-module-label">Revenue Assets</div>
            </div>
            <div class="hero-cmd-module is-live">
              <span class="hero-cmd-module-status"></span>
              <?php tolx_icon('project', 18); ?>
              <div class="hero-cmd-module-label">Workflows</div>
            </div>
            <div class="hero-cmd-module is-live">
              <span class="hero-cmd-module-status"></span>
              <?php tolx_icon('revenue', 18); ?>
              <div class="hero-cmd-module-label">CRM</div>
            </div>
            <div class="hero-cmd-module">
              <span class="hero-cmd-module-status"></span>
              <?php tolx_icon('inventory', 18); ?>
              <div class="hero-cmd-module-label">Inventory</div>
            </div>
            <div class="hero-cmd-module">
              <span class="hero-cmd-module-status"></span>
              <?php tolx_icon('billing', 18); ?>
              <div class="hero-cmd-module-label">Billing</div>
            </div>
            <div class="hero-cmd-module">
              <span class="hero-cmd-module-status"></span>
              <?php tolx_icon('dashboard', 18); ?>
              <div class="hero-cmd-module-label">Dashboards</div>
            </div>
          </div>

          <!-- Route line -->
          <div class="hero-cmd-route">
            <div class="hero-cmd-route-label">Discovery</div>
            <div class="hero-cmd-route-line"><span class="cmd-packet"></span></div>
            <div class="hero-cmd-route-label">Go Live</div>
          </div>
        </div>
      </div>

    </div>
  </div>
</section>

<!-- ============================================
     PROBLEM DIAGNOSTIC
     ============================================ -->
<section class="section">
  <div class="container">
    <div class="section-head fade-in">
      <div>
        <div class="section-tag mono">Sound familiar?</div>
        <h2 class="section-title">The signals you've outgrown your current setup.</h2>
      </div>
    </div>
    <div class="diag-grid">
      <div class="diag-card fade-in" data-stagger="1">
        <div class="diag-card-tag">01 · Signal</div>
        <h3>Spreadsheet dependency</h3>
        <p>The operation lives in Excel files and chat threads. Nothing reconciles, nothing scales.</p>
      </div>
      <div class="diag-card fade-in" data-stagger="2">
        <div class="diag-card-tag">02 · Signal</div>
        <h3>Disconnected tools</h3>
        <p>Each app is fine on its own. The trouble starts where they're meant to agree and don't. Data gets re-entered, handoffs slip.</p>
      </div>
      <div class="diag-card fade-in" data-stagger="3">
        <div class="diag-card-tag">03 · Signal</div>
        <h3>No real-time visibility</h3>
        <p>You can't say where an asset, order, or account stands right now. Decisions wait on someone finding the truth.</p>
      </div>
      <div class="diag-card fade-in" data-stagger="4">
        <div class="diag-card-tag">04 · Signal</div>
        <h3>Software that doesn't fit</h3>
        <p>The last system asked you to change how you work to match how it was built. Half the team quietly went back to spreadsheets.</p>
      </div>
    </div>
  </div>
</section>

<!-- ============================================
     SOLUTIONS MATRIX
     ============================================ -->
<section class="section">
  <div class="container">
    <div class="section-head">
      <div class="fade-in">
        <div class="section-tag mono">What we build</div>
        <h2 class="section-title">Systems built around how your business runs.</h2>
      </div>
      <a href="<?php echo home_url('/solutions/'); ?>" class="card-link fade-in" data-stagger="1">View all systems →</a>
    </div>

    <div class="sol-matrix">

      <a href="<?php echo home_url('/solutions/'); ?>" class="sol-card is-primary fade-in" data-stagger="1">
        <div class="sol-card-head">
          <div class="sol-card-icon"><?php tolx_icon('asset', 22); ?></div>
          <div class="sol-card-tag">Core System</div>
        </div>
        <h3>Revenue Asset Systems</h3>
        <p>Manage the assets, capacity, contracts, teams, and workflows that generate revenue, with the visibility to run them instead of chase them.</p>
        <div class="sol-card-foot">
          <div class="chip-row">
            <span class="chip">Assets</span>
            <span class="chip">Capacity</span>
            <span class="chip">Contracts</span>
            <span class="chip">Teams</span>
            <span class="chip">Workflows</span>
          </div>
          <span class="sol-card-link">Explore the system</span>
        </div>
      </a>

      <a href="<?php echo home_url('/solutions/'); ?>" class="sol-card fade-in" data-stagger="2">
        <div class="sol-card-head">
          <div class="sol-card-icon"><?php tolx_icon('project', 22); ?></div>
        </div>
        <h3>Workflow Automation</h3>
        <p>Reduce manual work, approvals, double entry, and disconnected handoffs across the operation.</p>
        <div class="sol-card-foot">
          <div class="chip-row">
            <span class="chip">Approvals</span>
            <span class="chip">Automation</span>
            <span class="chip">Handoffs</span>
          </div>
          <span class="sol-card-link">Explore</span>
        </div>
      </a>

      <a href="<?php echo home_url('/solutions/'); ?>" class="sol-card fade-in" data-stagger="3">
        <div class="sol-card-head">
          <div class="sol-card-icon"><?php tolx_icon('revenue', 22); ?></div>
        </div>
        <h3>CRM &amp; Sales Operations</h3>
        <p>Structure leads, follow-ups, quotes, pipelines, and client records, with revenue visibility built in.</p>
        <div class="sol-card-foot">
          <div class="chip-row">
            <span class="chip">Leads</span>
            <span class="chip">Pipeline</span>
            <span class="chip">Quotes</span>
          </div>
          <span class="sol-card-link">Explore</span>
        </div>
      </a>

      <a href="<?php echo home_url('/solutions/'); ?>" class="sol-card fade-in" data-stagger="4">
        <div class="sol-card-head">
          <div class="sol-card-icon"><?php tolx_icon('dashboard', 22); ?></div>
        </div>
        <h3>Dashboards &amp; Reporting</h3>
        <p>Turn scattered data into clear operational and commercial decisions, in real time.</p>
        <div class="sol-card-foot">
          <div class="chip-row">
            <span class="chip">KPIs</span>
            <span class="chip">Reporting</span>
            <span class="chip">Visibility</span>
          </div>
          <span class="sol-card-link">Explore</span>
        </div>
      </a>

      <a href="<?php echo home_url('/growth-systems/'); ?>" class="sol-card fade-in" data-stagger="5">
        <div class="sol-card-head">
          <div class="sol-card-icon"><?php tolx_icon('module', 22); ?></div>
          <div class="sol-card-tag">Growth Systems</div>
        </div>
        <h3>Web &amp; Digital Infrastructure</h3>
        <p>Websites, landing pages, SEO foundations, analytics, and a conversion-focused digital presence.</p>
        <div class="sol-card-foot">
          <div class="chip-row">
            <span class="chip">Web</span>
            <span class="chip">SEO</span>
            <span class="chip">Analytics</span>
          </div>
          <span class="sol-card-link">Explore</span>
        </div>
      </a>

      <a href="<?php echo home_url('/growth-systems/'); ?>" class="sol-card fade-in" data-stagger="6">
        <div class="sol-card-head">
          <div class="sol-card-icon"><?php tolx_icon('route', 22); ?></div>
          <div class="sol-card-tag">Growth Systems</div>
        </div>
        <h3>Marketing Systems</h3>
        <p>Campaign planning, content systems, paid media setup, tracking, and growth workflows.</p>
        <div class="sol-card-foot">
          <div class="chip-row">
            <span class="chip">Campaigns</span>
            <span class="chip">Content</span>
            <span class="chip">Tracking</span>
          </div>
          <span class="sol-card-link">Explore</span>
        </div>
      </a>

    </div>
  </div>
</section>

<!-- ============================================
     ODOO READY PARTNER STRIP (Phase 5.2)
     ============================================ -->
<section class="section-sm">
  <div class="container">
    <div class="partner-strip partner-strip--lg fade-in">
      <a href="<?php echo home_url('/about/odoo-partnership/'); ?>" class="odoo-badge-chip odoo-badge-chip--lg" aria-label="Odoo Ready Partner">
        <img src="<?php echo get_template_directory_uri(); ?>/assets/img/odoo_ready_partners_rgb.svg" alt="Odoo Ready Partner badge" width="240" height="120" loading="lazy">
      </a>
      <div class="partner-strip-copy">
        <div class="section-tag mono">Verified by Odoo</div>
        <p>Certified Odoo Ready Partner. Local implementation, UAE compliance built in.</p>
      </div>
      <a href="<?php echo home_url('/about/odoo-partnership/'); ?>" class="partner-strip-link">About our partner status →</a>
    </div>
  </div>
</section>

<!-- ============================================
     MORE THAN SOFTWARE — Growth Systems intro
     ============================================ -->
<section class="section-sm">
  <div class="container">
    <div class="cmd-panel beyond-panel fade-in">
      <div class="beyond-panel-grid">
        <div>
          <div class="cmd-panel-title" style="margin-bottom:14px;">More than software</div>
          <h2 style="font-size:clamp(24px,3vw,32px);font-weight:700;letter-spacing:-0.6px;line-height:1.2;margin-bottom:14px;">Systems for how the business runs, and how it grows.</h2>
          <p style="font-size:15.5px;color:var(--text-sec);line-height:1.7;margin-bottom:20px;">We don't treat software, automation, CRM, dashboards, websites, and campaigns as separate pieces. We connect them around one question: how does the business generate revenue, and where is the system slowing it down?</p>
          <a href="<?php echo home_url('/growth-systems/'); ?>" class="btn-ghost">Explore Growth Systems →</a>
        </div>
        <div class="beyond-panel-tags">
          <span class="chip">Business Analysis</span>
          <span class="chip">Custom Software</span>
          <span class="chip">Odoo Configuration</span>
          <span class="chip">Workflow Automation</span>
          <span class="chip">Web Development</span>
          <span class="chip">Marketing Systems</span>
          <span class="chip">CRM &amp; Dashboards</span>
          <span class="chip">SEO &amp; Analytics</span>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- ============================================
     STATS — values strip
     ============================================ -->
<section class="stats">
  <div class="container">
    <div class="stats-inner fade-in">
      <div class="stat">
        <div class="stat-label mono">Delivery</div>
        <div class="stat-value">Scope-led</div>
        <div class="stat-note">Defined before any build starts</div>
      </div>
      <div class="stat">
        <div class="stat-label mono">Compliance</div>
        <div class="stat-value">UAE-native</div>
        <div class="stat-note">VAT and local compliance aware</div>
      </div>
      <div class="stat">
        <div class="stat-label mono">Approach</div>
        <div class="stat-value">Operation-first</div>
        <div class="stat-note">Built around how you actually work</div>
      </div>
      <div class="stat">
        <div class="stat-label mono">Support</div>
        <div class="stat-value">Hands-on</div>
        <div class="stat-note">Built into every engagement</div>
      </div>
    </div>
  </div>
</section>

<!-- ============================================
     ODOO + OPERATIONAL LAYER (combined)
     ============================================ -->
<section class="section">
  <div class="container">
    <div class="hero-grid">

      <div class="fade-in">
        <div class="section-tag mono">The Tolx Layer</div>
        <h2 class="section-title">Odoo first. The right fit, always.</h2>
        <p style="font-size:16px;color:var(--text-sec);line-height:1.7;margin-bottom:18px;"><a href="<?php echo home_url('/odoo/'); ?>" style="color:var(--text-sec);border-bottom:1px solid var(--gold);text-decoration:none;">Odoo</a> is an open-source ERP foundation — modular, proven across thousands of businesses, and a genuine alternative to SAP and Oracle without the enterprise overhead. It is our core platform and where most of our projects start.</p>
        <p style="font-size:16px;color:var(--text-sec);line-height:1.7;margin-bottom:24px;">We don't sell blank Odoo licences. We configure Odoo around how your business actually works. If, after discovery, Odoo genuinely isn't the right fit, we tell you and implement a solution that is.</p>
        <div style="display:flex;gap:14px;flex-wrap:wrap;">
          <a href="<?php echo home_url('/odoo/'); ?>" class="btn-ghost">What is Odoo? →</a>
          <a href="<?php echo home_url('/odoo-partner-dubai/'); ?>" class="btn-ghost">Odoo Partner Dubai →</a>
        </div>
      </div>

      <div class="op-grid fade-in" data-stagger="1">
        <div class="op-block">
          <div class="op-block-icon"><?php tolx_icon('open-source', 18); ?></div>
          <div>
            <h4>Open Source</h4>
            <p>You own the system and your data. No vendor lock-in.</p>
          </div>
        </div>
        <div class="op-block">
          <div class="op-block-icon"><?php tolx_icon('module', 18); ?></div>
          <div>
            <h4>Modular</h4>
            <p>Start with what you need today. Add modules as the operation grows.</p>
          </div>
        </div>
        <div class="op-block">
          <div class="op-block-icon"><?php tolx_icon('shield', 18); ?></div>
          <div>
            <h4>UAE-aware</h4>
            <p>VAT and UAE compliance, plus Arabic support — configured, not bolted on.</p>
          </div>
        </div>
        <div class="op-block">
          <div class="op-block-icon"><?php tolx_icon('scale', 18); ?></div>
          <div>
            <h4>SME-ready</h4>
            <p>Enterprise capability, configured for the size of operation that actually runs the field.</p>
          </div>
        </div>
      </div>

    </div>
  </div>
</section>

<!-- ============================================
     DEPLOYMENT ROUTE
     ============================================ -->
<section class="section">
  <div class="container">
    <div class="section-head fade-in">
      <div>
        <div class="section-tag mono">How we deploy</div>
        <h2 class="section-title">Five stops from discovery to go live.</h2>
      </div>
    </div>

    <div class="route">
      <div class="route-stop fade-in" data-stagger="1">
        <div class="route-marker">01</div>
        <h4>Discovery</h4>
        <p>30-minute call. We learn the operation — assets, workflows, pain points.</p>
      </div>
      <div class="route-stop fade-in" data-stagger="2">
        <div class="route-marker">02</div>
        <h4>Scope</h4>
        <p>We define what gets built, configured, connected, or automated before any work starts. Clear scope, no ambiguity.</p>
      </div>
      <div class="route-stop fade-in" data-stagger="3">
        <div class="route-marker">03</div>
        <h4>Build</h4>
        <p>We build, configure, connect, or automate against the agreed scope — around how your business already works.</p>
      </div>
      <div class="route-stop fade-in" data-stagger="4">
        <div class="route-marker">04</div>
        <h4>Train</h4>
        <p>Operational staff train on a system that already speaks the language of your field.</p>
      </div>
      <div class="route-stop fade-in" data-stagger="5">
        <div class="route-marker">05</div>
        <h4>Go Live</h4>
        <p>System goes live with ongoing support and improvements as the operation grows.</p>
      </div>
    </div>
  </div>
</section>

<!-- ============================================
     SCORECARD CTA — lead magnet entry point
     ============================================ -->
<section class="section sc-home-cta">
  <div class="container">
    <div class="sc-home-card fade-in">
      <div class="sc-home-grid-bg" aria-hidden="true"></div>
      <div class="sc-home-inner">
        <div class="section-tag mono">Free · 2 minutes · No account</div>
        <h2 class="sc-home-title">What is your operation costing you?</h2>
        <p class="sc-home-text">
          Most growing businesses lose money and time to scattered spreadsheets and
          manual work — without ever seeing it clearly. Answer 6 questions and get a
          personalized report on your biggest opportunities: where to make more, and
          where to work easier. Each one matched to the capability that delivers it.
        </p>
        <a href="<?php echo home_url('/operations-readiness-scorecard/'); ?>" class="sc-home-btn">
          Find Your Opportunities
          <span aria-hidden="true">&rarr;</span>
        </a>
      </div>
    </div>
  </div>
</section>

<style>
.sc-home-cta .sc-home-card {
  position: relative;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg, 16px);
  padding: 64px 56px;
  overflow: hidden;
}
.sc-home-grid-bg {
  position: absolute; inset: 0;
  background-image:
    linear-gradient(rgba(255,255,255,0.04) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255,255,255,0.04) 1px, transparent 1px);
  background-size: 48px 48px; pointer-events: none;
  mask-image: radial-gradient(ellipse 70% 80% at 80% 50%, #000 20%, transparent 100%);
  -webkit-mask-image: radial-gradient(ellipse 70% 80% at 80% 50%, #000 20%, transparent 100%);
}
.sc-home-inner { position: relative; max-width: 640px; }
.sc-home-title {
  font-family: 'Chakra Petch', sans-serif; font-weight: 700;
  color: var(--text);
  font-size: clamp(30px, 4vw, 46px); line-height: 1.08;
  letter-spacing: -1px; margin: 14px 0 18px;
}
.sc-home-text {
  font-size: 17px; line-height: 1.65; color: var(--text-sec); margin: 0 0 32px;
}
.sc-home-btn {
  display: inline-flex; align-items: center; gap: 11px;
  background: var(--gold); color: #0a0a0a;
  font-family: 'Chakra Petch', sans-serif; font-weight: 600; font-size: 16px;
  padding: 15px 30px; border-radius: var(--radius, 10px);
  text-decoration: none; transition: all 0.22s ease;
}
.sc-home-btn:hover { background: var(--gold-hover); transform: translateY(-2px); }
.sc-home-btn span { transition: transform 0.22s ease; }
.sc-home-btn:hover span { transform: translateX(4px); }
@media (max-width: 600px) {
  .sc-home-cta .sc-home-card { padding: 40px 28px; }
}
</style>

<?php get_footer(); ?>
