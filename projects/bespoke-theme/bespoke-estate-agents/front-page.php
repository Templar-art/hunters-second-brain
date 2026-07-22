<?php if (!defined('ABSPATH')) exit; get_header(); ?>

<!-- HERO -->
<section class="hero">
  <div class="hero__media">
    <video autoplay muted loop playsinline poster="<?php echo esc_url(bea_asset('hero.jpg')); ?>">
      <source src="<?php echo esc_url(bea_asset('hero.mp4')); ?>" type="video/mp4">
    </video>
  </div>
  <div class="hero__inner">
    <div class="wrap">
      <span class="eyebrow on-dark">Gold Coast Prestige Property</span>
      <h1>Beyond luxury real estate.</h1>
      <p class="lead">Every property has a story. Every seller deserves the right person to tell it. Boutique, people first, and built on local knowledge you will not find anywhere else.</p>
      <div class="btn-row">
        <a class="btn btn--light" href="<?php echo esc_url(home_url('/contact/')); ?>">Book a Free Appraisal</a>
        <a class="btn btn--outline-light" href="<?php echo esc_url(home_url('/sold-listings/')); ?>">View Recent Results</a>
      </div>
    </div>
  </div>
  <div class="hero__scroll">Scroll</div>
</section>

<!-- INTRO -->
<section class="section">
  <div class="wrap">
    <div class="split split--media-right">
      <div class="reveal">
        <span class="eyebrow">The Bespoke Difference</span>
        <h2>A straightforward approach to prestige property.</h2>
        <p class="lead mt-md">Jason Ward brings clarity to a market that too often trades on noise. No jargon, no pressure, just local knowledge and honest advice. Whether you are selling the family home or your next investment, you will always know exactly where you stand.</p>
        <p class="muted mt-md">The Gold Coast is not one market. It is thirty different micro markets, each with its own buyers, its own timing, and its own price ceiling. Knowing the difference is what separates a good result from an exceptional one.</p>
        <a class="btn btn--outline mt-lg" href="<?php echo esc_url(home_url('/about/')); ?>">Meet Jason</a>
      </div>
      <div class="split__media reveal" data-delay="1">
        <img src="<?php echo esc_url(bea_asset('cairngorm-04.jpg')); ?>" alt="Prestige Gold Coast residence" loading="lazy">
      </div>
    </div>
  </div>
</section>

<!-- STATS -->
<section class="section--tight section--green">
  <div class="wrap">
    <div class="stats reveal">
      <div class="stat"><b>30+</b><span>Gold Coast micro markets</span></div>
      <div class="stat"><b>14</b><span>Median days to sold</span></div>
      <div class="stat"><b>100%</b><span>Boutique attention</span></div>
      <div class="stat"><b>1</b><span>Agent, start to finish</span></div>
    </div>
  </div>
</section>

<!-- FEATURED PROJECTS -->
<section class="section section--offwhite">
  <div class="wrap">
    <div class="center maxw-prose reveal">
      <span class="eyebrow">Recent Results</span>
      <h2>The visual proof of what Bespoke delivers.</h2>
      <p class="muted mt-md">A closer look at the homes we have taken to market, presented the way prestige property deserves to be seen.</p>
    </div>
    <div class="property-grid mt-2xl">
      <?php
        $feat = array(
          array('boulevard-01.jpg', 'The Boulevard', 'A waterfront residence captured at golden hour, from the air and at ground level.'),
          array('cairngorm-01.jpg', '11 Cairngorm Street', 'A light filled family home framed by established gardens, styled and sold at full potential.'),
          array('northview-01.jpg', '43 Northview', 'A marina-front position told through ground and aerial photography.'),
        );
        $d = 0;
        foreach ($feat as $f) : ?>
        <a class="property reveal"<?php echo $d ? ' data-delay="' . $d . '"' : ''; ?> href="<?php echo esc_url(home_url('/sold-listings/')); ?>">
          <span class="property__tag">Sold</span>
          <div class="property__img"><img src="<?php echo esc_url(bea_asset($f[0])); ?>" alt="<?php echo esc_attr($f[1]); ?>" loading="lazy"></div>
          <div class="property__body">
            <h3><?php echo esc_html($f[1]); ?></h3>
            <p class="muted" style="color:var(--be-grey-300)"><?php echo esc_html($f[2]); ?></p>
          </div>
        </a>
      <?php $d++; endforeach; ?>
    </div>
    <div class="center mt-2xl reveal"><a class="btn btn--primary" href="<?php echo esc_url(home_url('/sold-listings/')); ?>">View All Listings</a></div>
  </div>
</section>

<!-- SERVICES TEASER -->
<section class="section">
  <div class="wrap">
    <div class="center maxw-prose reveal">
      <span class="eyebrow">How We Work</span>
      <h2>Managed so you do not have to think about it.</h2>
    </div>
    <div class="grid grid-3 mt-2xl">
      <div class="card reveal"><h3>Selling</h3><p class="muted">A considered campaign built around your property and your timing, from first appraisal to settlement day, with no surprises.</p></div>
      <div class="card reveal" data-delay="1"><h3>Appraisals</h3><p class="muted">An honest read on what your home is worth right now, grounded in real local data, not a number designed to win your business.</p></div>
      <div class="card reveal" data-delay="2"><h3>Market Insight</h3><p class="muted">Suburb by suburb intelligence on price movement and buyer demand, so every decision you make is an informed one.</p></div>
    </div>
    <div class="center mt-2xl reveal"><a class="btn btn--outline" href="<?php echo esc_url(home_url('/services/')); ?>">Explore Services</a></div>
  </div>
</section>

<!-- CLOSING CTA -->
<section class="page-hero has-img">
  <div class="page-hero__media"><img src="<?php echo esc_url(bea_asset('location-aerial.jpg')); ?>" alt="Gold Coast from above" loading="lazy"></div>
  <div class="wrap">
    <div class="maxw-prose reveal">
      <span class="eyebrow on-dark">Thinking of selling?</span>
      <h1>Let us show you what is happening in your street.</h1>
      <p>A short conversation is often all it takes to see the difference the right agent makes. No pressure, no obligation.</p>
      <div class="btn-row mt-lg"><a class="btn btn--light" href="<?php echo esc_url(home_url('/contact/')); ?>">Book a Free Appraisal</a></div>
    </div>
  </div>
</section>

<?php get_footer(); ?>
