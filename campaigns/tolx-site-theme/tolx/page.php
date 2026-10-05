<?php
/**
 * Default page template
 */
get_header(); ?>

<section class="page-hero">
  <div class="container">
    <div class="fade-in">
      <h1><?php the_title(); ?></h1>
    </div>
  </div>
</section>

<section style="position:relative;z-index:1;padding:0 0 100px;">
  <div class="container">
    <div class="fade-in" style="max-width:760px;font-size:16px;color:var(--text-sec);line-height:1.8;">
      <?php while (have_posts()) : the_post(); ?>
        <?php if (get_post_meta(get_the_ID(), '_tolx_content_key', true) && has_post_thumbnail()) : ?>
          <figure class="single-article-feature">
            <?php the_post_thumbnail('large', ['class' => 'single-article-feature-img']); ?>
            <figcaption><?php echo esc_html(wp_get_attachment_caption(get_post_thumbnail_id())); ?></figcaption>
          </figure>
        <?php endif; ?>
        <?php the_content(); ?>
      <?php endwhile; ?>
    </div>
  </div>
</section>

<?php get_footer(); ?>
