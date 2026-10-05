<?php
/**
 * Template Name: EV Solution
 */
get_header(); ?>

<div class="container"><?php tolx_render_breadcrumbs(); ?></div>

<!-- ============================================
     PAGE HERO — split with vertical command panel
     ============================================ -->
<section class="page-hero">
  <div class="container">
    <div class="hero-grid">

      <div class="fade-in">
        <div class="section-tag mono">Example · Revenue Asset System</div>
        <h1>One system for every stage of <em>your EV operation.</em></h1>
        <p>An example of a Tolx Revenue Asset System, applied to charging operations. From site survey to invoice: track every charger, every fault, every dirham, in a system built around how the operation actually works.</p>
        <a href="<?php echo home_url('/contact/'); ?>" class="btn-primary">Book a Demo <span>→</span></a>
      </div>

      <div class="hero-cmd" aria-hidden="true">
        <div class="cmd-panel">
          <div class="cmd-panel-head">
            <div class="cmd-panel-title">EV · Lifecycle Modules</div>
            <div class="cmd-panel-meta"><span class="cmd-panel-dot"></span> 8 modules</div>
          </div>
          <div class="cmd-row">
            <div class="cmd-row-icon"><?php tolx_icon('survey', 18); ?></div>
            <div class="cmd-row-label">Site Survey &amp; BOQ</div>
            <div class="cmd-row-tag">Pre-sales</div>
          </div>
          <div class="cmd-row">
            <div class="cmd-row-icon"><?php tolx_icon('project', 18); ?></div>
            <div class="cmd-row-label">Project Management</div>
            <div class="cmd-row-tag">Install</div>
          </div>
          <div class="cmd-row">
            <div class="cmd-row-icon"><?php tolx_icon('field-service', 18); ?></div>
            <div class="cmd-row-label">Field Service</div>
            <div class="cmd-row-tag">Operate</div>
          </div>
          <div class="cmd-row">
            <div class="cmd-row-icon"><?php tolx_icon('asset', 18); ?></div>
            <div class="cmd-row-label">Charger Register</div>
            <div class="cmd-row-tag">Lifecycle</div>
          </div>
          <div class="cmd-row">
            <div class="cmd-row-icon"><?php tolx_icon('billing', 18); ?></div>
            <div class="cmd-row-label">Contracts &amp; Billing</div>
            <div class="cmd-row-tag">Revenue</div>
          </div>
          <div class="hero-cmd-route">
            <div class="hero-cmd-route-label">Site Survey</div>
            <div class="hero-cmd-route-line"></div>
            <div class="hero-cmd-route-label">Invoice</div>
          </div>
        </div>
      </div>

    </div>
  </div>
</section>

<!-- ============================================
     WHO IT'S FOR
     ============================================ -->
<section class="section">
  <div class="container">
    <div class="section-head fade-in">
      <div>
        <div class="section-tag mono">Who it's for</div>
        <h2 class="section-title">Built for the UAE EV operator stack.</h2>
      </div>
    </div>
    <div class="diag-grid">
      <div class="diag-card fade-in" data-stagger="1">
        <div class="diag-card-tag">01 · Audience</div>
        <h3>Installers</h3>
        <p>DEWA-approved companies installing EV chargers in buildings, malls, and parking facilities.</p>
      </div>
      <div class="diag-card fade-in" data-stagger="2">
        <div class="diag-card-tag">02 · Audience</div>
        <h3>Operators</h3>
        <p>Companies operating public or semi-public charging stations and managing field maintenance.</p>
      </div>
      <div class="diag-card fade-in" data-stagger="3">
        <div class="diag-card-tag">03 · Audience</div>
        <h3>Charge Point Operators</h3>
        <p>CPOs generating per-session revenue who need to track kWh, revenue, and margin per charger.</p>
      </div>
      <div class="diag-card fade-in" data-stagger="4">
        <div class="diag-card-tag">04 · Audience</div>
        <h3>Real Estate &amp; Fleets</h3>
        <p>Developers and fleet owners deploying EV infrastructure for tenants, staff, or vehicles.</p>
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
        <h2 class="section-title">Your EV operation is growing. Your systems aren't.</h2>
        <p style="font-size:16px;color:var(--text-sec);line-height:1.7;margin-bottom:16px;">You can't track which charger assets are at which site. Maintenance requests come through WhatsApp — nothing documented. Installation projects run on spreadsheets with no milestone tracking. Invoicing is manual and always late.</p>
        <p style="font-size:16px;color:var(--text-sec);line-height:1.7;">If you're a CPO, you have no visibility into charger revenue versus energy costs. You're flying blind on your highest-value asset.</p>
      </div>
      <div class="fade-in" data-stagger="1">
        <?php
        tolx_image_slot('ev_hero', function() {
            ?>
            <div class="tolx-visual-placeholder tolx-visual-placeholder--wide">
              <div class="tolx-visual-placeholder-tag">Visual · Field Operations</div>
              <div class="tolx-visual-placeholder-label">EV charging site operations<br>(image placeholder)</div>
            </div>
            <?php
        }, [
            'alt' => 'EV charging site operations — Tolx EV Charger Operator System',
            'wrapper_class' => 'tolx-img-wrap--landscape',
        ]);
        ?>
      </div>
    </div>
  </div>
</section>

<!-- ============================================
     MODULES — full operational stack
     ============================================ -->
<section class="section">
  <div class="container">
    <div class="section-head fade-in">
      <div>
        <div class="section-tag mono">What's included</div>
        <h2 class="section-title">Eight modules. One system.</h2>
      </div>
    </div>

    <div class="op-grid op-grid--modules">
      <div class="op-block fade-in" data-stagger="1">
        <div class="op-block-icon"><?php tolx_icon('survey', 18); ?></div>
        <div>
          <h4>Site Survey &amp; BOQ</h4>
          <p>Pre-sales site assessments, Bills of Quantity, drawings, and approvals — captured in one place.</p>
        </div>
      </div>
      <div class="op-block fade-in" data-stagger="2">
        <div class="op-block-icon"><?php tolx_icon('project', 18); ?></div>
        <div>
          <h4>Project Management</h4>
          <p>Track installations from contract to handover with task assignments, milestones, and documents.</p>
        </div>
      </div>
      <div class="op-block fade-in" data-stagger="3">
        <div class="op-block-icon"><?php tolx_icon('field-service', 18); ?></div>
        <div>
          <h4>Field Service &amp; Maintenance</h4>
          <p>Schedule technician visits, manage work orders, track spare parts, log fault history per charger.</p>
        </div>
      </div>
      <div class="op-block fade-in" data-stagger="4">
        <div class="op-block-icon"><?php tolx_icon('asset', 18); ?></div>
        <div>
          <h4>Charger Asset Register</h4>
          <p>Full asset lifecycle — warranty tracking, maintenance history, location, and DEWA approval status.</p>
        </div>
      </div>
      <div class="op-block fade-in" data-stagger="5">
        <div class="op-block-icon"><?php tolx_icon('inventory', 18); ?></div>
        <div>
          <h4>Inventory &amp; Spare Parts</h4>
          <p>Stock management for cables, connectors, controllers — reorder alerts and supplier management.</p>
        </div>
      </div>
      <div class="op-block fade-in" data-stagger="6">
        <div class="op-block-icon"><?php tolx_icon('contract', 18); ?></div>
        <div>
          <h4>Client Contracts &amp; Billing</h4>
          <p>AMC contracts, recurring invoicing, SLA tracking, and a client portal for service requests.</p>
        </div>
      </div>
      <div class="op-block fade-in" data-stagger="1">
        <div class="op-block-icon"><?php tolx_icon('revenue', 18); ?></div>
        <div>
          <h4>CPO Revenue <span class="chip" style="margin-left:6px;">Add-on</span></h4>
          <p>Track kWh delivered, session revenue, energy cost, and gross margin per charger.</p>
        </div>
      </div>
      <div class="op-block fade-in" data-stagger="2">
        <div class="op-block-icon"><?php tolx_icon('dashboard', 18); ?></div>
        <div>
          <h4>Management Dashboard</h4>
          <p>Live KPIs — chargers deployed, open faults, revenue MTD, top-performing sites, pending invoices.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- ============================================
     IMPLEMENTATION TIMELINE
     ============================================ -->
<section class="section">
  <div class="container">
    <div class="section-head fade-in">
      <div>
        <div class="section-tag mono">Implementation</div>
        <h2 class="section-title">Go live in 4–8 weeks.</h2>
      </div>
    </div>

    <div class="route route--phases">
      <div class="route-stop fade-in" data-stagger="1">
        <div class="route-marker">W1–2</div>
        <h4>Setup &amp; Discovery</h4>
        <p>Requirements mapping, system setup, data migration planning.</p>
      </div>
      <div class="route-stop fade-in" data-stagger="2">
        <div class="route-marker">W3–4</div>
        <h4>Configuration</h4>
        <p>Vertical modules configured, workflows built, integrations connected.</p>
      </div>
      <div class="route-stop fade-in" data-stagger="3">
        <div class="route-marker">W5–6</div>
        <h4>Training</h4>
        <p>Your team trained on every module. Onsite or remote. Field staff included.</p>
      </div>
      <div class="route-stop fade-in" data-stagger="4">
        <div class="route-marker">W7–8</div>
        <h4>Go Live</h4>
        <p>System live. Support period active. Ongoing enhancements via AMC.</p>
      </div>
    </div>
  </div>
</section>

<?php get_footer(); ?>
