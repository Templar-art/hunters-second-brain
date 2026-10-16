You are upgrading my EXISTING fitness video-production system for online coaches and PTs. The attached fitness-system-kit is the consolidated setup specification. Do not rebuild functioning architecture or replace approved styles.

Read 00_START_HERE, docs/02_SETUP, docs/03_ARCHITECTURE and VERIFICATION first. Inspect the existing repository and current instructions before changes. Then read relevant documents on demand.

GOAL
Client-worthy edits: meaningful shot selection, clear dialogue, deliberate music/sound, readable captions, face/movement-aware graphics, strong typography and purposeful transitions. More effects are not the goal.

WORK PLAN
1. Run the local doctor and inspect installed packages/lockfiles/tool versions. Report implemented, tested, unverified and missing capabilities briefly. Detect OS/architecture and hardware; never assume NVIDIA or Apple Silicon. Do not expose secrets.
2. Preserve current project rules. Propose minimal reversible patches. Do not overwrite CLAUDE.md or package files, install/upgrade software, download weights, spend money, upload private footage or publish without the applicable approval. Use existing equivalents where better.
3. Set up an isolated Python analysis environment and use the current Node project. Start with FFmpeg/ffprobe plus faster-whisper CPU int8 unless supported hardware and test evidence justify another backend. Pin a tested environment after the smoke test. No indiscriminate dependency install.
4. Implement the analysis contract: source-linked word transcript, actual VAD regions, uncertain timing flags, source-to-timeline mapping and caption phrase generation. Alignment/diarisation are optional upgrades. Audit existing capability before adding them.
5. Use one real coach-education pilot with permissioned media. Create a compact brief and three style frames. If no footage exists, render the clearly labelled specimen and list missing production inputs; do not call it editing improvement.
6. Adapt optional Remotion starters. Register the demo without replacing the entry point. Drive animation and audio volume from frame/timeline inputs. Replace placeholders with real approved data. Render before visual claims.
7. Integrate face observations and manually defined movement regions through actual crop transforms. Measure rendered text/card bounds after fonts load. Include entrances/exits and stable placement across each scene. Unknown detection or sparse coverage stays provisional. No safe placement means simplify/recompose/request review, not cover the subject.
8. Keep dialogue/music/SFX separate. Map speech timing to the edited timeline before ducking. Use local audio analysis plus actual listening. Ask for destination-specific mastering targets; do not enforce the synthetic test target universally.
9. Evaluate actual render evidence. Still images cannot establish motion, pacing, sync or audio quality. Use null/NOT_ASSESSED for unavailable modalities. Return timecoded findings and specific fixes with preserve lists.
10. Bound automatic creative revision to two passes and configured compute budget. Freeze approved elements. Human approval required for delivery and permanent taste rules. Run regressions before shared changes.

DELIVER
Short audit; patches actually made; exact commands/checks run; actual previews/style frames; technical PASS/FAIL/NOT_ASSESSED table; unresolved issues; feedback-ready revision record. Do not stop at a giant plan. First response should be a short audit and smallest compatible execution plan, then proceed where authorised.
