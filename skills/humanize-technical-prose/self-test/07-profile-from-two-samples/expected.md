# Expected — HTP-SELFTEST-07

`PROFILE-BUILT`

## What must happen

- The script measures both samples. Each is over 500 words of own prose, so neither is thin.
- The slip tally counts three slips: one *swapped letters* misspelling, one *doubled word* (revision
  residue) and one *wrong form* (substitution). `on_name_or_term` is zero.
- The profile is written to `~/.claude/humanize-technical-prose/profiles/plain.json`, and the report
  names that path.
- The report's `PROFILE-BUILT` line gives 2 samples, the words measured, the sentence median and 90th
  percentile, zero contractions, zero questions, and the slips split into grammar 2 and spelling 1.

## What must NOT happen

- No phrase holding *Halvorsen* is stored, because the sentence names a client.
- No word of the colleague's quotation is measured or stored.
- The code block adds nothing to the counts.
- The slipped words appear nowhere: not in the profile, the tally or the report.
- No file outside the two named samples is read.

## Why this fixture exists

It is the build's whole contract in one run. Every seeded detail is one the profile must keep out.
