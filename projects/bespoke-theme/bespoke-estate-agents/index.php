<?php if (!defined('ABSPATH')) exit; get_header(); ?>

<section class="page-hero">
  <div class="wrap">
    <h1><?php echo esc_html(wp_get_document_title()); ?></h1>
  </div>
</section>

<section class="section">
  <div class="wrap prose">
    <?php if (have_posts()) : while (have_posts()) : the_post(); ?>
      <article <?php post_class('reveal'); ?>>
        <?php the_content(); ?>
      </article>
    <?php endwhile; else : ?>
      <p class="muted">Nothing to show here yet.</p>
    <?php endif; ?>
  </div>
</section>

<?php get_footer(); ?>
