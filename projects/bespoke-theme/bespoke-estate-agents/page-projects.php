<?php if (!defined('ABSPATH')) exit; get_header(); ?>

<section class="page-hero has-img">
  <div class="page-hero__media"><img src="<?php echo esc_url(bea_asset('boulevard-01.jpg')); ?>" alt="A Bespoke campaign" loading="lazy"></div>
  <div class="wrap"><div class="maxw-prose">
    <span class="eyebrow on-dark">Signature Campaigns</span>
    <h1>Presentation is everything.</h1>
    <p>The way a home is seen shapes what it sells for. A closer look at how Bespoke brings prestige property to market.</p>
  </div></div>
</section>

<section class="section">
  <div class="wrap">
    <div class="center maxw-prose reveal">
      <span class="eyebrow">Featured Work</span>
      <h2>Every property treated as a brand statement.</h2>
      <p class="muted mt-md">Cinematic, considered, and never overproduced. Each campaign is built to make the right buyer stop and look.</p>
    </div>
    <div class="property-grid mt-2xl">
      <?php
        $campaigns = array(
          array('boulevard-01.jpg', 'The Boulevard', 'Golden-hour drone and lifestyle capture across a waterfront enclave.'),
          array('cairngorm-01.jpg', '11 Cairngorm Street', 'Twilight architectural photography and considered styling.'),
          array('northview-02.jpg', '43 Northview', 'Ground and aerial capture telling the full story of a marina home.'),
        );
        $d = 0;
        foreach ($campaigns as $c) : ?>
        <a class="property reveal"<?php echo $d ? ' data-delay="' . $d . '"' : ''; ?> href="<?php echo esc_url(home_url('/sold-listings/')); ?>">
          <span class="property__tag">Campaign</span>
          <div class="property__img"><img src="<?php echo esc_url(bea_asset($c[0])); ?>" alt="<?php echo esc_attr($c[1]); ?> campaign" loading="lazy"></div>
          <div class="property__body">
            <h3><?php echo esc_html($c[1]); ?></h3>
            <p class="muted" style="color:var(--be-grey-300)"><?php echo esc_html($c[2]); ?></p>
          </div>
        </a>
      <?php $d++; endforeach; ?>
    </div>
  </div>
</section>

<section class="section section--green">
  <div class="wrap">
    <div class="center maxw-prose reveal">
      <span class="eyebrow on-dark">The Approach</span>
      <h2>What goes into a Bespoke campaign.</h2>
    </div>
    <div class="grid grid-4 mt-2xl">
      <div class="reveal"><div class="stat" style="border-radius:var(--be-radius-lg);background:var(--be-green-light)"><b>Film</b><span>Cinematic walkthroughs</span></div></div>
      <div class="reveal" data-delay="1"><div class="stat" style="border-radius:var(--be-radius-lg);background:var(--be-green-light)"><b>Stills</b><span>Architectural photography</span></div></div>
      <div class="reveal" data-delay="2"><div class="stat" style="border-radius:var(--be-radius-lg);background:var(--be-green-light)"><b>Aerial</b><span>Drone &amp; location</span></div></div>
      <div class="reveal" data-delay="3"><div class="stat" style="border-radius:var(--be-radius-lg);background:var(--be-green-light)"><b>Story</b><span>Styling &amp; copy</span></div></div>
    </div>
  </div>
</section>

<section class="section section--offwhite">
  <div class="wrap">
    <div class="center maxw-prose reveal">
      <span class="eyebrow">A Closer Look</span>
      <h2>Selected frames.</h2>
    </div>
    <div class="gallery mt-2xl reveal">
      <img src="<?php echo esc_url(bea_asset('boulevard-03.jpg')); ?>" alt="Campaign frame" loading="lazy">
      <img src="<?php echo esc_url(bea_asset('cairngorm-11.jpg')); ?>" alt="Campaign frame" loading="lazy">
      <img src="<?php echo esc_url(bea_asset('northview-17.jpg')); ?>" alt="Campaign frame" loading="lazy">
      <img src="<?php echo esc_url(bea_asset('cairngorm-14.jpg')); ?>" alt="Campaign frame" loading="lazy">
      <img src="<?php echo esc_url(bea_asset('northview-25.jpg')); ?>" alt="Campaign frame" loading="lazy">
      <img src="<?php echo esc_url(bea_asset('boulevard-04.jpg')); ?>" alt="Campaign frame" loading="lazy">
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap center maxw-prose reveal">
    <h2>Have a property that deserves this?</h2>
    <p class="muted mt-md">Let us show you what a considered campaign looks like for your home.</p>
    <div class="btn-row mt-lg" style="justify-content:center"><a class="btn btn--primary" href="<?php echo esc_url(home_url('/contact/')); ?>">Start a Conversation</a></div>
  </div>
</section>

<?php get_footer(); ?>
