<?php
/**
 * Template Name: Odoo UAE Implementation
 * URL: /odoo/uae-implementation/
 *
 * Implementation-focused landing page targeting `odoo implementation uae`,
 * `odoo dubai consultant`, `odoo partner dubai`, `odoo middle east`.
 */

tolx_register_faq([
    [
        'How long does an Odoo implementation take in the UAE?',
        'A focused, vertical-specific Odoo implementation typically goes live in 4 to 8 weeks. Broader cross-functional rollouts take 3 to 6 months. The variance depends on scope, data complexity, integration count, and stakeholder availability. Tolx works to the 4–8 week range for most engagements through pre-built vertical configurations.'
    ],
    [
        'What\'s the difference between a UAE Odoo implementation and a global one?',
        'UAE-specific Odoo implementations need configuration for 5% VAT, FTA-compliant invoice formatting, multi-currency handling for GCC operations, Arabic language and RTL rendering, and operational realities like Mulkiya renewals (fleets), DEWA approval workflows (EV chargers), RTA registration cycles, and ESMA certifications. None of this is "out of the box" — it\'s configured during implementation by a partner who knows the UAE context.'
    ],
    [
        'Can my UAE business implement Odoo without a partner?',
        'Technically yes — Odoo Online and Odoo.sh both support self-implementation. In practice, most UAE businesses with operational complexity benefit significantly from a partner. The partner brings vertical knowledge, UAE compliance experience, data migration discipline, training resources, and direct escalation to Odoo\'s technical team for edge cases. Self-implementation works for very small operations with simple needs.'
    ],
    [
        'Do you handle Odoo licence purchases as part of implementation?',
        'We coordinate the licence purchase but Odoo SA bills the customer directly. Tolx does not mark up Odoo licensing — you pay Odoo what they charge. We handle the partner-side coordination during Week 1 setup, including tier selection (Standard vs Custom) and user-count planning.'
    ],
    [
        'What happens after go-live? Do you stay involved?',
        'Yes. Every Tolx implementation includes a 30-day post-launch support window with same-day response on operational issues. After that window, most clients sign an Annual Maintenance Contract (AMC) for ongoing support, system updates, and vertical-specific enhancements. AMC scope is agreed alongside the implementation proposal.'
    ],
    [
        'What if my industry isn\'t EV, fleet, or logistics?',
        'Tolx configures Odoo across many kinds of UAE operations. We map how your business runs, then configure the modules around it — sales, inventory, accounting, projects, field service, and more. The same scope-led approach applies across industries; less common ones simply need a little more discovery.'
    ],
]);

get_header(); ?>

<div class="container"><?php tolx_render_breadcrumbs(); ?></div>

<section class="page-hero">
  <div class="container">
    <div class="hero-grid">
      <div class="fade-in">
        <div class="section-tag mono">Odoo Implementation in the UAE</div>
        <h1>Odoo implementation, <em>built for UAE operations.</em></h1>
        <p>VAT-aware. DEWA-compatible. RTA-friendly. Arabic-capable. Tolx is a Dubai-based Odoo implementation partner that delivers vertical-specific systems for UAE operators in 4 to 8 weeks — not 4 to 6 months.</p>
        <div style="margin-top: 28px;">
          <a href="<?php echo home_url('/contact/'); ?>" class="btn-primary">Book a Discovery Call <span>→</span></a>
        </div>
      </div>

      <div class="hero-cmd" aria-hidden="true">
        <div class="cmd-panel">
          <div class="cmd-panel-head">
            <div class="cmd-panel-title">UAE · Compliance Layer</div>
            <div class="cmd-panel-meta"><span class="cmd-panel-dot"></span> Configured</div>
          </div>
          <div class="cmd-row">
            <div class="cmd-row-icon"><?php tolx_icon('shield', 18); ?></div>
            <div class="cmd-row-label">UAE 5% VAT</div>
            <div class="cmd-row-tag">FTA-ready</div>
          </div>
          <div class="cmd-row">
            <div class="cmd-row-icon"><?php tolx_icon('charger', 18); ?></div>
            <div class="cmd-row-label">DEWA workflows</div>
            <div class="cmd-row-tag">EV operators</div>
          </div>
          <div class="cmd-row">
            <div class="cmd-row-icon"><?php tolx_icon('vehicle', 18); ?></div>
            <div class="cmd-row-label">RTA &amp; Mulkiya</div>
            <div class="cmd-row-tag">Fleet</div>
          </div>
          <div class="cmd-row">
            <div class="cmd-row-icon"><?php tolx_icon('contract', 18); ?></div>
            <div class="cmd-row-label">Arabic &amp; RTL</div>
            <div class="cmd-row-tag">Bilingual</div>
          </div>
          <div class="cmd-row">
            <div class="cmd-row-icon"><?php tolx_icon('billing', 18); ?></div>
            <div class="cmd-row-label">Multi-currency</div>
            <div class="cmd-row-tag">GCC-ready</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- ============================================
     WHY UAE IS DIFFERENT
     ============================================ -->
<section class="section">
  <div class="container">
    <div class="section-head fade-in">
      <div>
        <div class="section-tag mono">Why UAE is different</div>
        <h2 class="section-title">UAE Odoo isn't generic Odoo with a VAT toggle.</h2>
      </div>
    </div>

    <div class="single-article single-article-content fade-in" style="max-width: 820px;">

      <p>Most Odoo implementations in the UAE are run by partners who treat UAE compliance as an afterthought — a checkbox at the end. The result is a system that technically meets requirements but doesn't reflect how UAE operations actually work.</p>

      <p>UAE-specific implementation done right means configuring the platform around realities like:</p>

      <ul>
        <li><strong>5% VAT integration that matches FTA invoice format requirements</strong> — including TRN display, mandatory fields, and bilingual invoice support</li>
        <li><strong>Multi-currency handling for GCC operations</strong> — AED, SAR, KWD, OMR, BHD, QAR with proper consolidation reporting</li>
        <li><strong>Arabic language support that goes beyond translated menus</strong> — full RTL document generation, Arabic legal entity names, bilingual customer-facing outputs</li>
        <li><strong>Operational compliance built into workflows</strong> — Mulkiya renewals as automated alerts, DEWA approval status as charger asset states, RTA registration cycles as fleet milestones, ESMA certifications as equipment readiness gates</li>
        <li><strong>Multi-emirate awareness</strong> — different regulatory cycles, different government touchpoints, different documentation requirements between Dubai, Abu Dhabi, Sharjah, and other emirates</li>
      </ul>

      <p>This isn't bolted-on customisation. It's how the system is configured during implementation — by a partner that has done it before, in this market, for this industry.</p>

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
        <div class="section-tag mono">Timeline</div>
        <h2 class="section-title">Four phases. 4–8 weeks.</h2>
      </div>
    </div>

    <div class="route route--phases">
      <div class="route-stop fade-in" data-stagger="1">
        <div class="route-marker">W1–2</div>
        <h3>Discovery &amp; Setup</h3>
        <p>Workflow mapping, asset inventory review, system environment provisioning, base configuration begins.</p>
      </div>
      <div class="route-stop fade-in" data-stagger="2">
        <div class="route-marker">W3–4</div>
        <h3>Configuration &amp; Data</h3>
        <p>Vertical modules configured. Existing data (asset register, client list, history) migrated and verified.</p>
      </div>
      <div class="route-stop fade-in" data-stagger="3">
        <div class="route-marker">W5–6</div>
        <h3>Training &amp; Validation</h3>
        <p>Hands-on training for office staff and field teams. Onsite or remote. UAT against real-world scenarios.</p>
      </div>
      <div class="route-stop fade-in" data-stagger="4">
        <div class="route-marker">W7–8</div>
        <h3>Go-Live &amp; Support</h3>
        <p>Cutover to production. Same-day support during the post-launch period. AMC engagement begins.</p>
      </div>
    </div>
  </div>
</section>

<!-- ============================================
     WHAT'S INCLUDED
     ============================================ -->
<section class="section">
  <div class="container">
    <div class="section-head fade-in">
      <div>
        <div class="section-tag mono">What's included</div>
        <h2 class="section-title">Every UAE implementation, every time.</h2>
      </div>
    </div>

    <div class="op-grid op-grid--modules">
      <div class="op-block fade-in" data-stagger="1">
        <div class="op-block-icon"><?php tolx_icon('contract', 18); ?></div>
        <div>
          <h3>Scope-led proposal</h3>
          <p>Detailed scope document before work begins. Modules, configuration depth, data migration, training, support window — all defined in a single scope-led proposal.</p>
        </div>
      </div>
      <div class="op-block fade-in" data-stagger="2">
        <div class="op-block-icon"><?php tolx_icon('shield', 18); ?></div>
        <div>
          <h3>UAE compliance configuration</h3>
          <p>VAT, FTA invoice formats, multi-currency, Arabic/RTL, and industry-specific regulatory workflows configured during implementation.</p>
        </div>
      </div>
      <div class="op-block fade-in" data-stagger="3">
        <div class="op-block-icon"><?php tolx_icon('module', 18); ?></div>
        <div>
          <h3>Data migration</h3>
          <p>Existing data — customer records, asset registers, transactional history — migrated, verified, and ready in the new system.</p>
        </div>
      </div>
      <div class="op-block fade-in" data-stagger="4">
        <div class="op-block-icon"><?php tolx_icon('users', 18); ?></div>
        <div>
          <h3>Hands-on training</h3>
          <p>Office staff trained on back-end modules. Field teams trained on mobile workflows. Onsite or remote, English or Arabic.</p>
        </div>
      </div>
      <div class="op-block fade-in" data-stagger="5">
        <div class="op-block-icon"><?php tolx_icon('operator', 18); ?></div>
        <div>
          <h3>Dedicated project manager</h3>
          <p>One person owns the engagement from kickoff to go-live. Weekly check-ins, clear status, direct access throughout.</p>
        </div>
      </div>
      <div class="op-block fade-in" data-stagger="6">
        <div class="op-block-icon"><?php tolx_icon('live', 18); ?></div>
        <div>
          <h3>Post-launch support window</h3>
          <p>30 days of close hands-on support after go-live. Same-day response on operational issues. AMC begins after the support window.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- ============================================
     INDUSTRIES
     ============================================ -->
<section class="section">
  <div class="container">
    <div class="section-head fade-in">
      <div>
        <div class="section-tag mono">Industries we know</div>
        <h2 class="section-title">Where Tolx goes deepest.</h2>
      </div>
    </div>

    <div class="sol-matrix">
      <a href="<?php echo home_url('/solutions/ev-charger-operator-system/'); ?>" class="sol-card is-primary fade-in" data-stagger="1">
        <div class="sol-card-head">
          <div class="sol-card-icon"><?php tolx_icon('charger', 22); ?></div>
          <div class="sol-card-tag">Primary Vertical</div>
        </div>
        <h3>EV Charger Operations</h3>
        <p>Survey to billing in one system. Asset register, project management, field service, contracts, and CPO revenue — for UAE EV operators and DEWA-approved installers.</p>
        <div class="sol-card-foot">
          <div class="chip-row">
            <span class="chip">Site Survey</span>
            <span class="chip">DEWA</span>
            <span class="chip">Field Service</span>
            <span class="chip">CPO Revenue</span>
          </div>
          <span class="sol-card-link">Explore</span>
        </div>
      </a>

      <a href="<?php echo home_url('/solutions/fleet-management-system/'); ?>" class="sol-card fade-in" data-stagger="2">
        <div class="sol-card-head">
          <div class="sol-card-icon"><?php tolx_icon('fleet', 22); ?></div>
        </div>
        <h3>Fleet Management</h3>
        <p>Vehicle register, maintenance, fuel, drivers, compliance, TCO — for fleets of 10 to 500 vehicles.</p>
        <div class="sol-card-foot">
          <div class="chip-row">
            <span class="chip">Mulkiya</span>
            <span class="chip">RTA</span>
            <span class="chip">Drivers</span>
          </div>
          <span class="sol-card-link">Explore</span>
        </div>
      </a>

      <a href="<?php echo home_url('/solutions/logistics-last-mile-system/'); ?>" class="sol-card fade-in" data-stagger="3">
        <div class="sol-card-head">
          <div class="sol-card-icon"><?php tolx_icon('delivery', 22); ?></div>
        </div>
        <h3>Logistics &amp; Last-Mile</h3>
        <p>Order intake, route planning, proof of delivery, COD reconciliation. Real-time client portal.</p>
        <div class="sol-card-foot">
          <div class="chip-row">
            <span class="chip">Routes</span>
            <span class="chip">POD</span>
            <span class="chip">COD</span>
          </div>
          <span class="sol-card-link">Explore</span>
        </div>
      </a>

      <a href="<?php echo home_url('/solutions/cpo-revenue-module/'); ?>" class="sol-card fade-in" data-stagger="4">
        <div class="sol-card-head">
          <div class="sol-card-icon"><?php tolx_icon('revenue', 22); ?></div>
          <div class="sol-card-tag">Add-on</div>
        </div>
        <h3>CPO Revenue</h3>
        <p>Margin clarity per charger — kWh, session revenue, energy cost, gross margin.</p>
        <div class="sol-card-foot">
          <div class="chip-row">
            <span class="chip">kWh</span>
            <span class="chip">Margin</span>
            <span class="chip">DEWA</span>
          </div>
          <span class="sol-card-link">Explore</span>
        </div>
      </a>
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
          <div class="cmd-panel-title" style="margin-bottom: 14px;">Adjacent verticals</div>
          <h2 style="font-size: clamp(22px, 2.6vw, 28px); font-weight: 700; letter-spacing: -0.5px; line-height: 1.25; margin-bottom: 14px;">UAE operation outside our flagship verticals?</h2>
          <p style="font-size: 15.5px; color: var(--text-sec); line-height: 1.7; margin-bottom: 20px;">Facility management, contracting, equipment rental, distribution, service operations — if your operation involves physical assets, distributed teams, and compliance overlap, the same UAE-aware Odoo playbook applies. The vertical pre-configurations are deepest for EV/Fleet/Logistics, but the operational logic transfers.</p>
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
        <h2 class="section-title">UAE implementation questions.</h2>
      </div>
    </div>

    <div class="single-article single-article-content fade-in" style="max-width: 820px;">

      <h3>How long does an Odoo implementation take in the UAE?</h3>
      <p>A focused, vertical-specific Odoo implementation typically goes live in 4 to 8 weeks. Broader cross-functional rollouts take 3 to 6 months. The variance depends on scope, data complexity, integration count, and stakeholder availability.</p>

      <h3>What's the difference between a UAE implementation and a global one?</h3>
      <p>UAE-specific implementations need configuration for 5% VAT, FTA-compliant invoice formatting, multi-currency for GCC, Arabic/RTL, and operational realities like Mulkiya, DEWA, RTA, ESMA. None of this is "out of the box" — it's configured by a partner who knows the UAE context.</p>

      <h3>Can my UAE business implement Odoo without a partner?</h3>
      <p>Technically yes. In practice, most UAE businesses with operational complexity benefit significantly from a partner. The partner brings vertical knowledge, UAE compliance experience, data migration discipline, training resources, and direct escalation to Odoo's technical team.</p>

      <h3>Do you handle Odoo licence purchases as part of implementation?</h3>
      <p>We coordinate the licence purchase but Odoo SA bills the customer directly. Tolx does not mark up Odoo licensing — you pay Odoo what they charge.</p>

      <h3>What happens after go-live? Do you stay involved?</h3>
      <p>Yes. Every implementation includes a 30-day post-launch support window with same-day response. After that, most clients sign an AMC for ongoing support, updates, and enhancements.</p>

      <h3>What if my industry isn't EV, fleet, or logistics?</h3>
      <p>Tolx configures Odoo across many kinds of UAE operations. The same scope-led approach applies, shaped by how your business actually works.</p>

    </div>
  </div>
</section>

<?php get_footer(); ?>
