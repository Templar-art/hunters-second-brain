---
type: concept
tags: [ads, meta, facebook, tracking, pixel, dataset, capi, wordpress, lead-gen]
status: active
updated: 2026-07-29
---

# Meta Tracking Setup — dataset, events, and what covers which lead type

How to install and verify Meta's tracking on a client site, and — the part that gets assumed wrong — which lead types it actually covers. Written against [[mvx-electrical]], whose site was audited 29 Jul 2026 and has **no Meta pixel at all**: one Google tag (`GT-PLHFWDZJ`), no GTM container, Formidable Forms handling submissions. Companion to [[paid-ads-diagnostic-rulebook]] Rule 8 and [[zidane-meta-ads-tips]].

## First: the pixel does not track instant-form leads

This is the distinction that decides everything below, and getting it backwards means installing tracking that reports nothing while believing the campaign is measured.

| Lead type | Where the lead happens | What records it | Dataset needed? |
|---|---|---|---|
| **On-Facebook instant form** | Inside Facebook or Instagram | Meta, natively. Appears as *Leads* in Ads Manager with zero setup | **No** |
| **Website form** | Your site | Dataset + a `Lead` event you fire | **Yes** |
| **Click-to-call from an ad** | The phone | Meta counts the *click*, never the call | No — needs call tracking |
| **Lead quality / did it become a job** | Your CRM, days later | Offline conversions or CRM-connected CAPI | Different mechanism — see below |

A dataset is a record of events **on a website**. An instant form never loads the website, so there is nothing for it to observe. This is why the [[mvx-electrical]] hot water campaign, which is instant-form by design, gains nothing from the pixel on its optimisation — and why a missing pixel explains nothing if that campaign underperforms.

## So why install it at all

Three reasons that are all real, none of which are "to track the instant-form campaign":

1. **Retargeting pools.** The Google Ads landing pages already take paid traffic. Every visitor is a warm audience Meta could re-approach, and audiences only accumulate from the day the pixel goes live — there is no backfill. Installing late costs the pool permanently.
2. **Lookalikes.** Once there is a converter list, Meta can model against it. Same no-backfill rule.
3. **Future website-destination campaigns.** The moment any Meta ad points at a landing page instead of an instant form, the dataset becomes the only thing measuring it.

Point 1 is the argument for doing it now rather than when it is needed. The audience you can build in six months is decided by whether the pixel was live today.

## Setup — the dataset itself

1. **Business Manager → Events Manager → Connect data source → Web.** This creates the dataset. It is a *business* asset, not an ad-account asset — create it on the client's Business Manager, then assign the ad account to it. One per business, shared across ad accounts; do not create a second one per campaign.
2. **Verify the domain.** Business Settings → Brand Safety → Domains, then a DNS TXT record or a meta tag. Domain verification is what lets the business own and configure that domain's events, and it is a prerequisite for Aggregated Event Measurement priority ordering post-ATT. Skipping it works until it silently doesn't.
3. **Assign the ad account** to the dataset so campaigns can read it.

## Installing the code on WordPress + Elementor

Three routes, in order of preference for a site in MVX's shape — WP with a Google tag but no GTM container:

**Route A — Google Tag Manager (recommended if adding a container is acceptable).** Install a GTM container, then deploy the Meta base pixel and every event as GTM tags. Cost: one more layer and one more thing to hold admin on. Benefit: the same container serves Google Ads conversions, which are needed anyway per [FORM-FIX.md](../../projects/mvx-lead-fix/FORM-FIX.md), so both platforms get fixed in one pass instead of two.

**Route B — a WordPress pixel plugin.** No code, fastest to a working base pixel. ⚠️ Confirm the plugin's form-event support covers **Formidable Forms** specifically before relying on automatic lead events — plugin form integrations commonly cover Contact Form 7 and WPForms while Formidable sits behind a paid tier or is absent. Verify against the live plugin, don't assume.

**Route C — hand-place the base code** in the theme header via a child theme or Elementor's custom-code feature. Fine for the base pixel; the event firing still has to be solved separately.

### Firing the `Lead` event reliably

The robust method, independent of plugin support and of any JavaScript event name that a form plugin might rename:

**Redirect each form to its own thank-you page on submit, and fire `Lead` on that URL.**

- Set both Formidable forms — `form_id 2` (`air-con`) and `form_id 3` (`general-electrician`) — plus the hot water form, to redirect to distinct pages: `/thanks-aircon/`, `/thanks-electrician/`, `/thanks-hot-water/`.
- Fire `Lead` on each thank-you page load, with a parameter distinguishing which form.
- This doubles as the clean **Google Ads** conversion trigger, which [FORM-FIX.md](../../projects/mvx-lead-fix/FORM-FIX.md) already needs, and it makes per-page conversion rate readable in GA4 without extra work.

The alternative — listening for the form plugin's AJAX success event — is fewer clicks and more fragile: the event name is the plugin's to change, and a silent rename produces a campaign that looks like it stopped converting.

### The phone calls are the actual leads — track them separately

The MVX landing pages are phone-first by design (8–12 `tel:` links each; *the calls are the leads*). Neither a pixel nor an instant form captures a phone call.

- Fire a Meta **`Contact`** event on `tel:` link clicks so click-to-call intent at least appears in the dataset.
- ⚠️ A `tel:` click is not a connected call. It counts taps, including mis-taps and people who hang up. Treat it as an intent signal, never as a lead count — and never report it to a client as calls received.
- The real number needs **call tracking** — which is what Lach's system is for. See below.

## Lead *quality* is a different mechanism entirely

Worth separating, because it is the one that would actually fix [[mvx-electrical]]'s original problem of cheap junk leads.

The pixel answers "did a lead happen". It cannot answer "was the lead any good", because that is known days later, in a CRM, by a human. Meta learns lead quality through **offline conversions / CRM-connected Conversions API**: lead statuses get sent back — quoted, won, junk — and Meta then optimises toward the people who become jobs rather than the people who fill forms.

This is the upgrade path already noted in [BUILD.md](../../projects/mvx-meta-rebuild/BUILD.md): once Lach's call tracking feeds lead status back, the ad-set performance goal switches from *Maximise number of leads* to **Maximise number of conversion leads**. That switch, not the pixel, is the real fix for lead quality — and it works for instant-form campaigns, which the pixel does not.

## Verification — before trusting any of it

Never assume an install works because the plugin says it's active.

1. **Meta Pixel Helper** (Chrome extension) on each landing page — confirms the base pixel fires and shows the events.
2. **Events Manager → Test Events** — submit a real form from a phone and watch the `Lead` event arrive live. This is the same instruction as Rule 3 in [[paid-ads-diagnostic-rulebook]]: submit a real test lead and confirm where it lands.
3. **Check for duplicate events.** A plugin plus a hand-placed snippet plus a GTM tag will happily fire the pixel three times and inflate every number. Pixel Helper shows the duplication.
4. **Wait for the dataset to accumulate** before judging any campaign that depends on it. A dataset installed the same week as the campaign has no history during exactly the week the campaign gets judged.

## Access blockers — this needs Matt, not just Hunter

Nothing here is 10x's to configure unilaterally, and it is the same wall [FORM-FIX.md](../../projects/mvx-lead-fix/FORM-FIX.md) hit:

- **Client Business Manager access** — to create the dataset and verify the domain.
- **WordPress admin** — to place code or install a plugin, and to set the form redirects.
- **DNS access** — for the domain verification TXT record, if the meta-tag method isn't used.

Bundle all three into one ask rather than three separate ones, and bundle it with the form fix, since both need the same WP admin session.
