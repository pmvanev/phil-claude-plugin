# Self-test — start

The acceptance and regression gate for `../SKILL.md`. Run it whenever that file or `commands/start.md`
changes.

**Driven by `tests/test_start_fixtures.py`, in the repo suite.** The driver checks structure: each
fixture is well-formed, names outcomes the skill defines, forbids a board write, and claims
`WROTE-NOTHING`; together the fixtures cover every outcome. It cannot judge whether a run composed the
right report — the fixtures are model-driven, and that read is by hand.

| Fixture | Terminal | Alongside | Pins |
|---|---|---|---|
| `01-several-matches` | `NOT-LAUNCHED` | `PICKED`, `BUILD-PATH` | AC1.1, and issue 80's first fixture behaviour: an ambiguous argument lists candidates instead of picking one |
| `02-no-match` | `NO-MATCH` | — | AC1.2 |
| `03-closed-card` | `REFUSED-CLOSED` | — | AC1.3, and issue 80's third fixture behaviour: a closed card is never restarted silently |
| `04-open-card-in-done` | `STOPPED` | `OPEN-IN-DONE` | AC1.3 |
| `05-someone-elses-card` | `STOPPED` | `ANOTHERS-CARD` | AC1.4, and issue 80's second fixture behaviour: a card assigned to someone else stays theirs unless the developer says otherwise |
| `06-no-done-when` | `NOT-LAUNCHED` | `NO-DONE-WHEN` | AC2.3 |
| `07-build-path-overrides` | `LAUNCHED` | `BUILD-PATH` | AC2.2 |
| `08-no-yes-no-launch` | `NOT-LAUNCHED` | `BUILD-PATH` | AC2.1, and issue 80's sixth fixture behaviour: the recommendation names a route and launches none without a yes |
| `09-wave-label-routes` | `LAUNCHED` | `ROUTE-OVERRIDDEN` | D9 rule 2, and the learning hypothesis: an override is the evidence that the card and CLAUDE.md did not choose the route |
| `10-pull-request-number` | `NO-MATCH` | — | A number names an issue or a pull request on GitHub; a pull request is no card |
| `11-fits-one-sitting` | `LAUNCHED` | — | D9 rule 4: a card that fits one sitting goes inline, overriding rule 3 |
| `12-too-many-matches` | `STOPPED` | — | D4: a list the query cut short is never offered as the whole |
| `13-go-on-past-done` | `NOT-LAUNCHED` | `OPEN-IN-DONE` | skill-reviewer, 2026-11-03: the go-on path, where a later-claim promise tempted a write, had no fixture |
| `14-go-on-past-another` | `NOT-LAUNCHED` | `ANOTHERS-CARD` | skill-reviewer, 2026-11-03: the go-on path had no fixture, and AC1.4 holds on it too |
| `15-colon-in-the-argument` | `LAUNCHED` | `BUILD-PATH` | The slice brief's dogfood moment |
| `16-no-forge-line` | `CANNOT-RUN` | — | plugin-validator, 2026-11-03: an early stop matched no terminal outcome |
| `17-number-names-nothing` | `NO-MATCH` | — | plugin-validator, run live 2026-11-03: a number naming nothing errors; it never answers null |
| `18-build-path-step-done` | `NOT-LAUNCHED` | `BUILD-PATH` | skill-reviewer, 2026-11-03: the build path sent card 80 back through a wave that had run |

Every fixture expects `WROTE-NOTHING`: this version writes nothing before the launch.
