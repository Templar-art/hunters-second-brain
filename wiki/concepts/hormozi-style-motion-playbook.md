---
type: concept
tags: [motion-graphics, short-form, editing, hormozi, remotion, research]
status: active
updated: 2026-10-16
---
# Hormozi-level motion playbook

> Context: built for Hunter's personal side work (fitness coach edits, e.g. Tyson's intro reel). Separate from 10x Visuals.

What separates a "someone spent hours on this" short-form edit from a template edit, distilled from research on Alex Hormozi-style editing and chart/motion design (16 Oct 2026). It's the target for the Remotion pipeline (`projects/remotion-pipeline/app/`). Pairs with [[talking-head-edit-standards]] and [[remotion-motion-upgrades]].

## What the Hormozi style actually is
- **Word-by-word highlighted captions** are the constant. The current word is highlighted, set in a bold condensed sans and high contrast. Sources differ on the font (Montserrat Black/Bold-ish).
- **Punch-ins of 10–20%** for emphasis, on cuts and key words.
- **B-roll that adds information**, not decoration. It breaks up the single talking-head angle.
- **Pops, slides and emoji** to reinforce ideas. The 2026 trend is "dynamic minimalism": fewer emoji and SFX, with the voice carrying the energy. → Use SFX sparingly and keep emoji to chips and icons, not confetti.
- One talking-head angle, dark and high-contrast. The edit does the work.

## Charts that read in under 2 seconds
- **One chart, one question, one takeaway.** Never a dashboard.
- **Simplify before animating.** Use direct labels, not legends, and keep 3–4 data points or annotations at most.
- **Motion directs attention.** Wipe-reveal lines left to right, grow bars from the baseline, count numbers up in sync, put a pulsing dot on the leading edge, and pop annotations at the moment the line reaches them.
- Always ease (expo/cubic out), never linear.
- Label made-up data **ILLUSTRATIVE** unless the client gives real numbers.

## Popups that feel hand-made
- **Spring with overshoot** (stiffness ~260, damping ~12), a slight tilt, a soft drop shadow, and an exit that scales back. Not a fade.
- **Anchor to the exact word** (word-level timing). A popup a beat late looks automated.
- **Place it in empty space** beside the head (background and chair). Never over the face, mic or hands. Use face tracking.
- **Types that work:** skill/topic chips with icons, checklist recap cards that tick through, notification-style cards, lower-third name tags, location pins, follow/CTA cards with a cursor click.

## Transitions
- Prefer a **clean push/slide panel** or a hard cut over iris wipes. Motion blur on a big wipe ghosts badly (seen in v5 and fixed in v6).
- **Light leaks: rejected.** Hunter's call, 16 Oct 2026: the orange flare looked off-brand.

## Scripts beat polish
The edit can't add value the script doesn't have. Coach videos should open with a tip, a bold claim or a specific number, not "if you're seeing this you don't follow me yet". Hunter agreed on 16 Oct 2026. Push clients toward value-first scripts before the shoot.

## Next level (not built yet)
- B-roll cards (client gym/food clips) with rounded-corner masks and a slow Ken Burns move.
- Bar-chart comparison and before/after slider components for transformation content.
- Macro breakdown donut (protein/carbs/fat) for nutrition tips.
- Notification-stack popup ("3 new messages from clients") for social proof — real data only.

## Sources
- Riverside — Hormozi-style videos: https://riverside.com/blog/hormozi-style-videos
- Choppity — Hormozi editing style: https://www.choppity.com/tools/recreate-video-editing-style/alex-hormozi/
- Joyspace — does it still work in 2026: https://joyspace.ai/hormozi-editing-style-2026-analysis
- Vidpros — edit like Hormozi: https://vidpros.com/how-to-edit-videos-like-alex-hormozi/
- Online Journalism Blog — charts on video (2026): https://onlinejournalismblog.com/2026/06/23/showing-charts-on-video-here-are-two-essential-techniques-to-make-them-effective/
- Hera — animated infographics: https://hera.video/blog/animated-infographic-video-generator-data-storytelling
