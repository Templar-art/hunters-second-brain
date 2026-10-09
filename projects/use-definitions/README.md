# USE Definitions — episode template

Turns a raw talking-head clip of Sam into a finished "Definitions" episode in the series look (MCP / API / CRUD).
Local and free: Chrome canvas + Playwright, ffmpeg, faster-whisper (word timings), rembg (person cut-out), synthesised SFX.

Wiki: `wiki/projects/use-definitions-series.md` (the style rules and the lessons).

## New episode in four steps

```bash
tools/prep.sh ~/Downloads/<clip>.mp4 <name> [0-4 19-21]   # frames, words.json, cut-outs (all frames, or just these second ranges), starter episode.js
```
1. Read `episodes/<name>/words.json` and fix any misheard words (e.g. "EU Software" → "USE Software").
2. Edit `episodes/<name>/episode.js`: set `dur`, `voEnd`, caption windows, punch-ins, and the `frame(T)` scene list using the word times. Copy the CRUD episode's structure and swap the content.
3. Check stills while you work:
   ```bash
   NODE_PATH=tools/node_modules node tools/render.cjs episodes/<name> stills 1.0,5.5,12.0
   ```
   (written to `episodes/<name>/build/qa/`)
4. Build:
   ```bash
   tools/build.sh <name> v1     # → episodes/<name>/<name>-v1.mp4
   ```
   Drop a `music.wav` in the episode folder and it gets ducked under the voice automatically.

## Components (engine/engine.js)
Each component has a matching `.cue(...)` that registers its sound effects, so audio always follows motion.

| Component | Use |
|---|---|
| `titleCard(T, term, out)` | opening: "Definitions" + giant term behind the head + shards |
| `lowerThird(T, a, b, name, role)` | logo / divider / Sam Bruhn · FOUNDER & CEO |
| `captions(T)` | auto-chunked word captions with the sliding cyan highlight, inside `EP.captions` windows `[a, b, y]` (y can be a function of T) |
| `defCard(T, a, b, term, say, under)` | dictionary card, whips out at `b` revealing `under` |
| `standsFor(T, a, b, label, [[L, rest, t]...])` | navy acronym slide, speaker in an inset that expands back to full frame |
| `behindHead(T, a, b, word, tag)` | giant word behind the head on the talking head, optional cyan tag |
| `terminal(T, a, b, line1, line2)` | navy terminal card typing a command |
| `okCard(T, a, shatterAt, json)` | "200 OK" response card, then a triangle shatter |
| `mosaic(T, a, seed)` | triangle mosaic wipe; cut the scene underneath at `a + .4` |
| `panel(top)`, `faceCircle`, `pill`, `iconUser`, `iconDB`, `whip(T, a)` | building blocks for custom slides |
| `endCard(T, a, dur)` | white USE / Definitions end card |

Helpers: `th(rect, zoom, ay)` draws the speaker, `cutout(zoom, ay)` draws him on top (text behind head), `rise()` and `typeOn()` are the two text entrances, `expo` is the series curve.

## Rules that keep it on-brand
- Framing `BZ = 1.22` (cut at the thighs); punch-ins are ×1.12 on phrase starts.
- Captions only over the talking head, never over slides.
- Hard cuts or whips between scenes; triangle mosaic into and out of the big slides; always end on the white end card.
- Anything invented (example names, URLs, JSON) gets checked with USE before posting.
