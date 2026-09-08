# Expected — WSUM-SELFTEST-09

`SUMMARY-RENDERED` · `ATTRIBUTION-INCOMPLETE` · `READ-ONLY`

## What must happen

The slice is summarised from the commits that could be attributed. One line says how many in the range
could not be.

## What must NOT happen

The unattributed commit is not assigned on a guess, and not on file-path overlap — that would sweep in
any unrelated work touching the same files, which on a small repo is most of it.

The count is not omitted. It is the only signal the reader has that the landed view is partial, and a
landed view is precisely the thing that must not be silently incomplete.

The command does not refuse. A partial reconciliation with its gap named beats none.

## Why this fixture exists

Four of this repo's last nine commits name no slice, and one is a **precursor** — the work a slice does
before its headline change, which is exactly the work its brief is least likely to have described. So the
convention fails hardest on the content this mode exists to surface.
