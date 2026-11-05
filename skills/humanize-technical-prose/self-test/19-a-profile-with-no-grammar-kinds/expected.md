# Expected — HTP-SELFTEST-19

`WROTE` · `SLIPS-NONE-OF-KIND`

## What must happen

- The tells and voice passes run.
- `--allocate spelling 2` returns `none_of_kind`, and no slip is added.
- `SLIPS-NONE-OF-KIND` says the profile holds only *dropped letter* and *wrong vowel* misspellings,
  and none may be added without `--misspellings`.

## What must NOT happen

- No misspelling is added without `--misspellings`.
- No grammar kind is invented.
- `SLIPS-WARNING` is not printed.

## Why this fixture exists

A profile with no grammar kinds gives the default nothing to add. Falling back to misspellings or a
built-in list would break both the default and the rule that slips come from the samples.
