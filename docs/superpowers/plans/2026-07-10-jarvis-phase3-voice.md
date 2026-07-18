# Jarvis Phase 3 (Voice Layer) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Push-to-talk voice Jarvis on Hunter's Mac — hold right-option, speak, get a spoken + on-screen answer; can read CRM/JOB.md/wiki and create to-dos.

**Architecture:** Hammerspoon captures the hotkey and mic (ffmpeg), whisper-cli transcribes locally, `claude -p` (cwd = vault, VOICE-PROMPT.md system prompt) answers, `say -v Daniel` speaks, Hammerspoon overlays the text.

**Tech Stack:** Hammerspoon (Lua), ffmpeg avfoundation, whisper.cpp (`whisper-cli`, base.en model), Claude Code CLI, macOS `say`.

**Spec:** `docs/superpowers/specs/2026-07-10-jarvis-phase3-voice-design.md`

**Already installed:** ffmpeg, whisper-cli, claude 2.1.178. **Missing:** Hammerspoon, whisper model.

---

### Task 1: Install prerequisites

- [ ] **Step 1:** `brew install --cask hammerspoon` — expect "hammerspoon was successfully installed"
- [ ] **Step 2:** Download whisper model:

```bash
mkdir -p ~/.cache/whisper
curl -L -o ~/.cache/whisper/ggml-base.en.bin \
  https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-base.en.bin
```

- [ ] **Step 3:** Verify: `whisper-cli -m ~/.cache/whisper/ggml-base.en.bin -f /opt/homebrew/share/whisper-cpp/jfk.wav -nt -np` → expect JFK quote text.

### Task 2: Verify headless CRM access

- [ ] **Step 1:** From vault cwd run `claude -p "call the list_personal_todos tool and print the titles" --allowedTools "mcp__*"` (short timeout). If titles print → CRM reachable headless. If not → VOICE-PROMPT.md must tell Jarvis to answer task questions with "CRM not reachable by voice yet" and we file a follow-up; do not fake it.

### Task 3: Voice prompt + pipeline script + Hammerspoon config

**Files:** create `projects/jarvis/voice/VOICE-PROMPT.md`, `projects/jarvis/voice/jarvis-ask.sh`, `projects/jarvis/voice/jarvis.lua`; wire `~/.hammerspoon/init.lua`.

- [ ] **Step 1: VOICE-PROMPT.md** — identity + hard rules (full content in repo; key rules: answers ≤3 spoken sentences, plain text no markdown, allowed tools = read vault + CRM list/create todo, NEVER paid ops/file writes/shell side effects).
- [ ] **Step 2: jarvis-ask.sh** — wav → whisper-cli → guard short/empty transcript → `claude -p` with restricted tools → echo answer (Hammerspoon shows it) + `say` unless `.muted` exists.
- [ ] **Step 3: jarvis.lua** — eventtap on flagsChanged keycode 61 (right-option): down = start ffmpeg capture (`-f avfoundation -i :default -ar 16000 -ac 1`), up = `kill -INT` ffmpeg, run jarvis-ask.sh via hs.task, alert overlay for state + answer. Cmd+Alt+J toggles mute file.
- [ ] **Step 4:** Append to `~/.hammerspoon/init.lua`: `dofile(os.getenv("HOME") .. "/Documents/Hunters Second Brain/projects/jarvis/voice/jarvis.lua")`
- [ ] **Step 5:** Commit all files.

### Task 4: Wiki + docs

- [ ] **Step 1:** Update `wiki/concepts/jarvis.md` roadmap item 3 → live, with component paths + permissions caveat. Append `wiki/log.md` entry. Commit, push.

### Task 5: End-to-end test (needs Hunter at keyboard)

- [ ] **Step 1:** Launch Hammerspoon → grant Accessibility permission; first record → grant Microphone permission.
- [ ] **Step 2:** Hold right-⌥, ask "what's on my plate" → spoken + overlay answer within ~5 s listing CRM todos.
- [ ] **Step 3:** "Remind me to call Rob tomorrow" → todo appears in CRM (`list_personal_todos` confirms).
- [ ] **Step 4:** Silent press (no speech) → graceful "didn't catch that".
- [ ] **Step 5:** Fix issues found; if transcripts rough, swap model to `small.en` in jarvis-ask.sh.

---
_Vault: [[jarvis]]_
