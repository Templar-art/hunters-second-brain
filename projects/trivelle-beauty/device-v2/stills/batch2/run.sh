#!/bin/zsh
cd "/Users/10xhunter/Documents/Hunters Second Brain/projects/trivelle-beauty/device-v2"
one() {
  refs=(--image-references stills/01-hero-v2-pilot.png)
  [ "$2" = g ] && refs+=(--image-references stills/09-gel-studio.png)
  higgsfield generate create gpt_image_2 --prompt "$3 Keep the device's exact shape, colour and details from Image 1. No text, no logos added. 4:5." --aspect_ratio 4:5 --resolution 2k "${refs[@]}" --wait > stills/batch2/$1.log 2>&1
  url=$(grep -oE 'https://[^ ]*\.(png|jpg|jpeg|webp)' stills/batch2/$1.log | tail -1)
  [ -n "$url" ] && curl -s -o stills/batch2/$1.${url##*.} "$url"
  echo "$1: $url"
}
n=0
while IFS=$'\t' read -r name g p; do
  one "$name" "$g" "$p" &
  n=$((n+1)); wait
done < stills/batch2/retry.tsv
wait
