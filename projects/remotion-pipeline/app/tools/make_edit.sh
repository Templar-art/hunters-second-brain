#!/bin/sh
# Trim dead air: keep these source ranges (seconds), concat A then B, 15ms audio fades at each join.
set -e
cd "$(dirname "$0")/../public"
A="0.15:3.22 3.53:5.56 6.28:10.18 10.38:12.63 12.80:15.15 16.27:23.19 23.49:25.0"
B="0.27:3.74"
fc=""; n=0; ins=""
for r in $A; do s=${r%:*}; e=${r#*:}; d=$(echo "$e - $s - 0.015" | bc -l)
  fc="$fc[0:v]trim=$s:$e,setpts=PTS-STARTPTS[v$n];[0:a]atrim=$s:$e,asetpts=PTS-STARTPTS,afade=t=in:d=0.015,afade=t=out:st=$d:d=0.015[a$n];"; ins="$ins[v$n][a$n]"; n=$((n+1)); done
for r in $B; do s=${r%:*}; e=${r#*:}; d=$(echo "$e - $s - 0.015" | bc -l)
  fc="$fc[1:v]trim=$s:$e,setpts=PTS-STARTPTS[v$n];[1:a]atrim=$s:$e,asetpts=PTS-STARTPTS,afade=t=in:d=0.015,afade=t=out:st=$d:d=0.015[a$n];"; ins="$ins[v$n][a$n]"; n=$((n+1)); done
ffmpeg -v error -y -i IMG_9573.mp4 -i IMG_9577.mp4 -filter_complex "$fc${ins}concat=n=$n:v=1:a=1[v][a]" -map "[v]" -map "[a]" -r 30 -c:v libx264 -crf 16 -c:a aac -b:a 192k edit.mp4

# Voice chain (talking-head standard): HPF → mud dip → de-ess → gentle comp → presence lift.
# Writes edit_voiced.mp4 (video copied, audio processed). Loudness is normalised after the final mix.
ffmpeg -v error -y -i edit.mp4 -c:v copy -af "highpass=f=80,equalizer=f=300:t=q:w=1:g=-2,deesser=i=0.4,acompressor=threshold=-20dB:ratio=3:attack=10:release=120:makeup=4,equalizer=f=4000:t=q:w=1.5:g=2" -c:a aac -b:a 192k edit_voiced.mp4
