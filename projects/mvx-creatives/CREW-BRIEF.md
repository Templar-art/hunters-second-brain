# MVX Video — Crew Brief

**Monday 3 August 2026** · Gold Coast · ~2 hours on the ground, two locations
**Client:** MVX Electrical (Matt) · **Talent:** Matt, to camera
**Deliverable:** 6 vertical ads, 20 seconds each

Talent brief (the lines Matt is saying): [SHOOT-BRIEF.md](SHOOT-BRIEF.md) — **print it or have it on an iPad on set.** Matt won't have memorised it and shouldn't.

---

## Who does what

| Role | Who | Job |
|---|---|---|
| Shooter | _confirm_ | Camera, framing, calls the takes |
| Sound / 2nd | _confirm_ | Lav on Matt, monitors levels, watches for wind |
| Talent wrangler | Hunter | Feeds Matt his lines, keeps him relaxed, decides when a take is good |
| Edit | Lach | 6 cuts, captions, grade |

One person can shoot and monitor sound if it's a two-hander, but **somebody has to be listening on headphones**. Nobody listening is how you get 12 unusable takes.

---

## The shoot — 12 takes, 2 setups

Each ad is filmed in three pieces and cut together after:

- **3 opening lines** (~3s each) — the variable. We test which one stops the scroll.
- **1 middle** (~12s) — identical across all cuts of that ad.
- **2 sign-offs** (~5s each)

Twice over — once for the general electrical ad, once for new builds. **12 takes total.** Shoot everything at setup 1 before moving.

### Setup 1 — General electrical
In front of the van, or at a switchboard. Needs to read as a normal house.

### Setup 2 — New builds
An actual site. Frame up, bare studs, rough-in visible.

⚠️ **Unconfirmed dependency: does Matt have a site we can stand on Monday?** Fallback is Matt with the plans on the ute tailgate. Weaker, but it works. **Confirm before Monday, not on the day.**

**Same shirt at both setups.** Takes get mixed between the two ads in the edit, so wardrobe has to match. Tell Matt this when you confirm the call time — no MVX polo at one and a hi-vis at the other.

---

## Camera

- **4K, 16:9, framed for a centre 9:16 crop.** Cropping 4K down to vertical still lands above 1080×1920, so we keep the resolution and gain room to reframe — plus a 1:1 version later if we want one. Turn on crop guides and compose to them; do not eyeball it.
- **25fps** for all talking. **50fps** for the close-ups so they can be slowed.
- **S-Log3**, per the usual pipeline — Lach's grading it and the finish has to sit with the rest of the MVX work.
- Fast-ish glass, shallow but not silly. Matt should be sharp from ear to ear.
- Eyes on the upper third, **and keep the top ~15% and bottom ~20% clear** — that's where Facebook's own UI and our burned-in captions land. Face and any on-screen text stay out of those bands.

## Sound — this is the one that ruins the day

Outdoor, near a van, on a building site. Wind is the actual risk, not the camera.

- **Lav on Matt**, deadcat on it, cable hidden.
- **On-camera mic as backup**, always running.
- **Headphones on, all day.** Check between setups, not at the end.
- If a plane, a drop saw or a truck goes over a take, call it and go again immediately. It's five seconds to re-do on the day and it's unfixable later.

## Light

- **Avoid roughly 11am–2pm.** Morning or late arvo, or find shade.
- Open shade or backlit with a bounce. No harsh top sun on his face.
- If setup 1 ends up at an indoor switchboard, small LED to lift his face and let the practicals do the rest.

---

## Close-ups — grab after the talking is done

Few seconds each, no camera moves, just hands working. Six to eight per ad is plenty.

**General electrical:** screwing a powerpoint cover on · fan starting up · switchboard door opening · testing a safety switch · downlight going in · van door shutting with the tools.

**New builds:** cable running through studs · marking a stud with a pencil · plans held up · drilling a joist · switchboard rough-in on a bare wall · wide of the frame with someone working in it.

**Check `photos/` first** — `42995.jpg` and `2203.jpg` already cover two of the new-build shots as stills. Don't reshoot what we've got.

---

## Files and handoff

Name on ingest so Lach isn't guessing:

```
MVX_AD1-GEN_HOOK-01_T01.mov
MVX_AD1-GEN_MIDDLE_T01.mov
MVX_AD1-GEN_CTA-A_T01.mov
MVX_AD2-BUILD_HOOK-01_T01.mov
...
MVX_BROLL_AD1_powerpoint-cover.mov
```

Card offload to SSD on the day, both cards, before anything gets formatted. Then SSD → Drive via rclone (see [[rclone-drive-upload]]).

**Circle the takes on set.** Note the take number of the good one against each line while it's fresh. Nobody wants to watch four versions of the same sentence a week later.

---

## Edit — what Lach delivers

**Round 1: 3 cuts per ad, 6 total.** One per opening line, all using the same middle and **sign-off A**. That's it.

Hold sign-off B back. The hooks get tested first; once one wins, sign-off B becomes the next thing we test against it. Cutting all 12 combinations now means 6 of them never run.

Each cut:

- **20 seconds**, 1080×1920, H.264
- **Captions burned in for the whole thing.** These get watched on mute — that's the default, not the exception.
- Opening line also on screen as text, held for the full 3 seconds. **Static, not animated in** — movement competes with the scroll instead of stopping it.
- Brand green on the sign-off only, and no more than about 10% of the frame ([[brand-system]]).
- Close-ups cut under the middle section. Talking head on screen for the opening line and the sign-off.
- One grade across all six so they look like a set.

⚠️ **When these get uploaded: Advantage+ creative enhancements OFF on every ad.** Meta will otherwise re-crop the frame and rewrite the copy — and re-cropping a vertical we deliberately framed for caption safe zones is exactly the damage that setting does. Detail in [BUILD.md](../mvx-meta-rebuild/BUILD.md).

---

## Before Monday

1. **Site access for setup 2** — Matt. The one that changes the plan.
2. **Confirm Matt's on camera.** The whole "we are the electricians" angle only works owner-led.
3. **Two lines need Matt's yes** — *"we turn up when we say we will"* and how we describe the lighting/power work. Both flagged in [SHOOT-BRIEF.md](SHOOT-BRIEF.md).
4. **Call time and wardrobe** to Matt, with the brief attached.
5. Batteries, cards, lav batteries. Deadcat.

---

_Vault: [[mvx-electrical]] · scripts + reasoning: [VIDEO-SCRIPTS.md](VIDEO-SCRIPTS.md) · talent brief: [SHOOT-BRIEF.md](SHOOT-BRIEF.md)_
