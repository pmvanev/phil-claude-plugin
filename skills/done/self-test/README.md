# Self-test — done

The acceptance and regression gate for `../SKILL.md`. Run it whenever that file or `commands/done.md`
changes.

**Driven by `tests/test_done_fixtures.py`, in the repo suite.** The driver checks structure: each
fixture is well-formed, names outcomes the skill defines, forbids a merge, lists the writes it expects and claims
`WROTE-NOTHING` exactly when that list is empty, and states the developer's answers when it runs past the report;
together the fixtures cover every outcome. It cannot judge whether a run composed the right report —
the fixtures are model-driven, and that read is by hand.

| Fixture | Terminal | Alongside | Pins |
|---|---|---|---|
| `01-open-checklist-item` | `NOT-READY` | `OPEN-ASKS` | An item with no evidence holds the close |
| `02-narrated-only` | `NOT-READY` | `OPEN-ASKS` | A reply or a tick is not evidence; the search for real evidence comes back empty |
| `03-open-pull-request` | `NOT-READY` | `NOT-LANDED` | An open pull request blocks, and is never merged |
| `04-red-main` | `NOT-READY` | `NOT-LANDED` | Green on the branch, red on main, is not landed |
| `05-no-pipeline` | `CLOSED` | `NO-PIPELINE` | A repo with no pipeline reads `no pipeline`, never green |
| `06-session-ask-beside-the-card` | `CLOSED` | — | The report lists a request made only in the session |
| `07-closed-unmerged-only` | `NOT-READY` | `NOT-LANDED` | A pull request closed unmerged is not landed work |
| `08-merged-into-a-feature-branch` | `NOT-READY` | `NOT-LANDED` | A merge into any base but the default branch has not landed |
| `09-head-not-yet-reported` | `NOT-READY` | `NOT-LANDED` | A head with no rollup yet is not a repo with no pipeline |
| `10-no-pull-request-found` | `NOT-READY` | `NOT-LANDED` | Verified files do not stand in for a merge |
| `11-list-cut-short` | `NOT-READY` | `NOT-LANDED` | A list with a failed page is never judged |
| `12-numbered-requirements` | `NOT-READY` | `OPEN-ASKS` | A numbered requirement list is read as asks |
| `13-card-edit-ask` | `CLOSED` | — | A card or board edit is verified on the card |
| `14-ask-dropped-with-a-reason` | `CLOSED` | `OPEN-ASKS` `ASK-DROPPED` | A dropped ask and its reason reach the comment |
| `15-comment-before-done` | `CLOSED` | — | Comment, then Done, then read the state before any close |
| `16-read-back-mismatch` | `CLOSED` | `READ-BACK-MISMATCH` | The read-back reports what it finds and repairs nothing |
| `17-finished-block` | `CLOSED` | `BLOCK-REFRESHED` | The block's writer renders a closed card finished |
| `18-stop-at-the-plan` | `STOPPED` | `WROTE-NOTHING` | A stop at the plan writes nothing |
| `19-a-write-fails` | `CLOSE-FAILED` | — | The first failed write stops the sequence |
| `20-stop-at-resolve` | `STOPPED` | `OPEN-ASKS` `WROTE-NOTHING` | A stop at RESOLVE; the quoted ask stays out of the question |
| `21-card-not-on-this-board` | `CLOSED` | — | A card on another board gets no Status write and no false mismatch |
| `22-card-already-closed` | `CLOSED` | — | A closed card gets its comment, never `close -c` |

`WROTE-NOTHING` is expected on every fixture that writes nothing.
