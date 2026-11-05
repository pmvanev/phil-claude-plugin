# Expected — HTP-SELFTEST-10

`PROFILE-BUILT`

## What must happen

The run reads the existing profile's `samples`, adds `b.md`, and rebuilds from both. Both samples are
measured by the script and read again for slips. The report gives 2 samples.

## What must NOT happen

- The profile is not replaced by one built from `b.md` alone.
- Old totals are not summed with new ones, and the old slip tally is not reused.
- `a.md` is not counted twice.

## Why this fixture exists

Overwriting would lose the first sample without a word, and summing totals would double-count
phrases that recur across samples.
