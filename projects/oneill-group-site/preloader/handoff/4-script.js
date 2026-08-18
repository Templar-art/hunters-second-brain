/* ===== O'Neill Group — preloader init ===== */
/* Merge into the site's main JS file, run on DOMContentLoaded (or wherever
   the site's existing init sequence lives — same pattern as Bespoke's site.js). */

function initPreloader(){
  var pre = document.getElementById('preloader');
  if (!pre) return;
  var seen = false;
  try { seen = !!sessionStorage.getItem('ogSeen'); } catch(e){}
  if (seen) { pre.remove(); return; }

  document.body.classList.add('preloading');
  var done = false;
  function dismiss(){
    if (done) return; done = true;
    try { sessionStorage.setItem('ogSeen','1'); } catch(e){}
    pre.classList.add('done');
    document.body.classList.remove('preloading');
    setTimeout(function(){ if (pre.parentNode) pre.remove(); }, 950);
  }
  // animation runs ~4.2s (draw 3.2s, then fill 3.2s→4.2s) — hold slightly past that, then release
  setTimeout(dismiss, 4400);
}

document.addEventListener('DOMContentLoaded', initPreloader);
