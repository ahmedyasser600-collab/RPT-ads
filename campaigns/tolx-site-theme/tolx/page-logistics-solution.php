<?php
/**
 * Template Name: Logistics Solution
 */
get_header(); ?>

<div class="container"><?php tolx_render_breadcrumbs(); ?></div>

<!-- ============================================
     PAGE HERO
     ============================================ -->
<section class="page-hero">
  <div class="container">
    <div class="hero-grid">

      <div class="fade-in">
        <div class="section-tag mono">Example · Workflow System</div>
        <h1>From order to <em>proof of delivery</em> — in one system.</h1>
        <p>An example of a Tolx workflow system, applied to delivery and distribution. Order intake, route planning, proof of delivery, returns, and COD reconciliation, with a real-time client portal.</p>
        <a href="<?php echo home_url('/contact/'); ?>" class="btn-primary">Book a Demo <span>→</span></a>
      </div>

      <div class="hero-cmd" aria-hidden="true">
        <div class="cmd-panel">
          <div class="cmd-panel-head">
            <div class="cmd-panel-title">Logistics · Order Flow</div>
            <div class="cmd-panel-meta"><span class="cmd-panel-dot"></span> 6 modules</div>
          </div>
          <div class="cmd-row">
            <div class="cmd-row-icon"><?php tolx_icon('order', 18); ?></div>
            <div class="cmd-row-label">Order Intake</div>
            <div class="cmd-row-tag">Multi-channel</div>
          </div>
          <div class="cmd-row">
            <div class="cmd-row-icon"><?php tolx_icon('route', 18); ?></div>
            <div class="cmd-row-label">Route Planning</div>
            <div class="cmd-row-tag">Optimised</div>
          </div>
          <div class="cmd-row">
            <div class="cmd-row-icon"><?php tolx_icon('check', 18); ?></div>
            <div class="cmd-row-label">Proof of Delivery</div>
            <div class="cmd-row-tag">Mobile</div>
          </div>
          <div class="cmd-row">
            <div class="cmd-row-icon"><?php tolx_icon('cash', 18); ?></div>
            <div class="cmd-row-label">COD Reconciliation</div>
            <div class="cmd-row-tag">Per route</div>
          </div>
          <div class="cmd-row">
            <div class="cmd-row-icon"><?php tolx_icon('portal', 18); ?></div>
            <div class="cmd-row-label">Client Portal</div>
            <div class="cmd-row-tag">Live</div>
          </div>
          <div class="hero-cmd-route">
            <div class="hero-cmd-route-label">Order</div>
            <div class="hero-cmd-route-line"></div>
            <div class="hero-cmd-route-label">Delivered</div>
          </div>
        </div>
      </div>

    </div>
  </div>
</section>

<!-- ============================================
     THE PROBLEM
     ============================================ -->
<section class="section">
  <div class="container">
    <div class="hero-grid">
      <div class="fade-in">
        <div class="section-tag mono">The problem</div>
        <h2 class="section-title">Last-mile is where margin lives or dies.</h2>
        <p style="font-size:16px;color:var(--text-sec);line-height:1.7;margin-bottom:16px;">Orders arrive across channels — phone, WhatsApp, email, e-commerce — and someone retypes them into a spreadsheet. Routes are planned by intuition. Failed deliveries vanish into the void. COD cash gets reconciled days later, if at all.</p>
        <p style="font-size:16px;color:var(--text-sec);line-height:1.7;">Clients want a tracking link. You want a margin number. Neither exists.</p>
      </div>
      <div class="fade-in" data-stagger="1">
        <?php
        tolx_image_slot('logistics_hero', function() {
            ?>
            <div class="tolx-visual-placeholder tolx-visual-placeholder--wide">
              <div class="tolx-visual-placeholder-tag">Visual · Last-Mile Operations</div>
              <div class="tolx-visual-placeholder-label">Dispatch &amp; route operations<br>(image placeholder)</div>
            </div>
            <?php
        }, [
            'alt' => 'Last-mile dispatch and route operations — Tolx Logistics System',
            'wrapper_class' => 'tolx-img-wrap--landscape',
        ]);
        ?>
      </div>
    </div>
  </div>
</section>

<!-- ============================================
     MODULES
     ============================================ -->
<section class="section">
  <div class="container">
    <div class="section-head fade-in">
      <div>
        <div class="section-tag mono">What's included</div>
        <h2 class="section-title">Six modules added on top of fleet.</h2>
      </div>
    </div>

    <div class="op-grid op-grid--modules">
      <div class="op-block fade-in" data-stagger="1">
        <div class="op-block-icon"><?php tolx_icon('order', 18); ?></div>
        <div>
          <h3>Customer Order Management</h3>
          <p>Inbound orders from multiple channels, auto-assignment to delivery routes.</p>
        </div>
      </div>
      <div class="op-block fade-in" data-stagger="2">
        <div class="op-block-icon"><?php tolx_icon('route', 18); ?></div>
        <div>
          <h3>Route Optimisation</h3>
          <p>Planned route management, stop sequencing, estimated arrival times.</p>
        </div>
      </div>
      <div class="op-block fade-in" data-stagger="3">
        <div class="op-block-icon"><?php tolx_icon('check', 18); ?></div>
        <div>
          <h3>Proof of Delivery</h3>
          <p>Digital signature capture, photo upload, delivery confirmation — fully mobile.</p>
        </div>
      </div>
      <div class="op-block fade-in" data-stagger="4">
        <div class="op-block-icon"><?php tolx_icon('return', 18); ?></div>
        <div>
          <h3>Returns &amp; Failed Deliveries</h3>
          <p>Return workflows, re-delivery scheduling, automated client notifications.</p>
        </div>
      </div>
      <div class="op-block fade-in" data-stagger="5">
        <div class="op-block-icon"><?php tolx_icon('portal', 18); ?></div>
        <div>
          <h3>Client Portal &amp; Tracking</h3>
          <p>Clients log in and track their shipment status in real time.</p>
        </div>
      </div>
      <div class="op-block fade-in" data-stagger="6">
        <div class="op-block-icon"><?php tolx_icon('cash', 18); ?></div>
        <div>
          <h3>Billing &amp; COD Management</h3>
          <p>Cash-on-delivery reconciliation, automated invoicing per delivery batch.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<?php get_footer(); ?>
