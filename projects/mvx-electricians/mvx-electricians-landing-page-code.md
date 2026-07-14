---
type: reference
tags: [mvx, landing-page, elementor]
updated: 2026-07-14
---

# MVX Electricians Landing Page — Final Code (shareable)

Residential electricians Google Ads landing page (gold-coast-electricians). Paste the ENTIRE code block below into the Elementor HTML widget, replacing anything already in it. Includes the theme link-colour guard, mobile optimisation, and the no-dash copy rules.

After pasting:
1. "Prefer we call you?" scrolls to `#form`. Give your Elementor form section the CSS ID `form` (section > Advanced > CSS ID).
2. Confirm the blue chip names row (City of Gold Coast / Gold Coast Airport / McDonald's) is fine to publish with Matt.

```html
<!DOCTYPE html>
<html lang="en-AU">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>Residential Electricians Gold Coast | MVX Electrical | Call 0427 593 990</title>
<meta name="robots" content="noindex, nofollow">
</head>
<body>

<!-- ════════════════════════════════════════════════════════════════
     COPY EVERYTHING BELOW THIS LINE INTO THE ELEMENTOR HTML WIDGET
     (fonts link + style block + all sections, ends after FAQ)
     ════════════════════════════════════════════════════════════════ -->

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=League+Gothic&family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">

<style>
/* MVX Residential Electricians Landing Page, per MVX Brand Guidelines v0.1.
   All rules scoped under .mvx-lp so nothing leaks into the WP theme. */
.mvx-lp{
  --mvx-green:#7EC004;
  --mvx-green-dark:#5E8519;
  --mvx-green-text:#4F7011; /* green for normal-size text on white, 5.7:1 */
  --mvx-black:#000000;
  --mvx-charcoal:#1a1a1a;
  --mvx-bg-deep:#0f0f0f;
  --mvx-bg-dark:#161616;
  --mvx-bg-mid:#1e1e1e;
  --mvx-white:#ffffff;
  --mvx-light-grey:#d8d8d8;
  --mvx-ink:#f4f4f4;
  --mvx-ink-2:#a8a8a8;
  --mvx-body-ink:#2b2b2b;
  --mvx-muted:#5e5e5e;
  --mvx-line-dark:rgba(255,255,255,0.1);
  --mvx-line-light:#e4e4e4;
  --mvx-r-sm:4px; --mvx-r-md:8px; --mvx-r-lg:12px;
  --mvx-shadow:0 4px 16px rgba(0,0,0,0.4);
  --mvx-display:'League Gothic','Arial Narrow',sans-serif;
  --mvx-sans:'Poppins',-apple-system,sans-serif;
  font-family:var(--mvx-sans);
  font-weight:400;
  font-size:16.5px;
  line-height:1.7;
  color:var(--mvx-body-ink);
  background:var(--mvx-white);
  -webkit-font-smoothing:antialiased;
}
.mvx-lp *,.mvx-lp *::before,.mvx-lp *::after{margin:0;padding:0;box-sizing:border-box}
.mvx-lp img{max-width:100%;display:block}
.mvx-lp p{text-wrap:pretty;max-width:68ch}
.mvx-wrap{width:min(1200px,92vw);margin-inline:auto}

/* Display headings: League Gothic, uppercase, per brand type scale */
.mvx-lp .mvx-h1,.mvx-lp .mvx-h2{font-family:var(--mvx-display);font-weight:400;text-transform:uppercase;line-height:0.95;letter-spacing:-1px;text-wrap:balance}
.mvx-lp .mvx-h1{font-size:clamp(3rem,2rem + 5.5vw,5.5rem);letter-spacing:-2px}
.mvx-lp .mvx-h2{font-size:clamp(2.1rem,1.6rem + 2.6vw,3.4rem)}
.mvx-lp h3{font-family:var(--mvx-sans);font-weight:600;line-height:1.3}

/* Buttons: green = CTA accent per brand, radius-md, no pills */
.mvx-btn-call{display:inline-flex;align-items:center;gap:.65rem;background:var(--mvx-green);color:var(--mvx-black);font-family:var(--mvx-sans);font-weight:700;text-decoration:none;padding:1rem 1.8rem;border-radius:var(--mvx-r-md);font-size:clamp(1.05rem,1rem + .3vw,1.25rem);box-shadow:var(--mvx-shadow);transition:background .2s cubic-bezier(0.4,0,0.2,1),transform .2s cubic-bezier(0.4,0,0.2,1)}
.mvx-btn-call:hover{background:var(--mvx-green-dark);color:var(--mvx-black);transform:translateY(-2px)}
.mvx-btn-call svg{flex:none}
.mvx-btn-call .mvx-sub{display:block;font-size:.72rem;font-weight:500;letter-spacing:.04em;opacity:.8}
.mvx-btn-ghost{display:inline-flex;align-items:center;gap:.5rem;color:var(--mvx-white);font-weight:500;text-decoration:none;padding:1rem 1.5rem;border-radius:var(--mvx-r-md);border:1px solid var(--mvx-line-dark);font-size:1rem;transition:border-color .2s,background .2s}
.mvx-btn-ghost:hover{border-color:var(--mvx-green);background:rgba(126,192,4,0.1);color:var(--mvx-white)}

/* Sticky mobile call bar */
.mvx-callbar{position:fixed;left:0;right:0;bottom:0;z-index:100;display:none;background:var(--mvx-black);border-top:2px solid var(--mvx-green);padding:.7rem .9rem calc(.7rem + env(safe-area-inset-bottom));gap:.6rem}
.mvx-callbar a{flex:1;justify-content:center;padding:.85rem 1rem;font-size:1.05rem;box-shadow:none}
@media(max-width:820px){.mvx-callbar{display:flex}.mvx-lp{padding-bottom:78px}}

/* Hero */
.mvx-hero{position:relative;background:var(--mvx-black);color:var(--mvx-white);overflow:hidden}
.mvx-hero::before{content:"";position:absolute;inset:0;background:url('https://mvxelectrical.com.au/wp-content/uploads/2026/04/MVX-Liversaver-14-scaled.jpg') center/cover no-repeat;opacity:.5}
.mvx-hero::after{content:"";position:absolute;inset:0;background:linear-gradient(90deg,rgba(0,0,0,0.94) 0%,rgba(0,0,0,0.82) 42%,rgba(0,0,0,0.35) 100%)}
.mvx-hero .mvx-wrap{position:relative;z-index:1;padding:clamp(3.5rem,8vw,6.5rem) 0 clamp(3rem,7vw,5.5rem)}
.mvx-hero-inner{max-width:660px}
.mvx-hero-rule{position:absolute;bottom:0;left:0;width:100%;height:3px;background:var(--mvx-green);z-index:2}
.mvx-rating{display:inline-flex;align-items:center;gap:.55rem;border:1px solid var(--mvx-line-dark);background:rgba(0,0,0,0.45);border-radius:var(--mvx-r-sm);padding:.45rem 1rem;font-size:.9rem;font-weight:500;color:var(--mvx-ink);margin-bottom:1.5rem}
.mvx-rating .mvx-stars{color:var(--mvx-green);letter-spacing:.1em;font-size:.95rem}
.mvx-hero .mvx-h1{color:var(--mvx-white);margin-bottom:1.1rem}
.mvx-hero .mvx-h1 span{color:var(--mvx-green)}
.mvx-hero .mvx-lede{color:var(--mvx-ink-2);font-weight:300;font-size:clamp(1.02rem,.95rem + .4vw,1.2rem);margin-bottom:2rem;max-width:54ch}
.mvx-ctas{display:flex;flex-wrap:wrap;gap:.9rem;align-items:center;margin-bottom:2.2rem}
.mvx-points{display:flex;flex-wrap:wrap;gap:.5rem 1.6rem;padding:0;list-style:none}
.mvx-points li{display:flex;align-items:center;gap:.5rem;color:var(--mvx-ink);font-size:.95rem;font-weight:400}
.mvx-points .mvx-tick{color:var(--mvx-green);font-weight:700}

/* Licence strip: black surface, green accents only (never green fill) */
.mvx-licences{background:var(--mvx-charcoal);color:var(--mvx-ink-2)}
.mvx-licences .mvx-wrap{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:.4rem 2rem;padding:.85rem 0;font-size:.88rem;font-weight:400}
.mvx-licences b{color:var(--mvx-green);font-weight:600}

/* Sections */
.mvx-sec{padding:clamp(3.2rem,7vw,5.5rem) 0}
.mvx-sec-head{max-width:760px;margin-bottom:clamp(2rem,4vw,3rem)}
.mvx-sec-head .mvx-h2{margin-bottom:.9rem;color:var(--mvx-charcoal)}
.mvx-sec-head p{color:var(--mvx-muted);font-size:1.05rem;font-weight:300}
.mvx-sec-dark{background:var(--mvx-bg-deep);color:var(--mvx-ink)}
.mvx-sec-dark .mvx-sec-head .mvx-h2,.mvx-sec-dark .mvx-h2{color:var(--mvx-white)}
.mvx-sec-dark .mvx-sec-head p{color:var(--mvx-ink-2)}

/* Services: 2x2 tiles */
.mvx-svc-list{display:grid;grid-template-columns:1fr 1fr;gap:1.25rem}
@media(max-width:760px){.mvx-svc-list{grid-template-columns:1fr}}
.mvx-svc{background:var(--mvx-white);border:1px solid var(--mvx-line-light);border-radius:var(--mvx-r-md);padding:1.9rem 1.8rem 1.7rem;display:flex;flex-direction:column;gap:.7rem;transition:box-shadow .2s,transform .2s}
.mvx-svc:hover{box-shadow:0 12px 32px rgba(0,0,0,0.12);transform:translateY(-3px)}
.mvx-svc h3{font-size:1.25rem;color:var(--mvx-charcoal)}
.mvx-svc p{color:var(--mvx-muted);font-size:.97rem;font-weight:300;flex:1}
.mvx-svc-cta{display:inline-flex;align-items:center;gap:.45rem;color:var(--mvx-charcoal);font-weight:600;text-decoration:none;font-size:.98rem;margin-top:.1rem;padding:.7rem 0;margin-bottom:-.4rem}
.mvx-svc-cta .mvx-num{color:var(--mvx-green-text)}
.mvx-svc-cta:hover .mvx-num{text-decoration:underline}
.mvx-svc-icon{width:46px;height:46px;border-radius:var(--mvx-r-md);background:var(--mvx-charcoal);display:grid;place-items:center;color:var(--mvx-green)}

/* CTA band */
.mvx-band{background:var(--mvx-black);color:var(--mvx-white);text-align:center}
.mvx-band .mvx-h2{color:var(--mvx-white);margin-bottom:.8rem}
.mvx-band p{color:var(--mvx-ink-2);font-weight:300;margin:0 auto 1.8rem;font-size:1.05rem}
.mvx-band .mvx-ctas{justify-content:center;margin-bottom:0}

/* Why MVX */
.mvx-why .mvx-wrap{display:grid;grid-template-columns:1.05fr .95fr;gap:clamp(2rem,5vw,4.5rem);align-items:center}
@media(max-width:900px){.mvx-why .mvx-wrap{grid-template-columns:1fr}}
.mvx-why-img{border-radius:var(--mvx-r-lg);overflow:hidden;box-shadow:var(--mvx-shadow);position:relative}
.mvx-why-img img{width:100%;height:100%;object-fit:cover;min-height:420px}
@media(max-width:900px){.mvx-why-img img{min-height:280px}}
.mvx-why-img .mvx-img-tag{position:absolute;left:1.1rem;bottom:1.1rem;background:rgba(0,0,0,0.85);color:var(--mvx-white);font-size:.82rem;font-weight:500;padding:.5rem .95rem;border-radius:var(--mvx-r-sm);border-left:none}
.mvx-why .mvx-h2{color:var(--mvx-charcoal);margin-bottom:1.2rem}
.mvx-diff{display:flex;gap:1rem;padding:1.15rem 0;border-bottom:1px solid var(--mvx-line-light)}
.mvx-diff:last-of-type{border-bottom:0}
.mvx-diff-n{flex:none;width:40px;height:40px;border-radius:var(--mvx-r-md);background:var(--mvx-black);color:var(--mvx-green);display:grid;place-items:center;font-weight:700;font-size:1rem}
.mvx-diff h3{font-size:1.08rem;color:var(--mvx-charcoal);margin-bottom:.25rem}
.mvx-diff p{color:var(--mvx-muted);font-size:.96rem;font-weight:300}
.mvx-diff p strong{color:var(--mvx-charcoal);font-weight:600}
.mvx-why .mvx-btn-call{margin-top:1.6rem}

/* Steps */
.mvx-steps{background:var(--mvx-bg-deep)}
.mvx-step-row{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:1.25rem;counter-reset:mvxstep}
.mvx-step{background:var(--mvx-bg-mid);border:1px solid var(--mvx-line-dark);border-radius:var(--mvx-r-md);padding:1.8rem 1.7rem}
.mvx-step::before{counter-increment:mvxstep;content:counter(mvxstep);display:inline-block;font-family:var(--mvx-display);font-size:3rem;line-height:1;color:rgba(126,192,4,0.4);margin-bottom:.8rem}
.mvx-step h3{font-size:1.12rem;color:var(--mvx-white);margin-bottom:.35rem}
.mvx-step p{color:var(--mvx-ink-2);font-size:.96rem;font-weight:300}

/* Reviews */
.mvx-rev-head{display:flex;flex-wrap:wrap;align-items:end;justify-content:space-between;gap:1rem;margin-bottom:2.2rem}
.mvx-gbadge{display:flex;align-items:center;gap:.9rem;background:var(--mvx-black);border-radius:var(--mvx-r-md);padding:.9rem 1.3rem}
.mvx-gbadge .mvx-score{font-family:var(--mvx-display);font-size:2.6rem;color:var(--mvx-white);line-height:1}
.mvx-gbadge .mvx-stars{color:var(--mvx-green);font-size:1rem;letter-spacing:.08em}
.mvx-gbadge small{display:block;color:var(--mvx-ink-2);font-size:.8rem;font-weight:300}
.mvx-rev-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:1.25rem}
.mvx-rev{background:var(--mvx-white);border:1px solid var(--mvx-line-light);border-radius:var(--mvx-r-md);padding:1.7rem 1.6rem;display:flex;flex-direction:column;gap:.8rem}
.mvx-rev .mvx-stars{color:var(--mvx-green-text);letter-spacing:.1em}
.mvx-rev p{font-size:.95rem;font-weight:300;color:var(--mvx-body-ink)}
.mvx-rev cite{font-style:normal;font-weight:600;color:var(--mvx-charcoal);font-size:.92rem;margin-top:auto}
.mvx-rev cite small{display:block;font-weight:300;color:var(--mvx-muted)}

/* Brands */
.mvx-brands{background:var(--mvx-black);color:var(--mvx-white);text-align:center;padding:2.8rem 0}
.mvx-brands p{margin:0 auto .9rem;color:var(--mvx-ink-2);font-size:.8rem;font-weight:500;letter-spacing:2.5px;text-transform:uppercase}
.mvx-brands .mvx-row{display:flex;flex-wrap:wrap;justify-content:center;gap:.4rem 2.6rem;font-family:var(--mvx-display);text-transform:uppercase;font-size:clamp(1.3rem,1.1rem + 1vw,1.9rem);color:var(--mvx-white);opacity:.92}
.mvx-brands .mvx-row span{white-space:nowrap}

/* Areas */
.mvx-chip-row{display:flex;flex-wrap:wrap;gap:.55rem}
.mvx-chip{background:var(--mvx-white);border:1px solid var(--mvx-line-light);border-radius:var(--mvx-r-sm);padding:.42rem 1rem;font-size:.9rem;font-weight:400;color:var(--mvx-body-ink)}
.mvx-chip-green{background:var(--mvx-green);border-color:var(--mvx-green);color:var(--mvx-black);font-weight:600}
.mvx-areas{background:#f5f5f5}

/* FAQ */
.mvx-faq{background:var(--mvx-bg-deep)}
.mvx-faq .mvx-wrap{max-width:840px}
.mvx-faq details{background:var(--mvx-bg-mid);border:1px solid var(--mvx-line-dark);border-radius:var(--mvx-r-md);margin-bottom:.7rem;overflow:hidden}
.mvx-faq summary{cursor:pointer;font-weight:600;color:var(--mvx-white);padding:1.15rem 1.4rem;list-style:none;display:flex;justify-content:space-between;align-items:center;gap:1rem;font-size:1.02rem}
.mvx-faq summary::-webkit-details-marker{display:none}
.mvx-faq summary::after{content:"+";font-size:1.5rem;font-weight:300;color:var(--mvx-green);transition:transform .2s}
.mvx-faq details[open] summary::after{transform:rotate(45deg)}
.mvx-faq details p{padding:0 1.4rem 1.25rem;color:var(--mvx-ink-2);font-weight:300;font-size:.97rem}

/* Touch devices: no hover-dependent motion, give active feedback instead */
@media (hover:none){
  .mvx-btn-call:hover{transform:none;background:var(--mvx-green);color:var(--mvx-black)}
  .mvx-btn-call:active{background:var(--mvx-green-dark);color:var(--mvx-black)}
  .mvx-svc:hover{transform:none;box-shadow:none}
  .mvx-svc:active{box-shadow:0 6px 18px rgba(0,0,0,0.12)}
}

/* Mobile (ads traffic is thumb-first) */
@media (max-width:640px){
  .mvx-lp{font-size:16px}
  .mvx-hero .mvx-wrap{padding:2.6rem 0 2.4rem}
  /* text spans full width on mobile: one solid legibility layer instead of a side gradient */
  .mvx-hero::after{background:linear-gradient(180deg,rgba(0,0,0,0.88) 0%,rgba(0,0,0,0.8) 100%)}
  .mvx-hero .mvx-h1{font-size:clamp(2.7rem,14vw,3.4rem)}
  .mvx-rating{font-size:.82rem;padding:.4rem .8rem;margin-bottom:1.1rem}
  .mvx-hero .mvx-lede{margin-bottom:1.5rem}
  .mvx-ctas{flex-direction:column;align-items:stretch;gap:.7rem;margin-bottom:1.7rem}
  .mvx-btn-call,.mvx-btn-ghost{width:100%;justify-content:center;text-align:center}
  .mvx-points{flex-direction:column;gap:.55rem}
  .mvx-licences .mvx-wrap{flex-direction:column;align-items:flex-start;gap:.3rem;padding:1rem 0;font-size:.84rem}
  .mvx-sec-head{margin-bottom:1.6rem}
  .mvx-svc{padding:1.5rem 1.35rem 1.35rem}
  .mvx-step{padding:1.5rem 1.35rem}
  .mvx-step::before{font-size:2.4rem;margin-bottom:.5rem}
  .mvx-rev-head{flex-direction:column;align-items:flex-start;gap:1.2rem;margin-bottom:1.6rem}
  .mvx-rev{padding:1.4rem 1.3rem}
  .mvx-why-img .mvx-img-tag{font-size:.78rem;left:.8rem;bottom:.8rem}
  .mvx-brands{padding:2.2rem 0}
  .mvx-brands .mvx-row{gap:.3rem 1.6rem}
  .mvx-faq summary{padding:1rem 1.1rem;font-size:.98rem}
  .mvx-faq details p{padding:0 1.1rem 1.1rem}
}

/* Keyboard focus: visible on both light and dark surfaces */
.mvx-lp a:focus-visible,.mvx-lp summary:focus-visible{outline:2px solid var(--mvx-green);outline-offset:2px;border-radius:var(--mvx-r-sm)}
.mvx-sec:not(.mvx-sec-dark) a:focus-visible{outline-color:var(--mvx-green-text)}

@media (prefers-reduced-motion:reduce){
  .mvx-lp *,.mvx-lp *::before,.mvx-lp *::after{transition:none !important;animation:none !important}
}

/* WordPress/Elementor override guard: the theme's global link colour
   (green a{}) outranks widget styles, so pin every link colour here. */
.mvx-lp a{text-decoration:none !important}
.mvx-lp a.mvx-btn-call,.mvx-lp a.mvx-btn-call span,.mvx-lp a.mvx-btn-call:hover,.mvx-lp a.mvx-btn-call:active{color:var(--mvx-black) !important}
.mvx-lp a.mvx-btn-ghost,.mvx-lp a.mvx-btn-ghost:hover{color:var(--mvx-white) !important}
.mvx-lp a.mvx-svc-cta{color:var(--mvx-charcoal) !important}
.mvx-lp a.mvx-svc-cta .mvx-num{color:var(--mvx-green-text) !important}
.mvx-lp .mvx-callbar a.mvx-btn-call{color:var(--mvx-black) !important}
</style>

<div class="mvx-lp">

<!-- Sticky mobile call bar -->
<div class="mvx-callbar" aria-label="Quick contact">
  <a class="mvx-btn-call" href="tel:0427593990">
    <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M6.6 10.8c1.4 2.8 3.8 5.1 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1C10.6 21 3 13.4 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.2.2 2.4.6 3.6.1.3 0 .7-.2 1l-2.3 2.2z"/></svg>
    Call 0427 593 990
  </a>
</div>

<!-- HERO -->
<section class="mvx-hero">
  <div class="mvx-wrap">
    <div class="mvx-hero-inner">
      <span class="mvx-rating"><span class="mvx-stars" aria-hidden="true">★★★★★</span> 4.9 / 5 on Google from Gold Coast locals</span>
      <h1 class="mvx-h1">Residential Electricians, <span>Gold Coast</span></h1>
      <p class="mvx-lede">Power tripping, lights out, or planning a reno? We're local licensed electricians with 15+ years on Gold Coast homes and blue chip sites. One call and it's sorted.</p>
      <div class="mvx-ctas">
        <a class="mvx-btn-call" href="tel:0427593990">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M6.6 10.8c1.4 2.8 3.8 5.1 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1C10.6 21 3 13.4 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.2.2 2.4.6 3.6.1.3 0 .7-.2 1l-2.3 2.2z"/></svg>
          <span>Call now: 0427 593 990<span class="mvx-sub">Talk to a real local electrician</span></span>
        </a>
        <a class="mvx-btn-ghost" href="#form">Prefer we call you? ↓</a>
      </div>
      <ul class="mvx-points">
        <li><span class="mvx-tick">✓</span> Same day and emergency response</li>
        <li><span class="mvx-tick">✓</span> Upfront pricing before we start</li>
        <li><span class="mvx-tick">✓</span> Fully licensed and insured, 15+ years</li>
        <li><span class="mvx-tick">✓</span> No job too small, no job too big</li>
      </ul>
    </div>
  </div>
  <div class="mvx-hero-rule" aria-hidden="true"></div>
</section>

<!-- Licence strip -->
<div class="mvx-licences" role="note">
  <div class="mvx-wrap">
    <span>QLD Electrical Licence <b>87592</b></span>
    <span>NSW Contractor <b>483405C</b></span>
    <span>ARC Licence <b>L198354</b></span>
    <span>Fully insured, certificate of compliance on every job</span>
  </div>
</div>

<!-- SERVICES (2x2) -->
<section class="mvx-sec" id="mvx-services">
  <div class="mvx-wrap">
    <div class="mvx-sec-head">
      <h2 class="mvx-h2">Home electrical services, all handled by one crew</h2>
      <p>From a single power point to a full renovation rewire. The same licensed team that works on council and airport sites handles your home, and we treat both with the same care.</p>
    </div>
    <div class="mvx-svc-list">
      <article class="mvx-svc">
        <div class="mvx-svc-icon" aria-hidden="true"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><rect x="3" y="5" width="18" height="8" rx="2"/><path d="M7 17c0 1.5-1 2-1 3M12 17c0 1.5-1 2-1 3M17 17c0 1.5-1 2-1 3"/></svg></div>
        <h3>Lighting &amp; Power</h3>
        <p>LED downlights, ceiling fans, power points, USB outlets, outdoor and garden lighting. Installed neatly, positioned properly, and certified.</p>
        <a class="mvx-svc-cta" href="tel:0427593990">Book it in → <span class="mvx-num">0427 593 990</span></a>
      </article>
      <article class="mvx-svc">
        <div class="mvx-svc-icon" aria-hidden="true"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14.7 6.3a5 5 0 0 0-6.6 6.6L3 18v3h3l5.1-5.1a5 5 0 0 0 6.6-6.6L14 12l-2-2 2.7-3.7z"/></svg></div>
        <h3>Repairs &amp; Fault Finding</h3>
        <p>Tripping breakers, dead outlets, flickering lights, burning smells. We find the fault fast and fix it properly the first time, with emergency response when it can't wait.</p>
        <a class="mvx-svc-cta" href="tel:0427593990">Get it fixed today → <span class="mvx-num">0427 593 990</span></a>
      </article>
      <article class="mvx-svc">
        <div class="mvx-svc-icon" aria-hidden="true"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12a9 9 0 1 1-9-9"/><path d="M21 3v6h-6"/></svg></div>
        <h3>Switchboard &amp; Safety</h3>
        <p>Switchboard upgrades, safety switches, smoke alarms and safety inspections. The stuff that protects your family and keeps an older home compliant.</p>
        <a class="mvx-svc-cta" href="tel:0427593990">Book an inspection → <span class="mvx-num">0427 593 990</span></a>
      </article>
      <article class="mvx-svc">
        <div class="mvx-svc-icon" aria-hidden="true"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 21V8l9-5 9 5v13"/><path d="M9 21v-6h6v6"/></svg></div>
        <h3>Renos, New Builds &amp; EV</h3>
        <p>Renovation wiring, extensions, new builds, EV chargers, solar and battery. Planned with you up front so the electrical work never holds the project up.</p>
        <a class="mvx-svc-cta" href="tel:0427593990">Talk it through → <span class="mvx-num">0427 593 990</span></a>
      </article>
    </div>
  </div>
</section>

<!-- CTA band -->
<section class="mvx-sec mvx-band">
  <div class="mvx-wrap">
    <h2 class="mvx-h2">Got an electrical job at home?</h2>
    <p>Call and talk to a local electrician, not a call centre. Most Gold Coast jobs get a same day response.</p>
    <div class="mvx-ctas">
      <a class="mvx-btn-call" href="tel:0427593990">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M6.6 10.8c1.4 2.8 3.8 5.1 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1C10.6 21 3 13.4 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.2.2 2.4.6 3.6.1.3 0 .7-.2 1l-2.3 2.2z"/></svg>
        Call 0427 593 990
      </a>
    </div>
  </div>
</section>

<!-- WHY MVX -->
<section class="mvx-sec mvx-why">
  <div class="mvx-wrap">
    <div class="mvx-why-img">
      <img src="https://mvxelectrical.com.au/wp-content/uploads/2026/04/MVX-Liversaver-11-scaled.jpg" alt="Matt, Director of MVX Electrical, on site on the Gold Coast" loading="lazy" decoding="async" width="2560" height="1707">
      <span class="mvx-img-tag">Meet Matt, MVX Director</span>
    </div>
    <div>
      <h2 class="mvx-h2">Why locals keep MVX in their phone</h2>
      <div class="mvx-diff">
        <span class="mvx-diff-n" aria-hidden="true">⚡</span>
        <div>
          <h3>Blue chip standards, home job care</h3>
          <p>15+ years across commercial, council and construction sites, including the City of Gold Coast and Gold Coast Airport. Your home gets the <strong>same standard of work</strong> those sites demand.</p>
        </div>
      </div>
      <div class="mvx-diff">
        <span class="mvx-diff-n" aria-hidden="true">$</span>
        <div>
          <h3>Upfront price before we start</h3>
          <p>A clear quote before any work begins. No surprises, no pressure, and honest advice on repair vs replace.</p>
        </div>
      </div>
      <div class="mvx-diff">
        <span class="mvx-diff-n" aria-hidden="true">✓</span>
        <div>
          <h3>Done right, certified, guaranteed</h3>
          <p>Fully licensed and insured. Every job to Australian Standard with a certificate of compliance, backed by our workmanship guarantee.</p>
        </div>
      </div>
      <a class="mvx-btn-call" href="tel:0427593990">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M6.6 10.8c1.4 2.8 3.8 5.1 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1C10.6 21 3 13.4 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.2.2 2.4.6 3.6.1.3 0 .7-.2 1l-2.3 2.2z"/></svg>
        Call 0427 593 990
      </a>
    </div>
  </div>
</section>

<!-- STEPS -->
<section class="mvx-sec mvx-steps mvx-sec-dark">
  <div class="mvx-wrap">
    <div class="mvx-sec-head">
      <h2 class="mvx-h2">Sorted in three steps</h2>
    </div>
    <div class="mvx-step-row">
      <div class="mvx-step">
        <h3>Call us</h3>
        <p>Tell us what's going on. We'll ask a few quick questions and give you a straight answer on what it needs.</p>
      </div>
      <div class="mvx-step">
        <h3>Fixed price, fast booking</h3>
        <p>You get an upfront quote and a booking. Same day for most repairs and faults, fast turnaround on bigger jobs.</p>
      </div>
      <div class="mvx-step">
        <h3>Job done, certified</h3>
        <p>We do the job properly, clean up after ourselves, and hand over your certificate of compliance.</p>
      </div>
    </div>
  </div>
</section>

<!-- REVIEWS -->
<section class="mvx-sec" id="mvx-reviews">
  <div class="mvx-wrap">
    <div class="mvx-rev-head">
      <div class="mvx-sec-head" style="margin-bottom:0">
        <h2 class="mvx-h2">Trusted by Gold Coast homes &amp; businesses</h2>
      </div>
      <div class="mvx-gbadge">
        <span class="mvx-score">4.9</span>
        <div>
          <span class="mvx-stars" aria-hidden="true">★★★★★</span>
          <small>Google rating from Gold Coast locals</small>
        </div>
      </div>
    </div>
    <div class="mvx-rev-grid">
      <article class="mvx-rev">
        <span class="mvx-stars" aria-hidden="true">★★★★★</span>
        <p>"Matt has fixed a few electrical problems at our place over the past year, from a burned out wire to checking all the electrical work after flooding. Friendly, punctual, clean and tidy, and always happy to provide advice."</p>
        <cite>Elizabeth G. <small>Gold Coast homeowner</small></cite>
      </article>
      <article class="mvx-rev">
        <span class="mvx-stars" aria-hidden="true">★★★★★</span>
        <p>"Very professional, calm, reliable and attentive. I needed his help twice during emergencies and he arrived instantly to make sure we were safe. He knows his expertise and treats his customers fairly."</p>
        <cite>Lisa W. <small>Gold Coast</small></cite>
      </article>
      <article class="mvx-rev">
        <span class="mvx-stars" aria-hidden="true">★★★★★</span>
        <p>"We've used Matt on our existing home, two previous homes and an investment property over the last 5 to 6 years. Great electrician: reliable, honest, well priced and gets the job done."</p>
        <cite>Google review <small>Repeat client, 5+ years</small></cite>
      </article>
    </div>
  </div>
</section>

<!-- BRANDS -->
<section class="mvx-brands">
  <div class="mvx-wrap">
    <p>Trusted on blue chip sites across the Gold Coast</p>
    <div class="mvx-row">
      <span>City of Gold Coast</span><span>Gold Coast Airport</span><span>McDonald's</span>
    </div>
  </div>
</section>

<!-- AREAS -->
<section class="mvx-sec mvx-areas">
  <div class="mvx-wrap">
    <div class="mvx-sec-head">
      <h2 class="mvx-h2">Servicing the whole Gold Coast &amp; Northern NSW</h2>
      <p>Based locally, so "we'll be there soon" actually means soon.</p>
    </div>
    <div class="mvx-chip-row">
      <span class="mvx-chip">Burleigh Heads</span><span class="mvx-chip">Palm Beach</span><span class="mvx-chip">Currumbin</span><span class="mvx-chip">Tallebudgera</span><span class="mvx-chip">Robina</span><span class="mvx-chip">Mermaid Waters</span><span class="mvx-chip">Broadbeach</span><span class="mvx-chip">Nerang</span><span class="mvx-chip">Southport</span><span class="mvx-chip">Ashmore</span><span class="mvx-chip">Helensvale</span><span class="mvx-chip">Coomera</span><span class="mvx-chip">Beenleigh</span><span class="mvx-chip">Tweed Heads</span><span class="mvx-chip">Casuarina</span><span class="mvx-chip">Kingscliff</span><span class="mvx-chip mvx-chip-green">and surrounding areas</span>
    </div>
  </div>
</section>

<!-- FAQ (final section) -->
<section class="mvx-sec mvx-faq mvx-sec-dark">
  <div class="mvx-wrap">
    <div class="mvx-sec-head">
      <h2 class="mvx-h2">Quick answers</h2>
    </div>
    <details>
      <summary>How fast can you get to me?</summary>
      <p>We're based on the Gold Coast and prioritise faults that leave you without power or feel unsafe. Most calls get a same day response. Call 0427 593 990 and we'll give you an honest ETA on the spot.</p>
    </details>
    <details>
      <summary>Are you licensed and insured?</summary>
      <p>Yes. QLD Electrical Licence 87592, NSW Contractor Licence 483405C, fully insured, and every job comes with a certificate of compliance. 15+ years across residential, commercial and council work.</p>
    </details>
    <details>
      <summary>Do you take on small jobs?</summary>
      <p>Yes. A single power point, a ceiling fan, one flickering light. No job too small, and you get the same upfront price and tidy finish as a full renovation.</p>
    </details>
    <details>
      <summary>What does an electrician cost?</summary>
      <p>It depends on the job, but you'll always get a fixed upfront price before we start. No hourly surprises, no hidden extras on the invoice.</p>
    </details>
    <details>
      <summary>Can you handle renovations and new builds?</summary>
      <p>Yes. We work with builders and owners on renovations, extensions and new builds across the Gold Coast and Northern NSW, from first fix to final certification.</p>
    </details>
    <details>
      <summary>What if something goes wrong after hours?</summary>
      <p>Call us. Genuine electrical emergencies get priority, and we'll tell you straight over the phone whether it's safe to wait or needs someone now.</p>
    </details>
  </div>
</section>

</div><!-- /.mvx-lp -->

<!-- ════════════════════════════════════════════════════════════════
     END OF ELEMENTOR COPY REGION
     Hunter adds his own WordPress form section below this in Elementor.
     ════════════════════════════════════════════════════════════════ -->

</body>
</html>
```
