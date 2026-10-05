<?php
/**
 * Template Name: CPO Solution
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
        <div class="section-tag mono">Example · Revenue Visibility Layer</div>
        <h1>Margin clarity, <em>per charger.</em></h1>
        <p>An example of a Tolx revenue-visibility layer, applied to charging operations. kWh delivered, session revenue, energy cost, and gross margin, tracked at the charger level, not the network level.</p>
        <a href="<?php echo home_url('/contact/'); ?>" class="btn-primary">Add to your EV system <span>→</span></a>
      </div>

      <div class="hero-cmd" aria-hidden="true">
        <div class="cmd-panel">
          <div class="cmd-panel-head">
            <div class="cmd-panel-title">CPO · Revenue Layer</div>
            <div class="cmd-panel-meta"><span class="cmd-panel-dot"></span> Per charger</div>
          </div>
          <div class="cmd-row">
            <div class="cmd-row-icon"><?php tolx_icon('kwh', 18); ?></div>
            <div class="cmd-row-label">kWh Delivered</div>
            <div class="cmd-row-tag">Throughput</div>
          </div>
          <div class="cmd-row">
            <div class="cmd-row-icon"><?php tolx_icon('session', 18); ?></div>
            <div class="cmd-row-label">Session Revenue</div>
            <div class="cmd-row-tag">Per session</div>
          </div>
          <div class="cmd-row">
            <div class="cmd-row-icon"><?php tolx_icon('lightning', 18); ?></div>
            <div class="cmd-row-label">Energy Cost</div>
            <div class="cmd-row-tag">DEWA tariff</div>
          </div>
          <div class="cmd-row">
            <div class="cmd-row-icon"><?php tolx_icon('revenue', 18); ?></div>
            <div class="cmd-row-label">Gross Margin</div>
            <div class="cmd-row-tag">Per charger</div>
          </div>
          <div class="hero-cmd-route">
            <div class="hero-cmd-route-label">Session start</div>
            <div class="hero-cmd-route-line"></div>
            <div class="hero-cmd-route-label">Margin booked</div>
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
    <div class="hero-grid">
      <div class="fade-in">
        <div class="section-tag mono">Who needs it</div>
        <h2 class="section-title">For operators who get paid per session.</h2>
        <p style="font-size:16px;color:var(--text-sec);line-height:1.7;margin-bottom:16px;">If you generate revenue from charger sessions — public charging, semi-public stations, fleet-as-a-service — you need to know which chargers earn and which chargers cost.</p>
        <p style="font-size:16px;color:var(--text-sec);line-height:1.7;">Without per-charger margin, you can't make decisions about siting, pricing, or expansion. The CPO Revenue Module sits on top of the EV Charger Operator System and pulls session data into a clear margin view.</p>
      </div>
      <div class="fade-in" data-stagger="1">
        <?php
        tolx_image_slot('cpo_hero', function() {
            ?>
            <div class="tolx-visual-placeholder tolx-visual-placeholder--wide">
              <div class="tolx-visual-placeholder-tag">Visual · Revenue Layer</div>
              <div class="tolx-visual-placeholder-label">Charger-level margin view<br>(image placeholder)</div>
            </div>
            <?php
        }, [
            'alt' => 'Per-charger margin view — Tolx CPO Revenue Module',
            'wrapper_class' => 'tolx-img-wrap--landscape',
        ]);
        ?>
      </div>
    </div>
  </div>
</section>

<!-- ============================================
     WHAT IT TRACKS
     ============================================ -->
<section class="section">
  <div class="container">
    <div class="section-head fade-in">
      <div>
        <div class="section-tag mono">What it tracks</div>
        <h2 class="section-title">Four signals. Per charger. Per period.</h2>
      </div>
    </div>

    <div class="op-grid op-grid--modules">
      <div class="op-block fade-in" data-stagger="1">
        <div class="op-block-icon"><?php tolx_icon('kwh', 18); ?></div>
        <div>
          <h3>kWh Delivered</h3>
          <p>Energy throughput per charger, per session, per period — reconciled against the meter.</p>
        </div>
      </div>
      <div class="op-block fade-in" data-stagger="2">
        <div class="op-block-icon"><?php tolx_icon('session', 18); ?></div>
        <div>
          <h3>Session Revenue</h3>
          <p>Revenue collected per session and rolled up by charger, site, and operator.</p>
        </div>
      </div>
      <div class="op-block fade-in" data-stagger="3">
        <div class="op-block-icon"><?php tolx_icon('lightning', 18); ?></div>
        <div>
          <h3>Energy Cost</h3>
          <p>Energy cost per kWh — DEWA tariff aware. Variable rates and time-of-use supported.</p>
        </div>
      </div>
      <div class="op-block fade-in" data-stagger="4">
        <div class="op-block-icon"><?php tolx_icon('revenue', 18); ?></div>
        <div>
          <h3>Gross Margin per Charger</h3>
          <p>Session revenue minus energy cost, normalised to a per-charger view for siting decisions.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<?php get_footer(); ?>
