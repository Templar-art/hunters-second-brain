---
type: concept
tags: [ai-video, blender, higgsfield, magnific, pipeline]
status: setup-complete
updated: 2026-10-26
---
# Blender block-out → AI video pipeline

Claude builds a rough 3D block-out (grey geometry, real metre sizes, locked camera path) in Blender, renders a clay/depth pass, and that pass becomes the structure reference for a video-to-video or first/last-frame generation in [[higgsfield-pipelines|Higgsfield]] or Magnific. The block-out fixes camera motion and proportions; the AI only paints the surface. This removes AI video's main failure, random camera drift.

## Install (done 2026-10-12)
- Blender 5.2.2 via Homebrew cask (`/Applications/Blender.app`, CLI `blender`).
- `blender-mcp` server (PyPI, run via `uvx`), registered user-scope in Claude Code as `blender` with `DISABLE_TELEMETRY=true`.
- Addon "MCP for Blender" v1.8 (`~/BlenderMCP/addon.py`, github ahujasid/blender-mcp) installed and enabled in Blender prefs. Addon telemetry is off by default; leave it off. Optional paid add-ons (Hyper3D, Sketchfab, premium) are not needed.
- Headless test passed: Claude rendered a grey room block-out with `blender -b -P script.py` in about 3s.

## Two modes
- **Headless** (no UI): Claude writes `bpy` scripts and runs them with `blender -b`. Best for automated batches.
- **Live MCP**: Blender is open and the addon's "Connect to Claude" is clicked, so Claude edits the scene in real time. Best for iterating with Hunter watching.

## Alternative
Magnific's MCP has a built-in 3D Scene builder (cameras, keyframes, captures) that appears free to build in. Only the generation step is metered. Untested at the time of setup.

## Rules
Building the block-out is free. The generation step always gets a cost quote and Hunter's go-ahead first. Never full-frame a drone wide (see [[staging-rules]]).

## Block-outs built
- 2026-10-12: [living-room-pushin-v1.blend](../../projects/blender-blockouts/living-room-pushin-v1.blend), the first live-MCP test. A 5×4m room with the sofa on the back wall and a 24mm push-in from 1.9m to 0.5m back over 5s (120f @24fps). Gotcha: in a script, calling `frame_set()` between keyframe inserts re-evaluates the animation and overwrites the new pose, so pass `frame=` to `keyframe_insert` instead.

## Default route (2026-10-12, Hunter picked it after the shot-1 test)
Blender guide frame → **GPT Image 2.5 Sunburst** (high, 2K, about 2.75 HF credits) for an **editorial** look → **Seedance 2.5 on Higgsfield** (omni_reference start frame, 96 HF credits per 8s at 1080p). Kling 2.5 on Magnific (725cr for the test) held the move but redesigned the pool late in the clip, so it is not the default.

## Material-ID colour map (2026-10-16)
Each material is rendered as one flat colour, then passed to the image model as a second reference with a key written in prose ("wherever Image 2 is red, the surface is timber…"). The model then knows which surface is which instead of guessing. Script: [material_id_pass.py](../../projects/blender-blockouts/scripts/material_id_pass.py) sorts every material by name into 17 categories: red timber, cyan glass, grey concrete, white render, black metal, blue pool, navy ocean, yellow sand, green grass, dark green plants, brown trunks, magenta fabric/furniture, orange stone, and so on. It uses Standard view transform and flat emission so the colours stay exact. Thin glass (fences, balustrades) is hidden from the map so it doesn't paint over what sits behind it.

## Scene density matters
Hunter's verdict on the first beach build (274 objects): too bare. The rebuild went to about 1,600 objects: dune-grass scatter, hedges, tropical garden beds, potted plants, outdoor dining, an umbrella, mullions, gutters and downpipes, a boardwalk, street lights, cars, eight detailed neighbour houses, and a full walk-through interior (stairs cut through the slabs, a garage, laundry, powder room, and a master suite with ensuite and robe). An empty block-out gives the AI room to invent; a dense one leaves it nothing to make up.

## Add-ons worth installing (research, 2026-10-16, not yet verified live)
Ranked for a Python/MCP-driven pipeline:
1. Poly Haven (free, already wired in)
2. BlenderKit (free tier / about $9 a month)
3. Camera Shakify (free, real gimbal feel)
4. Archipack (free, parametric walls, windows and roofs)
5. Botaniq (about $49+, landscaping)
6. Photographer 5 (about $30)

Skip Geo-Scatter, Kitbash, Fab and Fluent for now: they're weak to drive from a script. Spend on silhouette, vegetation shape and camera motion, because the AI repaints the surfaces anyway.

**Update from the 23 Oct research pair ([[claude-blender-guides-2026-10]]):**
- ⚠️ **Archipack contradicts the "free" above.** Only the older edition is free. The current 2.x, which advertises Blender 3–5 support, is paid.
- ⚠️ **Geo-Scatter:** the new research recommends it once exterior landscaping is frequent (5.6.4 targets Blender 5.2 LTS; Biome-Reader is a free, limited alternative, and the two must never be installed together). The "weak to drive from a script" call above still stands for our headless kit, which does its own scatter. Revisit only if hand-built exteriors become routine.
- **New: fSpy + its Blender importer** (free). It solves a camera from one still photo, so a Blender camera can match a real listing photo or a scan. Validate the solve against one known dimension. It is still-only; video still goes through the [[plate-vfx]] camera solve.
- The Poly Haven Asset Browser add-on is paid and redundant, because the MCP's own Poly Haven import covers it. Node Wrangler is bundled with Blender.
- **Acceptance test before trusting an add-on via MCP:** inspect read-only first, run one reversible test in a temporary collection, read the values back. Never invent operator names, and never treat "no error" as proof it worked.

## MCP bridge notes (23 Oct research)
- The community package is now `mcp-for-blender`. Our `uvx blender-mcp` config still works, so no migration is needed until something breaks.
- The socket on `localhost:9876` has no authentication, so keep it on localhost. `BLENDER_MCP_SAFE_MODE=1` validates scripts but is not a security boundary.
- The official Blender Lab MCP is a separate product (API and manual lookup, file audits). Never connect both bridges at once.
- `generate_3d` and the premium asset services are separately metered, so they fall under the cost gate.
- Long Cycles renders time out the tool call. Render previews small over MCP and finals headless (`blender -b`).

## Install audit against the Mac mini checklist (26 Oct)
Audit of this Mac (Mac mini, M5 Pro, 48 GB, macOS 27.0.1) against the [install checklist](../../raw/blender/mac-mini-claude-blender-install-checklist-2026-10-26.md):

| Checklist item | State |
|---|---|
| Blender stable Apple Silicon | ✅ 5.2.2 LTS, arm64. The checklist targets 5.2.3, an optional patch update. |
| Claude Code | ✅ 2.1.222 |
| uv / uvx | ✅ 0.11.28 (Homebrew) |
| MCP registered | ✅ as `uvx blender-mcp`, which prints the rename notice but works. Deliberately scoped to the vault rather than the checklist's separate `~/Documents/10x-Blender` folder. |
| Telemetry off | ✅ `DISABLE_TELEMETRY=true` |
| Safe mode | ❌ **off by Hunter's decision (26 Oct).** The checklist wants it on, but it gives little protection here and adds friction for the live scripts. |
| Socket local only | ✅ |
| Metal GPU | ✅ Metal, with the 20-core GPU enabled and the CPU unticked |
| Acceptance tests | ✅ effectively passed; the MCP has driven every build since 12 Oct |
| Node Wrangler | not enabled (bundled; enable when needed) |

✅ **Duplicate add-on fixed (26 Oct):** `scripts/addons/` held two identical copies of MCP for Blender v1.8, `addon.py` and `blender_mcp.py`, and both were enabled. That caused an unregister exception when Blender quit. The `addon` module is now disabled and the user prefs saved; only `blender_mcp` loads, and Blender quits cleanly. The `addon.py` file is still on disk but inactive. Prefs backup from before the change: `$TMPDIR/userpref-backup-2026-10-26.blend` (temporary).

**Add-on updated to protocol 15 (26 Oct):** `uvx mcp-for-blender install-addon` brought the add-on up to the server's protocol; the old v14 had made newer features run on fallbacks. **The installer rewrites both `blender_mcp.py` and `addon.py` every time**, so the duplicate file comes back on each update. That's harmless while the `addon` module stays disabled. The installer also leaves the files world-writable (666), so `chmod 644` them after updating. Restart Blender afterwards. The live check passed: protocol 15, up to date, telemetry off.

✅ **Poly Haven, Sketchfab and Poly Pizza search turned on (26 Oct)** in the add-on's N-panel and confirmed via `get_addon_status`. They had been off, contrary to "already wired in" above. The 3D generators (Hunyuan3D, Hyper3D, Meshy, Tripo) stay off because they are metered.

## When Blender is the final pixel (no AI repaint)
Most of the pipeline uses Blender only as a guide frame. For shots where the render *is* the deliverable, follow the photoreal checklist and critique loop in [[claude-blender-guides-2026-10]]:
- Bevel every hard edge.
- Light from the HDRI first, adding a sun only to match the HDRI's direction.
- Use AgX and save as EXR.
- Keep albedo between 0.03 and 0.9 and vary the roughness.
- Score each render on an 8-axis rubric and apply fixes one at a time from the same camera.

Floor checks test **support points against the support surface**, not "lowest point at z = 0".

## Model shootout: guide + colour-ID map, same prompt (2026-10-16, 12.25 HF credits)
Run on the beach house pool shot. Grid: [shootout-grid.jpg](../../projects/blender-blockouts/beach/shootout/shootout-grid.jpg).

| Model | Result |
|---|---|
| **Seedream 5.0 Pro** (2.5 cr) | Most photographic and closest to the layout. It turned the hedge into a concrete wall. Default when realism matters. |
| **GPT Image 2.5 Sunburst** (2.75 cr) | Most editorial and lush, but it re-framed slightly and swapped some elements. Default when the editorial look matters. |
| **Nano Banana 2.1** (2 cr) | Very real, but leaked the magenta and lavender key colours into the image. |
| **FLUX 3** (3 cr) | Faithful, got the hedges right, slightly CG-looking. |
| **Nano Banana Pro** (2 cr) | Weakest; heavy key-colour leaks. |

**Lesson:** key colours that look like real paint (magenta, lavender) leak into the image. Neighbour houses now share the house-render white, and people moved to purple.

## People and camera realism (2026-10-16)
- **MPFB2 2.0.18** (free, official Blender extension, 46MB, checksum-verified) is installed. `HumanService.create_human(macro_detail_dict=…)` takes gender, age, height, weight and muscle; `add_builtin_rig(h,"default")` adds the skeleton. The body faces −y. Bending the leg forward is upperleg01 −X; the knee bends on lowerleg01 +X. Arms rest at upperarm01 Z −45 (L) / +45 (R) from the A-pose. A walk cycle is upperleg ±23°, knee 4–38° and arm swing ±14° over 26 frames with CYCLES modifiers. Each human is parented to a `Rig_` empty that carries its walk path. No clothes or skin pack yet; the AI dresses them from the prompt.
- **Camera Shakify 0.5.1** (free, 78KB) is installed. Walking shots use WALK_TO_THE_STORE at 0.25–0.35; static or glide shots use INVESTIGATION at 0.15–0.2. It replaces the generic F-curve noise on those cameras.
- **Tracking shot:** the camera keeps a TRACK_TO on an empty that copies the walker's location at chest height, while the camera itself runs a parallel path.

## Beach build — video results (16 Oct, harvested 20 Oct)

Job: [JOB.md](../../projects/blender-blockouts/beach/JOB.md). **Status: done (Hunter confirmed 2026-10-26).** Total spend is 791.5 HF credits, of which 672 went on video.

- **Stills:** Hunter picked GPT Image 2.5 Sunburst for all 7 shots. Seedream copied the Blender low-poly palms literally, failed the top-down shot and invented a pool.
- **Video:** 7 × Seedance 2.5 (8s, 1080p) from the Sunburst stills, with no cast refs (refs would have cost 128 per shot). Shots 03, 04 and 05 passed. 02 passed with minor props appearing. 01 barely moves. 06 dissolves and morphs at about 2s. 07: the car doesn't roll. Rough cut: `projects/blender-blockouts/beach/video/rough-assembly-v1.mp4` (local only, media is gitignored).
- **Face test on shot 06** (Hunter: faces were messing up): Kling 3.0 Pro (12.5) against Veo 3.1 Fast (32). Both held faces in one continuous take. Kling gave a true sideways track with a stable background. Veo gave sharper faces, but the background houses drift late. Side-by-side: `video/facetest/facetest-side-by-side.mp4`.
- **Lesson:** Seedance from a still is fine for empty-architecture moves (03/04/05) but weak for people and vehicles. For shots with people, Kling 3.0 Pro is the cheapest clean option tested.
- **Closed 2026-10-26:** Hunter confirmed the people-shot model pick, the 01/06/07 re-rolls and the re-cut are done. Which model won and the final spend weren't recorded here.

## Kit v1: spec-driven builds (20 Oct)

Hand-building is replaced. Scenes are now described in a `scene.json` and built headless by the [Blender kit](../../projects/blender-kit/README.md) (modules: site, landscape, people, cameras, passes, plus an asset library extracted from the beach scene). **The beach rebuild took 4.3 s instead of about 6 h**: 1,729 objects against 1,768, 78 of 86 object families matching exactly, and all 8 guide frames lining up ([compare sheet](../../projects/blender-blockouts/beach/kit/build/compare-guides.jpg)). Density and camera clearance are checked automatically on every build. The house is still imported until phase 4 (house generator) of [[job-framework-v2]].

**Gotcha:** Blender 5 uses layered actions, so `action.fcurves` is gone. Use `bpy_extras.anim_utils.action_get_channelbag_for_slot(action, slot).fcurves` (wrapped as `core.fcurves`).

## House generator (20 Oct)

`house` module: a plan-derived spec goes in and a full multi-level shell comes out in under 0.1 s (see the [kit README](../../projects/blender-kit/README.md)). Tested on Lot 48 from the summary facts; the real plans weren't on the Mac. Next real job: read the plan PDF's dimensions into the spec at Gate A, and Hunter checks the summary table before the build.

## Coastal drone-reveal test (26 Oct)
The first fully kit-built scene, with no imported geometry: an invented two-storey beach house from the `house` generator on the beach site, and a street-to-ocean drone reveal (8 s, 24 mm). Built in about 4 s, with guide and ID frames at the start, middle and end. Job: [JOB.md](../../projects/blender-blockouts/coastal-test/JOB.md). Waiting on Hunter's go for Sunburst stills (about 8 HF).

**Three kit bugs found and fixed on this build:**
1. `core.copy_obj` copied the library template's hidden flag, so **every kit tree has been invisible since v1**, including in the beach rebuild. Placed copies are now forced visible.
2. In the ID rules, "foot**path**" matched `path → timber` before it reached its own rule, so footpaths and driveways rendered timber red. They are now concrete.
3. `island_tree` materials matched the kitchen-island `island → stone` rule, so tree trunks rendered stone orange. They are now trunk brown.

Shots can list `guide_frames` (frame offsets) to get guide and ID frames at the start, middle and end, which first-and-last-frame video needs.
