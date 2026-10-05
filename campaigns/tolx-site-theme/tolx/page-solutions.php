<?php
/**
 * Template Name: Solutions Hub
 */
get_header(); ?>

<div class="container"><?php tolx_render_breadcrumbs(); ?></div>

<section class="page-hero">
  <div class="container">
    <div class="fade-in">
      <div class="section-tag mono">Our Systems</div>
      <h1>Software to organise orders, stock, customers and <em>team tasks.</em></h1>
      <p>For kiosks, shops, trading companies and service teams across the UAE, we help reduce missed orders, conflicting stock records, repeated entry and chasing staff for updates. We choose suitable tools, implement the agreed workflow and support adoption. We use <a href="<?php echo home_url('/odoo/'); ?>" style="color:inherit;border-bottom:1px solid var(--gold);text-decoration:none;">Odoo</a> when it is the right foundation, and build or connect what fits when it isn't.</p>
    </div>
  </div>
</section>

<?php
// Optional Solutions hub hero band — renders only if Customizer image is set
$hub_img = get_theme_mod('tolx_img_solutions_hub_hero', '');
if (!empty($hub_img)):
?>
<section class="section-sm">
  <div class="container">
    <div class="fade-in">
      <?php
      tolx_image_slot('solutions_hub_hero', null, [
          'alt'           => 'Tolx business systems across UAE operations',
          'wrapper_class' => 'tolx-img-wrap--wide',
      ]);
      ?>
    </div>
  </div>
</section>
<?php endif; ?>

<!-- ============================================
     SOLUTIONS MATRIX (same component as homepage)
     ============================================ -->
<section class="section-sm">
  <div class="container">
    <div class="sol-matrix">

      <a href="<?php echo esc_url(tolx_published_destination('stock-sales-management', '/contact/')); ?>" class="sol-card is-primary fade-in" data-stagger="1">
        <div class="sol-card-head">
          <div class="sol-card-icon"><?php tolx_icon('asset', 22); ?></div>
          <div class="sol-card-tag">Core System</div>
        </div>
        <h3>Stock &amp; Sales Systems</h3>
        <p>For businesses that need visibility and control over the assets, capacity, locations, contracts, or teams that create revenue.</p>
        <div class="sol-card-foot">
          <div class="chip-row">
            <span class="chip">Assets</span>
            <span class="chip">Capacity</span>
            <span class="chip">Locations</span>
            <span class="chip">Contracts</span>
            <span class="chip">Teams</span>
          </div>
          <span class="sol-card-link">Start with a conversation</span>
        </div>
      </a>

      <a href="<?php echo esc_url(tolx_published_destination('team-tasks-approvals', '/contact/')); ?>" class="sol-card fade-in" data-stagger="2">
        <div class="sol-card-head">
          <div class="sol-card-icon"><?php tolx_icon('project', 22); ?></div>
        </div>
        <h3>Workflow &amp; Automation Systems</h3>
        <p>For businesses losing time to spreadsheets, approvals, repeated admin, and disconnected tools.</p>
        <div class="sol-card-foot">
          <div class="chip-row">
            <span class="chip">Approvals</span>
            <span class="chip">Automation</span>
            <span class="chip">Integrations</span>
          </div>
          <span class="sol-card-link">Explore</span>
        </div>
      </a>

      <a href="<?php echo esc_url(tolx_published_destination('order-tracking-customer-follow-up', '/contact/')); ?>" class="sol-card fade-in" data-stagger="3">
        <div class="sol-card-head">
          <div class="sol-card-icon"><?php tolx_icon('revenue', 22); ?></div>
        </div>
        <h3>CRM &amp; Commercial Operations</h3>
        <p>For businesses that need clearer pipelines, lead tracking, follow-ups, quotes, and client records.</p>
        <div class="sol-card-foot">
          <div class="chip-row">
            <span class="chip">Pipeline</span>
            <span class="chip">Leads</span>
            <span class="chip">Quotes</span>
          </div>
          <span class="sol-card-link">Explore</span>
        </div>
      </a>

      <a href="<?php echo esc_url(home_url('/contact/')); ?>" class="sol-card fade-in" data-stagger="4">
        <div class="sol-card-head">
          <div class="sol-card-icon"><?php tolx_icon('dashboard', 22); ?></div>
        </div>
        <h3>Dashboards &amp; Decision Systems</h3>
        <p>For managers who need real-time visibility over performance, revenue, operations, and bottlenecks.</p>
        <div class="sol-card-foot">
          <div class="chip-row">
            <span class="chip">KPIs</span>
            <span class="chip">Reporting</span>
            <span class="chip">Visibility</span>
          </div>
          <span class="sol-card-link">Explore</span>
        </div>
      </a>

      <a href="<?php echo home_url('/odoo/'); ?>" class="sol-card fade-in" data-stagger="5">
        <div class="sol-card-head">
          <div class="sol-card-icon"><?php tolx_icon('module', 22); ?></div>
        </div>
        <h3>Odoo Configuration</h3>
        <p>When Odoo is the right foundation, Tolx configures it around your workflows. Our most established platform, and one of several.</p>
        <div class="sol-card-foot">
          <div class="chip-row">
            <span class="chip">ERP</span>
            <span class="chip">Inventory</span>
            <span class="chip">Accounting</span>
          </div>
          <span class="sol-card-link">Explore Odoo</span>
        </div>
      </a>

      <a href="<?php echo home_url('/growth-systems/'); ?>" class="sol-card fade-in" data-stagger="6">
        <div class="sol-card-head">
          <div class="sol-card-icon"><?php tolx_icon('route', 22); ?></div>
          <div class="sol-card-tag">Growth Systems</div>
        </div>
        <h3>Growth Systems</h3>
        <p>Websites, landing pages, SEO, analytics, paid campaigns, content systems, and marketing infrastructure.</p>
        <div class="sol-card-foot">
          <div class="chip-row">
            <span class="chip">Web</span>
            <span class="chip">Marketing</span>
            <span class="chip">SEO</span>
            <span class="chip">Analytics</span>
          </div>
          <span class="sol-card-link">Explore Growth Systems</span>
        </div>
      </a>

    </div>
  </div>
</section>

<!-- ============================================
     COMPARISON — generic partner vs. Tolx
     ============================================ -->
<section class="section">
  <div class="container">
    <div class="section-head fade-in">
      <div>
        <div class="section-tag mono">Why it's different</div>
        <h2 class="section-title">Generic software vs. Tolx.</h2>
      </div>
    </div>

    <div class="compare-grid fade-in">
      <div class="compare-col compare-col--neg">
        <div class="compare-col-head">
          <span class="compare-col-tag">Generic Approach</span>
        </div>
        <ul class="compare-list">
          <li>Software chosen first, operation second</li>
          <li>You change how you work to fit the tool</li>
          <li>Disconnected tools that don't reconcile</li>
          <li>Consultant learns your business during the project</li>
          <li>A system people quietly stop using</li>
          <li>Support that doesn't understand the operation</li>
        </ul>
      </div>
      <div class="compare-col compare-col--pos">
        <div class="compare-col-head">
          <span class="compare-col-tag">Tolx Approach</span>
        </div>
        <ul class="compare-list">
          <li>We map how revenue moves before recommending anything</li>
          <li>The system is built around how you already work</li>
          <li>One connected source of truth, not five</li>
          <li>Clear scope defined before any build starts</li>
          <li>Adoption is the metric — a system people use</li>
          <li>Hands-on support that knows the operation</li>
        </ul>
      </div>
    </div>
  </div>
</section>

<!-- ============================================
     BEYOND OUR CORE
     ============================================ -->
<section class="section-sm">
  <div class="container">
    <div class="cmd-panel beyond-panel fade-in">
      <div class="beyond-panel-grid">
        <div>
          <div class="cmd-panel-title" style="margin-bottom:14px;">Examples of where this applies</div>
          <h2 style="font-size:clamp(22px,2.6vw,28px);font-weight:700;letter-spacing:-0.5px;line-height:1.25;margin-bottom:14px;">The pattern transfers across industries.</h2>
          <p style="font-size:15.5px;color:var(--text-sec);line-height:1.7;margin-bottom:20px;">Wherever a business depends on assets, workflows, and data to generate revenue, the same approach applies: map how revenue moves, then build the system around it. The industry is the example, not the identity.</p>
          <a href="<?php echo esc_url(home_url('/contact/')); ?>" class="btn-ghost">Talk to us about your operation →</a>
        </div>
        <div class="beyond-panel-tags">
          <span class="chip">Mobility</span>
          <span class="chip">Service Operations</span>
          <span class="chip">Logistics</span>
          <span class="chip">Equipment</span>
          <span class="chip">Facilities</span>
          <span class="chip">Trading</span>
          <span class="chip">Hospitality</span>
          <span class="chip">Clinics</span>
        </div>
      </div>
    </div>
  </div>
</section>

<?php get_footer(); ?>
