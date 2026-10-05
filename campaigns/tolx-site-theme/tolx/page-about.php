<?php
/**
 * Template Name: About
 */
get_header(); ?>

<div class="container"><?php tolx_render_breadcrumbs(); ?></div>

<section class="page-hero">
  <div class="container">
    <div class="fade-in">
      <div class="section-tag mono">About Tolx</div>
      <h1>Built in the UAE. <em>Built around how you run.</em></h1>
      <p>A UAE software house and business systems partner. We build systems around the assets, workflows, data, and digital channels that generate revenue. Odoo-first implementation, plus software, automation, CRM, dashboards and web.</p>
    </div>
  </div>
</section>

<!-- ============================================
     WHY WE EXIST — operation-first philosophy
     ============================================ -->
<section class="section">
  <div class="container">
    <div class="hero-grid">

      <div class="fade-in">
        <div class="section-tag mono">Why we exist</div>
        <h2 class="section-title">Most software starts with the software.</h2>
        <p style="font-size:16px;color:var(--text-sec);line-height:1.7;margin-bottom:16px;">Most software houses and partners in the UAE lead with the tool. They sell the same blank system to a clinic, a trading company, and a service business, then ask each one to change how they work to fit it.</p>
        <p style="font-size:16px;color:var(--text-sec);line-height:1.7;margin-bottom:16px;">The result is long timelines, unclear cost, and systems that never quite fit how the business actually operates, so people drift back to spreadsheets.</p>
        <p style="font-size:16px;color:var(--text-sec);line-height:1.7;">Tolx starts the other way round. We map how revenue moves through your business — the assets, workflows, and data it depends on — then build the system around it. Usually on Odoo, and on another platform when Odoo isn't the right fit.</p>
      </div>

      <div class="fade-in" data-stagger="1">
        <div class="section-tag mono">Why UAE</div>
        <h2 class="section-title">The right market, the right time.</h2>
        <div class="op-grid" style="grid-template-columns:1fr;margin-top:8px;">
          <div class="op-block">
            <div class="op-block-icon"><?php tolx_icon('shield', 18); ?></div>
            <div>
              <h4>Compliance Is Tightening</h4>
              <p>VAT, corporate tax, and the 2026 e-invoicing mandate push every UAE business toward connected, auditable systems.</p>
            </div>
          </div>
          <div class="op-block">
            <div class="op-block-icon"><?php tolx_icon('growth', 18); ?></div>
            <div>
              <h4>SMEs Are Digitising</h4>
              <p>UAE SMEs are moving off spreadsheets and disconnected tools, but most are under-served by generic partners.</p>
            </div>
          </div>
          <div class="op-block">
            <div class="op-block-icon"><?php tolx_icon('module', 18); ?></div>
            <div>
              <h4>Tools Have Multiplied</h4>
              <p>Businesses run on five apps that don't talk to each other. The need now is connection, not more software.</p>
            </div>
          </div>
          <div class="op-block">
            <div class="op-block-icon"><?php tolx_icon('scale', 18); ?></div>
            <div>
              <h4>Local Knowledge Matters</h4>
              <p>UAE compliance and the way local businesses actually operate favour a partner on the ground, not offshore.</p>
            </div>
          </div>
        </div>
      </div>

    </div>
  </div>
</section>

<!-- ============================================
     VALUES
     ============================================ -->
<section class="section">
  <div class="container">
    <div class="section-head fade-in">
      <div>
        <div class="section-tag mono">What we stand for</div>
        <h2 class="section-title">Four principles, applied to every engagement.</h2>
      </div>
    </div>
    <div class="diag-grid">
      <div class="diag-card fade-in" data-stagger="1">
        <div class="diag-card-tag">01 · Principle</div>
        <h3>Operation before software</h3>
        <p>We map how the business works before recommending any tool. The operation leads; the software follows.</p>
      </div>
      <div class="diag-card fade-in" data-stagger="2">
        <div class="diag-card-tag">02 · Principle</div>
        <h3>Scope before build</h3>
        <p>We define what needs to be built, configured, connected, or automated before implementation starts. Clear scope, no guesswork.</p>
      </div>
      <div class="diag-card fade-in" data-stagger="3">
        <div class="diag-card-tag">03 · Principle</div>
        <h3>Systems around revenue</h3>
        <p>We focus on the workflows, assets, channels, and data that directly support revenue, not features for their own sake.</p>
      </div>
      <div class="diag-card fade-in" data-stagger="4">
        <div class="diag-card-tag">04 · Principle</div>
        <h3>Adoption is the metric</h3>
        <p>A system that doesn't get used is a system that failed. We measure by adoption, not deployment.</p>
      </div>
    </div>
  </div>
</section>

<?php
// Optional founder section — renders only if Customizer image is set
$founder_img = get_theme_mod('tolx_img_about_founder', '');
if (!empty($founder_img)):
?>
<section class="section">
  <div class="container">
    <div class="hero-grid">
      <div class="fade-in" data-stagger="1">
        <?php
        tolx_image_slot('about_founder', null, [
            'alt'           => 'Founder of Tolx',
            'wrapper_class' => 'tolx-img-wrap--portrait',
        ]);
        ?>
      </div>
      <div class="fade-in">
        <div class="section-tag mono">The founder</div>
        <h2 class="section-title">Why Tolx exists.</h2>
        <p style="font-size:16px;color:var(--text-sec);line-height:1.7;margin-bottom:16px;">Tolx was founded out of a simple observation: most software projects in the UAE fail not because the tool is wrong, but because nobody mapped the operation first. The business is asked to bend around the software, instead of the software being built around the business.</p>
        <p style="font-size:16px;color:var(--text-sec);line-height:1.7;">Tolx is the alternative — a UAE software house that starts with how revenue actually moves through your business, then builds the system around it. The result: a better fit, lower risk, and a system people actually use.</p>
      </div>
    </div>
  </div>
</section>
<?php endif; ?>

<?php
// Optional team / office wide image — renders only if uploaded
$team_img = get_theme_mod('tolx_img_about_team', '');
if (!empty($team_img)):
?>
<section class="section-sm">
  <div class="container">
    <div class="fade-in">
      <?php
      tolx_image_slot('about_team', null, [
          'alt'           => 'The Tolx team in Dubai',
          'wrapper_class' => 'tolx-img-wrap--wide',
      ]);
      ?>
    </div>
  </div>
</section>
<?php endif; ?>

<!-- ============================================
     ODOO PARTNER TEASER
     ============================================ -->
<section class="section-sm">
  <div class="container">
    <div class="cmd-panel fade-in" style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:24px;padding:40px;">
      <div>
        <div class="section-tag mono" style="margin-bottom:8px;">Odoo Partner</div>
        <h3 style="font-size:22px;font-weight:600;letter-spacing:-0.3px;">An Odoo partner, and a software house.</h3>
        <p style="font-size:14px;color:var(--text-sec);margin-top:6px;">Odoo is our most established foundation, and one of several. Learn what working with an Odoo partner means for your project.</p>
      </div>
      <a href="<?php echo home_url('/about/odoo-partnership/'); ?>" class="btn-ghost">Read more →</a>
    </div>
  </div>
</section>

<?php get_footer(); ?>
