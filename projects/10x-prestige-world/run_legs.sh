#!/bin/bash
# Architecture A leg chain — STRICTLY SEQUENTIAL.
# leg_1 starts from the scene_1 still; every later leg starts from the
# previous leg's ACTUAL last frame (extracted with ffmpeg). No end-images.
# Idempotent: re-runs skip finished legs. bash-3.2-safe (no assoc arrays).
set -u
cd "$(dirname "$0")"

VMODEL="seedance_2_0"
TRIES=3

for i in 1 2 3 4 5; do
  raw="clips/leg_${i}_raw.mp4"
  if [ -s "$raw" ]; then echo "[leg $i] already done, skipping"; continue; fi

  # start image: still for leg 1, previous leg's real last frame after that
  if [ "$i" = "1" ]; then
    start="stills/scene_1.png"
  else
    prev=$((i-1))
    start="frames/leg_${prev}_last.png"
    if [ ! -s "$start" ]; then
      ffmpeg -y -sseof -0.15 -i "clips/leg_${prev}_raw.mp4" -frames:v 1 -q:v 2 "$start" 2>/dev/null
    fi
    [ -s "$start" ] || { echo "[leg $i] FATAL: no start frame $start"; exit 1; }
  fi

  ok=0
  for t in $(seq 1 $TRIES); do
    echo "[leg $i] attempt $t (start=$start)"
    higgsfield generate create "$VMODEL" \
      --prompt "$(cat prompts/leg_${i}.txt)" \
      --start-image "$start" \
      --mode std --resolution 1080p --aspect_ratio 16:9 --duration 8 \
      --wait --wait-timeout 20m --json > "clips/leg_${i}.json" 2> "clips/leg_${i}.err"
    url=$(python3 -c "
import json,sys
try:
    d=json.load(open('clips/leg_${i}.json'))
    j=d[0]
    print(j['result_url'] if j.get('status')=='completed' and j.get('result_url') else '')
except Exception:
    print('')")
    if [ -n "$url" ]; then
      curl -s -o "$raw" "$url" && [ -s "$raw" ] && ok=1 && break
    fi
    echo "[leg $i] attempt $t failed:"; tail -2 "clips/leg_${i}.err" 2>/dev/null
    python3 -c "
import json
try:
    d=json.load(open('clips/leg_${i}.json')); print('  status:', d[0].get('status'))
except Exception as e: print('  no json:', e)"
    sleep 5
  done
  [ "$ok" = "1" ] || { echo "[leg $i] FAILED after $TRIES tries — stopping chain"; exit 1; }

  # extract this leg's last frame for the next leg + eyeball check
  ffmpeg -y -sseof -0.15 -i "$raw" -frames:v 1 -q:v 2 "frames/leg_${i}_last.png" 2>/dev/null
  echo "[leg $i] DONE -> $raw"
done
echo "ALL LEGS DONE"
