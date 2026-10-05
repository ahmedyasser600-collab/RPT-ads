<?php
/**
 * Single post template
 */
get_header(); ?>

<div class="container"><?php tolx_render_breadcrumbs(); ?></div>

<?php while (have_posts()) : the_post(); ?>

<section class="page-hero">
  <div class="container">
    <div class="fade-in single-article">
      <div class="single-article-meta">
        <?php
          $cats = get_the_category();
          if ($cats) echo '<span class="blog-card-cat">' . esc_html($cats[0]->name) . '</span>';
          echo '<span class="blog-card-date">' . get_the_date('F j, Y') . '</span>';
          echo '<span class="blog-card-date">By ' . esc_html(get_the_author()) . '</span>';
        ?>
      </div>
      <h1><?php the_title(); ?></h1>
    </div>
  </div>
</section>

<?php if (has_post_thumbnail()) : ?>
<section class="section-bare" style="padding:0 0 56px;">
  <div class="container">
    <div class="single-article-feature">
      <?php the_post_thumbnail('large', ['class' => 'single-article-feature-img']); ?>
      <?php if (get_post_meta(get_post_thumbnail_id(), '_tolx_editorial_image_key', true)) : ?>
        <p><?php echo esc_html(wp_get_attachment_caption(get_post_thumbnail_id())); ?></p>
      <?php endif; ?>
    </div>
  </div>
</section>
<?php endif; ?>

<section class="section-bare" style="padding:0 0 var(--section-y);">
  <div class="container">
    <article class="fade-in single-article single-article-content">
      <?php the_content(); ?>
      <?php if (strpos(get_post_field('post_name', get_the_ID()), 'whatsapp') !== false) : ?>
      <p><a href="<?php echo esc_url(tolx_published_destination('order-tracking-customer-follow-up', '/contact/')); ?>">Discuss order tracking and customer follow-up</a></p>
      <?php endif; ?>
    </article>

    <!-- Post navigation -->
    <?php
      $prev_post = get_previous_post();
      $next_post = get_next_post();
      if ($prev_post || $next_post) :
    ?>
    <nav class="single-article" style="margin-top:64px;display:grid;grid-template-columns:1fr 1fr;gap:14px;" aria-label="Post navigation">
      <?php if ($prev_post) : ?>
        <a href="<?php echo get_permalink($prev_post); ?>" class="op-block" style="text-decoration:none;color:inherit;">
          <div class="op-block-icon"><?php tolx_icon('return', 18); ?></div>
          <div>
            <h3 style="font-size:11px;font-family:'Share Tech Mono',monospace;letter-spacing:1.8px;text-transform:uppercase;color:var(--gold);margin-bottom:6px;">Previous</h3>
            <p style="color:var(--text);"><?php echo esc_html(get_the_title($prev_post)); ?></p>
          </div>
        </a>
      <?php else : ?>
        <div></div>
      <?php endif; ?>
      <?php if ($next_post) : ?>
        <a href="<?php echo get_permalink($next_post); ?>" class="op-block" style="text-decoration:none;color:inherit;text-align:right;grid-template-columns:1fr 38px;">
          <div>
            <h3 style="font-size:11px;font-family:'Share Tech Mono',monospace;letter-spacing:1.8px;text-transform:uppercase;color:var(--gold);margin-bottom:6px;">Next</h3>
            <p style="color:var(--text);"><?php echo esc_html(get_the_title($next_post)); ?></p>
          </div>
          <div class="op-block-icon"><?php tolx_icon('arrow', 18); ?></div>
        </a>
      <?php else : ?>
        <div></div>
      <?php endif; ?>
    </nav>
    <?php endif; ?>

  </div>
</section>

<?php endwhile; ?>

<?php get_footer(); ?>
