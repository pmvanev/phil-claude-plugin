# Self-test — start

The acceptance and regression gate for `../SKILL.md`. Run it whenever that file or `commands/start.md`
changes.

**Driven by `tests/test_start_fixtures.py`, in the repo suite.** The driver checks structure: each
fixture is well-formed, names outcomes the skill defines, and forbids a board write; a run that stops
before CLAIM claims `WROTE-NOTHING`; together the fixtures cover every outcome. It cannot judge whether a
run composed the right report — the fixtures are model-driven, and that read is by hand.

Unless a fixture says otherwise, the repo is this one, its CLAUDE.md holds the board block, the session
runs from the main checkout, and the card is open, on the board in Todo, and unassigned, with no
worktree, no open pull request and no surviving branch.

The `gitlab-` fixtures, 48–59, replace the repo with a GitLab one, `team/app` on `gitlab.example.dev`;
each states its forge line and status family, and each forbids AC5.9's four traps and a stop for the
forge.

| Fixture | Terminal | Alongside | Pins |
|---|---|---|---|
| `01-several-matches` | `NOT-LAUNCHED` | `PICKED`, `CLAIMED`, `BUILD-PATH`, `WORKTREE-CUT` | AC1.1, and issue 80's first fixture behaviour: an ambiguous argument lists candidates instead of picking one |
| `02-no-match` | `NO-MATCH` | `WROTE-NOTHING` | AC1.2: filing is offered, and happens only on a yes |
| `03-closed-card` | `REFUSED-CLOSED` | `WROTE-NOTHING` | AC1.3, and issue 80's third fixture behaviour: a closed card is never restarted silently |
| `04-open-card-in-done` | `STOPPED` | `OPEN-IN-DONE`, `WROTE-NOTHING` | AC1.3 |
| `05-someone-elses-card` | `STOPPED` | `ANOTHERS-CARD`, `WROTE-NOTHING` | AC1.4, and issue 80's second fixture behaviour: a card assigned to someone else stays theirs unless the developer says otherwise |
| `06-no-done-when` | `NOT-LAUNCHED` | `CLAIMED`, `NO-DONE-WHEN`, `WORKTREE-CUT` | AC2.3 |
| `07-build-path-overrides` | `LAUNCHED` | `CLAIMED`, `BUILD-PATH`, `WORKTREE-CUT` | AC2.2 |
| `08-no-yes-no-launch` | `NOT-LAUNCHED` | `CLAIMED`, `BUILD-PATH`, `WORKTREE-CUT` | AC2.1, and issue 80's sixth fixture behaviour: the recommendation names a route and launches none without a yes |
| `09-wave-label-routes` | `LAUNCHED` | `CLAIMED`, `ROUTE-OVERRIDDEN`, `WORKTREE-CUT` | D9 rule 2, and the learning hypothesis: an override is the evidence that the card and CLAUDE.md did not choose the route |
| `10-pull-request-number` | `NO-MATCH` | `WROTE-NOTHING` | A number names an issue or a pull request on GitHub; a pull request is no card |
| `11-fits-one-sitting` | `LAUNCHED` | `CLAIMED`, `WORKTREE-CUT` | D9 rule 4: a card that fits one sitting goes inline, overriding rule 3 |
| `12-too-many-matches` | `STOPPED` | `WROTE-NOTHING` | D4: a list the query cut short is never offered as the whole |
| `13-go-on-past-done` | `NOT-LAUNCHED` | `OPEN-IN-DONE`, `CLAIMED`, `WORKTREE-CUT` | skill-reviewer, 2026-11-03: the go-on path had no fixture |
| `14-go-on-past-another` | `NOT-LAUNCHED` | `ANOTHERS-CARD`, `CLAIMED`, `WORKTREE-CUT` | AC1.4 and AC3: another's card answered yes adds the developer beside them, never in their place |
| `15-colon-in-the-argument` | `LAUNCHED` | `CLAIMED`, `BUILD-PATH`, `WORKTREE-CUT` | The slice brief's dogfood moment |
| `16-no-forge-line` | `CANNOT-RUN` | `WROTE-NOTHING` | plugin-validator, 2026-11-03: an early stop matched no terminal outcome |
| `17-number-names-nothing` | `NO-MATCH` | `WROTE-NOTHING` | plugin-validator, run live 2026-11-03: a number naming nothing errors; it never answers null |
| `18-build-path-step-done` | `NOT-LAUNCHED` | `CLAIMED`, `WORKTREE-CUT`, `BUILD-PATH` | skill-reviewer, 2026-11-03: the build path sent card 80 back through a wave that had run |
| `19-card-not-on-the-board` | `NOT-LAUNCHED` | `CLAIMED`, `WORKTREE-CUT` | AC3.1, and `phil:issue-board`: an issue never added has no field to set, and editing it does nothing |
| `20-read-back-mismatch` | `NOT-LAUNCHED` | `READ-BACK-MISMATCH`, `WORKTREE-CUT` | AC3.2: a board write that reports success while the card sits elsewhere is the characteristic failure |
| `21-no-signed-in-account` | `CANNOT-RUN` | `WROTE-NOTHING` | D5, AC3.3, and issue 80's fourth fixture behaviour: an account the run cannot name is reported, never guessed |
| `22-unassignable-account` | `NOT-LAUNCHED` | `NOT-ASSIGNED`, `WORKTREE-CUT` | D5, AC3.3: an account the forge will not assign is reported, and nothing is assigned in its place |
| `23-no-board-block` | `NOT-LAUNCHED` | `NO-BOARD-BLOCK`, `WORKTREE-CUT` | D8, AC3.4, and the learning hypothesis: the board block, not a probe, supplies the Status ids |
| `24-filed-on-a-yes` | `NOT-LAUNCHED` | `FILED`, `CLAIMED`, `NO-DONE-WHEN`, `WORKTREE-CUT` | AC3.5: a card filed on a yes is claimed, and carries only the developer's words |
| `25-missing-project-scope` | `NOT-LAUNCHED` | `CLAIM-FAILED`, `WORKTREE-CUT` | D8: the claim stops at the first write that fails, and `phil:issue-board` names the scope `gh auth login` omits |
| `26-item-never-lands` | `NOT-LAUNCHED` | `CLAIM-FAILED`, `WORKTREE-CUT` | plugin-validator, 2026-11-03: a re-read with no board node had no rule |
| `27-done-with-no-board-block` | `NOT-LAUNCHED` | `OPEN-IN-DONE`, `NO-BOARD-BLOCK`, `WORKTREE-CUT` | skill-reviewer and plugin-validator, 2026-11-03: go on promised a move that CLAIM without a block never makes |
| `28-assign-silently-dropped` | `NOT-LAUNCHED` | `NOT-ASSIGNED`, `WORKTREE-CUT` | skill-reviewer, 2026-11-03: the forge can drop an assignee it will not accept, and exit 0 |
| `29-read-fails-mid-claim` | `NOT-LAUNCHED` | `READ-BACK-MISMATCH`, `WORKTREE-CUT` | skill-reviewer, 2026-11-03: a read that failed after the first write had no outcome |
| `30-blocked-card` | `STOPPED` | `WROTE-NOTHING` | skill-reviewer, 2026-11-03: a card in Blocked left it silently, hiding the blocker |
| `31-no-worktree-cut-fresh` | `NOT-LAUNCHED` | `CLAIMED`, `WORKTREE-CUT` | D1, AC4.1 |
| `32-worktree-entered` | `UNDERWAY` | `CLAIMED`, `WORKTREE-ENTERED`, `WROTE-NOTHING` | D2, D3, AC4.2, and issue 80's fifth fixture behaviour: a card that already has a worktree reuses it |
| `33-two-candidate-worktrees` | `UNDERWAY` | `CLAIMED`, `WORKTREE-ENTERED`, `WROTE-NOTHING` | D3: several candidates are the developer's pick |
| `34-snapshot-in-the-worktree` | `UNDERWAY` | `CLAIMED`, `WORKTREE-ENTERED`, `WROTE-NOTHING` | D2, AC4.3: a card with a snapshot is resumed, not started |
| `35-session-in-another-worktree` | `STOPPED` | `WROTE-NOTHING` | AC4.4: a session already in another worktree is moved only on a yes |
| `36-move-out-of-another-worktree` | `NOT-LAUNCHED` | `CLAIMED`, `WORKTREE-CUT` | AC4.4, and the tool's rule that a worktree cannot be created from inside another worktree session |
| `37-open-pull-request-no-worktree` | `UNDERWAY` | `CLAIMED`, `WROTE-NOTHING` | D2: an open pull request means the work is underway, and a fresh worktree would restart it |
| `38-worktree-another-session-holds` | `UNDERWAY` | `CLAIMED`, `WROTE-NOTHING` | Seen 2026-11-03 on this repo: a worktree another live session holds carries its lock reason |
| `39-tool-refuses` | `NOT-LAUNCHED` | `CLAIMED`, `WORKTREE-FAILED` | A refusal is reported, never worked around with a grant this command lacks |
| `40-base-ref-head` | `NOT-LAUNCHED` | `CLAIMED`, `WORKTREE-CUT` | D1: the report names the base commit the developer actually got |
| `41-already-in-the-cards-worktree` | `UNDERWAY` | `CLAIMED`, `WORKTREE-ENTERED`, `WROTE-NOTHING` | skill-reviewer and plugin-validator, 2026-11-03: the second run, the slice brief's dogfood moment, had no rule |
| `42-refused-enter-underway` | `UNDERWAY` | `CLAIMED`, `WORKTREE-FAILED`, `WROTE-NOTHING` | skill-reviewer and plugin-validator, 2026-11-03: a refused enter sent an underway card to ROUTE |
| `43-underway-card-still-claimed` | `UNDERWAY` | `CLAIMED`, `WORKTREE-ENTERED` | D2, plugin-validator, 2026-11-03: a card underway is still claimed |
| `44-surviving-branch` | `UNDERWAY` | `CLAIMED` | skill-reviewer, 2026-11-03: a branch left after its worktree was removed collides with the cut |
| `45-worktree-by-pr-branch` | `UNDERWAY` | `CLAIMED`, `WORKTREE-ENTERED` | D3's second rule: a worktree is the card's when it holds the branch of the developer's open pull request |
| `46-prunable-entry` | `NOT-LAUNCHED` | `CLAIMED`, `WORKTREE-CUT` | skill-reviewer, 2026-11-03: a prunable entry counted as the card's, and entering it fails |
| `47-exit-does-nothing` | `NOT-LAUNCHED` | `CLAIMED`, `WORKTREE-FAILED` | plugin-validator and skill-reviewer, 2026-11-03: ExitWorktree acts only on a worktree this session entered |
| `48-gitlab-claim-cut-fresh` | `NOT-LAUNCHED` | `CLAIMED`, `WORKTREE-CUT` | AC5.1, and slice 04's learning hypothesis: the GitHub steps translate call for call, and only the claim changes shape |
| `49-gitlab-another-assignee-kept` | `NOT-LAUNCHED` | `ANOTHERS-CARD`, `CLAIMED`, `WORKTREE-CUT` | D14, AC5.2: a login without `+` replaces every assignee and exits 0 |
| `50-gitlab-no-in-progress-label` | `NOT-LAUNCHED` | `CLAIMED`, `WORKTREE-CUT` | D12, AC5.3: no label reads in progress, so the developer names it before any label is written |
| `51-gitlab-closed-card` | `REFUSED-CLOSED` | `WROTE-NOTHING` | D15, AC5.4: the closed list is GitLab's Done |
| `52-gitlab-blocked-label` | `STOPPED` | `WROTE-NOTHING` | D15, AC5.4: a blocked label asks, as Blocked does on GitHub |
| `53-gitlab-merge-request-underway` | `UNDERWAY` | `CLAIMED`, `WROTE-NOTHING` | D18, AC5.5: the developer's open merge request means the work is underway |
| `54-gitlab-no-status-family` | `NOT-LAUNCHED` | `NO-BOARD-BLOCK`, `WORKTREE-CUT` | D13, AC5.6: no status family writes no label and still assigns |
| `55-gitlab-filed-on-a-yes` | `NOT-LAUNCHED` | `FILED`, `CLAIMED`, `NO-DONE-WHEN`, `WORKTREE-CUT` | D19, AC5.7: a card filed through `glab` carries only the developer's title |
| `56-gitlab-open-with-a-done-label` | `STOPPED` | `OPEN-IN-DONE`, `WROTE-NOTHING` | AC5.4's third clause: an open card with a done label is a defect, asked |
| `57-gitlab-free-another-assignee` | `NOT-LAUNCHED` | `ANOTHERS-CARD`, `NOT-ASSIGNED`, `WORKTREE-CUT` | skill-reviewer and plugin-validator, 2026-11-05: GitLab Free holds one assignee per issue |
| `58-gitlab-label-not-on-the-project` | `NOT-LAUNCHED` | `CLAIM-FAILED`, `WORKTREE-CUT` | skill-reviewer and plugin-validator, 2026-11-05: `--label` with a missing name creates it and reads back as set |
| `59-gitlab-several-in-progress-labels` | `STOPPED` | `WROTE-NOTHING` | D12, AC5.3's second clause: several matches are the developer's pick |
