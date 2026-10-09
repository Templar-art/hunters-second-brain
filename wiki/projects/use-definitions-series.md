---
type: project
tags: [motion-graphics, talking-head, template, use-software]
status: in-review
updated: 2026-10-09
---

# USE Definitions series: CRUD episode + template

Client: [[use-software]]. Brief from Hunter, 9 Oct 2026: take a raw talking-head clip of Sam explaining CRUD (20s, 4K, 25fps) and make it "very similar" to their existing MCP and API episodes.

**Deliverables:**
- CRUD: `projects/use-definitions/episodes/crud/crud-v6.mp4` (23.6s, 1080x1920, 30fps; template build, stereo SFX, no end freeze). v1–v5 are in `projects/use-crud-talking-head/`.
- Bus case study (22 Oct clip, 46s): `projects/use-definitions/episodes/bus-network/bus-network-v2.mp4` (49.8s). v2 replaced v1 after Hunter's "it has to do other animations… different layouts": animation kit v2 plus new layouts (floating card stage, bento grid). Sam's "favourite build": an on-time tracking rebuild for an unnamed transport operator. The job log is `projects/use-crud-talking-head/JOB.md`.

**Template:** `projects/use-definitions/`. See its README.

**Cost:** 0 credits. Everything runs locally: Chrome canvas driven by Playwright, ffmpeg, faster-whisper for word timings, rembg for the person cut-out, and sound effects synthesised in Python. Magnific music/SFX were quoted (80cr per 30s track, 20cr per SFX type ×4 takes) but not run.

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

## What it taught us
- **Ask which brand, and ask for the series' own past episodes up front.** v1 and v2 were built off the wrong reference: an Empire Technologies ad that Hunter sent only for its motion feel. v1 copied Empire's colours and logo, v2 swapped in USE colours but kept the wrong style. Both were rejected ("dog shit"). The fix was the client's own MCP/API episodes, so ask for those first next time.
- **Match the references side by side, not from memory.** Each round that improved (v3→v5) came from putting reference and render frames next to each other and from 25fps frame strips of the reference motion. That's how the framing, whip-blur, 200 OK shatter and name-card details were found.
- **Draw the talking head inside the canvas** (pre-extracted frames plus mattes) instead of compositing graphics over video in ffmpeg. That unlocked text behind the head, inset/circle crops, zoom cuts and true motion blur (8 subframes, full-frame shutter).
- **SFX cues should come from the components**, so the sound always matches the motion. That's built into the template.
- **Don't let an episode repeat the same three moves.** v1 of the bus episode reused rise-in, shards and panel for every beat, and Hunter asked for different animations and layouts. Pick a different move and layout per beat from the kit.
- **SFX engine v2** (`tools/sfx.py`): stereo, layered transients, room reverb, plus risers, chimes and an end-card swell. Still synthesised; a Magnific SFX pack is the upgrade path (about 120cr).
- **Mattes only where needed.** A full-clip person matte runs about 1s per frame. Pass second ranges to `prep.sh` so only the title and behind-the-head shots get cut out.
- Source clips end a few frames after the last word. The template ping-pongs the final 12 frames so Sam never freezes under the end-of-clip graphics.

## Open
- Bus episode: the trip-log rows, before/after bar lengths, trend line and "ONGOING" tag are illustrative, not client data. Check them with USE. The end-card title "Case Study" is a placeholder until they confirm the series name.
- Music bed: none yet. Waiting for the series track, or a go-ahead to spend Magnific credits.
- USE to approve the invented content: table names, `api.example.com`, and "say: see · are · you · dee".

## Links
[[use-software]] · [[brand-system]]
