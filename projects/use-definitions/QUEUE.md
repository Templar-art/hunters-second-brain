# Episode queue

Rules per episode: face check (`render.cjs … facecheck`) must say FACE CLEAR, then `tools/qa.sh` → boss review (`tools/BOSS.md`) loop until PASS, then build and send.

# Episode queue (batch from Hunter, 9 Oct 2026)
Source clips: ~/Downloads/NN_OCTOBER TALKING HEADS.mp4. Transcripts in episodes/<name>/words.json.

Skipped:
- 01 API, 02 MCP: raw clips of the already-published reference episodes.
- 13 (1), 22 (1): exact duplicates of 13 (CRUD, done) and 22 (bus-network, done).
- 4 Alex Keith zips: unrelated real-estate camera files.

| # | Episode | Type | Status |
|---|---|---|---|
| 03 | cli | Definition | v2 boss-passed, sent |
| 04 | json | Definition | v2 boss-passed, sent |
| 05 | sdk | Definition | v2 boss-passed, sent |
| 06 | ui-ux | Definition | v1 boss-passed, sent |
| 07 | ide | Definition | v1 boss-passed, sent |
| 08 | saas | Definition | v1 boss-passed, sent |
| 09 | gpu | Definition | v1 boss-passed, sent |
| 10 | cpu | Definition | v1 boss-passed, sent |
| 11 | git | Definition | v1 boss-passed, sent |
| 12 | docker | Definition | v1 boss-passed, sent |
| 14 | webhooks | Definition | v1 boss-passed, sent |
| 15 | state-management | Definition | v1 boss-passed, sent |
| 16 | sql | Definition | v1 boss-passed, sent |
| 17 | erd | Definition | v1 boss-passed, sent |
| 18 | excel-wince | Q&A | v1 boss-passed, sent |
| 19 | scope-myth | Q&A | v1 boss-passed, sent |
| 20 | promises | Q&A | v1 boss-passed, sent |
| 21 | ask-the-vision | Q&A | v1 boss-passed, sent |
| 23 | handover | Q&A | v1 boss-passed, sent |

# v2 redo pass (Hunter, 20 Oct 2026): all 21 episodes, ONE AT A TIME

Hunter: redo every sent episode with everything improved since, and make each one better. **Strictly one episode at a time.** Each one gets Hunter's look before the next starts, so a lesson from one carries into the next. Nothing is re-sent to USE without Hunter's go.

What "updated" means. Apply all of it to each episode:
- **SFX** (the biggest gap; Hunter rated the current effects poor): replace the synth and 1s Magnific takes with real library sounds. Sources: the Ocular Sounds packs in `~/Music/SFX Library/Ocular Sounds/` (auto-sorted by the [[sfx-sorter]]), the free commercial packs being collected by the asset-library session, and [Sound Lab](../sound-lab/) for custom 48k/24 renders. Cues stay driven by the components so sound matches motion.
- **Gates** ([[job-framework-v2]] style, adapted for motion): A = what changes on this episode → build → B = Hunter reviews v-next → C = final before sending.
- **Existing rules still apply:** FACE CLEAR check, `tools/qa.sh`, the boss review loop (`tools/BOSS.md`), never cover the face, pop-ups never over text, no text off-screen.
- **Automatic QC:** run `gen_runner.py qc` on each render to catch frozen sections or accidental dissolves, plus a contact sheet.
- Keep the v1/v2 finals and write the new one as the next version number.

Order: as listed (01 CRUD first, the anchor episode). Update the row after every step.

| # | Episode | Current final | v2-redo status |
|---|---|---|---|
| 01 | crud | v6 | ✅ **LOCKED v7** (Hunter, 20 Oct). Sound Lab UI + Ocular kit (sfx-lib-v2), SUB16/shutter .5 blur, cuts list, shards off face, alive end card. QC ok, FACE/TEXT CLEAR, −17.5 LUFS |
| 02 | bus-network | v2 | ✅ **LOCKED v3** (Hunter, 20 Oct). v7 upgrades ported (cuts, qcAllow, alive end card, sfx-lib-v2, SUB16/shutter .5); hook shards moved off the ear; panel caption holds at 1200 until pushed (was clipped); Simple./Standard. restacked on two lines, each on its spoken word (Hunter caught the overprint), plus buses running the standard grid and a grid push to kill the 0.8 s freeze this exposed. QC ok, RISE CLEAR, FACE/TEXT CLEAR, −15.8 LUFS (= v2) |
| 03 | cli | v2 | ✅ **LOCKED v3** (Hunter, 20 Oct). Upgrades ported (qcAllow, shards off face, alive end card, sfx-lib-v2, SUB16/shutter .5). QC caught 3 freezes in the CRT scene, fixed with a cursor that glides in and clicks Get started, a CRT roll band and a slow push. Card-stack labels were hugging the edge, fixed in the engine with measured width. QC ok, FACE/TEXT/RISE CLEAR, −16.5 LUFS (= v2) |
| 04 | json | v3 | ✅ **LOCKED v4** (Hunter, 20 Oct). Upgrades ported (qcAllow, shards off face, alive end card, sfx-lib-v2, SUB16/shutter .5). QC found file icons + type cards sitting dead between beats, fixed with an idle float. QC ok, FACE/TEXT/RISE CLEAR, −16.6 LUFS (= v3) |
| 05 | sdk | v3 | ✅ **LOCKED v4** (Hunter, 20 Oct). Upgrades ported. QC found 6 dead stretches (wrap diagram 7–13.5 s, stack 20.7–22.4 s), fixed with a wrap pulse ring, request packets dev→SDK, and the stack floating as one unit. QC ok, FACE/TEXT/RISE CLEAR, −16.5 LUFS (= v3) |
| 06 | ui-ux | v1 | ✅ **LOCKED v2** (Hunter, 20 Oct). Upgrades ported; dead holds pre-fixed from a still_scan of v1 (the phone floats + sways), so it passed first build. QC ok, FACE/TEXT/RISE CLEAR, no still stretches, −17.4 LUFS (v1 −17.3) |
| 07 | ide | v2 | ✅ **LOCKED v3** (Hunter, 20 Oct). Upgrades ported; still_scan of v2 found the IDE window still ~8 s, pre-fixed with a window float (both passes). First-build pass. QC ok, FACE/TEXT/RISE CLEAR, no still stretches, −16.1 LUFS (= v2) |
| 08 | saas | v1 | ✅ **LOCKED v2** (Hunter, 20 Oct). Upgrades ported; dead holds pre-fixed (app card float, a 'this month' ring stepping the calendar, update packets hub→companies). First-build pass. QC ok, FACE/TEXT/RISE CLEAR, no still stretches, −17.9 LUFS (= v1) |
| 09 | gpu | v1 | ✅ **LOCKED v2** (Hunter, 20 Oct). Upgrades ported; dead holds pre-fixed (workload sweep through the racks, idle core twinkle, NN pass starts once built). First build; 3 LOOK flags were deliberate transitions with too-tight allow windows (fixed, no rebuild). QC ok, FACE/TEXT/RISE CLEAR, −16.6 LUFS (v1 −16.5) |
| 10 | cpu | v2 | ✅ **LOCKED v3** (Hunter, 20 Oct). Upgrades ported; dead holds pre-fixed (cores take turns, traces grow on chip landing with early pulses, Memory/CPU cards float, packet bobs). still_scan caught 0.5 s at 16.1 s, fixed by starting the pulses earlier. QC ok, FACE/TEXT/RISE CLEAR, no still stretches, −17.2 LUFS (v2 −17.1) |
| 11 | git | v2 | ✅ **LOCKED v3** (Hunter, 20 Oct). Upgrades ported; 16 dead holds in v2 pre-fixed (repo card floats with pulse rings, devs type and bob, sync starts on landing, clashing laptops shake, merge cards float + merged lanes shimmer, commits climb the tree and run every branch, customers bob). One LOOK flag at 24.1 s was the whip entry, window widened without a rebuild. QC ok, FACE/TEXT/RISE CLEAR, no still stretches, −15.2 LUFS (v2 −15.1) |
| 12 | docker | v1 | ✅ **LOCKED v2** (Hunter, 20 Oct). Upgrades ported; 10 dead holds in v1 pre-fixed (source container floats with a shine sweep and copy beams reaching each machine, copies bob, the two computers float in opposite phase, mismatch ✗s pulse, escape attempts bounce off the shield with ripple rings). First build froze 1.3 s in the copy scene: a float alone doesn't register on the light background, so the beams and shine were added. QC ok, FACE/TEXT/RISE CLEAR, no still stretches, −17.8 LUFS (v1 −17.8) |
| 13 | webhooks | v1 | skip: already done by USE (Damon Hall, 10 Oct) |
| 14 | state-management | v1 | ✅ **LOCKED v2** (Hunter, 20 Oct). Upgrades ported; 5 dead holds in v1 pre-fixed (stored chips keep floating with pulse rings off the store; a cursor clicks the tabs, one click per re-fetch line in the log, with spinners, then rides the bobbing NOT NEEDED pill). First build passed QC, but still_scan found two ~0.5 s holds; the cursor glides were lengthened and the pill bobs. QC ok, FACE/TEXT/RISE CLEAR, no still stretches, −17.2 LUFS (v1 −17.2) |
| 15 | sql | v1 | skip: already done by USE (Damon Hall, 9 Oct) |
| 16 | erd | v1 | ✅ **LOCKED v2** (Hunter, 20 Oct). Upgrades ported; 4 dead holds in v1 pre-fixed (a blueprint scanner bar sweeps the sheet, records flow from users to houses along the connector). The face circle moved off the houses table, which it overlapped in v1. QC ok, FACE/TEXT/RISE CLEAR, no still stretches, −17.4 LUFS (v1 −17.3) |
| 17 | excel-wince | v3 | ✅ **LOCKED v4** (Hunter, 20 Oct). Upgrades ported. The Q&A opener is now alive engine-wide (shards drift, rings pulse off the QUESTION pill, a caret blinks, the face circle bobs), and the end card is alive. The boss review caught "Complete and utter garbage." running into the face circle (also in v3, missed by TEXT CLEAR), so it was raised and shrunk. QC ok, FACE/TEXT/RISE CLEAR, no still stretches, −16.4 LUFS (v3 −16.4) |
| 18 | scope-myth | v2 | **v3 built → Gate B.** Upgrades ported; dead holds pre-fixed (the alive Q&A opener from the engine; the scope's core cards float and fill progress bars as they get built, the scope border marches, the Manageable pill bobs; alive end card). The boss review caught the Over-delivered pill touching the caption (also in v2), so it moved inside the delivery card. QC ok, FACE/TEXT/RISE CLEAR, no still stretches, −17.6 LUFS (v2 −17.6) |
| 19 | promises | v2 | todo |
| 20 | ask-the-vision | v1 | todo |
| 21 | handover | v1 | todo |

**Redo workflow (from 06 on):** run `python3 tools/still_scan.py episodes/<ep>/<ep>-<old>.mp4` FIRST and pre-fix every dead hold with on-story motion. Then port (qcAllow, shards [985,800], alive end card), build with `SFX_LIB=sfx-lib-v2 SUB=16 SHUTTER=0.5`, then run `tools/qc_episode.py`, `tools/qa.sh` (FACE/TEXT/RISE CLEAR), and `still_scan` on the new render. Allow windows around a hard cut need ±0.3 s: QC compares frames 0.2 s apart, so a tight window still trips LOOK. Widening a window needs no rebuild; just re-run `qc_episode.py`.
