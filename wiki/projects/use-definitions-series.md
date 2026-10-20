---
type: project
tags: [motion-graphics, talking-head, template, use-software]
status: in-review
updated: 2026-10-20
---

# USE Definitions series: CRUD episode + template

Client: [[use-software]]. Brief from Hunter, 9 Oct 2026: take a raw talking-head clip of Sam explaining CRUD (20s, 4K, 25fps) and make it "very similar" to their existing MCP and API episodes.

**Deliverables:**
- CRUD: `projects/use-definitions/episodes/crud/crud-v6.mp4` (23.6s, 1080x1920, 30fps; template build, stereo SFX, no end freeze). v1–v5 are in `projects/use-crud-talking-head/`.
- Bus case study (22 Oct clip, 46s): `projects/use-definitions/episodes/bus-network/bus-network-v2.mp4` (49.8s). v2 replaced v1 after Hunter's "it has to do other animations… different layouts": animation kit v2 plus new layouts (floating card stage, bento grid). Sam's "favourite build": an on-time tracking rebuild for an unnamed transport operator. The job log is `projects/use-crud-talking-head/JOB.md`.

**Template:** `projects/use-definitions/`. See its README.

**Cost:** 120 credits (Magnific SFX library, 9 Oct, approved by Hunter); everything else is 0. Everything runs locally: Chrome canvas driven by Playwright, ffmpeg, faster-whisper for word timings, rembg for the person cut-out, and sound effects synthesised in Python. Magnific music/SFX were quoted (80cr per 30s track, 20cr per SFX type ×4 takes) but not run.

## The series look (what "very similar" means)
Measured from the MCP/API reference episodes:
- **Footage:** full-frame talking head framed tight (cut at the thighs, face about a quarter of the way down), with punch-in zoom cuts on phrase starts.
- **Captions:** 2–4 words at a time, Barlow Condensed, white with a soft shadow, sitting on his chest. A **cyan highlight box slides** from word to word, and each chunk rises in from a mask.
- **Title:** "Definitions" mono label plus a giant term placed **behind his head** (needs a person matte).
- **Lower third:** white card with the USE logo, a divider, "Sam Bruhn / FOUNDER & CEO", and a moving cluster of triangle shards on the corner.
- **Shards:** blue low-poly triangles fly in on an expo-out and drift. They're the series' signature.
- **Transitions:** a full-screen **triangle mosaic** wipe, and vertical **whip-blur** exits on slides.
- **Slides:**
  - Light dictionary card (DEFINITIONS · NOUN pill, giant term, "say: …").
  - Navy "X stands for" slide, with Sam in an inset box and the first letters in cyan.
  - Light panel rising under the talking head with a node diagram.
  - Full light slide with method pills, a giant verb and a data table.
  - Navy terminal card.
  - "200 OK" response card that shatters into triangles.
  - White end card: logo, "Definitions", "understand · solve · execute", URL.
- **Motion:** expo-out entrances (~0.45–0.6s), quick in-out exits, and heavy motion blur on anything fast.

## Batch (9–10 Oct 2026): 19 episodes delivered
Every episode passed the face check and the boss review. Latest file per episode is under `projects/use-definitions/episodes/<name>/`; `QUEUE.md` is the master list.
- **Definitions (14):** CLI, JSON, SDK, UI/UX, IDE, SaaS, GPU, CPU, Git, Docker, Webhooks, State management, SQL, ERD.
- **Q&A (5):** Excel wince, scope myth, promises, ask the vision, handover. These use the new `qOpener` (QUESTION card). The end card reads "Q&A", a **placeholder series name to confirm with Hunter**.
- **Skipped:** 01 API and 02 MCP (raw clips of the published reference episodes), plus duplicates and the Alex Keith zips.
- **Pipeline added:** OpenCV face tracking with outlier rejection, which drives both framing and the face check. Also `tools/qa.sh`, the `tools/BOSS.md` reviewer loop, `EP.cuts` (motion blur never dissolves across a cut), and frame-centre captions.
- **Lesson:** an early tracker without outlier rejection jumped the framing up to ~700px for a few frames in 5 delivered episodes. They were rebuilt and re-sent. Always smooth and outlier-filter any per-frame tracking that drives the camera.

## Standing rules (Hunter, 9 Oct 2026)
- **Never cover Sam's face.** No overlay may touch his face at any frame. Text behind his head via the matte is fine.
- **Pop-ups never overlay text; text never leaves the frame** (Hunter, 10 Oct 2026). No card, bubble, pill or stamp on top of other text. All text fully on screen with a margin, entrances included.
- **Boss review loop on every episode.** An independent reviewer checks the stills and contact sheet (face clear, variety, brand, no invented facts, captions) and the episode is fixed until it passes, before it's sent.
- **SFX quality:** Hunter rates the current effects poor (synth plus Magnific 1s takes). Needs a rethink.

## What it taught us
- **Ask which brand, and ask for the series' own past episodes up front.** v1 and v2 were built off the wrong reference: an Empire Technologies ad that Hunter sent only for its motion feel. v1 copied Empire's colours and logo, v2 swapped in USE colours but kept the wrong style. Both were rejected ("dog shit"). The fix was the client's own MCP/API episodes, so ask for those first next time.
- **Match the references side by side, not from memory.** Each round that improved (v3→v5) came from putting reference and render frames next to each other and from 25fps frame strips of the reference motion. That's how the framing, whip-blur, 200 OK shatter and name-card details were found.
- **Draw the talking head inside the canvas** (pre-extracted frames plus mattes) instead of compositing graphics over video in ffmpeg. That unlocked text behind the head, inset/circle crops, zoom cuts and true motion blur (8 subframes, full-frame shutter).
- **SFX cues should come from the components**, so the sound always matches the motion. That's built into the template.
- **Don't let an episode repeat the same three moves.** v1 of the bus episode reused rise-in, shards and panel for every beat, and Hunter asked for different animations and layouts. Pick a different move and layout per beat from the kit.
- **SFX engine v2** (`tools/sfx.py`): stereo, layered transients, room reverb, plus risers, chimes and an end-card swell. Upgraded the same day with a real sample library: 6 sound types × 4 takes on Magnific, 120cr, in `sfx-lib/` and reused by every episode. Magnific bills SFX at 5cr per take-second, so 1s takes keep a pack cheap.
- **Mattes only where needed.** A full-clip person matte runs about 1s per frame. Pass second ranges to `prep.sh` so only the title and behind-the-head shots get cut out.
- Source clips end a few frames after the last word. The template ping-pongs the final 12 frames so Sam never freezes under the end-of-clip graphics.

## Open
- Bus episode: the trip-log rows, before/after bar lengths, trend line and "ONGOING" tag are illustrative, not client data. Check them with USE. The end-card title "Case Study" is a placeholder until they confirm the series name.
- Music bed: none yet (Magnific music is 80cr per 30s track).
- USE to approve the invented content: table names, `api.example.com`, and "say: see · are · you · dee".

## Links
[[use-software]] · [[brand-system]]

## v2 redo pass (queued 2026-10-20)

Hunter wants **all 21 sent episodes redone, one at a time**, updated with everything improved since. The main change is real SFX, since the current effects were rated poor; the new sources are Ocular, the free packs and Sound Lab. The redo also uses framework-style gates, automatic video QC and the existing face, QA and boss-review rules. Each episode gets Hunter's look before the next starts. Order and status are tracked in [QUEUE.md](../../projects/use-definitions/QUEUE.md). Nothing is re-sent without Hunter's go. Skipped as already done by USE: API, MCP, SQL, Webhooks. No music, per Hunter.

**01 CRUD v7 (20 Oct): built, awaiting Gate B.** The new SFX kit `sfx-lib-v2` has 75 takes: Ocular Foundation whooshes, thuds and risers, Sound Lab UI pops, clicks, keys and chimes rendered offline via `tools/uikit/render_uikit.cjs`, and the old glass. It is built by `tools/build_sfxkit.py` and selected with `SFX_LIB=sfx-lib-v2`. Engine changes: a `SHUTTER` param, used here as SUB=16 with shutter 0.5 to fix motion-blur banding; the title-card shards are placeable so they stay off the face; and the end card is optionally alive (push-in plus drift) instead of a dead hold. Episodes now declare `cuts` and `qcAllow`, so gen-runner's `qc --edit` can check them. Loudness matches v6. The render takes about 5 min. **Locked by Hunter 20 Oct.**

**02 bus-network v3 (20 Oct): built, awaiting Gate B.** The v7 upgrades are ported. Two v2 defects were caught by the boss sheet: the hook shards beside the ear (moved to the shoulder), and the panel caption jumping down to the panel edge and getting clipped as the panel rose. That caption now holds at y=1200 until the panel pushes it up, a pattern to reuse wherever a caption follows a rising panel. New `tools/qc_episode.py <ep> <ver>` reads `qcAllow` straight from episode.js, after a hand-rolled regex dropped half the windows and gave a false LOOK flag. The render takes about 13 min (49.8 s at 30 fps). Hunter then caught "Simple." and "Standard." overprinting at about 14 s. "Standard." was landing 0.8 s after it was spoken, on the same line. They are now restacked, each on its word. That was standing-rule material, so `tools/lint_rise.py` (headline-overprint check) now runs in `qa.sh` (RISE CLEAR) and is BOSS.md hard rule 6. A sweep of all 21 episodes found no other real case. The fix exposed a 0.8 s FREEZE (gen-runner QC caught it), fixed with buses running the standard grid plus a slow push on the grid only. **Locked by Hunter 20 Oct.**

**03 CLI v3 (20 Oct): built, awaiting Gate B.** gen-runner QC found three static stretches (6.5–9.6 s) in the CRT scene that the 1 s boss sheets never showed. They were fixed with on-story motion rather than a generic drift: a mouse cursor clicks "Get started" on the pretty GUI, and a CRT roll band runs over the old terminal. A slow push alone barely changes pixels on a dark screen, so it doesn't register. An engine fix also landed: `cardStack` labels now measure their real width (they had been hugging the right edge in every episode that uses it). **Locked by Hunter 20 Oct.**

**04 JSON v4 (20 Oct): built, awaiting Gate B.** The file icons and value-type cards now idle-float between beats, because QC flagged them as dead. ⚠️ **Tooling bug found and fixed:** a broken `episode.js` crashed the render, but `build.sh` still printed "built" and re-muxed the *old* picture. zsh `set -e` ignores a failure inside `[[ … ]] || cmd`, and `qa.sh` piped into `tail`. So QC passed a stale file, and only the missing FACE/TEXT CLEAR lines gave it away. `build.sh` now syntax-checks the episode, deletes the old picture before rendering, and refuses to mux without a new one. `qa.sh` runs with `pipefail`. **Rule: if FACE/TEXT/RISE CLEAR lines are missing, the run failed. Never read silence as a pass.**
