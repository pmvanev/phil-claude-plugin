# review-code — Self-Test

`review-code` writes a backlog, and its failures are silent: a finding filed under the wrong smell, a
correct test flagged, or a test finding routed to a loop that must not apply it all look like an
ordinary backlog. These fixtures feed the reviewer known code and state what its backlog must and must
not contain.

Run them whenever `skills/review-code/SKILL.md` changes, or whenever a rule it names changes what it
flags. Format mirrors `skills/redesign-tests/self-test/`.

## What the fixtures pin

| Fixture | Situation | Rule under test | Expected outcome |
|---|---|---|---|
| `01-test-findings-name-a-pattern/` | three test smells and one correct gateway-mock test | `rules/test-patterns.md` Smell Catalogue; the unmanaged-dependency exemption | three Priority 6 items, each with the catalogue's smell, fix and route; the gateway test not flagged |
| `02-security-findings-cite-a-cwe/` | ten security defects beside six safe look-alikes | `rules/security.md` Always-flag rows; its Do-not-flag list | ten Priority 1 items, each with its row's CWE id and Preferred form; no look-alike flagged |
| `03-security-trust-judgement/` | helpers whose inputs are untrusted in some places and not others | `rules/security.md`'s definition of untrusted | the hook and the label prompt flagged; the granted write left alone; the ledger raised as Advisory |
| `04-security-row-precision/` | a probe and two hooks on the edge of four rows | the rule's precision lines: accidental guards, CWE-636's scope, CWE-1333's threshold, one id per defect | four items; the wording gate unflagged; no CWE-770 beside CWE-1333 |
| `05-security-guard-integrity/` | a write guard that works until its subject attacks it, and the transcript it keeps | the guard-integrity rows (CWE-180, CWE-807); the transcript Advisory bullet | two guard items; the transcript raised as Advisory |
| `06-security-agent-grant/` | a subagent narrowed by `Bash(git log:*)` beside a read-only one | the CWE-250 agent row: a command pattern grants the whole shell | one CWE-250 item on the history reader; the read-only drafter left alone |

## Layout

Each fixture is self-contained and dependency-free (`python -m pytest` runs it green):

- the code under test (`invoice.py`) — clean, and contributes no Priority 6 item;
- the test file the review judges (`test_invoice.py`);
- any data file a smell needs (`invoice_cases.json`, the Mystery Guest's hidden input);
- `manifest.json` — what the fixture pins;
- `expected.md` — the hard assertions, and what a gate failure is;
- `expected-backlog.md` — the items the review must write.

## How to drive it

1. Run `python -m pytest -q` in the fixture directory. Expect **green**: a review fixture with a red
   suite tests the wrong thing.
2. Run `/phil:review-code .` in the fixture directory.
3. Compare the written `.refactoring-backlog.md` against `expected-backlog.md` on the criteria in
   `expected.md`. Any hard assertion that fails blocks the skill change.
4. Delete `.refactoring-backlog.md` and any `__pycache__/` the run left.

## What runs automatically, and what does not

`tests/test_test_patterns_wiring.py` checks that every fixture is complete and green, and that each
expected Priority 6 finding takes its smell, fix and route from one catalogue row. **Whether a review
produces those findings is model judgement**, and nothing here automates it: step 2 needs a person to
run it and step 3 a person to judge it. A green repo suite says the fixtures are well-formed, not that
the reviewer passes them.