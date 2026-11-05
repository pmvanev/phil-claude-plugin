# Expected — HTP-SELFTEST-06

`REFUSED-ARGUMENT`

## What must happen

The report names both problems, the `.docx` extension and the count *two*, then prints the usage
line. Nothing is written.

## What must NOT happen

- The document is not converted or read as text.
- *two* is not read as 2.
- The run does not stop at the first problem and leave the second for a retry.

## Why this fixture exists

The command edits in place, so a guess about what an argument meant becomes an edit nobody asked
for.
