# Elevra Media — invoice generator

Rebuild of the `EM-260713-001` invoice as a re-runnable generator. Config in, A4 PDF out.

## Run

```bash
cd projects/elevra-invoices
python3 make_invoice.py invoices/EM-260724-002.json
```

Writes `<name>.html` and `<name>.pdf` beside the JSON. Stdlib only — no pip installs. PDF is
produced by headless Chrome (binary lives on the Desktop on this machine, not `/Applications`).

## New invoice

Copy the previous JSON, bump `invoice_no` and `date`, swap the `items`. Nothing else changes.

- **Numbering:** `EM-YYMMDD-NNN`, where the date is the invoice date and `NNN` is the sequence
  for that day. `001` = 13/07/2026.
- **GST** is a *string* (`"Not applicable"`), because ABN 84 992 512 038 is not GST-registered.
  Printing `$0.00` would wrongly imply a 0%-rated supply. Set it to a number only if that changes.
- **`items[].total`** is optional — it defaults to `qty × rate`. Set it explicitly only for a
  flat-fee or discounted line.

## Fidelity

Layout was reverse-engineered from the original PDF, not eyeballed: text baselines were extracted
with PyMuPDF and the CSS tuned until they matched. Worst remaining drift is **1.3 mm**, one page,
same Helvetica base-14 font and same Tailwind slate/blue-600 palette. Invoices in one sequence have
to look identical, so re-check the y-positions if the template is ever edited.

## Files

| File | Purpose |
|---|---|
| `make_invoice.py` | Renderer: JSON → HTML → PDF |
| `invoice_template.html` | Layout, `__PLACEHOLDER__` slots |
| `invoices/*.json` | One config per issued invoice — the record of what was billed |
| `invoices/*.pdf` | The sent artefact |

⚠️ The JSON configs contain BSB + account number. They are in the vault git repo — see the
payment block before pushing anywhere public.
