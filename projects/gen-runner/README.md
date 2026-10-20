# gen-runner

Phase 1 of [Job Framework v2](../../wiki/concepts/job-framework-v2.md). One runner for every Higgsfield generation batch, plus the JOB.md cost ledger and QC contact sheets.

```bash
python3 projects/gen-runner/gen_runner.py estimate path/to/x.jobs.json   # free; quote the total to Hunter
python3 projects/gen-runner/gen_runner.py run path/to/x.jobs.json        # spends; needs Hunter's go (money gate)
python3 projects/gen-runner/gen_runner.py log JOB.md 125 cr "magnific upscale x2"
python3 projects/gen-runner/gen_runner.py tally JOB.md
python3 projects/gen-runner/gen_runner.py sheet qc.jpg out/*.mp4 out/*.png
```

- `run` refuses without an `estimate` from the last 2 h, or when the batch is over the job's `cap_hf`. It skips rows whose output already exists, so a re-run only picks up what failed.
- Transient errors (upload/520/timeout) retry up to 3 times. A failed row is not written to the ledger.
- The money-gate hook (`.claude/hooks/magnific-gate.py`) blocks `gen_runner.py run` and `higgsfield generate create` until Hunter's latest message starts with yes/go/approved.
- Schema and details are in the docstring at the top of `gen_runner.py`.
- Example job file: `projects/blender-blockouts/beach/video/veo-reroll.jobs.json` (96 HF, on hold).
- Magnific stays MCP-driven (`simulate_cost`, then the call). Record each spend with `log`.

Tested 20 Oct 2026: a real estimate on the beach Veo re-roll came to 96 HF, matching the manual quote. A fake-CLI run covered the refusal without an estimate, a transient retry, a permanent failure (not charged), skip-on-rerun, ledger and tally, and the contact sheet. No credits were spent.
