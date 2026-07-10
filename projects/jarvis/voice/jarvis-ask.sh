#!/bin/bash
# Jarvis voice pipeline: wav -> whisper -> claude -> answer (stdout) + TTS.
# Called by jarvis.lua with the recorded wav path. Prints the spoken answer.
set -uo pipefail

WAV="${1:?usage: jarvis-ask.sh <wav>}"
DIR="$(cd "$(dirname "$0")" && pwd)"
VAULT="$HOME/Documents/Hunters Second Brain"
MODEL="$HOME/.cache/whisper/ggml-base.en.bin"
VOICE="Daniel"
MUTE_FLAG="$DIR/.muted"

speak() {
  [ -f "$MUTE_FLAG" ] || say -v "$VOICE" "$1" &
}

if [ ! -s "$WAV" ]; then
  speak "I didn't hear anything."
  echo "I didn't hear anything."
  exit 0
fi

TRANSCRIPT="$(whisper-cli -m "$MODEL" -f "$WAV" -nt -np 2>/dev/null | tr '\n' ' ' | sed -E 's/^ +| +$//g')"

if [ "${#TRANSCRIPT}" -lt 4 ]; then
  speak "Didn't catch that."
  echo "Didn't catch that."
  exit 0
fi

echo "» $TRANSCRIPT" >>"$DIR/ask.log"

ANSWER="$(cd "$VAULT" && env -u ANTHROPIC_BASE_URL claude -p "$TRANSCRIPT" \
  --append-system-prompt "$(cat "$DIR/VOICE-PROMPT.md")" \
  --allowedTools "Read,Grep,Glob" \
  --disallowedTools "Write,Edit,NotebookEdit,Bash,WebFetch,WebSearch" \
  2>>"$DIR/ask.log")"

if [ -z "$ANSWER" ]; then
  ANSWER="Something went wrong talking to the brain. Check the ask log."
fi

echo "« $ANSWER" >>"$DIR/ask.log"
speak "$ANSWER"
echo "$ANSWER"
