# gen-runner

Phase 1 of [Job Framework v2](../../wiki/concepts/job-framework-v2.md). One runner for every Higgsfield generation batch, plus the JOB.md cost ledger and QC contact sheets.

```bash
python3 projects/gen-runner/gen_runner.py estimate path/to/x.jobs.json   # free; quote the total to Hunter
python3 projects/gen-runner/gen_runner.py run path/to/x.jobs.json        # spends; needs Hunter's go (money gate)
python3 projects/gen-runner/gen_runner.py log JOB.md 125 cr "magnific upscale x2"
python3 projects/gen-runner/gen_runner.py tally JOB.md
python3 projects/gen-runner/gen_runner.py sheet qc.jpg out/*.mp4 out/*.png
python3 projects/gen-runner/gen_runner.py qc out/*.mp4 --json qc.json --sheet qc.jpg   # automatic video flags
```

- `run` refuses without an `estimate` from the last 2 h, or when the batch is over the job's `cap_hf`. It skips rows whose output already exists, so a re-run only picks up what failed.
- Transient errors (upload/520/timeout) retry up to 3 times. A failed row is not written to the ledger.
- The money-gate hook (`.claude/hooks/magnific-gate.py`) blocks `gen_runner.py run` and `higgsfield generate create` until Hunter's latest message starts with yes/go/approved.
- Schema and details are in the docstring at the top of `gen_runner.py`.
- Example job file: `projects/blender-blockouts/beach/video/veo-reroll.jobs.json` (96 HF, on hold).
- Magnific stays MCP-driven (`simulate_cost`, then the call). Record each spend with `log`.

Tested 20 Oct 2026: a real estimate on the beach Veo re-roll came to 96 HF, matching the manual quote. A fake-CLI run covered the refusal without an estimate, a transient retry, a permanent failure (not charged), skip-on-rerun, ledger and tally, and the contact sheet. No credits were spent.

## Automatic video QC (phase 5, 20 Oct 2026)

`qc_video.py` flags every video that `run` downloads, and the flags go into `qc-<stamp>.json` and in red on the contact sheet. It also runs standalone via `qc`.

| Flag | Rule | What it catches |
|---|---|---|
| `NO_MOTION` | median optical flow < 0.12 px/frame (frames at 320 px wide); warns below 0.18 | Shot barely moves, or the subject doesn't (beach 01 surf, 07 car) |
| `MORPH/DISSOLVE@t` | ORB matches 6 frames apart stop fitting one homography; 3-sample min inlier ratio < 0.35; warns below 0.50 | Cross-fades, morphs and cuts (beach 06 at 2.0 s) |

Calibration: the 7 beach Seedance clips plus 2 face tests came out **9/9 correct**. The three known failures were flagged, including the dissolve time. Every pass scored ≥ 0.20 motion and ≥ 0.61 continuity. Takes about 5 s per 8 s clip. The flags are prompts to look, not verdicts; the contact sheet is still the final check. It can't see identity drift (a face changing into someone else while the shot stays continuous), so faces still need a look.

**Gate quirk:** the money-gate hook matches the runner's spend command by text, so any Bash command that merely *quotes* it (docs, commit messages) is blocked too. Put such edits in a script file. It also blocks fake-CLI test runs, which is correct, since it can't tell them apart.
