#!/bin/bash
# Salisbury postcard reels v3 (Hunter 2026-10-21: no pop animation; hard click-ins spaced out so each clip breathes;
# slower music; click SFX on every card + a heavier click/thud when the logo clicks in).
# Layout from the Solis Postcard Post reference: ink bg, 16:9 cards x37 1006x566 at y 64/678/1290.
# Clips slowed 0.5x (work/slow2). Cards at 0.5 / 3.5 / 6.5s, all hold to 10.4s, hard cut to logo, 13.4s total. 0 credits.
set -e
cd "$(dirname "$0")/.."
P1=0.5; P2=3.5; P3=6.5; CUT=10.4; TOT=13.4
WIND="$HOME/Downloads/traian1984-ambience-wind-blowing-through-trees-01-186986.mp3"
ms() { python3 -c "print(int($1*1000))"; }
reel() { # out music music_start a b c
  out=$1; music=$2; mst=$3
  ffmpeg -v error -y -f lavfi -i "color=c=0x0b0b0a:s=1080x1920:r=50:d=$TOT" \
    -i work/slow2/$4.mp4 -i work/slow2/$5.mp4 -i work/slow2/$6.mp4 \
    -loop 1 -framerate 50 -t $TOT -i assets/endcard_postcard_916.png -ss $mst -i "$music" -i "$WIND" \
    -i assets/sfx/click_1.wav -i assets/sfx/click_5.wav -i assets/sfx/thud_4.wav -filter_complex "
  [1]scale=1006:566:flags=lanczos,unsharp=5:5:0.3,setpts=PTS-STARTPTS+$P1/TB[a];
  [2]scale=1006:566:flags=lanczos,unsharp=5:5:0.3,setpts=PTS-STARTPTS+$P2/TB[b];
  [3]scale=1006:566:flags=lanczos,unsharp=5:5:0.3,setpts=PTS-STARTPTS+$P3/TB[c];
  [0][a]overlay=37:64:eof_action=repeat:enable='between(t,$P1,$CUT)'[o1];
  [o1][b]overlay=37:678:eof_action=repeat:enable='between(t,$P2,$CUT)'[o2];
  [o2][c]overlay=37:1290:eof_action=repeat:enable='between(t,$P3,$CUT)'[o3];
  [o3][4]overlay=0:0:enable='gte(t,$CUT)',format=yuv420p[v];
  [5]atrim=0:$TOT,asetpts=PTS-STARTPTS,afade=in:st=0:d=0.8,afade=out:st=$(python3 -c "print($TOT-2.2)"):d=2.2,loudnorm=I=-16:TP=-2[m];
  [6]atrim=0:$TOT,asetpts=PTS-STARTPTS,volume=0.12,afade=out:st=$(python3 -c "print($TOT-2.2)"):d=2.2[w];
  [7]asplit=3[k1][k2][k3];
  [k1]adelay=$(ms $P1)|$(ms $P1),volume=0.55[s1];[k2]adelay=$(ms $P2)|$(ms $P2),volume=0.55[s2];[k3]adelay=$(ms $P3)|$(ms $P3),volume=0.55[s3];
  [8]adelay=$(ms $CUT)|$(ms $CUT),volume=0.7[s4];[9]adelay=$(ms $CUT)|$(ms $CUT),volume=0.6[s5];
  [m][w][s1][s2][s3][s4][s5]amix=inputs=7:normalize=0:duration=first,alimiter=limit=0.89[aout]" \
  -map "[v]" -map "[aout]" -c:v libx264 -crf 16 -preset slow -c:a aac -b:a 256k -ar 48000 -movflags +faststart -t $TOT reels/$out
}
reel salisbury_reel1_arrival_916.mp4 "$HOME/Downloads/AVE - Meet Me In The Dark (Official Audio).mp3" 1.5 01_exterior_v1 11_hallway_v1 06_kitchen_v1
reel salisbury_reel2_inside_916.mp4 "$HOME/Downloads/Relax My Eyes.mp3" 0 04_living_v1 08_bedroom_v1 05_powder_v3
