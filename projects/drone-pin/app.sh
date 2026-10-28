#!/bin/zsh
# Drone Pin.app backend: open (or start) a review job for a folder of drone stills.
#   app.sh <photos folder> [address]
# Prints JOB=<dir> when the folder already has a job, NEED_ADDRESS when it needs one,
# or ERROR=<message>. With an address it creates the job, then serves the review page
# and opens it in the browser.
set -u
HERE=${0:A:h}
PY=~/.venvs/typeset/bin/python
photos=${1:A}
address=${2:-}
slug=$(print -r -- "${photos:t}" | tr -cs 'A-Za-z0-9' '-' | sed 's/^-//; s/-$//')
# Job lives beside the tool, keyed by the photo folder's name and its parent (Done/Drone → "<job>-Drone").
parent=$(print -r -- "${photos:h:h:t}" | tr -cs 'A-Za-z0-9' '-' | sed 's/^-//; s/-$//')
job="$HERE/jobs/${parent:+$parent-}$slug"

if [[ ! -f "$job/site.json" ]]; then
  # No address given: read it (and the client) from the SSD's "Client | Address" folder name.
  guessed=0
  if [[ -z "$address" ]]; then
    address=$("$PY" -I -c 'import sys; sys.path.insert(0, sys.argv[1]); import drone_pin as d; print(d.from_folder(sys.argv[2])[1] or "")' "$HERE" "$photos")
    [[ -z "$address" ]] && { print "NEED_ADDRESS"; exit 0; }
    guessed=1
  fi
  if ! out=$("$PY" -I "$HERE/drone_pin.py" init "$job" "$photos" --address "$address" 2>&1); then
    rm -rf "$job"
    (( guessed )) && { print "NEED_ADDRESS"; exit 0; }   # folder name wasn't enough (no suburb, several matches)
    print -r -- "ERROR=$(print -r -- "$out" | tail -1)"; exit 0
  fi
fi

# One review server at a time: stop the last one the app started, then serve this job.
pidf="$HERE/jobs/.server.pid"
[[ -f $pidf ]] && kill $(<$pidf) 2>/dev/null && sleep 0.5
port=8770
nohup "$PY" -I "$HERE/drone_pin.py" review "$job" --port $port >"$HERE/jobs/.server.log" 2>&1 &
print $! >$pidf
print -r -- "JOB=$job"
