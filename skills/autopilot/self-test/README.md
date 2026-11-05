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
