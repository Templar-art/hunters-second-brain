#!/bin/bash
# Salisbury "postcard" reels (layout matched to Hunter's Solis Postcard Post reference):
# ink background, three 16:9 cinemagraphs stacked full width (x37, 1006x566 at y 64/678/1290),
# each pops in with a hard cut and plays from its pop, then a hard cut to the bone-tinted Salisbury logo.
# No dissolves, no fade to black (Hunter). Music + soft wind bed; only the audio fades out. 0 credits.
set -e
cd "$(dirname "$0")/.."
P1=0.5; P2=1.2; P3=1.9; CUT=7.4; TOT=10.0
WIND="$HOME/Downloads/traian1984-ambience-wind-blowing-through-trees-01-186986.mp3"
reel() { # out music a b c
  out=$1; music=$2
  ffmpeg -v error -y -f lavfi -i "color=c=0x0b0b0a:s=1080x1920:r=50:d=$TOT" \
    -i work/slow/$3.mp4 -i work/slow/$4.mp4 -i work/slow/$5.mp4 \
    -loop 1 -framerate 50 -t $TOT -i assets/endcard_postcard_916.png -i "$music" -i "$WIND" -filter_complex "
  [1]scale=1006:566:flags=lanczos,unsharp=5:5:0.3,setpts=PTS-STARTPTS+$P1/TB[a];
  [2]scale=1006:566:flags=lanczos,unsharp=5:5:0.3,setpts=PTS-STARTPTS+$P2/TB[b];
  [3]scale=1006:566:flags=lanczos,unsharp=5:5:0.3,setpts=PTS-STARTPTS+$P3/TB[c];
  [0][a]overlay=37:64:eof_action=pass:enable='between(t,$P1,$CUT)'[o1];
  [o1][b]overlay=37:678:eof_action=pass:enable='between(t,$P2,$CUT)'[o2];
  [o2][c]overlay=37:1290:eof_action=pass:enable='between(t,$P3,$CUT)'[o3];
  [o3][4]overlay=0:0:enable='gte(t,$CUT)',format=yuv420p[v];
  [5]atrim=0:$TOT,asetpts=PTS-STARTPTS,afade=in:st=0:d=0.4,afade=out:st=$(python3 -c "print($TOT-2)"):d=2,volume=0.9[m];
  [6]atrim=0:$TOT,asetpts=PTS-STARTPTS,volume=0.18,afade=out:st=$(python3 -c "print($TOT-2)"):d=2[w];
  [m][w]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[aout]" \
  -map "[v]" -map "[aout]" -c:v libx264 -crf 16 -preset slow -c:a aac -b:a 256k -ar 48000 -movflags +faststart -t $TOT reels/$out
}
reel salisbury_reel1_arrival_916.mp4 "$HOME/Downloads/AURENZA - Found my Way.mp3" 01_exterior_v1 11_hallway_v1 06_kitchen_v1
reel salisbury_reel2_inside_916.mp4 "$HOME/Downloads/AVE - Meet Me In The Dark (Official Audio).mp3" 04_living_v1 08_bedroom_v1 05_powder_v3
