<?php
/**
 * Template Name: Software House Dubai
 * URL: /software-house-dubai/
 *
 * Head-term landing page targeting `software house dubai`,
 * `software solutions dubai`, `software company dubai`,
 * `operational software dubai`. Honest framing — Odoo-led,
 * with genuine custom configuration, not a full custom-dev shop.
 */

tolx_register_faq([
    [
        'What does Tolx do as a software house in Dubai?',
        'Tolx is a Dubai software house that builds operational systems for businesses. The core of the work is Odoo implementation — configuring the Odoo ERP platform around how a specific operation runs. This includes vertical configuration, custom module work where the standard platform needs extending, data migration, and ongoing support. Tolx focuses on operational software: systems that run a business day to day, rather than consumer apps or marketing websites.'
    ],
    [
        'Is Tolx a custom software development company?',
        'Partly. Tolx builds primarily on Odoo — an open-source platform that is highly configurable — and extends it with custom module development where an operation needs something the standard platform does not cover. This is different from a pure custom-software house that builds every system from scratch. The Tolx approach is faster and lower-risk for operational software: most of what a business needs already exists in Odoo and is configured, with custom work reserved for the genuinely unique parts.'
    ],
    [
        'What kind of software solutions does Tolx build?',
        'Operational systems — software that runs the daily operations of businesses. That includes asset registers, field service and maintenance management, project and contract management, fleet and logistics operations, billing and recurring invoicing, and management dashboards. Tolx goes deepest in EV charging, fleet, and logistics, and also serves adjacent verticals like facility management, contracting, and equipment rental.'
    ],
    [
        'Why choose a specialised software house over a large IT company?',
        'Large generalist IT companies in Dubai cover everything — websites, mobile apps, infrastructure, ERP — which means they rarely go deep on any one thing. A specialised software house brings focused expertise. For operational software specifically, a partner who understands operations and builds on a proven platform delivers faster, with less risk, than a generalist building from scratch.'
    ],
    [
        'Does Tolx work with SMEs or only large companies?',
        'Tolx works primarily with SMEs and mid-market operators in the UAE — typically businesses running 10 to 500 staff or assets. This is the range where operational software delivers the most value: large enough to outgrow spreadsheets, not so large that enterprise platforms like SAP become necessary.'
    ],
    [
        'How does Tolx price software projects?',
        'Tolx delivers scope-led projects. After a discovery call, you receive a proposal with a defined scope and cost agreed before work begins — no hourly billing, no open-ended estimates. This protects the buyer: the partner absorbs the risk of their own estimates.'
    ],
]);

get_header(); ?>

<div class="container"><?php tolx_render_breadcrumbs(); ?></div>

<!-- ============================================
     HERO
     ============================================ -->
<section class="page-hero">
  <div class="container">
    <div class="fade-in">
      <div class="section-tag mono">Software House · Dubai</div>
      <h1>A Dubai software house for <em>operational systems.</em></h1>
      <p>Tolx builds the software that runs businesses — fleets, EV charging operations, logistics, and adjacent verticals. We're a Dubai-based software house and Odoo Ready Partner, focused on operational systems that fit how your business actually works.</p>
      <div style="margin-top: 28px;">
        <a href="<?php echo home_url('/contact/'); ?>" class="btn-primary">Book a Discovery Call <span>→</span></a>
      </div>
    </div>
  </div>
</section>

<!-- ============================================
     WHAT WE MEAN BY OPERATIONAL SOFTWARE
     ============================================ -->
<section class="section">
  <div class="container">
    <div class="section-head fade-in">
      <div>
        <div class="section-tag mono">Our focus</div>
        <h2 class="section-title">Not every kind of software. One kind, done well.</h2>
      </div>
    </div>

    <div class="single-article single-article-content fade-in" style="max-width: 820px;">
      <p>Dubai has hundreds of software companies. Most are generalists — they build websites, mobile apps, e-commerce stores, marketing platforms, and ERP systems, all under one roof. Breadth like that has a cost: it's hard to go deep on everything.</p>

      <p>Tolx is deliberately narrower. We build <strong>operational software</strong> — the systems that run a business day to day. The asset register that tracks every vehicle or charger. The field-service system that dispatches technicians and logs work orders. The billing engine that invoices clients on contract schedules. The dashboard that shows an operations director what's actually happening.</p>

      <p>This is unglamorous software. It doesn't have a consumer-facing app or a flashy marketing site. It's the layer that decides whether an operation runs smoothly or runs on spreadsheets and WhatsApp. And for businesses, it's the software that matters most.</p>

      <h3>What we build</h3>
      <ul>
        <li><strong>Asset management systems</strong> — full lifecycle tracking for vehicles, chargers, equipment</li>
        <li><strong>Field service &amp; maintenance</strong> — technician dispatch, work orders, parts, fault history</li>
        <li><strong>Project &amp; contract management</strong> — from quote to handover, with milestone billing</li>
        <li><strong>Fleet &amp; logistics operations</strong> — vehicles, routes, deliveries, compliance</li>
        <li><strong>Billing &amp; recurring invoicing</strong> — AMC contracts, COD reconciliation, VAT-compliant</li>
        <li><strong>Management dashboards</strong> — live operational KPIs for decision-makers</li>
      </ul>

      <h3>What we don't build</h3>
      <p>We're honest about scope. Tolx doesn't build consumer mobile apps, marketing websites, e-commerce storefronts, or games. If that's what you need, a generalist agency is a better fit. We build the operational core — and we'd rather tell you that plainly than take a project we're not the right partner for.</p>
    </div>
  </div>
</section>

<!-- ============================================
     HOW WE BUILD — ODOO + CUSTOM
     ============================================ -->
<section class="section">
  <div class="container">
    <div class="section-head fade-in">
      <div>
        <div class="section-tag mono">How we build</div>
        <h2 class="section-title">Odoo as the foundation. Custom work where it counts.</h2>
      </div>
    </div>

    <div class="single-article single-article-content fade-in" style="max-width: 820px;">
      <p>Most operational software does not need to be built from scratch. The functions an operationally complex business needs — inventory, projects, invoicing, maintenance, field service — already exist, proven, in <a href="<?php echo home_url('/odoo/'); ?>">Odoo</a>, the open-source ERP platform Tolx builds on.</p>

      <p>Building from scratch what already exists is slow, expensive, and risky. So the Tolx approach is:</p>

      <ul>
        <li><strong>Configure first.</strong> Start from Odoo and from our pre-built vertical configurations. Most of what an operation needs is already there — it gets configured to match how the business runs.</li>
        <li><strong>Customise where it counts.</strong> Where an operation has a genuinely unique requirement the standard platform doesn't cover, we develop custom modules to extend it.</li>
        <li><strong>Don't rebuild the wheel.</strong> We don't write custom code for problems Odoo already solves. That discipline is what keeps implementations to a 4–8 week timeline instead of 6 months.</li>
      </ul>

      <p>This makes Tolx a software house with a specific model: Odoo-led, custom-extended, vertically focused. It is faster and lower-risk than pure custom development for operational software — and far more tailored than handing a client a blank ERP licence.</p>

      <p><a href="<?php echo home_url('/odoo-partner-dubai/'); ?>">More on Tolx as an Odoo partner in Dubai →</a></p>
    </div>
  </div>
</section>

<!-- ============================================
     WHO WE BUILD FOR
     ============================================ -->
<section class="section">
  <div class="container">
    <div class="section-head fade-in">
      <div>
        <div class="section-tag mono">Example applications</div>
        <h2 class="section-title">Examples of what we build.</h2>
      </div>
    </div>

    <div class="sol-matrix">
      <a href="<?php echo home_url('/solutions/ev-charger-operator-system/'); ?>" class="sol-card is-primary fade-in" data-stagger="1">
        <div class="sol-card-head">
          <div class="sol-card-icon"><?php tolx_icon('charger', 22); ?></div>
          <div class="sol-card-tag">Example</div>
        </div>
        <h3>EV Charging Operations</h3>
        <p>Operational software for EV charger installers and operators — survey to billing in one system.</p>
        <div class="sol-card-foot">
          <div class="chip-row">
            <span class="chip">Asset Register</span>
            <span class="chip">Field Service</span>
          </div>
          <span class="sol-card-link">Explore</span>
        </div>
      </a>

      <a href="<?php echo home_url('/solutions/fleet-management-system/'); ?>" class="sol-card fade-in" data-stagger="2">
        <div class="sol-card-head">
          <div class="sol-card-icon"><?php tolx_icon('fleet', 22); ?></div>
        </div>
        <h3>Fleet Operators</h3>
        <p>Fleet management software for 10–500 vehicles — maintenance, fuel, drivers, compliance.</p>
        <div class="sol-card-foot">
          <div class="chip-row">
            <span class="chip">Maintenance</span>
            <span class="chip">Compliance</span>
          </div>
          <span class="sol-card-link">Explore</span>
        </div>
      </a>

      <a href="<?php echo home_url('/solutions/logistics-last-mile-system/'); ?>" class="sol-card fade-in" data-stagger="3">
        <div class="sol-card-head">
          <div class="sol-card-icon"><?php tolx_icon('delivery', 22); ?></div>
        </div>
        <h3>Logistics Companies</h3>
        <p>Last-mile software — orders, routes, proof of delivery, COD reconciliation.</p>
        <div class="sol-card-foot">
          <div class="chip-row">
            <span class="chip">Routes</span>
            <span class="chip">POD</span>
          </div>
          <span class="sol-card-link">Explore</span>
        </div>
      </a>

      <a href="<?php echo home_url('/solutions/cpo-revenue-module/'); ?>" class="sol-card fade-in" data-stagger="4">
        <div class="sol-card-head">
          <div class="sol-card-icon"><?php tolx_icon('revenue', 22); ?></div>
          <div class="sol-card-tag">Example</div>
        </div>
        <h3>Charge Point Operators</h3>
        <p>Revenue and margin tracking software, per charger.</p>
        <div class="sol-card-foot">
          <div class="chip-row">
            <span class="chip">kWh</span>
            <span class="chip">Margin</span>
          </div>
          <span class="sol-card-link">Explore</span>
        </div>
      </a>
    </div>
  </div>
</section>

<!-- ============================================
     WHY A SPECIALISED SOFTWARE HOUSE
     ============================================ -->
<section class="section">
  <div class="container">
    <div class="section-head fade-in">
      <div>
        <div class="section-tag mono">Generalist vs. specialist</div>
        <h2 class="section-title">Why a focused software house.</h2>
      </div>
    </div>

    <div class="compare-grid fade-in">
      <div class="compare-col compare-col--neg">
        <div class="compare-col-head">
          <span class="compare-col-tag">Generalist IT company</span>
        </div>
        <ul class="compare-list">
          <li>Builds everything — websites, apps, ERP, infrastructure</li>
          <li>Rarely deep in any single domain</li>
          <li>Operational software is one service among many</li>
          <li>Often builds custom from scratch — slow and costly</li>
          <li>Learns your industry during your project</li>
        </ul>
      </div>
      <div class="compare-col compare-col--pos">
        <div class="compare-col-head">
          <span class="compare-col-tag">Tolx — focused software house</span>
        </div>
        <ul class="compare-list">
          <li>Builds one thing: operational systems for operationally complex business</li>
          <li>Deep in EV, fleet, logistics — and the adjacent verticals</li>
          <li>Operational software is the entire focus</li>
          <li>Odoo-led, custom-extended — faster, lower-risk</li>
          <li>Pre-built vertical configurations from day one</li>
        </ul>
      </div>
    </div>
  </div>
</section>

<!-- ============================================
     BEYOND CORE
     ============================================ -->
<section class="section-sm">
  <div class="container">
    <div class="cmd-panel beyond-panel fade-in">
      <div class="beyond-panel-grid">
        <div>
          <div class="cmd-panel-title" style="margin-bottom: 14px;">Examples of where this applies</div>
          <h2 style="font-size: clamp(22px, 2.6vw, 28px); font-weight: 700; letter-spacing: -0.5px; line-height: 1.25; margin-bottom: 14px;">The pattern transfers across industries.</h2>
          <p style="font-size: 15.5px; color: var(--text-sec); line-height: 1.7; margin-bottom: 20px;">Wherever a business depends on assets, workflows, and data to generate revenue, the same approach applies: map how revenue moves, then build the software around it. The industry is the example, not the identity.</p>
          <a href="<?php echo home_url('/contact/'); ?>" class="btn-ghost">Talk to us about your operation →</a>
        </div>
        <div class="beyond-panel-tags">
          <span class="chip">Facility Management</span>
          <span class="chip">Contracting</span>
          <span class="chip">Equipment Rental</span>
          <span class="chip">Distribution</span>
          <span class="chip">Service Operations</span>
          <span class="chip">Field Maintenance</span>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- ============================================
     FAQ
     ============================================ -->
<section class="section" id="faq">
  <div class="container">
    <div class="section-head fade-in">
      <div>
        <div class="section-tag mono">Frequently asked</div>
        <h2 class="section-title">Software house questions.</h2>
      </div>
    </div>

    <div class="single-article single-article-content fade-in" style="max-width: 820px;">

      <h3>What does Tolx do as a software house in Dubai?</h3>
      <p>Tolx is a Dubai software house that builds operational systems for businesses. The core of the work is Odoo implementation — configuring the Odoo ERP platform around how a specific operation runs — including vertical configuration, custom module work where needed, data migration, and ongoing support.</p>

      <h3>Is Tolx a custom software development company?</h3>
      <p>Partly. Tolx builds primarily on Odoo — a highly configurable open-source platform — and extends it with custom module development where an operation needs something the standard platform doesn't cover. This is faster and lower-risk for operational software than building every system from scratch.</p>

      <h3>What kind of software solutions does Tolx build?</h3>
      <p>Operational systems — asset registers, field service and maintenance, project and contract management, fleet and logistics operations, billing and recurring invoicing, and management dashboards. Tolx goes deepest in EV charging, fleet, and logistics.</p>

      <h3>Why choose a specialised software house over a large IT company?</h3>
      <p>Large generalist IT companies cover everything, which means they rarely go deep on any one thing. For operational software specifically, a partner who understands operations and builds on a proven platform delivers faster, with less risk, than a generalist building from scratch.</p>

      <h3>Does Tolx work with SMEs or only large companies?</h3>
      <p>Tolx works primarily with SMEs and mid-market operators in the UAE — typically 10 to 500 staff or assets. This is the range where operational software delivers the most value.</p>

      <h3>How does Tolx price software projects?</h3>
      <p>Scope-led. After a discovery call, you receive a proposal with a defined scope and cost agreed before work begins — no hourly billing, no open-ended estimates.</p>

    </div>
  </div>
</section>

<!-- ============================================
     RELATED
     ============================================ -->
<section class="section">
  <div class="container">
    <div class="section-head fade-in">
      <div>
        <div class="section-tag mono">Continue</div>
        <h2 class="section-title">More about how Tolx works.</h2>
      </div>
    </div>
    <div class="op-grid op-grid--modules">
      <a href="<?php echo home_url('/odoo-partner-dubai/'); ?>" class="op-block fade-in" data-stagger="1" style="text-decoration: none; color: inherit;">
        <div class="op-block-icon"><?php tolx_icon('shield', 18); ?></div>
        <div>
          <h3>Odoo Partner in Dubai</h3>
          <p>Tolx as an Odoo Ready Partner — what that means and how to choose a partner.</p>
        </div>
      </a>
      <a href="<?php echo home_url('/odoo/'); ?>" class="op-block fade-in" data-stagger="2" style="text-decoration: none; color: inherit;">
        <div class="op-block-icon"><?php tolx_icon('module', 18); ?></div>
        <div>
          <h3>What is Odoo?</h3>
          <p>The platform Tolx builds on — what it is, the modules, and where it fits.</p>
        </div>
      </a>
      <a href="<?php echo home_url('/about/our-approach/'); ?>" class="op-block fade-in" data-stagger="3" style="text-decoration: none; color: inherit;">
        <div class="op-block-icon"><?php tolx_icon('check', 18); ?></div>
        <div>
          <h3>Our Approach</h3>
          <p>Scope-led delivery, built around your operation — how Tolx delivers.</p>
        </div>
      </a>
      <a href="<?php echo home_url('/solutions/'); ?>" class="op-block fade-in" data-stagger="4" style="text-decoration: none; color: inherit;">
        <div class="op-block-icon"><?php tolx_icon('operator', 18); ?></div>
        <div>
          <h3>Our Solutions</h3>
          <p>Operational software for EV, fleet, logistics, and adjacent verticals.</p>
        </div>
      </a>
    </div>
  </div>
</section>

<?php get_footer(); ?>
