/* ==========================================================================
   BESPOKE, prototype app logic
   - Data-access layer (getListings/getListing/getRegions) is the ONLY seam
     that touches data. Swap its body for Payload/WP fetch; UI is untouched.
   - Filtering mirrors BUILD-SPEC section 7 (URL-synced, status map, min-semantics).
   - Motion is progressive: content is visible by default; reveal only enhances.
   ========================================================================== */
(function () {
  "use strict";
  var D = window.BESPOKE_DATA;
  var HERO_FALLBACK = "https://bespoke.agents.10xvisuals.co/wp-content/uploads/2026/07/47-Somersert-Drive-_-Print-Drone-2-scaled.jpg";

  // Shared footer (injected into [data-footer]) so all pages stay identical. Handles
  // are the client's real accounts from the live site.
  var IG = "M12 2.2c3.2 0 3.6 0 4.9.07 1.17.05 1.8.25 2.23.41.56.22.96.48 1.38.9.42.42.68.82.9 1.38.16.42.36 1.06.41 2.23.06 1.27.07 1.65.07 4.85s0 3.58-.07 4.85c-.05 1.17-.25 1.8-.41 2.23-.22.56-.48.96-.9 1.38-.42.42-.82.68-1.38.9-.42.16-1.06.36-2.23.41-1.27.06-1.65.07-4.85.07s-3.58 0-4.85-.07c-1.17-.05-1.8-.25-2.23-.41a3.7 3.7 0 0 1-1.38-.9 3.7 3.7 0 0 1-.9-1.38c-.16-.42-.36-1.06-.41-2.23C2.21 15.6 2.2 15.2 2.2 12s0-3.58.07-4.85c.05-1.17.25-1.8.41-2.23.22-.56.48-.96.9-1.38.42-.42.82-.68 1.38-.9.42-.16 1.06-.36 2.23-.41C8.42 2.21 8.8 2.2 12 2.2Zm0 1.8c-3.15 0-3.5 0-4.75.07-.9.04-1.38.19-1.7.31-.43.17-.74.37-1.06.69-.32.32-.52.63-.69 1.06-.12.32-.27.8-.31 1.7C3.6 8.5 3.6 8.85 3.6 12s0 3.5.07 4.75c.04.9.19 1.38.31 1.7.17.43.37.74.69 1.06.32.32.63.52 1.06.69.32.12.8.27 1.7.31 1.25.07 1.6.07 4.75.07s3.5 0 4.75-.07c.9-.04 1.38-.19 1.7-.31.43-.17.74-.37 1.06-.69.32-.32.52-.63.69-1.06.12-.32.27-.8.31-1.7.07-1.25.07-1.6.07-4.75s0-3.5-.07-4.75c-.04-.9-.19-1.38-.31-1.7a2.85 2.85 0 0 0-.69-1.06 2.85 2.85 0 0 0-1.06-.69c-.32-.12-.8-.27-1.7-.31C15.5 4 15.15 4 12 4Zm0 3.06A4.94 4.94 0 1 1 7.06 12 4.94 4.94 0 0 1 12 7.06Zm0 8.15A3.21 3.21 0 1 0 8.79 12 3.21 3.21 0 0 0 12 15.21Zm6.29-8.35a1.15 1.15 0 1 1-1.15-1.15 1.15 1.15 0 0 1 1.15 1.15Z";
  var FB = "M22 12a10 10 0 1 0-11.56 9.88v-6.99H7.9V12h2.54V9.8c0-2.5 1.49-3.89 3.77-3.89 1.09 0 2.24.2 2.24.2v2.46h-1.26c-1.24 0-1.63.77-1.63 1.56V12h2.78l-.44 2.89h-2.34v6.99A10 10 0 0 0 22 12Z";
  var LI = "M20.45 20.45h-3.56v-5.57c0-1.33-.02-3.04-1.85-3.04-1.85 0-2.14 1.45-2.14 2.94v5.67H9.35V9h3.42v1.56h.05a3.75 3.75 0 0 1 3.37-1.85c3.6 0 4.27 2.37 4.27 5.46v6.28ZM5.34 7.43a2.07 2.07 0 1 1 0-4.13 2.07 2.07 0 0 1 0 4.13Zm1.78 13.02H3.55V9h3.57v11.45ZM22.22 0H1.77C.8 0 0 .78 0 1.75v20.5C0 23.22.79 24 1.77 24h20.45c.98 0 1.78-.78 1.78-1.75V1.75C24 .78 23.2 0 22.22 0Z";
  function soc(href, label, path) { return '<a href="' + href + '" aria-label="' + label + '" target="_blank" rel="noopener"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="' + path + '"/></svg></a>'; }
  var FOOTER =
    '<div class="wrap"><div class="footer-top">' +
      '<div class="footer-brand"><a class="brand" href="../index.html" aria-label="Bespoke Estate Agents home">' +
        '<img class="brand__icon" src="../assets/logos/bespoke-icon-offwhite.png" alt=""><span class="brand__word"><b>BESPOKE</b><span>Estate Agents</span></span></a>' +
        '<p>Boutique prestige real estate on the Gold Coast. Every property has a story, and every seller deserves the right person to tell it.</p>' +
        '<div class="socials">' + soc("https://www.instagram.com/bespoke.international", "Instagram", IG) + soc("https://www.facebook.com/bespokeinternationalrealty", "Facebook", FB) + soc("https://www.linkedin.com/company/bespoke-international-realty", "LinkedIn", LI) + '</div>' +
      '</div>' +
      '<div class="footer-col"><h4>Explore</h4><a href="../index.html">Home</a><a href="index.html">Collection</a><a href="../index.html#team">About</a><a href="../services.html">Services</a><a href="../projects.html">Projects</a><a href="../index.html#contact">Contact</a></div>' +
      '<div class="footer-col"><h4>Get in touch</h4><a href="tel:0424731063">0424 731 063</a><a href="mailto:info@bespokerealestate.com.au">info@bespokerealestate.com.au</a><p>Gold Coast, Queensland</p>' +
        '<a class="btn btn--outline-light" href="soon.html?s=appraisal" data-appraisal style="margin-top:16px">Book a Private Appraisal</a></div>' +
    '</div>' +
    '<div class="footer-bottom"><span>&copy; <span data-year></span> Bespoke Estate Agents. All rights reserved.</span><span>Beyond Luxury Real Estate</span></div></div>';

  /* ----------------------------- DATA ACCESS ----------------------------- */
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
      // Price range applies to numeric prices only; EOI/POA/contact always pass.
      if (l.price.display === "numeric") {
        if (f.pmin && l.price.amount < f.pmin) return false;
        if (f.pmax && l.price.amount > f.pmax) return false;
      }
      return true;
    });
    out.sort(function (a, b) {
      if ((f.status || "buy") === "sold") {
        return (b.soldData ? b.soldData.date : "").localeCompare(a.soldData ? a.soldData.date : "");
      }
      return (b.price.amount || 0) - (a.price.amount || 0);
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
    return '<span class="p-meta-i"><img src="' + ICON.bed + '" alt="Beds">' + l.beds + '</span>' +
           '<span class="p-meta-i"><img src="' + ICON.bath + '" alt="Baths">' + l.baths + '</span>' +
           '<span class="p-meta-i"><img src="' + ICON.car + '" alt="Car spaces">' + l.cars + '</span>' +
           (l.landSize ? '<span class="p-meta-i">' + l.landSize + ' m&sup2;</span>' : "");
  }

  /* ---------------------------- PROPERTY CARD ---------------------------- */
  function cardHTML(l, delay) {
    var m = markerFor(l), sold = l.status === "sold";
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
    if (reduce || !("IntersectionObserver" in window)) return;
    document.documentElement.classList.add("reveal-on");
    io = new IntersectionObserver(function (ents) {
      ents.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } });
    }, { rootMargin: "0px 0px -8% 0px" });
    observeReveals();
    setTimeout(function () { document.querySelectorAll(".reveal:not(.in)").forEach(function (el) { el.classList.add("in"); }); }, 1600);
  }
  function observeReveals() { if (io) document.querySelectorAll(".reveal:not(.in)").forEach(function (el) { io.observe(el); }); }

  /* --------------------------- HEADER / CHROME --------------------------- */
  function initChrome() {
    var foot = document.querySelector("[data-footer]"); if (foot) foot.innerHTML = FOOTER;
    var header = document.querySelector(".site-header");
    if (header) {
      var onScroll = function () { header.classList.toggle("scrolled", window.scrollY > 24); };
      onScroll(); window.addEventListener("scroll", onScroll, { passive: true });
    }
    var toggle = document.querySelector(".menu-toggle");
    if (toggle) {
      var setOpen = function (open) {
        document.body.classList.toggle("menu-open", open);
        toggle.setAttribute("aria-expanded", open ? "true" : "false");
      };
      toggle.addEventListener("click", function () { setOpen(!document.body.classList.contains("menu-open")); });
      var menu = document.getElementById("site-menu");
      if (menu) menu.addEventListener("click", function (e) { if (e.target.tagName === "A" || e.target === menu) setOpen(false); });
      document.addEventListener("keydown", function (e) { if (e.key === "Escape") setOpen(false); });
    }
    // Appraisal CTAs (event-delegated so dynamically-injected ones work too).
    document.addEventListener("click", function (e) {
      var t = e.target.closest && e.target.closest("[data-appraisal]");
      if (t) { e.preventDefault(); openAppraisal(); }
    });
    document.querySelectorAll("[data-year]").forEach(function (y) { y.textContent = new Date().getFullYear(); });
  }

  /* ------------------------------ FORMS ---------------------------------- */
  function fld(name, label, type, pfx) {
    var id = pfx + name, opt = name === "phone";
    return '<div class="fld"><label for="' + id + '">' + label + '</label>' +
      '<input id="' + id + '" name="' + name + '" type="' + type + '"' + (opt ? "" : " required") + '>' +
      '<div class="err">Please enter a valid ' + label.toLowerCase().replace(" (optional)", "") + '.</div></div>';
  }
  function buildEnquiry(pfx, intro, submitLabel) {
    return '<div class="form-body">' +
      (intro ? '<p class="muted" style="margin-bottom:16px">' + intro + '</p>' : "") +
      fld("name", "Full name", "text", pfx) + fld("email", "Email", "email", pfx) + fld("phone", "Phone (optional)", "tel", pfx) +
      '<div class="fld"><label for="' + pfx + 'msg">Message</label><textarea id="' + pfx + 'msg" name="message"></textarea></div>' +
      '<div class="fld consent"><input type="checkbox" id="' + pfx + 'consent"><label for="' + pfx + 'consent" style="letter-spacing:0;text-transform:none;font-weight:400">I agree to be contacted by Bespoke Estate Agents.</label></div>' +
      '<button type="submit" class="btn btn--primary">' + submitLabel + '</button>' +
      '</div><div class="ok"><strong>Thank you.</strong><br>Jason and Barbara will be in touch shortly.</div>';
  }
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
      var consent = form.querySelector(".consent input");
      if (consent && !consent.checked) { ok = false; consent.closest(".fld").style.color = "#8a5a4a"; }
      if (!ok) return;
      var btn = form.querySelector("button[type=submit]"); btn.setAttribute("aria-busy", "true"); btn.textContent = "Sending";
      var lead = {
        name: name.value.trim(), email: email.value.trim(),
        phone: (form.querySelector('[name="phone"]') || {}).value || "",
        message: (form.querySelector('[name="message"]') || {}).value || "",
        source: ctx.source, relatedListing: ctx.relatedListing || null, relatedRegion: ctx.relatedRegion || null,
        consent: true, createdAt: new Date().toISOString(), status: "new"
      };
      // PRODUCTION: POST to createLead() -> Payload Lead collection / WP form handler.
      console.log("[Bespoke] Lead captured:", lead);
      setTimeout(function () { form.classList.add("sent"); }, 500);
    });
  }

  /* --------------------------- LISTINGS PAGE ----------------------------- */
  function readFilterFromURL() {
    var q = new URLSearchParams(location.search);
    var num = function (k) { var v = parseInt(q.get(k), 10); return isNaN(v) ? null : v; };
    return { status: q.get("status") || "buy", suburb: q.get("suburb") || null, type: q.get("type") || null,
      beds: num("beds"), baths: num("baths"), cars: num("cars"), pmin: num("pmin"), pmax: num("pmax") };
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
    var grid = document.getElementById("listings-grid"), count = document.getElementById("fb-count"),
        clearBtn = document.getElementById("fb-clear"), tabs = root.querySelectorAll(".fb-tab"),
        fields = root.querySelectorAll(".fb-field select"), state = readFilterFromURL();
    var subSel = root.querySelector('select[name="suburb"]');
    if (subSel) getRegions().forEach(function (r) { var o = document.createElement("option"); o.value = r.slug; o.textContent = r.name; subSel.appendChild(o); });

    function syncControls() {
      tabs.forEach(function (t) { t.setAttribute("aria-selected", t.dataset.status === state.status ? "true" : "false"); });
      fields.forEach(function (sel) {
        var v = state[sel.name]; sel.value = v == null ? "" : String(v);
        var wrap = sel.closest(".fb-field"); if (wrap) wrap.toggleAttribute("data-active", v != null && v !== "");
      });
      clearBtn.hidden = !(state.suburb || state.type || state.beds || state.baths || state.cars || state.pmin || state.pmax);
    }
    function render() {
      grid.innerHTML = skeleton(4); writeFilterToURL(state); syncControls();
      setTimeout(function () {
        var results = getListings(state);
        if (!results.length) {
          grid.innerHTML = '<div class="p-empty"><h3>No properties match these filters.</h3><p class="muted">Try widening your price or bedroom range, or clear the filters.</p></div>';
          count.textContent = ""; return;
        }
        grid.innerHTML = results.map(function (l, i) { return cardHTML(l, (i % 3) + 1); }).join("");
        count.textContent = results.length + (results.length === 1 ? " property" : " properties");
        observeReveals();
      }, 220);
    }
    tabs.forEach(function (t) { t.addEventListener("click", function () { state.status = t.dataset.status; render(); }); });
    fields.forEach(function (sel) {
      sel.addEventListener("change", function () {
        state[sel.name] = sel.value === "" ? null : (/^(beds|baths|cars|pmin|pmax)$/.test(sel.name) ? parseInt(sel.value, 10) : sel.value);
        render();
      });
    });
    clearBtn.addEventListener("click", function () {
      state = { status: state.status, suburb: null, type: null, beds: null, baths: null, cars: null, pmin: null, pmax: null }; render();
    });
    render();
  }
  function skeleton(n) { var s = ""; for (var i = 0; i < n; i++) s += '<div class="sk-card"><div class="sk-card__img"></div><div class="sk-card__line"></div><div class="sk-card__line" style="width:40%"></div></div>'; return s; }

  /* ---------------------------- LISTING PAGE ----------------------------- */
  function initListing() {
    var root = document.getElementById("listing-detail");
    if (!root) return;
    var slug = new URLSearchParams(location.search).get("id");
    var l = (slug && getListing(slug)) || D.LISTINGS[0];
    var agent = getAgent(l.agent), co = l.coAgent ? getAgent(l.coAgent) : null;
    document.title = l.seo.title + " | Bespoke Estate Agents";
    var galleryShown = l.gallery.slice(0, 6), extra = l.gallery.length - galleryShown.length;

    root.innerHTML =
      '<section class="listing-hero"><img src="' + l.hero.url + '" alt="' + esc(l.hero.alt) + '">' +
        '<div class="listing-hero__in"><div class="wrap">' +
          '<div class="listing-hero__suburb">' + esc(suburbName(l.address.suburb)) + " &middot; " + esc(l.address.state) + '</div>' +
          '<h1>' + esc(l.address.street) + '</h1></div></div></section>' +
      '<div class="wrap section--tight">' +
        '<div class="listing-bar reveal">' +
          '<span class="listing-price">' + esc(priceLine(l)) + (l.status === "sold" && l.soldData ? ' <span class="muted" style="font-size:.9rem">&middot; ' + fmtMonth(l.soldData.date) + '</span>' : "") + '</span>' +
          '<div class="listing-metrics">' + metric(ICON.bed, l.beds, "Bed") + metric(ICON.bath, l.baths, "Bath") + metric(ICON.car, l.cars, "Car") +
            (l.landSize ? metric(null, l.landSize + " m&sup2;", "Land") : "") + (l.floorSize ? metric(null, l.floorSize + " m&sup2;", "Internal") : "") + '</div></div>' +
        '<div class="section--tight listing-cols"><div>' +
          '<div class="reveal listing-desc">' + l.description.map(function (p) { return "<p>" + esc(p) + "</p>"; }).join("") + '</div>' +
          (l.features.length ? '<div class="reveal" data-d="1"><span class="eyebrow" style="margin-top:24px">The Detail</span><ul class="listing-features">' + l.features.map(function (f) { return "<li>" + esc(f) + "</li>"; }).join("") + '</ul></div>' : "") +
          '<div class="reveal" data-d="1"><span class="eyebrow" style="margin-top:40px">Gallery</span><div class="gallery">' +
            galleryShown.map(function (g, i) { var last = i === galleryShown.length - 1 && extra > 0; return '<button type="button" data-i="' + i + '"' + (last ? ' class="more" data-more="+' + extra + '"' : "") + '><img src="' + g.url + '" alt="' + esc(g.alt) + '" loading="lazy"></button>'; }).join("") + '</div></div>' +
        '</div>' +
        '<aside class="listing-aside reveal" data-d="1"><div class="agent-card">' + agentRow(agent) + (co ? agentRow(co) : "") +
          '<form class="enquiry" novalidate>' + buildEnquiry("f-", "Enquire about " + esc(l.address.street) + ".", "Send enquiry") + '</form>' +
        '</div></aside></div></div>' + relatedHTML(l);

    root.querySelectorAll(".gallery button").forEach(function (b) { b.addEventListener("click", function () { openLightbox(l.gallery, parseInt(b.dataset.i, 10)); }); });
    wireForm(root.querySelector(".enquiry"), { source: "listing_enquiry", relatedListing: l.slug });
    observeReveals();
  }
  function metric(icon, val, label) { return '<span class="listing-metric">' + (icon ? '<img src="' + icon + '" alt="">' : "") + '<b>' + val + '</b> <span class="muted" style="font-size:.82rem">' + esc(label) + '</span></span>'; }
  function agentRow(a) { return a ? '<div class="agent-row"><img src="' + a.photo.url + '" alt="' + esc(a.photo.alt) + '"><div><div class="nm">' + esc(a.name) + '</div><div class="rl">' + esc(a.role) + '</div></div></div>' : ""; }
  function fmtMonth(iso) { return new Date(iso).toLocaleDateString("en-AU", { month: "long", year: "numeric" }); }
  function relatedHTML(l) {
    var rel = getListings({ status: "buy", suburb: l.address.suburb }).filter(function (x) { return x.slug !== l.slug; });
    if (!rel.length) rel = D.LISTINGS.filter(function (x) { return x.slug !== l.slug; }).slice(0, 2); else rel = rel.slice(0, 2);
    if (!rel.length) return "";
    return '<section class="section section--offwhite"><div class="wrap"><div class="related-head"><h2 class="reveal">More in this market</h2>' +
      '<a class="reveal muted" href="index.html" style="text-decoration:underline;text-underline-offset:4px">View all listings</a></div>' +
      '<div class="p-grid">' + rel.map(function (x, i) { return cardHTML(x, i + 1); }).join("") + '</div></div></section>';
  }

  /* --------------------------- APPRAISAL MODAL --------------------------- */
  function openAppraisal() {
    var dlg = document.createElement("dialog"); dlg.className = "modal";
    dlg.innerHTML = '<button class="modal-close" aria-label="Close">&#10005;</button><div class="modal-in">' +
      '<span class="eyebrow">Private Appraisal</span><h3 style="margin-top:6px">Book a private appraisal.</h3>' +
      '<form class="enquiry" novalidate>' + buildEnquiry("m-", "A quiet, no obligation conversation about your property and the current market, with real numbers on the table.", "Request appraisal") + '</form></div>';
    dlg.querySelector(".modal-close").onclick = function () { dlg.close(); };
    dlg.addEventListener("click", function (e) { if (e.target === dlg) dlg.close(); });
    dlg.addEventListener("close", function () { dlg.remove(); });
    document.body.appendChild(dlg); dlg.showModal();
    wireForm(dlg.querySelector(".enquiry"), { source: "appraisal" });
  }

  /* ----------------------------- LIGHTBOX -------------------------------- */
  function openLightbox(images, index) {
    var i = index || 0, dlg = document.createElement("dialog"); dlg.className = "lb";
    function draw() {
      dlg.innerHTML = '<button class="lb-close" aria-label="Close">&#10005;</button>' +
        '<button class="lb-btn lb-prev" aria-label="Previous">&#8249;</button>' +
        '<div class="lb-stage"><img src="' + images[i].url + '" alt="' + esc(images[i].alt) + '"></div>' +
        '<button class="lb-btn lb-next" aria-label="Next">&#8250;</button>' +
        '<div class="lb-count">' + (i + 1) + " / " + images.length + "</div>";
      dlg.querySelector(".lb-close").onclick = function () { dlg.close(); };
      dlg.querySelector(".lb-prev").onclick = function () { i = (i - 1 + images.length) % images.length; draw(); };
      dlg.querySelector(".lb-next").onclick = function () { i = (i + 1) % images.length; draw(); };
    }
    draw();
    dlg.addEventListener("click", function (e) { if (e.target === dlg) dlg.close(); });
    dlg.addEventListener("keydown", function (e) { if (e.key === "ArrowRight") { i = (i + 1) % images.length; draw(); } if (e.key === "ArrowLeft") { i = (i - 1 + images.length) % images.length; draw(); } });
    dlg.addEventListener("close", function () { dlg.remove(); });
    document.body.appendChild(dlg); dlg.showModal();
  }

  /* ------------------------------- SOON ---------------------------------- */
  function initSoon() {
    var root = document.getElementById("soon-root");
    if (!root) return;
    var s = new URLSearchParams(location.search).get("s") || "";
    var map = {
      suburbs: { ey: "Suburbs", h: "Suburb guides are on the way.", p: "Curated guides to the Gold Coast prestige pockets Bespoke works, each with its own story and current listings, arrive in the next phase." },
      journal: { ey: "Journal", h: "The Journal is being written.", p: "Considered notes on the prestige market, suburb insight and notable results. Coming shortly." },
      about:   { ey: "About", h: "Jason and Barbara Ward.", p: "The full story of the boutique team behind Bespoke arrives in the next phase." },
      appraisal: { ey: "Private Appraisal", h: "Book a private appraisal.", p: "A quiet, no obligation conversation about your property and the current market.", form: true },
      contact:   { ey: "Contact", h: "Get in touch.", p: "Reach Jason and Barbara directly, or request a private appraisal below.", form: true }
    };
    var d = map[s] || { ey: "Bespoke", h: "This section is on the way.", p: "Arriving in the next phase." };
    document.title = d.h + " | Bespoke Estate Agents";
    var html = '<section class="p-hero" style="min-height:46vh"><div class="p-hero__media"><img src="' + HERO_FALLBACK + '" alt=""></div>' +
      '<div class="wrap"><span class="eyebrow on-dark">' + d.ey + '</span><h1>' + d.h + '</h1><p>' + d.p + '</p></div></section>' +
      '<section class="section"><div class="wrap prose">';
    if (d.form) {
      html += '<div style="max-width:520px"><form class="enquiry" novalidate>' + buildEnquiry("s-", "", s === "appraisal" ? "Request appraisal" : "Send message") + '</form>' +
        '<p class="muted" style="margin-top:20px">Or call Jason and Barbara on <a href="tel:0424731063" style="color:var(--be-green);text-decoration:underline;text-underline-offset:3px">0424 731 063</a>.</p></div>';
    } else {
      html += '<div class="btn-row"><a class="btn btn--primary" href="index.html">Browse listings</a> <a class="btn btn--outline" href="soon.html?s=appraisal" data-appraisal>Book a private appraisal</a></div>';
    }
    html += "</div></section>";
    root.innerHTML = html;
    if (d.form) wireForm(root.querySelector(".enquiry"), { source: "appraisal" });
    observeReveals();
  }

  /* ------------------------------- BOOT ---------------------------------- */
  document.addEventListener("DOMContentLoaded", function () {
    initChrome(); initReveal(); initListings(); initListing(); initSoon();
  });
})();
