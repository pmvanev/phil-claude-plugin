# Self-test — start

The acceptance and regression gate for `../SKILL.md`. Run it whenever that file or `commands/start.md`
changes.

**Driven by `tests/test_start_fixtures.py`, in the repo suite.** The driver checks structure: each
fixture is well-formed, names outcomes the skill defines, and forbids a board write; a run that stops
before CLAIM claims `WROTE-NOTHING`; together the fixtures cover every outcome. It cannot judge whether a
run composed the right report — the fixtures are model-driven, and that read is by hand.

Unless a fixture says otherwise, the repo is this one, its CLAUDE.md holds the board block, and the card
is open, on the board in Todo, and unassigned.

| Fixture | Terminal | Alongside | Pins |
|---|---|---|---|
| `01-several-matches` | `NOT-LAUNCHED` | `PICKED`, `CLAIMED`, `BUILD-PATH` | AC1.1, and issue 80's first fixture behaviour: an ambiguous argument lists candidates instead of picking one |
| `02-no-match` | `NO-MATCH` | `WROTE-NOTHING` | AC1.2: filing is offered, and happens only on a yes |
| `03-closed-card` | `REFUSED-CLOSED` | `WROTE-NOTHING` | AC1.3, and issue 80's third fixture behaviour: a closed card is never restarted silently |
| `04-open-card-in-done` | `STOPPED` | `OPEN-IN-DONE`, `WROTE-NOTHING` | AC1.3 |
| `05-someone-elses-card` | `STOPPED` | `ANOTHERS-CARD`, `WROTE-NOTHING` | AC1.4, and issue 80's second fixture behaviour: a card assigned to someone else stays theirs unless the developer says otherwise |
| `06-no-done-when` | `NOT-LAUNCHED` | `CLAIMED`, `NO-DONE-WHEN` | AC2.3 |
| `07-build-path-overrides` | `LAUNCHED` | `CLAIMED`, `BUILD-PATH` | AC2.2 |
| `08-no-yes-no-launch` | `NOT-LAUNCHED` | `CLAIMED`, `BUILD-PATH` | AC2.1, and issue 80's sixth fixture behaviour: the recommendation names a route and launches none without a yes |
| `09-wave-label-routes` | `LAUNCHED` | `CLAIMED`, `ROUTE-OVERRIDDEN` | D9 rule 2, and the learning hypothesis: an override is the evidence that the card and CLAUDE.md did not choose the route |
| `10-pull-request-number` | `NO-MATCH` | `WROTE-NOTHING` | A number names an issue or a pull request on GitHub; a pull request is no card |
| `11-fits-one-sitting` | `LAUNCHED` | `CLAIMED` | D9 rule 4: a card that fits one sitting goes inline, overriding rule 3 |
| `12-too-many-matches` | `STOPPED` | `WROTE-NOTHING` | D4: a list the query cut short is never offered as the whole |
| `13-go-on-past-done` | `NOT-LAUNCHED` | `OPEN-IN-DONE`, `CLAIMED` | skill-reviewer, 2026-11-03: the go-on path had no fixture |
| `14-go-on-past-another` | `NOT-LAUNCHED` | `ANOTHERS-CARD`, `CLAIMED` | AC1.4 and AC3: another's card answered yes adds the developer beside them, never in their place |
| `15-colon-in-the-argument` | `LAUNCHED` | `CLAIMED`, `BUILD-PATH` | The slice brief's dogfood moment |
| `16-no-forge-line` | `CANNOT-RUN` | `WROTE-NOTHING` | plugin-validator, 2026-11-03: an early stop matched no terminal outcome |
| `17-number-names-nothing` | `NO-MATCH` | `WROTE-NOTHING` | plugin-validator, run live 2026-11-03: a number naming nothing errors; it never answers null |
| `18-build-path-step-done` | `NOT-LAUNCHED` | `CLAIMED`, `BUILD-PATH`, `WROTE-NOTHING` | skill-reviewer, 2026-11-03: the build path sent card 80 back through a wave that had run |
| `19-card-not-on-the-board` | `NOT-LAUNCHED` | `CLAIMED` | AC3.1, and `phil:issue-board`: an issue never added has no field to set, and editing it does nothing |
| `20-read-back-mismatch` | `NOT-LAUNCHED` | `READ-BACK-MISMATCH` | AC3.2: a board write that reports success while the card sits elsewhere is the characteristic failure |
| `21-no-signed-in-account` | `CANNOT-RUN` | `WROTE-NOTHING` | D5, AC3.3, and issue 80's fourth fixture behaviour: an account the run cannot name is reported, never guessed |
| `22-unassignable-account` | `NOT-LAUNCHED` | `NOT-ASSIGNED` | D5, AC3.3: an account the forge will not assign is reported, and nothing is assigned in its place |
| `23-no-board-block` | `NOT-LAUNCHED` | `NO-BOARD-BLOCK` | D8, AC3.4, and the learning hypothesis: the board block, not a probe, supplies the Status ids |
| `24-filed-on-a-yes` | `NOT-LAUNCHED` | `FILED`, `CLAIMED`, `NO-DONE-WHEN` | AC3.5: a card filed on a yes is claimed, and carries only the developer's words |
| `25-missing-project-scope` | `NOT-LAUNCHED` | `CLAIM-FAILED` | D8: the claim stops at the first write that fails, and `phil:issue-board` names the scope `gh auth login` omits |
| `26-item-never-lands` | `NOT-LAUNCHED` | `CLAIM-FAILED` | plugin-validator, 2026-11-03: a re-read with no board node had no rule |
| `27-done-with-no-board-block` | `NOT-LAUNCHED` | `OPEN-IN-DONE`, `NO-BOARD-BLOCK` | skill-reviewer and plugin-validator, 2026-11-03: go on promised a move that CLAIM without a block never makes |
| `28-assign-silently-dropped` | `NOT-LAUNCHED` | `NOT-ASSIGNED` | skill-reviewer, 2026-11-03: the forge can drop an assignee it will not accept, and exit 0 |
| `29-read-fails-mid-claim` | `NOT-LAUNCHED` | `READ-BACK-MISMATCH` | skill-reviewer, 2026-11-03: a read that failed after the first write had no outcome |
| `30-blocked-card` | `STOPPED` | `WROTE-NOTHING` | skill-reviewer, 2026-11-03: a card in Blocked left it silently, hiding the blocker |
