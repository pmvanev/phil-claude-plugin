# Expected — 28 (the ceiling clips the why, and only the why)

**Pins:** issue #43. The 300-word bound on a read-back, and the rule that decides *which* half yields.

**Expected decision:** `RESUME-CURRENT` + `BOARD-AGREES` + `ROUTE` + `REPORT-CLIPPED`.

## What must appear

Everything mandatory, in the emitted order the skill fixes — verdict, board outcome, stack, content,
owner:

- the freshness verdict, naming the matching commit and the clean tree;
- `BOARD-AGREES`, naming the card, because a detector silent on agreement cannot be told from one that
  never fires;
- **all three stack frames**, each with its age, its `crossed` **where non-zero** — the innermost frame
  is at `crossed 0` and prints none, per step 5b, which carries this path's copy of the rule — and
  `⚠ stale` on the outermost frame at `crossed 2`;
- the recorded next action;
- the owner route, `/nw-execute`, named and not run;
- `REPORT-CLIPPED`, **with a count taken against the whole recorded population** — of the form *four of
  eleven recorded items shown; three decisions and four ruled-out approaches withheld* — and a pointer
  to `.session-handoff.md` as their home. The exact split is not pinned; the *basis* of the count is.

**The budget, measured rather than assumed.** The mandatory content costs 105 words — a 10-word current
verdict, a 15-word agreement line, 59 words of frames, a 12-word next action, a 9-word route — leaving
195 for a why that runs 520. **This fixture's first draft asserted "room for about two decisions" and
was wrong**: at the 16-word average of the skill's own worked example, all eleven items would have
fitted and nothing would have been clipped at all. Fixture 29 was corrected for the same class of error
on the same day. A ceiling fixture whose arithmetic does not force the clip is not testing the ceiling.

## Gate failures

- **Any mandatory item withheld to fit.** A dropped frame is the worst of these: the frame is why the
  stack exists, and a diversion nobody prints is a diversion nobody remembers.
- **`REPORT-CLIPPED` without the count**, or a count against what was printed rather than what was
  recorded. *Five withheld* out of seven and out of thirty are different instructions to the reader.
- **Clipping in silence.** A read-back that prints two decisions and reports only `RESUME-CURRENT` has
  asserted it carried the why.
- **Editing the snapshot.** The record is uncounted. A run that shortens the file to shorten its output
  has destroyed the one thing a fresh session cannot derive, which inverts the skill.
- **Reporting `CEILING-BREACHED` too.** The mandatory content fits here; clipping did real work, so the
  two outcomes cannot both hold.
- **Dropping the ruled-out approaches without saying so** while printing decisions. Both are the why,
  and the discarded alternatives are the half the next session re-proposes when it never learns they
  existed.

**Why this fixture is not a brevity test.** The withheld decisions are still on disk, one file read
away. That asymmetry is the whole licence for a word bound on this path — and it is why the same bound
may never reach the snapshot, the frames, or the verdict.
