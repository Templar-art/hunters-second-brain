# Bespoke site — polish notes

Site is in great shape and renders correctly (the scroll-reveal system works, content shows). These are three minor, non-blocking polish items — safe to knock out whenever. No urgent bugs.

Context: WordPress + Elementor/ElementsKit build at https://bespoke.agents.10xvisuals.co

---

## 1. Services page `<title>` is the lowercase WP default

**What:** The Services tab/title reads `services - Bespoke Estate Agents` (lowercase "services", hyphen separator). The homepage title is correct: `Bespoke Estate Agents | Gold Coast`.

**Why it matters:** Weak for SEO and looks unpolished in the browser tab / when shared as a link.

**Fix:** Set the Services page's SEO title so it matches the site's format. If you're using an SEO plugin (Yoast / RankMath / SEO Framework), set the page title template or the per-page SEO title to something like:

`Services | Bespoke Estate Agents | Gold Coast Prestige Property`

Check the other sub-pages (Projects, Sold, About, Contact) while you're in there — same lowercase-default issue likely applies. Make the separator/format consistent with Home.

---

## 2. Site language is `en-US`, should be `en-AU`

**What:** The `<html lang="en-US">` attribute is set to US English on an Australian business site.

**Why it matters:** Minor, but it's the correct signal for screen readers, browser spellcheck, and locale/SEO. Easy win.

**Fix:** `WordPress Admin → Settings → General → Site Language →` set to **English (Australia)**. That updates the `lang` attribute site-wide. (If the theme hard-codes the lang attribute in header.php instead, change it there.)

---

## 3. (Optional, taste) Eyebrow label above most sections

**What:** Most sections carry a small uppercase kicker label (e.g. SERVICES, SELLING, APPRAISALS, PRESENTATION & MARKETING, MARKET INTELLIGENCE, THE PROCESS). Having one above nearly every block is a common template pattern that slightly softens the "custom, expensive" feel.

**Why it matters:** Purely aesthetic, low priority. The design is strong as-is.

**Fix (only if you agree):** Keep the kicker on one or two anchor sections (e.g. the hero and "The Process") and drop it from the rest, OR let the section headings carry themselves. Not a must — leave it if you like the rhythm.

---

Everything else checks out: contrast passes, mobile layout is clean, brand type/colour are on-system, hero video is solid. Nice work.
