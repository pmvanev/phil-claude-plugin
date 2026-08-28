# Evolution — decision-request-standard (`skills/shared/decision-request.md`)

Shipped 2026-08-26, 0.65.0 → 0.72.0. All four slices.
Board: [#33](https://github.com/pmvanev/phil-claude-plugin/issues/33), one card, no slice cards.

## Feature summary

A standard for the moment a command stops and needs a call only the human can make. It governs what a
decision request must contain, what it must not, and where it sits relative to surrounding output —
delivered as a shared fragment referenced by every asking skill, enforced by a build check inside a
command and by a tool-call hook everywhere else.

Three failure modes were reported and all three are now pinned by fixtures: **a bare list** (options
render, framing absent), **a jargon wall** (the reader decodes the question before answering it), and
**a buried ask** (correct wording, no signal — a placement defect, not a wording one).

## Business context (JTBD)

Job `answer-a-tools-question-without-decoding-it`, persona `ari-interrupted-decider` — both new, and
the persona is defined by a **position** rather than a domain: someone holding a question without the
asker's context. That is why it is a new persona and not a facet of an existing one; every existing
persona becomes this one at their own ask sites, so attaching it to any single one would imply the
other seven never hit it. The opposite call to `board-setup-block`'s, and recorded as such.

The push force was a typed workaround: *"explain in 200 words of plain English, using no jargon or
labels, what is needed from me"*, entered by hand most times a decision came up. That prompt was the
specification. That it worked is the evidence the missing artifact was small; that it had to be retyped
every time is the defect.

## The design axis

**Where a standard can be made to fire.** Four candidate homes, three killed by measurement rather than
argument:

| Shape | Verdict | Why |
|---|---|---|
| A rule with a `paths:` glob | dead | fires on the file being touched; a decision request happens whatever file is open. `rules/ux.md`'s own no-jargon line is structurally dark for a terminal question |
| A rule with no `paths:` | dead | not an always-on rule — a *manual-reference* rule that fires only if something already decided to consult it. `rules/llm-inference.md` says so in as many words |
| Per-command prose | dead | already tried: `skills/spirit-walk/SKILL.md` invented this exact rule locally, propagated nowhere — and its command grants no question tool at all. Thirteen commands that could ask had no instructions |
| **A shared fragment** | **chosen** | `test-runner-detection.md` is the exact precedent: one fragment, five consumers, no duplication. Inside a command the reference is deterministic |

## Key decisions

- **[D4] 200 words is a hard ceiling — and its *scope* was wrong for two slices.** As first shipped the
  count spanned the framing plus every option, summed. No real request can meet that: the three this
  standard was written from measure **564, 324 and 441**, and the prescribed remedy (cut option text)
  deletes the cost statements the same file mandates. Repaired to **two limits of 200** — the framing,
  and each question with its own options, never summed. Calibrated against 134 real questions: 128
  already fit.
- **[D5] Supporting context is separated, ABOVE the ask, and bounded in practice.** "Below" was
  unimplementable: the question tool blocks, so anything after it arrives once the answer is given.
  "Unbounded" was an overclaim — length above the ask buries the framing by another route. Both struck.
- **[D9] Placement is part of the standard, not only wording.** Nearly a sentence rather than a clause:
  it survived only because a real ask was found that fails on placement **and nothing else**.
- **[D10] Enforcement by script — and its disproof condition was literally met.** A referencing skill
  can still emit a bare option list and pass. It ships because the shallowness is *stated*, three times,
  with tests that fail if those sentences are deleted. A shallow signal is acceptable when its
  shallowness is stated and dangerous when it is not.
- **[D11] The conversational half is unenforceable — DISPROVED.** The premise was reasoned from two
  measurements, both still true, and neither had anything to say about a **tool-call hook**. A tool call
  is not untagged prose; it is structured data. Two clauses are now enforced in flight, everywhere.

## Work completed

| Slice | Shipped | What it learned |
|---|---|---|
| 01 | the fragment + one real asker + one countable fixture | the shape holds; the ceiling had no instance behind its escape hatch |
| 02 | six fixtures, four checks, the emission format | **[D4] refuted then repaired**; [D9] survived on one decisive fixture |
| 03 | 10 skills wired, a build check in two directions | [D10] holds on stated shallowness; found a live dead ask |
| 04 | a `PreToolUse` hook, opt-in split | **[D11] disproved** — delivery outside a command is deterministic |

## Verification

- Test suite **370 → 482**. Four check families over six fixtures, every one mutation-proven failable;
  a 19-row mutation register in `skills/shared/self-test/decision-request/README.md`.
- **Every fixture is a verbatim recording** of a real decision request, extracted from session logs with
  its source named so anyone can re-extract it. A synthetic ask is written by whoever is also writing the
  standard, so it demonstrates intent rather than testing it. Only the *oracle's* own edge cases — a
  framing over 200 words, a region after the call — use hand-built inputs, and they are labelled
  synthetic.
- New checks: `scripts/check-decision-request-reference.py`, `scripts/check-tests.py`,
  `hooks/decision-request/check-ask.py`.

## Permanent artifacts

`skills/shared/decision-request.md` · `skills/shared/self-test/decision-request/` (six fixtures +
register) · `hooks/decision-request/check-ask.py` + its `hooks/hooks.json` registration ·
`scripts/check-decision-request-reference.py` · `scripts/check-tests.py` ·
`tests/test_decision_request_fixtures.py`, `tests/test_decision_request_hook.py`,
`tests/test_check_decision_request_reference.py` · persona `ari-interrupted-decider` · job
`answer-a-tools-question-without-decoding-it` · journey `decision-request-standard.yaml`

## Lessons learned

**Three defects were found only because a reviewer read the work, and mutation testing had reported
twelve of twelve.** The first mutation pass covered the checks that existed; it could not invent inputs
nobody had written. A corpus of well-formed recordings cannot produce a malformed frame, so the
interposed-text rule, the region-order rule and the preview exclusion were all written and never
exercised. Both halves were needed and only review found that out.

**A measurement can refute a decision's scope without refuting the decision.** [D4] looked dead — every
real instance failed it — and the honest-looking move was to demote it to a target. The same
measurement showed both halves were consistently sized and only their *sum* impossible. This board has
the mirror lesson recorded from 2026-08-14 (refuting a decision's rationale does not refute the
decision); this is the other direction.

**The feature reproduced its own defect twice, in its own files.** Slice 02 shipped *"no check reads a
live ask, and none can"* — an impossibility claim a reviewer had already softened once on the grounds
the evidence did not support it. Slice 04 refuted it outright, hours later. The correction then landed
in two of the four files carrying the claim and missed the other two, and the suite stayed green because
nothing asserted them. A feature about statements that mislead on first read, leaving misleading
statements behind. Now swept by `test_no_artifact_still_claims_a_live_ask_cannot_be_checked`, which is
case-folded — the first version was not, and a capitalised reintroduction sailed through it.

**Enforcement that ships to strangers needs its own measurement.** The enforcement question was answered
"refuse on both reachable rules". Measured afterwards, that refuses **81%** of this repo's recorded
requests — genuinely, not by misfiring. Right here, where a filename is internal jargon; wrong in a
project where `config.json` is the plainest way to name the decision. The ceiling ships unconditional
and the wording rule is opt-in, declared as a deviation rather than discovered by whoever gets denied.

**Nothing ran the test suite.** No CI exists in this repository, and `SessionStart` wired two checks, so
every check written as a test — including all twelve this feature added — reported compliance by staying
quiet. Found while building a feature about exactly that failure shape.

## Deferred / follow-ups

- **No repaired instance for `06-over-the-ceiling`.** The standard claims trimming closes a 266-word
  question without losing a cost statement. Real and unpinned; pinning it needs a *constructed* ask,
  against this fixture set's recordings-only discipline.
- **The mutation register is hand-maintained.** A new check without a row is a check nobody has proven
  can fail. Deriving it needs a mutation harness.
- **Compliance in ordinary conversation is still not deterministic.** Delivery is. Two clauses are
  enforced; option costs are semantic and placement never enters the payload, so both stay unreachable
  by any mechanism, not merely by this one.
- **The hook has never fired in a live session.** It ships inside the plugin, and the installed copy is
  behind this tree. Its first real exercise is the next `/plugin` update.

## Scope / accepted limitations

Rewording individual commands' existing prompts was out of scope — the reference lands, the rewording
follows per-site. `rules/` was closed by measurement rather than left open. Issue #34's 200-word board
snapshot shares the bounded-output idea and nothing else: different persona, different job, different
mechanism — related, not merged.
