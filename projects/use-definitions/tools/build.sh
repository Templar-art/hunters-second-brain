#!/bin/zsh
# Render + mix an episode. Usage: tools/build.sh <episode-name> [version-label]
# MIX_ONLY=1 skips the picture render (audio/music changes only).
# Output: episodes/<name>/<name>-<label>.mp4. Optional episodes/<name>/music.wav is ducked under the VO.
set -e; ROOT="${0:a:h:h}"; EP="$ROOT/episodes/$1"; V="${2:-latest}"
export NODE_PATH="$ROOT/tools/node_modules"
[[ -n "$MIX_ONLY" ]] || node "$ROOT/tools/render.cjs" "$EP" video   # MIX_ONLY=1 re-mixes audio without re-rendering
DUR=$(python3 -c "import json;print(json.load(open('$EP/build/render.json'))['dur'])")
VOEND=$(python3 -c "import json;print(json.load(open('$EP/build/render.json'))['voEnd'])")
"$ROOT/.venv/bin/python" "$ROOT/tools/sfx.py" "$EP" "$DUR"
VO="[1:a]atrim=0:$VOEND,afade=t=out:st=$((VOEND-0.2)):d=0.2,loudnorm=I=-16:TP=-1.5,aresample=48000,aformat=channel_layouts=stereo,apad"
if [[ -f "$EP/music.wav" ]]; then
  MIX="${VO},asplit[vo][key];[2:a]volume=0.9[fx];[3:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:${DUR},volume=0.35[m];[m][key]sidechaincompress=threshold=0.05:ratio=8:attack=20:release=300[md];[vo][fx][md]amix=inputs=3:duration=shortest:normalize=0,alimiter=limit=0.95,atrim=0:${DUR}[a]"
  IN=(-i "$EP/build/picture.mp4" -i "$EP/source.mp4" -i "$EP/build/sfx.wav" -i "$EP/music.wav")
else
  MIX="${VO}[vo];[2:a]volume=0.9[fx];[vo][fx]amix=inputs=2:duration=shortest:normalize=0,alimiter=limit=0.95,atrim=0:${DUR}[a]"
  IN=(-i "$EP/build/picture.mp4" -i "$EP/source.mp4" -i "$EP/build/sfx.wav")
fi
ffmpeg -v error -y "${IN[@]}" -filter_complex "$MIX" -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 256k -movflags +faststart "$EP/$1-$V.mp4"
echo "built $EP/$1-$V.mp4"
