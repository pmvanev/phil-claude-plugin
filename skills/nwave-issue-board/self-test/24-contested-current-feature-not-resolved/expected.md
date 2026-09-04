# Expected outcome — fixture 24 (a contested current feature enumerates nothing)

**Pins:** *"Where the owner returns a contested or absent current feature, render that and enumerate
nothing."*

**Expected:** the four-row feature roster in full, then, in place of the current-feature heading:

```
Current feature: contested — position 02 claimed by chat-in-web-ui and saved-sessions. No slice roster.
```

**No slice roster.** Four rows, not ten.

**Why this is the recurring defect in its newest costume.** `phil:nwave-slice-status` deliberately
refuses to resolve a position collision — its own fixture 18 pins that refusal, on the grounds that
tie-breaking by directory name, mtime or discovery order invents the one fact the artifacts do not
contain. The story block is structured around a *single* current feature whose slices get expanded. So a
renderer that wants a slice roster must **choose a contender**, and that choice is precisely the
derivation the owner withheld — performed by the publisher, in the skill whose documented recurring
defect is deriving what it had just delegated away.

**The structural pressure is what makes this dangerous.** Nothing here looks like folding a state. It
looks like filling in a template: the heading takes a feature id, so the renderer supplies one. The
defect arrives disguised as completeness, which is why it needs a fixture rather than a caution.

**An absent slice roster is the honest rendering of an unresolved order.** The reader learns the story's
state, every member and its state, and that the order is contested — everything the artifacts actually
contain. What they do not get is a fabricated answer to *what do I work on next*, which is the field the
collision genuinely destroys.

**Same shape when every member is `done`.** The owner omits the current feature entirely; the heading
becomes `Current feature: none — every member is done.` and again no slice roster is rendered. A
renderer that expands the last member "because it was most recent" has invented a current feature for a
finished story.

**Gate failures:**

- Expanding either contender's slices. The defect, stated.
- Expanding the alphabetically or positionally first member. Same defect with a rule attached; the rule
  is one the artifacts do not license.
- Dropping the contested statement and rendering only the roster. The reader cannot tell an unresolved
  order from a story whose current feature simply was not rendered.
- Emitting an empty `Current feature NN — slices:` heading with no table under it. A heading promising a
  table that is absent reads as a rendering failure, not as a deliberate refusal.
- Writing a board column different from the story state because the order is contested. The state is
  quantified over members, not their order; the collision does not change it.
- Resolving the collision by editing the artifacts. The forge is a projection; nothing here writes to
  `docs/feature/`.
