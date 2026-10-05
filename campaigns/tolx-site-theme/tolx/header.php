<!DOCTYPE html>
<html <?php language_attributes(); ?>>
<head>
  <meta charset="<?php bloginfo('charset'); ?>">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0">
  <meta name="theme-color" content="#09090B">
  <meta name="msapplication-TileColor" content="#09090B">
  <meta name="application-name" content="Tolx">
  <meta name="apple-mobile-web-app-title" content="Tolx">
  <meta name="author" content="Tolx">
  <meta name="generator" content="Tolx · UAE Software House &amp; Business Systems Partner">
  <link rel="icon" type="image/x-icon" href="<?php echo get_template_directory_uri(); ?>/favicon.ico">
  <link rel="icon" type="image/png" sizes="32x32" href="<?php echo get_template_directory_uri(); ?>/favicon-32x32.png">
  <link rel="icon" type="image/png" sizes="16x16" href="<?php echo get_template_directory_uri(); ?>/favicon-16x16.png">
  <link rel="apple-touch-icon" sizes="180x180" href="<?php echo get_template_directory_uri(); ?>/apple-touch-icon.png">
  <link rel="manifest" href="<?php echo get_template_directory_uri(); ?>/site.webmanifest">
  <script>try{if(sessionStorage.getItem('tolxSeen'))document.documentElement.classList.add('no-preload')}catch(e){}</script>
  <?php wp_head(); ?>
</head>
<body <?php body_class(); ?>>
<?php wp_body_open(); ?>

<div class="scroll-progress" aria-hidden="true"></div>

<!-- PRELOADER -->
<div id="preloader">
  <div class="preloader-inner">
    <?php tolx_helm(80, 'preloader-helm'); ?>
    <span class="preloader-wordmark">TOLX<span style="color:#D4A843">.</span></span>
  </div>
</div>

<!-- NAV -->
<nav class="nav">
  <div class="nav-inner">
    <a href="<?php echo home_url(); ?>" class="nav-logo">
      <?php tolx_helm(32); ?>
      <span class="nav-wordmark">TOLX<span>.</span></span>
    </a>
    <ul class="nav-links">
      <li><a href="<?php echo home_url('/'); ?>" <?php if(is_front_page()) echo 'class="active"'; ?>>Home</a></li>
      <li><a href="<?php echo home_url('/solutions/'); ?>" <?php
        $sol_page = get_page_by_path('solutions');
        $is_sol = is_page('solutions') || (is_page() && $sol_page && wp_get_post_parent_id(get_the_ID()) == $sol_page->ID);
        if($is_sol) echo 'class="active"'; ?>>Systems</a></li>
      <li><a href="<?php echo home_url('/growth-systems/'); ?>" <?php if(is_page('growth-systems')) echo 'class="active"'; ?>>Growth Systems</a></li>
      <li><a href="<?php echo home_url('/about/'); ?>" <?php
        $abt_page = get_page_by_path('about');
        $is_abt = is_page('about') || (is_page() && $abt_page && wp_get_post_parent_id(get_the_ID()) == $abt_page->ID);
        if($is_abt) echo 'class="active"'; ?>>About</a></li>
      <li><a href="<?php echo home_url('/blog/'); ?>" <?php if(is_home() || is_single()) echo 'class="active"'; ?>>Blog</a></li>
      <li><a href="<?php echo home_url('/contact/'); ?>" <?php if(is_page('contact')) echo 'class="active"'; ?>>Contact</a></li>
      <li><a href="<?php echo home_url('/operations-readiness-scorecard/'); ?>" class="nav-cta nav-cta-ghost">Find Your Opportunities</a></li>
      <li><a href="<?php echo home_url('/contact/'); ?>" class="nav-cta">Book a Call</a></li>
    </ul>
    <button class="nav-mobile-toggle" aria-label="Toggle menu" aria-expanded="false" aria-controls="nav-mobile">
      <span></span><span></span><span></span>
    </button>
  </div>
</nav>

<!-- Mobile Menu -->
<div class="nav-mobile" id="nav-mobile">
  <a href="<?php echo home_url('/'); ?>">Home</a>
  <a href="<?php echo home_url('/solutions/'); ?>">Systems</a>
  <a href="<?php echo home_url('/growth-systems/'); ?>">Growth Systems</a>
  <a href="<?php echo home_url('/about/'); ?>">About</a>
  <a href="<?php echo home_url('/blog/'); ?>">Blog</a>
  <a href="<?php echo home_url('/contact/'); ?>">Contact</a>
  <a href="<?php echo home_url('/operations-readiness-scorecard/'); ?>" class="nav-cta nav-cta-ghost">Find Your Opportunities</a>
  <a href="<?php echo home_url('/contact/'); ?>" class="nav-cta">Book a Call</a>
</div>
