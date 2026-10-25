# Mac mini: Claude Code + Blender Installation Checklist

Prepared for 10x Visuals on 26 October 2026. Tailored to your reported Mac mini M5 Pro with 48 GB RAM, Claude Code, and the latest stable Blender.

## Target setup

The current Blender download page lists **Blender 5.2.3 LTS for Apple Silicon**, requiring macOS 13 or newer; it separately offers experimental builds, which it does not recommend for production ([Blender downloads](https://www.blender.org/download/)). This checklist targets that stable release, but your installed version and macOS version have not been inspected.

The recommended connection is **Claude Code → community MCP for Blender → Blender**, using the current package name `mcp-for-blender`; the project documents Claude Code support and the installation commands used below ([project README](https://github.com/ahujasid/mcp-for-blender)). This is a third-party project, not the official Blender connector.

You do not need Claude Desktop for this path. This is an installation guide for you to run locally, not a claim that anything has been installed or tested on your Mac.

## Before installing

- [ ] Save your open Blender projects and make a backup copy.
- [ ] Use a disposable test scene, not a client production file.
- [ ] Install one MCP bridge only for the initial setup.
- [ ] Keep Claude Code's normal permission prompts enabled.
- [ ] Do not enable automatic purchases, paid generation, or external uploads.
- [ ] Keep optional third-party add-ons disabled until the baseline test passes.

### Confirm the actual versions

Open macOS Terminal and run:

```bash
sw_vers -productVersion
uname -m
"/Applications/Blender.app/Contents/MacOS/Blender" --version
```

- [ ] Record the macOS version: `________________`.
- [ ] Record the architecture reported by `uname`: `________________`.
- [ ] Record the Blender version: `________________`.
- [ ] If the Blender command cannot find the app, locate it in Finder or use Blender's About screen instead.
- [ ] If you installed a beta or daily build, use the stable Apple Silicon download for this test instead ([Blender downloads](https://www.blender.org/download/)).

Use the Apple Silicon download rather than the Intel build ([Blender downloads](https://www.blender.org/download/)). If your reported version differs from this checklist, check add-on compatibility before continuing rather than downgrading or overwriting a working installation.

## Install or verify Claude Code

Skip installation if Claude Code already works. Check it in Terminal:

```bash
claude --version
```

If missing, choose one official installation method, not both; Anthropic documents a native installer and a Homebrew option ([Claude Code quickstart](https://code.claude.com/docs/en/quickstart)).

### Option A: already using Homebrew

```bash
brew install --cask claude-code
```

### Option B: native installer

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

The native command downloads and executes an installer, so use it only after reviewing and trusting the official source; native installs auto-update, whereas the Homebrew installation uses Homebrew upgrades ([Claude Code quickstart](https://code.claude.com/docs/en/quickstart)).

- [ ] Open a fresh Terminal window after installation.
- [ ] Run `claude --version` successfully.
- [ ] Start `claude` and complete the browser sign-in prompts.
- [ ] Confirm your intended subscription or API billing account before continuing.

The documented account routes include eligible Claude subscriptions and Claude Console API access; this checklist does not assume that a free Claude account provides Claude Code access ([Claude Code quickstart](https://code.claude.com/docs/en/quickstart)).

## Install uv and prepare Python

The MCP project requires `uv` and Python 3.10 or newer, and advises against installing `uv` through `pip` for this setup ([project README](https://github.com/ahujasid/mcp-for-blender)). Choose one of Astral's documented installation routes ([uv installation](https://docs.astral.sh/uv/getting-started/installation/)).

### If Homebrew is available

```bash
brew install uv
```

### Otherwise

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Open a fresh Terminal window, then verify:

```bash
uv --version
uvx --version
command -v uvx
```

- [ ] All three commands succeed.
- [ ] If a command is not found, follow the installer's PATH instructions before proceeding.
- [ ] Do not solve PATH problems by running the MCP server with `sudo`.

For an explicit Python setup, run the following documented command; `uv` can also download Python automatically when needed, so you do not need to replace macOS's Python ([uv Python guide](https://docs.astral.sh/uv/guides/install-python/)).

```bash
uv python install 3.12
```

## Install the Blender-side add-on

Save your work and quit Blender before installing the add-on files. Run the project's documented installer in Terminal ([project README](https://github.com/ahujasid/mcp-for-blender)):

```bash
uvx mcp-for-blender install-addon
```

- [ ] Check the command output identifies the Blender installation you intend to use.
- [ ] If it fails or cannot locate Blender, stop and retain the exact error rather than copying files into guessed folders.
- [ ] Open Blender.
- [ ] Open **Edit → Preferences → Add-ons**.
- [ ] Enable **Interface: MCP for Blender**.
- [ ] In the 3D viewport, press **N** and open the **MCP for Blender** sidebar.
- [ ] Check the server is running; click **Start MCP Server** if needed.

The project documents that the add-on starts its server with Blender and provides that manual start control in the sidebar ([project README](https://github.com/ahujasid/mcp-for-blender)). Keep Blender open while testing the Claude connection.

### Security settings

- [ ] Keep the server bound to localhost.
- [ ] Do not expose it through your router, public tunnel, or a public network interface.
- [ ] Leave the add-on's telemetry consent unchecked for client work.
- [ ] Use the safe-mode and telemetry environment settings in the next section.

The add-on socket has no authentication or encryption, and anyone who can reach it can execute Python in Blender; safe mode validates scripts but is not an operating-system sandbox ([project README](https://github.com/ahujasid/mcp-for-blender)). The project documents `DISABLE_TELEMETRY=true` to disable even its minimal anonymous usage record ([project README](https://github.com/ahujasid/mcp-for-blender)).

These settings concern the MCP project, not all data processing by Claude or asset-generation providers. Do not treat telemetry being disabled as permission to submit confidential client material to external services.

## Register the connection in Claude Code

### Create a dedicated working folder

Run in Terminal:

```bash
mkdir -p "$HOME/Documents/10x-Blender"
cd "$HOME/Documents/10x-Blender"
```

Check for an existing Blender server before adding one:

```bash
claude mcp list
```

- [ ] If a server named `blender` already exists, inspect it with `claude mcp get blender`.
- [ ] Do not delete or overwrite a working configuration without recording it.
- [ ] Continue with the following command only if you need a new registration.

### Add the server with conservative defaults

This combines Anthropic's documented local stdio configuration syntax with the MCP project's documented environment variables ([Claude Code MCP documentation](https://code.claude.com/docs/en/mcp); [project README](https://github.com/ahujasid/mcp-for-blender)).

```bash
claude mcp add \
  --transport stdio \
  --scope local \
  --env BLENDER_MCP_SAFE_MODE=1 \
  --env DISABLE_TELEMETRY=true \
  blender -- "$(command -v uvx)" mcp-for-blender
```

The command records the currently resolved `uvx` executable path. Run the earlier `command -v uvx` check first, because an empty path will not work.

Local scope keeps the server private to your account and limited to this project; user scope would make it available across projects ([Claude Code MCP documentation](https://code.claude.com/docs/en/mcp)). Start with local scope so the Blender tools are not exposed in unrelated work.

- [ ] Run `claude mcp get blender` and confirm the executable, package name, and environment settings.
- [ ] Run `claude mcp list`.
- [ ] Start Claude Code from this same directory:

```bash
claude
```

- [ ] Inside Claude Code, type `/mcp`.
- [ ] Confirm the Blender server starts/connects.
- [ ] If the session was already open during registration, restart that session.

`/mcp` is a Claude Code session command, not a macOS shell command; Anthropic documents it as a way to inspect MCP connection status ([Claude Code MCP documentation](https://code.claude.com/docs/en/mcp)). A connected MCP process alone does not prove it can communicate with the open Blender scene, so complete the next tests.

## Run the acceptance tests

### Read-only connection test

Paste this into Claude Code:

> Use the Blender MCP tools to inspect the open scene without changing anything. Report Blender version, render engine, unit system, active camera, and object names. Capture one viewport image. Do not run shell commands, import assets, write files, or modify the scene. If a tool fails, show the exact error and stop.

- [ ] The reported scene matches what you see in Blender.
- [ ] The returned image is from your actual open scene.
- [ ] No objects, settings, or files were changed.

### Reversible edit test

Save a new Blender file named `mcp_connection_test.blend` yourself, then ask:

> In this disposable scene, create a collection named MCP_TEST and add a cube named MCP_TEST_Cube. Set its dimensions to exactly 1 m × 1 m × 1 m. Do not delete or modify anything outside MCP_TEST. Read back its dimensions and capture a viewport image. Stop after verification.

- [ ] The named collection and cube appear.
- [ ] The read-back dimensions are correct.
- [ ] Other objects remain unchanged.
- [ ] Approve cleanup only after inspecting the result.

Do not accept “done” as the verification. Require both a value read-back and an image, and keep the test limited to disposable content.

## Configure rendering for your Mac

Blender documents Metal as the Apple GPU backend, with macOS 13 or newer for all features; GPU rendering requires enabling the backend/device in Preferences and choosing GPU Compute in the scene ([Cycles GPU manual](https://docs.blender.org/manual/en/latest/render/cycles/gpu_rendering.html)).

- [ ] Open **Edit → Preferences → System**.
- [ ] Under **Cycles Render Devices**, choose **Metal**.
- [ ] Enable the available Apple GPU device.
- [ ] In **Render Properties**, select **Cycles**.
- [ ] Set the scene's device to **GPU Compute**.
- [ ] Render a small test and confirm it finishes without errors.

Suggested initial settings, not measured benchmarks for your exact Mac:

| Setting | First test |
|---|---|
| Resolution | 1280 × 720 |
| Samples | 64–128 |
| Denoising | On |
| Assets | A few simple objects |
| Textures | Mostly 1K or 2K |
| Final render | Decide after inspecting a full-resolution crop |

Your 48 GB RAM is the capacity you reported, not a guarantee that any scene will fit or render quickly. Start conservatively, measure performance, and increase texture sizes or scene complexity only when the image needs it.

- [ ] Record test resolution, samples, and render time.
- [ ] Check macOS Activity Monitor for memory pressure during a render.
- [ ] Avoid assuming every performance problem needs more samples.
- [ ] Render large final outputs outside a single long MCP interaction if the connection repeatedly times out.

## Add optional tools only after the tests pass

This is an installation order recommendation, not a claim that the full combination has been tested together. Keep the previously researched plugin guide alongside this checklist.

| Priority | Tool | Installation gate |
|---|---|---|
| First | Node Wrangler | Enable it using your Blender version's add-on controls and test one material setup ([Blender manual](https://docs.blender.org/manual/en/latest/addons/node_wrangler.html)). |
| First asset workflow | Community MCP's Poly Haven integration | Test one HDRI or material before adding another asset manager; the bridge has its own search/import integration ([integration documentation](https://www.mcp-for-blender.com/docs/integrations/poly-haven)). |
| When furnishing | Blendkit | Start with its free asset selection and check the installed add-on build against your Blender version ([official repository](https://github.com/BlenderKit/blenderkit)). |
| When matching a still photo | fSpy plus Blender importer | Test the importer in a disposable scene before relying on it in production ([fSpy](https://fspy.io/)). |
| When camera controls become a bottleneck | Photographer | Verify the exact installed release and engine-specific limitations, not just broad Blender 5 support ([documentation](https://sites.google.com/view/photographer-5-documentation/home)). |
| When landscaping | Geo-Scatter | The vendor lists version 5.6.4 for Blender 5.2 LTS, but test your exact patch version and scene ([changelog](https://www.geoscatter.com/docs-changelogs.html)). |
| When building repeated room shells | Archipack | Check the download package for Blender 5.2 before purchasing or enabling it ([vendor page](https://blender-archipack.gumroad.com/l/ZRMyP?a=632791219)). |

- [ ] Add only one optional tool at a time.
- [ ] Save a clean baseline before enabling it.
- [ ] Test scene creation, save/reopen, and a small render.
- [ ] Record the add-on version and any manual-only steps.
- [ ] Do not assume Claude can operate an add-on merely because it is installed.

## Troubleshooting and maintenance

| Symptom | First check |
|---|---|
| `claude` or `uvx` not found | Reopen Terminal, inspect the installer's PATH instructions, and rerun the version/path checks. |
| `blender` server name already exists | Run `claude mcp get blender`; inspect scope and settings rather than creating duplicates. |
| Server missing in a different project | This checklist intentionally uses local scope. Return to `~/Documents/10x-Blender`. |
| MCP connected but cannot inspect the scene | Check Blender is open, the add-on is enabled, and its sidebar server is running. |
| Tool descriptions look duplicated | Check for another bridge or client connected to the same Blender session. |
| Safe mode blocks a task | Inspect the exact requested operation; prefer a narrower operation or manual step rather than disabling safe mode globally. |
| Metal unavailable | Verify macOS requirements, installed Blender architecture, and the available device list. |
| Missing textures after reopening | Check asset paths and package the approved dependencies before moving the project. |
| Update changes the scene | Restore the saved checkpoint and investigate in a copy, not the production file. |

The MCP project advises running only one server instance at a time and documents this update command ([project README](https://github.com/ahujasid/mcp-for-blender)):

```bash
uvx mcp-for-blender@latest update
```

Do not run updates during a deadline-critical job simply because they are available. Back up the scene first, then restart both Blender and Claude Code and repeat the acceptance tests after an intentional update; restarting is part of the project's update instructions ([project README](https://github.com/ahujasid/mcp-for-blender)).

### Finished when

- [ ] Blender is the intended stable Apple Silicon build.
- [ ] Claude Code can inspect the real open scene.
- [ ] Claude can create and verify the test cube.
- [ ] Safe mode is enabled and project telemetry is disabled.
- [ ] The add-on socket remains local.
- [ ] A Metal/Cycles test render succeeds.
- [ ] You have a saved test scene and version record.

At this point, move to one measured room, one camera, and one lighting setup. Establish a reliable shot before attempting whole-property automation.
