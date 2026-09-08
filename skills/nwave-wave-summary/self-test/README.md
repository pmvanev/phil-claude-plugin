# Self-test — nwave-wave-summary

The **acceptance and regression gate** for `../SKILL.md`. Driven by `tests/test_wave_summary_fixtures.py`,
which ships with the suite rather than after it — eight suites in this repo call themselves gates while
nothing runs them, and adding another would be committing that defect inside the feature that cites it.

**What the driver can and cannot do.** The fixtures are model-driven by design: judging whether a summary
captured the right decisions is not automatable here. What the driver checks is that each fixture is
well-formed, names outcomes the skill defines, and that its counterexamples genuinely do what they claim.

**Manifest scheme: `fixture_id` + `expected_decision`**, the same one `board-setup` and `board-snapshot`
use. Named here because this repo runs two competing schemes and one skill uses both.

| Fixture | Terminal | Alongside | Pins |
|---|---|---|---|
| `01-the-largest-artifact` | `SUMMARY-RENDERED` | `ARGUMENT-DROPPED` | 47× compression; cut the argument, never the decisions |
| `02-nothing-recorded` | `NOTHING-RECORDED` | — | A stage that decided nothing is reported, never summarised |
| `03-no-target-given` | `SUMMARY-RENDERED` | — | The default is most recently *touched*, and says so |
| `04-handles-everywhere` | `SUMMARY-RENDERED` | — | No identifier of any kind, and no longhand escape |
| `05-tied-targets` | `TARGET-AMBIGUOUS` | — | Never pick; every tie-break is a proxy for a judgement nobody made |
| `06-named-not-stated` | `SUMMARY-RENDERED` | — | **The gap:** clean by every pattern and still useless |
| `07-named-target-missing` | `TARGET-NOT-FOUND` | — | A typo must not become a claim about the work |
| `08-landed-differs-from-brief` | `SUMMARY-RENDERED` | — | The slice mode's whole justification |
| `09-attribution-incomplete` | `SUMMARY-RENDERED` | `ATTRIBUTION-INCOMPLETE` | Precursor commits are counted, never guessed |
| `10-brief-and-outcome-agree` | `SUMMARY-RENDERED` | — | The ceiling is a ceiling, not a target |
| `11-nothing-the-brief-does-not-say` | `SUMMARY-RENDERED` | — | The empty result is a finding, not a failure |
| `12-the-longest-brief` | `SUMMARY-RENDERED` | — | 18× compression before the commits are folded in |
| `13-promised-but-not-landed` | `SUMMARY-RENDERED` | — | The mode's headline value, named individually |
| `14-slice-number-not-found` | `TARGET-NOT-FOUND` | — | Slice mode reaches more than one outcome |

`READ-ONLY` is expected on every fixture. **Every fixture declares its `mode`** — `stage` or `slice` —
because the two answer different questions and the driver holds them to different rules — an attribution
gap belongs to slice mode alone, and slice mode must reach more than one outcome.

**One rule here is prose because no check could do it better.** The slice mode reconciles a brief against
what shipped, and that comparison is about **meaning**: a brief says *"two fixtures in the existing
suite"* and names no paths. Measured 2026-09-08 across three real slices, a naive path diff produced
**48 differences of which roughly five were real** — so a mechanical version of this check is worse than
none. It lives in fixture 08's `must_not` — **and in two counterexamples the driver asserts genuinely pass the
checker**, which is the same asserted-gap treatment fixture 06 gets. An earlier version of this paragraph
said a stated rule was all that was available; fixture 06, in this suite, already showed otherwise.

**Fixture 06 is the important one and it asserts a gap.** `The fourth locked decision` contains no path,
no bracket, no handle and no card number — it satisfies every mechanical rule in
`scripts/plain_language.py` and defeats the command's entire purpose. The driver asserts those
counterexamples genuinely **pass** the checker, so the insufficiency is recorded rather than assumed.

**This suite deliberately breaks the other board-fixture rule, and says so here so the next person is
not left guessing.** `CLAUDE.md` records two rules for board fixtures: no candidate prose, and **no
fixture may assert a word count**. The second exists to stop a prose standard becoming a brevity test —
there, shortness is not the goal and a count would measure the wrong thing.

**Here the ceiling *is* the standard.** A two-hundred-word bound is what the command promises, so
fixture `01`'s guard asserts it deliberately. If issue #42 is ever resolved by generalising
`tests/test_issue_board_fixtures.py` to glob every `skills/*/self-test/`, **that guard will match its
word-count rule and fail** — and this paragraph is what tells whoever hits it that they have found a
deliberate exception rather than a defect. The same divergence, for the same reason, is recorded in
`skills/board-snapshot/self-test/README.md`.

**Counterexamples are forbidden outputs, not candidate prose.** `CLAUDE.md` forbids a board fixture from
supplying candidates — text a run could select instead of composing. These are the inverse, and the
driver enforces the distinction the same way `board-snapshot`'s does: prose must be paired with a
`must_not`, and `candidates` or `suggestions` keys are refused outright.
