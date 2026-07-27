#!/bin/zsh
# Monthly cache maintenance for Hunter's MacBook Pro (M2 Pro, 16GB).
#
# Clears only caches that regrow on their own and cost nothing to lose.
# Deliberately does NOT touch:
#   - ~/Library/Caches/Adobe Camera Raw 2      (deleting cripples Lightroom for weeks)
#   - Adobe Camera Raw BigTableGroupCache      (same reason)
#   - Claude's live Cache / Code Cache         (unsafe while the app is running;
#                                               handled below only when Claude is quit)
#
# Installed as launchd job com.10x.aios.mac-maintenance — 1st of the month, 09:14.

set -u
setopt NULL_GLOB

LOG_TS="$(date '+%Y-%m-%d %H:%M:%S')"
echo "==================== $LOG_TS  mac-maintenance ===================="

avail_before=$(df -k /System/Volumes/Data | tail -1 | awk '{print $4}')

# --- caches that always regrow -------------------------------------------
purge_dirs=(
  "$HOME/Library/Caches/Google"
  "$HOME/Library/Caches/Homebrew"
  "$HOME/Library/Caches/pip"
  "$HOME/Library/Caches/node-gyp"
  "$HOME/Library/Caches/electron"
  "$HOME/Library/Caches/com.apple.python"
  "$HOME/Library/Caches/Adobe"
  "$HOME/Library/Caches/com.adobe.LightroomClassicCC7"
  "$HOME/Library/Caches/com.adobe.Photoshop"
)

for d in $purge_dirs; do
  [[ -d "$d" ]] || continue
  size=$(du -sh "$d" 2>/dev/null | cut -f1)
  if rm -rf "$d" 2>/dev/null; then
    echo "  purged  ${size:-?}\t$(basename "$d")"
  else
    echo "  FAILED  $(basename "$d")"
  fi
done

# --- log directories: empty the files, keep the dirs ----------------------
log_dirs=(
  "$HOME/Library/Logs/Adobe"
  "$HOME/Library/Logs/CreativeCloud"
  "$HOME/Library/Logs/NGL"
  "$HOME/Library/Logs/AdobeVulcan"
)

for d in $log_dirs; do
  [[ -d "$d" ]] || continue
  size=$(du -sh "$d" 2>/dev/null | cut -f1)
  find "$d" -type f -delete 2>/dev/null
  echo "  emptied ${size:-?}\t$(basename "$d") logs"
done

# --- Claude caches: only when the app is not running ----------------------
# NB: macOS pgrep has no -q (it exits 0 regardless), and -f against the full
# path does not match. Compare comm strings directly instead.
if ps -axo comm | grep -q "Claude.app/Contents/MacOS/Claude"; then
  echo "  skipped\tClaude caches (app is running)"
else
  for d in "$HOME/Library/Application Support/Claude/Cache" \
           "$HOME/Library/Application Support/Claude/Code Cache"; do
    [[ -d "$d" ]] || continue
    size=$(du -sh "$d" 2>/dev/null | cut -f1)
    rm -rf "$d" 2>/dev/null && echo "  purged  ${size:-?}\tClaude $(basename "$d")"
  done
fi

# --- keep the Adobe autostart agents disabled -----------------------------
# Adobe's updater re-enables these on every Creative Cloud update.
for job in com.adobe.AdobeCreativeCloud com.adobe.AdobeDesktopService com.adobe.ccxprocess; do
  launchctl disable "gui/$(id -u)/$job" 2>/dev/null
done
echo "  re-asserted disable on Adobe autostart agents"

# --- report ---------------------------------------------------------------
avail_after=$(df -k /System/Volumes/Data | tail -1 | awk '{print $4}')
freed_mb=$(( (avail_after - avail_before) / 1024 ))
echo "  ----"
echo "  freed:  ${freed_mb} MB"
echo "  free:   $(df -h /System/Volumes/Data | tail -1 | awk '{print $4}')"
echo "  swap:   $(sysctl -n vm.swapusage)"
echo "==================== done ===================="
echo
