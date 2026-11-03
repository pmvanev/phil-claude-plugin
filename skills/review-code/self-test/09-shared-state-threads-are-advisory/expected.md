# Expected outcome — fixture 09 (threads that share state)

`tally.py` holds four functions, all on threads, and `test_tally.py` is green. Two of the four
share mutable state: `count_by_status` sends four threads through one lock to update one dict, and
`count_by_carrier` lets four threads update one dict with no lock at all. `fetch_carrier_statuses`
overlaps independent network waits, and `count_by_region` lets each worker count its own chunk and
merges the counts once at the end.

**Pins:** review-code's paragraph on threads that share mutable state, its Priority 1 race bullet, and
`rules/modern-software-engineering.md`'s *Performance: Concurrency Is Complexity* section.

**How to drive it:** drive this working tree's `skills/review-code/SKILL.md` by hand over this
directory (`/phil:review-code` runs the released copy).

**Expected:** the three items in `expected-backlog.md` — two Advisory items matched on Smell, Route and
a Rationale naming the Farley section, and one Priority 1 race item matched on its lines and its guard.

**Hard assertions (any failure blocks the skill change):**

- **`count_by_status` yields one Advisory question and no defect item about its threads.** The file
  shows the threads and the lock, never the measurement that justified them, so the item asks the
  author for it.
- **`count_by_carrier` yields a Priority 1 race item beside its Advisory.** Its threads write one dict
  with no guard; an Advisory alone downgrades a correctness bug to a question.
- **`fetch_carrier_statuses` raises no item about its threads.** Overlapping independent network waits
  needs no measurement, as the Farley section and review-code's paragraph both say.
- **`count_by_region` raises no item about its threads.** Its workers share nothing until one merge at
  the end, which the section and the paragraph exempt.

**Not a failure:** Priority 2 to 7 items elsewhere — the chunking comprehension the counts repeat,
missing type hints; a note inside an Advisory that a bare thread swallows its exception; line numbers
within ±2.
