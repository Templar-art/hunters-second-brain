<?php if (!defined('ABSPATH')) exit; get_header(); ?>

<section class="page-hero">
  <div class="wrap">
    <span class="eyebrow on-dark">Recent Results</span>
    <h1>Sold Listings</h1>
    <p class="maxw-prose">The visual proof of what Bespoke delivers. A closer look at the homes we have taken to market, presented the way prestige property deserves to be seen.</p>
  </div>
</section>

<!-- THE BOULEVARD -->
<section class="section">
  <div class="wrap">
    <div class="split split--media-right reveal">
      <div>
        <span class="property__tag" style="position:static;display:inline-block;margin-bottom:16px">Sold</span>
        <h2>The Boulevard</h2>
        <p class="lead mt-md">A striking waterfront residence in a tightly held riverside enclave. Captured at golden hour from the air, with light filled, indoor to outdoor living at its heart.</p>
        <div class="stats mt-lg" style="background:var(--be-grey-200);border-color:var(--be-grey-200)">
          <div class="stat" style="background:var(--be-green)"><b>4</b><span>Bedrooms</span></div>
          <div class="stat" style="background:var(--be-green)"><b>3</b><span>Bathrooms</span></div>
          <div class="stat" style="background:var(--be-green)"><b>2</b><span>Car</span></div>
          <div class="stat" style="background:var(--be-green)"><b>River</b><span>Frontage</span></div>
        </div>
      </div>
      <div class="split__media"><img src="<?php echo esc_url(bea_asset('boulevard-01.jpg')); ?>" alt="The Boulevard waterfront residence at sunset" loading="lazy"></div>
    </div>
    <div class="gallery mt-2xl reveal">
      <?php echo bea_gallery('boulevard', 5, array('boulevard-location.jpg')); ?>
    </div>
  </div>
</section>

<!-- 11 CAIRNGORM STREET -->
<section class="section section--offwhite">
  <div class="wrap">
    <div class="split reveal">
      <div class="split__media"><img src="<?php echo esc_url(bea_asset('cairngorm-01.jpg')); ?>" alt="11 Cairngorm Street at twilight" loading="lazy"></div>
      <div>
        <span class="property__tag" style="position:static;display:inline-block;margin-bottom:16px">Sold</span>
        <h2>11 Cairngorm Street</h2>
        <p class="lead mt-md">A light filled, two storey family home framed by established gardens. Styled, photographed at golden hour, and taken to market at its full potential.</p>
        <div class="stats mt-lg" style="background:var(--be-grey-300);border-color:var(--be-grey-300)">
          <div class="stat" style="background:var(--be-green)"><b>4</b><span>Bedrooms</span></div>
          <div class="stat" style="background:var(--be-green)"><b>2</b><span>Bathrooms</span></div>
          <div class="stat" style="background:var(--be-green)"><b>2</b><span>Car</span></div>
          <div class="stat" style="background:var(--be-green)"><b>14d</b><span>To Sold</span></div>
        </div>
      </div>
    </div>
    <div class="gallery mt-2xl reveal">
      <?php echo bea_gallery('cairngorm', 19); ?>
    </div>
  </div>
</section>

<!-- 43 NORTHVIEW -->
<section class="section">
  <div class="wrap">
    <div class="split split--media-right reveal">
      <div>
        <span class="property__tag" style="position:static;display:inline-block;margin-bottom:16px">Sold</span>
        <h2>43 Northview</h2>
        <p class="lead mt-md">A waterfront position on the marina, captured from the ground and the air to tell the full story of the home and its setting.</p>
        <div class="stats mt-lg" style="background:var(--be-grey-200);border-color:var(--be-grey-200)">
          <div class="stat" style="background:var(--be-green)"><b>5</b><span>Bedrooms</span></div>
          <div class="stat" style="background:var(--be-green)"><b>3</b><span>Bathrooms</span></div>
          <div class="stat" style="background:var(--be-green)"><b>2</b><span>Car</span></div>
          <div class="stat" style="background:var(--be-green)"><b>Water</b><span>Frontage</span></div>
        </div>
      </div>
      <div class="split__media"><img src="<?php echo esc_url(bea_asset('northview-04.jpg')); ?>" alt="43 Northview waterfront residence" loading="lazy"></div>
    </div>
    <div class="gallery mt-2xl reveal">
      <?php echo bea_gallery('northview', 40); ?>
    </div>
  </div>
</section>

<section class="page-hero has-img">
  <div class="page-hero__media"><img src="<?php echo esc_url(bea_asset('cairngorm-08.jpg')); ?>" alt="Gold Coast home" loading="lazy"></div>
  <div class="wrap"><div class="maxw-prose reveal">
    <h1>Your home could be next.</h1>
    <p>See what a considered campaign and the right agent can do. Book a free appraisal today.</p>
    <div class="btn-row mt-lg"><a class="btn btn--light" href="<?php echo esc_url(home_url('/contact/')); ?>">Book a Free Appraisal</a></div>
  </div></div>
</section>

<?php get_footer(); ?>
