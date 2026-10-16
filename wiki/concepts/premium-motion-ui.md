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

## v7 actions (from this research)
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
