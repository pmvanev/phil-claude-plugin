<!-- markdownlint-disable MD024 -->
# Feature Delta — loop-agent-least-privilege

Wave: DISCUSS ✓ (2026-10-20) · Density: lean
Build path: DISCUSS here, then the agent files, hook and rule change are written directly — the
deliverable is prose, configuration and one hook script, so DESIGN, DISTILL and DELIVER stay out (edd-loop
DDD8). `plugin-dev:agent-development` and `plugin-dev:hook-development` are read before each slice's
files; `plugin-dev:plugin-validator` runs over the result.

`/phil:refactor-loop` starts five agents that hold a full shell and any-path write: the gate runner,
applier, reverter, committer and ledger writer. Issue 48 (CWE-250) requires each to start as an agent
type granted only what its task needs, proven by a probe that tries something outside the grant. This
feature names the boundary that can actually hold and slices the work.

---

## Wave: DISCUSS / [REF] The gap, measured

Measured 2026-10-20 against `main` at `ab5bf22`:

- **Five agents start untyped.** `workflows/refactor-loop.js` passes no `agentType` at lines 302 and
  366 (gate), 362 (apply), 371 and 389 (revert), 383 (commit), and 316 and 403 (ledger). Each holds the
  default workflow agent's tools, shell and write included. The proposer, its fix mode and the critic
  already start as read-only types (`ab5bf22`).
- **A command pattern in an agent's `tools:` line limits nothing.** A probe agent granted only
  `Bash(echo:*)` ran from a fresh process in bypass mode: `touch`, a redirect, an `&&` chain and a
  `$(…)` substitution each wrote a file, and `ls` ran. In default mode the writes were refused, but
  every refusal cited the working-directory rule, never the grant. The agent held `Bash` and nothing
  else, so `tools:` selects tools and not commands. The documentation agrees: a specifier in
  `disallowedTools` "still removes the whole tool".
- **A plugin hook keyed on agent type does hold.** A spike ran a `PreToolUse` hook on `Bash` from a
  fresh process in bypass mode, under a Workflow `agent()` with an `agentType`. The hook's input
  carried `agent_type`, `agent_id` and `permission_mode: bypassPermissions`; its deny refused the
  `touch`, the redirect, the chain, the substitution and the `ls`, and nothing reached disk through
  `Bash`. The hook saw each command line whole.
- **Plugin agents cannot carry their own hooks.** The sub-agents page: plugin subagents ignore
  `hooks`, `mcpServers` and `permissionMode`; a plugin ships hooks in `hooks/hooks.json`.
- **The security standard recommends the form that limits nothing.** `rules/security.md:155` gives
  `Bash(git log:*)`, "not `Bash`", as the narrowest grant for an agent. Every consumer's review
  applies it.

## Wave: DISCUSS / [REF] Pre-requisites

- **Spike, done (2026-10-20):** the probe and hook spike above. Their scripts were throwaway and live
  in no tracked file; the measurements are recorded here.
- **Unverified, slice 01 settles it:** the `agent_type` string a *plugin* agent carries in hook input.
  The spike used a built-in type; a plugin agent is expected to arrive as `phil:<name>`.
- **Existing artifacts touched:** `workflows/refactor-loop.js`, `hooks/hooks.json`,
  `hooks/refactor-loop/` (one new script, README), `agents/` (five new files),
  `docs/design/refactor-loop/adr-008-workflow-orchestrator.md` and `adr-009-…` (dated updates),
  `rules/security.md`, `skills/review-code/self-test/`, `.claude-plugin/plugin.json`,
  `docs/product/jobs.yaml`.

## Wave: DISCUSS / [REF] Persona ID

**`quinn-codebase-steward`, unchanged.** Quinn runs `/phil:refactor-loop` to pay down a codebase's
debt and, to let it run unattended, often runs in bypass mode. Same person, same command; the loop's
agents must stop holding more than their steps need.

**Rejected: `rowan-skeptical-delegator`.** Rowan wants a finished task attacked by a non-builder. Quinn
wants the builder's mechanical hands limited before anything is finished.

## Wave: DISCUSS / [REF] JTBD one-liner

**New job: `delegate-mechanical-steps-without-handing-over-a-shell`.**

> When I let an autonomous loop change my repository unattended, I want each of its mechanical steps to
> hold only the command or file that step needs, so I can grant the loop bypass mode without granting
> every agent in it my whole machine.

Not a facet of `keep-test-suite-trustworthy`: that job protects what the tests verify; this one bounds
what the loop's agents can do at all. Recorded in `docs/product/jobs.yaml`.

## Wave: DISCUSS / [REF] Locked decisions

| ID | Decision | Rationale |
|----|----------|-----------|
| D1 | **Two parts make the boundary.** The agent file's `tools:` line picks whole tools; one plugin `PreToolUse` hook, keyed on `agent_type`, allows each role only its exact commands and paths. | The probe: `tools:` cannot pick commands. The spike: the hook sees the agent type and its deny holds in bypass mode. Plugin agents cannot carry their own hooks. |
| D2 | **The hook fails closed for the five types and stays silent for every other caller**, whether or not a loop run is active. | The agent type is the trigger. A role's grant does not depend on a ledger the guarded party could write (CWE-807). |
| D3 | **The hook parses each command into words and matches every word**, and refuses any shell syntax first: `;`, `&`, `\|`, `<`, `>`, `$`, a backtick, a newline. Never a prefix match. | The probe's escapes were a chain, a redirect and a substitution; each begins with an allowed word. |
| D4 | **Data reaches a role through one fixed file per kind, never through its command line.** The applier writes the patch and the committer the message, each with `Write` pinned to that one path; `Bash` then names the file. | A diff or a message on the command line needs quoting, heredocs or pipes — the syntax D3 refuses. |
| D5 | **The reverter runs `git apply -R` on the same patch file.** If that fails, the run halts and reports; it never widens to `git checkout`. Amends ADR-009's scoped revert by a dated update. | One allowed command instead of `checkout` plus `rm` on paths the hook cannot bound. `git apply` is atomic, so the tree is HEAD plus exactly the patch when a revert runs. |
| D6 | **On `git apply` and `git add`, the hook reads the patch file itself**: it refuses a patch touching a test path, the ledger or a loop file, and an `add` naming a path the patch does not. | The cage scanned the proposer's diff, not the bytes the applier wrote. An applier misled by its prompt could write a different patch. |
| D7 | **The gate runner runs only the run's own test command**, read by the hook from a source no subagent can write. Slice 05 names the source. | The test command is the user's, so it is arbitrary code by design. The grant stops the agent running anything else; it cannot make the tests safe. |
| D8 | **Only the ledger-writer type may write the ledger, among subagents.** | Falls out of D1. Narrows the accepted CWE-807 gap — "an agent that writes the ledger directly can still switch G2 off" — from any agent to the one whose content the cage composes. |
| D9 | **`rules/security.md` corrects its preferred form to what was measured**: in an agent file, a command pattern selects the tool, not the command; the narrow form is a tool set plus an enforced allow-list, or no shell. Command `allowed-tools` were not measured, and the rule says so. | Route "what a skill asserts": fold into the rule, add the fixture that would have caught it, bump the version. |
| D10 | **Each slice proves its grant two ways**: pytest over the hook with hostile commands, and a live probe from a fresh `claude -p` process in bypass mode that tries something outside the grant. | Issue 48's done-when. A fresh process, because `/clear` keeps an agent registry that predates a new agent file. |

## Wave: DISCUSS / [REF] Driving ports

- **`/phil:refactor-loop`** — its workflow starts each mechanical step as a narrowed agent type.
- **The `PreToolUse` hook in `hooks/hooks.json`** — every tool call from those types passes through it.
- **`/phil:review-code`** — reads the corrected row of `rules/security.md`.

## Wave: DISCUSS / [REF] WS strategy

**A — none.** Brownfield: the loop runs end to end today. Slice 01 is the thinnest change that proves
the mechanism on a plugin agent.

## Wave: DISCUSS / [REF] Scope Assessment: PASS

Five slices, each one role or one rule row; one context (the refactor loop and its hooks), one new hook
script. No oversized signal fires.

## Wave: DISCUSS / [REF] User stories

All stories trace to `job_id: delegate-mechanical-steps-without-handing-over-a-shell`.

### US-01 — The ledger writer writes the ledger and nothing else *(mechanism slice)*

**Problem.** The ledger step holds a shell and any-path write to copy text into one file.

**Solution.** A `phil:refactor-ledger-writer` type with `Read` and `Write`; the new hook pins both to
the ledger path, and refuses a ledger write from any other subagent type (D8).

#### Elevator Pitch
Before: the agent that records a run can run any command and write any file.
After: run `/phil:refactor-loop` on a scope → sees the ledger written as before, and a probe of the
ledger-writer type trying `touch` or another path sees `refused by the refactor-loop allow-list`.
Decision enabled: whether the hook mechanism holds for plugin agents, before the four other roles use it.

#### Acceptance Criteria
- [ ] The hook's input for a plugin agent carries the `agent_type` the hook keys on, recorded verbatim.
- [ ] The ledger-writer type writes and overwrites the ledger; every other path, and every `Bash` call,
      is refused with a reason naming the allow-list.
- [ ] A `Write` or `Edit` to the ledger from any other subagent type is refused.
- [ ] The hook stays silent for the main session and for every other agent type.
- [ ] Both ledger steps in the workflow pass `agentType`, and a test pins each to it.

### US-02 — The standard stops recommending a grant that limits nothing

**Problem.** `review-code` tells consumers that `Bash(git log:*)` is the narrow grant for an agent.

**Solution.** Correct the preferred form per D9, with a self-test fixture whose agent file grants a
command pattern and expects the finding.

#### Elevator Pitch
Before: a review accepts `tools: Bash(git log:*)` on an agent as narrow.
After: run `/phil:review-code agents/` on a fixture agent with that line → sees a CWE-250 item saying
the pattern selects the tool, not the command, and naming the enforced form.
Decision enabled: whether an agent's grant actually confines it, or needs a hook or no shell.

#### Acceptance Criteria
- [ ] The row states what was measured and what was not (command `allowed-tools`).
- [ ] A fixture fails without the corrected row and passes with it.
- [ ] The version is bumped.

### US-03 — The applier and reverter run one command each

**Problem.** Applying and reverting a diff hold a full shell.

**Solution.** `phil:refactor-applier` (`Read` and `Write` pinned to the patch file; `Bash` allowing
`git apply --recount [--check] <patch>`) and `phil:refactor-reverter` (`Bash` allowing only
`git apply --recount -R [--check] <patch>`), per D4–D6.

#### Elevator Pitch
Before: a misled applier could run anything, or apply a patch other than the one the cage checked.
After: run `/phil:refactor-loop` on a scope → sees diffs applied and reverted as before; a patch
touching a test path is refused at apply time with the path named.
Decision enabled: whether to trust an unattended run's apply and revert steps.

#### Acceptance Criteria
- [ ] Each type's allow-list matches exactly the command shapes above; D3's syntax is refused.
- [ ] The hook refuses `git apply` of a patch touching a test path, the ledger or a loop file.
- [ ] A failed `git apply -R` halts the run with the error, and never falls back to `checkout`.
- [ ] Every diff scan refuses a diff touching the patch file.
- [ ] ADR-009 carries a dated update for D5.

### US-04 — The committer stages only what the patch changed

**Problem.** Committing holds a full shell and could stage anything.

**Solution.** `phil:refactor-committer`: `Read` and `Write` pinned to the message file; `Bash` allowing
`git add -- <paths>` where every path is one the patch names, and `git commit -F <message file>`.

#### Elevator Pitch
Before: the committer could stage unrelated files or run any command.
After: run `/phil:refactor-loop` on a scope → sees one commit per green refactoring as before; an `add`
naming a path outside the patch is refused.
Decision enabled: whether a run's commits can be pushed without auditing what they staged.

#### Acceptance Criteria
- [ ] `git add` with any path the patch does not name is refused, as is any other `git` verb.
- [ ] `git commit` accepts only `-F` with the pinned message file.
- [ ] The repository's own pre-commit hooks still run; the README says they run the repository's code.

### US-05 — The gate runner runs the test command and nothing else *(last)*

**Problem.** The gate holds a full shell to run one command the user named.

**Solution.** `phil:refactor-gate-runner`: `Read`, `Grep`, `Glob`, and `Bash` allowing the run's test
command exactly, plus the read-only `git` calls its public-API check needs. The hook reads the test
command from a source no subagent can write (D7).

#### Elevator Pitch
Before: the agent that runs the tests could also run anything else.
After: run `/phil:refactor-loop` on a scope → sees each gate result as before; a probe of the gate type
running any other command sees it refused.
Decision enabled: whether the only arbitrary code in a run is the user's own test suite.

#### Acceptance Criteria
- [ ] The test command reaches the hook from a source no subagent type can write, named in the slice.
- [ ] Every command other than the test command and the named `git` reads is refused.
- [ ] The README states that the test suite itself runs arbitrary code, and the grant does not limit it.

## Wave: DISCUSS / [REF] Out-of-scope

- Narrowing command `allowed-tools` across this plugin. D9 states it is unmeasured; a probe is a card.
- Sandboxing the test suite or pre-commit hooks the repository ships.
- The interactive `--interactive` skill path, where the main session runs the loop's steps itself.
- The proposer, its fix mode and the critic — done in `ab5bf22`.

## Wave: DISCUSS / [REF] Definition of Done

1. Every `agent()` call in `workflows/refactor-loop.js` passes an `agentType`, pinned by a test.
2. Each new agent file's `tools:` line names whole tools only, pinned by a test.
3. The hook's tests cover every role's allowed shapes and the D3 syntax, chains and substitutions.
4. A live probe per role, from a fresh process in bypass mode, is recorded with its version.
5. A full refactor-loop run on a real scope completes green with all five types, recorded.
6. ADR-008 and ADR-009 carry dated updates; the hooks README describes the new hook.
7. `rules/security.md` row corrected, with its fixture; the version is bumped per slice.
8. `python3 -m pytest -q` and `scripts/check-invariants.py` pass.
9. Each commit names that `nw-discuss` ran and which `plugin-dev` skills and reviewers ran.

## Wave: DISCUSS / [REF] Outcome KPIs

- **Who:** a developer running `/phil:refactor-loop` unattended.
- **Does what:** runs the loop with no step able to act outside its task.
- **By how much:** loop agents holding an unchecked shell or any-path write fall from 5 to 0; every
  live probe outside a grant is refused (target: all, per role).
- **Measured by:** the workflow's agent-type pins, the hook's tests, and the recorded probes.
- **Baseline:** 5 of 8 agent calls untyped, measured at `ab5bf22`.

## Wave: DISCUSS / [REF] DoR validation

All nine items pass: job traceable (new job in `jobs.yaml`); persona exists (Quinn); ACs testable by
pytest and live probe; KPIs numeric; scope assessed; the mechanism is measured, not assumed (probe and
spike); the one open fact is named with the slice that settles it; boundaries with ADR-008 and ADR-009
named; out-of-scope listed.

## Wave: DISCUSS / [REF] Slice briefs

- `docs/feature/loop-agent-least-privilege/slices/slice-01-ledger-writer.md`
- `docs/feature/loop-agent-least-privilege/slices/slice-02-security-rule-row.md`
- `docs/feature/loop-agent-least-privilege/slices/slice-03-applier-and-reverter.md`
- `docs/feature/loop-agent-least-privilege/slices/slice-04-committer.md`
- `docs/feature/loop-agent-least-privilege/slices/slice-05-gate-runner.md`

## Wave: DISCUSS / [REF] Handoff

Order: 01 → 02 → 03 → 04 → 05. Slice 01 carries the one unverified fact — a plugin agent's
`agent_type` — and builds the hook the rest extend, so it goes first. Slice 02 follows once a plugin
agent has proved the corrected form. The gate runner goes last, by the human's decision (2026-10-20).

## Wave: DISCUSS / [REF] Delivered and dogfooded

### Slice 01 — the ledger writer (1.2.19, 2026-10-20)

Driven against this working tree through `claude -p --plugin-dir`, in bypass mode; the released copy
was not run.

- **The pre-requisite is settled.** A plugin agent arrives in the hook's payload as
  `phil:refactor-ledger-writer`. Unnarrowed workflow agents arrive as `workflow-subagent`.
- **Live probe.** The ledger writer wrote and read the ledger at a repository root and was refused
  `other.md` and `/etc/hostname`, each refusal naming the allow-list; it held only `Read` and `Write`.
  A `general-purpose` agent was refused the ledger and allowed `other.md`; the ledger kept
  `active-run: true`.
- **Real run.** One iteration of `/phil:refactor-loop` on a seeded repository: the ledger writer wrote
  the ledger at the start and the end, one refactoring committed, the run ended `HALT-INCOMPLETE` at its
  iteration bound, as configured. The hook refused nothing.
- **Review.** `plugin-dev:plugin-validator`: pass. Its warning — other subagents can still write the
  ledger through `Bash` — was already the stated residual; the docstring now says so too. No command
  filter stands in for it, because a glob spells the name past any filter (D10 of
  security-standards-rule: flag the capability, never a missing filter).
