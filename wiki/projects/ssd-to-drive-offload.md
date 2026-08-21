---
type: project
tags: [ops, storage, google-drive, ssd, backup]
status: in-progress
updated: 2026-08-12
---

# SSD → Google Drive offload

Ongoing project: clear footage off 10x's external SSDs (**10X SSD2, SSD3, SSD5, SSD6, WD_BLACK**) onto Google Drive, organized under the existing **`Clients/<client name>/`** folder structure (plus a separate one-off stream direct to **`Internal | 10x/Giovanni /`** for footage handed to Giovanni specifically). Multi-day job, still running as of 2026-08-12 — pick this page up cold if a new session inherits it.

## Mechanism
- `rclone` is installed with a preconfigured remote named **`gdrive`** (config at `~/.config/rclone/rclone.conf`). No auth setup needed.
- Drive folder structure: top-level **`Clients`** (per-client subfolders, most already existed before this project) and **`Internal | 10x`** (has a `Giovanni ` subfolder — note the trailing space in the name — used for footage handed to Giovanni specifically, separate from the Clients archive).
- **Upload speed is capped around ~13MB/s** consistently regardless of job — looks like a bandwidth ceiling, not an rclone tuning issue. Plan multi-day timelines accordingly.
- **Zip-then-upload, not raw copy.** Hunter's convention: each top-level client folder gets zipped into a single `.zip` (client folders can be 50–300GB+), then the zip is uploaded as one file to `Clients/<Client>/<folder name>.zip`. Local zip staging happens on **SSD2** (`/Volumes/10X SSD2/_zip_staging/`, chosen for having the most free space) since the Mac's boot drive has almost no free space (~13GB). Delete the local zip after a confirmed successful upload.
- Hunter also has his own pre-existing zips sitting directly on the source SSDs from prior manual work — those get uploaded as-is (no re-zipping), then the source zip gets trashed.
- **After a folder is confirmed uploaded, move the original source (raw folder or zip) to Trash** (via macOS `trash` CLI or Finder) — never delete outright. Hunter empties the Trash himself.

## Known gotchas (hit repeatedly — check before assuming something's broken)
- **External drives disconnect mid-job frequently** (USB/hub flakiness). When a drive drops, every job reading from it fails instantly with "directory not found" — this can look like a mass failure across dozens of queued jobs when it's really just one drive dropping. Always `ls /Volumes/` first when something looks wrong.
- Because of the above, any batch script needs a **guard that checks the source directory exists before attempting**, and skips cleanly (logged, not a hard fail) rather than burning through the whole queue.
- `rclone copy`/`copyto` only creates the destination object after a file fully transfers — a killed/interrupted job does **not** leave corrupt partial files on Drive, safe to just resume.
- Background jobs launched via the harness's tracked backgrounding can silently die across session/environment resets. Prefer `nohup ... & disown` for anything multi-hour, and independently verify with `ps aux` rather than trusting a stale task ID.
- The scratchpad tmp directory gets recycled across sessions — scripts/logs written there can vanish. For anything that needs to survive, prefer a fixed path like `/private/tmp/claude-501/offload_scratch/` over relying on a session-specific scratchpad.
- Folder names on these drives are messy: trailing spaces, pipe characters (`|`), colons — always quote carefully and double check with `stat`/`ls` rather than assuming a name matches exactly.

## Folder → client mapping (established, don't re-derive)
Most folders map to existing `Clients/` names directly (Whitefox Real Estate, Ashley Cooper Construction, Coast Life Constructions, Kodiak Projects, Salisbury Building Projects, Zed Real Estate, MVX Electrical, Empire Technologies, Unqi, BMW, Maker Build, SHAPE AUS, Jessica Wallace, Urban Core, Livit Constructions, 183 Broken Head Rd). New client folders were created for: **Chandler**, **Mitch Palmer** (31 Coobowie St). Ambiguous/unlabeled folders (BYD Photos, 10x BTS Stuff, untitled folder, September, Villa Noosa, 25 Davenport Drive, Master 10th July 2026) went into the existing **`mystery stuff`** Drive folder — flagged, not confirmed with Hunter. **Jason Ward** and **Bespoke**-adjacent shoots (3026 The Boulevard, 3049 Boulevard Jason, BMW x Jace social content) route to **Bespoke**. Logan → **Belle Property Hope Island**. Tyson SD Dump, Lach's House, 47 Somerset Drive → **10x Visuals**.

`.fcpbundle` files and Final Cut motion template folders are explicitly **excluded** — they're live project libraries/app templates, not client deliverables.

## Status as of 2026-08-12
- Confirmed fully uploaded (Clients/ archive): Urban Core - The Community (raw, before the zip convention), Whitefox BTS part 2, Ashley Cooper Toowoomba, plus ~15 of Hunter's pre-existing zips (Chandler/1 Tibbing St, July 14th Coastlife, BYD Photos, Master 10th July 2026, Bespoke BMW x Jace, September, 1007:30 Marine Parade, Livit Constructions x2, Livit Site 1, Chandler Commercial Photos, Jason Ward, 183 Broken Head, 25 Davenport Drive, 3049 Boulevard Jason, Safi Photos|Zed).
- **Still queued, not started** (Clients/ archive): the bulk of the raw-folder job list — Kodiak (×7 folders), Coast Life (×6), Salisbury (×3), Zed (×2 more), Ashley Cooper Construction (×5 more), BMW (×2), MVX, Empire Technologies (×2), Unqi, Maker Build, SHAPE AUS, Jessica Wallace, and the newly-created Chandler/Mitch Palmer/mystery-stuff items not yet covered by pre-existing zips.
- **Confirmed fully uploaded (Giovanni stream, `Internal | 10x/Giovanni /`, raw not zipped)**:
  - `Whitheriff | Salt PM Shoot 11 | Aug | 2026` (SSD2) — 226GB, drone *photos* excluded, everything else (A7S3 NO1/NO2, BTS A7S3, BTS DRONE, Mavic 4 PRO video) included.
  - `37 Hibiscus Parade, Banora Point Site Update` (SSD6) — Video (93GB) + Drone (6.4GB), Photo/Drone Photo excluded.
  - `Byron shoot` (SSD6) — Video (57GB, includes DJI drone clips — no separate drone folder existed for this one), Pictures excluded.
  - `Workshop | Sel Studios | 12th of Aug 2026` (SSD2) — Videos only (123GB, 169 files), Photos excluded. Survived a mid-job computer restart cleanly (rclone resumed, skipped already-uploaded files — no data lost, just needed a relaunch since `/private/tmp` gets wiped on reboot).
  - `Project August Content Retainer Bespoke` (SSD6) — Video only (46GB, 92 files), Photo folder (88GB) excluded.
- **Currently uploading (Giovanni stream)**: `ACC | BROADWALK TAVERN | FINISHED PROJECT` (SSD3) — A7S3 Videos (77GB) + Drone Videos (8.1GB), A7R5 Photos (64GB) and Drone Photos (7.3GB) excluded.
- New drive seen in this project: **SSD6** (has its own backlog too — Broll for 6/08/26, Lach Salisbury, 47 Somerset Drive + Project Files, Zed Real Estate 2105/1 Grant Avenue, McGrath Palm Beach, and a `TO BE UPLOADED | DON'T DELETE` folder that's presumably a priority queue — none of these have been actioned yet).
- Given the ~13MB/s ceiling (sometimes better, ~20-40MB/s, when only one job runs), the remaining Clients/ backlog is realistically several more days of continuous background uploading.

## Next steps for whoever picks this up
1. Check `ls /Volumes/` for which drives are currently connected before resuming anything.
2. Resume the raw-folder job queue (see mapping above) — zip each to SSD2 staging, upload, trash source, repeat.
3. Look at SSD6's `TO BE UPLOADED | DON'T DELETE` folder — name suggests it's Hunter's own priority list, worth checking before assuming the mapping above is exhaustive.
4. Confirm the flagged `mystery stuff` placements with Hunter when there's a natural pause.
5. Keep an eye on SSD2 staging free space — it was the largest free volume (~1TB) when this started.
