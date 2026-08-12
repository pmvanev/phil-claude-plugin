# ATDD Infrastructure Policy

Per `nw-distill` § Project Infrastructure Policy. One file per project, decided once — not
renegotiated per feature. Apply-if-exists; write-if-absent; rewrite with `--policy=fresh`. Git history
is the audit trail.

Placed under `docs/product/architecture/` rather than the skill's suggested `docs/architecture/`,
because this repo already keeps its architecture SSOT there and project conventions win.

**This is a prose plugin.** The deliverable is skills, commands, and agents, not an application, so
the "adapters" below are the shell and filesystem calls a prose skill instructs the model to make.
Mechanisms are named accordingly: there is no DI container and no test host.

## Driving

| Port | Mechanism | Note |
|---|---|---|
| Slash command (`/phil:*`) | Golden fixture under `skills/<skill>/self-test/`, fed as a described situation | The plugin's established form; see `skills/edd/self-test/` |
| Slash command — end-to-end | Same-day dogfood on this repo, captured verbatim | The example-interaction evidence the `plugin` deliverable type requires |
| Lifecycle hook | `hooks/hooks.json` entry, exercised by a real session | Only `PreToolUse` G2 is currently verified this way |

## Driven internal (real)

| Port | Mechanism | Note |
|---|---|---|
| Filesystem (`.session-handoff.md`, backlogs) | Real files in a throwaway dir | `tests/test_self_test_fixtures.py` already builds throwaway repos this way |
| Git (tree fingerprint, commit, revert) | Real `git` in a throwaway repo | Real-adapter-always per Mandate 6 |

## Driven external / non-deterministic (fake)

| Port | Fake | Note |
|---|---|---|
| Forge (`gh`) | Fixture-supplied board state in `manifest.json` | Keeps the network out of the fixtures; the live board is covered by dogfood instead |
| Delegate commands (`/nw-continue`, `/phil:nwave-slice-status`) | Fixture-supplied return value in `manifest.json` | They own their own gates; this suite does not re-test them |
| The model itself | — | Judgment scenarios are adjudicated by a human or the model, not asserted |

## Runner reality

There is no CI in this plugin. Fixtures are driven by a human or the model, exactly as
`skills/work/self-test/` and `skills/edd/self-test/` are; tags carry traceability, not a collector.
`tests/test_self_test_fixtures.py` automates the subset whose outcomes are mechanically decidable
(currently `refactor-tests` and `refactor-loop`), and **pytest is not installed in the current
environment**, so that driver could not be executed during this wave.
