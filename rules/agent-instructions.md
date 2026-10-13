---
paths:
  - "**/CLAUDE.md"
  - "**/CLAUDE.local.md"
  - "**/AGENTS.md"
  - "**/SKILL.md"
  - "**/.claude/rules/**/*.md"
  - "**/.claude/agents/**/*.md"
  - "**/.claude/commands/**/*.md"
---

# Agent Instructions

Guidelines extracted from Randal L. Schwartz's *Synthetic Scars* series (DEV Community, September–October 2026) — <https://dev.to/randalschwartz/series/44156>. Mike Mol's `nemik` is named where it applies.

This rule owns **how an instruction is phrased and where it lives** in any file a model reads as instructions: `CLAUDE.md`, `AGENTS.md`, a skill, an agent, a command, a rule. `claude-md.md` owns what belongs in `CLAUDE.md` and how that file is laid out; `writing.md` owns the sentences. `/phil:harden-instructions` applies this rule to a file.

---

### Core Philosophy

> **A rule the model must remember is a rule the model can forget.**

Compaction, a long context or a pushy user can wear away any rule that lives in prose. Put each rule where the model cannot lose it. Phrase whatever must stay in prose so the model recalls its meaning instead of inventing one.

---

### Where a Rule Lives

Place each rule on the highest tier it can reach.

| Tier | The rule lives in | It holds |
|---|---|---|
| **Enforce** | A hook, script, test, linter or CI check that refuses the violation | By construction |
| **Derive** | State on disk or in the forge, read fresh at each start | Across compaction and handoff |
| **Name** | A formalism the model already knows, written in the prompt | Often; the model recalls the semantics |
| **State** | An affirmative sentence in the prompt | When the model reads, retrieves and obeys it |

- **Enforce what a machine can check.** The model cannot argue past a guard the runtime fires. A prompt that holds 98% of the time fails twice in a hundred runs.
- **Prove the check before cutting the prose.** Replay the input that motivated the rule and watch the check refuse it. Then cut the prose to one line naming the rule and the check. Mike Mol's `nemik` deletes a prose rule only after its hook refuses a replayed bad payload.
- **Derive position from the world.** The model reads the branch, the tree, the open PR and the files on disk to learn where it stands, never a remembered step number.

---

### Name the Protocol

When a rule must live in prose, name a protocol the model learned in training instead of describing one it met seconds ago.

| Prose | Name instead |
|---|---|
| "Do step 1, then 2, loop back if tests fail" | Makefile: `target: prerequisites` |
| "Keep a progress file updated" | `init.d` drop-ins with `Key: Value` headers |
| "Format your output strictly as…" | An EBNF grammar, JSON Schema or `Key: Value` lines |
| "Handle edge cases" | `@requires` / `@ensures` / `@invariant` |
| "Don't leave the build half-broken" | Two-phase commit: prepare, vote, commit or abort |
| "Try a couple of times, then ask me" | Circuit breaker: `CLOSED → OPEN` after `k = 2` failures |
| "Figure out why this test fails" | `git bisect` |
| "Use subagents; keep the context clean" | `fork()` / `wait()` |
| "Break this into clean commits" | `[PATCH k/N]` series |

A canonical form is **familiar, precise and short** at once. The evidence does not separate the three, so write all three: "a couple of times" becomes `k = 2`.

Invent no bracketed tags, sigils or private shorthand (`[CRITICAL_GATE_4]`). An invented tag forces the model to simulate an interpreter for a language it has never seen.

---

### State Reflexes, Not Prohibitions

- **Write the invariant that must hold.** "Check the widget is mounted before any async callback updates state" beats "don't update disposed widgets."
- **Name the alternative beside any prohibition that stays.** "Write `Refs #22`, never `Fixes #22`, when the commit does not fix it." A bare "never X" puts X in context and offers nothing in its place.
- **Ask a question that leads somewhere.** "What happens to `_sub` if the network reconnects twice in 50 ms?" leads to the right fix. "Do not touch other code" draws attention to other code.

---

### Rule Anatomy: Reflex, Trap, Wound

Give a non-obvious rule three parts, in this order:

1. **Reflex** — the invariant, one imperative line.
2. **Trap** — the tempting shortcut it blocks, one clause.
3. **Wound** — the incident that earned it, one line with a date or a link.

The reflex leads because it is the instruction. The wound justifies the rule and keeps it from looking arbitrary. History beyond one line belongs in git, an ADR or `docs/`; link to it.

Write a rule after the incident that earns it, unless its reason is obvious.

---

### Graphs, Not Checklists

- **Write a workflow as targets and prerequisites.** Each target names the condition that proves it is done: a file on disk, a green check, an exit code. The model locates itself by finding the first unmet target.
- **Write no routing prose.** "If the bot comments after step 9, jump to step 12.2" asks the model to hold a program counter across a hundred tool calls. A target reopens when its condition fails: a dirty tree reopens `commit` with no routing at all.
- **Give each human gate its own target**, with one readiness prerequisite beside the approval: `land: ready-to-land human-approval`. A gate buried fifth in a list of four mechanical checks gets ticked, not honored.

---

### State by Write Discipline

Split working state by how it changes, not by topic:

| File | Written | Holds |
|---|---|---|
| Laws | Once | Invariants and safety rules |
| Lessons | Append-only | What went wrong, in reflex/trap/wound form |
| Position | Overwritten | Where the work stands now |

Load laws first. Keep invariants out of anything a summarizer or the model rewrites.

---

### Separate the Maker from the Judge

- **Have another party verify a gate.** A script, a test or a fresh agent that never saw the maker's reasoning. An agent never notarizes its own work.
- **Give a reviewer's output a failing scenario, not a patch.** Inputs, ordering, timing. Leave room for "already handled, here's why."
- **Give an agent a way to decline.** Let it verify before it promises, then counter-offer or decline. An agent that commits at the first token invents whatever it committed to.

---

### Budget

Every line in an always-loaded file costs context in every session. Cut what the model infers from the code, what a check enforces, and history the reflex does not need. A file that grows by one rule per incident ends as the rulebook nobody follows.

---

### Evidence

Treat these as practice, not measured law. One controlled benchmark backs **Name the Protocol**: 1,680 paired trials, Gemini models only, built and graded by the author. It confounds familiarity with precision and length. The other sections rest on one practitioner's field log of 50 to 150 tickets with no baseline. Cite the series for its architecture and its incidents, and quote none of its percentages as effect sizes.

---

### Quick Reference Checklist

- [ ] Does a hook, script or test enforce this rule? Then is the prose one line naming it?
- [ ] Does the model learn its position from disk or forge state?
- [ ] Could a known formalism replace this paragraph?
- [ ] Does each rule state what holds, not what to avoid?
- [ ] Does each non-obvious rule lead with its reflex and carry a one-line wound?
- [ ] Is each workflow a set of targets, free of "go back to step N"?
- [ ] Does someone other than the maker verify each gate?
