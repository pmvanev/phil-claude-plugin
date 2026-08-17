# Driving the board-setup self-test fixtures

Twelve fixtures, model-driven rather than automated. There is no CI runner in this plugin, so
`tests/test_self_test_fixtures.py` does not collect these: drive each one by giving the
`board-setup` skill the situation in its `manifest.json` and comparing the decision reached against
its `expected.md`. Do that whenever `SKILL.md` or `commands/board-setup.md` changes.

## The two halves of acceptance, automated to different degrees

**The scripts are tested.** `tests/test_probe_board.py` covers the refusal paths, `project` scope
detection, and both ambiguity directions — including AC4, which is otherwise unverifiable without
stripping the operator's live `gh` scope. `tests/test_region_place.py` covers slice 02's guarantee:
byte-identity outside the markers on every path, deterministic placement, all five classification
states, all four malformed-marker shapes, the sha guard, the three drift buckets, the create-if-
absent path, and the retire offer's refusals.

**Those tests were written before the script.** Slice 01 recorded a test-after deviation whose
stated reason was that the probe's shape could not be known until the live forge answered. Nothing
in local text manipulation inherits that excuse, so slice 02 did not carry it over.

**The prose is model-driven.** That is what this directory is for.

## What each manifest key means

| Key | Means |
|---|---|
| `expected_decision` | the **one** terminal outcome. Never more than one |
| `expected_report_lines` | `DRIFT`, `UNEVALUATED` and `REPORTED-NOT-WRITTEN` — each accompanies a terminal outcome and never stands alone |
| `expected_guard` | the property that must hold, stated so a passing-but-wrong run is visible |
| `must_not` | the specific wrong answers, usually the tempting ones |
| `supersedes` | present when a fixture's expectation was deliberately changed by a later slice |

`expected_decision` and `expected_report_lines` are separate because conflating them is a defect
this suite already caught: fixture 01 listed `REPORTED-NOT-WRITTEN` alongside `WROTE` while
`SKILL.md` said "exactly one", and three later fixtures running against the same board omitted it
entirely. Same input, three different reported shapes.

## AC3 splits across the two halves, and the split is the point

**Detecting** ambiguity is tested — `--list-targets` over a real two-remote checkout returns
`ambiguous` with both candidates. **Asking** is prose, and stays unverified until the command runs
as a command. Detection was moved out of prose for exactly the reason the probe is a script: a
property code holds beats one a model is asked to honour.

No fixture covers `AMBIGUOUS-TARGET`, so one of eight terminal outcomes has no fixture. That is
disclosed rather than missed — reproducing it needs a session rooted in a two-remote checkout,
because `--list-targets` reads `git remote -v` from the session's working directory.

`docs/feature/board-setup-block/slices/slice-01-probe-and-write.md` holds the criteria and the
KPI-1 reading; `slice-02-coexist-with-prose.md` holds slice 02's AC verdicts and its dogfood result.

**Every failure mode here is silent.** A block with a remembered id looks exactly like a probed one,
a partial block looks more complete than a refusal, and a drift report that judged nothing looks
like one that found nothing wrong.
