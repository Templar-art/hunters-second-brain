# Claude + Blender MCP: Automation and Photoreal Render Guide

Prepared for 10x Visuals. Updated 23 October 2026. Focus: architectural, interior and property visualisation.

Update note: the community installation section below has been corrected against the current project README. The companion document, “Claude and Blender: Recommended Plugins and Add-ons”, contains the researched extension shortlist, compatibility caveats, and refinements to this guide's recommendations.

---

## 1. What "Blender MCP" means in 2026

There are now two main options, and they are different products:

| Option | Who makes it | Strengths | Notes |
|---|---|---|---|
| Blender Lab MCP Server (official) | Blender developers, blender.org/lab | Code execution, blend-file and object summaries, screenshots, viewport/thumbnail renders, built-in search of the Blender Python API and manual (26 tools) | Officially available for Claude since Apr 2026 ([StraySpark comparison](https://www.strayspark.studio/blog/official-blender-mcp-server-comparison-2026), [LagIndicator](https://lagindicator.com/dev-tools/codex-blender-control-2026-09-10/)) |
| MCP for Blender / blender-mcp (community) | ahujasid, MIT licence | Object/material control, multi-angle "visual verification", Poly Haven, Sketchfab, Poly Pizza, Hyper3D Rodin, Hunyuan3D, Tripo | Not affiliated with the Blender Foundation ([GitHub](https://github.com/ahujasid/mcp-for-blender), [GitHub topic](https://github.com/topics/blender-mcp)) |
| blender-ai-mcp | PatrykIti, Apache-2.0 | Verification-first: bounded tools, measurements and assertions; runs in Docker | ([Blender for Visual Investigation](https://blendervisualinvestigation.com/knowledge-base/docs/addons/blender-mcp/)) |

Recommendation: use the community plugin for asset-heavy scene building (HDRIs, furniture, textures); use the official server when you want grounded API answers and file auditing. Don't connect both to the same session at once.

### How it works
A Blender add-on opens a local socket server (default `localhost:9876`); the MCP server translates Claude's tool calls into commands over that socket ([MEHADI.ME](https://mehadi.me/mcps/blender-mcp/)). Key tools: `get_scene_info`, `get_object_info`, `get_viewport_screenshot`, and `execute_blender_code`, which runs arbitrary `bpy` Python — the "escape hatch" for anything not covered by dedicated tools ([MEHADI.ME](https://mehadi.me/mcps/blender-mcp/)). Newer versions add `look` (scene images), `search_assets`, `import_asset`, `generate_3d` and `get_guide` ([MCP for Blender docs](https://www.mcp-for-blender.com/docs/concepts/how-it-works)).

---

## 2. Setup (community plugin)

The project now recommends `mcp-for-blender` for new installs; existing `uvx blender-mcp` configurations still work ([current README](https://github.com/ahujasid/mcp-for-blender)). The following is the community setup, not the separate official Blender connector.

1. Check your Blender and Python versions against the README's prerequisites, currently Blender 3.0+ and Python 3.10+; individual features and other add-ons still need version-specific checks ([current README](https://github.com/ahujasid/mcp-for-blender)).
2. Install `uv` using the project-recommended platform method, such as `brew install uv` on macOS or `winget install --id=astral-sh.uv -e` on Windows; the project specifically advises against `pip install uv` for this setup ([current README](https://github.com/ahujasid/mcp-for-blender)).
3. For manual Claude Desktop setup, add the following to `claude_desktop_config.json`; safe mode is included as a recommended precaution ([current README](https://github.com/ahujasid/mcp-for-blender)):
```json
{
  "mcpServers": {
    "blender": {
      "command": "uvx",
      "args": ["mcp-for-blender"],
      "env": { "BLENDER_MCP_SAFE_MODE": "1" }
    }
  }
}
```
4. Run `uvx mcp-for-blender install-addon`, enable “Interface: MCP for Blender” in Blender, and fully quit and reopen Claude; the add-on starts its server with Blender, with a manual Start MCP Server option in its sidebar ([current README](https://github.com/ahujasid/mcp-for-blender)).
5. For Claude Code, the documented command is `claude mcp add blender uvx mcp-for-blender`; configure safe mode for that server separately if using Code rather than Desktop ([current README](https://github.com/ahujasid/mcp-for-blender)).
6. Safe mode validates scripts but normal Blender operations, including saving and import/export, remain possible; the socket has no authentication or encryption, so keep it on localhost and do not treat safe mode as a security boundary ([current README](https://github.com/ahujasid/mcp-for-blender)).
7. Check telemetry settings before client-confidential work ([Hysen Labs](https://hysenlabs.com/projects/ahujasid-blender-mcp)).

---

## 3. Capabilities

- Build scenes from a prompt: layout, props, lighting, HDRI environments, cameras ([MCP for Blender capabilities](https://www.mcp-for-blender.com/docs/concepts/capabilities)).
- Create, move, rotate, scale, rename, delete objects; apply and edit materials.
- Generate custom models from text or reference images (Rodin, Hunyuan3D, Tripo).
- Animation: keyframes, turntables, camera moves; basic rigging.
- Self-checking: multi-angle, camera, wireframe, X-ray views and renders so the AI checks its own work ([GitHub](https://github.com/ahujasid/mcp-for-blender)).
- Anything scriptable in `bpy`: render settings, compositor nodes, batch exports, naming clean-up.

## 4. Limitations

- Complex operations need small steps; one giant prompt fails more often ([capabilities docs](https://www.mcp-for-blender.com/docs/concepts/capabilities)).
- Blender needs a GUI; headless needs `xvfb-run`. Only one MCP client per Blender session ([same](https://www.mcp-for-blender.com/docs/concepts/capabilities)).
- `execute_blender_code` can run arbitrary code — always save first ([README](https://github.com/ahujasid/mcp-for-blender/blob/main/README.md)).
- Claude's spatial judgement is weaker than its coding: expect floating objects, intersections, wrong scale, odd rotations.
- Organic/hero modelling is weak; AI-generated meshes are often messy topology with baked lighting in textures.
- Screenshots are low-res — fine detail (noise, fireflies, texture stretching) is easy for the AI to miss.
- Long Cycles renders can time out the tool call; render previews small, finals manually or in background.
- Token/context cost grows with big scenes; ask for summaries, not full dumps.

---

## 5. Best-practice workflow

### Golden rules
1. Real-world units (metres), scale applied (Ctrl+A) — physically based lighting depends on it.
2. One task per prompt; verify with a screenshot after each.
3. Give numbers, not adjectives: "ceiling 2.7 m, sofa 2.2 m wide against north wall, 5600 K key light at 1000 W".
4. Name everything (`WALL_N`, `LGT_Key`, `MAT_Oak`) and use collections — Claude reasons far better over a clean scene graph.
5. Save incremental versions (`scene_v01.blend`…) before each big step.
6. Lock in a camera early and judge everything through it.

### Stage-by-stage prompts

Scene setup
> "Set units to metric, scale 1.0. Create a 6 × 4.5 m living room, 2.7 m ceiling, 0.2 m walls, a 2.4 × 2.1 m window opening on the north wall. Name objects and put them in a ROOM collection. Then take a screenshot from the top and from a 3/4 view and check for gaps."

Camera
> "Add CAM_Main at 1.5 m height, 24 mm lens, sensor 36 mm, aimed at the window corner. Keep verticals straight (camera pitch 0°, use shift Y to frame). Set 3:2 output at 3000 × 2000."

Lighting
> "Download a Poly Haven daylight HDRI suited to an overcast mid-morning, strength 1.0. Add a sun at 35° elevation matching the HDRI direction, 3 strength, angle 0.5°. Add an area light in the window opening as a portal. Use Filmic/AgX, exposure 0."

Materials
> "Create MAT_Oak with Principled BSDF using Poly Haven wood floor 2K textures: base colour sRGB, roughness and normal Non-Color, normal strength 0.5, box mapping at real scale (planks ~0.18 m wide). Add slight roughness variation with a noise texture."

Object manipulation
> "Import a sofa from Poly Haven or Sketchfab, scale to 2.2 m width, place on floor (z bounding-box min = 0), 0.1 m from the south wall, facing the window. Report its dimensions and confirm no intersection with walls."

Render
> "Cycles, GPU, 128 samples preview at 50% resolution with OpenImageDenoise, light paths: max bounces 12, clamp indirect 10. Render and show me the result."

---

## 6. Realism checklist (what actually makes renders look real)

Geometry
- Bevel every hard edge (Bevel modifier, 2–5 mm, harden normals) — perfectly sharp edges are the #1 CG giveaway.
- Add real-world imperfection: slightly uneven cushions, curtains with cloth sim, skirting boards, power points, light switches, cornices.
- Correct scale of everything: door 2.04 m, benchtop 0.9 m, chair seat 0.45 m.

Lighting
- Use an HDRI + matching sun; use light portals at windows for interiors.
- Use real colour temperatures (Blackbody node): daylight 5500–6500 K, warm downlights 2700–3000 K.
- Use IES profiles for downlights/wall washers.
- Contrast ratio: let shadows go dark; don't over-fill.

Materials
- Never pure black/white albedo (keep base colour ~0.03–0.9).
- Roughness variation is more important than colour — add grunge/fingerprint maps to glossy surfaces.
- Glass: real thickness, IOR 1.45–1.52; use 4K textures only for close-up surfaces.
- Avoid visible texture tiling: rotate/offset, use Blender's random-per-tile tricks or mix two scales.

Camera
- Architectural: 16–24 mm, two-point perspective (vertical lines vertical), 1.2–1.6 m height.
- Subtle depth of field for detail shots; a touch of lens distortion, chromatic aberration, vignette and film grain in the compositor.

Render & colour
- AgX view transform (Blender 4+) with appropriate look; render to EXR for grading.
- Enough bounces for interiors (diffuse 4–8, glossy 4–8, transmission 12).
- Final 512–2048 samples + denoise; check for fireflies.
- Grade in DaVinci Resolve or Lightroom like a real photo (white balance, highlight roll-off, local contrast).

---

## 7. Refining renders with AI tools

| Tool type | Use | Tips |
|---|---|---|
| Claude vision (via MCP screenshot/render) | Critique composition, lighting, scale, material errors | Ask for a scored checklist (see section 8) |
| Image-to-image enhancers (Magnific/Freepik Upscaler, Krea Enhance, Topaz Gigapixel) | Add micro-detail and photo texture | Keep "creativity"/resemblance low (≈ 2–4 / 0.2–0.35) so geometry doesn't change |
| Nano Banana / Firefly Generative Fill / Photoshop | Fix small regions: add plants, styling props, replace sky, remove artefacts | Mask locally; never regenerate the whole architecture for client deliverables |
| ComfyUI + ControlNet (depth/normal/line passes from Blender) | Re-light or re-style while locking geometry | Export Z-depth, normal and Cryptomatte passes from Blender as control images |
| AI video (Seedance, Kling, Higgsfield) | Turn stills into short motion pieces | Start from your final render as first frame; low motion prompts keep architecture stable |
| Lightroom/Resolve AI masks | Sky, subject, lens blur, denoise | Final photographic grade |

Workflow: Blender render (EXR + passes) → composite/grade → AI upscale at low creativity → local AI fixes → final grade → disclose AI enhancement where required for real-estate marketing (renders of unbuilt property should be labelled "artist's impression").

---

## 8. Iterative critique-and-refine loop

Loop per iteration (aim for 4–8 rounds):
1. Render a preview through `CAM_Main`.
2. Ask Claude to critique with a fixed rubric.
3. Pick the top 1–3 fixes only; apply them one at a time.
4. Re-render the same camera; compare with the previous version side-by-side.
5. Save `vNN` and log what changed.

Critique prompt (copy-paste):
> "Look at this render as a senior architectural visualiser. Score 1–10 for: scale/proportion, geometry detail (bevels, imperfections), lighting realism, exposure and contrast, material realism (roughness, tiling, reflections), composition and verticals, styling/storytelling, noise/artefacts. For each score under 8, give the specific cause and the exact Blender change (node, value, object) to fix it. Then list the 3 highest-impact fixes in order. Don't make changes yet."

Then: "Apply fix #1 only, re-render, and tell me whether the score improved."

Verification prompts
- "List any object whose lowest point isn't at z = 0 or that intersects another object."
- "Report dimensions of all furniture and flag anything outside real-world ranges."
- "Render a clay (white override) pass so we can judge lighting without materials."
- "Render a wireframe and an X-ray view to check hidden geometry."

Reference matching: give Claude a real photo of a similar room and ask: "Compare my render to this reference. What differs in light direction, shadow softness, colour temperature, contrast and material sheen? Give numeric adjustments."

---

## 9. Worked example: north-facing Brisbane living room

1. Shell + window + camera (section 5 prompts) → screenshot check.
2. Clay render: fix sun angle until shadow shape is right.
3. HDRI + portal; exposure set so window isn't fully blown (slight highlight roll-off).
4. Materials: oak floor, off-white walls (base 0.8, roughness 0.85), linen sofa with sheen, brushed brass.
5. Bevels + styling props (plants, throw, books, coffee cups) imported and placed with dimension checks.
6. Critique loop ×5 using the rubric.
7. Final render 3000 × 2000, 1024 samples, EXR + depth/normal passes.
8. Grade in Resolve/Lightroom, upscale at low creativity, AI-fill tiny styling tweaks, export for web and print.

---

## 10. Quick troubleshooting

| Problem | Fix |
|---|---|
| Claude says it can't connect | Click Connect in Blender N-panel; ensure only one client; restart Claude |
| Objects float/intersect | Ask for bounding-box checks and snap z-min to floor |
| Render looks "CG" | Bevels, roughness variation, AgX, lower fill light, add grain |
| Noisy interior | Light portals, more samples, clamp indirect, denoise |
| Texture stretching | Apply scale, use box/real-world UVs |
| Tool call times out | Lower preview resolution/samples; render finals manually |
| Messy AI-generated models | Use for background props only; decimate/remesh; replace hero items with real assets |

## Sources
- https://github.com/ahujasid/mcp-for-blender
- https://github.com/ahujasid/mcp-for-blender/blob/main/README.md
- https://www.mcp-for-blender.com/docs/concepts/capabilities
- https://www.mcp-for-blender.com/docs/concepts/how-it-works
- https://www.strayspark.studio/blog/official-blender-mcp-server-comparison-2026
- https://lagindicator.com/dev-tools/codex-blender-control-2026-09-10/
- https://blendervisualinvestigation.com/knowledge-base/docs/addons/blender-mcp/
- https://mehadi.me/mcps/blender-mcp/
- https://clauderules.net/mcp/ahujasid-blender-mcp
- https://www.skillsdirectory.com/skills/akillness-blender-mcp
- https://hysenlabs.com/projects/ahujasid-blender-mcp
