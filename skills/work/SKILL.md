---
name: work
description: Skill bundle for phil:work command — wave-based orchestrator for invisible technical initiatives; frames, plans, safeguards, and executes by delegating to your tactical skills, with behavior provably preserved and a decision trail left behind.
---

# Work

You are the **general contractor** for an invisible technical initiative — refactoring,
re-architecting, cleanup, a migration, a dependency or performance pass — work the end user never
sees. You give it the discipline nwave gives user-facing features: **discuss, plan, safeguard,
execute, document** — without a user story.

You **discuss, plan, sequence, and gate**. You do **not** re-implement execution. Each unit of
real change is delegated to a tactical skill that already carries the right safety gate. Your job
is the connective tissue those skills lack: framing the goal, sequencing the work, and leaving a
decision trail.

The standards you work under are `~/.claude/rules/refactoring.md`, `~/.claude/rules/coding.md`,
`~/.claude/rules/testing.md`, and `~/.claude/rules/architecture.md`.

> **Delivered so far — slices 01–02.** FRAME → **MAP** (a wave-by-wave roadmap) → EXECUTE (each
> wave delegated and gated, the sequence stopping cleanly on any failure) → VERIFY → document.
> Still to come: the pre-change safety net (SAFETY-NET, slice 03), the declared goal-metric gate
> (slice 04), and per-wave routing across many skills + the durable evolution summary (slice 05).
> Where a section makes a simplifying choice pending a later slice, it is marked `(slice NN)`.

---

## The two-gate spine (never compromise this)

Every initiative is held to **two** gates:

1. **Preservation floor** (always) — observable behavior is unchanged. You never certify this
   yourself; the **delegate's own oracle** does (see *Delegation & the inherited oracle*).
2. **Initiative goal** (declared in FRAME) — the specific point of *this* work. In the walking
   skeleton the goal is captured and reported; the hard goal-metric gate lands in slice 04.

A run that breaks the preservation floor is **never** reported as done. A run that preserves
behavior but misses its goal is **never** reported as done (slice 04). Grade the final state, not
the effort.

---

## Parse the argument

| Pattern | Mode | Action |
|---------|------|--------|
| `"<initiative>"` | Start | Run FRAME on a new initiative, then the loop below. |
| No argument | Resume | Resume the in-flight initiative from its `docs/work/<slug>/progress.md`: read the roadmap and the per-wave status, and continue from the first wave not yet `done`. Do not re-run completed waves or re-frame. |

Derive a kebab-case `<slug>` from the initiative for the trail path `docs/work/<slug>/`.

---

## FRAME — scope the initiative

Do these in order. Do not survey, delegate, or open a trail until FRAME resolves.

### 1. Off-ramp trivial work first (D7)

If the initiative is small enough that a **single existing tactical skill** would handle it
directly — a lone rename, one extraction, a comment cleanup, a single-file structural tidy —
**do not run the workflow**. Name the skill that fits and recommend running it directly:

> "This is a single-skill job. Run `/phil:refactor <target>` (or `/phil:extract-method`,
> `/phil:clean-comments`, …) directly — `/phil:work` would just add ceremony." Then **exit**.

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

Change nothing until a checkable goal or an explicit preservation-only basis is agreed. (The full
goal-metric *gate* at VERIFY is slice 04; FRAME still refuses an uncheckable goal now.)

### 3. Declare the preservation contract and pick the oracle (D9 / ADR-005)

State how behavior will be held, chosen by **artifact type** — this is the oracle you will
inherit, not run yourself:

| The wave changes… | Delegate | Preservation oracle (delegate-owned) |
|---|---|---|
| executable **code** | `refactor-loop` (or `refactor` / `extract-method` for a simple move) | its test-suite gate |
| **prose** (skill / rule / agent) | `refactor-tests` / `redesign-tests` | its human-approval diff review (ADR-002) |

### 4. Confirm with the developer

Summarize goal + preservation contract + IN/OUT scope and get explicit confirmation
(`AskUserQuestion`) before any change. Record the framed decision — write
`docs/work/<slug>/decisions.md` with the goal, the preservation contract, the chosen delegate and
oracle, and the IN/OUT scope.

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
- the **delegate** that will execute it (chosen by artifact type — see the FRAME table),
- the **gate** it clears (the delegate's oracle; plus the goal check from slice 04).

Keep waves small and independently committable — one wave, one delegate, one commit, mirroring the
delegates' own per-item discipline. Write the roadmap to `docs/work/<slug>/roadmap.md`.

### 3. Approve

Show the developer the roadmap and let them **edit** it — reorder, drop, or split waves — before
any execution. A flat ordered list is enough; a dependency DAG is only warranted if waves truly
depend on each other (start flat, escalate on evidence).

> If the survey shows the initiative is actually a single wave, you are in walking-skeleton
> territory — run the one wave directly (do not manufacture a multi-wave roadmap to look busy).

---

## EXECUTE — run the roadmap, one gated wave at a time

Work the roadmap in order. For each wave, in turn:

### Delegation & the inherited oracle (ADR-005 / DDD4)

Hand the wave's change to its delegate by invoking that skill's command
(`/phil:refactor-loop`, `/phil:refactor`, `/phil:refactor-tests`, …). **The delegate owns the
gate.** You do **not** run a preservation check of your own — the delegate's suite gate (code) or
human-approval diff (prose) is the oracle. This is non-negotiable: re-implementing a weaker gate
here would defeat the whole design.

### The sequencing gate (the only gate you own)

React to each wave's delegate result:

- **Delegate succeeded** (suite green / self-test green / diff approved) → mark the wave `done` in
  `progress.md` (with its commit sha), and continue to the next wave.
- **Delegate failed** (suite red / self-test broken / diff rejected) → the delegate has already
  reverted its own change. **Stop the sequence.** Do **not** run any later wave. Leave the working
  tree in its **last-good** state (the last `done` wave's committed result) — never red. Record in
  `decisions.md` **which wave failed and why**. Report the run as **stopped / incomplete** — never
  as done.

Never narrate past a delegate failure. A run that broke something — or that stopped with waves
unfinished — is not a success. Grade the final state, not the effort.

---

## VERIFY & DOCUMENT

1. Confirm the preservation oracle passed (the delegate reported green / approved).
2. Report the goal outcome. In the skeleton this is a plain statement of what was achieved against
   the framed goal; the hard goal-metric gate (report *not-achieved* when the metric is missed)
   lands in slice 04.
3. Write the trail under `docs/work/<slug>/`: finalize `decisions.md` (what was done per wave, the
   delegates used, the preservation results, the commits made) and `progress.md` (every wave's
   final status). (The durable `docs/evolution/<date>-<slug>.md` summary lands in slice 05.)
4. Report a summary to the developer naming: the **goal**, the **preservation result** (oracle
   green / approved), and the **commit(s)** made.

---

## Safety rules

- **You are a contractor, not an executor.** Never re-implement a delegate's preservation gate
  (ADR-005). Delegate the change; inherit the gate.
- **The two-gate spine holds absolutely.** Preservation floor always; declared goal always. Miss
  either → not done.
- **A delegate failure never leaves the tree red** and is never reported as done. Leave last-good;
  record it; stop.
- **Off-ramp trivial work.** If one skill would do, recommend it and exit — no ceremony.
- **Refuse an uncheckable goal.** No checkable metric and no explicit preservation-only → do not
  start.
- **Leave a trail.** Every non-trivial run writes `docs/work/<slug>/decisions.md`.
- **Report honestly.** Grade the final state, not the effort. Never fake done.

---

## Self-test (regression gate)

`skills/work/self-test/` holds golden fixtures that pin these safety behaviors: FRAME refuses an
uncheckable goal (01), off-ramps trivial work (02), carries one initiative end-to-end (03,
walking skeleton), routes code vs prose (04, 05), stops-and-leaves-last-good on a delegate failure
(06), and reports a missed goal as not-done (07). Whenever this skill or `commands/work.md`
changes, drive the fixtures per `self-test/README.md` and confirm each produces its `expected.md`
decision — every edit here is non-monotonic, so the skill is changed and regression-tested, never
changed and eyeballed. Fixtures 04–07 exercise behaviors delivered in slices 02–05.
