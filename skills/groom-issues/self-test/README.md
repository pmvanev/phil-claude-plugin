# phil:groom-issues — Acceptance Self-Test (slices 01–04)

The **scan and report** is the software under test. Its bugs are silent, and one of them is worse
than the rest: a completeness claim over a partial read looks exactly like a completeness claim over
a whole one. "52 clean" is a statement about issues nobody looked at, and nothing in the output
distinguishes the two.

These fixtures assert the correct **decision outcome**.

Slice 01, the scan — `/phil:groom-issues`:

`REPORT-DEFECT` · `REPORT-CLEAN` · `REPORT-PARTIAL` · `REPORT-UNEVALUATED` · `SURFACE-CANDIDATE` ·
`NOT-A-DEFECT` · `NO-MARKER` · `READ-ONLY`

Slice 02, the apply — `/phil:groom-fix`:

`SCOPE-FIRST` · `APPLY-MECHANICAL` · `LEAVE-SEMANTIC` · `STALE-REREAD` · `REFUSE-GENERATED`

Slice 03, the set-level loop — `/phil:groom-set`:

`ASK-SET-LEVEL` · `APPLY-MERGE` · `APPLY-SPLIT` · `REFUSE-UNVERIFIED` · `DECLINE-NO-TRACE` ·
`REDERIVE-BETWEEN`

Slice 04, the elicitation loop — `/phil:groom-ask`:

`ASK-CONTENT` · `WRITE-ELICITED` · `WRITE-PARTIAL` — reusing `DECLINE-NO-TRACE`, `STALE-REREAD` and
`REFUSE-GENERATED`, which mean the same things they mean elsewhere. `ASK-CONTENT` precedes every
outcome, including the decline and the refusal: a run that wrote a body without it wrote one nobody
sanctioned.

**Both write outcomes are incomplete without provenance** (amended 2026-08-14). Each written field carries
one of `you wrote` · `you accepted my suggestion` · `you edited my suggestion` · `I rephrased your answer`,
and **an unlabelled field fails the outcome regardless of how the body reads**. This replaced the verbatim
rule, and it is stricter: verbatim was silent on the suggestion path, so a session that offered a draft and
got a nod satisfied it while producing a body nobody composed.

**`ASK-SET-LEVEL` precedes every apply in slice 03**, and is encoded that way — fixtures `18`, `19`, `21`
and `22` carry it in the array form alongside their terminal outcome, as `13` does for `LEAVE-SEMANTIC`.
A runner comparing `expected_decision` therefore checks that the ask happened, which is the property
these fixtures exist to guard; a scalar terminal outcome would have let a session skip the question and
still pass. It is the outcome on its own wherever the question is the whole deliverable — `17`, where the
evidence admits four resolutions, and `23`, where the answer is a container this command cannot create.

`20` is the deliberate exception: `REFUSE-UNVERIFIED` stands alone because nothing was asked there. An
unconfirmed candidate is not put to a vote.

**`LEAVE-SEMANTIC` is additive too**, and pairs with `APPLY-MECHANICAL` on the same issue — fixture `13`
pins the case where one card holds one of each, because the column is a property of the defect and not of
the card.

**`REPORT-UNEVALUATED` is additive**, like `REFUSE-DERIVABLE` in `skills/session-handoff/`. A run
reports it *alongside* `REPORT-DEFECT`, `REPORT-CLEAN` or `REPORT-PARTIAL` whenever a check went dark —
a board with defects can also have rules that never ran. Fixture `09` pins the case where it is the
only thing left to say, which is the one most likely to be swallowed by a clean-looking summary.

Format and intent mirror `skills/rank-issues/self-test/` and `skills/session-handoff/self-test/`.
Forge responses are supplied by `manifest.json` so the suite runs unattended.

## What the fixtures pin

| Fixture | Situation | Guard under test | Expected |
|---|---|---|---|
| `01-scan-and-report/` | 7 issues, 2 with body defects (**walking skeleton**) | the oracle produces checkable findings, not taste | `REPORT-DEFECT` — each cites rule + evidence |
| `02-partial-read-no-claim/` | pagination truncates at 100 of ~180 | a completeness claim over a partial read | `REPORT-PARTIAL` — no "N clean", ever |
| `03-clean-board/` | every issue well-formed | manufacturing work to justify the run | `REPORT-CLEAN` — and stop |
| `04-generated-line-not-a-defect/` | a wave-labelled card whose block has no `Work this with:` | generated regions are not body content | `NOT-A-DEFECT` |
| `05-session-scratch-is-a-defect/` | a body carrying session working state | the board is world-readable (ADR-013) | `REPORT-DEFECT` |
| `06-no-marker-anywhere/` | a board previously groomed | a stored marker is a second authority | `NO-MARKER` — re-derive; declined items reappear |
| `07-surface-not-act/` | two issues overlapping in part | set-level ops are slice 03 and ask-first | `SURFACE-CANDIDATE` — evidence, no action |
| `08-read-only/` | defects found and obviously fixable | the slice is read-only | `READ-ONLY` — nothing written |
| `09-unevaluated-is-not-clean/` | whole board read, but rules 3 and 4 have no oracle here | silence from a rule reading as compliance | `REPORT-UNEVALUATED` — name the dark rules |
| `10-one-sided-chain/` | one chain named from one end only, beside a correctly mirrored pair | half a relationship reads as a whole one | `REPORT-DEFECT` — mechanical, on the silent end |
| `11-scope-before-write/` | four defects, all mechanical, nothing scoped yet | the classification read as authorisation | `SCOPE-FIRST` — group by class, write nothing |
| `12-apply-reports-its-reason/` | scoped to one class; a mechanical defect sits outside it | the scope treated as a hint | `APPLY-MECHANICAL` — with per-change reasons |
| `13-semantic-untouched-same-issue/` | one card, one mechanical + one semantic defect | the semantic column becoming contagious | `APPLY-MECHANICAL` + `LEAVE-SEMANTIC` |
| `14-stale-since-scan/` | the body changed between scan and apply | a silent overwrite of prose nobody read | `STALE-REREAD` — say what moved and when |
| `15-generated-region-refused/` | a mechanical fix inside `nwave:status` markers | right content, wrong owner | `REFUSE-GENERATED` — with the generator named |
| `16-population-of-one/` | six checks with oracles, exactly one defect (**measured**) | ceremony over a population of one | `SCOPE-FIRST` — proportionate, passes named |
| `17-partial-overlap-three-outcomes/` | 07's pair, now handed to the set-level loop | a binary question over evidence admitting four answers | `ASK-SET-LEVEL` — every outcome offered |
| `18-merge-survivor-is-a-choice/` | duplicate where the newer card is the better one | the lower number treated as the survivor | `APPLY-MERGE` — user's choice, references re-pointed |
| `19-split-second-pass/` | one card, three seams, split approved | a cross-reference to a number not yet assigned | `APPLY-SPLIT` — create, add to board, then link |
| `20-obe-unverified/` | one card claims another's work shipped; the repo does not | closing a live card on board prose | `REFUSE-UNVERIFIED` — say what would settle it |
| `21-declined-leaves-no-trace/` | the same pair declined for the third run | a decline record, which is a marker renamed | `DECLINE-NO-TRACE` — and say it will reappear |
| `22-rederive-between-candidates/` | candidate 1's merge closes candidate 3's subject | walking a list the run's own applies invalidated | `REDERIVE-BETWEEN` — drop it, and say why |
| `23-ungrouped-effort-container/` | two LaTeX cards, no milestone is that goal (**measured**) | inventing the container, or filing under the nearest | `ASK-SET-LEVEL` — propose, hand over the call, stop |
| `24-wave-family-needs-no-declaration/` | nWave repo declaring nothing, two cards with accumulated wave labels | a normative family going dark for want of a local copy | `REPORT-DEFECT` + `REPORT-UNEVALUATED` — both halves |
| `25-elicit-and-write/` | empty body; the user answers both questions | the session composing instead of transcribing | `WRITE-ELICITED` — each field attributed to its answer |
| `26-elicit-declined/` | the user cannot answer and declines | a helpful placeholder, which is a body nobody dictated | `DECLINE-NO-TRACE` — and say the finding returns |
| `27-elicit-body-moved/` | the body gained two paragraphs since the scan | a refused write that also discards the answers | `STALE-REREAD` — refuse, and hand the answers back |
| `28-partial-answer-stays-partial/` | purpose given, done-condition explicitly not known | completing the body by inference | `WRITE-PARTIAL` — one field, and rule 2 still open |
| `29-no-batch-elicitation/` | five failing cards, four looking interchangeable | one answer written to five cards | `ASK-CONTENT` — one card, and name the queue |
| `30-ask-only-what-is-missing/` | purpose stated, done-condition absent; rule 2 only (**measured**) | asking for a rule that passed, and overwriting prose that satisfies it | `WRITE-ELICITED` — one question, one field |
| `31-elicited-prose-not-in-generated-region/` | the whole body is an `nwave:status` block | placing dictated prose where a generator will overwrite it | `REFUSE-GENERATED` — refuse, and hand the answers back |
| `32-ambiguous-reply-is-unanswered/` | a suggestion is on the table and the reply is "ok" (**measured**) | reading assent as acceptance and writing an unsanctioned body | `ASK-CONTENT` twice — nothing written, say what is needed |
| `33-suggestion-replaced-not-adopted/` | both purpose suggestions are wrong about the direction of the problem | a rejected framing surviving as residue in the card | `WRITE-ELICITED` — `you wrote` + `you edited my suggestion` |

## The sharpest

**`02` is the one that matters most.** Every other failure here produces a wrong item in a list a
human reads and can argue with. This one produces a *right-looking* summary line that is false about
work nobody examined — and the reader has no way to tell. If `02` fails while the rest pass, the tool
is more dangerous than no tool.

**`09` is `02`'s quieter twin, and harder to catch.** Both emit a summary that overstates what was
examined. In `02` the issue count is visibly short, so a reader who checks the numbers can see it. In
`09` every number is honest and complete, and what is missing is which *rules* were awake — invisible
from the output alone. `02` was found by reasoning about pagination; `09` came out of the first real
run, where two rules produced no findings because neither had an oracle on that board.

**`08` and `11` are the same temptation at two distances.** Both present defects that are obviously
correct to fix, and both must refuse. In `08` the refusal is free — the scan holds no write tool, so
failing it means the session tried to acquire one. In `11` the session *has* the tools, the scope is
merely unstated, and nothing but the rule stands between it and four correct edits. A suite containing
only `08` proves the guarantee where it is structural and never tests it where it is a decision.

**`16`, `23`, `30` and `32` are the four fixtures here that are measurements rather than constructions.** `16`'s
numbers came off this repo's real board after slice 01 had been dogfooded twice, and they contradict the
slice brief: the mechanical column held one defect, not a queue, and the maintainer had authored it that
same session. It pins proportionate scoping — but its more important job is to stop a future reader from
designing a bulk fixer for a population that has never been observed to exist.

`23` is the same board a day later, and it landed on the one branch of *ungrouped effort* the slice brief
did not plan for. The brief says *join the existing milestone, or propose creating one* as though they
were two shapes of the same offer. On the real board they are not: eleven of thirteen cards carry a
milestone, the two that do not are the same effort, and **no existing container is that goal** — so the
only honest move is the one this command cannot perform. Keep it measured. Constructing a fixture where a
fitting milestone happens to exist would test the easy branch and hide that the hard one ends in a refusal.

`30` is the third, and it is the one that indicts the suite rather than a brief. Fixtures `25` through
`28` each construct a card with an **empty body** and two findings — so all four pass while the loop asks
two questions regardless of what the scan found, and **nothing in the suite could fail**. The real board
says the population is *partial*: three cards fail rule 2 (#1, #2, #3) and none fail rule 1. Against the
only population ever observed, a two-question loop is wrong every time. Four fixtures agreeing with each
other is not coverage when they share the assumption under test.

`32` is the fourth, and it is a measurement of a *reply* rather than a board. The single word "ok" is what
the maintainer actually typed when the slice-04 dogfood asked its question on 2026-08-14. **On that morning
the reply was merely unanswerable; by the afternoon it was dangerous**, because the scribe→editor amendment
put a suggestion on the table for it to be read as accepting. Nothing else in the suite reaches that shape:
`25` has an explicit accept, `26` an explicit decline, `28` an explicit refusal of one half, `33` an
explicit replacement. An ambiguous reply is the gap between them — and it is the one a real user produced
first, before any of the constructed cases were exercised at all.

**`17` carries slice 03's whole bet, and it is a bet about the question rather than the evidence.** The
slice was written to disprove that set-level defects can be surfaced with actionable evidence, and `07`
had already shown a partial overlap could be *described*. What `17` pins is that describing it is not
enough: a correct finding put behind *merge? y/n* still produces a wrong board, because the right answer —
split along the seam, or a dependency edge — was never on the menu, and the user's **no** is then read as
a fourth position they were never shown. The ask has to have the same arity as the finding.

**`20` is `02`'s failure mode moved from the report into the world.** `02` emits a false claim about
issues nobody read; `20` acts on one. Its evidence is a sentence in another card's body, which is exactly
the stale copy of forge state the defect table already distrusts — so the candidate that reads most
convincingly is sourced from the thing the skill trusts least. Refusing costs one line in one report;
being wrong closes a live card, and nobody notices for months.

**`21` is `06` under pressure.** `06` refuses the marker when nothing wants one. `21` refuses it on the
third run of the same declined pair, where writing one would be a kindness and every user would thank
you for it. A guarantee only tested where it is free is not tested — the same relationship `08` has
to `11`, one slice further along.

**`22` is the only fixture where the session is its own adversary.** Every other staleness case here
involves someone else editing between read and write. This one cannot be avoided by being careful about
other people: the run's first apply invalidates its own remaining candidates, so any run that resolves
more than one candidate from a single scan is wrong by construction.

**`09` and `24` are the same undeclared board with one difference, and it is the whole change.** Both
run against a project whose `CLAUDE.md` declares no label family. In `09` there are no wave labels, so
rule 4 has nothing but project-local pairs to judge and correctly reports only `REPORT-UNEVALUATED`. In
`24` two cards have accumulated wave labels, and rule 4 must fire on those while still going dark on
`documentation` + `enhancement` — **one rule, two authorities, resolved independently in a single run**.
A session that treats the two fixtures alike has either broken `09` by inferring families from the
labels in use, or failed `24` by letting a normative invariant wait for a local copy that no forge
requires.

`24` also inverts `09`'s visibility argument. There, the danger was a clean summary hiding a dark rule.
Here the summary already carries findings, so it *looks* thorough — which makes the missing unevaluated
note harder to spot, not easier.

**`28` is the sharpest fixture in slice 04, and the only one where the refusal is genuinely hard.**
Every other elicitation guard is a refusal the session holds while the right answer is unknown. In `28`
the user has just explained that retries fire on 4xx and should not, so "done when retries no longer
fire on 4xx" writes itself and would be a good criterion. It would also be the session's, and the user
said in as many words that they do not know it yet. A body that is complete and partly invented is
worse than one honestly half-done: the half-done card keeps reporting rule 2 until a human answers it,
and the invented one looks finished and stops asking.

**`29` is where slice 02's own rule points the wrong way.** That slice established that the offer
scales to the population — one finding gets one confirmation rather than a menu — so five findings
would ordinarily justify a batch. The scaling rule does not reach this command, because what scales
there is *consent*: one answer can authorise five identical link rewrites because the fix is derivable
and identical in kind. Here the deliverable is *content*, and five cards have five purposes. A fixture
suite that only inherited slice 02's reasoning would have built the batch.

**`04` and `05` resolve in opposite directions over the same surface.** Both concern content that
appears in an issue body; `05` must flag it and `04` must not. A rule that catches one by a principle
that breaks the other — "flag anything unexpected in a body", or "never flag body content" — is a
gate failure. The distinction is *who owns the text*: a human owns their prose, a generator owns
what is between its markers.

## Running

Drive each fixture by giving the session the situation in `manifest.json` and comparing the decisions
reached against `expected.md`. Model-driven; there is no CI runner in this plugin.
