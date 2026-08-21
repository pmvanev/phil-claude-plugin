# Slice 04 — The reach outside a command

**Goal:** Address the case the enforceable half cannot reach — a decision request in ordinary
conversation — and declare plainly what mechanism covers it and how well.

**Stories:** S5 (know where the standard cannot reach)
**WS strategy:** n/a — slice 01 holds the skeleton

## Learning hypothesis

**Disproves [D11] — that the conversational half is unenforceable** — if it turns out to be reachable
after all. That would be good news and is recorded as a hypothesis precisely so it gets tested rather than
assumed: [D11] was reasoned from two measurements ([D6] on `rules/`, E2/E6 on per-command prose) and a
third mechanism may exist that neither ruled out. A `SessionStart` hook, a skill description that fires
reliably, or something in the harness that nobody here has checked.

**Confirms**, if it holds, that the standard covers the command case deterministically and the
conversational case probabilistically — and that the difference is stated in the artifact rather than
discovered by a user whose question arrived as a bare list anyway.

**The honest failure mode of this slice is silence.** Shipping a probabilistic mechanism and describing it
as coverage is worse than shipping nothing, because it converts a known gap into an invisible one.

## IN scope

- A section in `skills/shared/decision-request.md` stating that outside a `/phil:*` command no
  deterministic trigger exists, naming what is used instead and how it fails.
- Whichever mechanism is chosen — the two candidates, not exclusive:
  - a **skill description** that triggers on the moment: reaches ordinary conversation, ships to
    consumers, fires unreliably;
  - a line in **`CLAUDE.md`**: always loaded, fires reliably, repo-local, does **not** ship to consumers.
- The choice recorded with its cost, and the split stated if both are used.
- KPI-6 restated in the fragment as unmeasurable by construction, so a later reader does not mistake its
  absence for an oversight.

## OUT of scope

- Putting the standard in `rules/`. Closed by [D6] on measurement: a globbed rule fires on file type
  (`ux.md` is the worked example), and a pathless rule is a manual-reference rule that never auto-loads
  (`rules/llm-inference.md` states this in as many words, naming `definitions.md` as precedent). A future
  reader wanting to reopen it should read E5 and E7 first.
- Any claim of coverage the chosen mechanism cannot deliver.
- Fabricating a number for KPI-6.

## Acceptance criteria

- **AC1** The fragment states plainly that the conversational case has no deterministic trigger.
- **AC2** The chosen mechanism is named, with its failure mode, in the fragment itself — not only in this
  brief.
- **AC3** `CLAUDE.md`'s repo-local reach and its non-shipping to consumers are stated explicitly wherever
  that route is used. A standard that silently depends on a file consumers never receive would report
  coverage it does not have.
- **AC4** No coverage claim exceeds the mechanism ([D11]).
- **AC5** If a deterministic mechanism **is** found, [D11] is amended in the feature delta and this slice's
  hypothesis is recorded as disproved — a reversal recorded as a reversal, per this repo's standing habit
  of naming which decision moved.
- **AC6** KPI-6 is restated as unmeasurable by construction, with the reason.

## Dependencies

**Slice 03** — the mechanism chosen here should be informed by what enforcement actually caught, and
choosing before that is measured would be the speculative design the repo's own principles forbid.

## Effort · reference class

**≤1 day**, and likely half of one — the deliverable is prose plus one small mechanism. Reference class:
`board-setup-block` slice 04 (a taxonomy and its labels, prose-dominant).

## Pre-slice SPIKE

**Yes — timeboxed to an hour, before the slice.** The one open question is whether a third mechanism
exists that [D6] and [D7] did not rule out. That is a *search*, not a build, and doing it as a spike keeps
a negative result cheap: if nothing is found, [D11] stands unchanged and the slice ships the declaration.
