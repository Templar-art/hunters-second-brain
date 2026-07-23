#!/bin/bash
# 10x Visuals — SSD → Google Drive (Clients shared drive) PARALLEL batch uploader.
# Reads upload-map.tsv (source<TAB>client-folder) and uploads up to MAXJOBS zips at
# once, each to gdrive:Clients/<client-folder>. Google throttles ~per connection, so
# N files in parallel ≈ N× the aggregate speed of one-at-a-time.
#
# Fully RESUMABLE: rclone skips anything already uploaded (same size). If it stops
# (daily cap, sleep, unplugged SSD) just re-run — it picks up where it left off.
#
# Usage:
#   ./upload.sh              # real upload, 4 files at once
#   MAXJOBS=6 ./upload.sh    # crank concurrency higher
#   ./upload.sh --dry-run    # show what WOULD upload, send nothing
#   ./upload.sh --check      # verify every source file exists, no upload

set -uo pipefail
DIR="$(cd "$(dirname "$0")" && pwd)"
MAP="$DIR/upload-map.tsv"
LOG="$DIR/upload.log"
REMOTE="gdrive:Clients"
MODE="${1:-run}"
MAXJOBS="${MAXJOBS:-4}"

PER_FILE_FLAGS=(--drive-chunk-size 128M --drive-stop-on-upload-limit
                --stats 20s --stats-one-line -v --log-file "$LOG")
[ "$MODE" = "--dry-run" ] && PER_FILE_FLAGS+=(--dry-run)

echo "================ PARALLEL upload run: $(date) (mode: $MODE, $MAXJOBS at once) ================" | tee -a "$LOG"

total=0; missing=0
while IFS=$'\t' read -r SRC DEST; do
  [ -z "${SRC// }" ] && continue
  case "$SRC" in \#*) continue;; esac
  total=$((total+1))

  if [ ! -e "$SRC" ]; then
    echo "  ⚠️  MISSING (SSD not mounted?): $SRC" | tee -a "$LOG"
    missing=$((missing+1)); continue
  fi

  if [ "$MODE" = "--check" ]; then
    echo "  ✓ found: $SRC  ->  $REMOTE/$DEST"
    continue
  fi

  # throttle: keep at most MAXJOBS rclone workers running at once (bash 3.2 safe)
  while [ "$(jobs -rp | wc -l | tr -d ' ')" -ge "$MAXJOBS" ]; do sleep 2; done

  echo ">>> launching: $(basename "$SRC")  ->  $REMOTE/$DEST" | tee -a "$LOG"
  rclone copy "$SRC" "$REMOTE/$DEST" "${PER_FILE_FLAGS[@]}" &
done < "$MAP"

echo "…waiting for in-flight uploads to finish…" | tee -a "$LOG"
wait

echo "================ finished: $(date) ================" | tee -a "$LOG"
echo "mapped: $total | missing: $missing" | tee -a "$LOG"
