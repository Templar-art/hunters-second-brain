---
type: project
tags: [ops, tooling, invoicing]
status: live
updated: 2026-07-27
---

# Elevra Media — invoice generator

A re-runnable invoice tool built 26 Jul 2026 from the original `EM-260713-001` PDF: JSON config in, A4 PDF out. Stdlib Python only, rendered through headless Chrome. Lives in `projects/elevra-invoices/`.

```bash
python3 make_invoice.py invoices/EM-260724-002.json
```

New invoice = copy the previous JSON, bump `invoice_no` and `date`, swap the `items`.

## Decisions worth keeping

- **Numbering is `EM-YYMMDD-NNN`** — the date is the invoice date, `NNN` the sequence within that day. `001` = 13/07/2026.
- **GST is a string, `"Not applicable"`**, because the ABN is not GST-registered. Printing `$0.00` would wrongly imply a zero-rated supply. Only make it a number if registration changes.
- **Fidelity was measured, not eyeballed** — baselines extracted from the original PDF with PyMuPDF and the CSS tuned to match, worst drift 1.3 mm. Invoices in one sequence have to look identical, so re-check y-positions after any template edit.

## ⚠️ Bank details

The `invoices/*.json` configs carry a payment block with BSB and account number, and they sit inside this vault's git repo. The repo is private, but the folder is now excluded in `.gitignore` so the record stays local. If it ever needs to be tracked, pull the payment block into a separate ignored file first.

## Links
[[overview]] · [[business-craft]]

**Generator docs:** [projects/elevra-invoices/README.md](../../projects/elevra-invoices/README.md) — config in, A4 PDF out. The `invoices/` folder itself is gitignored: it carries BSB and account numbers.

