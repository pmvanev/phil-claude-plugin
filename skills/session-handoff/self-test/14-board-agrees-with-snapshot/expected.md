# Expected outcome — fixture 14 (the two records agree, and the check says so)

**This fixture exists so the check cannot pass by never firing.** A divergence detector that reports
nothing on the agreeing case is indistinguishable from one that is broken, mis-wired, or reading an
empty board — and `CLAUDE.md` names that exact shape as this board's recurring defect: *"A check
nobody runs reports compliance by staying quiet."* Fixture `13` proves the check can fire. This one
proves it fires on **both** branches.

**Pins:** issue #24 done-when — *"A self-test fixture covers the divergent case, and one covers
agreement, so the check cannot pass by never firing."*

## Expected decision

1. **`RESUME-CURRENT`** — commit matches and the dirty flag matches (dirty at capture, dirty now), so
   the standing caveat applies: the fingerprint records only *that* the tree was dirty, not what was
   in it.
2. **`BOARD-AGREES`** — stated positively and briefly, naming the card it agreed with:

```
BOARD-AGREES — snapshot Next and the board's in-flight card (#24, In Progress) name the same work.
```

One line is enough. The agreeing case must be **visible**, not verbose.

## The second thing this fixture pins

`#24` is In Progress while `#29` sits at the top of Todo. A check written literally against the card's
done-when — *"the board's top Todo card"* — compares the snapshot against **#29** and reports a false
divergence on a session doing exactly the right thing.

So the board's claim about what is in flight is: **the In Progress card where one exists, and the top
Todo card otherwise.** Fixture `13` exercises the second branch (nothing In Progress → top Todo);
this one exercises the first.

That is a deliberate widening of the card's literal wording, made because the literal wording is wrong
on the case the card's own title describes — *a divergence about what is in flight*. It costs nothing
where `In Progress` goes unused, which
[`slice-03-claimed-card-link.md`](https://github.com/pmvanev/phil-claude-plugin/blob/main/docs/feature/session-handoff/slices/slice-03-claimed-card-link.md)
§ *Verdict* finding 1 observed on 2026-08-13: the branch simply never fires and the behaviour is
identical to the literal reading.

## Gate failure (blocks the skill change)

- **nothing is reported** because the two agree. Silence here is the whole defect; the reader cannot
  tell agreement from a check that did not run.
- `#29` is compared instead of `#24`, producing `BOARD-DIVERGES` on a correctly-claimed card. A
  detector that cries wolf on the normal path gets ignored on the abnormal one.
- the agreement is reported as a paragraph of reassurance. It is one line.
- the board is written to.

## Read this fixture against `13`

They must not be satisfied by one rule that gets either wrong by getting the other right — the same
property `03` and `05` already hold for derivable state. A spine that always reports `BOARD-AGREES`
passes `14` and fails `13`; one that always reports `BOARD-DIVERGES` passes `13` and fails `14`. Only
an actual comparison passes both.
