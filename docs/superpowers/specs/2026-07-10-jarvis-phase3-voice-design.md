# Jarvis — Phase 3 Design (Voice Layer)

**Date:** 2026-07-10
**Status:** Approved by Hunter (approach A)
**Predecessors:** [Phase 1](2026-07-10-jarvis-phase1-design.md), [Phase 2](2026-07-10-jarvis-phase2-job-tracking-design.md)

## Scope

Push-to-talk voice interface to Jarvis on Hunter's Mac. Hold a hotkey → speak → Jarvis answers aloud and on screen.

- **Interaction:** push-to-talk (hold right-option). No wake word, no always-listening mic.
- **Powers:** ask + capture. Reads CRM to-dos, JOB.md files, the vault wiki. May create personal to-dos via the CRM MCP. No other writes, no file edits, no paid generation — ever, regardless of what is heard.
- **Output:** spoken answer (macOS `say`, voice Daniel en_GB) plus on-screen text overlay. Mute toggle hotkey.

## Architecture (approach A — Hammerspoon glue)

```
hold right-⌥ ──▶ Hammerspoon records mic (ffmpeg avfoundation, 16 kHz wav)
release      ──▶ whisper-cli (local, base.en model) → transcript
             ──▶ claude -p transcript, cwd = vault, system prompt = VOICE-PROMPT.md
             ──▶ answer → say -v Daniel (aloud) + hs.alert overlay (screen)
```

All components local and free except the Claude call (subscription CLI). Each stage swappable independently (better TTS, bigger whisper model, different hotkey).

## Components

- `projects/jarvis/voice/jarvis.lua` — Hammerspoon config: hotkey down = start ffmpeg mic capture; hotkey up = stop, run pipeline script async, show busy indicator; mute toggle (right-⌥ + M behaviour defined in file).
- `projects/jarvis/voice/jarvis-ask.sh` — pipeline: wav → whisper-cli → transcript guard (empty/too short → "didn't catch that") → `claude -p` → strip to spoken answer → `say` + overlay text via Hammerspoon IPC.
- `projects/jarvis/voice/VOICE-PROMPT.md` — system prompt: identity, allowed tools (CRM list/create todo, read-only vault/JOB.md access), hard bans (no paid ops, no file writes, no shell side effects), answer style ≤3 spoken-friendly sentences, no markdown in output.
- Hammerspoon `init.lua` requires `jarvis.lua` via symlink or loader line.

## Risks / build-time verifications

1. **Headless CRM access:** `claude -p` may not see the claude.ai `10x-crm` connector. Verify first; if absent, voice answers task questions from morning-brief cache or says so honestly — and we wire a local MCP config as follow-up.
2. **Whisper accuracy** on fast Australian speech: start with `base.en`, escalate to `small.en` if transcripts are rough.
3. **Mic + accessibility permissions:** macOS will prompt for Hammerspoon (accessibility) and ffmpeg/terminal (microphone) on first use — needs Hunter at the keyboard.

## Success criteria

Hold key, ask "what's on my plate", release → spoken + on-screen answer listing current CRM to-dos within ~5 s. "Remind me to call Rob tomorrow" → to-do appears in CRM. Mishears or empty audio fail gracefully, aloud.

---
_Vault: [[jarvis]]_
