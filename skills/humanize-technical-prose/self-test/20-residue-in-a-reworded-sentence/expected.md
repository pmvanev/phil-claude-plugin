# Expected — HTP-SELFTEST-20

`WROTE` · `SLIPS-WARNING`

## What must happen

One doubled word, such as *the the*, lands in a sentence the voice pass reworded. The `SLIPS 1:`
line names its line and kind.

## What must NOT happen

- The slip does not land in a sentence the voice pass left alone.
- No content word or technical term is doubled.
- `SLIPS-UNMIRRORED` is not printed, because this profile has no slips on names or terms.

## Why this fixture exists

A writer leaves residue where they reworded. The run knows which sentences it reworded, and this
fixture checks that it uses that knowledge.
