# Slice 01 — The standard, one asker, one countable fixture (walking skeleton)

**Goal:** Write the standard as a shared fragment, reference it from one real ask site, and prove the
200-word ceiling is countable on a real request.

**Stories:** S1 (answer without spending a turn on what it means) · S2 (get the detail without the wall)
**WS strategy:** C — real local resources (the real `groom-issues` skill, this repo's real board)

## Learning hypothesis

**Disproves [D8] — the shape** — if a referenced fragment does not change how the question actually comes
out. The fragment is read at authoring time, not at ask time; if the ask that ships still opens with a
bare option list, then the standard needs to be closer to the call site than a reference can put it, and
slices 02–04 are all built on a shape that does not work.

**Confirms**, if it passes, that one fragment plus a reference is enough to change output — which is the
premise every later slice inherits, and the premise E6 puts in doubt (`spirit-walk` wrote the rule locally
and it propagated nowhere).

**Second, smaller hypothesis:** that the hardest asker is survivable. `groom-ask` is the repo's only
*elicitation* ask — it asks what an issue is *for* — so it is the worst input a 200-word ceiling will ever
get. If [D4] breaks anywhere it breaks here, and here is where it is cheapest to find out.

## IN scope

- `skills/shared/decision-request.md` — the standard: C1–C8 from the feature delta, with the ask/detail
  split ([D5]) and the placement clause ([D9]).
- A reference to it by name from `skills/groom-issues/SKILL.md` at its ask site, following the
  `test-runner-detection.md` referencing pattern exactly.
- One fixture asserting the word count of a **real** request produced by that site — not a synthetic one.
- A dogfood run against this repo's board, with the version named or the hand-driven path stated, per
  `CLAUDE.md`'s *Which copy is under test*.

## OUT of scope

- The other 7 ask sites and the other 12 command grants — slice 03.
- The bare-list, jargon-wall and buried-ask fixtures — slice 02. This slice pins **only** the count,
  because the count is the one thing that must work before the rest is worth building.
- Any check script. Conformance is checked by eye here; mechanising it is [D10] and slice 03.
- The conversational half — slice 04, and [D11] already declares it out of reach.
- `plugin-dev` consultation is **not** out of scope: the build path requires
  `plugin-dev:skill-development` before the fragment is written, and the commit must say it ran.

## Acceptance criteria

- **AC1** `skills/shared/decision-request.md` exists and states C1–C8, including that the ceiling applies
  to the ask alone and that a buried conforming ask still fails.
- **AC2** `skills/groom-issues/SKILL.md` references it by name at its ask site.
- **AC3** A real ask from that site is ≤200 words, counted mechanically, and the count is recorded in this
  brief's Result section as a number.
- **AC4** That ask states what is being decided and what turns on it before its first option, and contains
  no wave label, issue number, slice id, skill name or artifact path.
- **AC5** The same ask carries a separated detail section that does carry those tokens — proving [D5] is a
  real clause and not an escape hatch nobody uses.
- **AC6** Each option in that ask names its own cost, not only its benefit.
- **AC7** `plugin-dev:skill-development` was consulted before the fragment was written, and the commit
  says so. Per `CLAUDE.md`, a sibling file is not a template.

## Dependencies

None blocking. The groom family is complete and installed.

## Effort · reference class

**≤1 day.** Reference class: `board-setup-block` slice 01 (one script + one skill + one command, one day)
and `live-work-stack` slice 01. This slice is smaller than both — one fragment, one reference, one
fixture, no new command and no new grant.

## Pre-slice SPIKE

**Not needed.** The uncertainty is whether a reference changes output, and that is answered by doing the
slice rather than by probing first — the slice *is* the probe, which is what makes it the skeleton.

---

## Result — 2026-08-21

**Built.** `skills/shared/decision-request.md` (1,096 words) ·
`skills/shared/self-test/decision-request/01-the-ask-that-shipped/` ·
`tests/test_decision_request_fixtures.py` · `tests/test_shared_fragment_registry.py` ·
reference wired into `skills/groom-issues/SKILL.md` · `skills/shared/README.md` corrected.

Full suite: **364 passed, 72 skipped.** `check-invariants.py`, `check-readonly-commands.py` and
`check-product-ssot.py` all clean.

**Build path: `plugin-dev:skill-development` was consulted before the fragment was written** — read
directly rather than invoked, because invoking it fails (issue 23, and `board-setup-block` slice 01
recorded the same workaround). What it changed: no frontmatter (`skills/shared/` deliberately holds no
`SKILL.md`, so frontmatter would read as a registrable skill — now asserted by a test), imperative
verb-first form throughout rather than second person, and lean-body discipline.

### AC status

| AC | Verdict |
|---|---|
| AC1 fragment states C1–C8 | ✓ — and four clauses are now test-asserted, not just present |
| AC2 `groom-issues` references it | ✓ |
| AC3 real ask ≤200 words, counted mechanically | ✓ — **143**, re-derived every run |
| AC4 framing before options, no forbidden tokens | ✓ — zero hits across six categories |
| AC5 the same ask carries a separated detail block | **✗ — NOT MET.** See below |
| AC6 each option names its own cost | ✓ |
| AC7 `plugin-dev` consulted first | ✓ |

### Learning hypothesis — CONFIRMED

A referenced fragment does change the output. The evidence is not the reference itself but what
happened while writing it: the framing emitted for this feature's own DISCUSS elicitation came in at
143 words with zero forbidden tokens, and it was written *because the standard was being written*. The
shape ([D8]) survives.

**The stronger evidence is what the reference displaced.** `groom-issues` already carried a local
ancestor of the standard — *"Present the card before asking… a question that assumes the reader
remembers the card gets a worse answer"*. That paragraph is kept, because it says which context to
restore, which the standard does not. That is the correct relationship between a shared standard and a
local rule, and it was only visible once both existed.

### AC5 failed, and the failure is informative

**The recorded conforming ask carries no detail block at all.** It did not need one: three
simultaneous decisions fit in 143 words, so nothing was displaced downward. The jargon-bearing context
that *was* present — the file-by-file reading checklist — sat **above** the ask, not below it, and it
was establishing context rather than supporting detail.

So [D5] — unbounded separated detail — is **unproven, not disproven**. It remains the clause that makes
[D4] affordable in theory, with no instance demonstrating it. Two consequences:

1. **Slice 02 must include a fixture whose ask genuinely needs a detail block**, or [D5] ships as
   untested prose. Added to slice 02's scope by this result.
2. **The ask/detail ordering is now an open question.** The fragment says detail *"sits below"*. The one
   real instance put its context above and read better for it. The distinction may be
   establishing-context (above) versus supporting-detail (below) — which the fragment does not draw.
   Not amended here: one instance is not enough to change a locked decision, and guessing at the
   distinction is the speculative design this repo's principles forbid. Recorded for slice 02.

### Proof that the checks can fail

`CLAUDE.md`'s standing rule — *"Test that a new check fails on the input that motivated it before
trusting a green run"*, written after `check-readonly-commands.py`'s first version silently passed
because the function was never called. A throwaway fixture `99-proof-of-red` was created, run, and
removed. All three mechanical checks fired:

```
ask is 409 words, ceiling is 200. Over is a failure, not a warning
manifest records 143 words, ask.md has 409
forbidden vocabulary in the ask — {'wave label': ['wave: discuss'], 'issue number': ['#33'],
  'slice id': ['slice 01'], 'decision number': ['[D4]'],
  'skill or command name': ['AskUserQuestion', '/phil:'],
  'artifact path': ['skills/shared/decision-request.md']}
```

The registry check was proven the same way, by corrupting one README row:
`README claims ['edd', 'work'], derived ['groom-issues']`.

### Scope taken beyond the brief, declared

**`skills/shared/README.md`'s loader table was wrong, and so was the fragment's own header.** Found
while copying the referencing pattern this slice is built on:

| Registry | Claimed | Reality |
|---|---|---|
| `README.md` table | `refactor-tests`, `redesign-tests`, `work`, `edd` | `adversarial-review`, `redesign-tests`, `refactor-loop`, `refactor-tests` |
| fragment header | `refactor`, `refactor-loop` | as above |

Three hand-maintained registries, three answers, one truth. Both corrected, and
`tests/test_shared_fragment_registry.py` now **derives** the table and fails on disagreement.

This is scope the brief did not name. Taken because adding a correct row to a table whose other row is
wrong ships a registry that is still a liability, and because the drift is direct evidence for slice
03: a hand-maintained record of who references what is exactly what that slice proposes to mechanise.
Declared here rather than folded in silently.

### Deviation from repo standards, recorded rather than hidden

**`CLAUDE.md` says "Test first. Write a failing test before production code."** Partially honoured. The
reference test (`test_the_fragment_is_actually_referenced`) was genuinely red before the reference was
wired — captured. The fragment's own content tests were written *after* the fragment, and the
ceiling/vocabulary checks passed on first run and were only proven failable retroactively via
`99-proof-of-red`. That is weaker than test-first and is the same shortfall `board-setup-block` slice
01 recorded.

**`plugin-dev:skill-reviewer` and `plugin-dev:plugin-validator` have NOT been run.** `CLAUDE.md` calls
both non-optional over the result. They are agents, and this session is under a standing instruction
not to dispatch agents unless asked. Flagged for the user rather than resolved unilaterally — and
recorded so a later reader does not read this slice as vetted.

### Dogfood claim — scoped honestly

Nothing was exercised through an installed `/phil:*` command. The plugin cache is at an earlier version
than this tree, and per `CLAUDE.md`'s *Which copy is under test* a run against it would exercise the
snapshot, not these edits. **What was exercised is the prose and the tests, in the working tree.** The
143-word ask is a real ask that a real human answered this session, which is stronger evidence than a
command run would have given — but it was emitted by a session following the standard as it was being
written, not by the released `groom-issues`.

---

## Review round — `plugin-dev:skill-reviewer` + `plugin-dev:plugin-validator`, 2026-08-21

Both run at the user's instruction after slice 01 was committed at `f36e603`. Each was given the design
intent up front (that `skills/shared/` holds no `SKILL.md` by design) so neither spent its pass on that,
and both were asked to be adversarial rather than encouraging. **Verdict: needs revision — the fragment
was not fit to propagate.** Every finding below was re-verified against the files before being accepted.

### The reviewer was right about the two decisions the fragment exists to encode

- **[D4]'s ceiling had no defined scope and a self-contradicting remedy.** The fragment said *"Count the
  framing"*, then offered *"cut options"* as the remedy for exceeding it — cutting something the count
  excluded. A third line treated the ask as framing **plus option labels**. Three readers, three counts,
  and the single fixture could not discriminate because its `ask.md` contains no options at all. So the
  143-word figure was a **framing-only** measurement reported against an *ask* ceiling, and slice 01's
  own AC1 (*"the ceiling applies to the ask alone"*) was ticked ✓ against prose that said something
  narrower. **Fixed:** the count now names items 3–5 plus every option label and description, excludes
  the context block, and names `wc -w` semantics. The remedy cuts descriptions → options → the decision
  itself, never the framing.
- **[D5]'s "sits below" was unimplementable against the emission order the same file mandated.** The
  fragment required emitting framing before the blocking `AskUserQuestion` call; anything genuinely below
  the option render arrives *after* the answer, where it cannot be opted into, and anything above the call
  sits between the framing and the options — the buried-ask failure rebuilt from sanctioned parts. Slice
  01's Result had already recorded this as open and the fragment stated it as settled, with no marker, so
  an instance loading it at ask time read a decided rule. **Put to the user and answered: context goes
  ABOVE.** [D5] amended in the feature delta, including the cost the user accepted — context above is
  *bounded in practice, not unbounded*, because length above the ask buries it by another route.

### Findings accepted and fixed

| # | Defect | Fix |
|---|---|---|
| 3 | *"in force deterministically"* claimed compliance where only **delivery** is guaranteed — contradicted by this slice's own test docstrings, which said it correctly first | *Reach* now separates delivery from compliance and names the propagation gap (1 of 6 skills) on its own side |
| 5 | Header claimed the fragment was *"Referenced by name from the skills that hold `AskUserQuestion`"* — 1 of 6. **The exact defect corrected in the sibling fragment hours earlier** | Header no longer names consumers; the README table and derived test own it |
| 6 | *"Ask once more, naming what is still needed"* was **byte-identical** in both files, and the fragment omitted the two-ask cap — so it licensed the nagging loop `groom-issues` explicitly forbids. Duplication with drift, day one, in a feature whose shape was justified by *"no duplication"* | Cap moved into the fragment; consumers may tighten and must say so |
| 7 | The consumer paraphrase was 47 words restating the standard; siblings manage `(reuse).` | Cut to a two-bullet statement of what only this skill knows |
| 8 | Prose permitted *"naming a command the reader is about to run"*; the oracle matches `/phil:` on sight. Prose and oracle contradicted | Exception deleted — prohibition is absolute, matching the oracle. A test now asserts the regex really does what the prose claims |
| 9 | The interruption line was required by one section and forbidden by two others, in a sentence whose requirement read as commentary | Now item 3 of an explicit emission order, and counted |
| 10 | Placement declared failable with **no observable** — [D4] got a counter, [D9] got nothing | A marker line, and nothing between framing and the tool call. Test-asserted |
| 12 | ~290 of 1,096 words were rationale and provenance | Cut the `rules/` provenance paragraph and the meta-commentary |

**Finding 6's residual duplication is accepted, not closed.** The fragment now owns the generic rule and
the cap; `groom-issues`' pre-existing affirmation prose stays. Deleting pre-existing behaviour spec from a
shipped skill is a larger change than this slice should make, and the two no longer disagree. Recorded so
it is a decision rather than an oversight.

**Finding 4 stands as a declared scope leak.** *Reach* is slice 04's deliverable and shipped here. Slice
01's OUT-of-scope names the conversational half as slice 04's, and slice 04's SPIKE — the search for a
mechanism [D6] and [D7] did not rule out — has not run, so the fragment now asserts a conclusion ahead of
the search that could refute it. Reduced to the minimum honest statement rather than pulled entirely,
because a fragment silent on its own reach overclaims by omission. **Slice 04 keeps its SPIKE and AC2/AC6;
its AC1 and AC3 landed early.**

**Two reviewer findings not adopted, with reasons.** Its defence-of-the-kept-paragraph critique was right
that the stated reason was wrong — the standard never said *"restore context"* — and the paragraph is kept
on the corrected reason, now written. Its finding 11 (the fragment coins *mode 1/2/3*, the class of
identifier it forbids) is fixed by naming them instead of numbering them; the failure-mode table survives
because a reader who does not know the three failures cannot apply the ordering rules.

### The validator found two defects, neither in the fragment

- **A live runtime bug in six pre-existing references, exposed by contrast.** `skills/shared/README.md`
  mandates `${CLAUDE_PLUGIN_ROOT}/skills/shared/…` because a bare relative path is left literal in a skill
  body and resolves against **the user's project**, where it does not exist. Four skills and one agent had
  bare paths at six sites — `adversarial-review`, `refactor-tests`, `redesign-tests`, `refactor-loop` (×2),
  `agents/adversarial-reviewer`. The new `decision-request` wiring was the only compliant reference in the
  repo. **All six prefixed.** This means `refactor-loop`, `refactor-tests`, `redesign-tests` and
  `adversarial-review` could not locate a test runner in a consumer's project.
- **The registry test written *this slice* certified a narrower claim than its own docstring.**
  `_loaders()` globbed `skills/*/SKILL.md`, so it could not see `agents/adversarial-reviewer.md` — a real
  consumer — and the row-match passed green while the table under-reported by one. That is this board's
  recurring defect reproduced inside the fix for it, for the second time in one slice. **Derivation widened
  to skills, agents, commands and `references/`; the table's column renamed from *Loaded by* to
  *Consumers (derived)*; and a new test asserts the reference FORM, not just its presence** — the first
  version matched a bare path and an absolute one equally, which is why six broken references passed free.

### Not adopted, referred to the user

The validator reports that in Claude Code 2.1.239 `allowed-tools` **does** interpolate
`${CLAUDE_PLUGIN_ROOT}`, contradicting `CLAUDE.md`'s doctrine that it does not and that such a grant
"matches nothing". It read the shipped binary and caveats that the doctrine may have been true of an
earlier build. **Not acted on.** That doctrine was written after a real incident, `check-readonly-commands.py`
enforces it, and re-measuring is a separate piece of work with its own fixture requirement. Referred rather
than resolved.

### Suite after the revision

**370 passed, 72 skipped** (was 364 — six new assertions). `check-invariants.py`,
`check-readonly-commands.py` and `check-product-ssot.py` all clean. Fragment 1,072 words, down from 1,096
with roughly 290 words of provenance cut and procedure added.
