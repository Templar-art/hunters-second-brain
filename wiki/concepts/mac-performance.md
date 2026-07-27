---
type: concept
tags: [machine, tooling, performance, maintenance]
updated: 2026-07-27
---

# Mac Performance — what actually slows the machine

The working machine is a **MacBook Pro M2 Pro, 10-core (6P/4E), 16 GB RAM, 460 GB SSD**. Audited 2026-07-27 after Hunter reported general slowness. The finding that matters: **it was never a disk problem**. 176 GB were free at the time of the complaint, Spotlight was idle, there were no Time Machine local snapshots, and only five apps were open. Reach for the storage cleaner last, not first.

## The three real constraints

**1. 16 GB of RAM against an Electron-heavy workload.** Claude desktop runs ~11 processes and Chrome ~12. With both open the machine pages to disk continuously — the audit caught 7.5 M pageouts in a 5-hour uptime and 990 MB of swap in use. No amount of cache clearing touches this. The lever is behavioural: quit Claude desktop when not actively in it. This is the ceiling on the machine and the reason a RAM upgrade would be the only real fix.

**2. WindowServer against three displays.** Built-in Liquid Retina XDR (3024×1964) plus two 1920×1080 externals, one running at **75 Hz**. WindowServer sat at 45% CPU doing nothing but compositing. Dropping the 75 Hz panel to 60 Hz is the single highest-leverage fix available and costs nothing. Even after the July cleanup it was still ~29% — this is the largest remaining item and it can only be fixed in System Settings → Displays, not from a shell.

**3. Adobe's background stack.** Five launch agents and three daemons (Creative Cloud, Adobe Desktop Service, ccxprocess, Core Sync, keystone) ran with no Adobe app open, one of them steady at 5.3% CPU. Disabled 2026-07-27 — Creative Cloud and Lightroom still launch normally on demand. **Adobe re-enables these on every CC update**, so the monthly maintenance loop re-asserts the disable each run.

## Standing rules

- **Never delete `~/Library/Caches/Adobe Camera Raw 2`.** It was 6.7 GB at audit and looks like the biggest win on any storage report. It is not — deleting it cripples Lightroom Classic for weeks while previews rebuild. Same for `Adobe Camera Raw BigTableGroupCache`. The monthly loop deliberately skips both.
- **Never clear a running Electron app's cache.** Claude's `Cache` and `Code Cache` are only safe to remove when the app is quit; the maintenance script guards on this.
- **Applications belong in `/Applications`.** Chrome was found installed on the Desktop (`~/Desktop/Google Chrome.app`), on a Desktop holding 59 GB of client footage. Moved 2026-07-27 and re-registered with LaunchServices.
- **Disk space is not the metric.** Judge the machine by swap used, load average and WindowServer CPU — not by free GB.

## Automation

`com.10x.aios.mac-maintenance` runs `projects/aios-dashboard/bin/mac-maintenance.sh` on the 1st of each month at 9:14am. It purges only caches that regrow on their own (Google/Chrome, Homebrew, pip, node-gyp, electron, Adobe app caches), empties Adobe's log directories, conditionally clears Claude's caches when the app is quit, and re-asserts the Adobe autostart disable. Output appends to `projects/aios-dashboard/logs/launchd-maintenance.log`. It is a plain zsh script, not an AIOS registry action — no `claude -p`, no commits. Registered alongside the other loops in [[agentic-os]].

**Gotcha worth keeping:** macOS `pgrep` has no `-q` flag — it exits 0 regardless, so `if pgrep -qf …` silently always passes. And `pgrep -f` against a full `/Applications/…` path does not match. Detect a running app with `ps -axo comm | grep -q "Name.app/Contents/MacOS/Name"` instead. The first version of the maintenance script had this bug and failed open on the Claude guard.

## The 2026-07-27 pass

Reclaimed ~13 GB and roughly halved the load average. Before → after: swap 990 MB → 386 MB, load 4.21 → 2.31, WindowServer 45.5% → 29.1%, top Claude helper 60.1% → 28.8%, free disk 176 GB → 189 GB. Cleared: Claude VM bundle 6.8 GB (rebuilds on next Cowork/sandbox use, ~1.3 GB re-download), Google caches 3.0 GB, Adobe app caches 967 MB, Adobe logs 647 MB, Homebrew 427 MB, pip 216 MB, electron 95 MB, node-gyp 62 MB. Camera Raw's 6.7 GB left untouched by design.

Outstanding and owned by Hunter, not by any script: **set the 75 Hz display to 60 Hz**, and reboot — the machine still carried 386 MB of swap and a handful of stale Adobe processes after the pass.
