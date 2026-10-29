---
client: {client-slug}
address: {street address}
opened: {YYYY-MM-DD}
status: intake        # intake → generating → review → delivered
cost: { credits: 0, hf_credits: 0, aud: 0 }   # derived from ## Ledger — never edit by hand
---

# Job — {address}

## Shots

| # | Shot | Pipeline | Status | Notes |
|---|------|----------|--------|-------|
| 1 | {shot name} | full-frame / masked / video | todo | |

## Log

- {YYYY-MM-DD} intake: {N} shots triaged

## Ledger

<!-- one line per spend; the cost: header is derived from this (gen_runner.py tally) -->
<!-- Higgsfield batches: gen_runner.py run appends here. Magnific/MCP or web spends: gen_runner.py log JOB.md <amount> <hf|cr|aud> <note> -->

---
_Vault: [[jarvis]]_
