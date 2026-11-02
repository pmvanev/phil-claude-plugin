# Self-test — done

The acceptance and regression gate for `../SKILL.md`. Run it whenever that file or `commands/done.md`
changes.

**Driven by `tests/test_done_fixtures.py`, in the repo suite.** The driver checks structure: each
fixture is well-formed, names outcomes the skill defines, forbids a merge, and claims `WROTE-NOTHING`;
together the fixtures cover every outcome. It cannot judge whether a run composed the right report —
the fixtures are model-driven, and that read is by hand.

| Fixture | Terminal | Alongside | Pins |
|---|---|---|---|
| `01-open-checklist-item` | `NOT-READY` | `OPEN-ASKS` | An item with no evidence holds the close |
| `02-narrated-only` | `NOT-READY` | `OPEN-ASKS` | A reply or a tick is not evidence; the search for real evidence comes back empty |
| `03-open-pull-request` | `NOT-READY` | `NOT-LANDED` | An open pull request blocks, and is never merged |
| `04-red-main` | `NOT-READY` | `NOT-LANDED` | Green on the branch, red on main, is not landed |
| `05-no-pipeline` | `READY` | `NO-PIPELINE` | A repo with no pipeline reads `no pipeline`, never green |
| `06-session-ask-beside-the-card` | `READY` | — | The report lists a request made only in the session |
| `07-closed-unmerged-only` | `NOT-READY` | `NOT-LANDED` | A pull request closed unmerged is not landed work |
| `08-merged-into-a-feature-branch` | `NOT-READY` | `NOT-LANDED` | A merge into any base but the default branch has not landed |
| `09-head-not-yet-reported` | `NOT-READY` | `NOT-LANDED` | A head with no rollup yet is not a repo with no pipeline |
| `10-no-pull-request-found` | `NOT-READY` | `NOT-LANDED` | Verified files do not stand in for a merge |
| `11-list-cut-short` | `NOT-READY` | `NOT-LANDED` | A truncated list is never judged |

`WROTE-NOTHING` is expected on every fixture: this version writes nothing.
