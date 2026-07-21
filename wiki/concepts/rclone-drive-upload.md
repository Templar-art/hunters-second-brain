---
type: concept
tags: [tooling, workflow, delivery, google-drive]
status: active
updated: 2026-07-21
---

# rclone — Fast SSD → Google Drive Upload

The fast, no-internal-space way to push big client files from an external SSD to the
**10x Visuals | Clients** shared drive. Replaces slow browser drag + dodges the
"not enough space" problem the Google Drive desktop app hits (internal drive only ~39 GB free).

## Why rclone (not browser / not desktop app)
- **Browser (Chrome drag):** throttles one stream (~10–15 MB/s). Slow.
- **Google Drive desktop app:** caches the file onto the *internal* drive first → runs out of space when uploading big files off an SSD. Bad fit for SSD workflow.
- **rclone:** reads straight off the SSD, streams to Drive in **parallel chunks**, **no local copy**. Fastest + no space issue. ~40–70 MB/s in practice (line max ~87 MB/s at 700 Mbps up).

## Setup (already done — 2026-07-21)
- Installed via `brew install rclone` (v1.74.4, arm64).
- Remote name: **`gdrive`** → points at the **10x Visuals | Clients** shared drive (team drive).
- Scope: full drive access. Auth via browser OAuth (token stored in local `rclone.conf`).
- ⚠️ The `rclone.conf` holds live access tokens — never paste that block into chat/share it.

## Daily commands

**Upload a single zip:**
```
rclone copy "/Volumes/WD_BLACK/154 Marine Parade.zip" "gdrive:Clients" --progress --transfers 8 --drive-chunk-size 128M
```

**Upload a whole project folder (keeps folder name):**
```
rclone copy "/Volumes/WD_BLACK/154 Marine Parade" "gdrive:Clients/154 Marine Parade" --progress --transfers 8 --drive-chunk-size 128M
```

**The pattern — swap SOURCE + DESTINATION only:**
```
rclone copy "SOURCE-on-SSD" "gdrive:Clients/DESTINATION" --progress --transfers 8 --drive-chunk-size 128M
```

## Handy flags
| Flag | Does |
|---|---|
| `--progress` | live speed + ETA bar |
| `--transfers 8` | 8 files uploading at once (fills the 700 Mbps pipe) |
| `--drive-chunk-size 128M` | bigger chunks = faster big-video upload |
| `--dry-run` | preview what WOULD upload, sends nothing (test first) |
| `-v` | verbose, per-file detail |

## Useful checks
```
rclone lsd gdrive:                 # list top folders in the shared drive
rclone lsd gdrive:Clients          # list client folders
rclone about gdrive:               # drive quota / space used
rclone config                      # edit/rename/re-auth the remote
```

## Gotchas
- **Google throttles server-side** — some days you get ~70 MB/s, some days ~30. Not your Mac/line; it's Google's mood. Shared-key rate limits ease if you make your own free Google client ID (Cloud Console, ~10 min) — do this if throttling annoys.
- **750 GB/day upload cap** per Google account, any method. Rare to hit, but exists.
- **`rclone copy` never deletes** anything at the destination — safe. (`rclone sync` DOES mirror-delete — don't use sync for deliveries unless you mean it.)
- Remote name is `gdrive` (renamed from the original spaces-in-name version so commands need no quoting).

## Related
- [[higgsfield-pipelines]] — where the deliverables come from
- Google Drive desktop app still installed but paused-in-favour-of-rclone for SSD uploads.
