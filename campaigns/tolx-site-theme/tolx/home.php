<?php
/**
 * Blog index / archive
 */
get_header(); ?>

<section class="page-hero">
  <div class="container">
    <div class="fade-in">
      <div class="section-tag mono">Insights</div>
      <h1>Blog</h1>
      <p>Practical guides for UAE SMEs managing orders, stock, customer follow-ups and team tasks, alongside Odoo, EV, fleet and logistics insights.</p>
    </div>
  </div>
</section>

<section style="position:relative;z-index:1;padding:0 0 100px;">
  <div class="container">
    <?php if (have_posts()) : ?>
      <div class="blog-grid">
        <?php $i = 0; while (have_posts()) : the_post(); $i++; ?>
          <a href="<?php the_permalink(); ?>" class="blog-card fade-in" data-stagger="<?php echo min($i, 6); ?>">
            <div class="blog-card-img">
              <?php if (has_post_thumbnail()) : ?>
                <?php the_post_thumbnail('medium_large'); ?>
              <?php else : ?>
                <div class="blog-card-img-fallback"><?php tolx_icon('module', 32); ?></div>
              <?php endif; ?>
            </div>
            <div class="blog-card-body">
              <div class="blog-card-meta">
                <?php
                  $cats = get_the_category();
                  if ($cats) echo '<span class="blog-card-cat">' . esc_html($cats[0]->name) . '</span>';
                  echo '<span class="blog-card-date">' . get_the_date('M j, Y') . '</span>';
                ?>
              </div>
              <h3><?php the_title(); ?></h3>
              <p><?php echo get_the_excerpt(); ?></p>
              <span class="blog-card-link">Read article →</span>
            </div>
          </a>
        <?php endwhile; ?>
      </div>

      <div style="text-align:center;margin-top:48px;">
        <?php
          the_posts_pagination(array(
            'prev_text' => '← Previous',
            'next_text' => 'Next →',
          ));
        ?>
      </div>
    <?php else : ?>
      <div style="text-align:center;padding:80px 0;">
        <p style="color:var(--text-sec);font-size:16px;">No posts yet. Check back soon.</p>
      </div>
    <?php endif; ?>
  </div>
</section>

<?php get_footer(); ?>
