# Expected outcome — fixture 15 (a count that is maintained by hand is not a rollup)

**Where it fails silently.** Both forges really will report `2 of 4` from a roster written as `- [ ] `
checkboxes, and on the day it is written the number is correct. But a checkbox is ticked by a person
and a glyph is regenerated from the artifacts, so the two diverge the first time anyone forgets to tick
— and what the feature displays is the state of the checkboxes. The failure is invisible in exactly the
way the rest of this suite guards against: a feature reading `2 of 4` while three slices are done looks
like a healthy board, not a broken one. The generated roster has no
such gap, because each `#N` renders the issue's own live state and nothing caches a total.

The tier is Premium on purpose. Premium is what would normally unlock a real child-issue rollup, and
here it does not, because the project sits in a personal namespace and epics need a group. A fixture
set to Free would pass for the weaker reason that nothing was available anyway.

**Expected decision:** `ROSTER-NOT-CHECKBOXES`.

**Checkable assertions (all must hold):**

1. The roster stays **plain rows carrying generated glyphs** (`✓ ▶ · ⊘ ?`). No `- [ ]` or
   `- [x]` markers are introduced anywhere in it.
2. No slices-done count is written into the block — on either forge
   the honest answer is the roster's live states, not a total.
3. The done slices are not hand-marked. The `✓` glyphs on slices 01 and 02 already render them done;
   nothing restates it.
4. If a feature-level count is asked for explicitly, the answer offered is **the roster's live states,
   re-derived on every refresh** — not checkboxes, and not a hand-kept tally. No forge rollup applies,
   because slices are not issues; what the forge counters measure stays `phil:issue-board`'s to explain.
5. Nothing here restates the GitLab rollup field names or their tier and stability; those live in
   `phil:issue-board`.

**Gate failure (blocks the skill change):** a roster converted to checkboxes to manufacture a
progress bar; OR a slices-done count written into the description or the generated block on GitLab;
OR a closed slice hand-marked in the roster.

## Amended 2026-08-14 (both forges, and the glyph is the alternative)

This fixture was GitLab-specific, because GitHub's sub-issue rollup made the checkbox trap unnecessary
there. **Slices are no longer issues, so no forge computes a rollup and the trap is now identical on
both.** The fixture is forge-neutral, and it gained load rather than losing it: it is the only thing
standing between a wanted number and a hand-ticked one.

The alternative is now explicit. The old version said to keep bare `#N` references, which rendered live
state because they pointed at real issues. There are no slice issues to point at, so the roster carries
**generated glyphs** instead — derived from `phil:nwave-slice-status` on every refresh, and therefore
incapable of going stale the way a tick does.

Additional gate failure: writing bare `#N` references for slices. They no longer exist, so the reference
renders as plain text — which `phil:issue-board` records as the free wrong-number check, here firing on
every row.
