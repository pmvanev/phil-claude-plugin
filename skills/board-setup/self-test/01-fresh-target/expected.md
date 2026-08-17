# Expected — BS-SELFTEST-01

`WROTE` · `REPORTED-NOT-WRITTEN`

## What must happen

The forge target is confirmed from the single remote **before** the script runs. The section is
appended, containing only the delimited region. Markers are bare and versioned
(`phil:board-setup:v1:begin` / `:end`) with `generated <timestamp>` on the first line **inside** —
not in the marker itself.

All 11 probed facts are written, including the five carrying no `template_field`. Each bullet cites a
`Q<n>`; `project-and-board-ids`, whose `query` is `"(see project-discovery)"`, cites the referenced
fact's number rather than printing the back-reference.

## What must NOT happen

The two `half_probed` workflow trigger statuses are **reported to the human and kept out of the
file**. Writing `Done` — even labelled — is a slice 04 behaviour and a failure here.

No question is asked beyond confirming the target.

## Why this fixture exists

This is the only path where a wrong result still looks like a success. A region containing a
remembered id, a guessed trigger status, or a dropped fact renders identically to a correct one; the
file gives no signal. The fixture is the signal.
