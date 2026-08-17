# Slice 02 — Coexist with prose the probe cannot regenerate

**Goal:** Insert the region into a `CLAUDE.md` whose `## Issue board` section is already full of
hand-written prose, without disturbing a byte of it — and report what the probe now confirms,
contradicts, or cannot evaluate.

**Stories:** S2 (add generated constants to a repo whose block is already hand-written)

## Learning hypothesis

**Disproves the delimited-region model** ([D4]) if the region cannot be placed without either
duplicating facts the prose already states, or orphaning prose that then reads as contradicting the
generated lines beside it. If placement forces a choice between duplication and contradiction, the
model is wrong and the whole-section-with-provenance alternative has to be reconsidered.

**Confirms**, if it passes, that a generated region can live inside a hand-written file — which is what
separates this feature from every other generated block in the plugin, where nothing human belongs.

**Dogfood target: this repo.** Its block is the hardest available case — mostly hazards recorded after
contact, none of it reproducible by any probe, and several lines stating facts the region will now own.

## IN scope

- Read and classify the existing file: no section · section without markers · region current · region stale.
- Insert the region into an existing section without wrapping, moving, reordering or reformatting any
  existing line.
- A drift report over the content **outside** the markers, in three buckets: **confirms** (the prose
  agrees with the probe), **contradicts** (it disagrees), **cannot evaluate** (nothing probed bears on it).
- The **retire offer**: for a contradicting line stating a fact the region now owns, offer to remove it —
  applied only on an explicit answer, declined silently leaves no trace.
- Refusals: malformed markers (`begin` without `end`, or nested); file changed between read and write.

## OUT of scope

- Rewriting or reflowing any hand-written line. The only permitted change outside the markers is
  deleting one whole line, on an explicit answer.
- Migrating this repo's block wholesale — #32 puts that out of scope and this slice honours it.
- Elicitation (slice 03) and assumption labels (slice 04).

## Acceptance criteria

1. Content outside the markers is **byte-identical** before and after, on every path including failure
   and including the refusal paths — verified with `git diff` restricted to those line ranges.
2. A contradicting hand-written line is reported and **not edited**.
3. The retire offer applies only on an explicit answer; silence writes nothing and records nothing.
4. `begin` without `end` refuses with the file unchanged. The region's extent is never guessed.
5. Placement is deterministic: two runs against the same file put the region in the same place.

## Outcome — authored 2026-08-17

| AC | Verdict | Evidence |
|---|---|---|
| 1 | **PASS** | `test_placing_into_a_prose_section_leaves_every_other_byte_identical` plus a run against this repo's real `CLAUDE.md`: 13,724 bytes outside the markers before, 13,724 after excision, byte-identical. `write_region` re-checks it before anything reaches disk, so a placer bug is refused rather than committed. |
| 2 | **PASS** | `test_drift_edits_nothing`; contradiction wins the line outright (`test_drift_never_reports_a_line_in_two_buckets`), so a line with one right id and one wrong one is not also filed as agreement. |
| 3 | **PASS by construction** | `retire_line` is a separate explicit call requiring its own `--expect-sha`; there is no code path from a drift report to a deletion. Two refusals tested: a line inside the markers, and out of range. |
| 4 | **PASS** | Three malformed shapes refused — `begin` without `end`, nested `begin`, `end` before `begin` — each with the file unchanged. The extent is never inferred. |
| 5 | **PASS** | `test_placement_is_deterministic`; the position derives from the heading's line number and nothing else. |

### Learning hypothesis — CONFIRMED

**The delimited-region model survives its hardest available case.** Against this repo's real
section — 52 content lines, mostly hazards recorded after contact, none of it reproducible by any
probe — placement forced neither duplication nor contradiction:

```
confirms 7 · contradicts 0 · cannot evaluate 45
```

Zero contradictions is the result that matters. The region can state the ids while the prose keeps
the hazards, and the two do not disagree, so [D4] is not refuted and the whole-section-with-
provenance alternative does not need reconsidering.

**The 45 cannot-evaluates are the finding, not the shortfall.** The hazards in a mature board
section are exactly the things no forge records — which is *why* each had to be written by hand
after something went wrong. A high cannot-evaluate count is what a correct report over a valuable
section looks like, and fixture 07 exists to stop a later run from apologising for it.

### Two defects the dogfood found that the tests had not

Both made the report look **better** than it was, which is the failure mode this feature keeps
reproducing on itself.

1. **A short probed scalar was treated as evidence.** The project number `3` and an option count
   `4` substring-matched into nineteen "confirms", one resting entirely on a line containing the
   digit 2. Fixed with a six-character minimum; pinned by
   `test_a_short_scalar_is_not_evidence_of_anything`.
2. **Fact values were walked one level deep.** `column-families` nests its option ids as a list of
   dicts, so the line stating all four option ids — the constant whose full-replacement hazard
   nearly destatused 25 cards — reported as `cannot evaluate`. Fixed with a recursive flatten;
   pinned by `test_option_ids_nested_inside_a_fact_are_evidence`.

Neither was reachable from the unit tests as first written, and neither would have been visible in
the finished file. **The dogfood is what found them**, which is the argument for WS strategy C
holding for slice 02 as it did for 01.

### The placement cost, accepted and recorded

The `end` marker sits directly above the first hand-written line, with no blank line between them,
because a blank line is a byte outside the markers that was not there before. AC1 is strict and
readability outside the markers is not this command's to spend. Anyone who finds the rendering
tight should change AC1 deliberately rather than adding the line.

**`git diff` reports one deleted line, and it is not a violation.** Placing into this repo's real
`CLAUDE.md` produced `40 insertions, 1 deletion` — the deletion is the blank line that followed the
`## Issue board` heading. It was not removed: its newline is now the terminator of the `end` marker
line, which is exactly the mechanism that makes excision restore the original. The authoritative
check is byte-level and it passes — 13,724 bytes at `HEAD`, 13,724 after excising the region,
identical.

Recorded because the line-level diff is what a reviewer actually looks at, and `1 deletion` on a
file of unreproducible hazards is alarming until you know why. A future run that reports **any
deletion other than that single blank line** is a real AC1 failure.

### The review round — `plugin-dev:skill-reviewer` + `plugin-validator`, 2026-08-17

Both ran against the authored slice. The validator returned **PASS with findings**; the skill
reviewer returned **Needs Improvement**, and was explicit that length was not the reason — four
correctness defects were. Every finding below is fixed, and each one that a fixture could have
caught now has one.

**The two that mattered most were self-contradictions, not omissions:**

1. **The skill said "exactly one outcome" while its own fixture 01 expected two.**
   `REPORTED-NOT-WRITTEN` was simultaneously an outcome and defined as something that *accompanies*
   one. Worse, fixtures 03/06/07 run against the same board — same two `half_probed` workflow
   entries — and expected it not at all. Same input, three reported shapes. Fixed by demoting it to
   a **report line** beside `DRIFT`, adding `expected_report_lines` to every manifest, and pinning
   the rule in `tests/test_board_setup_fixtures.py`. *A rule contradicted by the fixture that tests
   it is worse than no rule, because each looks like authority for the other.*
2. **The command's intent prose said it "runs exactly one program, the probe script, and that script
   only reads."** After this slice it runs two, and the second writes. That paragraph is the
   *compensating control* for the over-wide `Bash(python3:*)` grant — the one place the boundary the
   frontmatter cannot express is written down — so it was the worst possible sentence to leave
   stale. It now names both scripts and says which writes what, under which flags.

**Also fixed:** an unhandled `FileNotFoundError` on the skill's own documented create-if-absent path
(now a `file-absent` state with tests, because the alternative left the model no route but hand
placement, which the skill forbids); the flow materialising `PROBE.json` and `REGION.md` with
nowhere specified, defaulting them into the target repo and contradicting the *one file changes*
contract; three `###` sections mis-nested under `## The region`; two second-person leaks; a
malformed-marker enumeration listing three shapes where `classify()` returns four; and a description
advertising a trigger the skill stops on.

**Three grants removed.** `Bash(git remote:*)`, `Bash(git rev-parse:*)` and `Bash(git ls-tree:*)`
were unused — the scripts reach `git` through list-argv `subprocess`, inside the `python3` grant —
and the prose called all three read-only when `git remote` has `add`, `remove`, `set-url` and
`rename`. The repo's own allowlist already omits `git remote` for that reason; only `mutates: true`
stopped the check firing.

**Two findings went to route 2 rather than into this skill**, because they change what the repo
does rather than what `board-setup` asserts:

- `check-readonly-commands.py` reported *"204 `Bash(...)` grants verified matchable"* while counting
  every grant of every kind; the real figure was 43. Fixed, and now **40** after the three removals.
  An auditor reading 204 would infer fivefold the coverage that exists, and *a number nobody can
  reconcile is how a check stops being read*.
- That checker had **no tests** — the one script in `scripts/` without them, and the one whose first
  version `CLAUDE.md` records as silently passing. `tests/test_check_readonly_commands.py` now
  exercises it on the exact input that motivated it.

**On the length finding.** `SKILL.md` went 3,335 → 2,936 words, with the rationale moved to three
`references/` files and `self-test/README.md`, and every runtime-consulted rule kept in place. It is
still above the 1,500–2,000 target and that is a deliberate stop: the reviewer noted no skill in
this repo has ever met it, board-setup is the 4th largest of 23, and splitting further would set a
convention rather than correct a deviation. The discriminator applied was **does the model consult
this while executing a step** — if yes it stayed.

### Test-first, unlike slice 01

`tests/test_region_place.py` was written before `scripts/region-place.py` existed and was run RED
first. Slice 01 recorded a deviation from `CLAUDE.md`'s test-first rule on the grounds that the
probe's shape was unknowable until the live forge answered; nothing in local text manipulation
inherits that excuse, so the exemption was not carried over.

## Dependencies

Slice 01 (the probe).

## Effort · reference class

≤1 day. Reference class: `groom-issues` slice 02 — mechanical changes inside an agreed boundary, each
reported with the reason it needed no judgement.

## Taste tests

| Test | Result |
|---|---|
| Ships 4+ new components? | No — a reader, a placer, a drift report |
| Depends on a new abstraction? | Reuses slice 01's probe |
| Disproves a pre-commitment? | Yes — [D4], the second-largest untested commitment |
| Synthetic data? | No — this repo's real `CLAUDE.md` |
| Identical to another slice but for scale? | No — differs from 01 by the presence of prose, not by size |
