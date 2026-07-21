#!/bin/bash
# 10x Visuals — SSD → Google Drive (Clients shared drive) batch uploader.
# Reads upload-map.tsv (source<TAB>client-folder) and uploads each zip to
# gdrive:Clients/<client-folder>. Fully RESUMABLE: rclone skips anything already
# uploaded (same size), so if it dies (daily cap, sleep, unplugged SSD) just re-run.
#
# Usage:
#   ./upload.sh            # real upload
#   ./upload.sh --dry-run  # show what WOULD upload, send nothing
#   ./upload.sh --check    # verify every source file exists, no upload
#
# Runs safely for days: --drive-stop-on-upload-limit makes rclone stop cleanly when
# Google's 750 GB/day cap is hit. Re-run the next day and it picks up where it left off.

set -uo pipefail
DIR="$(cd "$(dirname "$0")" && pwd)"
MAP="$DIR/upload-map.tsv"
LOG="$DIR/upload.log"
REMOTE="gdrive:Clients"
MODE="${1:-run}"

RCLONE_FLAGS=(--transfers 8 --drive-chunk-size 128M --drive-stop-on-upload-limit --progress)
[ "$MODE" = "--dry-run" ] && RCLONE_FLAGS+=(--dry-run)

echo "================ upload run: $(date) (mode: $MODE) ================" | tee -a "$LOG"

total=0; done_ok=0; missing=0
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
    done_ok=$((done_ok+1)); continue
  fi

  echo "" ; echo ">>> $(basename "$SRC")  ->  $REMOTE/$DEST" | tee -a "$LOG"
  rclone copy "$SRC" "$REMOTE/$DEST" "${RCLONE_FLAGS[@]}" --log-file "$LOG" --log-level INFO
  rc=$?
  if [ $rc -ne 0 ]; then
    echo "  ✗ rclone exit $rc on this file (likely daily 750GB cap or transient)." | tee -a "$LOG"
    echo "    Stopping. Re-run ./upload.sh tomorrow — it resumes automatically." | tee -a "$LOG"
    break
  fi
  done_ok=$((done_ok+1))
done < "$MAP"

echo "" ; echo "================ finished: $(date) ================" | tee -a "$LOG"
echo "mapped: $total | ok/checked: $done_ok | missing: $missing" | tee -a "$LOG"
