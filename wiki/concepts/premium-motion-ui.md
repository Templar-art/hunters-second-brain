---
type: concept
tags: [motion-graphics, ui-ux, remotion, design-system, research]
status: active
updated: 2026-10-16
---
# Premium motion UI — specs for on-video graphics

Research on what makes on-screen UI (cards, pop-ups, chips, charts) read as *premium* rather than *template* (16 Oct 2026). These are concrete numbers for the Remotion pipeline. Read with [[hormozi-style-motion-playbook]] and [[talking-head-edit-standards]].

## 1. Springs: Apple's model, converted to Remotion
Apple defines springs by **duration + bounce** (WWDC23 "Animate with springs"). Remotion's `spring()` takes mass/stiffness/damping. Convert with mass = 1:
- `stiffness = (2π / duration)²`
- `damping = 4π · (1 − bounce) / duration`

| Use | duration | bounce | stiffness | damping |
|---|---|---|---|---|
| Default UI move (cards, panels, titles) | 0.5s | 0 | 158 | 25 |
| Small bounce (chips, pins, tick boxes) | 0.5s | 0.15 | 158 | 21 |
| Playful pop (only things "thrown" in) | 0.6s | 0.2 | 110 | 17 |

**Rule (Apple-derived):** critical damping (no overshoot) is the default. Save bounce for things with implied momentum, like a pop-up flicked in or a button press. Overshoot on something that simply fades in feels cheap.
⚠️ **Audit of v6:** `Pop` uses stiffness 260 / damping 12, which works out to about 0.39s with **~0.6 bounce**. That's too springy for "premium". Move it to the small-bounce row in v7. Card entrances at 90/20 are fine (soft, about 0.66s, bounce ~0).

## 2. Easing
- Never linear. Use expo/cubic **out** for entrances and cubic **in** for exits. Exits should be faster than entrances (roughly 60%).
- For "snappy" energy: a sharp ease-in, then a long ease-out.

## 3. Depth and material
- **Layered shadows, not one shadow.** Combine a tight contact shadow with a wide soft ambient one, e.g. `0 1px 2px rgba(0,0,0,.25), 0 12px 40px rgba(0,0,0,.25)`. One big blurry shadow looks flat.
- **Glass only on elevated, temporary layers** (pop-ups, notifications, chips over footage), never behind body text. Use a `backdrop-filter: blur(20px) saturate(1.4)`, a thin edge highlight (1px border at ~30–50% white on light, ~12% white on dark), and a faint top-left inner gradient.
- Apple's 2025 "liquid glass" refracts rather than just blurring. For video, fake it with a subtle highlight sweep across the card on entrance.
- **Glow/shadow bloom** marks the *active* state (the current caption word, a selected checkbox), never every element.

## 4. Choreography
- **Stagger**: 40–80ms between siblings. Anything slower reads as sluggish, anything faster reads as all at once.
- **Lead with the container, then the content.** The card lands first and its text follows 80–120ms later.
- **Masked line reveals** for headlines: the text slides up inside a clip (already done in `Title`).
- **Parallax** on scene entrances: background layers move about 0.6× as far as foreground cards, for cheap depth.
- **Motion blur** only on fast linear moves (slide-ins, punch-ins), never on big wipes (the v5 ghosting lesson).

## 5. Animate the right properties
- transform/opacity → movement and press feedback
- blur/filter → focus pulls and softened entrances (blur 12px → 0 as a card lands reads very premium)
- clip-path/masks → wipes and editorial reveals
- shadow/glow → active state and focus

## 6. Typography in motion
- Use a condensed display face for titles and mono for eyebrows (current system). Tighten tracking on big titles (−1 to −2%) and open it up on small caps/mono (+5–8%).
- Never animate letter-spacing on body text, and never let text scale past 1.08 in a pop.

## v7 actions (from round 1 — see round 2 below for more)
1. Retune all springs to the table above. Bounce only on chips, pins and the follow click.
2. Layered shadows + glass treatment on pop-ups/chips/recap over footage.
3. Entrance focus-pull (blur 12→0) on cards.
4. Container-then-content stagger on every card (80–120ms).
5. Highlight sweep on the follow card and recap card.
6. Parallax on scene push (background vs cards).

## Sources
- Apple WWDC23 "Animate with springs": https://developer.apple.com/videos/play/wwdc2023/10158/
- Apple-design skill summary (secondary): https://www.ui-skills.com/skills/emilkowalski/apple-design/
- Setproduct — glass vs liquid glass 2026: https://setproduct.com/blog/liquid-glass-vs-glassmorphism
- Soft-glass design kit (edge-highlight values): https://cdn.jsdelivr.net/npm/@wrongstack/core@0.295.1/design-kits/soft-glass/KIT.md
- UX Collective — motion design principles: https://uxdesign.cc/a-guide-to-motion-design-principles-7f05f10ccd79
- Impeccable motion reference (properties → effects): https://git.secluded.site/agent-skills/blob/main/vendor/impeccable/skill/reference/motion-design.md?raw=1
- Miracamp — motion graphics techniques: https://www.miracamp.com/learn/motion-graphics/best-techniques-mg

## Research round 2 (16 Oct 2026): safe zones, sound sync, caption readability

### 7. Platform safe zones (1080×1920)
The guides disagree, and the figures are third-party and measured, not official. The consensus:
- **Cross-platform safe area ≈ 900×1400, centred** → x 90–990, y ~260–1660.
- **Reels bottom dead zone grew in late 2025.** Keep captions **at least ~450–480px above the bottom edge**, i.e. y ≤ ~1440. TikTok blocks ~250–320px at the bottom (+50 for ad CTAs).
- **Right side:** the like/comment/share rail needs ~84–180px clear.
- **Top:** keep ~220–260px clear (platform header).
- **Caption size:** 65–70px recommended, never below 55px for primary captions.

⚠️ **Audit of v6 against this:**
| Element | Where it sits | Problem | Fix in v7 |
|---|---|---|---|
| Captions during graphic scenes | y 1560 | inside the Reels bottom dead zone | raise to ≤ 1400 and shrink the scene cards to make room |
| "Nutrition" chip | right edge ~1050 | under the right-side button rail | keep right edge ≤ 900 |
| Face circle in scenes | x 700–1000 | grazes the button rail | x 640–940 |
| Captions on talking head | y ~1100–1260 at 60px | OK. 60px is within spec (Hunter wants subtle) | keep, maybe 64px |
| Name tag / recap / follow card | top ~220–260 | borderline with the platform header | start at y ≥ 260 |

### 8. Sound ↔ picture sync (practitioner rules)
- **Whoosh:** start early so its *peak* lands on the fastest frame of the move. Our whoosh peaks ~0.35s after it starts, and expo-out moves are fastest at frame 0 → start it ~0.35s *before* the move. v6 starts it only 0.15s early, so it lands ~0.2s late. **Fix.**
- **Click/tap:** on the frame the button visibly depresses, or 1 frame early. Late reads as out of sync.
- **Impact:** exactly on the impact/flash frame.
- **Before a big reveal:** 3–8 frames of near-silence (duck the music).
- **Beat snapping:** frames per beat = fps × 60 / bpm → 30 × 60 / 96 = 18.75 frames at our 96 bpm bed.
- Keep every cue in the same event list as the visuals (our `SoundDesign` already does this) so sound and picture can't drift.
- A UI micro-interaction's sweet spot is ~0.5s (15 frames). Anything under 2 frames doesn't register.

### 9. Caption readability (research)
- A 2024 kinetic-typography study (Dolić et al.) found an *optimal word rate* and showed that the interpolation/easing choice changes readability. Smooth eased motion helps; jittery motion hurts.
- Deaf/HoH viewers prefer ~6-word lines over single-word captions, because they split attention with the video. Short-form RSVP style (1–3 words) trades comprehension for punch. → Our 3-word pages are a reasonable middle. Don't go to single words.
- Kinetic text slows reading (Hillner 2005) → keep caption motion small (≤8% scale pop, already done). Save big motion for titles.
- Arm's-length test: if a line can't be read with the phone at arm's length, it's too long, thin, low-contrast or fast.
- When there's voiceover, on-screen *titles* should summarise, not duplicate (the captions already carry the words).

### Sources (round 2)
- Vidpros — vertical video safe zone: https://vidpros.com/vertical-video-safe-zone/
- Adaptlypost — social safe zones 2026: https://adaptlypost.com/blog/social-media-safe-zones-2026-complete-guide
- Trymypost — safe zones & templates 2026: https://www.trymypost.com/blog/social-media-safe-zones-templates-2026
- Argil — Reel size spec 2026: https://argil.ai/blog/instagram-reel-size-e350f
- Blitzcut — caption size for Reels 2026: https://blitzcutai.com/blog/best-caption-size-instagram-reels-2026
- Motion-designer skill (sound sync rules): https://skills.sh/ncklrs/startup-os-skills/motion-designer
- Adobe Research — MoSound (CHI 2026): https://research.adobe.com/publication/mosound-an-interactive-tool-for-generative-sound-design-in-motion-graphics/
- Dolić et al. 2024 — kinetic typography: https://www.grid.uns.ac.rs/symposium/download/2024/89.pdf
- Glasser et al. 2021 — caption width (W4A): https://par.nsf.gov/servlets/purl/10253921
- Kairos — futures for captioning: https://kairos.technorhetoric.net/23.1/topoi/zdenek/conclusion.html
- Nemo — kinetic typography for ads: https://www.nemovideo.com/blog/kinetic-typography-product-ads
