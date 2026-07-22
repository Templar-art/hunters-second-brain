/* ==========================================================================
   BESPOKE — prototype app logic
   - Data-access layer (getListings/getListing/getRegions/...) is the ONLY seam
     that touches data. Swap its body for Payload/WP fetch; UI is untouched.
   - Filtering mirrors BUILD-SPEC §7 (URL-synced, status->data map, min-semantics).
   - Motion is progressive: content is visible by default; reveal only enhances.
   ========================================================================== */
(function () {
  "use strict";
  var D = window.BESPOKE_DATA;

  /* ----------------------------- DATA ACCESS ----------------------------- */
  // Replace these four bodies with real fetches later. Signatures stay fixed.
  function getRegions() { return D.REGIONS.slice(); }
  function getRegion(slug) { return D.REGIONS.filter(function (r) { return r.slug === slug; })[0] || null; }
  function getAgent(id) { return D.AGENTS[id] || null; }
  function getListing(slug) { return D.LISTINGS.filter(function (l) { return l.slug === slug; })[0] || null; }

  function getListings(f) {
    f = f || {};
    var statusMap = { buy: ["for_sale", "under_offer"], sold: ["sold"], upcoming: ["upcoming"] };
    var allowed = statusMap[f.status || "buy"];
    var out = D.LISTINGS.filter(function (l) {
      if (allowed.indexOf(l.status) === -1) return false;
      if (f.suburb && l.address.suburb !== f.suburb) return false;
      if (f.type && l.propertyType !== f.type) return false;
      if (f.beds && l.beds < f.beds) return false;
      if (f.baths && l.baths < f.baths) return false;
      if (f.cars && l.cars < f.cars) return false;
      // Price range applies to numeric prices only; EOI/POA/contact always pass
      // (prestige listings frequently have no published number).
      if (l.price.display === "numeric") {
        if (f.pmin && l.price.amount < f.pmin) return false;
        if (f.pmax && l.price.amount > f.pmax) return false;
      }
      return true;
    });
    // Sort: sold by most recent; others by price desc (numeric first).
    out.sort(function (a, b) {
      if ((f.status || "buy") === "sold") {
        return (b.soldData ? b.soldData.date : "").localeCompare(a.soldData ? a.soldData.date : "");
      }
      var pa = a.price.amount || 0, pb = b.price.amount || 0;
      return pb - pa;
    });
    return out;
  }

  /* ------------------------------- HELPERS ------------------------------- */
  var AUD = new Intl.NumberFormat("en-AU", { style: "currency", currency: "AUD", maximumFractionDigits: 0 });
  function suburbName(slug) { var r = getRegion(slug); return r ? r.name : slug; }
  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) { return ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c]; }); }

  function priceLine(l) {
    if (l.status === "sold") return "Sold";
    if (l.status === "upcoming") return "Coming soon";
    if (l.status === "under_offer") return "Under offer";
    switch (l.price.display) {
      case "numeric": return AUD.format(l.price.amount);
      case "eoi": return l.price.label || "Expressions of Interest";
      case "poa": return "Price on application";
      default: return "Contact agent";
    }
  }
  function markerFor(l) {
    if (l.status === "sold") return l.soldData && l.soldData.suburbRecord
      ? { cls: "marker--record", txt: "Suburb Record" } : { cls: "marker--muted", txt: "Sold" };
    if (l.status === "under_offer") return { cls: "", txt: "Under Offer" };
    if (l.status === "upcoming") return { cls: "", txt: "Coming Soon" };
    return null;
  }
  var ICON = { bed: "../assets/icons/Bed.svg", bath: "../assets/icons/Shower.svg", car: "../assets/icons/Car.svg" };
  function metaRow(l) {
    return '<span class="p-meta-i"><img src="' + ICON.bed + '" alt="">' + l.beds + '</span>' +
           '<span class="p-meta-i"><img src="' + ICON.bath + '" alt="">' + l.baths + '</span>' +
           '<span class="p-meta-i"><img src="' + ICON.car + '" alt="">' + l.cars + '</span>' +
           (l.landSize ? '<span class="p-meta-i">' + l.landSize + ' m²</span>' : "");
  }

  /* ---------------------------- PROPERTY CARD ---------------------------- */
  function cardHTML(l, delay) {
    var m = markerFor(l);
    var sold = l.status === "sold";
    return '<a class="p-card reveal"' + (delay ? ' data-d="' + delay + '"' : "") +
      ' href="listing.html?id=' + encodeURIComponent(l.slug) + '">' +
      '<div class="p-card__media' + (sold ? " is-sold" : "") + '">' +
        (m ? '<span class="marker ' + m.cls + '">' + m.txt + '</span>' : "") +
        '<img src="' + l.hero.url + '" alt="' + esc(l.hero.alt) + '" loading="lazy">' +
      '</div>' +
      '<div class="p-card__body">' +
        '<div class="p-card__suburb">' + esc(suburbName(l.address.suburb)) + '</div>' +
        '<div class="p-card__addr">' + esc(l.address.street) + '</div>' +
        '<div class="p-card__meta">' + metaRow(l) + '</div>' +
        '<div class="p-card__price">' + esc(priceLine(l)) + '</div>' +
      '</div></a>';
  }

  /* ------------------------------ REVEAL --------------------------------- */
  var io = null;
  function initReveal() {
    var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (reduce || !("IntersectionObserver" in window)) return; // content already visible
    document.documentElement.classList.add("reveal-on");
    io = new IntersectionObserver(function (ents) {
      ents.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } });
    }, { rootMargin: "0px 0px -8% 0px" });
    observeReveals();
    // Failsafe: never leave content hidden if the observer never fires.
    setTimeout(function () {
      document.querySelectorAll(".reveal:not(.in)").forEach(function (el) { el.classList.add("in"); });
    }, 1600);
  }
  function observeReveals() {
    if (!io) return;
    document.querySelectorAll(".reveal:not(.in)").forEach(function (el) { io.observe(el); });
  }

  /* --------------------------- HEADER / CHROME --------------------------- */
  function initChrome() {
    var header = document.querySelector(".site-header");
    if (header) {
      var onScroll = function () { header.classList.toggle("scrolled", window.scrollY > 24); };
      onScroll(); window.addEventListener("scroll", onScroll, { passive: true });
    }
    var toggle = document.querySelector(".menu-toggle");
    var menu = document.getElementById("site-menu");
    if (toggle && menu) {
      var setOpen = function (open) {
        menu.classList.toggle("open", open);
        toggle.setAttribute("aria-expanded", open ? "true" : "false");
        document.body.style.overflow = open ? "hidden" : "";
      };
      toggle.addEventListener("click", function () { setOpen(!menu.classList.contains("open")); });
      menu.addEventListener("click", function (e) { if (e.target.tagName === "A" || e.target === menu) setOpen(false); });
      document.addEventListener("keydown", function (e) { if (e.key === "Escape") setOpen(false); });
    }
    var yr = document.querySelector("[data-year]"); if (yr) yr.textContent = new Date().getFullYear();
  }

  /* --------------------------- LISTINGS PAGE ----------------------------- */
  function readFilterFromURL() {
    var q = new URLSearchParams(location.search);
    var num = function (k) { var v = parseInt(q.get(k), 10); return isNaN(v) ? null : v; };
    return {
      status: q.get("status") || "buy",
      suburb: q.get("suburb") || null,
      type: q.get("type") || null,
      beds: num("beds"), baths: num("baths"), cars: num("cars"),
      pmin: num("pmin"), pmax: num("pmax")
    };
  }
  function writeFilterToURL(f) {
    var q = new URLSearchParams();
    Object.keys(f).forEach(function (k) { if (f[k] !== null && f[k] !== "" && !(k === "status" && f[k] === "buy")) q.set(k, f[k]); });
    var s = q.toString();
    history.replaceState(null, "", s ? "?" + s : location.pathname);
  }

  function initListings() {
    var root = document.getElementById("listings");
    if (!root) return;
    var grid = document.getElementById("listings-grid");
    var count = document.getElementById("fb-count");
    var clearBtn = document.getElementById("fb-clear");
    var tabs = root.querySelectorAll(".fb-tab");
    var fields = root.querySelectorAll(".fb-field select");
    var state = readFilterFromURL();

    // populate suburb dropdown from regions
    var subSel = root.querySelector('select[name="suburb"]');
    if (subSel) {
      getRegions().forEach(function (r) {
        var o = document.createElement("option"); o.value = r.slug; o.textContent = r.name; subSel.appendChild(o);
      });
    }

    function syncControls() {
      tabs.forEach(function (t) { t.setAttribute("aria-selected", t.dataset.status === state.status ? "true" : "false"); });
      fields.forEach(function (sel) {
        var k = sel.name; var v = state[k];
        sel.value = v == null ? "" : String(v);
        var wrap = sel.closest(".fb-field");
        if (wrap) wrap.toggleAttribute("data-active", v != null && v !== "");
      });
      var dirty = state.suburb || state.type || state.beds || state.baths || state.cars || state.pmin || state.pmax;
      clearBtn.hidden = !dirty;
    }

    function render() {
      // loading skeletons (simulate async fetch)
      grid.innerHTML = skeleton(4);
      writeFilterToURL(state); syncControls();
      setTimeout(function () {
        var results = getListings(state);
        if (!results.length) {
          grid.innerHTML = '<div class="p-empty"><h3>No properties match these filters.</h3>' +
            '<p class="muted">Try widening your price or bedroom range.</p></div>';
          count.textContent = "";
          return;
        }
        grid.innerHTML = results.map(function (l, i) { return cardHTML(l, (i % 3) + 1); }).join("");
        count.textContent = results.length + (results.length === 1 ? " property" : " properties");
        observeReveals();
      }, 220);
    }

    tabs.forEach(function (t) { t.addEventListener("click", function () { state.status = t.dataset.status; render(); }); });
    fields.forEach(function (sel) {
      sel.addEventListener("change", function () {
        var v = sel.value === "" ? null : (/^(beds|baths|cars|pmin|pmax)$/.test(sel.name) ? parseInt(sel.value, 10) : sel.value);
        state[sel.name] = v; render();
      });
    });
    clearBtn.addEventListener("click", function () {
      state = { status: state.status, suburb: null, type: null, beds: null, baths: null, cars: null, pmin: null, pmax: null };
      render();
    });

    render();
  }
  function skeleton(n) {
    var s = ""; for (var i = 0; i < n; i++) s += '<div class="sk-card"><div class="sk-card__img"></div><div class="sk-card__line"></div><div class="sk-card__line" style="width:40%"></div></div>';
    return s;
  }

  /* ---------------------------- LISTING PAGE ----------------------------- */
  function initListing() {
    var root = document.getElementById("listing-detail");
    if (!root) return;
    var slug = new URLSearchParams(location.search).get("id");
    var l = (slug && getListing(slug)) || D.LISTINGS[0];
    var agent = getAgent(l.agent), co = l.coAgent ? getAgent(l.coAgent) : null;
    document.title = l.seo.title + " | Bespoke Estate Agents";

    var m = markerFor(l);
    var galleryShown = l.gallery.slice(0, 6);
    var extra = l.gallery.length - galleryShown.length;

    root.innerHTML =
      // HERO
      '<section class="listing-hero">' +
        '<img src="' + l.hero.url + '" alt="' + esc(l.hero.alt) + '">' +
        '<div class="listing-hero__in"><div class="wrap">' +
          '<div class="listing-hero__suburb">' + esc(suburbName(l.address.suburb)) + ' · ' + esc(l.address.state) + '</div>' +
          '<h1>' + esc(l.address.street) + '</h1>' +
        '</div></div>' +
      '</section>' +
      // BODY
      '<div class="wrap section--tight">' +
        '<div class="listing-bar reveal">' +
          '<span class="listing-price">' + esc(priceLine(l)) + (l.status === "sold" && l.soldData ? ' <span class="muted" style="font-size:.9rem">· ' + fmtMonth(l.soldData.date) + '</span>' : "") + '</span>' +
          '<div class="listing-metrics">' +
            metric(ICON.bed, l.beds, "Bed") + metric(ICON.bath, l.baths, "Bath") + metric(ICON.car, l.cars, "Car") +
            (l.landSize ? metric(null, l.landSize + " m²", "Land") : "") +
            (l.floorSize ? metric(null, l.floorSize + " m²", "Internal") : "") +
          '</div>' +
        '</div>' +
        '<div class="section--tight listing-cols">' +
          // MAIN
          '<div>' +
            '<div class="reveal listing-desc">' + l.description.map(function (p) { return "<p>" + esc(p) + "</p>"; }).join("") + '</div>' +
            (l.features.length ? '<div class="reveal" data-d="1"><span class="eyebrow" style="margin-top:24px">The Detail</span><ul class="listing-features">' +
              l.features.map(function (f) { return "<li>" + esc(f) + "</li>"; }).join("") + '</ul></div>' : "") +
            '<div class="reveal" data-d="1"><span class="eyebrow" style="margin-top:40px">Gallery</span>' +
              '<div class="gallery">' + galleryShown.map(function (g, i) {
                var last = i === galleryShown.length - 1 && extra > 0;
                return '<button type="button" data-i="' + i + '"' + (last ? ' class="more" data-more="+' + extra + '"' : "") +
                  '><img src="' + g.url + '" alt="' + esc(g.alt) + '" loading="lazy"></button>';
              }).join("") + '</div>' +
            '</div>' +
          '</div>' +
          // ASIDE
          '<aside class="listing-aside reveal" data-d="1">' +
            '<div class="agent-card">' +
              agentRow(agent) + (co ? agentRow(co) : "") +
              '<form class="enquiry" novalidate>' +
                '<div class="form-body">' +
                  '<p class="muted" style="margin-bottom:16px">Enquire about ' + esc(l.address.street) + '.</p>' +
                  fld("name", "Full name", "text") + fld("email", "Email", "email") + fld("phone", "Phone (optional)", "tel") +
                  '<div class="fld"><label for="f-msg">Message</label><textarea id="f-msg" name="message"></textarea></div>' +
                  '<div class="fld consent"><input type="checkbox" id="f-consent" required><label for="f-consent" style="letter-spacing:0;text-transform:none;font-weight:400">I agree to be contacted about this property.</label></div>' +
                  '<button type="submit" class="btn btn--primary">Send enquiry</button>' +
                '</div>' +
                '<div class="ok"><strong>Thank you.</strong><br>Jason & Barbara will be in touch shortly.</div>' +
              '</form>' +
            '</div>' +
          '</aside>' +
        '</div>' +
      '</div>' +
      // RELATED
      relatedHTML(l);

    // gallery + lightbox
    var buttons = root.querySelectorAll(".gallery button");
    buttons.forEach(function (b) { b.addEventListener("click", function () { openLightbox(l.gallery, parseInt(b.dataset.i, 10)); }); });
    // form
    wireForm(root.querySelector(".enquiry"), { source: "listing_enquiry", relatedListing: l.slug });
    observeReveals();
  }

  function metric(icon, val, label) {
    return '<span class="listing-metric">' + (icon ? '<img src="' + icon + '" alt="">' : "") +
      '<b>' + esc(val) + '</b> <span class="muted" style="font-size:.82rem">' + esc(label) + '</span></span>';
  }
  function agentRow(a) {
    if (!a) return "";
    return '<div class="agent-row"><img src="' + a.photo.url + '" alt="' + esc(a.photo.alt) + '">' +
      '<div><div class="nm">' + esc(a.name) + '</div><div class="rl">' + esc(a.role) + '</div></div></div>';
  }
  function fld(name, label, type) {
    var id = "f-" + name;
    return '<div class="fld"><label for="' + id + '">' + label + '</label>' +
      '<input id="' + id + '" name="' + name + '" type="' + type + '"' + (name === "message" ? "" : "") + '>' +
      '<div class="err">Please enter a valid ' + label.toLowerCase().replace(" (optional)", "") + '.</div></div>';
  }
  function fmtMonth(iso) {
    var d = new Date(iso); return d.toLocaleDateString("en-AU", { month: "long", year: "numeric" });
  }
  function relatedHTML(l) {
    var rel = getListings({ status: "buy", suburb: l.address.suburb }).filter(function (x) { return x.slug !== l.slug; });
    if (!rel.length) rel = D.LISTINGS.filter(function (x) { return x.slug !== l.slug; }).slice(0, 2);
    else rel = rel.slice(0, 2);
    if (!rel.length) return "";
    return '<section class="section section--offwhite"><div class="wrap">' +
      '<div class="related-head"><h2 class="reveal">More in this market</h2>' +
      '<a class="reveal muted" href="index.html" style="text-decoration:underline;text-underline-offset:4px">View all listings</a></div>' +
      '<div class="p-grid">' + rel.map(function (x, i) { return cardHTML(x, i + 1); }).join("") + '</div>' +
      '</div></section>';
  }

  /* ------------------------------ FORM ----------------------------------- */
  function wireForm(form, ctx) {
    if (!form) return;
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var ok = true;
      var name = form.querySelector('[name="name"]'), email = form.querySelector('[name="email"]');
      [name, email].forEach(function (inp) {
        var valid = inp.name === "email" ? /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(inp.value) : inp.value.trim().length > 1;
        inp.closest(".fld").toggleAttribute("data-err", !valid); if (!valid) ok = false;
      });
      var consent = form.querySelector("#f-consent");
      if (consent && !consent.checked) { ok = false; consent.closest(".fld").style.color = "#8a5a4a"; }
      if (!ok) return;
      var btn = form.querySelector("button[type=submit]"); btn.setAttribute("aria-busy", "true"); btn.textContent = "Sending…";
      var lead = {
        name: name.value.trim(), email: email.value.trim(),
        phone: (form.querySelector('[name="phone"]') || {}).value || "",
        message: (form.querySelector('[name="message"]') || {}).value || "",
        source: ctx.source, relatedListing: ctx.relatedListing || null, relatedRegion: ctx.relatedRegion || null,
        consent: true, createdAt: new Date().toISOString(), status: "new"
      };
      // PRODUCTION: POST this to createLead() -> Payload Lead collection / WP form handler.
      console.log("[Bespoke] Lead captured:", lead);
      setTimeout(function () { form.classList.add("sent"); }, 500);
    });
  }

  /* ----------------------------- LIGHTBOX -------------------------------- */
  function openLightbox(images, index) {
    var i = index || 0;
    var dlg = document.createElement("dialog");
    dlg.className = "lightbox";
    function draw() {
      dlg.innerHTML =
        '<button class="lb-close" aria-label="Close">✕</button>' +
        '<button class="lb-btn lb-prev" aria-label="Previous">‹</button>' +
        '<div class="lb-stage"><img src="' + images[i].url + '" alt="' + esc(images[i].alt) + '"></div>' +
        '<button class="lb-btn lb-next" aria-label="Next">›</button>' +
        '<div class="lb-count">' + (i + 1) + " / " + images.length + '</div>';
      dlg.querySelector(".lb-close").onclick = function () { dlg.close(); };
      dlg.querySelector(".lb-prev").onclick = function () { i = (i - 1 + images.length) % images.length; draw(); };
      dlg.querySelector(".lb-next").onclick = function () { i = (i + 1) % images.length; draw(); };
    }
    draw();
    dlg.addEventListener("click", function (e) { if (e.target === dlg) dlg.close(); });
    dlg.addEventListener("keydown", function (e) {
      if (e.key === "ArrowRight") { i = (i + 1) % images.length; draw(); }
      if (e.key === "ArrowLeft") { i = (i - 1 + images.length) % images.length; draw(); }
    });
    dlg.addEventListener("close", function () { dlg.remove(); });
    document.body.appendChild(dlg); dlg.showModal();
  }

  /* ------------------------------- BOOT ---------------------------------- */
  document.addEventListener("DOMContentLoaded", function () {
    initChrome(); initReveal(); initListings(); initListing();
  });
})();
