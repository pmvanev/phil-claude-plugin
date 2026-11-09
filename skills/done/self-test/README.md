# Self-test — done

The acceptance and regression gate for `../SKILL.md`. Run it whenever that file, a file in
`../references/` or `commands/done.md` changes.

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
| `23-earlier-sessions-worktree-removed` | `CLOSED` | `CLEARED` | A clean, unlocked worktree an earlier session made goes on the one yes |
| `24-unmerged-branch-survives` | `CLOSED` | `CLEARED` `LEFT` | A branch a worktree holds is never offered for force-delete |
| `25-dirty-worktree-survives` | `CLOSED` | `LEFT` | A dirty worktree keeps its snapshot |
| `26-name-only-branch-is-no-candidate` | `CLOSED` | `CLEARED` | A branch that only looks like the card's is never touched |
| `27-clean-finish-asks-once` | `CLOSED` | `CLEARED` | A clean finish asks exactly one question |
| `28-retire-the-snapshot-here` | `CLOSED` | `CLEARED` | The snapshot here goes only on the third answer |
| `29-current-worktree-removed-last` | `CLOSED` | `CLEARED` | The worktree the session started in goes last, through `git worktree remove` |
| `30-remote-tip-ahead-of-the-merge` | `CLOSED` | `CLEARED` `LEFT` | A remote branch past the merge survives; git would not guard it |
| `31-local-tip-ahead-of-the-merge` | `CLOSED` | `LEFT` | A local commit after the merge holds the branch and its remote |
| `32-retire-refused` | `CLOSED` | `LEFT` | A snapshot changed after the plan survives |
| `33-shared-or-foreign-branch-held` | `CLOSED` | `LEFT` | Protected, fork and shared branches are never deleted |
| `34-push-url-names-another-repo` | `CLOSED` | `CLEARED` `LEFT` | The push URL, not the fetch URL, decides the remote |
| `35-another-authors-pull-request` | `CLOSED` | `CLEARED` `LEFT` | A colleague's branch is never a candidate |
| `36-force-delete-an-unmerged-branch` | `CLOSED` | `CLEARED` | An unmerged branch goes only on its own answer, its commits shown |
| `37-colleague-reused-the-name` | `CLOSED` | `LEFT` | A branch under an old name is not the developer's to force-delete |
| `38-too-many-commits-to-show` | `CLOSED` | `LEFT` | Past 50 commits the tip goes unshown, so nothing is offered |
| `39-gitlab-card-closes` | `CLOSED` | `CLEARED` | GitLab closes the card through `glab`: note, status label off, close |
| `40-gitlab-pipeline-still-running` | `NOT-READY` | `NOT-LANDED` `WROTE-NOTHING` | Only a `success` pipeline is green |
| `41-gitlab-fork-merge-request-held` | `CLOSED` | `CLEARED` `LEFT` | A fork's merge request gives no candidate, whatever its branch is named |
| `42-no-card-clean-finish` | `FINISHED` | `CLEARED` | No argument checks the session's work and touches no card |
| `43-no-card-open-session-task` | `NOT-READY` | `OPEN-ASKS` `WROTE-NOTHING` | A session task with no evidence holds the finish |
| `44-no-card-retire-the-snapshot-only` | `FINISHED` | `CLEARED` | A plan holding only the snapshot here asks once: retire it or keep it |
| `45-no-card-branch-the-session-never-named` | `FINISHED` | `CLEARED` | A branch the conversation never names is no candidate |
| `46-no-card-reused-branch-name` | `NOT-READY` | `OPEN-ASKS` `NOT-LANDED` `WROTE-NOTHING` | An old pull request under a reused branch name is not the session's work |
| `47-session-worktree-removed` | `FINISHED` | `CLEARED` | A worktree this session made, clean at the merged tip, goes on the one yes |
| `48-hidden-work-holds-the-worktree` | `FINISHED` | `LEFT` `WROTE-NOTHING` | Work `git worktree remove` would delete silently holds the worktree |
| `49-session-worktree-with-a-snapshot` | `FINISHED` | `CLEARED` | The worktree holding the snapshot here goes only on the third answer |
| `50-locked-worktree-is-held` | `CLOSED` | `LEFT` | A locked worktree stays, however clean |
| `51-locked-session-worktree-is-listed` | `CLOSED` | `LEFT` | A lock on the worktree the session started in lists it, never plans its removal |
| `52-stale-snapshot-here-is-flagged` | `CLOSED` | `CLEARED` `LEFT` | The snapshot here carries its STALE verdict and distance, and a plain yes still keeps it |
| `53-current-snapshot-here-is-marked-current` | `CLOSED` | `CLEARED` `LEFT` | A snapshot at `HEAD` on a clean tree reads CURRENT, never STALE |
| `54-snapshot-off-heads-history` | `CLOSED` | `CLEARED` `LEFT` | A snapshot off `HEAD`'s history reads STALE with no commit count |

`WROTE-NOTHING` is expected on every fixture that writes nothing.
