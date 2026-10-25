# Claude and Blender: Recommended Plugins and Add-ons

Research update for 10x Visuals, 23 October 2026. This companion to the render guide focuses on architectural visualisation, property imagery, scene automation, and controlled AI finishing.

## Recommended approach

My recommendation is to start with one Claude-to-Blender connection, one asset source, and a camera-matching tool if you are working from photographs. Add specialist lighting, architecture, and landscaping tools only when those tasks become recurring bottlenecks.

This is documentation-based research, not a hands-on compatibility test. Vendor capabilities are cited below; installation priorities, example prompts, and workflow advice are my recommendations rather than guarantees.

## What counts as a plugin?

Claude distinguishes connectors that provide access to external tools, skills that teach a workflow, and plugins that package skills, connectors, commands, and sometimes agents together ([Claude extension overview](https://claude.com/docs/extend/overview)). Installing a plugin does not automatically sign you into its bundled services, and support varies between chat, Cowork, and Claude Code ([Claude plugin documentation](https://claude.com/docs/plugins/overview)).

For this workflow, think in three layers: Claude plans and critiques; the MCP connection executes supported actions; Blender and its add-ons provide the actual scene-building tools. Do not assume that installing a Blender add-on also gives Claude a dedicated integration with it.

## Claude-side shortlist

### Official Blender connector: best starting point for scene inspection

- **Documented capabilities:** Reads the open scene through Blender's Python API, explains node and modifier setups, batch-applies changes, cleans unused data, and writes Python-based interface tools ([Claude Academy](https://academy.claude.com/tutorials/using-the-blender-connector-in-claude)).
- **Requirements and cost:** The tutorial specifies Blender 4.2 or later and Claude Desktop on any plan, including Free; it explicitly says this local connection does not work through claude.ai in a browser ([Claude Academy](https://academy.claude.com/tutorials/using-the-blender-connector-in-claude)).
- **Installation:** Add Blender under Customize → Connectors, install the Blender-side extension from the linked Blender MCP Server page, then start its server inside Blender ([Claude Academy](https://academy.claude.com/tutorials/using-the-blender-connector-in-claude)).
- **My recommendation:** Use it first if you mostly want Claude to inspect existing scenes, explain materials, make controlled edits, and help maintain reusable production scripts.

Example prompt:

> Inspect the active scene without modifying it. Report Blender version, render engine, unit scale, camera settings, missing assets, material dependencies, and the heaviest objects relative to their visible size in the main camera. Suggest three improvements and wait for approval.

### Community MCP for Blender: best fit for asset-assisted scene building

- **Documented capabilities:** Object and material manipulation, Python execution, visual verification, and integrations with Poly Haven, Sketchfab, Poly Pizza, Meshy, Tripo, Hyper3D Rodin, and Hunyuan3D ([project README](https://github.com/ahujasid/mcp-for-blender)).
- **Requirements:** The README lists Blender 3.0+, Python 3.10+, and `uv`; new installs should use `mcp-for-blender`, although the older `blender-mcp` command remains supported ([project README](https://github.com/ahujasid/mcp-for-blender)).
- **Cost caveat:** The project offers premium AI model generation without supplying your own API keys; do not assume generation services are included free with the bridge ([project README](https://github.com/ahujasid/mcp-for-blender)).
- **Security limitation:** The local socket has no authentication or encryption, and Python execution is powerful; the README recommends localhost and offers `BLENDER_MCP_SAFE_MODE=1` script validation ([project README](https://github.com/ahujasid/mcp-for-blender)).
- **My recommendation:** Choose this instead of the official connector when integrated asset search and import are your main priority. Start with one bridge rather than two competing setups.

Example prompt:

> Search Poly Haven for three suitable oak-floor materials. Show previews and source IDs before importing. Apply the selected material only to FLOOR_Main, record its source, check texture scale, and render a comparison without changing the camera.

The community integration explicitly documents asset search/import, automatic PBR material creation, and source metadata stored on imported data ([Poly Haven integration documentation](https://www.mcp-for-blender.com/docs/integrations/poly-haven)).

### Adobe for creativity: relevant for finishing and delivery

- **Documented capabilities:** Anthropic describes access to more than 50 tools across Creative Cloud applications, including Photoshop, Premiere, and Express ([Anthropic announcement](https://www.anthropic.com/news/claude-for-creative-work?lang=us)).
- **Cost and compatibility:** Exact connector entitlements, supported desktop versions, and per-operation costs are n.a. in the announcement; the general connector documentation warns that providers may require their own accounts or paid plans ([Anthropic announcement](https://www.anthropic.com/news/claude-for-creative-work?lang=us); [Claude plugin documentation](https://claude.com/docs/plugins/overview)).
- **My recommendation:** Investigate this before adding another image-editing subscription, given your Adobe workflow. Check the actual exposed tools first; the announcement does not establish unrestricted control over every Photoshop or Premiere function.

Suggested first request:

> List the image-editing and export tools this connector actually exposes. Tell me which can prepare approved Blender renders for delivery without generating or altering architectural features. Do not modify or upload anything yet.

### Affinity by Canva: optional production automation

- **Documented capabilities:** Batch image adjustments, layer renaming, file export, and creation of custom features inside the application ([Anthropic announcement](https://www.anthropic.com/news/claude-for-creative-work?lang=us)).
- **Cost and compatibility:** Exact plan requirements and supported application versions are n.a. in the announcement ([Anthropic announcement](https://www.anthropic.com/news/claude-for-creative-work?lang=us)).
- **My recommendation:** Consider it if you use Affinity for compositing and delivery. Otherwise, avoid adding a second finishing stack solely for an AI connection.

### SketchUp connector: optional concept-blocking route

- **Documented capabilities:** Turns a conversation describing a room, furniture item, or site concept into a starting point to refine in SketchUp ([Anthropic announcement](https://www.anthropic.com/news/claude-for-creative-work?lang=us)).
- **Cost and compatibility:** Exact connector pricing and supported application versions are n.a. in the announcement ([Anthropic announcement](https://www.anthropic.com/news/claude-for-creative-work?lang=us)).
- **My recommendation:** Useful if your clients already provide SketchUp models. Do not add another modelling application unless the input workflow justifies the conversion and cleanup.

### Custom archviz skill: recommended process layer, not an existing product

Claude skills can contain workflow instructions, scripts, and reference files; plugins can package those skills alongside connectors ([Claude extension overview](https://claude.com/docs/extend/overview)). I recommend eventually creating your own “10x Archviz QA” skill rather than relying on a generic realism prompt.

Suggested contents:

- **Scene rules:** Metric dimensions, collection naming, approved cameras, approved materials, and explicit protected objects.
- **Editing rules:** Inspect before modifying, change one subsystem at a time, save checkpoints, and never silently replace assets.
- **Verification rules:** Dimension checks, support-surface checks, missing-texture checks, and fixed-camera comparisons.
- **Finishing rules:** Preserve openings, structural proportions, branding, and client-specified finishes during AI enhancement.

This skill is a proposal, not something installed or built as part of this research. Start with a short checklist and refine it based on actual production failures.

## Blender-side shortlist

### Blendkit, formerly BlenderKit: furniture, styling, and material sourcing

- **What it does:** Searches, downloads, uploads, and rates assets inside Blender; offers a free selection and a paid Full plan for broader asset access ([official repository](https://github.com/BlenderKit/blenderkit); [vendor naming and add-on page](https://www.blendkit.com/get-blender-add-ons/)).
- **Compatibility:** A current explicit minimum Blender version is n.a. in the fetched repository overview; verify the exact download against your Blender release ([official repository](https://github.com/BlenderKit/blenderkit)).
- **Claude integration status:** A dedicated Claude or MCP interface is n.a. in the fetched documentation ([official repository](https://github.com/BlenderKit/blenderkit)).
- **My recommendation:** High priority for furnishing rooms. Select and import an approved asset manually first, then ask Claude to inspect and arrange the resulting Blender objects.

Example prompt:

> Inspect the imported sofa collection. Preserve the original as a hidden backup. Set the visible version to 2.2 m overall width, place its support points on the finished floor, and verify the intended clearance from the wall. Report any transforms that could affect modifiers.

### Poly Haven Asset Browser: HDRIs and physically based materials

- **What it does:** Adds HDRIs, models, and materials to Blender's Asset Browser, with resolution switching, texture-scale assistance, and displacement setup ([Poly Haven product page](https://polyhaven.com/plugins/blender)).
- **Cost:** The assets are free, but the convenient Asset Browser add-on is currently paid through purchase or Patreon; the vendor says it plans to release the add-on free after reaching its patron goal ([Poly Haven product page](https://polyhaven.com/plugins/blender)).
- **Compatibility:** Exact supported Blender versions are n.a. on the fetched product page ([Poly Haven product page](https://polyhaven.com/plugins/blender)).
- **Overlap:** The community MCP bridge already provides its own Poly Haven search/import path, so the paid Asset Browser add-on is not a prerequisite for that integration ([community integration documentation](https://www.mcp-for-blender.com/docs/integrations/poly-haven)).
- **My recommendation:** Start with the MCP integration if you choose the community bridge. Buy the separate add-on only if its visual browsing, scale tools, and manual workflow are useful to you.

Example prompt:

> Keep the room geometry and camera unchanged. Test two approved HDRIs, render both at identical exposure, and compare shadow direction, window reflections, and highlight clipping before selecting one.

### Photographer 5: camera and lighting controls

- **What it does:** Adds physical exposure controls, white balance, automatic lens shift, autofocus, per-camera settings, light/world mixers, IES and gobo tools, and a render queue ([Photographer documentation](https://sites.google.com/view/photographer-5-documentation/home)).
- **Compatibility:** The documentation describes Blender 3, 4, and 5 support, Cycles and EEVEE support with exceptions, Cycles-only IES/gobo features, and no LuxCore support in version 5; it also says Photographer 5.6 does not support Blender below 3.2.2 ([Photographer documentation](https://sites.google.com/view/photographer-5-documentation/home)).
- **Cost:** Paid add-on; the documentation refers to purchasing through Gumroad, but an exact current price is n.a. on the fetched page ([Photographer documentation](https://sites.google.com/view/photographer-5-documentation/home)).
- **My recommendation:** A strong fit for a photography-led workflow. Test changing cameras and rendering with the specific version you plan to use before adopting it on a client project.

Example prompt:

> Identify which camera and lighting properties are controlled by Photographer in this scene. Propose an architectural setup with straight verticals, locked white balance, and consistent exposure. Do not change the same parameter through both native Blender controls and the add-on.

### fSpy plus its Blender importer: still-photo camera matching

- **What it does:** A free, open-source standalone camera-matching tool with a separate Blender importer that transfers camera parameters and can set the reference photo as the camera background ([fSpy](https://fspy.io/); [official importer](https://github.com/perarnia/fSpy-Blender)).
- **Compatibility:** The importer README declares Blender 2.80+ for importer version 1.0.3; this is a declared minimum, not evidence that every current Blender release has been tested ([official importer](https://github.com/perarnia/fSpy-Blender)).
- **My recommendation:** High priority for matching existing property photographs. Treat the result as a camera solution to verify against measured geometry, not a substitute for a measured floor plan.

Recommended workflow:

1. Choose a photograph with useful structural lines and prepare it consistently.
2. Solve its perspective in fSpy and import the result.
3. Use a known physical dimension to validate scene scale.
4. Overlay simple wall and opening geometry before adding furniture.
5. Lock the approved camera before lighting and AI finishing.

Do not treat this still-image workflow as a moving-camera tracking solution. For video work, scope camera tracking separately.

### Geo-Scatter: lawns, gardens, vegetation, and exterior context

- **What it does:** Geometry Nodes-based scattering of plants, rocks, buildings, and other objects, with support for third-party assets; the vendor distinguishes the scatter tool from its asset libraries ([Geo-Scatter FAQ](https://www.geoscatter.com/docs-faq.html)).
- **Cost:** Geo-Scatter is paid; Biome-Reader is a free, more limited route for using and lightly adjusting biomes ([Geo-Scatter FAQ](https://www.geoscatter.com/docs-faq.html)).
- **Compatibility:** The fetched changelog lists Geo-Scatter 5.6.4 for Blender 5.2 LTS and warns that upgrades can change existing scatter systems ([Geo-Scatter changelog](https://www.geoscatter.com/docs-changelogs.html)).
- **Important limitation:** Do not install Geo-Scatter and Biome-Reader simultaneously; render-farm behaviour also depends on whether you animate plugin-interface settings or underlying Geometry Nodes properties ([Geo-Scatter FAQ](https://www.geoscatter.com/docs-faq.html)).
- **My recommendation:** Add it when exterior landscaping becomes frequent. Use curated plants appropriate to the project rather than scattering a generic mix everywhere.

Example prompt:

> Inspect the existing scatter system and its documented controls. Propose a grass-density mask excluding paths, building footprints, and hardscape. Keep the random seed fixed while comparing density changes. Do not assume Geo-Scatter operator names.

### Archipack: parametric architectural construction

- **What it does:** Parametric walls, windows, doors, slabs, floors, stairs, roofs, and other architectural elements; generated geometry is regular Blender mesh data ([Archipack features](https://blender-archipack.org/features/)).
- **Cost and compatibility:** The vendor distinguishes an older free edition from paid 2.x; the current sales description advertises Blender 3.x, 4.x, and 5.x and updates within the 2.x series ([Archipack features](https://blender-archipack.org/features/); [vendor sales page](https://blender-archipack.gumroad.com/l/ZRMyP?a=632791219)).
- **My recommendation:** Useful for repeated room shells and buildings when starting from dimensions. Verify the exact package for your Blender version rather than interpreting broad “5.x” wording as a tested compatibility matrix.

Example prompt:

> Inspect the installed Archipack version and available object parameters. Build only the approved wall layout from the supplied dimensions, retaining parametric controls. Report wall lengths, wall thicknesses, opening widths, and any discrepancies before adding finishes.

### Node Wrangler: material setup and debugging

- **What it does:** Speeds node editing and can construct a Principled texture setup by loading maps, selecting colour spaces, and connecting them based on filename conventions ([current Blender manual](https://docs.blender.org/manual/en/latest/addons/node_wrangler.html)).
- **Availability:** Blender's older manual identifies it as GPL-licensed and bundled; the current manual provides instructions for enabling it, so check your installed Blender's add-on controls before downloading another copy ([Blender 3.4 manual](https://docs.blender.org/manual/en/3.4/addons/node/node_wrangler.html); [current manual](https://docs.blender.org/manual/en/latest/addons/node_wrangler.html)).
- **Limitation:** Automatic texture identification depends on filenames and matching tags, so inspect the resulting connections rather than assuming a material is correct ([current Blender manual](https://docs.blender.org/manual/en/latest/addons/node_wrangler.html)).
- **My recommendation:** Enable this early for manual inspection and repair. Claude can also work directly on Blender node trees, so Node Wrangler is a useful complement, not a mandatory AI dependency.

## Which combination should you start with?

These are suggested combinations, not vendor bundles or interoperability guarantees. Add only one new tool at a time to a disposable test scene.

| Your main task | Suggested initial combination | Add later if needed |
|---|---|---|
| Inspecting and refining an existing Blender scene | Official Blender connector + Node Wrangler | Photographer |
| Furnishing and rendering a new interior | Community MCP + its Poly Haven integration + Blendkit free selection | Photographer and Archipack |
| Matching an existing property photograph | fSpy/importer + one MCP bridge + approved assets | Photographer |
| Building exterior marketing renders | One MCP bridge + approved architecture and vegetation | Geo-Scatter |
| Packaging final images and social assets | Your existing finishing application | Its relevant Claude connector after checking exposed tools |

My suggested priority for you is: get the bridge stable, establish accurate cameras and scale, improve assets and materials, then add specialist production tools. Avoid buying multiple products that solve the same asset-import or lighting-control problem before testing one complete shot.

## How to establish whether Claude can control an add-on

For most Blender add-ons in this shortlist, I did not verify a dedicated Claude integration. Treat their automation as untested until the installed version passes a small, reversible test.

Use this acceptance prompt:

> Read-only first: identify the Blender version, enabled add-on version, relevant registered operators, properties, and node groups. Consult the add-on documentation before naming commands. Propose one reversible test in a temporary collection. After approval, run it, read back the changed values, capture the result, and report any manual steps. Never invent an operator or claim success only because no error appeared.

Suggested acceptance tests:

- **Connection:** Read scene metadata and capture a view without editing.
- **Creation:** Add a named test object and verify its dimensions.
- **Material:** Change one material value and read it back.
- **Add-on:** Exercise one documented feature and inspect the resulting data.
- **Persistence:** Save a separate test file, reopen it, and check behaviour.
- **Rendering:** Produce a small preview with the intended engine.
- **Recovery:** Delete only the temporary collection or restore the checkpoint.

Keep a short version manifest with Blender version, add-on version, render engine, operating system, tested actions, known failures, and the test file location. Do not upgrade the production scene simply because a newer release exists.

## Refinements to the earlier render guide

The earlier guide remains a workflow starting point, but several recommendations need qualification. Use the following refinements when building a repeatable setup.

- **Installation:** Use `mcp-for-blender` for new community installs and the recommended `uv` installation method; the updated setup section now reflects this ([project README](https://github.com/ahujasid/mcp-for-blender)).
- **Official versus community:** The official Claude tutorial specifies Blender 4.2+ and Desktop, while the community project's own minimum requirements differ; keep these installation paths separate ([Claude Academy](https://academy.claude.com/tutorials/using-the-blender-connector-in-claude); [community README](https://github.com/ahujasid/mcp-for-blender)).
- **Safe mode:** It is script validation, not a guarantee that scene data cannot be changed or saved; normal Blender saving and import/export remain supported ([project README](https://github.com/ahujasid/mcp-for-blender)).
- **Light portals:** Blender describes portals as aids for sampling environment light in interiors, with potentially slower rendering per sample but faster convergence; they are not useful outdoors, so benchmark rather than prescribing them universally ([Cycles manual](https://docs.blender.org/manual/en/latest/render/cycles/light_settings.html)).
- **HDRI plus sun:** My recommendation is to inspect the HDRI's existing directional light before adding a sun; do not automatically combine an overcast HDRI with a strong sharp-shadow sun.
- **Floor placement:** Replace “every object's lowest point must equal z=0” with “each object's intended support points must meet its intended support surface”; wall art, pendants, stacked objects, and upper floors need different tests.
- **AI enhancement settings:** Disregard universal numeric creativity settings from the earlier guide; use the selected tool's own controls, then compare geometry, openings, surface finishes, and text before accepting a result.
- **Render samples:** Treat example sample counts as test settings, not quality guarantees; compare small crops at final output scale before choosing the final render budget.

## Suggested first production exercise

Choose one room, one approved camera, one lighting condition, and three hero assets. Use that shot to validate the workflow before attempting whole-property automation.

1. Establish measured geometry and a reference camera.
2. Inspect the scene through the chosen MCP connection.
3. Import approved assets and verify dimensions and support surfaces.
4. Build and verify the materials.
5. Compare lighting variants without moving the camera.
6. Critique the same render against a fixed checklist.
7. Apply one high-impact correction and re-render.
8. Test restrained AI finishing on a copy, then compare against the unaltered render.
9. Save the accepted scene, versions, asset provenance, and change log.

The goal is not to install the largest collection of plugins. It is to produce an accurate shot that can be reopened, revised, and reproduced without guesswork.
