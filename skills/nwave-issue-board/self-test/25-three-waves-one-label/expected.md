# Expected outcome — fixture 25 (three waves, one label)

**Pins:** *"on a story card the label is the current feature's wave — still exactly one, still swapped
never added."*

**Expected:** the card carries **`wave: design`** and nothing else. The routing line reads
`Work this with: /nw-design · feature chat-in-web-ui`. `wave: discuss` — correct while position 02 was
itself in DISCUSS, stale now that it has advanced to DESIGN — is **removed in the same call** that adds
`wave: design`.

**Why the current feature and not some aggregate.** A story has no wave of its own; its members do. The
label exists so a reader can act, and the only member whose wave is actionable is the one being worked.
An aggregate would name a wave nobody is in.

**Why not `wave: mixed`.** It names no command, so the routing line dies with it, and it conceals which
member is moving — the single fact the label carries. Rejected in the delta, not revisited here.

**Why not four labels.** That is the measured failure the single-valued rule exists to prevent: a feature
walked DISCUSS→DELIVER accumulates four wave labels and the record becomes unreadable **while every
command reports success**. A story card makes it worse, not better — four members × four waves.

**It also breaks something outside this skill.** `phil:groom-issues` rule 4 reads a normative
single-valued declaration for `wave: *` in every nWave repo. Multi-valuing here would require changing
that declaration, and **if the story tier needed that, the story tier would be wrong.** The declaration
is untouched by this fixture, and that is part of the assertion.

**Position 04 has no wave and that is not an error.** Only the current feature's wave reaches the label.
A member without one contributes nothing and is not backfilled from a neighbour.

**Gate failures:**

- Two or more `wave:` labels on the card. The defect, stated.
- Adding `wave: design` without removing `wave: discuss`. On GitHub nothing enforces exclusion, so the
  card silently carries both and reports success.
- `wave: mixed`, or any synthesised value not naming a real wave.
- Taking the wave from position 01 (furthest along) or 04 (least far). Neither is being worked.
- Emitting a bare `Work this with: /nw-design` with no feature qualifier. This fixture and `26` pin the
  qualified form positively; `27` pins the case where no line is emitted at all.
- Changing `groom-issues` rule 4's declaration to accommodate this card.
