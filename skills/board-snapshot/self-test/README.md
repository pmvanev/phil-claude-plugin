# Self-test — board-snapshot

The **acceptance and regression gate** for `../SKILL.md`. Run it whenever that file, the command loader,
or `phil:issue-board`'s items-query sections change.

**Driven by `tests/test_board_snapshot_fixtures.py`, which runs in the repo suite.** That driver exists
from the first commit rather than being deferred: issue #42 records eight suites in this repo whose
READMEs call themselves gates while nothing runs them, and 131 fixtures sitting behind none. A suite that
describes itself as authoritative and never fires is a false negative the whole board trusts.

**What the driver can and cannot do.** The fixtures are model-driven by design — judging whether a run
rendered the right snapshot is not automatable here, and the driver does not pretend otherwise. What it
checks is that each fixture is still well-formed and still names outcomes the skill actually defines.
That is the honest half, and the pattern is `tests/test_board_setup_fixtures.py`.

**Manifest scheme: `fixture_id` + `expected_decision`.** Issue #42 records that this repo runs two
competing schemes and that one skill uses both. This suite picks one deliberately and names it here, so a
future driver author meets the choice rather than inferring it.

**Two fixtures are sized to breach the ceiling and they have opposite answers.** `01` is the ordinary
clip — the mandatory sections fit and the queued section gives ground. `13` is the collision — the
mandatory sections alone exceed the ceiling, so the queued section empties *and* the ceiling yields,
because dropping a blocked card is the worse failure. The driver checks each is sized for its own case,
which is what fixture 01's prose got wrong before it was corrected.

| Fixture | Terminal | Alongside | Pins |
|---|---|---|---|
| `01-ceiling-breached` | `SNAPSHOT-CLIPPED` | — | The ceiling, on a board large enough to breach it |
| `02-two-empty-sections` | `SNAPSHOT-RENDERED` | — | One sentence for empty sections; board order consumed |
| `03-blocker-unrecorded` | `SNAPSHOT-RENDERED` | — | "Unrecorded" is an answer; nothing is inferred |
| `04-open-card-in-done` | `SNAPSHOT-RENDERED` | `DRIFT` | Free detection, reported and never fixed |
| `05-page-dropped` | `SNAPSHOT-PARTIAL` | — | Partial supersedes clipped; no completeness claim |
| `06-slice-cards-inflate` | `SNAPSHOT-RENDERED` | `INFLATION` | Report, never consolidate, never refuse |
| `07-card-with-no-status` | `SNAPSHOT-RENDERED` | `UNCOLUMNED` | A card in no section must still be named |
| `08-all-drops-nothing` | `SNAPSHOT-RENDERED` | `UNCOLUMNED` | The per-row bound; no total ceiling in `--all` |
| `09-title-is-not-a-description` | `SNAPSHOT-RENDERED` | — | Composed, never reworded from the title |
| `10-all-cannot-clip` | `SNAPSHOT-RENDERED` | — | 200 cards; length is not a reason to drop |
| `11-empty-card-body` | `SNAPSHOT-RENDERED` | — | A card that says nothing is reported, never invented |
| `12-handles-in-a-description` | `SNAPSHOT-RENDERED` | — | Handles stripped; card numbers kept, and never laundered |
| `13-mandatory-sections-exceed-the-ceiling` | `SNAPSHOT-CLIPPED` | — | The tiebreak: the ceiling yields, never a blocked card |
| `14-open-issue-off-the-board` | `SNAPSHOT-RENDERED` | `OFF-BOARD` | Issues never added to the project are named, never rendered |

`READ-ONLY` is expected on every fixture, because it is a claim about every run.

**Every fixture declares its `mode`** — `standing` or `all` — because the two modes bound themselves
differently and the driver holds them to different rules. The standing check clips its queued section;
the orientation read drops nothing, so `SNAPSHOT-CLIPPED` there is a defect rather than a mode.

**Fixture 09 carries counterexamples, and they are forbidden outputs rather than candidate prose.**
`CLAUDE.md` records that a board fixture may not supply candidates — text a run could select instead of
composing, which is passed by publishing the shorter string. A counterexample is the inverse: prose the
run must not produce, paired with the `must_not` clause that forbids it. The driver enforces the
distinction, and it also checks each counterexample genuinely violates what it claims to — the
over-length one really exceeds 100 words, and the reworded-title one deliberately does **not**, so it can
only fail on rewording.

**Fixture 01 asserts a word count, and that does not contradict the board-prose rule.** `CLAUDE.md`
records that `tests/test_issue_board_fixtures.py` forbids a fixture from asserting a word count — a rule
about the *prose standard*, where the point is compose well and never compose short, and where a count
would turn a composition test into a brevity test. **This ceiling is a specified feature.** Issue #34 asks
for output verifiably at or under 200 words and for a fixture that pins it on a board large enough to
breach it. Asserting the count here is the requirement; asserting it over a composed description would be
the defect. Stated because the two look identical from a distance.
