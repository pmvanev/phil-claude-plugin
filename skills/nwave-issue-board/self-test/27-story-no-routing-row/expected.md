# Expected outcome — fixture 27 (no row, no line — at the story tier, and it says why)

**Pins:** the **no-label** branch at the story tier — the one shipped routing rule whose justification
does *not* transfer — and *"no line ever names a command for the story."*

**Which branch fires, precisely.** Neither member is in a wave the table knows, so the card carries **no
wave label**, and the rule that fires is *no label, no line* — not *no row, no line*. At the feature tier
that branch licenses **silence**, because a card outside a wave may simply not be nWave work. **A story
card is nWave work by definition, so that licence cannot apply**, and the story tier therefore requires
the statement the feature tier does not. That is a real change to the rule at this tier, and it is the
reason this fixture exists rather than being covered by the shipped one.

**Expected:** **no `Work this with:` line**, and in its place a statement that the routing table covers
the seven nWave waves and has no row for this repo's authoring path. No wave label either, since neither
member is in a wave the table knows.

**The rule is exercised, not re-derived, and that distinction is the fixture.** A story tier that
restated the rule in its own words would have two copies to drift; instead the three shipped rules apply
unchanged and only the *feature qualifier* is new. This fixture proves the shipped rule reaches the new
tier — which is the cheaper and more durable outcome.

**Saying why is the whole value.** An omitted line and a forgotten line look identical. On a story card
the stakes rise: a reader seeing no routing line on the board's largest card is more likely to conclude
the card is malformed than that the table is narrow.

**The routing table does not cover the build path of the repo that owns it.** True at the feature tier
since 2026-08-14, and now true of that repo's only story. It is not an edge case here; it is the normal
case.

**A bare command would be worse than nothing.** With no feature qualifier, `Work this with: /nw-discuss`
on a two-feature card asserts the command owns the story. It does not — no wave command does — and a
reader who runs it operates over a scope it was never written for.

**Gate failures:**

- Emitting any `Work this with:` line. No row means no line.
- Emitting the line with a feature qualifier anyway. The qualifier fixes *which* feature, not *whether*
  there is a command.
- Omitting the line silently, with no statement. Indistinguishable from a generation failure.
- Inventing a routing row for `plugin-dev`. The table covers nWave waves; extending it is not this
  block's call.
- Inferring a wave label from the members' completed DISCUSS. Past a wave is not in it.
- Naming a command for the story rather than a feature.
