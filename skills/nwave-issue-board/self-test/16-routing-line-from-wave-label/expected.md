# Expected outcome — fixture 16 (the routing line comes from the wave label, or not at all)

A card describes work, and an agent handed a work description does the work — inline, skipping the
wave command that owns it. The `Work this with:` line is what stops that, and it is only trustworthy
if it is *derived* rather than typed.

**Pins:** the routing-line rule, and its two boundaries.

**Expected outcome:**

- **Card 41** — parent carries `wave: deliver`, so the generated block reads:

  ```
  Wave: DELIVER · generated <ts>
  Work this with: /nw-deliver for the wave; /nw-execute for a single step
  ```

  The line sits directly under `Wave:`, inside the markers, so it is regenerated with the block and
  cannot drift from the label it came from.

- **Card 42** — no wave label, so **no routing line is emitted**. Not `Work this with: unknown`, not
  a guess at the most likely command, not an omission quietly filled from the card's text.

**Gate failures (any one blocks the skill change):**

- A routing line on card 42. Most cards on a mixed board are not nWave work, and a confident wrong
  owner is worse than none — it sends the reader to a command that will not know what to do with it.
- A routing line typed into the description rather than generated into the block. It then survives a
  wave change that should have rewritten it, which is the drift the delimited block exists to prevent.
- A line that *launches* rather than names. This line tells a reader which command owns the work;
  nothing in this skill runs anything.

## Amended 2026-08-14 — the wave with no row

This fixture pins two branches: a labelled card gets its `Work this with:` line, and an unlabelled one gets
none rather than a guess. **A third branch exists and had no coverage.**

A repo may carry a wave label the routing table does not cover, because the table maps the seven nWave waves
and this repo's build path leaves them — DISCUSS runs, then prose is authored with `plugin-dev`. So a
post-DISCUSS feature has a *legitimate* wave and no owning command.

**Third expected branch:** emit **no line**, and **state that the table does not cover this build path.**
Additional gate failures:

- Guessing a command. `/nw-design` is the next wave in the table and is exactly wrong here.
- Emitting nothing at all, silently. Indistinguishable from the no-label case, and a reader cannot tell
  whether the line was withheld by rule or forgotten.
- Citing `plugin-dev` as though it were a wave command. It is a skill consulted while authoring, not an
  entry point that owns the work.

The finding behind this branch: **the routing table does not cover the build path of the repo that owns it.**
