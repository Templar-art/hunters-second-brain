#!/bin/bash
# Two slow 9:16 reels from the slowed 16:9 clips: 608px vertical slice per clip, 1s dissolves, fade in/out. 0 credits.
set -e
cd "$(dirname "$0")/.."
reel() { # out a xa b xb c xc
  out=$1; shift
  ffmpeg -v error -y -i work/slow/$1.mp4 -i work/slow/$3.mp4 -i work/slow/$5.mp4 -filter_complex "
  [0]trim=0:6.9,setpts=PTS-STARTPTS,crop=608:1080:$2:0,scale=1080:1920:flags=lanczos,unsharp=5:5:0.35,fps=50,format=yuv420p[a];
  [1]trim=0:6.9,setpts=PTS-STARTPTS,crop=608:1080:$4:0,scale=1080:1920:flags=lanczos,unsharp=5:5:0.35,fps=50,format=yuv420p[b];
  [2]trim=0:6.9,setpts=PTS-STARTPTS,crop=608:1080:$6:0,scale=1080:1920:flags=lanczos,unsharp=5:5:0.35,fps=50,format=yuv420p[c];
  [a][b]xfade=transition=fade:duration=1:offset=5.9[ab];[ab][c]xfade=transition=fade:duration=1:offset=11.8,fade=in:st=0:d=0.6,fade=out:st=17.7:d=1[v]" \
  -map "[v]" -c:v libx264 -crf 16 -preset slow -an -movflags +faststart reels/$out
}
reel salisbury_reel1_arrival_916.mp4 01_exterior_v1 876 11_hallway_v1 596 06_kitchen_v1 656
reel salisbury_reel2_inside_916.mp4 04_living_v1 646 08_bedroom_v1 826 05_powder_v3 296
