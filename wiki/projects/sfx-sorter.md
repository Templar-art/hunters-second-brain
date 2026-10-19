---
type: project
tags: [audio, sfx, automation, launchd]
status: live
updated: 2026-10-20
---

# SFX Sorter

A background watcher that moves downloaded sound packs out of `~/Downloads` and into `~/Music/SFX Library`. Hunter asked for it on 20 October 2026 while downloading Ocular Sounds packs: "in future put all sounds in a folder".

## What it does

[sfx-sorter.mjs](../../projects/sfx-sorter/sfx-sorter.mjs) runs under launchd as `com.10x.sfx-sorter` (plist in `~/Library/LaunchAgents/`). It wakes on every change to `~/Downloads`, and every 10 minutes as a fallback.

- **Sound-pack zip** (5 or more audio files, mostly audio): extracted into `SFX Library/Ocular Sounds/<pack>/` when "ocular" appears in the zip name or its contents, otherwise into `SFX Library/_Incoming/<pack>/`. The original zip is kept in `SFX Library/_Archives/`.
- A wrapper folder named after the pack is unwrapped. A lone category folder such as `Impacts` is kept.
- Nothing is deleted. A name clash gets a ` (2)` suffix.
- It waits until a file has gone 20 s without changing, so it never grabs a half-finished download. Partial `.crdownload` files are ignored.
- Log: `SFX Library/_sorter.log` (launchd output goes to `~/Library/Logs/sfx-sorter.log`).

## What it deliberately leaves alone

- **Loose audio files.** Downloads also holds music tracks (ANOTR, AVE…) and client VO (TBolt). The first dry run would have swept 10+ of those into the SFX library, so loose audio is never touched.
- **Zips older than `SFX Library/.sorter-since`.** That is set to 20 October 09:00, so old zips such as the TRILHA music download stay where they are.
- RAWs, video, photos, PDFs, installer zips: never touched.

## Operating it

- Stop: `launchctl bootout gui/$(id -u)/com.10x.sfx-sorter`
- Start: `launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.10x.sfx-sorter.plist`
- Preview: `node projects/sfx-sorter/sfx-sorter.mjs --dry-run`
- Ocular packs whose zip doesn't say "Ocular" land in `_Incoming/`. Move them into `Ocular Sounds/` by hand, or rename the zip before it finishes downloading.

## Verified

The scratch-folder tests covered an Ocular zip, a non-Ocular pack, a photo zip, RAWs, a partial download and a file still being written. A live launchd test with a 5-wav zip dropped into Downloads was extracted within seconds, and the test files were then removed. launchd's `node` can read `~/Downloads`, the same TCC pattern as [[agentic-os]].

## Related

[[agentic-os]] · [[claude-code-setup]] · [Sound Lab](../../projects/sound-lab/) · `~/Music/SFX Library/catalog.csv` (Ocular index)
