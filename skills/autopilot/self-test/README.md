# Autopilot self-test register

One directory per fixture, each with a `manifest.json` and an `expected.md`.
`tests/test_autopilot_fixtures.py` checks their structure and that every outcome autopilot adds has a
fixture. Judging a run against a fixture is a read by hand. Claim and worktree outcomes are
`/phil:start`'s, and its own fixtures pin them. The Outcome column lists every token the manifest
expects.

| # | Fixture | Pins | Outcome |
|---|---|---|---|
| 01 | `declared-path-beside-nwave` | AC1.1, AC1.3, AC1.4 | `PLANNED` · `CLAIMED` · `WORKTREE-CUT` · `DECLARED-PATH` · `RECORDED` |
| 02 | `no-declared-path` | AC1.2 | `PLANNED` · `CLAIMED` · `WORKTREE-CUT` · `FALLBACK-PATH` · `RECORDED` |
| 03 | `nwave-fallback` | D2 | `PLANNED` · `CLAIMED` · `WORKTREE-CUT` · `FALLBACK-PATH` · `RECORDED` |
| 04 | `already-recorded` | D5 | `PLANNED` · `CLAIMED` · `UNDERWAY` · `WORKTREE-ENTERED` · `DECLARED-PATH` · `ALREADY-RECORDED` · `WROTE-NOTHING` |
| 05 | `gitlab-path-recorded` | AC1.5, D10 | `PLANNED` · `CLAIMED` · `WORKTREE-CUT` · `DECLARED-PATH` · `RECORDED` |
| 06 | `comment-fails` | D6 | `PLANNED` · `CLAIMED` · `WORKTREE-CUT` · `DECLARED-PATH` · `RECORD-FAILED` |
| 07 | `closed-card` | inherited | `REFUSED-CLOSED` · `WROTE-NOTHING` |
| 08 | `no-match` | D9 | `NO-MATCH` · `WROTE-NOTHING` |
| 09 | `stopped-at-anothers-card` | inherited | `STOPPED` · `ANOTHERS-CARD` · `WROTE-NOTHING` |
| 10 | `nwave-no-label` | D2 | `PLANNED` · `CLAIMED` · `WORKTREE-CUT` · `FALLBACK-PATH` · `RECORDED` |
| 11 | `underway-no-worktree` | D5 | `PLANNED` · `CLAIMED` · `UNDERWAY` · `DECLARED-PATH` · `RECORDED` |
| 12 | `done-step-is-yours` | D13 | `PLANNED` · `CLAIMED` · `WORKTREE-CUT` · `DECLARED-PATH` · `DONE-IS-YOURS` · `RECORDED` |
| 13 | `no-forge-line` | inherited | `CANNOT-RUN` · `WROTE-NOTHING` |
| 14 | `move-to-done-is-yours` | D13 | `PLANNED` · `CLAIMED` · `WORKTREE-CUT` · `DECLARED-PATH` · `DONE-IS-YOURS` · `RECORDED` |
| 15 | `gitlab-already-recorded` | D10, D5 | `PLANNED` · `CLAIMED` · `UNDERWAY` · `DECLARED-PATH` · `ALREADY-RECORDED` · `WROTE-NOTHING` |
| 16 | `carried-to-landing` | AC2.2, AC4.1, AC4.4 | `CARRIED` · `CLAIMED` · `WORKTREE-CUT` · `DECLARED-PATH` · `RECORDED` · `LANDED` · `HANDED-OFF` |
| 17 | `rule-answers` | AC2.1, D9 | `CARRIED` · `CLAIMED` · `WORKTREE-CUT` · `DECLARED-PATH` · `RECORDED` · `LANDED` · `HANDED-OFF` |
| 18 | `blocker-own-material` | AC2.3, AC3.1 | `BLOCKED` · `CLAIMED` · `WORKTREE-CUT` · `DECLARED-PATH` · `RECORDED` · `HANDED-OFF` |
| 19 | `check-keeps-failing` | D1 | `BLOCKED` · `CLAIMED` · `WORKTREE-CUT` · `DECLARED-PATH` · `RECORDED` · `HANDED-OFF` |
| 20 | `resumed` | AC3.2 | `CARRIED` · `CLAIMED` · `UNDERWAY` · `WORKTREE-ENTERED` · `DECLARED-PATH` · `ALREADY-RECORDED` · `RESUMED` · `LANDED` · `HANDED-OFF` |
| 21 | `unnamed-write-stops` | AC3.3 | `BLOCKED` · `CLAIMED` · `WORKTREE-CUT` · `DECLARED-PATH` · `RECORDED` · `HANDED-OFF` |
| 22 | `gitlab-carried` | D10 | `CARRIED` · `CLAIMED` · `WORKTREE-CUT` · `DECLARED-PATH` · `RECORDED` · `LANDED` · `HANDED-OFF` |
| 23 | `path-end-hands-off` | D13, AC4.4 | `CARRIED` · `CLAIMED` · `WORKTREE-CUT` · `DECLARED-PATH` · `DONE-IS-YOURS` · `RECORDED` · `HANDED-OFF` |
| 24 | `blocker-still-stands` | AC3.2 | `BLOCKED` · `CLAIMED` · `UNDERWAY` · `WORKTREE-ENTERED` · `DECLARED-PATH` · `ALREADY-RECORDED` · `HANDED-OFF` |
| 25 | `route-verdict-is-yours` | D1 | `BLOCKED` · `CLAIMED` · `WORKTREE-CUT` · `FALLBACK-PATH` · `RECORDED` · `HANDED-OFF` |
| 26 | `red-pipeline-fixed` | AC4.2 | `CARRIED` · `CLAIMED` · `WORKTREE-CUT` · `DECLARED-PATH` · `RECORDED` · `LANDED` · `HANDED-OFF` |
| 27 | `red-pipeline-blocks` | AC4.2 | `BLOCKED` · `CLAIMED` · `WORKTREE-CUT` · `DECLARED-PATH` · `RECORDED` · `HANDED-OFF` |
| 28 | `default-branch-red` | AC4.2 | `BLOCKED` · `CLAIMED` · `WORKTREE-CUT` · `DECLARED-PATH` · `RECORDED` · `HANDED-OFF` |
| 29 | `no-pipeline` | AC4.2 | `BLOCKED` · `CLAIMED` · `WORKTREE-CUT` · `DECLARED-PATH` · `RECORDED` · `HANDED-OFF` |
| 30 | `wave-boundary` | D7 | `CARRIED` · `CLAIMED` · `WORKTREE-CUT` · `FALLBACK-PATH` · `RECORDED` · `HANDED-OFF` |
| 31 | `last-wave-stays-in-progress` | AC4.3, D13 | `CARRIED` · `CLAIMED` · `WORKTREE-CUT` · `FALLBACK-PATH` · `RECORDED` · `HANDED-OFF` |
| 32 | `closing-reference-blocks` | D13 | `BLOCKED` · `CLAIMED` · `WORKTREE-CUT` · `DECLARED-PATH` · `RECORDED` · `HANDED-OFF` |
| 33 | `gitlab-no-pipeline` | D10, AC4.2 | `BLOCKED` · `CLAIMED` · `WORKTREE-CUT` · `DECLARED-PATH` · `RECORDED` · `HANDED-OFF` |
| 34 | `default-branch-red-before-merge` | AC4.2 | `BLOCKED` · `CLAIMED` · `WORKTREE-CUT` · `DECLARED-PATH` · `RECORDED` · `HANDED-OFF` |
| 35 | `dogfood-from-repo-guide` | AC5.1, D3, D10 | `CARRIED` · `CLAIMED` · `WORKTREE-CUT` · `DECLARED-PATH` · `RECORDED` · `LANDED` · `HANDED-OFF` |
| 36 | `dogfood-test-account` | AC5.1, AC5.4 | `CARRIED` · `CLAIMED` · `WORKTREE-CUT` · `DECLARED-PATH` · `RECORDED` · `HANDED-OFF` |
| 37 | `dogfood-local-run` | AC5.2 | `CARRIED` · `CLAIMED` · `WORKTREE-CUT` · `DECLARED-PATH` · `RECORDED` · `HANDED-OFF` |
| 38 | `dogfood-no-way-blocks` | AC5.3 | `BLOCKED` · `CLAIMED` · `WORKTREE-CUT` · `DECLARED-PATH` · `RECORDED` · `HANDED-OFF` |
| 39 | `no-running-product-no-walk` | AC5.2 | `CARRIED` · `CLAIMED` · `WORKTREE-CUT` · `DECLARED-PATH` · `RECORDED` · `LANDED` · `HANDED-OFF` |
| 40 | `repo-rule-binds-the-walk` | D3 | `CARRIED` · `CLAIMED` · `WORKTREE-CUT` · `DECLARED-PATH` · `RECORDED` · `HANDED-OFF` |
