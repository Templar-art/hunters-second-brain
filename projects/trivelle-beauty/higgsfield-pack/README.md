# Trivelle — Higgsfield pack

Everything to paste into the Higgsfield web app. Two jobs:
**A. UGC ads** (Marketing Studio — a person talking to camera)
**B. Product motion clips** (image-to-video from our stills)

All 9:16, 1080p if your plan allows, 15 s for UGC, 5 s for motion.

---

## Step 1 — Set up the product (once)

Marketing Studio → **Products → Create**

- **Title:** Trivelle 3-in-1 Sculpt & Glow
- **Images:** upload all 5 from `1-product-refs/` (the button close-up is the real device — it helps the model get the buttons right)
- **Description:** A cordless handheld beauty device with three modes: red light for a radiant-looking finish, EMS micro-pulses for a toning, firming feel, and a moving suction massage that leaves skin looking smoother. White oval body, grey ring button on top, clear suction cup with steel roller balls underneath. Used with a lime-yellow tube of Glide Gel. About 10 minutes a session.

**Brand kit** (if it asks): use the one Higgsfield made you, **but** change "Free worldwide shipping" to "Free shipping Australia-wide" (the store only ships to AU right now).

---

## Step 2 — UGC ads (Marketing Studio → Video)

Mode in brackets. Pick a preset avatar who matches the note, or let it create one. Paste the script as the prompt.

### UGC 1 — "Skin that's lived a little" (mode: `ugc`)
*Avatar: woman, late 40s, warm, natural makeup, bathroom.*
> Hook (0–3 s): "Okay, I'm 48 and I was so over paying for salon treatments."
> (3–9 s): "This is Trivelle. Red light, EMS and a suction massage, all in one little device. I use it about ten minutes, a few nights a week, with the gel."
> (9–13 s): "It feels like a warm massage with a tiny tingle. My skin just looks smoother and more awake."
> CTA (13–15 s): "It's got a thirty-day money-back guarantee, so honestly, just try it."

### UGC 2 — Unboxing (mode: `ugc_unboxing`)
*Avatar: woman, 30s, bright bedroom.*
> "It's here! So this is the Trivelle kit. You get the device, the face and body heads, the charger, and this gel. Look how small it is, it's cordless. Three modes: glow, lift, sculpt. I'm doing my thighs tonight, I'll report back."

### UGC 3 — How I use it (mode: `ugc_how_to`)
*Avatar: woman, 50s, bathroom vanity.*
> "Here's my ten-minute routine. Thin layer of gel. Pick a mode, start on level one. Then slow upward strokes, keep it moving. Red light on my face, suction on my arms. Wipe off, moisturiser, done. That's it."

### UGC 4 — Product review (mode: `product_review`)
*Avatar: woman, early 40s, sitting on couch.*
> "Honest review after a few weeks. What I like: it's cordless, it's quick, and it actually feels nice. What to know: you need the gel for the EMS, and you've got to be consistent, three to five times a week. For under a dollar a session, I'm keeping it."

### UGC 5 — Hook test variants (mode: `ugc`, same body as UGC 1, swap the first line)
- "Things I stopped paying for in my 40s: salon body treatments."
- "If your skin has lived a little, watch this."
- "Ten minutes, three rituals, one device."
- "My bathroom drawer was full of gadgets. Now it's this."

**Rules for every script** (keeps Meta and the ACCC happy):
- Say "looks smoother / firmer-looking / feels", never "removes cellulite", "burns fat", "tightens skin" or "clinically proven".
- No before/after claims, no percentages.
- Don't mention "4-in-1" or heat — the device is 3-in-1.

---

## Step 3 — Product motion clips (Image-to-Video)

Model: Seedance (or Kling) · 9:16 · 5 s · start image from `2-start-frames/`. Prompts:

| File | Prompt |
|---|---|
| 01 stomach | Slow push-in. Her hand glides the white device in a slow upward stroke across her stomach, gel catching the light. Soft bathroom window light. Camera steady. |
| 02 thigh | Static camera. She glides the device slowly up the back of her thigh in one smooth stroke. Natural, unhurried. |
| 03 arm | Gentle handheld drift. She moves the device slowly along the back of her upper arm, calm small smile. |
| 04 lifestyle | Slow push-in on her face and the device. She looks down at it, then up to camera and smiles. |
| 05 roster stomach | Slow push-in. Device glides in a slow stroke across her stomach, gel sheen on the skin. |
| 06 roster thigh | Static. She glides the device up the back of her thigh once, slowly. |
| 07 roster lifestyle | She turns the device in her hand to show the top, then smiles to camera. Slow push-in. |
| 08 bench | Slow orbit right around the device and gel on the marble bench, morning light shifting softly. |
| 09 hero | Slow 15-degree orbit around the device and tube, soft light rays moving gently behind. |

**Every prompt — add at the end:** "Keep the device exactly as in the image: white oval body, grey ring button on top, clear cup with steel rollers underneath. No text, no logos."

Reject any clip where the device changes shape, the cup ends up on top, or text appears.

---

## Step 4 — Ad captions (for Meta / TikTok)

- **Primary text:** Made for skin that's lived a little. Heat, red light, EMS and vacuum massage in one cordless device, for brighter, smoother, firmer-looking skin in about 10 minutes. 30-day money-back guarantee.
- **Headline:** Four rituals. One device.
- **Description:** $219 · 30-day money-back guarantee
- **CTA button:** Shop now

---

If Higgsfield can't do it or runs out, tell Claude "quote Magnific" and it'll price the same clips there.
