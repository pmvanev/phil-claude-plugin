---
name: work
description: Skill bundle for phil:work command — wave-based orchestrator for invisible technical initiatives; frames, plans, safeguards, and executes by delegating to your tactical skills, with behavior provably preserved and a decision trail left behind.
---

# Work

Act as the **general contractor** for an invisible technical initiative — refactoring,
re-architecting, cleanup, a migration, a dependency or performance pass — work the end user never
sees. Give it the discipline nwave gives user-facing features: **discuss, plan, safeguard, execute,
document** — without a user story.

**Discuss, plan, sequence and gate; re-implement no execution.** Delegate each unit of real change to a
tactical skill that already carries the right safety gate. Supply what those skills lack: framing the
goal, sequencing the work, and leaving a decision trail.

Read the standards to work under before FRAME: `${CLAUDE_PLUGIN_ROOT}/rules/refactoring.md`,
`${CLAUDE_PLUGIN_ROOT}/rules/coding.md`, `${CLAUDE_PLUGIN_ROOT}/rules/testing.md`, and
`${CLAUDE_PLUGIN_ROOT}/rules/architecture.md`.

> **The workflow.** FRAME → MAP (a wave-by-wave roadmap, each wave routed to the fitting skill) →
> SAFETY-NET (pin the change surface) → EXECUTE (each wave delegated and gated, the sequence
> stopping cleanly on any failure or pausing for a release) → VERIFY (both gates: preservation floor
> + declared goal metric) → document (working trail + durable evolution summary).

---

## The two-gate spine (never compromise this)

Every initiative is held to **two** gates:

1. **Preservation floor** (always) — observable behavior is unchanged. Never certify this yourself;
   the **delegate's own oracle** does (see *Delegation & the inherited oracle*).
2. **Initiative goal** (declared in FRAME) — the specific point of *this* work, captured as a
   **checkable metric** and read at VERIFY.

A run that breaks the preservation floor is **never** reported as done. A run that preserves
behavior but misses its declared goal metric is **never** reported as done. On an accepted
preservation-only basis, the preservation floor is the only gate (see FRAME §2). Grade the final
state, not the effort.

---

## Parse the argument

| Pattern | Mode | Action |
|---------|------|--------|
| `"<initiative>"` | Start | Run FRAME on a new initiative, then the loop below. |
| No argument | Resume | Resume the in-flight initiative from its `docs/work/<slug>/progress.md`: read the roadmap and the per-wave status, and continue from the first wave not yet `done`. Do not re-run completed waves or re-frame. With several in-flight initiatives under `docs/work/`, ask which; with none, say so and stop. When that wave is `failed`, the run stopped on it: ask before re-running the wave that stopped it. When it is `awaiting-release`, ask the developer to confirm that the release containing the previous wave's commit reached production — and, before a contract wave, that no release a rollback could restore still reads or writes the old shape. On a yes, mark the wave `pending` and run it. On a no, leave it `awaiting-release`, report the run **paused for release**, and stop. |

Derive a kebab-case `<slug>` from the initiative for the trail path `docs/work/<slug>/`.

---

## FRAME — scope the initiative

Do these in order. Do not survey, delegate, or open a trail until FRAME resolves.

### 1. Off-ramp trivial work first

If the initiative is small enough that a **single existing tactical skill** would handle it
directly — a lone rename, one extraction, a comment cleanup, a single-file structural tidy —
**do not run the workflow**. Name the skill that fits and recommend running it directly:

> "This is a single-skill job. Run `/phil:refactor <target>` (or `/phil:extract-method`,
> `/phil:clean-comments`, …) directly — `/phil:work` would just add ceremony." Then **exit**.

A rename of a shape a running release reads or writes — a column, a message field, an API field — is
not a lone rename: it takes expand and contract waves (MAP §2).

Do not build a roadmap, run a safety net, or open a `docs/work/<slug>/` trail for trivial work.
Ceremony on small work is the thing developers resent; the off-ramp exists to prevent it.

### 2. Frame a checkable goal (or refuse)

State the initiative's goal as a **checkable metric**. Draw from the taxonomy:

- **Code:** coupling / fan-out target, dependency count, cyclomatic complexity, a benchmark or
  latency budget.
- **Prose (skills/rules/agents):** the self-test passes, no dead links or broken skill refs,
  valid frontmatter, file length under N, a required citation present.

If the stated goal cannot be made checkable (e.g. *"make it better"*, *"clean it up"*), **do not
proceed**. Either:
- ask the developer to restate it as a checkable metric, **or**
- offer to continue on a **behavior-preservation-only** basis (the preservation floor as the sole
  gate), which the developer must explicitly accept.

Change nothing until a checkable goal or an explicit preservation-only basis is agreed. Record the
goal metric's **current (before) reading** now, so VERIFY can measure the delta against the target.

### 3. Declare the preservation contract and pick the oracle

State how behavior will be held, chosen by **artifact type** — the oracle to inherit, never to run
yourself:

| The wave changes… | Delegate | Preservation oracle (delegate-owned) |
|---|---|---|
| executable **code** | `refactor-loop` (or `refactor` / `extract-method` for a simple move) | its test-suite gate |
| **test prose** (test files) | `refactor-tests` / `redesign-tests` | its human-approval diff review |
| **other prose** (skill / rule / agent / doc) | the **human-approval diff gate directly** — no dedicated delegate exists | human diff review |

> **Non-test prose has no delegate.** `refactor-tests` and `redesign-tests` handle *test* files only,
> so a skill, rule, agent or doc wave uses the human-approval diff gate **directly**: apply the
> smallest change, pause for the developer to review the uncommitted diff in their editor, commit on
> approve, `git checkout` on reject. This inherits the *oracle* — the human — and re-implements no
> preservation check.

### 4. Confirm with the developer

Summarize goal + preservation contract + IN/OUT scope and get explicit confirmation
(`AskUserQuestion`) before any change. Then record the framed decision: write
`docs/work/<slug>/decisions.md` with the goal and its before reading, the preservation contract,
the chosen delegate and oracle, and the IN/OUT scope.

**This ask follows `${CLAUDE_PLUGIN_ROOT}/skills/shared/decision-request.md`.** Load it before the call.
Every question this skill puts to the developer follows it — the goal restatement in §2, the roadmap
approval, an unpinnable seam, a prose wave's diff review and a resume choice included.

- **The context block is the framed contract** — goal, preservation contract, IN/OUT scope, chosen
  delegate and oracle. The counted ask states what is being sanctioned and what it commits to, in
  plain terms; the artifact paths and the delegate's name stay above it.
- **A decline here is not a deferral.** Nothing may change before this answer, so record a decline and
  stop rather than proceeding on a partial one.

---

## MAP — plan the waves

Survey the change surface, then produce an ordered, editable roadmap of waves.

### 1. Survey (delegate the reading)

Understand the current state before planning. Delegate the survey to the fitting skill rather than
doing it ad hoc: `/phil:review-code <scope>` to seed a smell backlog, `/phil:spirit-walk` to
understand unfamiliar code, or a change-frequency hotspot pass to prioritize. Use the survey to
find the real change surface and its risks.

### 2. Roadmap

Decompose the initiative into an **ordered list of waves**. Each wave names:
- the **change** it makes (one cohesive structural step),
- the **delegate** that will execute it, **routed by the change type** (table below),
- the **gate** it clears (the delegate's oracle, plus the goal check at VERIFY).

**Per-wave routing.** Pick the delegate that fits the wave's change type, and justify the choice
in the roadmap:

| Wave change type | Delegate | Oracle inherited |
|---|---|---|
| Larger / gated code refactor | `/phil:refactor-loop` | suite gate (Workflow cage) |
| Simple code refactor from a backlog | `/phil:refactor` | suite gate |
| A single extraction | `/phil:extract-method` | suite gate |
| Comment / docstring cleanup | `/phil:clean-comments` | suite gate |
| Test-prose structure cleanup | `/phil:refactor-tests` | human-approval diff |
| Sanctioned test-prose behavior change | `/phil:redesign-tests` | human-approval diff |
| Other-prose (skill / rule / agent / doc) structure | human-approval diff gate directly (no dedicated delegate) | human diff review |
| Surveying the change surface (MAP §1) | `/phil:review-code`, `/phil:spirit-walk`, hotspot | n/a (read-only) |

The same FRAME→MAP→SAFETY-NET→EXECUTE→VERIFY spine carries every initiative type (refactor,
re-architecture, cleanup, migration, dependency/perf) — only the per-wave delegate differs. A
migration is handled as a re-architecture initiative routed across these delegates; there is no
bespoke migration engine.

A migration that changes a database schema, or any other shape a running release reads or writes,
works under `${CLAUDE_PLUGIN_ROOT}/rules/continuous-delivery.md` as well; a release here is an
artifact deployed to production. Read the rule's Database Changes section and its *Roll back on
demand* paragraph before the roadmap. Plan expand and contract as separate waves. The expand wave
adds the new shape and writes both. Between them, plan a backfill wave when existing rows hold data
the new shape needs, then a wave that switches reads to the new shape, then one that stops writing
the old. Ship each of these waves as its own release: the release before a wave must still run
against the schema that wave leaves, because that release is the rollback target. Each wave's own
release must run against that schema too: the expand wave relaxes any constraint that forces a write
to the old shape, such as `NOT NULL`, before a later wave stops writing it. Plan the contract wave
last; Resume confirms before it runs that no release a rollback could restore still reads or writes
the old shape. In the roadmap, mark each of these waves `ships alone`.

Keep waves small and independently committable — one wave, one delegate, one commit, mirroring the
delegates' own per-item discipline. Write the roadmap to `docs/work/<slug>/roadmap.md`, and write
`docs/work/<slug>/progress.md` with every wave `pending`, so a run that stops on its first wave still
leaves a status to resume from.

### 3. Approve

Show the developer the roadmap and let them **edit** it — reorder, drop, or split waves — before
any execution. A flat ordered list is enough; a dependency DAG is only warranted if waves truly
depend on each other (start flat, escalate on evidence).

> If the survey shows the initiative is actually a single wave, run the one wave directly; manufacture
> no multi-wave roadmap to look busy.

---

## SAFETY-NET — pin the change surface before you cut

The preservation floor is only real if something actually **catches** a regression. Before EXECUTE
touches anything, make sure each wave's change surface is pinned. A green suite you don't trust —
or a prose skill with no self-test — is not a safety net.

### 1. Detect a thin pin (per artifact type)

- **Code:** is the wave's change surface (the functions/files it will touch) exercised by the
  suite? Grep the tests for the target symbols/files; if a coverage tool is available, check the
  target is hit. A target with no test exercising it is **thinly pinned**.
- **Prose (skill / rule / agent):** is the specific behavior this wave changes pinned by a
  self-test fixture or acceptance scenario? No self-test harness, or no fixture covering the
  touched behavior, means **thinly pinned** — prose has no code coverage, so the pin is a
  self-test scenario or a recorded human-approval baseline, not a percentage.

### 2. Pin it (delegate the authoring where a skill fits)

Where the pin is thin, pin **current** observable behavior before changing structure:
- **Code:** add characterization / golden-master / contract tests that capture today's behavior,
  built as `${CLAUDE_PLUGIN_ROOT}/rules/test-patterns.md` describes them — a Characterization Test asserts
  what the code does now, not what it should; an approval test scrubs every field that varies between
  runs, or the pin is erratic; a contract test holds a fake to the real implementation, and a
  consumer-driven contract pins a service boundary.
- **Prose:** capture the current self-test scenarios, or record a human-approval baseline of the
  current output, so a later diff can be judged against it.

### 3. Establish a good baseline

Run the pin once and confirm it is green (code) or captured (prose) **before** EXECUTE. This is the
baseline the delegates' gates will hold against.

### 4. When a seam cannot be pinned

If a seam genuinely has no feasible executable oracle and cannot be characterized, do **not**
proceed silently. Fall back to the **human-approval diff** gate for that wave and **flag it
high-risk for manual review** in `decisions.md`. Surface the risk to the developer; never treat an
unpinnable seam as if it were safe.

---

## EXECUTE — run the roadmap, one gated wave at a time

Work the roadmap in order. For each wave, in turn:

### Delegation & the inherited oracle

Hand the wave's change to its delegate by invoking that skill's command
(`/phil:refactor-loop`, `/phil:refactor`, `/phil:refactor-tests`, …). **The delegate owns the
gate:** its suite gate (code) or human-approval diff (prose) is the oracle. Run no preservation check
of your own. This is non-negotiable: re-implementing a weaker gate here would
defeat the whole design.

### The sequencing gate (the only gate you own)

React to each wave's delegate result:

- **Delegate succeeded** (suite green / self-test green / diff approved) → mark the wave `done` in
  `progress.md` with its commit sha and oracle result. Then:
  - if no wave remains, go on to VERIFY;
  - if this wave or the next is marked `ships alone`, mark the next wave `awaiting-release` and
    stop. Report the run as **paused for release** — neither done nor failed — naming the wave that
    waits and the commit its release must contain;
  - otherwise, continue to the next wave.
- **Delegate failed** (suite red / self-test broken / diff rejected) → the delegate has already
  reverted its own change. **Stop the sequence.** Do **not** run any later wave. Leave the working
  tree in its **last-good** state (the last `done` wave's committed result) — never red. Mark the
  wave `failed` in `progress.md`, and record in `decisions.md` **which wave failed and why**. Report
  the run as **stopped / incomplete** — never as done.

Never narrate past a delegate failure. A run that broke something — or that stopped with waves
unfinished — is not a success. Grade the final state, not the effort.

---

## VERIFY & DOCUMENT

A run paused for release has not reached VERIFY: report it paused, never done, and leave the goal
gate for the run that finishes the last wave.

1. **Preservation gate** — confirm the preservation oracle passed for every wave (the delegates
   reported green / approved). If not, the run should already have stopped in EXECUTE — never report it
   green here.
2. **Goal gate** — read the goal metric now (its **after** value) and compare to the target
   recorded in FRAME. Report the reading as `before → after (target)`. On a preservation-only basis,
   skip the goal gate: the preservation result alone decides done, and the report says no goal was
   declared.
   - **Met** → the goal gate clears.
   - **Not met** → report the goal as **not achieved**, showing the reading as evidence, and do
     **not** report the initiative as done — even though behavior was preserved. Preservation
     alone is not success; the initiative had a point, and it was not reached. The developer
     decides whether to run another pass.
3. Write the trail under `docs/work/<slug>/`: finalize `decisions.md` (what was done per wave, the
   delegates used, the preservation results, the commits made) and `progress.md` (every wave's
   final status).
4. Write the **durable evolution summary** to `docs/evolution/<date>-<slug>.md` — what changed,
   why, the goal outcome (before → after vs target), and the preservation result. Create
   `docs/evolution/` if the repository has none. This is the record that outlives the working trail.
5. Report a summary to the developer naming: the **goal outcome**, the **preservation result**
   (oracle green / approved), and the **commit(s)** made.

---

## Safety rules

- **A contractor, not an executor.** Never re-implement a delegate's preservation gate. Delegate the
  change; inherit the gate.
- **The two-gate spine holds absolutely.** Preservation floor always; the declared goal whenever one
  was declared. Miss either → not done.
- **A delegate failure never leaves the tree red** and is never reported as done. Leave last-good;
  record it; stop.
- **A wave that ships alone pauses the run for its release.** A paused run is neither done nor
  failed.
- **Off-ramp trivial work.** If one skill would do, recommend it and exit — no ceremony.
- **Refuse an uncheckable goal.** No checkable metric and no explicit preservation-only → do not
  start.
- **Leave a trail.** Every non-trivial run writes `docs/work/<slug>/decisions.md`.
- **Report honestly.** Grade the final state, not the effort. Never fake done.

---

## Self-test (regression gate)

`${CLAUDE_PLUGIN_ROOT}/skills/work/self-test/` holds golden fixtures that pin these safety
behaviors: FRAME refuses an uncheckable goal (01), off-ramps trivial work (02), carries one
initiative end-to-end (03, walking skeleton), routes code vs prose (04, 05),
stops-and-leaves-last-good on a delegate failure (06), reports a missed goal as not-done (07), and
splits a schema migration into expand and contract waves (08), and pauses for release after a wave
that ships alone (09). Whenever this skill or `${CLAUDE_PLUGIN_ROOT}/commands/work.md` changes,
drive the fixtures per its `README.md` and confirm each produces its `expected.md` decision — every
edit here is non-monotonic, so the skill is changed and regression-tested, never changed and
eyeballed.
