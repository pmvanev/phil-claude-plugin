# review-ci — Self-Test

`review-ci` writes a backlog, and its failures are silent: a finding filed under the wrong row, a
documented idiom flagged, or a supply-chain defect filed as a pipeline item all look like an ordinary
backlog. These fixtures hand the reviewer a known pipeline and state what its backlog must and must not
contain. Run them whenever `skills/review-ci/SKILL.md`, `commands/review-ci.md` or
`rules/ci-pipelines.md` changes.

## What the fixtures pin

| Fixture | Situation | Rule under test | Expected outcome |
|---|---|---|---|
| `01-pipeline-findings-cite-a-row/` | twelve pipeline defects and one mutable image tag beside six look-alikes, on both forges, including defects one edit fixes across several jobs | `rules/ci-pipelines.md` Always-flag and Do not flag; `security.md`'s CWE-829 row | thirteen must-fix items, each with its row's id and Preferred form, each shared defect filed once; no look-alike filed |

## Layout

Each fixture holds the pipeline under review — the CI files, any `Dockerfile` a job builds, and the
scripts its jobs call — plus:

- `manifest.json` — what the fixture pins, its look-alikes, and how many items it must yield;
- `expected.md` — the hard assertions, and what does not count as a failure;
- `expected-backlog.md` — the items the review must write.

## How to drive it

1. Copy the fixture's project files to a scratch directory — everything except `manifest.json`,
   `expected.md` and `expected-backlog.md`, which a review of `.` would otherwise read.
2. In that copy, follow this working tree's `skills/review-ci/SKILL.md` with `.` as the argument.
3. Compare the written `.ci-review.md` with `expected-backlog.md` on the criteria in `expected.md`. Any
   hard assertion that fails blocks the change.

## What runs automatically, and what does not

`tests/test_ci_pipelines_rule.py` checks that every expected item takes its id and fix from one row,
that every Zampetti id the rule cites was checked against the paper, and that each look-alike is in the
fixture and absent from its expected backlog. **Whether a review produces those items is model
judgement.** Step 2 needs an agent or a person, and step 3 needs a judge. A green repo suite says the
fixtures are well-formed, not that the reviewer passes them.
