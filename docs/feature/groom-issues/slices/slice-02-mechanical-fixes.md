# Slice 02 — Mechanical fixes within a scope

Feature: groom-issues · Job: `keep-a-backlog-trustworthy` · Persona: `robin-backlog-curator`

## Goal

After the report, let the user pick a scope, and fix inside it only the defects that need no
judgement.

## Learning hypothesis

**Disproves that any fix is safe unasked.** If every defect the report classifies as "mechanical"
turns out to need a question once it is about to be applied, then the mechanical/semantic boundary is
empty, grooming is entirely conversational, and this slice collapses into slice 03.

**Confirms** that the boundary is real and worth drawing — that a link which would 404, an
accumulated single-valued label, or a missing cross-link can be corrected without consulting anyone.

## IN scope

- **Scoping**: the user picks a defect class, a subset of issues, or everything. The tool does not
  choose and does not start fixing to demonstrate progress.
- **The mechanical set**, applied inside that scope: relative links that 404 on GitHub, accumulated
  single-valued labels, missing bare cross-references, and similar corrections with one right answer.
- **Per-change reporting**: what changed on which issue, and why it needed no judgement.
- **Re-read before write** — if an issue changed since the scan, report it rather than overwrite.

## OUT scope

- Anything that changes the *set* of cards — merge, split, close, group. Slice 03, all ask-first.
- Anything requiring a judgement about meaning: missing acceptance criteria, unclear purpose, wrong
  granularity. These are reported, never fixed here.
- Writing inside a generated region (C3).

## Acceptance criteria

1. Given the defect table, when scoping runs, then the user selects the scope and nothing is written
   before that selection.
2. Given an agreed scope, when fixes are applied, then only defects classified mechanical are touched,
   and each change is reported with its justification.
3. Given a defect requiring judgement, then it is left alone and listed as needing a decision.
4. Given an issue modified since the scan, then the session re-reads it and reports the change rather
   than overwriting silently.
5. Given a fix that would edit inside a `nwave:status` block, then it is refused with the reason.

**Production data:** this repo's real board, with its real relative-link and label state.

## Dogfood moment

Same day: fix the mechanical defects slice 01 found on this board, and confirm by re-running slice 01
that they are gone and nothing else changed.

## Dependencies

**Slice 01** — consumes its defect table and its classification of mechanical vs semantic.

## Effort and reference class

≤1 day. Reference class: `phil:refactor-tests` — a scoped, per-item apply loop over a backlog the
previous step produced.

## Carpaccio taste tests

| Test | Result |
|---|---|
| Ships 4+ new components? | No — a scoping step and an apply loop in the existing skill. |
| Depends on a new abstraction? | Consumes slice 01's; introduces none. |
| Disproves a pre-commitment? | Yes — that a mechanical/semantic boundary exists at all. |
| Synthetic data only? | No. |
| Duplicate of another slice at scale? | No — 03 is ask-first by definition; this is ask-never by definition. |
