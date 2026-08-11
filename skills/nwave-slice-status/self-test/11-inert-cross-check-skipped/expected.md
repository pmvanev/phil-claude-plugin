# Expected outcome — fixture 11 (a check that cannot discriminate must not be reported as one)

The git cross-check assumes each step owns distinct paths. Here it does not: `implementation_scope`
is roadmap-level and every step shares one `test_file`. Run as written, the log returns the same
commits for all five rows — so the `⚠ no commit found` warning can never fire, and the check's
silence reads as five steps corroborated when nothing was corroborated at all.

A check that cannot fail is worse than no check, because its absence of warnings is mistaken for
evidence.

**Expected decision:** `CROSS-CHECK-SKIPPED`.

**Checkable assertions (all must hold):**

1. The cross-check is skipped, not run-and-ignored.
2. Notes says the paths are not step-distinct, so drift could not be checked.
3. No row carries a drift warning, and no row is presented as git-corroborated.
4. Statuses come from the record alone and are not upgraded by the presence of commits.

**Gate failure (blocks the skill change):** running the log per step and reporting empty Notes, which
silently asserts five clean cross-checks; OR marking every step drifted because the paths did not
resolve; OR omitting the skip from Notes, leaving the reader to assume the check ran.

**Boundary.** Where paths *are* step-distinct, the check runs and its warning fires — see fixture 08.
This fixture pins the degenerate case only.
