#!/bin/zsh
# AIOS loop runner — executes one action headless. Used by launchd; same
# engine the dashboard buttons use. Usage: run-action.sh <action-id>
set -u
ACTION="${1:?usage: run-action.sh <action-id>}"
DASH="$(cd "$(dirname "$0")/.." && pwd)"
VAULT="$(cd "$DASH/../.." && pwd)"
PROMPT_FILE="$DASH/actions/$ACTION.md"
LOG="$DASH/logs/$(date +%F)-$ACTION.log"
mkdir -p "$DASH/logs"

# launchd has a bare PATH — add the nvm node bin where claude lives
export PATH="$HOME/.nvm/versions/node/v24.16.0/bin:/usr/local/bin:/opt/homebrew/bin:$PATH"

[[ -f "$PROMPT_FILE" ]] || { echo "missing prompt $PROMPT_FILE" >> "$LOG"; exit 1; }

{
  echo "=== aios loop: $ACTION @ $(date '+%F %T') ==="
  cd "$VAULT" && claude -p "$(cat "$PROMPT_FILE")" \
    --output-format text \
    --permission-mode acceptEdits \
    --allowedTools 'Read,Write,Edit,Glob,Grep,Bash(git add:*),Bash(git commit:*),Bash(git push:*),Bash(git status:*),Bash(git log:*),Bash(ls:*)' \
    --disallowedTools 'mcp__magnific__*,mcp__higgsfield__*' </dev/null
  EXIT=$?
  echo "=== exit $EXIT @ $(date '+%F %T') ==="
  if [[ $EXIT -ne 0 ]]; then
    osascript -e "display notification \"$ACTION failed (exit $EXIT) — see logs\" with title \"AIOS loop\" sound name \"Basso\"" || true
  fi
} >> "$LOG" 2>&1
