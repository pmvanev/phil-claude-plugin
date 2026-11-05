# Expected — HTP-SELFTEST-21

`WROTE` · `SLIPS-UNMIRRORED` · `SLIPS-WARNING`

## What must happen

- `--allocate paper 3 --misspellings` returns one *dropped letter*, one *added letter* and one
  *doubled word*, and exactly those are added.
- Each misspelling lands on an ordinary word of five letters or more, and spells no other real word.
- `SLIPS-UNMIRRORED` says the samples put 6 of 21 slips on names or technical terms, and none was
  placed there.

## What must NOT happen

- No technical term is misspelled, though the paper's own slips include misspelled terms.
- No misspelling turns one real word into another.
- No number, comparison or hedge that carries a claim changes.

## Why this fixture exists

The paper put six of its fourteen misspellings on names and terms. Copying that would misspell the
words a reader most needs to trust. So the run places none there, and it says how many it could not
mirror.
