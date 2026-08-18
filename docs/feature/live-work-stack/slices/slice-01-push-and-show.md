# Slice 01 — Push and show, on the file that already holds the stack (WS)

**Goal:** A diversion can be recorded the moment it happens, and the stack read back at any depth,
without ending the session.

**Stories:** S1 (record a diversion as it happens), S3 (ask where I am)
**Carries:** [D1] the write-authority decision, and the amendment to the overwrite rule it requires.

## Learning hypothesis

**Disproves** [D1]'s single-file, whole-file-regenerate authority if a push cannot rebuild the
snapshot without either losing the `Why`/`Next` payload or needing a carve-out — in which case the
stack has to move to its own file and `/phil:handoff` gains a dependency it does not own.
**Confirms**, if it holds, that the overwrite rule was only ever anti-arbitration, and that the
fixture-19 pattern (whole-block regeneration by the one writer that owns it) transfers from the card
side to the file side unchanged.

## IN scope

- **`/phil:stack push "<what>" "<why>"`** — appends a frame to `## Stack` in `.session-handoff.md`,
  stamped with the current UTC minute, by reading the whole file and writing the whole file back.
- **`/phil:stack`, bare** — renders the trace: each frame's what, why and age, innermost marked.
- **A compare-and-swap guard** (DESIGN DDD-1). `git hash-object` at read, re-hashed immediately before
  write; if it moved, refuse and report both hashes. **No `session:` field** — an authorship check
  would refuse the primary path, since resuming a previous session's snapshot is what the file is for.
- **The overwrite rule, amended in as many words** in `skills/session-handoff/SKILL.md` step 6:
  it forbids merging a snapshot *this session did not write*, not rebuilding one it did. The
  amendment quotes the existing sentence and its stated worktree rationale rather than paraphrasing.
- **Push with no prior snapshot creates one carrying the stack alone.** A diversion is payload, so
  this is not the `NO-OP` case — recorded as [D3] because it amends the NO-OP rule's premise that the
  payload is the why and the next action.
- **`commands/stack.md`** with `mutates: true` and a grant that carries no path or variable, per the
  `adversarial-review` pattern in `CLAUDE.md`.

## OUT scope

- **Pop.** Slice 02. Push and show are end-to-end without it: the frames a session opens are
  consumed at wind-down by `/phil:handoff`, exactly as they are today.
- **Staleness marking.** Slice 02, with pop, because a never-popped frame is only a defect once
  popping exists.
- **Arbitration between two live sessions.** Detected and refused, never resolved — inherited
  verbatim from `session-handoff` slice 03. More likely with a session-stamped header, and still out.
- **Any change to `/phil:handoff`'s projection.** It reads the same file it always wrote. Stating
  this as OUT rather than silently not doing it: "no work needed" is a finding.
- **A hook that pushes automatically.** The reason is the payload and no hook can see it — the same
  ground on which ADR-014 deferred the `Stop` hook.

## Acceptance criteria

1. `/phil:stack push "deploy script" "blocked the blocker"` on a snapshot carrying a `Why` and a
   `Next` leaves both **byte-identical** and the stack one frame deeper. This is the slice's sharpest
   assertion and needs its own fixture.
2. Bare `/phil:stack` at depth 3 renders all three frames, each with what it is, why it was pushed,
   and how long it has been open, innermost marked.
3. A push against a snapshot that **changed between read and write** refuses, reports both hashes,
   and writes nothing. A fixture asserts no merge and no retry is attempted. Resuming a *previous*
   session's snapshot and pushing to it is the normal path and must succeed.
4. A push with no snapshot on disk creates one whose `## Stack` is populated and whose `Why` and
   `Next` are absent rather than invented.
5. Bare `/phil:stack` with no snapshot renders `unknown`; with a snapshot but no `## Stack` renders
   `none`. The two are distinct, per the rule already shipped for the projection.
6. `scripts/check-readonly-commands.py` passes on `commands/stack.md`, and its `Bash(...)` grant
   contains no slash and no `${...}`.

## Dependencies

`.session-handoff.md`, its delimited header and the `## Stack` format all exist (slice 04 of
`single-issue-per-feature`). Nothing blocks this.

## Effort

~1 day. The read-modify-write is small; AC1 and AC3 are the fixtures that must not be waved through,
and the `core.autocrlf` question against `git hash-object` (DESIGN open question 2) needs its own
fixture before this slice closes.

Reference class: `session-handoff` slices 01-03, and `single-issue-per-feature` slice 04, which
shipped the stack format itself at roughly this size.

## Result — 2026-08-18

**Authored; not yet exercised.** `push` and `show` landed with five fixtures. No run has produced a
frame, so ACs 1-6 are unverified and **KPI-1 is not measured** — the same standing this feature was
raised to correct in slice 04, and it stays open until a real diversion is pushed and popped.

### What landed

1. **`commands/stack.md`** — `mutates: true`; `Bash(git rev-parse:*)`, `Bash(git status:*)`,
   `Bash(git hash-object:*)`, `Bash(date:*)`. No path and no variable in any grant.
2. **`## Writing the snapshot`** in `skills/session-handoff/SKILL.md` — the compare-and-swap, shared by
   all three paths, with the header rule below.
3. **`## STACK`** — `push` and `show`. `pop` is a stub naming slice 02 rather than a gap.
4. **Fixtures 16-20**, the register, `acceptance.feature`'s five scenarios, and the outcome vocabulary
   in `tests/test_session_handoff_fixtures.py`.

### The scope violation, and what it cost

**Slice 01 shipped slice 02's work and I did not notice.** `pop`, the staleness rule and the
`nwave-issue-board` cross-reference — all three named in the OUT scope above, all three written anyway.
`plugin-dev:plugin-validator` found it; my own fixture 18 had recorded the truth in its
`expected_guard` (`"slice-01 AC2 + slice-02 AC3/AC4"`) while the register called the same fixture slice
01. **The evidence of the violation was inside the artifact that committed it.**

Reverted on decision, 2026-08-18. Worth recording because of *how* it happened: `push`, `show` and `pop`
are one prose section, and writing two of three verbs felt like leaving a sentence unfinished. A slice
boundary that cuts through a paragraph is one the author will close without deciding to.

### The two defects both reviewers found independently

**The header.** `push` regenerates the whole file, and nothing said the delimited header was CAPTURE's.
A whole-file regeneration run by something holding a live tree and a `git rev-parse` grant re-stamps
`commit:` — after which it always matches `HEAD` and **`RESUME-STALE` can never fire again**. The worst
outcome this skill can produce, reached through a routine mid-session note. Now stated in *Writing the
snapshot*, in the never-do list, and asserted in fixtures 16 and 20.

**Fixture 18 passed on impossible input.** It supplied `captures_since_frame_N` as manifest data — a
field the real snapshot cannot carry, because the header holds one `captured:` overwritten at every
capture. So *whether* a frame outlived a capture is derivable and *how many* is not, and the fixture was
defending a behaviour neither it nor any implementation could produce. This is `CLAUDE.md`'s recurring
defect exactly: **test that a new check fails on the input that motivated it.** Rebuilt to take only a
snapshot; the count question goes to slice 02 with the staleness rule.

### Also corrected

- Frames at depth ≥2 stamped a bare `HH:MMZ`. Fine while the stack was only displayed; `show` subtracts
  from it now, and a frame open across a handoff has likely crossed midnight. Full `YYYY-MM-DDTHH:MMZ`
  on every frame — and the canonical example, inherited from slice 04, did not follow its own stated
  format and now does.
- A push with no snapshot had no defined header. `captured: never`, with `commit:`/`dirty:` stamped —
  fixture 20, the AC4 coverage that was missing.
- `/phil:stack` was absent from `README.md`. The list is now 26/26 against `commands/`; **no gate in this
  repo checks it**, and this is the first occurrence, so no check was added — see the note below.
- Two never-do lists, neither a subset of the other. Merged into the global one.
- `3b.`/`3c.` were not CommonMark ordered-list markers and had been silently breaking the CAPTURE list
  into three since slice 04. Renumbered 1-10.
- The skill description named two commands and carried no trigger phrases; `acceptance.feature` claimed
  to be the scenario SSOT while holding nothing about the stack, and asserted "every other outcome is
  live" over a list missing six.

### Not done

- **`plugin-dev:command-development` still could not be consulted** — issue #23, third recurrence. The
  cause on the card was wrong and is now corrected there: the loader executes `` !`cmd` `` **inside
  fenced code blocks**, so the skill documenting the syntax cannot load. Read off disk with `sed` instead.
- **Progressive disclosure deferred.** 5,656 words against a <5,000 guideline. `skill-reviewer`'s
  recommendation — split by *kind* (procedure vs. justification), never by path, since nothing loads a
  fraction of a `SKILL.md` — is sound and is slice 02's opening move, before it adds more.
- **A README-vs-`commands/` check is a candidate for `scripts/check-invariants.py`.** Not added:
  `CLAUDE.md` says add one when a defect is found twice, and this is once.

## Carpaccio taste tests

| Test | Result |
|---|---|
| Ships 4+ new components? | No — one new command, one new section in an existing skill, one new header field. |
| Depends on a new abstraction? | No. The file, the format and the delimiters exist; this adds operations over them. |
| Disproves a pre-commitment? | Yes — [D1]. If whole-file regeneration cannot preserve the payload, the authority moves to a second file. |
| Synthetic data only? | No. The dogfood is a real diversion in this repo, which is the KPI that slice 04 could not measure. |
| Duplicate of another slice at scale? | No. Slice 02 is pop and staleness — different operation, different failure mode. |
