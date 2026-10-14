# Feature and story states

Part of the `nwave-slice-status` skill. Read it whole before emitting a feature-level or story-level state. Its `SKILL.md` governs this file too.

## The feature-level state, on request

A count is not a state. `5 of 9 done` says how much is finished; it does not say what the feature *is*,
which is what a caller placing it in a board column needs. **Emit a feature-level state only when asked
for one** — by the `--feature-state` flag, or by a question that plainly asks for one (*"what state is
this feature in"*, *"which column does this card belong in"*) — and derive it by this fold, in this order,
because the order is the content:

| Test, applied in order | State |
|---|---|
| The roster is empty — no slice files and no roadmap phases | `unknown` |
| The current slice is `blocked` | `blocked` |
| Every slice that is not `deferred` is `done` | `done` — note any deferred slices |
| Any slice is `done` or `current` | `in progress` |
| Every slice is `deferred` | `deferred` |
| Any slice is `unknown`, and none is `done` or `current` | `unknown` |
| Otherwise — every slice `not started` or `next` | `to do` |

**Order matters most at the `in progress` row.** A feature with five of six slices `done` and the
sixth `not started` folds to `in progress`; reading only the current slice gives `to do`, reporting
nearly-finished work as untouched.

**`unknown` sits below `done`/`current` deliberately.** A feature with three slices done and one
unrecorded is in progress, not unknown; the unrecorded slice is a `Notes` entry, not a verdict on the
feature. But where nothing is known, `unknown` is the answer and **never `to do`** — the cardinal rule of
this skill applied to the fold.

**The empty-roster row is the one place `unknown` outranks everything**, because every universal below
it is vacuously true over an empty roster. A feature never decomposed would otherwise fold to `done`;
`phil:nwave-issue-board` maps `done` to the Done column, and on a board with auto-close the card closes.
An empty roster is a fact about the record, not about the work.

**Render the state as one line, with the count beside it** — `Feature: <id> — <state> · N of M slices
done · current slice NN` — because a state and a count answer different questions and a caller placing a
card needs both. **The empty roster is the one case that carries no count:** `0 of 0 done` reads as
completion, which is the same lie arithmetically. Say what is missing there and name the command that
fixes it.

This state is a derivation, so it belongs here rather than in whatever publishes it. Two derivations over
the same files drift apart, and a publisher that folds locally is inventing a status while claiming to
delegate one. `phil:nwave-issue-board` consumes this and renders it; it does not compute it.

## The story-level state, on request

A **story** is several nWave features worked as one piece by one owner, carried on one card. Emit a
story-level state only when asked — by `--story-state <slug>`, or by a question that plainly asks for
one (*"what state is this story in"*). `phil:nwave-issue-board` renders this value; it must never
compute it.

**Build the roster from the features' own declarations.** Scan `docs/feature/*/feature-delta.md` for
`Story: <slug> · position NN` — **anchored at column 0, in the file's header region, at most one per
file**. The story's roster is every feature declaring that slug, in `position` order.

**The anchor is load-bearing.** A feature delta may discuss the convention as well as use it, so an
unanchored match finds decoys that parse as conflicting declarations, and `**Story:**` appears in
slice briefs for an unrelated concept. **A file matching twice at column 0 is a defect** — name both
and do not pick.

- **A feature with no `Story:` line is in no story.** That is the normal case and never an error.
- **A missing `position` sorts last**, and Notes says the order was not declared.
- **A position collision is named in Notes, never resolved.** Two features claiming position 02 is a
  fact about the record; picking one invents an order the artifacts do not contain.
- **Nothing here reads a forge.** Membership lives in `docs/feature/`, so this derivation stays a pure
  read of artifacts — which is what lets the publisher stay a renderer.

**The fold is the feature fold with features substituted for slices. It is not a second table, and
must never become one** — two tables over the same seven tests drift, and preventing that drift is why
this skill owns both folds. Apply *The feature-level state, on request* with exactly these
substitutions:

| In the feature fold, read | As |
|---|---|
| "slice" | "feature" |
| a slice's status (seven values, `SKILL.md` Step 3) | a feature's state, from the feature fold itself (six values) |
| `current` | `in progress` |
| `not started` | `to do` — the feature fold returns `to do`, never `not started`; without this row the final test's condition is unmatchable |
| `next` | **absent** — the feature vocabulary has no such value, so no test can match it |
| the roster is empty (no slice files, no roadmap phases) | **no feature declares this slug** — the guard row does not survive a literal substitution, and it is the row that matters most |

Each member's state therefore comes from running the feature fold over that feature's own roster. A
story fold is M feature folds and one application of the same table.

**Render as one line, with the count beside it:**

```
Story: <slug> — <state> · N of M features done · current feature <id>
Notes: <one short clause per defect, one per line; omitted entirely when the sources agree>
```

**`current feature` is the first member, in `position` order, whose state is not `done`.** Omit it
entirely when every member is `done`.

**Where the position order is contested, the ordinal does not resolve — say so in its place:**

```
Story: <slug> — <state> · N of M features done · current feature contested — position NN claimed by <a> and <b>
```

The state is quantified over members, not over their order, so a collision cannot change it. What a
collision *does* change is `current feature`, the field a reader acts on when asking what to work on
next. Emitting a winner there — by directory name, by mtime, by discovery order — invents the one fact
the artifacts do not contain, and the result is indistinguishable from a story whose positions were
declared correctly. Report the state, withhold the ordinal.

**The guard matters more here, and it must be tested on its conjunction.** The empty-roster row exists
because every universal below it is vacuously true over an empty set, so an unguarded fold answers
`done`, `phil:nwave-issue-board` maps `done` to Done, and auto-close turns the rendering into a closed
issue. One level up, that closed card holds **N features**. Two emptinesses are distinct and resolve
differently:

- **No feature declares the slug** — the roster is empty. `unknown`, **no count**, and say the slug
  matched nothing. Guard row.
- **Features declare the slug but every one folds to `unknown`** — the roster is populated. `unknown`
  **with a count**, from the existential row, and Notes names the unreadable members.

A guard weakened to one clause stays green on the other, which is why both are pinned.

**A story is never `next`, and never inherits a slice's status directly.** Reading a member's *slice*
status where its *feature* state is required crosses two vocabularies and produces a value the six-state
table cannot render.
