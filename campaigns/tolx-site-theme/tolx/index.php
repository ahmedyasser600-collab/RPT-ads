<?php
/**
 * Fallback template - redirects to blog
 */
get_header(); ?>

<section class="page-hero">
  <div class="container">
    <div class="fade-in">
      <h1><?php wp_title(''); ?></h1>
    </div>
  </div>
</section>

<section style="position:relative;z-index:1;padding:0 0 100px;">
  <div class="container">
    <?php if (have_posts()) : ?>
      <div class="blog-grid">
        <?php while (have_posts()) : the_post(); ?>
          <a href="<?php the_permalink(); ?>" class="blog-card fade-in">
            <div class="blog-card-img">
              <?php if (has_post_thumbnail()) the_post_thumbnail('medium_large'); ?>
            </div>
            <div class="blog-card-body">
              <div class="blog-card-meta"><?php echo get_the_date('M j, Y'); ?></div>
              <h3><?php the_title(); ?></h3>
              <p><?php echo get_the_excerpt(); ?></p>
            </div>
          </a>
        <?php endwhile; ?>
      </div>
    <?php endif; ?>
  </div>
</section>

<?php get_footer(); ?>
