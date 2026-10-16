#!/bin/sh
# Cut B-roll selects from Tyson's gym clips: crop letterbox bars, 720x1280 @30fps, muted.
# usage: make_broll.sh <uploads dir>
set -e
U="$1"; D="$(dirname "$0")/../public/broll"; mkdir -p "$D"
cut() { ffmpeg -v error -y -ss "$3" -t "$4" -i "$U"/$1*.mov -an -vf "$2scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280,fps=30" -c:v libx264 -crf 18 "$D/$5.mp4"; }
cut 95dd7eb9 ""                    1.0 3.0 bench-spot
cut f2985f5f "crop=292:518:0:58,"  4.0 3.0 incline-db
cut 67d7e6bb ""                    15.0 3.0 seated-row
cut 67d7e6bb ""                    79.5 3.0 to-camera
cut e84192e6 "crop=440:780:0:88,"  3.0 3.5 squat
