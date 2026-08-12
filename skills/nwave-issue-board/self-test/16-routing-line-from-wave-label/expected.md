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
