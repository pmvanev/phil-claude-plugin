# Slice 01 — Scan and report (WALKING SKELETON, read-only)

Feature: groom-issues · Job: `keep-a-backlog-trustworthy` · Persona: `robin-backlog-curator`

## Goal

Read a whole board in one call and report what is wrong with it, changing nothing.

## Learning hypothesis

**Disproves that a defect oracle can be stated at all.** If the report reads as taste rather than
checkable findings — if a reasonable person disagrees with half the defects — then the house-default
body standard (D7) is insufficient, and slices 02 and 03 are building on nothing. Everything
downstream depends on this being answerable.

**Confirms** that the gap #5 names first is closeable: `phil:issue-board` says how to manipulate an
issue but never what a body must contain, and this slice is the answer to that.

Read-only, so a failed bet costs only the reading.

## IN scope

- **The house-default body standard** — what a well-formed issue contains, stated explicitly and
  overridable per project in `CLAUDE.md`. This is the deliverable that makes the rest checkable.
- **One-call scan per forge**: `gh issue list --json …` / `glab issue list -O json`. Verified to
  return bodies, labels and milestone in a single call on both.
- **The defect table**, derived fresh every run against that standard — never read from or written
  to a marker (D6/C1).
- **Set-level candidates surfaced but not acted on**: duplicates, oversized cards, work overcome by
  events, ungrouped effort — each with the evidence behind it.
- **A clean board reported clean** (C5).

## OUT scope

- Any write to any issue. This slice mutates nothing.
- Scoping and fixing → slice 02. Set-level operations → slice 03.
- Ranking; status derivation; anything inside a generated block.

## Acceptance criteria

1. Given a board, when the session runs, then every issue is fetched in **one call per forge** and
   the count of issues read is reported.
2. Given the scan, when the defect table is produced, then each finding names the standard it
   violates and quotes the evidence.
3. Given a board with no defects, then it is reported clean and nothing is proposed.
4. Given a **partial** read (pagination failed, forge unreachable), then the session says the read
   was partial and **does not** report "N clean" (C4).
5. Given a body containing session scratch, then it is flagged as a defect (ADR-013).
6. Given a card whose `nwave:status` block lacks a routing line, then it is **not** reported as a
   body defect — that region is generated.
7. Given the session completes, then **no issue was modified** — verifiable by comparing the board
   before and after.

**Production data:** run against this repo's real board and, if reachable, the self-hosted GitLab
project already used for verification.

## Dogfood moment

Same day: run it on this board. The board was ranked but never groomed by tool, so whatever it
reports is the first honest measure of how well the standard holds.

## Dependencies

None. Ships the standard and the scan that slices 02 and 03 both consume.

## Effort and reference class

≤1 day. Reference class: `phil:nwave-slice-status` — a read-only skill that reads artifacts, derives
a table, and writes nothing. Closest analogue in the plugin.

## Carpaccio taste tests

| Test | Result |
|---|---|
| Ships 4+ new components? | No — one skill, one thin command loader, one standard. |
| Depends on a new abstraction? | It *is* the abstraction (the body standard), shipped first. |
| Disproves a pre-commitment? | Yes — that a defect oracle can be stated rather than felt. |
| Synthetic data only? | No — the real board. |
| Duplicate of another slice at scale? | No. |
