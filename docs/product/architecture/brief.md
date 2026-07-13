# Architecture Brief (SSOT)

Bootstrapped by DESIGN wave, feature: refactor-tests (2026-07-01).

## Application Architecture

Owner: Morgan (nw-solution-architect).

### refactor-tests

A new `/phil:refactor-tests` command + `skills/refactor-tests/SKILL.md` that cleans test code
to `testing.md` structure standards via a **human-approved, structure-only** refactoring loop.
It follows the plugin's established command→skill split and `phil:refactor`'s backlog loop,
but swaps the automated pass/fail gate for a human-approval interaction port: the tool applies
one proposed move to the working tree, runs the suite as a sanity check, and pauses for the
developer to review the uncommitted diff **in their IDE/editor** before it is committed or
reverted.

**Status:** IMPLEMENTED (2026-07-02) — shipped `commands/refactor-tests.md` +
`skills/refactor-tests/SKILL.md` (acceptance suite: `skills/refactor-tests/self-test/` +
`acceptance.feature`). Evolution: `docs/evolution/2026-07-02-refactor-tests.md`. The test-diff
critic remains deferred to slice 04 (the "future pre-screen seam" in the diagram below is accurate).

**Pattern:** modular prose skill, ports-and-adapters. Loop core = the skill; adapters = git,
filesystem, test runner (all via Bash), and the human-approval port (AskUserQuestion + editor
review). See feature-delta.md `DESIGN / [REF]` sections for the full decision record (DD1–DD8),
component decomposition, and Reuse Analysis.

**Safety oracle:** human approval per diff (DISCUSS D2). A green suite is only a secondary
sanity check; the automated test-diff critic is deferred (slice 04, ADR-002).

### C4: System Context

```mermaid
graph TB
    Tess["Tess — developer / test maintainer<br/>(reviews diffs in her IDE)"]
    RT["phil:refactor-tests<br/>(command + skill)"]
    Git[("git repository")]
    Runner["Test runner<br/>(pytest / npm test / ...)"]
    IDE["IDE / editor<br/>(diff review surface)"]

    Tess -->|"runs /phil:refactor-tests"| RT
    RT -->|"applies move, commits/reverts"| Git
    RT -->|"runs suite (baseline + sanity)"| Runner
    RT -->|"pauses for approval"| Tess
    Tess -->|"reviews uncommitted diff"| IDE
    IDE -.->|"reads working tree"| Git
```

### C4: Container

```mermaid
graph TB
    subgraph plugin["phil plugin"]
        Cmd["commands/refactor-tests.md<br/>(thin loader)"]
        Skill["skills/refactor-tests/SKILL.md<br/>(loop + D5 taxonomy + gate)"]
        Detect["skills/shared/test-runner-detection.md<br/>(REUSE)"]
        Critic["agents/refactor-tests-critic.md<br/>(DEFERRED — slice 04)"]
    end
    Backlog[(".test-refactoring-backlog.md")]
    Git[("git")]
    Runner["Test runner"]
    Human["Human approval<br/>(AskUserQuestion + IDE)"]

    Cmd --> Skill
    Skill --> Detect
    Skill -->|"--review writes"| Backlog
    Skill -->|"reads pending items"| Backlog
    Skill -->|"apply / commit / revert"| Git
    Skill -->|"run suite"| Runner
    Skill -->|"propose → pause"| Human
    Skill -.->|"future pre-screen seam"| Critic
```

### redesign-tests

A new `/phil:redesign-tests` command + `skills/redesign-tests/SKILL.md` — the behavior-CHANGING
sibling of `refactor-tests`. Same gated loop (never-on-red → propose → apply → suite sanity →
human gate → commit/revert → prune), but the allowed moves **deliberately change what tests
verify**: rewrite implementation-coupled / over-mocked / flaky assertions toward observable
behavior. Detection reuses `review-code`'s Priority 6 (Test Quality) taxonomy; the loop shape is
pattern-copied from `refactor-tests` (DESIGN Option A), not shared-module-extracted.

**Status:** DESIGNED (2026-07-06) — not yet implemented. DISCUSS + DESIGN complete;
`feature-delta.md` holds the full record.

**Pattern:** modular prose skill, ports-and-adapters (same as `refactor-tests`). Adapters = git,
filesystem, test runner (Bash), and the human-approval port.

**Safety oracle:** human approval per diff — the **sole** oracle (v1). Unlike `refactor-tests`, a
behavioral rewrite can change coverage, so the proposal carries a **coverage-equivalence claim**
(before/after "what it caught then / catches now") the human validates (ADR-004). An automated
coverage oracle (mutation / break-confirm) is deferred; the propose step reserves a pre-screen seam.

**Backlog:** `.test-redesign-backlog.md` — separate from `.test-refactoring-backlog.md` so the two
tools never collide.

See `docs/feature/redesign-tests/feature-delta.md` `DESIGN / [REF]` sections for DDD1–DDD9,
component decomposition, Reuse Analysis, and the C4 Container diagram.

### phil-work

A new `/phil:work` command + `skills/work/SKILL.md` — a **wave-based orchestrator** for invisible
(non-user-facing) technical initiatives: refactoring, re-architecting, cleanup, migrations,
dependency/perf work. It is the invisible-work sibling to nwave. It follows the plugin's
command→skill split and ports-and-adapters pattern, but its distinguishing move is that it is a
**general contractor**: it discusses, plans, and sequences waves, then **delegates execution to
the tactical skills already in the plugin**, inheriting each delegate's gate rather than building
its own.

**Status:** IMPLEMENTED (2026-07-13) — shipped `commands/work.md` + `skills/work/SKILL.md` across
5 thin slices (walking skeleton first). Acceptance suite: `skills/work/self-test/` (7 fixtures) +
`skills/work/acceptance.feature`. Evolution: `docs/evolution/2026-07-13-phil-work.md`. `feature-delta.md`
holds the full DISCUSS+DESIGN+DISTILL record; DELIVER progress in `docs/feature/phil-work/deliver/`.
One v1 boundary (UI-1): non-test prose uses the ADR-002 human-approval gate directly (no dedicated
non-test-prose delegate yet).

**Pattern:** modular prose skill, ports-and-adapters. **Substrate (ADR-005):** hybrid — a prose
spine (`skills/work/SKILL.md`) owns the interactive, non-safety-critical flow (FRAME → MAP →
SAFETY-NET setup → sequencing → VERIFY → decision trail); each EXECUTE wave delegates to the
tactical skill that already owns the correct gate.

**Verification spine (DISCUSS D4/D9):** preservation floor (always) + declared initiative goal
(per initiative). The preservation oracle is **artifact-aware and inherited from the delegate** —
code → `refactor-loop`'s deterministic Workflow cage; prose (skills/rules/agents) →
`refactor-tests`/`redesign-tests` human-approval diff (ADR-002). `/phil:work` adds only the
cross-wave sequencing gate: any delegate failure stops the sequence and leaves the tree last-good.

**Documentation trail (ADR-006):** working trail under `docs/work/<initiative>/`
(frame, roadmap, decisions, progress); durable evolution summary migrates to
`docs/evolution/<date>-<initiative>.md`.

#### C4: System Context

```mermaid
graph TB
    Quinn["Quinn — codebase steward<br/>(frames goal, approves roadmap, reviews prose diffs)"]
    Work["phil:work<br/>(command + orchestrator skill)"]
    Delegates["Tactical skills<br/>(refactor-loop, refactor-tests, redesign-tests,<br/>refactor, extract-method, clean-comments, review-code, spirit-walk)"]
    Git[("git repository")]
    Runner["Test runner<br/>(pytest / npm test / self-test harness)"]
    IDE["IDE / editor<br/>(prose diff review)"]
    Trail[("docs/work/&lt;initiative&gt;/ + docs/evolution/")]

    Quinn -->|"runs /phil:work '&lt;initiative&gt;'"| Work
    Work -->|"delegates each wave"| Delegates
    Delegates -->|"apply / commit / revert"| Git
    Delegates -->|"run suite (code oracle)"| Runner
    Delegates -->|"pause for diff approval (prose oracle)"| Quinn
    Quinn -->|"reviews prose diff"| IDE
    Work -->|"FRAME confirm, roadmap approval, VERIFY"| Quinn
    Work -->|"writes frame/roadmap/decisions/progress + evolution"| Trail
```

#### C4: Container

```mermaid
graph TB
    subgraph plugin["phil plugin"]
        Cmd["commands/work.md<br/>(thin loader)"]
        Skill["skills/work/SKILL.md<br/>(orchestrator: FRAME · MAP · SAFETY-NET · EXECUTE · VERIFY)"]
        SelfTest["skills/work/self-test/<br/>(safety-behavior fixtures — regression gate)"]
        Detect["skills/shared/test-runner-detection.md<br/>(REUSE)"]
        RL["refactor-loop<br/>(REUSE — code oracle: Workflow cage)"]
        RT["refactor-tests / redesign-tests<br/>(REUSE — prose oracle: human diff, ADR-002)"]
        Other["refactor · extract-method · clean-comments · review-code · spirit-walk<br/>(REUSE — per-wave delegates / MAP survey)"]
    end
    Trail[("docs/work/&lt;initiative&gt;/")]
    Evol[("docs/evolution/")]
    Git[("git")]
    Runner["Test runner"]
    Human["Human port<br/>(AskUserQuestion + IDE)"]

    Cmd --> Skill
    Skill --> Detect
    Skill -->|"MAP survey"| Other
    Skill -->|"EXECUTE: code wave"| RL
    Skill -->|"EXECUTE: prose wave"| RT
    Skill -->|"EXECUTE: targeted moves"| Other
    Skill -->|"FRAME / roadmap / VERIFY gates"| Human
    Skill -->|"frame·roadmap·decisions·progress"| Trail
    Skill -->|"evolution summary at VERIFY"| Evol
    RL -->|"suite gate"| Runner
    RL --> Git
    RT -->|"human gate"| Human
    RT --> Git
    Skill -. "changed when skill changes" .-> SelfTest
```

### ADRs

- [ADR-001](adr-001-refactor-tests-reuse-boundaries.md) — refactor-tests: new command + reuse boundaries.
- [ADR-002](adr-002-human-approval-via-ide-diff.md) — refactor-tests: human-approval oracle via IDE diff review; critic deferred.
- [ADR-003](adr-003-redesign-tests-reuse-boundaries.md) — redesign-tests: new command + reuse boundaries (Option A).
- [ADR-004](adr-004-redesign-tests-coverage-equivalence-claim.md) — redesign-tests: coverage-equivalence claim at the human gate; automated oracle deferred.
- [ADR-005](adr-005-phil-work-hybrid-substrate-delegated-gates.md) — phil-work: hybrid substrate (prose spine + delegate-owned gates); no re-implemented gating.
- [ADR-006](adr-006-phil-work-documentation-namespace.md) — phil-work: `docs/work/<initiative>/` trail + evolution summary to `docs/evolution/`.
