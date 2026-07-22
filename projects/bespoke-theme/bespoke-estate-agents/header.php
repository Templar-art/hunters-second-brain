<?php if (!defined('ABSPATH')) exit; ?><!doctype html>
<html <?php language_attributes(); ?>>
<head>
  <meta charset="<?php bloginfo('charset'); ?>">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="preload" href="<?php echo esc_url(get_template_directory_uri()); ?>/assets/fonts/Zodiak-Light.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="<?php echo esc_url(get_template_directory_uri()); ?>/assets/fonts/poppins-400.woff2" as="font" type="font/woff2" crossorigin>
  <script>try{if(sessionStorage.getItem('beaSeen'))document.documentElement.dataset.preloaded='1'}catch(e){}</script>
  <?php wp_head(); ?>
</head>
<body <?php body_class(); ?>>
<?php wp_body_open(); ?>

  <!-- Startup logo-draw intro (plays once per session) -->
  <div class="preloader" id="preloader" aria-hidden="true">
    <video class="preloader__vid" autoplay muted playsinline>
      <source src="<?php echo esc_url(get_template_directory_uri()); ?>/assets/video/loadscreen.mp4" type="video/mp4">
    </video>
  </div>

  <?php
    $icon = get_template_directory_uri() . '/assets/logos/bespoke-icon-offwhite.svg';
    $nav  = array(
      ''              => 'Home',
      'about'         => 'About',
      'services'      => 'Services',
      'sold-listings' => 'Sold Listings',
      'projects'      => 'Projects',
      'contact'       => 'Contact',
    );
  ?>

  <header class="site-header">
    <div class="wrap">
      <a class="brand" href="<?php echo esc_url(home_url('/')); ?>" aria-label="Bespoke Estate Agents home">
        <img class="brand__icon" src="<?php echo esc_url($icon); ?>" alt="">
        <span class="brand__word"><b>BESPOKE</b><span>Estate Agents</span></span>
      </a>

      <nav class="nav-desktop" aria-label="Primary">
        <?php foreach ($nav as $slug => $label) :
          $url = $slug === '' ? home_url('/') : home_url('/' . $slug . '/');
          $current = ($slug === '' && is_front_page()) || ($slug !== '' && is_page($slug));
        ?>
          <a href="<?php echo esc_url($url); ?>"<?php echo $current ? ' aria-current="page"' : ''; ?>><?php echo esc_html($label); ?></a>
        <?php endforeach; ?>
      </nav>

      <a class="btn btn--light header-cta" href="<?php echo esc_url(home_url('/contact/')); ?>">Book an Appraisal</a>

      <button class="menu-toggle" aria-label="Open menu" aria-expanded="false" aria-controls="site-menu">
        <span></span><span></span><span></span>
      </button>
    </div>
  </header>

  <!-- Full-screen slide-over menu -->
  <div class="site-menu" id="site-menu">
    <nav aria-label="Full site">
      <?php $n = 0; foreach ($nav as $slug => $label) : $n++;
        $url = $slug === '' ? home_url('/') : home_url('/' . $slug . '/'); ?>
        <a href="<?php echo esc_url($url); ?>"><span class="num"><?php echo esc_html(sprintf('%02d', $n)); ?></span><?php echo esc_html($label); ?></a>
      <?php endforeach; ?>
    </nav>
    <div class="site-menu__foot">
      <span>Gold Coast, Queensland</span>
      <span>
        <a href="tel:0422228229">0422 228 229</a>
        &nbsp;&middot;&nbsp;
        <a href="mailto:info@bespokerealestate.com.au">info@bespokerealestate.com.au</a>
      </span>
    </div>
  </div>

  <main id="main">
