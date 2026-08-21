# Slice 03 — Every asker conforms, and a script says so

**Goal:** Reference the fragment from all remaining ask sites, and make a command that grants
`AskUserQuestion` without the reference fail the build.

**Stories:** S4 (trust that every asker conforms, without reading nineteen files)
**WS strategy:** n/a — slice 01 holds the skeleton

## Learning hypothesis

**Disproves [D10] — enforcement by script** — if conformance turns out not to be mechanically checkable.
The check can verify that a *reference exists*; it cannot verify that an ask *conforms*. If the reachable
check is so shallow that a referencing skill can still emit a bare option list and pass, then [D10]
delivers a green run that means nothing, and the honest outcome is to say so rather than to ship a check
that certifies the wrong property. This is the exact failure `CLAUDE.md` records for
`check-readonly-commands.py`: *"absence of `Write` never meant read-only"* — a shallow signal standing in
for the real one.

**Confirms**, if it passes, that the standard is in force inside a command as a fact rather than a hope —
the half of the feature that is enforceable at all.

## IN scope

- References added at the remaining **7** ask sites across 5 skills: `refactor-tests` (2),
  `redesign-tests` (2), `work`, `refactor`, `edd`.
- `scripts/check-decision-request-reference.py` — fails on a command granting `AskUserQuestion` whose
  loaded skill carries no reference to the fragment.
- Wiring into `scripts/check-invariants.py`, reporting **only** failures per *Repo invariants run
  themselves*.
- An explicit exemption mechanism, and it must be explicit — a command that legitimately needs no
  reference declares it. Silence is never conformance.
- A stated account, in the script's own header, of what the check verifies and what it does **not**: it
  verifies a reference resolves, never that an ask conforms.

## OUT of scope

- Any attempt to check ask *content* mechanically. The check is a reference check and says so; the content
  is pinned by slice 02's fixtures and by review. Conflating them is the [D10] failure this slice exists to
  test for.
- The conversational half — slice 04. A command grant is the only signal this check can read, so ordinary
  conversation is structurally invisible to it, by construction rather than by omission.
- Rewording the 7 sites' existing prompts. The reference lands; the rewording follows from it and is
  reviewed per-site, not batched blind.

## Acceptance criteria

- **AC1** The check fails on a command granting `AskUserQuestion` whose skill carries no reference.
- **AC2** **The check is proven to fail on the input that motivated it before any green run is trusted.**
  Non-negotiable: `CLAUDE.md` records that the first `check-readonly-commands.py` was written and never
  called, and silently passed — this board's recurring defect reproduced inside the fix for it.
- **AC3** All 8 skill ask sites reference the fragment; all 13 command grants are covered by a referencing
  skill or an explicit exemption.
- **AC4** The check reports only failures and is silent on a clean tree.
- **AC5** An exemption is expressible, explicit, and carries a reason in the file that claims it.
- **AC6** The script's header states the gap between what it checks and what the standard requires, in as
  many words. A check whose limits are undocumented is the shallow-signal failure again.
- **AC7** No `Bash(...)` grant introduced by this slice contains a path or a variable — `allowed-tools`
  does not interpolate `${CLAUDE_PLUGIN_ROOT}`, and such a grant matches nothing while looking narrow.

## Dependencies

**Slice 01** (the fragment must exist to reference) and **slice 02** (the fixtures are what the reference
is worth referencing — a reference to an untested standard propagates confidence, not conformance).

## Effort · reference class

**≤1 day.** Reference class: `scripts/check-readonly-commands.py` (one script, one invariant wiring, one
day — including the day lost to the uncalled function, which AC2 exists to prevent repeating).

## Pre-slice SPIKE

**Not needed.** The mechanism is a grep over frontmatter and skill bodies; the uncertainty is about what
the check *means*, not whether it can be written, and AC6 answers that in prose rather than by probe.
