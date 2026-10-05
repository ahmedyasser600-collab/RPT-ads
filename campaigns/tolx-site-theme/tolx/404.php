<?php
/**
 * 404 template
 */
get_header(); ?>

<section class="section" style="padding-top:160px;">
  <div class="container">
    <div class="cmd-panel fade-in" style="text-align:center;padding:80px 40px;max-width:680px;margin:0 auto;">
      <div class="cmd-panel-head" style="justify-content:center;border-bottom:none;padding-bottom:0;margin-bottom:32px;">
        <div class="cmd-panel-title">Status · 404</div>
      </div>
      <div style="font-family:'Share Tech Mono',monospace;font-size:96px;font-weight:700;letter-spacing:-2px;color:var(--gold);line-height:1;margin-bottom:24px;">404</div>
      <h1 style="font-size:32px;font-weight:600;margin-bottom:12px;letter-spacing:-0.6px;">Off the route.</h1>
      <p style="font-size:16px;color:var(--text-sec);margin-bottom:32px;line-height:1.6;">The page you're looking for doesn't exist or has been moved.</p>
      <div style="display:flex;gap:14px;justify-content:center;flex-wrap:wrap;">
        <a href="<?php echo home_url(); ?>" class="btn-primary">Back to Home <span>→</span></a>
        <a href="<?php echo home_url('/solutions/'); ?>" class="btn-ghost">View Solutions</a>
      </div>
    </div>
  </div>
</section>

<?php get_footer(); ?>
