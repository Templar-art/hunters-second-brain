#!/bin/zsh
cd "/Users/10xhunter/Documents/Hunters Second Brain/projects/trivelle-beauty/device-v2"
S=/private/tmp/claude-502/-Users-10xhunter-Documents-Hunters-Second-Brain/9974ae33-b8a7-4036-b036-3b4ab4bb421b/scratchpad
gen() { # name line
  P="A friendly woman in a beige knit jumper sits on a cream sofa in a bright living room, holding up a white handheld skincare device toward the camera like a casual product recommendation video. She smiles and says once, clearly, in an Australian accent: \"$2\" The brand name Trivelle is pronounced triv-ELL, rhyming with bell. Fully clothed, natural daylight, no music."
  higgsfield generate create marketing_studio_video --mode ugc --duration 8 --resolution 720p --aspect_ratio 9:16 --generate_audio true --start-image $S/presenter.jpg --avatar_ids '["14a92875-b433-47c8-8171-cd31396d1320"]' --image-references stills/01-hero-v2-pilot.png --prompt "$P" --wait > hooks/batch2/$1.log 2>&1
  url=$(grep -o 'https://[^ ]*\.mp4' hooks/batch2/$1.log | tail -1)
  [ -n "$url" ] && curl -s -o hooks/batch2/$1.mp4 "$url"
  echo "$1 done: $url"
}
gen d4 "Okay, does this actually work? Honest answer." &
gen d5 "I was spending a hundred and fifty dollars a month on facials. Now I don't." &
gen d6 "Christmas sorted for Mum. Trust me." &
gen d7 "I'm fifty-four, and this is my ten minutes." &
gen d8 "My daughter keeps stealing this off me." &
gen d9 "Red light therapy, without the salon booking." &
gen d10 "This is my wind-down before bed now." &
gen d11 "Everyone asks what I've done to my skin." &
gen name "It's called Trivelle, and it does four things in one." &
wait
