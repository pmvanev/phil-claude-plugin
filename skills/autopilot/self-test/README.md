# Autopilot self-test register

One directory per fixture, each with a `manifest.json` and an `expected.md`.
`tests/test_autopilot_fixtures.py` checks their structure and that every outcome autopilot adds has a
fixture. Judging a run against a fixture is a read by hand. Claim and worktree outcomes are
`/phil:start`'s, and its own fixtures pin them.

| # | Fixture | Pins | Outcome |
|---|---|---|---|
| 01 | `declared-path-beside-nwave` | AC1.1, AC1.3, AC1.4 | `PLANNED` · `DECLARED-PATH` · `RECORDED` |
| 02 | `no-declared-path` | AC1.2 | `PLANNED` · `FALLBACK-PATH` |
| 03 | `nwave-fallback` | D2 | `PLANNED` · `FALLBACK-PATH` |
| 04 | `already-recorded` | D5 | `PLANNED` · `UNDERWAY` · `ALREADY-RECORDED` · `WROTE-NOTHING` |
| 05 | `gitlab` | D10 | `CANNOT-RUN` · `GITHUB-ONLY` |
| 06 | `comment-fails` | D6 | `PLANNED` · `RECORD-FAILED` |
| 07 | `closed-card` | inherited | `REFUSED-CLOSED` |
| 08 | `no-match` | D9 | `NO-MATCH` |
| 09 | `stopped-at-anothers-card` | inherited | `STOPPED` · `ANOTHERS-CARD` |
| 10 | `nwave-no-label` | D2 | `PLANNED` · `FALLBACK-PATH` |
| 11 | `underway-no-worktree` | D5 | `PLANNED` · `UNDERWAY` · `RECORDED` |
