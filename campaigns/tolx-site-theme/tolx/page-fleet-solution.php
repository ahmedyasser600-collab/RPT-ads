<?php
/**
 * Template Name: Fleet Solution
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
        <div class="section-tag mono">Example · Revenue Asset System</div>
        <h1>Every vehicle. Every cost. <em>One system.</em></h1>
        <p>An example of a Tolx Revenue Asset System, applied to vehicle-based operations. Asset register, maintenance, fuel, drivers, compliance, and total cost of ownership, for fleets running 10 to 500 vehicles in the UAE.</p>
        <a href="<?php echo home_url('/contact/'); ?>" class="btn-primary">Book a Demo <span>→</span></a>
      </div>

      <div class="hero-cmd" aria-hidden="true">
        <div class="cmd-panel">
          <div class="cmd-panel-head">
            <div class="cmd-panel-title">Fleet · Vehicle Lifecycle</div>
            <div class="cmd-panel-meta"><span class="cmd-panel-dot"></span> 7 modules</div>
          </div>
          <div class="cmd-row">
            <div class="cmd-row-icon"><?php tolx_icon('asset', 18); ?></div>
            <div class="cmd-row-label">Vehicle Register</div>
            <div class="cmd-row-tag">Lifecycle</div>
          </div>
          <div class="cmd-row">
            <div class="cmd-row-icon"><?php tolx_icon('maintenance', 18); ?></div>
            <div class="cmd-row-label">Maintenance</div>
            <div class="cmd-row-tag">Schedule</div>
          </div>
          <div class="cmd-row">
            <div class="cmd-row-icon"><?php tolx_icon('driver', 18); ?></div>
            <div class="cmd-row-label">Drivers</div>
            <div class="cmd-row-tag">Compliance</div>
          </div>
          <div class="cmd-row">
            <div class="cmd-row-icon"><?php tolx_icon('fuel', 18); ?></div>
            <div class="cmd-row-label">Fuel</div>
            <div class="cmd-row-tag">Cost / km</div>
          </div>
          <div class="cmd-row">
            <div class="cmd-row-icon"><?php tolx_icon('shield', 18); ?></div>
            <div class="cmd-row-label">Mulkiya &amp; Insurance</div>
            <div class="cmd-row-tag">Renewals</div>
          </div>
          <div class="hero-cmd-route">
            <div class="hero-cmd-route-label">Acquire</div>
            <div class="hero-cmd-route-line"></div>
            <div class="hero-cmd-route-label">Dispose</div>
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
        <h2 class="section-title">Built for vehicle-based operations.</h2>
      </div>
    </div>
    <div class="diag-grid">
      <div class="diag-card fade-in" data-stagger="1">
        <div class="diag-card-tag">01 · Audience</div>
        <h3>Logistics Companies</h3>
        <p>Last-mile delivery and freight operators running 10 to 500 vehicles across the UAE.</p>
      </div>
      <div class="diag-card fade-in" data-stagger="2">
        <div class="diag-card-tag">02 · Audience</div>
        <h3>Construction Fleets</h3>
        <p>Contracting companies managing heavy equipment and service vehicles across multiple sites.</p>
      </div>
      <div class="diag-card fade-in" data-stagger="3">
        <div class="diag-card-tag">03 · Audience</div>
        <h3>Service Companies</h3>
        <p>Field technician fleets where vehicles, drivers, and parts move together every day.</p>
      </div>
      <div class="diag-card fade-in" data-stagger="4">
        <div class="diag-card-tag">04 · Audience</div>
        <h3>Government Pools</h3>
        <p>Government and semi-government entities managing shared vehicle pools and compliance.</p>
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
        <h2 class="section-title">Your fleet is running. Your cost picture isn't.</h2>
        <p style="font-size:16px;color:var(--text-sec);line-height:1.7;margin-bottom:16px;">Mulkiya renewals get missed. Maintenance schedules sit in someone's head. Fuel spend goes uncontested. Driver compliance is reactive. The real cost per vehicle — depreciation, maintenance, fuel, downtime — never gets calculated.</p>
        <p style="font-size:16px;color:var(--text-sec);line-height:1.7;">When a vehicle goes off-road, you find out from the driver. When a licence expires, you find out from the police.</p>
      </div>
      <div class="fade-in" data-stagger="1">
        <?php
        tolx_image_slot('fleet_hero', function() {
            ?>
            <div class="tolx-visual-placeholder tolx-visual-placeholder--wide">
              <div class="tolx-visual-placeholder-tag">Visual · Fleet Depot</div>
              <div class="tolx-visual-placeholder-label">Vehicle depot operations<br>(image placeholder)</div>
            </div>
            <?php
        }, [
            'alt' => 'Fleet depot operations — Tolx Fleet Management System',
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
        <h2 class="section-title">Seven modules. Per vehicle.</h2>
      </div>
    </div>

    <div class="op-grid op-grid--modules">
      <div class="op-block fade-in" data-stagger="1">
        <div class="op-block-icon"><?php tolx_icon('asset', 18); ?></div>
        <div>
          <h4>Vehicle Asset Register</h4>
          <p>Full profile per vehicle — registration, insurance, Mulkiya, service history, depreciation tracking.</p>
        </div>
      </div>
      <div class="op-block fade-in" data-stagger="2">
        <div class="op-block-icon"><?php tolx_icon('maintenance', 18); ?></div>
        <div>
          <h4>Maintenance &amp; Service</h4>
          <p>Preventive schedules by mileage or date, work orders, garage management, parts consumption.</p>
        </div>
      </div>
      <div class="op-block fade-in" data-stagger="3">
        <div class="op-block-icon"><?php tolx_icon('driver', 18); ?></div>
        <div>
          <h4>Driver Management</h4>
          <p>Driver profiles, licence expiry alerts, trip assignments, and performance tracking.</p>
        </div>
      </div>
      <div class="op-block fade-in" data-stagger="4">
        <div class="op-block-icon"><?php tolx_icon('fuel', 18); ?></div>
        <div>
          <h4>Fuel Tracking</h4>
          <p>Fuel card integration or manual logging, cost-per-km analysis, and anomaly detection.</p>
        </div>
      </div>
      <div class="op-block fade-in" data-stagger="5">
        <div class="op-block-icon"><?php tolx_icon('route', 18); ?></div>
        <div>
          <h4>Trip &amp; Route Management</h4>
          <p>Trip planning, driver assignment, mileage logging, and client delivery confirmation.</p>
        </div>
      </div>
      <div class="op-block fade-in" data-stagger="6">
        <div class="op-block-icon"><?php tolx_icon('shield', 18); ?></div>
        <div>
          <h4>Compliance &amp; Documents</h4>
          <p>Automated alerts for expiring licences, insurance, registration, and Mulkiya renewals.</p>
        </div>
      </div>
      <div class="op-block fade-in" data-stagger="1">
        <div class="op-block-icon"><?php tolx_icon('dashboard', 18); ?></div>
        <div>
          <h4>Cost Reporting</h4>
          <p>Total cost of ownership per vehicle, cost per km, and maintenance versus depreciation analysis.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<?php get_footer(); ?>
