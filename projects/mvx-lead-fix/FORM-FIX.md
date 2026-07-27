# MVX Electrical — Ad Landing Page Lead-Capture Fix

**Date:** 2026-07-27 · **Client:** MVX Electrical (Matt) · **Vault:** [[mvx-electrical]]
**Scope:** the two live Google Ads landing pages. No design change, no rebuild — form friction only, plus one copy bug.
**Cost:** $0. No credits, no new pages.

## Why

Both landing pages went live on 14 Jul built from [CONVERSION-NOTES.md](../mvx-aircon/CONVERSION-NOTES.md). The page design shipped correctly (message-matched H1, 7 tap-to-call links, sticky call bar, licence strip, "one trade, one visit" differentiator). **The form did not.** The spec cut the form to 4 fields and removed email deliberately; the Formidable build put email back, kept postcode, and made the free-text message **required**.

Verified 2026-07-27 by reading the live page markup (`aria-required="true"` on each):

| Field | Aircon form (`form_id 2`, key `air-con`) | Electricians form (`form_id 3`, key `general-electrician`) | Spec | Action |
|---|---|---|---|---|
| Name | `item_meta[10]` required | `item_meta[17]` required | required | **keep** |
| Phone | `item_meta[11]` required | `item_meta[18]` required | required | **keep** |
| Email | `item_meta[12]` **required** | `item_meta[19]` **required** | removed | **delete field** |
| Project Postcode | `item_meta[13]` **required** | `item_meta[20]` **required** | suburb | **relabel → Suburb, keep required** |
| Job type (checkboxes) | `item_meta[14]` required | `item_meta[21]` required | required | **keep** |
| "How Can We Help?" textarea | `item_meta[15]` **required** | `item_meta[22]` **required** | optional | **make optional** |

Six required fields, one of them a free-text essay, on traffic that is mostly mobile phone-intent clicks. This is a phone-first page — the form exists as a callback request for people who won't call, and it is currently asking them for more than the call would.

## The fix — Formidable admin, ~10 minutes

For **both** forms (Formidable → Forms → *Air Con* / *General Electrician* → Fields):

1. **Delete the Email field.** Not "make optional" — delete. The callback is a phone call; an email field on a phone-first form is a question with no purpose, and every field costs completions. If entry notification emails are addressed to the *customer's* email anywhere, repoint them to Matt's inbox first, or step 1 breaks the notification.
2. **Relabel "Project Postcode" → "Suburb".** Keep it required. Suburb is what the sparky needs to route the job and what a resident types without thinking; a postcode is a lookup task.
3. **"How Can We Help?" → untick Required.** Keep the field, keep 8–9 rows. Change the label to **"Anything else? (optional)"** so it reads as skippable at a glance.
4. **Leave the honeypot alone.** Both forms carry Formidable's `frm_verify` spam field (`item_meta[24]`) — it is invisible to users and unrelated to friction. Do not remove it while removing fields.

Result: 4 required fields (name, phone, suburb, job type) + one optional note. Matches the approved spec.

## Bug found in the same pass — wrong service in the electricians form

On the **electricians** form (`form_id 3`), the job-type checkbox group's validation message still reads:

> "How can we help with your **aircon**? cannot be blank."

Copy-paste leftover from the aircon form. A visitor on the residential-electrician page who submits without picking a service gets an error about air conditioning. Fix the field label/validation text on `item_meta[21]` to "What do you need done?".

## Also worth doing while in there

- **Strip the site nav from both landing pages.** Spec called for this and it didn't happen — both pages ship the full menu with submenus. Ad landing pages leak: every nav item is an exit from a page you paid for the click on. Keep logo + phone in the header, kill the menu. (Elementor: use a landing-page template with no header, or hide the nav via the page's Elementor settings.)
- **Confirm conversion tracking exists.** Pre-launch checklist item that was never signed off. Both pages need `tel:` clicks firing as a Google Ads conversion, not just form submits — on a phone-first page the calls *are* the leads, and if only form submits are tracked, Google Ads is optimising toward the weaker action and reporting a fraction of real performance. Ideally a call-tracking number swap; at minimum GA4 `tel:` click events imported as conversions.

## Verify after the change

1. Submit a test lead from a **real phone** on both pages — confirm it arrives in Matt's inbox and in Formidable → Entries.
2. Tap the sticky call bar and confirm the conversion fires in Google Ads (or GA4 realtime).
3. Re-read the live markup and confirm only 4 `aria-required="true"` fields remain per form.

## Expected effect — stated honestly

Removing required fields raises form completion; a required free-text field on mobile is the single heaviest item on either form. Direction is reliable, size is not predictable — so **record the baseline before changing anything** (last 14 days: form entries + call conversions per page from Google Ads) or the lift is unmeasurable after the fact.

⚠️ This fix does **not** address lead *mix*. MVX has no hot water page anywhere on the site (verified against the full 29-page sitemap), which is why no hot water leads exist to shift toward. That is a separate build, blocked on whether Matt subs or partners a licensed plumber for the water side.
