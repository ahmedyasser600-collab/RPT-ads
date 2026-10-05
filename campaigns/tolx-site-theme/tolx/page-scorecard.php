<?php
/**
 * Template Name: Operations Readiness Scorecard
 * URL: /operations-readiness-scorecard/
 *
 * Interactive lead-magnet landing page — OPPORTUNITY-BASED (not a maturity tier).
 *
 * 6 questions, each mapped to a value lever (MONEY or TIME). Each answer that
 * signals a gap generates an "opportunity" tied to a real system capability.
 * The result surfaces the visitor's top opportunities, sorted into:
 *   - "Make more money"  (revenue capture / cost / visibility)
 *   - "Save time & get organized"  (manual work / control / admin)
 * No score, no tier — purely "here is what you stand to gain, and what fixes it."
 *
 * SESSION 1 SCOPE: full interactive frontend. Form delivery + Google Sheet
 * logging are wired in Session 3. For now the form shows a client-side success.
 */

get_header();
?>

<div class="scorecard-page">

  <!-- ============ INTRO ============ -->
  <section class="sc-stage sc-intro" id="sc-intro">
    <div class="sc-grid-bg" aria-hidden="true"></div>
    <div class="sc-intro-inner">
      <div class="sc-accent-stroke" aria-hidden="true"></div>
      <div class="sc-mono-label">TOLX · OPERATIONS OPPORTUNITY FINDER</div>
      <h1 class="sc-hero-title">What is your operation costing you?</h1>
      <p class="sc-hero-sub">
        Most growing Dubai businesses run on spreadsheets, WhatsApp, and memory.
        It works — but it quietly leaks money and burns time. Answer 6 questions
        and get a personalized report on where your biggest opportunities are:
        to make more, and to work easier.
      </p>
      <div class="sc-intro-meta">
        <div class="sc-intro-meta-item">
          <span class="sc-intro-meta-num">6</span>
          <span class="sc-intro-meta-lbl">QUESTIONS</span>
        </div>
        <div class="sc-intro-meta-divider" aria-hidden="true"></div>
        <div class="sc-intro-meta-item">
          <span class="sc-intro-meta-num">~2</span>
          <span class="sc-intro-meta-lbl">MINUTES</span>
        </div>
        <div class="sc-intro-meta-divider" aria-hidden="true"></div>
        <div class="sc-intro-meta-item">
          <span class="sc-intro-meta-num">2</span>
          <span class="sc-intro-meta-lbl">WAYS TO WIN</span>
        </div>
      </div>
      <button class="sc-btn sc-btn-primary" id="sc-start-btn" type="button">
        Find My Opportunities
        <span class="sc-btn-arrow" aria-hidden="true">→</span>
      </button>
      <p class="sc-intro-reassure">No account needed. Takes about two minutes.</p>
    </div>
  </section>

  <!-- ============ ASSESSMENT ============ -->
  <section class="sc-stage sc-assessment" id="sc-assessment" hidden>
    <div class="sc-grid-bg" aria-hidden="true"></div>
    <div class="sc-assessment-inner">
      <div class="sc-progress-head">
        <div class="sc-progress-meta">
          <span class="sc-mono-label" id="sc-q-counter">QUESTION 1 OF 6</span>
          <span class="sc-category-label mono" id="sc-lever">— —</span>
        </div>
        <div class="sc-progress-bar-track" aria-hidden="true">
          <div class="sc-progress-bar-fill" id="sc-progress-fill"></div>
        </div>
      </div>
      <div class="sc-question-slot" id="sc-question-slot"></div>
      <div class="sc-nav-controls">
        <button class="sc-back-btn" id="sc-back-btn" type="button" hidden>
          <span aria-hidden="true">←</span> Back
        </button>
      </div>
    </div>
  </section>

  <!-- ============ RESULT ============ -->
  <section class="sc-stage sc-result" id="sc-result" hidden>
    <div class="sc-grid-bg" aria-hidden="true"></div>
    <div class="sc-result-inner">
      <div class="sc-accent-stroke" aria-hidden="true"></div>
      <div class="sc-mono-label">YOUR OPPORTUNITIES</div>

      <h2 class="sc-result-headline" id="sc-result-headline">Here's where your operation can win.</h2>
      <p class="sc-result-lede" id="sc-result-lede"></p>

      <div class="sc-opp-cols">
        <div class="sc-opp-col" id="sc-col-money">
          <div class="sc-opp-col-head">
            <span class="sc-opp-col-icon" aria-hidden="true">$</span>
            <span class="sc-opp-col-title">Make more money</span>
          </div>
          <div class="sc-opp-list" id="sc-money-list"></div>
        </div>
        <div class="sc-opp-col" id="sc-col-time">
          <div class="sc-opp-col-head">
            <span class="sc-opp-col-icon" aria-hidden="true">&#9719;</span>
            <span class="sc-opp-col-title">Save time &amp; get organized</span>
          </div>
          <div class="sc-opp-list" id="sc-time-list"></div>
        </div>
      </div>

      <div class="sc-gap-teaser">
        <div class="sc-gap-teaser-head">
          <span class="mono" id="sc-opp-count-label">— OPPORTUNITIES IDENTIFIED</span>
        </div>
        <p class="sc-gap-teaser-body">
          Your personalised summary records your answers and suggests practical areas to review. It is a starting point for a discussion, rather than an estimate of savings or a promise of automation.
        </p>
      </div>

      <div class="sc-form-wrap" id="sc-form-wrap">
        <div class="sc-form-head">
          <h2 class="sc-form-title">Get your full opportunity report</h2>
          <p class="sc-form-sub">We'll email it over. No spam — one follow-up at most.</p>
        </div>
        <form class="sc-form" id="sc-form" novalidate>
          <div class="sc-form-row">
            <div class="sc-field">
              <label for="sc-name">Name</label>
              <input type="text" id="sc-name" name="name" autocomplete="name" required>
            </div>
            <div class="sc-field">
              <label for="sc-email">Work email</label>
              <input type="email" id="sc-email" name="email" autocomplete="email" required>
            </div>
          </div>
          <div class="sc-form-row">
            <div class="sc-field">
              <label for="sc-company">Company</label>
              <input type="text" id="sc-company" name="company" autocomplete="organization" required>
            </div>
            <div class="sc-field">
              <label for="sc-sector">Sector</label>
              <select id="sc-sector" name="sector" required>
                <option value="" disabled selected>Select…</option>
                <option>Retail &amp; E-commerce</option>
                <option>Trading &amp; Distribution</option>
                <option>Logistics &amp; Transport</option>
                <option>Construction &amp; Contracting</option>
                <option>Healthcare &amp; Clinics</option>
                <option>Professional Services</option>
                <option>Manufacturing &amp; Industrial</option>
                <option>Hospitality &amp; F&amp;B</option>
                <option>EV &amp; Energy</option>
                <option>Real Estate &amp; Facilities</option>
                <option>Automotive &amp; Fleet</option>
                <option>Education &amp; Training</option>
                <option>Field Service &amp; Maintenance</option>
                <option>Events &amp; Rentals</option>
                <option>Import / Export</option>
                <option>Agriculture &amp; Food Production</option>
                <option>Marine &amp; Shipping</option>
                <option>Government &amp; Semi-Government</option>
                <option>Other</option>
              </select>
            </div>
          </div>
          <div class="sc-form-row">
            <div class="sc-field sc-field-full">
              <label for="sc-role">Your role</label>
              <select id="sc-role" name="role" required>
                <option value="" disabled selected>Select…</option>
                <option>Owner / Founder</option>
                <option>CEO / Managing Director</option>
                <option>COO / Operations Director</option>
                <option>Operations Manager</option>
                <option>General Manager</option>
                <option>Finance / Admin Lead</option>
                <option>IT / Systems Lead</option>
                <option>Other</option>
              </select>
            </div>
          </div>

          <!-- Consent (required, unticked by default) -->
          <div class="sc-consent">
            <label class="sc-consent-label">
              <input type="checkbox" id="sc-consent" name="consent" value="yes">
              <span class="sc-consent-box" aria-hidden="true"></span>
              <span class="sc-consent-text">
                I agree that Tolx may use the details I've provided to send me my report and
                contact me about it. I can opt out any time. See the
                <a href="/privacy-policy/" target="_blank" rel="noopener">privacy policy</a>.
              </span>
            </label>
          </div>

          <!-- Honeypot (hidden from humans; bots fill it) -->
          <div class="sc-hp" aria-hidden="true">
            <label>Website<input type="text" id="sc-website" name="sc_website" tabindex="-1" autocomplete="off"></label>
          </div>

          <input type="hidden" id="sc-answers-field" name="answers" value="">
          <input type="hidden" id="sc-opps-field" name="opportunities" value="">

          <button class="sc-btn sc-btn-primary sc-form-submit" type="submit">
            Get My Full Report
            <span class="sc-btn-arrow" aria-hidden="true">→</span>
          </button>
          <p class="sc-form-error" id="sc-form-error" hidden>Please complete all fields with a valid email.</p>
        </form>
      </div>

      <div class="sc-success" id="sc-success" hidden>
        <div class="sc-success-icon" aria-hidden="true">&#10003;</div>
        <h2 class="sc-success-title">Your report is ready.</h2>
        <p class="sc-success-body">
          Your submission status and personalised summary appear here.
        </p>
        <a href="#" id="sc-download-btn" class="sc-btn sc-btn-primary" download>
          Download your report
          <span class="sc-btn-arrow" aria-hidden="true">↓</span>
        </a>
        <div class="sc-success-divider"></div>
        <a href="/contact/" class="sc-btn sc-btn-ghost">
          Want to talk it through? Book a discovery call
          <span class="sc-btn-arrow" aria-hidden="true">→</span>
        </a>
      </div>

      <button class="sc-retake-btn" id="sc-retake-btn" type="button">↺ Start over</button>
    </div>
  </section>

</div>

<style>
.scorecard-page {
  --sc-gap-soft: rgba(255,255,255,0.045);
  position: relative; min-height: calc(100vh - var(--nav-h));
  background: var(--bg); color: var(--text); overflow: hidden;
}
.scorecard-page [hidden] { display: none !important; }
.sc-stage {
  position: relative; min-height: calc(100vh - var(--nav-h));
  display: flex; align-items: center; justify-content: center; padding: 64px 24px;
}
.sc-grid-bg {
  position: absolute; inset: 0;
  background-image:
    linear-gradient(var(--sc-gap-soft) 1px, transparent 1px),
    linear-gradient(90deg, var(--sc-gap-soft) 1px, transparent 1px);
  background-size: 60px 60px; pointer-events: none;
  mask-image: radial-gradient(ellipse 80% 70% at 50% 40%, #000 30%, transparent 100%);
  -webkit-mask-image: radial-gradient(ellipse 80% 70% at 50% 40%, #000 30%, transparent 100%);
}
.sc-accent-stroke { width: 88px; height: 3px; background: var(--gold); margin-bottom: 22px; }
.sc-mono-label {
  font-family: 'Share Tech Mono', monospace; font-size: 13px;
  letter-spacing: 2.5px; text-transform: uppercase; color: var(--gold); margin-bottom: 18px;
}
.sc-btn {
  display: inline-flex; align-items: center; gap: 12px;
  font-family: 'Chakra Petch', sans-serif; font-weight: 600;
  font-size: 17px; letter-spacing: 0.3px; padding: 16px 32px;
  border-radius: var(--radius); cursor: pointer; border: none;
  transition: all 0.22s ease; text-decoration: none;
}
.sc-btn-primary { background: var(--gold); color: #0a0a0a; }
.sc-btn-primary:hover { background: var(--gold-hover); transform: translateY(-2px); }
.sc-btn-ghost { background: transparent; color: var(--gold); border: 1.5px solid var(--line-gold); }
.sc-btn-ghost:hover { border-color: var(--gold); background: var(--gold-soft); }
.sc-btn-arrow { transition: transform 0.22s ease; }
.sc-btn:hover .sc-btn-arrow { transform: translateX(4px); }
.sc-intro-inner { position: relative; max-width: 720px; text-align: left; }
.sc-hero-title {
  font-family: 'Chakra Petch', sans-serif; font-weight: 700;
  font-size: clamp(38px, 6vw, 68px); line-height: 1.04; letter-spacing: -1.5px; margin: 0 0 24px;
}
.sc-hero-sub { font-size: 19px; line-height: 1.65; color: var(--text-sec); margin: 0 0 40px; max-width: 600px; }
.sc-intro-meta { display: flex; align-items: center; gap: 28px; margin-bottom: 40px; }
.sc-intro-meta-item { display: flex; flex-direction: column; gap: 4px; }
.sc-intro-meta-num { font-family: 'Chakra Petch', sans-serif; font-weight: 700; font-size: 32px; color: var(--text); line-height: 1; }
.sc-intro-meta-lbl { font-family: 'Share Tech Mono', monospace; font-size: 11px; letter-spacing: 2px; color: var(--text-sec); }
.sc-intro-meta-divider { width: 1px; height: 36px; background: var(--border); }
.sc-intro-reassure { margin-top: 16px; font-size: 13px; color: var(--text-sec); font-family: 'Share Tech Mono', monospace; letter-spacing: 0.5px; }
.sc-assessment-inner { position: relative; width: 100%; max-width: 720px; }
.sc-progress-head { margin-bottom: 48px; }
.sc-progress-meta { display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 14px; }
.sc-category-label { font-size: 12px; letter-spacing: 2px; color: var(--text-sec); }
.sc-progress-bar-track { width: 100%; height: 3px; background: var(--border); border-radius: 2px; overflow: hidden; }
.sc-progress-bar-fill { height: 100%; width: 16.66%; background: var(--gold); border-radius: 2px; transition: width 0.4s cubic-bezier(0.4,0,0.2,1); }
.sc-question-slot { min-height: 340px; }
.sc-question-text {
  font-family: 'Chakra Petch', sans-serif; font-weight: 700;
  font-size: clamp(24px, 3.4vw, 34px); line-height: 1.2; letter-spacing: -0.5px; margin: 0 0 32px;
}
.sc-options { display: flex; flex-direction: column; gap: 12px; }
.sc-option {
  display: flex; align-items: center; gap: 16px; padding: 20px 22px;
  background: var(--surface); border: 1.5px solid var(--border);
  border-radius: var(--radius); cursor: pointer; transition: all 0.18s ease;
  text-align: left; font-family: 'Chakra Petch', sans-serif; font-size: 16px; color: var(--text); width: 100%;
}
.sc-option:hover { border-color: var(--line-gold); background: var(--surface-2); transform: translateX(4px); }
.sc-option-marker { width: 22px; height: 22px; border-radius: 50%; border: 1.5px solid var(--text-sec); flex-shrink: 0; transition: all 0.18s ease; }
.sc-option:hover .sc-option-marker { border-color: var(--gold); }
.sc-option.selected { border-color: var(--gold); background: var(--gold-soft); }
.sc-option.selected .sc-option-marker { border-color: var(--gold); background: var(--gold); box-shadow: inset 0 0 0 3px var(--surface); }
.sc-nav-controls { margin-top: 28px; min-height: 24px; }
.sc-back-btn { background: none; border: none; color: var(--text-sec); font-family: 'Share Tech Mono', monospace; font-size: 13px; letter-spacing: 1px; cursor: pointer; padding: 6px 0; transition: color 0.18s ease; }
.sc-back-btn:hover { color: var(--gold); }
.sc-question-slot.sc-fade-in-anim { animation: scFadeIn 0.32s ease forwards; }
@keyframes scFadeIn { from { opacity: 0; transform: translateX(12px); } to { opacity: 1; transform: translateX(0); } }
.sc-result-inner { position: relative; width: 100%; max-width: 760px; }
.sc-result-headline {
  font-family: 'Chakra Petch', sans-serif; font-weight: 700;
  font-size: clamp(30px, 4.5vw, 48px); line-height: 1.1; letter-spacing: -1px; margin: 0 0 16px;
}
.sc-result-lede { font-size: 18px; line-height: 1.6; color: var(--text-sec); margin: 0 0 40px; max-width: 640px; }
.sc-opp-cols { display: flex; gap: 20px; margin-bottom: 36px; }
.sc-opp-col { flex: 1; background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius-lg); padding: 24px; }
.sc-opp-col-head { display: flex; align-items: center; gap: 12px; margin-bottom: 18px; padding-bottom: 16px; border-bottom: 1px solid var(--border); }
.sc-opp-col-icon {
  width: 34px; height: 34px; display: flex; align-items: center; justify-content: center;
  background: var(--gold-soft); border: 1px solid var(--line-gold); border-radius: 8px;
  color: var(--gold); font-family: 'Chakra Petch', sans-serif; font-weight: 700; font-size: 18px;
}
.sc-opp-col-title { font-family: 'Chakra Petch', sans-serif; font-weight: 600; font-size: 18px; }
.sc-opp-list { display: flex; flex-direction: column; gap: 14px; }
.sc-opp-item { display: flex; gap: 12px; align-items: flex-start; }
.sc-opp-item-bullet { width: 7px; height: 7px; border-radius: 50%; background: var(--gold); margin-top: 7px; flex-shrink: 0; }
.sc-opp-item-text { font-size: 15px; line-height: 1.5; color: var(--text); }
.sc-opp-item-odoo { display: block; font-family: 'Share Tech Mono', monospace; font-size: 11px; letter-spacing: 1px; color: var(--text-sec); margin-top: 4px; text-transform: uppercase; }
.sc-opp-empty { font-size: 14px; color: var(--text-sec); line-height: 1.5; font-style: italic; }
.sc-gap-teaser { background: var(--surface); border: 1px solid var(--border); border-left: 3px solid var(--gold); border-radius: var(--radius); padding: 24px 26px; margin-bottom: 40px; }
.sc-gap-teaser-head { margin-bottom: 10px; }
.sc-gap-teaser-head .mono { font-family: 'Share Tech Mono', monospace; font-size: 13px; letter-spacing: 1.5px; color: var(--gold); }
.sc-gap-teaser-body { font-size: 15px; line-height: 1.6; color: var(--text-sec); margin: 0; }
.sc-form-wrap { background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius-lg); padding: 36px; }
.sc-form-head { margin-bottom: 28px; }
.sc-form-title { font-family: 'Chakra Petch', sans-serif; font-weight: 700; font-size: 28px; letter-spacing: -0.5px; margin: 0 0 8px; }
.sc-form-sub { font-size: 14px; color: var(--text-sec); margin: 0; line-height: 1.5; }
.sc-form-row { display: flex; gap: 16px; margin-bottom: 16px; }
.sc-field { flex: 1; display: flex; flex-direction: column; gap: 7px; }
.sc-field-full { flex: 1 1 100%; }
.sc-field label { font-family: 'Share Tech Mono', monospace; font-size: 11px; letter-spacing: 1.5px; text-transform: uppercase; color: var(--text-sec); }
.sc-field input, .sc-field select { background: var(--bg); border: 1.5px solid var(--border); border-radius: var(--radius); padding: 13px 15px; color: var(--text); font-family: 'Chakra Petch', sans-serif; font-size: 15px; transition: border-color 0.18s ease; }
.sc-field input:focus, .sc-field select:focus { outline: none; border-color: var(--gold); }
.sc-field select { cursor: pointer; }
.sc-form-submit { width: 100%; justify-content: center; margin-top: 12px; }
.sc-form-error { color: #E0696C; font-size: 13px; margin: 12px 0 0; font-family: 'Share Tech Mono', monospace; text-align: center; }

/* Consent checkbox */
.sc-consent { margin: 6px 0 4px; }
.sc-consent-label { display: flex; align-items: flex-start; gap: 12px; cursor: pointer; }
.sc-consent-label input { position: absolute; opacity: 0; width: 0; height: 0; }
.sc-consent-box {
  flex-shrink: 0; width: 22px; height: 22px; margin-top: 1px;
  border: 1.5px solid var(--border); border-radius: 6px; background: var(--bg);
  transition: all 0.18s ease; position: relative;
}
.sc-consent-label:hover .sc-consent-box { border-color: var(--line-gold); }
.sc-consent-label input:checked + .sc-consent-box {
  background: var(--gold); border-color: var(--gold);
}
.sc-consent-label input:checked + .sc-consent-box::after {
  content: ''; position: absolute; left: 7px; top: 3px;
  width: 5px; height: 10px; border: solid #0a0a0a;
  border-width: 0 2px 2px 0; transform: rotate(45deg);
}
.sc-consent-label input:focus-visible + .sc-consent-box { box-shadow: 0 0 0 3px var(--gold-soft); }
.sc-consent-text { font-size: 13px; line-height: 1.5; color: var(--text-sec); }
.sc-consent-text a { color: var(--gold); text-decoration: underline; }

/* Honeypot — visually hidden, off-screen */
.sc-hp { position: absolute; left: -9999px; top: -9999px; width: 1px; height: 1px; overflow: hidden; }

/* Success divider */
.sc-success-divider { height: 1px; background: var(--border); margin: 28px auto; max-width: 200px; }
#sc-download-btn { margin-bottom: 4px; }
.sc-success { text-align: center; padding: 48px 24px; background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius-lg); }
.sc-success-icon { width: 64px; height: 64px; margin: 0 auto 24px; display: flex; align-items: center; justify-content: center; background: var(--gold-soft); border: 2px solid var(--gold); border-radius: 50%; color: var(--gold); font-size: 30px; }
.sc-success-title { font-family: 'Chakra Petch', sans-serif; font-weight: 700; font-size: 30px; letter-spacing: -0.5px; margin: 0 0 12px; }
.sc-success-body { font-size: 16px; color: var(--text-sec); line-height: 1.6; margin: 0 auto 28px; max-width: 440px; }
.sc-retake-btn { display: block; margin: 28px auto 0; background: none; border: none; color: var(--text-sec); font-family: 'Share Tech Mono', monospace; font-size: 12px; letter-spacing: 1px; cursor: pointer; transition: color 0.18s ease; }
.sc-retake-btn:hover { color: var(--gold); }
@media (max-width: 700px) { .sc-opp-cols { flex-direction: column; } }
@media (max-width: 600px) {
  .sc-stage { padding: 40px 18px; }
  .sc-form-wrap { padding: 24px; }
  .sc-form-row { flex-direction: column; gap: 16px; }
  .sc-intro-meta { gap: 18px; }
  .sc-question-slot { min-height: 380px; }
}
</style>

<script>
(function () {
  'use strict';

  var QUESTIONS = <?php echo wp_json_encode(tolx_assessment_questions(), JSON_HEX_TAG | JSON_HEX_AMP | JSON_HEX_APOS | JSON_HEX_QUOT); ?>;

  var transitioning = false;
  var answers = new Array(QUESTIONS.length).fill(null);
  var current = 0;

  var introEl  = document.getElementById('sc-intro');
  var assessEl = document.getElementById('sc-assessment');
  var resultEl = document.getElementById('sc-result');
  var slot     = document.getElementById('sc-question-slot');
  var counter  = document.getElementById('sc-q-counter');
  var lever    = document.getElementById('sc-lever');
  var progFill = document.getElementById('sc-progress-fill');
  var backBtn  = document.getElementById('sc-back-btn');

  function renderQuestion() {
    var Q = QUESTIONS[current];
    counter.textContent = 'QUESTION ' + (current + 1) + ' OF ' + QUESTIONS.length;
    lever.textContent = Q.leverLabel;
    progFill.style.width = ((current + 1) / QUESTIONS.length * 100) + '%';
    backBtn.hidden = (current === 0);

    var html = '<h2 class="sc-question-text">' + Q.q + '</h2><div class="sc-options">';
    for (var i = 0; i < Q.opts.length; i++) {
      var sel = (answers[current] === i) ? ' selected' : '';
      html += '<button type="button" class="sc-option' + sel + '" data-idx="' + i + '">' +
              '<span class="sc-option-marker" aria-hidden="true"></span>' +
              '<span>' + Q.opts[i].t + '</span></button>';
    }
    html += '</div>';
    slot.innerHTML = html;

    slot.classList.remove('sc-fade-in-anim');
    void slot.offsetWidth;
    slot.classList.add('sc-fade-in-anim');

    var btns = slot.querySelectorAll('.sc-option');
    for (var j = 0; j < btns.length; j++) btns[j].addEventListener('click', onSelect);
  }

  function onSelect(e) {
    if (transitioning) return; transitioning = true;
    var idx = parseInt(e.currentTarget.getAttribute('data-idx'), 10);
    answers[current] = idx;
    var all = slot.querySelectorAll('.sc-option');
    for (var i = 0; i < all.length; i++) all[i].classList.remove('selected');
    e.currentTarget.classList.add('selected');
    setTimeout(function () {
      transitioning = false;
      if (current < QUESTIONS.length - 1) { current++; renderQuestion(); }
      else { showResult(); }
    }, 280);
  }

  backBtn.addEventListener('click', function () {
    if (!transitioning && current > 0) { current--; renderQuestion(); }
  });

  document.getElementById('sc-start-btn').addEventListener('click', function () {
    introEl.hidden = true; assessEl.hidden = false;
    current = 0; renderQuestion();
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });

  function collectOpportunities() {
    var money = [], time = [];
    for (var i = 0; i < QUESTIONS.length; i++) {
      if (answers[i] === null) continue;
      var opt = QUESTIONS[i].opts[answers[i]];
      if (opt.gap && opt.opp) {
        (QUESTIONS[i].lever === 'money' ? money : time).push(opt.opp);
      }
    }
    return { money: money, time: time };
  }

  function renderOppList(el, list) {
    if (list.length === 0) {
      el.innerHTML = '<p class="sc-opp-empty">No major gaps here \u2014 you\u2019re in good shape on this front.</p>';
      return;
    }
    var html = '';
    for (var i = 0; i < list.length; i++) {
      html += '<div class="sc-opp-item">' +
              '<span class="sc-opp-item-bullet" aria-hidden="true"></span>' +
              '<span class="sc-opp-item-text">' + list[i].text +
              '<span class="sc-opp-item-odoo">' + list[i].odoo + '</span>' +
              '</span></div>';
    }
    el.innerHTML = html;
  }

  function showResult() {
    var opps = collectOpportunities();
    var total = opps.money.length + opps.time.length;

    assessEl.hidden = true; resultEl.hidden = false;
    window.scrollTo({ top: 0, behavior: 'smooth' });

    var headlineEl = document.getElementById('sc-result-headline');
    var ledeEl = document.getElementById('sc-result-lede');
    var m = opps.money.length, t = opps.time.length;

    if (total === 0) {
      headlineEl.textContent = 'You\u2019re running a tight operation.';
      ledeEl.textContent = 'Few businesses answer this cleanly \u2014 you\u2019re clearly already disciplined about how you run things. There are no obvious gaps to flag. The remaining gains are in refinement, or in a specific need a general setup doesn\u2019t cover well. If there\u2019s one area still nagging you, that\u2019s the conversation worth having.';
    } else if (m > 0 && t > 0) {
      // both levers present — the most common case
      headlineEl.textContent = 'Your opportunities are on both fronts.';
      ledeEl.textContent = 'Based on how you answered, there are clear wins in both directions: ' + m + ' way' + (m>1?'s':'') + ' to capture revenue and see your numbers more clearly, and ' + t + ' way' + (t>1?'s':'') + ' to cut manual work and get organized. Each one below is matched to the system capability that delivers it.';
    } else if (m > 0) {
      // money only
      headlineEl.textContent = 'Your biggest opportunities are financial.';
      ledeEl.textContent = 'Based on how you answered, the clearest wins are in capturing revenue and seeing your true numbers \u2014 ' + m + ' opportunit' + (m>1?'ies':'y') + ' in total. Each one below is matched to the system capability that delivers it.';
    } else {
      // time only
      headlineEl.textContent = 'Your biggest opportunities are in time and control.';
      ledeEl.textContent = 'Based on how you answered, the clearest wins are in cutting manual work and getting organized \u2014 ' + t + ' opportunit' + (t>1?'ies':'y') + ' in total. Each one below is matched to the system capability that delivers it.';
    }

    renderOppList(document.getElementById('sc-money-list'), opps.money);
    renderOppList(document.getElementById('sc-time-list'), opps.time);

    var label = document.getElementById('sc-opp-count-label');
    if (total === 0) label.textContent = 'STRONG FOUNDATION \u2014 FEW GAPS';
    else if (total === 1) label.textContent = '1 OPPORTUNITY IDENTIFIED';
    else label.textContent = total + ' OPPORTUNITIES IDENTIFIED';

    document.getElementById('sc-answers-field').value = answers.join(',');
    var oppText = [];
    for (var i = 0; i < opps.money.length; i++) oppText.push('MONEY: ' + opps.money[i].text);
    for (var k = 0; k < opps.time.length; k++) oppText.push('TIME: ' + opps.time[k].text);
    document.getElementById('sc-opps-field').value = oppText.join(' | ');
  }

  var form = document.getElementById('sc-form');
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    if (form.querySelector('.sc-form-submit').disabled) return;
    var name = document.getElementById('sc-name').value.trim();
    var email = document.getElementById('sc-email').value.trim();
    var company = document.getElementById('sc-company').value.trim();
    var sector = document.getElementById('sc-sector').value;
    var role = document.getElementById('sc-role').value;
    var consent = document.getElementById('sc-consent').checked;
    var errEl = document.getElementById('sc-form-error');
    var submitBtn = form.querySelector('.sc-form-submit');
    var emailOk = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);

    if (!name || !emailOk || !company || !sector || !role) {
      errEl.textContent = 'Please complete all fields with a valid email.';
      errEl.hidden = false; return;
    }
    if (!consent) {
      errEl.textContent = 'Please tick the box to confirm you\u2019re happy for us to send your report.';
      errEl.hidden = false; return;
    }
    errEl.hidden = true;

    // If the WP-provided endpoint/nonce aren't present (e.g. previewing the
    // template outside WordPress), show a recoverable configuration error.
    if (typeof window.TOLX_SC === 'undefined') {
      errEl.textContent = 'Submission is unavailable. Please refresh or contact sales@tolx.ae.'; errEl.hidden = false;
      return;
    }

    // Real submission
    submitBtn.disabled = true;
    var originalLabel = submitBtn.innerHTML;
    submitBtn.innerHTML = 'Sending\u2026';

    var body = new URLSearchParams();
    body.append('action', 'tolx_scorecard_lead');
    body.append('sc_nonce', window.TOLX_SC.nonce);
    body.append('name', name);
    body.append('email', email);
    body.append('company', company);
    body.append('sector', sector);
    body.append('role', role);
    body.append('consent', consent ? 'yes' : '');
    body.append('sc_website', document.getElementById('sc-website').value);
    body.append('answers', document.getElementById('sc-answers-field').value);
    body.append('opportunities', document.getElementById('sc-opps-field').value);

    fetch(window.TOLX_SC.ajaxUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: body.toString()
    })
    .then(function (r) { return r.json(); })
    .then(function (res) {
      if (res && res.success) {
        showSuccess(email, res.data);
        if (!res.data.duplicate && window.tolxMeasure) window.tolxMeasure('assessment_saved');
      } else {
        submitBtn.disabled = false; submitBtn.innerHTML = originalLabel;
        errEl.textContent = (res && res.data && res.data.message) ? res.data.message
          : 'Something went wrong. Please try again, or email sales@tolx.ae.';
        errEl.hidden = false;
      }
    })
    .catch(function () {
      submitBtn.disabled = false; submitBtn.innerHTML = originalLabel;
      errEl.textContent = 'Network error. Please try again, or email sales@tolx.ae.';
      errEl.hidden = false;
    });
  });

  function showSuccess(email, data) {
    document.getElementById('sc-form-wrap').hidden = true;
    var body = document.querySelector('.sc-success-body');
    body.style.whiteSpace = 'pre-line';
    body.textContent = data.message + '\n\n' + data.summary;
    document.getElementById('sc-download-btn').hidden = true;
    document.getElementById('sc-success').hidden = false;
    document.querySelector('.sc-gap-teaser').style.display = 'none';
    document.querySelector('.sc-opp-cols').style.display = 'none';
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  document.getElementById('sc-retake-btn').addEventListener('click', function () {
    answers = new Array(QUESTIONS.length).fill(null);
    current = 0;
    resultEl.hidden = true;
    document.getElementById('sc-form-wrap').hidden = false;
    document.getElementById('sc-success').hidden = true;
    document.querySelector('.sc-gap-teaser').style.display = '';
    document.querySelector('.sc-opp-cols').style.display = '';
    var sb = form.querySelector('.sc-form-submit');
    sb.disabled = false;
    sb.innerHTML = 'Get My Full Report <span class="sc-btn-arrow" aria-hidden="true">\u2192</span>';
    introEl.hidden = false;
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });

})();
</script>

<?php get_footer(); ?>
