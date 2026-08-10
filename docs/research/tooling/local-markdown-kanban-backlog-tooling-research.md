# Research: Local, Markdown-Backed Kanban/Backlog Tooling for AI-Agent Workflows in VS Code

**Date**: 2026-08-10 | **Researcher**: nw-researcher (Nova) | **Confidence**: Medium-High | **Sources**: 22 cited (7 primary local-filesystem observations, 15 web)

---

## ⚠ FINDINGS SUPERSEDED BY EXECUTION — 2026-08-10, same day

**Read this before the Executive Summary.** This document's central limitation was that
**nothing was installed or run** (its own Gap G11). Backlog.md and the VS Code extension were
then installed and exercised. Several findings below are wrong, and the ranked recommendation
no longer reflects the decision taken.

| This document says | Execution showed |
|---|---|
| `antopolskiy/kanban-md` is a live contender; the `--mouse` test "decides between Combinations 1 and 3" | **Still stands — and C6's evidence was right.** An initial attempt to eliminate it on the docs landing page (which advertises *"Keyboard-driven navigation"* and omits mouse support) was **wrong**: the repo documents `kanban-md tui --mouse`, *"Hold a card, drag to another visible column, and release,"* with both input styles mixable. **G5 remains open** — whether that drag works in VS Code's *integrated terminal* is still the untested question. Two practical frictions do stand: it is Go and there is no `go` toolchain on this machine (Homebrew or a prebuilt binary needed), and it is a terminal app competing with the terminal used for git and tests |
| "R9's groom tier is missing from every markdown tool" | **False for Backlog.md.** A real `backlog/drafts/` folder, `--draft`, `task demote`, and a Drafts board view. Two drafts were promoted to tasks in the trial |
| R9's purge step unaddressed | **Covered** — `cleanup`, `task archive`, `task complete`, plus an Archived view |
| R8 "must be built. Nothing satisfies it" | **Too strong for task-scoped state.** `--plan`, `--notes`, `--modified-file`, `--doc`, `--ref` exist; a trap ledger, anti-instruction and supersession marker round-tripped verbatim through `## Implementation Notes`. The residue is *repo-scoped* payloads only |
| "the traps ledger … have no home in Backlog.md's schema" | Half right. No *dedicated field*, but they survive as prose. The real distinction is task-scoped (fits) vs repo-scoped (does not) |
| G2 — Backlog.md's last-publish date unmeasured | **Resolved:** v1.50.1 published 2026-08-10T07:49Z; package created 2025-06-13 |
| G5 — does `kanban-md --mouse` drag work in VS Code's terminal? | **STILL OPEN.** Mouse drag is documented in the repo; behaviour inside VS Code's integrated terminal is untested. Not needed for the decision taken, since Backlog.md was verified by execution first |
| G9 — no on-disk Claude Code task data located | **Confirmed:** `~/.claude/tasks/{session-uuid}/` holds only `.lock` and `.highwatermark`. R7 failure stands |
| G11 — no candidate installed or executed | **Discharged for Backlog.md.** A drag is a **3-line frontmatter diff**; draft→task promotion registers as a **git rename**; the extension writes the same format as the CLI, with no reformatting |

**Verified by execution:** R1, R2, R3, R5, R6, R7, R9 on Backlog.md v1.50.1 +
`ysamlan.vscode-backlog-md` v0.3.9. R5 (card-face descriptions) rests on operator report, not
measurement.

**Two adoption risks found only by running it**, neither documented above:
1. `backlog init` appends to an existing `CLAUDE.md` **non-destructively** (tested against a file
   with content to lose), but injects a `<CRITICAL_INSTRUCTION>` ordering the agent to run
   `backlog instructions overview` **before every user request**. Use `--agent-instructions none`.
2. `remoteOperations` and `--check-branches` default **on**, scanning local *and remote* branches
   on every board load — a latency risk on large repos.

**Decision actually taken (2026-08-10):** adopt Backlog.md for the board; **do not build a plugin
yet.** Ranking Combination 1 first is superseded — the tool already ships agent integration (CLI
`--plain`/`--json`, MCP, `CLAUDE.md` injection) and the files are plain markdown an agent edits
directly, so no plugin is needed for R1-R7 or R9. Pilot one real feature first, then let observed
friction specify any tooling. Two candidates surfaced afterwards: a **push/pop pair for
interruption stacks** (better defined than the repo-brief generator recommended below) and a
repo-scoped brief. Recommended pilot target: the `beatrix-vendor-form-autofill` worktree.

**What still stands:** the compliance matrix's structure and the R1+R2 / R3+R7 column readings;
the disposal of Obsidian, `taskell` (archived 2024-03-25), the server/desktop class, and
GitHub-backed options; the L5 payload analysis; and the core finding that the repo-scoped third of
`CONTEXT.md` has no analog in any tool assessed.

---

## Executive Summary

**Adopt for the board, build for the handoff.** Something worth adopting does exist — **Backlog.md** (MIT, 6.4k★, npm v1.50.1) stores one markdown file per task in `backlog/tasks/`, is explicitly built for AI agents (MCP auto-config for Claude Code, plus an `AGENTS.md`), and has a **community VS Code extension** (`ysamlan.vscode-backlog-md`, updated 2026-07-23) giving drag-and-drop kanban in-editor with no server. That covers R1-R7 and most of R9.

**R8 must be built. Nothing satisfies it.** Twelve candidate classes were assessed; not one stores resumable in-progress state at the fidelity the user's `CONTEXT.md` already reaches. The closest tools model *per-task plans* (Backlog.md), *dependency readiness* (beads) or *session snapshots* (`handoff`, 8★). None models what `CONTEXT.md` actually carries: a traps-already-paid-for ledger, explicit anti-instructions ("do not run the full suite to orient yourself"), supersession markers on its own stale sections, and falsifiable checkpoint values. The user's own file states the gap outright — the phase table "is the only place that tracks intra-DELIVER state, because `/nw-continue` structurally cannot."

**The decisive finding**: that grammar recurs across **three repos** (beatrix, basetwin, and this plugin's `continue.md`), so it is specifiable — therefore templatable and gate-able, in the user's existing plugin, using the `SessionStart` hook already wired in `~/.claude/settings.json`.

**Two corrections to the brief's premises.** Claude Code's Task tools are *not* ephemeral — they persist to `~/.claude/tasks/{uuid}/` — but they fail R7 decisively, being outside the repo and uncommittable. And `taskell` is **archived (2024-03-25)**; treat it as dead.

**Confidence: Medium-High.** What would change it: (1) hands-on trial of `ysamlan.vscode-backlog-md`, whose 361 installs and 17★ make it the thinnest link; (2) resolving whether Backlog.md's task schema can carry the trap/anti-instruction payloads without abuse.

## Research Methodology

**Search Strategy**: two parallel tracks. (a) **Local filesystem first** — `~/.claude/settings.json`, glob over `~/.claude/plugins/`, direct read of the installed `productivity` skill and its `dashboard.html`, the user's plugin tree, and the three `CONTEXT.md`/`feature-ideas.md` artifacts named in the brief. These are primary observations and the highest-authority evidence available for both the installed-tooling question and the R8/R9 requirements. (b) **Web** — targeted searches per candidate seed, then direct fetch of each project's own repo/marketplace page, plus discovery searches ("markdown kanban VS Code", "Claude Code session handoff") which surfaced four candidates absent from the seed list (`vscode-agent-kanban`, `kanban-md`, and the handoff-plugin class).

**Source Selection**: official first-party docs (`code.claude.com`), registries (`registry.npmjs.org`, `marketplace.visualstudio.com`) for existence/version/date/install claims only, and project repos on `github.com` (medium-high) for self-described capability. Per orchestration ruling, README capability claims are treated as authoritative for *what a project claims to do* and never for *whether it works well*.

**Quality Standards**: 3 sources/claim ideal, 2 acceptable, 1 authoritative minimum. Cells in the compliance matrix are marked `?` where unverified rather than inferred. Every capability claim traceable to only the project itself is labelled with its confidence, and quality claims sourced solely from enthusiast blogs are explicitly discounted.

**Known methodological limitation**: no candidate was installed or run. Every capability claim is documentary. The matrix therefore records *claimed* capability; four cells are flagged as needing a five-minute empirical test (Gaps G1, G3, G5, G7). ⚠ **SUPERSEDED same day for Backlog.md and its VS Code extension — both were installed and exercised; see the supersession block at the top of this file. This limitation still applies to every other candidate.**

## Evaluation Criteria (Requirements)

| # | Requirement | Kind |
|---|---|---|
| R1 | Visual kanban board with click-and-drag card movement | Hard |
| R2 | Runs fully locally in VS Code with no server process required | Hard |
| R3 | Markdown as the underlying storage format | Strong preference |
| R4 | An AI agent (Claude Code, via file edits or CLI) can read and write the backlog | Hard |
| R5 | High-level overview showing cards with brief descriptions | Hard |
| R6 | Separate detailed-notes view for an individual story | Hard |
| R7 | State is easy and clean to commit to git (text, diffable, low merge conflict) | Hard |
| R8 | Can store exact state of an in-progress story to resume seamlessly in a new agent session | Hard |
| R9 | Supports a groom → pick → track → purge/prune loop | Hard |

## Compliance Matrix

Legend: ✅ satisfied · ⚠️ partial · ❌ fails · ? unverified (see Knowledge Gaps). **R3 is a strong preference; all others are hard.**

| Candidate | R1 board+drag | R2 local in VS Code, no server | R3 markdown | R4 agent r/w | R5 overview+desc | R6 detail view | R7 git-clean | R8 resumable WIP state | R9 groom→pick→track→purge | Maintained? |
|---|---|---|---|---|---|---|---|---|---|---|
| **Backlog.md + `ysamlan.vscode-backlog-md`** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⚠️ | ✅/⚠️ | ✅ ext. 2026-07-23 |
| Backlog.md, first-party board only (`backlog browser`) | ✅ | ❌ server on 127.0.0.1 | ✅ | ✅ | ✅ | ✅ | ✅ | ⚠️ | ✅/⚠️ | ✅ v1.50.1 |
| `holooooo.markdown-kanban` (VS Code) | ✅ | ✅ | ✅ | ✅ | ✅ | ⚠️ same file | ⚠️ single file | ❌ | ⚠️ | ✅ 2026-07-23 |
| `AppSoftwareLtd.vscode-agent-kanban` | ✅ | ✅ | ✅ | ⚠️ Copilot-bound | ✅ | ✅ | ✅ | ⚠️ | ⚠️ | ⚠️ early (59★) |
| `antopolskiy/kanban-md` | ⚠️ TUI mouse | ⚠️ terminal not panel | ✅ | ✅ | ✅ | ✅ | ✅ | ⚠️ | ✅/⚠️ | ✅ (187★) |
| `productivity` `task-management` (installed) | ✅ | ⚠️ external Chromium | ✅ | ✅ | ⚠️ | ❌ | ✅ | ❌ | ⚠️ | ✅ v1.3.1 |
| beads (`bd`) | ? | ⚠️ no server, not VS Code | ❌ SQLite+JSONL | ✅ | ? | ❌ | ⚠️ generated | ⚠️ DAG readiness | ⚠️ | ✅ active |
| Claude Code built-in Task tools | ❌ | ✅ | ❌ | ✅ | ⚠️ | ❌ | **❌ `~/.claude/tasks/`** | ⚠️ | ⚠️ | ✅ first-party |
| Session-handoff plugins (`handoff`, `claude-code-handoff`, …) | ❌ | ✅ | ✅ | ✅ | ❌ | ⚠️ | ✅ | ⚠️ **best available** | ❌ | ⚠️ 8–12★ |
| Obsidian Kanban plugin | ✅ | ❌ separate desktop app | ✅ | ✅ | ✅ | ? | ✅ | ❌ | ⚠️ | ✅ (4.5k★) |
| `taskell` | ❌ | ⚠️ TUI | ✅ | ⚠️ | ⚠️ | ❌ | ✅ | ❌ | ❌ | **❌ ARCHIVED 2024-03-25** |
| CCPM (`automazeio/ccpm`) | ✅ via GitHub | ❌ remote required | ❌ GH Issues | ✅ | ✅ | ✅ | ❌ | ⚠️ | ✅ best R9 shape | ✅ active |
| GitHub Projects / Issues + `gh` | ✅ | ❌ | ❌ | ✅ | ✅ | ✅ | ❌ | ❌ | ⚠️ | ✅ |
| Focalboard / Vikunja / Plane / Huly / Wekan | ✅ | ❌ server | ❌ database | ⚠️ API | ✅ | ✅ | ❌ | ❌ | ⚠️ | ✅ |
| Kanri (desktop) | ✅ | ❌ separate app | ❌ JSON (?) | ⚠️ | ✅ | ? | ⚠️ | ❌ | ⚠️ | ✅ |
| **User's current `CONTEXT.md` + `feature-ideas.md`** | ❌ | ✅ | ✅ | ✅ | ⚠️ tables | ✅ | ✅ | **✅ the benchmark** | ✅ | n/a (hand-run) |

**The single most important row in this table is the last one.** The user's hand-maintained pair scores ✅ on **eight of nine** requirements. It fails exactly one: **R1, the visual drag-drop board.** No candidate tool inverts that — every tool that satisfies R1 is weaker on R8, and usually on R9 too.

**Column readings**:
- **R1+R2 together** eliminate almost everything. Only four candidates satisfy both natively in a VS Code panel: `ysamlan.vscode-backlog-md`, `holooooo.markdown-kanban`, `AppSoftwareLtd.vscode-agent-kanban`, and (with a browser caveat) the already-installed `productivity` dashboard.
- **R3 + R7 together favour file-per-task** over single-file boards. Backlog.md, vscode-agent-kanban and kanban-md are file-per-task; holooooo.markdown-kanban and the `productivity` skill are single-file.
- **R8 has no ✅ in any tool row.** This is the finding, developed below.
- **R9's groom tier is missing from every markdown tool.** Only CCPM models an idea/PRD tier above tasks — and it fails R2/R3/R7. ⚠️ **SUPERSEDED 2026-08-10: false for Backlog.md**, which has a physically separate `backlog/drafts/` folder, `--draft` on create, `task demote` to send a task back, and a Drafts board column. Verified by execution — two drafts were promoted to tasks, each registering in git as a rename.

## Per-Candidate Findings

### C1. Backlog.md (`backlog.md` on npm) — **strongest single candidate**

| Attribute | Value | Source |
|---|---|---|
| Repo | github.com/MrLesk/Backlog.md | [1] |
| Stars | 6.4k | [1], accessed 2026-08-10 |
| npm latest | **1.50.1** | registry.npmjs.org [2], accessed 2026-08-10 |
| License | MIT | [1], [2] |
| Storage | one plain `.md` file per task under `backlog/tasks/`, plus `backlog/config.yml`, `backlog/milestones/*.md` | [1], [3] |
| Maintenance | actively maintained; version 1.50.1 implies a high release cadence. **Exact last-publish date not captured — see Gap G2** | [2] |

**Evidence — storage (R3, R7)**: "every task is a plain `.md` file in your repo". Default folder `backlog/` (also `.backlog/` or custom via `backlog.config.yml`). Task files carry frontmatter/metadata: description, **acceptance criteria**, milestones, dependencies, status. Confirmed independently by the VS Code extension repo, which states it reads `backlog/tasks/*.md` and `backlog/config.yml`. Two independent sources agree on layout. **Confidence: High.**

**Evidence — board (R1, R2)**: three separate view surfaces, and the R2 answer differs by which one you use.
1. `backlog board` — terminal kanban. No drag-drop (keyboard/TUI).
2. `backlog browser` — "launches a local server on `127.0.0.1` with drag-and-drop kanban… The web server is **required** to run (`backlog browser`) for drag-and-drop functionality". **This is a server process. R2 fails for this path.**
3. **`vscode-backlog-md` VS Code extension** — "Kanban Board — Drag-and-drop tasks between status columns (Draft, To Do, In Progress, Done)"; "No [server]. The extension operates locally within VS Code and 'lives right in your repo,' requiring no external server infrastructure." Implemented as a VS Code **webview** (evidenced by `vite.webview.config.ts`, `tsconfig.webview.json` in the repo). **This is the path that satisfies R1 + R2 simultaneously.**

**The VS Code extension, assessed separately** (it is the load-bearing component for R1/R2):

| Attribute | Value | Source |
|---|---|---|
| Marketplace ID | `ysamlan.vscode-backlog-md` | [3] |
| Publisher | Yoni Samlan (community-built, **not** the Backlog.md maintainer) | [3], [1] |
| Version | 0.3.9 | [3] |
| Last updated | **2026-07-23** (18 days before access) | [3] |
| Installs | **361** | [3] |
| Rating | 5/5 from **1 review** | [3] |
| Repo | github.com/ysamlan/vscode-backlog-md — **17 stars**, 3 forks, 247 commits | [4] |
| CLI required? | No — "No standalone CLI is strictly required"; appears self-contained rather than a CLI wrapper | [3], [4] |

**Evidence — agent-manipulability (R4)**: three integration paths. (a) CLI: agents run `backlog instructions overview`. (b) **MCP connector**: "auto-configures Claude Code, Codex, Gemini CLI, Kiro via `backlog mcp start`"; agents read workflows at `backlog://workflow/overview`. (c) `AGENTS.md` written at `init` to instruct agents. Plus R4 is satisfiable trivially anyway, since tasks are markdown files Claude Code can Read/Edit directly. **Confidence: High** — this is the most explicitly agent-oriented candidate found.

**Evidence — R5/R6**: cards render on the board with configurable ID visibility and a details panel; the extension also offers "Rich Markdown rendering with Mermaid diagram support" and "Editor intelligence (autocomplete, hover tooltips)". Because each task *is* a markdown file, R6 is satisfied by simply opening the file.

**Evidence — R8 (partial)**: task fields include description, acceptance criteria, a project-wide-defaulted **"Definition of Done" checklist**, an **"Implementation plan"** ("agents write plans in tasks before coding; users approve"), **comments** with author attribution (`--comment`), and a **"final summary and completion notes"** field. It also enforces "a three-checkpoint review loop: spec review, plan review, then code review".

**Evidence — R9**: `backlog task create/edit/list/view/archive`, `backlog search`, `backlog milestone add/rename/remove`, `backlog config`. Prune is via `archive`: "No explicit prune/cleanup command documented; archiving tasks is the completion mechanism."

**Scoring rationale**:
- R1 ✅ *via the VS Code extension only*. ⚠️ if you constrain to first-party tooling — the first-party drag-drop board needs `backlog browser`.
- R2 ✅ via extension; ❌ via `backlog browser`.
- R3 ✅ one markdown file per task.
- R4 ✅ strongest of any candidate (MCP + CLI + AGENTS.md + plain files).
- R5 ✅ R6 ✅.
- R7 ✅ — file-per-task is the *best possible* shape for low merge conflict, since two agents editing different tasks touch different files. Contrast a single-file board, where every card move rewrites one file.
- R8 ⚠️ — "Implementation plan" + "Definition of Done" + comments is real structured in-progress state, and materially more than any other candidate offers. But it is *per-task planning*, not the repo-scoped orientation payload of Finding L5. No trap ledger, no falsifiable checkpoint values, no "what not to do first", no supersession markers.
- R9 ✅ for pick/track/purge (`archive`). ⚠️ for **groom** — no evidence found of an ungroomed-idea tier distinct from tasks; the "Draft" column is the nearest analogue.

**Risk to weigh (interpretation, not a sourced claim)**: R1+R2 depend entirely on a **361-install, 17-star, single-maintainer community extension** that is not maintained by the Backlog.md project. It is current (updated 2026-07-23), but this is the thinnest link in the chain. The mitigation is that the data lives in plain markdown owned by the 6.4k-star CLI, so extension abandonment costs a view, not the data. **This is a genuinely important asymmetry: adopting Backlog.md's *format* is low-risk; depending on that extension for the board is medium-risk.**

### C2. beads (`bd`) — right diagnosis of R8, wrong storage format

| Attribute | Value | Source |
|---|---|---|
| Repo | github.com/steveyegge/beads | [5] |
| Author | Steve Yegge (recognized industry figure) | [5], [6] |
| Language | Go | [5] |
| Storage | **SQLite** as working store, **JSONL** exported for git | [5], [6] |

**Evidence — storage (R3 ❌, R7 ⚠️)**: "When you run `bd create`, it writes to SQLite immediately, then exports to JSONL. When collaborators pull, the JSONL imports to their SQLite. No central server, git IS the database." JSONL is text and line-oriented, so it diffs and merges better than most binary or single-blob JSON — but it is **not markdown**, so R3 fails outright. R7 is ⚠️ rather than ✅: the committed artifact is generated, not authored, so the diff shows machine output and the SQLite file is a second source of truth that must not drift.

**Evidence — R8 (the interesting part)**: beads is explicitly built for exactly the problem the user has. It "solves what he calls the '50 First Dates' problem, where agents wake up with no memory of yesterday's work." It "models work as a directed acyclic graph (DAG) with explicit dependencies and priority levels, enabling agents to identify 'ready work' and maintain context across sessions without losing state." Hash-based IDs (`bd-a3f2`) exist specifically to prevent multi-agent collision — "avoiding 'both agents created bd-10' merge conflicts."
**Sources**: official docs [5]; Better Stack guide [6]; two independent practitioner writeups [7], [8]. **Confidence: High** that this is its stated purpose; **Medium** on how well it delivers (all quality claims trace to enthusiast posts, not to independent evaluation).

**Analysis**: beads' contribution to this decision is conceptual, not adoptable. Its R8 model is *dependency-graph readiness* — "which work is unblocked" — which is a genuinely different and narrower thing than the user's `CONTEXT.md`, which answers "what is the state of the world, what did I already learn the hard way, and what must you not do." beads would tell a fresh agent *which* card to pick. It would not tell it that `MSYS_NO_PATHCONV=1` is load-bearing or that the measured total must land just under Mains.

**Scoring**: R1 ? (no visual drag-drop board evidenced — see Gap G3), R2 ⚠️ (no server, but not in VS Code; official docs URL 404'd, see Gap G3), R3 ❌, R4 ✅ (CLI + MCP, purpose-built for agents), R5 ?, R6 ❌ (issue records, not per-story markdown documents), R7 ⚠️, R8 ⚠️ (best-in-class for *readiness* state; does not model the L5 payloads), R9 ⚠️.

**Disposition**: **rejected on R3 and R1.** Worth stealing from: hash-based IDs to kill merge collisions, and the DAG-of-ready-work idea for the pick step.

### C3. `holooooo.markdown-kanban` (VS Code) — single-file markdown board with agent launch

| Attribute | Value | Source |
|---|---|---|
| Marketplace ID | `holooooo.markdown-kanban` | [9] |
| Version | 2.0.0 | [9] |
| Last updated | **2026-07-23** | [9] |
| Installs | **2,012** | [9] |
| Rating | 4/5 from 3 reviews | [9] |
| Repo | github.com/holooooo/markdown-kanban | [10] |

**Evidence — storage (R3 ✅, R7 ⚠️)**: "Tasks use an indented list structure with attributes like `due: YYYY-MM-DD`, `tags: [tag1, tag2]`, `priority: high/medium/low`, and `workload` levels. Code blocks (``` md ```) contain detailed descriptions. The file organizes tasks under column headers (## To Do, ## Done, etc.)." So: **one markdown file, `##` headings as columns, list items as cards, fenced code blocks holding card detail.** This is the Obsidian-Kanban-family format.

**Evidence — R1, R2**: "supports dragging and dropping tasks between different columns"; "No server required; operates as a VS Code extension." Both hard requirements met natively in VS Code. **Confidence: High** (marketplace listing is authoritative for existence/version; drag-drop is corroborated by the repo).

**Evidence — R5, R6**: "tasks are collapsed by default" but expand "to show full details and multi-line descriptions." R5 ✅. R6 ⚠️ — detail is an *expanded card*, in the same file, not a separate document. Detailed notes on the scale of a 200-line slice spec would bloat the board file.

**Evidence — R4**: notable and unusual — "the extension includes 'Task Terminals' to 'start Codex, Claude Code, or another configured binary' from task cards. A reusable skill is available via GitHub." So it launches Claude Code *from* a card. Plus, being plain markdown, Claude Code can edit the file directly. R4 ✅.

**Evidence — R7 hazard**: no cross-file linking documented — "No mention of linking cards to other markdown files." Combined with single-file storage, **every card move rewrites the one board file**, which is the worst shape for merge conflicts among the markdown candidates and prevents pointing cards at `docs/feature/*/slices/*.md`. For a solo developer, merge conflict risk is low in practice; the inability to link to slice specs is the sharper problem.

**Scoring**: R1 ✅, R2 ✅, R3 ✅, R4 ✅, R5 ✅, R6 ⚠️, R7 ⚠️, R8 ❌ (no in-progress-state concept beyond column + description), R9 ⚠️ (columns give pick/track; groom and purge are manual editing).

### C4. `AppSoftwareLtd.vscode-agent-kanban` — closest in *intent* to what the user wants, wrong agent

| Attribute | Value | Source |
|---|---|---|
| Repo | github.com/appsoftwareltd/vscode-agent-kanban | [11] |
| Stars | 59 | [11] |
| Commits | 60 | [11] |
| Marketplace | published as `AppSoftwareLtd.vscode-agent-kanban` | [11] |
| Storage | **one `.md` per task with YAML frontmatter** in `.agentkanban/tasks/`, lane held in frontmatter | [11] |

**Evidence — purpose**: "A VS Code extension providing an integrated Kanban board with markdown-based `plan`/`todo`/`implement` workflow, designed to work with GitHub Copilot Chat for agent-assisted development."

**Evidence — R1, R2**: "Visual board with customisable lanes (default: Todo, Doing, Done). Drag-and-drop task cards between lanes." In-editor extension, no server. Both ✅.

**Evidence — R8 (the most relevant find besides beads)**: "The extension maintains context through **AGENTS.md sentinel sections that VS Code re-injects on every agent turn**." Agent interaction is via an `@kanban` chat participant with `/task` (select task), **`/refresh` (re-inject context)**, and `/worktree` (create isolated git branch). "Task-specific context persists through markdown files and AGENTS.md sections, supporting multi-turn conversations with automatic context recovery via `/refresh`."

**Analysis**: this is the only candidate found that treats *context re-injection into an agent* as a first-class feature — i.e. it takes R8 seriously as a mechanism, not just as a notes field. The mechanism (a sentinel-delimited region of `AGENTS.md` that the harness re-reads every turn) is directly transferable to a Claude Code design using `CLAUDE.md` or a `SessionStart` hook, which the user already has wired (Finding L3).

**Why it fails anyway (R4)**: the agent integration is bound to the **GitHub Copilot Chat** participant API (`@kanban`), which Claude Code does not implement. Claude Code could still Read/Edit `.agentkanban/tasks/*.md` directly, so R4 is ⚠️ not ❌ — the *files* are agent-manipulable, but the *designed* agent path is unavailable and the `/refresh` context-reinjection machinery would not fire for Claude Code.

**Maturity concern**: 59 stars, 60 commits, and the repo carries a self-noted staleness marker — "A note mentions '2026-03-12' regarding video updates needed." No release date confirmed. **Flag: early-stage, ~5 months since the referenced note.** See Gap G4.

**Scoring**: R1 ✅, R2 ✅, R3 ✅ (md + frontmatter, file-per-task), R4 ⚠️ (Copilot-bound; files still editable), R5 ✅, R6 ✅ (file-per-task), R7 ✅ (file-per-task), R8 ⚠️ (real re-injection mechanism, but Copilot-only and no L5-grade payload schema), R9 ⚠️ (plan/todo/implement lanes; no groom tier, no purge command evidenced).

### C5. `productivity@knowledge-work-plugins` `task-management` skill — **already installed**

See Finding L1 for the primary-source detail. Additional finding on R2 from direct inspection of `dashboard.html`:

**Evidence (R2)**: the dashboard uses the **File System Access API** — `window.showOpenFilePicker()` at line 2438 to acquire the `TASKS.md` handle, `window.showDirectoryPicker()` at line 2576 for the memory directory, and `handle.createWritable()` / `.write()` / `.close()` at lines 1856-1859, 2463-2465, 3026-3068 to save. There is **no `fetch()` to a local server and no `XMLHttpRequest`**.
**Source**: `/home/philvanevery/.claude/plugins/cache/knowledge-work-plugins/productivity/1.3.1/skills/dashboard.html`, accessed 2026-08-10. Primary source. **Confidence: High.**

**Analysis**: this confirms **no server process is required** — the file can be opened from disk and writes go straight to `TASKS.md`. Two costs follow from the API choice, and both are interpretations of the code rather than documented limitations: (a) the File System Access API is **Chromium-only** (unsupported in Firefox, and `showDirectoryPicker`/`createWritable` unsupported in Safari), and (b) it requires a **user gesture to grant the handle**, so each browser session likely begins with a manual file-pick. Most importantly for R2 as written: **it is a browser page, not a VS Code panel.** If "in VS Code" is strict, R2 is ⚠️ at best. VS Code's Simple Browser cannot serve `file://` with File System Access permissions, so this would run in an external Chrome window alongside the editor.

**Scoring**: R1 ✅ ("Supports drag-and-drop reordering of tasks and sections"), R2 ⚠️ (no server, but external Chromium browser rather than in-editor), R3 ✅ (`TASKS.md`), R4 ✅ (plain markdown in cwd; the skill itself is written for the agent to edit), R5 ⚠️ (one-line tasks + sub-bullets; no real card descriptions), R6 ❌ (no per-story document), R7 ✅ (single small markdown file), R8 ❌ (a checkbox is the entire state model), R9 ⚠️ (`Someday`→`Active`→`Done` is a pick/track/prune loop at *commitment* grain; no groom step, and prune is time-based not ship-based).

**Disposition**: **useful as an existence proof, not adoptable as the system of record.** It proves that markdown + drag-drop + agent-writable + no-server is achievable in ~3000 lines of a single HTML file. That is a meaningful data point for the build side of the decision.

### C6. `antopolskiy/kanban-md` — built for exactly this use case, but TUI-only

| Attribute | Value | Source |
|---|---|---|
| Repo | github.com/antopolskiy/kanban-md | [12] |
| Stars | **187** | [12] |
| Commits | 343 | [12] |
| License | MIT | [12] |
| Tagline | "File-based kanban board for autonomous agentic loop. CLI and TUI for multi-agent workflows. Skills included." | [12] |
| Storage | **markdown + YAML frontmatter, one file per task in `tasks/`**, plus `config.yml` | [12] |

**Evidence — R1/R2 (the deciding cells)**: "Terminal UI only. The project includes `kanban-md tui` for interactive navigation, but no GUI or VS Code extension." Drag-drop *does* exist: "Supported in TUI with `--mouse` flag. Users can 'hold a card, drag to another visible column, and release' to move tasks between statuses."

**Analysis (interpretation, flagged as such)**: this is the most interesting borderline case in the matrix. A TUI runs in VS Code's integrated terminal, so mouse drag-drop inside VS Code is *technically* achievable with no server — which is a literal satisfaction of R1 and R2. But it is not a VS Code panel; it cannot be a sidebar view, it competes with the terminal you need for git and tests, and mouse capture in the integrated terminal is a known source of friction. **I score R1 ⚠️ and R2 ⚠️ rather than ✅, and note this is a judgement call the user may score differently.** Whether `--mouse` drag actually works in the VS Code integrated terminal specifically is **[Gap G5]** — it is a five-minute empirical test, not a documentation question.

**Evidence — R4**: "CLI-based with installable skills. The tool provides 'command reference, decision trees, and workflows' via auto-triggered skill files that teach agents how to use the board. Agents interact by running CLI commands like `pick --claim` and `move`." It documents support for "Claude Code, Codex, Cursor, OpenClaw"; the repo carries `CLAUDE.md` and `.claude/skills` directories. R4 ✅ and notably idiomatic — it ships Claude Code *skills*, which is exactly the extension mechanism the user's own plugin uses.

**Evidence — R8/R9 field model**: tasks store "title, status, priority, assignee, tags, due dates, time estimates, class of service, parent/dependency relationships, **blocked status with reasons**, **claim ownership**, **creation/update/started/completed timestamps**, and body text." The `pick --claim` verb plus claim-ownership and `started` timestamps is a real *work-in-progress* model — better than most — and `blocked status with reasons` captures why something stalled. R9's pick and track steps are directly supported.

**Scoring**: R1 ⚠️ (TUI mouse drag only), R2 ⚠️ (no server, in-terminal not in-panel), R3 ✅, R4 ✅, R5 ✅, R6 ✅ (file-per-task), R7 ✅ (file-per-task), R8 ⚠️ (claim/started/blocked-reason is genuine WIP state; no L5 payloads), R9 ✅ for pick/track, ⚠️ for groom/purge (no evidence of an idea tier or archive command — **[Gap G6]**).

**Disposition**: **near-miss, and the best fallback if R1 is relaxed.** If the user would accept a TUI board, this is arguably a better fit than Backlog.md because its agent-skill integration matches the user's plugin idiom and it does not depend on a 361-install third-party extension. Its weakness is 187 stars against Backlog.md's 6.4k.

### C7. `taskell` — **DEAD. Definitively disposed.**

**Evidence**: "**Repository Status: Archived as of March 25, 2024. The repository is read-only.**" Maintainer notice: "I'm going to be taking a break from development of Taskell for a while. Trying to do it alongside my day job was proving a bit much." 1.8k stars, BSD-3-Clause.
**Source**: github.com/smallhadroncollider/taskell [13], accessed 2026-08-10. Authoritative (the repo's own archive flag).
**Confidence: High.**

**Format worth recording** even though the tool is dead, since it corroborates the de-facto markdown-kanban convention: configurable syntax, default title format `##`, default task format `-`, default sub-task format `    *`.

**Disposition**: **rejected on maintenance — unmaintained for ~2 years and 5 months at access date, and formally archived.** Per the source-discipline rule, this is flagged in the matrix as unmaintained. Also fails R1 (no drag-drop) and R2-in-VS-Code.

### C8. Obsidian Kanban plugin — the reference format, not an adoptable tool

| Attribute | Value | Source |
|---|---|---|
| Repo | github.com/mgmeyers/obsidian-kanban | [14] |
| Stars | **4.5k** | [14] |
| License | GPL-3.0 | [14] |

**Evidence gap**: the GitHub landing page did not disclose the storage format, drag-drop support, release version/date, or archive feature — it defers to separate plugin documentation. **I did not verify these from a primary source.** See **Gap G7**.

**What is established**: it is markdown-backed and widely adopted (4.5k stars). Its file convention (`##` headings as lanes, `- [ ]` list items as cards) is corroborated *indirectly* by the fact that both `holooooo.markdown-kanban` [9] and the archived `taskell` [13] use the same shape, and by an Adafruit blog piece describing "A Markdown-powered kanban task board for VS Code **and Obsidian**" [15] — i.e. cross-tool format compatibility is a thing people build for. **Confidence: Medium** on the format specifics; I am not citing an authoritative source for the exact Obsidian Kanban syntax.

**Disposition as requested — R2 fails.** Obsidian is a separate Electron desktop application. Running it against the repo folder alongside VS Code is possible (R3 ✅, R7 ✅, R1 ✅) but it is a second application with its own vault configuration, and "runs fully locally in VS Code" is false. GPL-3.0 is also worth noting if the user ever wanted to vendor any of it. **Retain as the format reference; reject as the tool.**

### C9. Disposed briefly — server/desktop apps and non-markdown stores

These were assessed against R2 and R3 only, per instruction not to spend depth. **Confidence: Medium** — dispositions rest on each project's own product category rather than on per-tool primary-source verification, which is proportionate to a disposal decision but is a stated limitation (**Gap G8**).

| Candidate | Category | R2 | R3 | Disposition |
|---|---|---|---|---|
| Focalboard | self-hosted/desktop board app (Mattermost lineage) | ❌ server or separate desktop app | ❌ database | Rejected |
| Vikunja | self-hosted to-do/kanban with API + web frontend | ❌ requires server | ❌ database | Rejected |
| Plane | self-hosted project management (Jira alternative) | ❌ requires server (multi-container) | ❌ database | Rejected |
| Huly | self-hosted all-in-one platform | ❌ requires server | ❌ database | Rejected |
| Wekan | self-hosted Meteor/MongoDB kanban | ❌ requires server + MongoDB | ❌ MongoDB | Rejected |
| Kanri | cross-platform **desktop** kanban (Tauri) | ❌ separate desktop app, not VS Code | ❌ JSON board files | Rejected |

**Note on Kanri specifically**: it is the closest of this group, since it is offline-first and needs no server — but it is a standalone desktop app storing JSON, so it fails R2-as-written and R3. **[Unverified in this research: Kanri's exact storage format. Flagged ? if the user wants it scored properly.]**

### C10. GitHub Projects / GitHub Issues — R2 fails, but note the counterpoint

**Disposition**: **rejected on R2** — the source of truth is a remote service. Offline work is impossible, and state is not a text file in the repo, so R3 and R7 also fail.

**The counterpoint worth recording**: agent-manipulability (R4) is *excellent* via the `gh` CLI, and `gh` is already on this machine's PATH (`/mnt/c/Program Files/GitHub CLI/`, per `~/.claude/settings.json`, accessed 2026-08-10). R1 and R5 are also strong (GitHub Projects' board view is mature and free). So the trade is precisely: **R4/R1/R5 excellence purchased with total R2/R3/R7 failure.**

**Cross-reference — CCPM builds exactly this trade.** `automazeio/ccpm` is "a project management system for Claude Code using GitHub Issues and Git worktrees for parallel agent execution", which "uses GitHub Issues as the single source of truth" and turns "ideas into PRDs, PRDs into epics, epics into GitHub issues, and issues into production code — with full traceability at every step". It claims "context preservation across sessions", "spec-driven development to prevent 'vibe coding'", and up to 12 concurrent agents per epic. It works with "Factory, Claude Code, Amp, OpenCode, Codex, Cursor".
**Sources**: [16] (repo), [17] (author's writeup — commercial interest noted: Ran Aroussi is affiliated with automaze), plus multiple forks (`kikoncuo/claude-code-pm`, `jeffersonwarrior/ccpm`, `Ninegd/ccpm`) which are **not** independent corroboration.
**Confidence: Medium** — the capability claims come from the project and its author only.

**Analysis**: CCPM's *workflow shape* (PRD → epic → issue → code, with a groom tier above the task tier) is the closest match to the user's R9 loop of anything found, and it independently validates the multi-tier promotion model derived in Finding L6. But its storage choice is the exact inverse of the user's requirement. **Rejected on R2/R3/R7; retained as workflow-design evidence.** Its "up to 12 concurrent agents" framing is also a poor fit for a solo developer and should be discounted as marketing rather than treated as a benefit.

### C11. Claude Code's built-in Task tools — **the expectation of ephemerality is WRONG, but they still fail R7**

This is a correction to a premise in the research brief, so it is documented at length.

**Evidence — the tools and their lifecycle (official, authoritative)**: "As of TypeScript Agent SDK 0.3.142 and Claude Code v2.1.142, sessions use the structured Task tools `TaskCreate`, `TaskUpdate`, `TaskGet`, and `TaskList` instead of `TodoWrite`." Lifecycle: "**Created** … as `pending`", "**Activated**: Claude sets the todo to `in_progress` when it starts the work", "**Completed**", "**Removed**: Claude deletes a todo it no longer needs by setting `status: "deleted"` in a `TaskUpdate` call".
Field shape: "`TaskCreate` input: `{ subject, description, activeForm?, metadata? }`. `TaskUpdate` input: `{ taskId, status?, subject?, description?, activeForm?, addBlocks?, addBlockedBy?, owner?, metadata? }`."
**Source**: [18] code.claude.com official docs, accessed 2026-08-10. **Reputation: High (official first-party).** **Confidence: High.**

**Evidence — persistence to disk (primary observation)**: `/home/philvanevery/.claude/tasks/` exists on this machine and contains two session-scoped directories — `d2f15440-2c94-470c-8591-431b24f49e18/` and `2d4c749a-c830-41a1-9d5c-3a4e1c4f5ca4/` — each holding `.lock` and `.highwatermark` files.
**Source**: local glob, accessed 2026-08-10. **Primary observation. Confidence: High** that tasks are filesystem-backed under `~/.claude/tasks/{uuid}/`.

**Evidence — cross-session sharing [WEAKLY SOURCED]**: a medium-trust secondary source states that "By setting the `CLAUDE_CODE_TASK_LIST_ID` environment variable, developers can point multiple instances of Claude at the same task list, allowing updates to be 'broadcast' to all active sessions", and that the Todo→Task replacement landed in v2.1.16 on 2026-01-22. **The official docs page I fetched does not mention `CLAUDE_CODE_TASK_LIST_ID`, the on-disk path, or cross-session persistence.** Flagged as **[unverified — Gap G9]**; the resolving action is `claude --help` / the official Claude Code (not SDK) docs.

**Scoring — why it still fails**:
- R1 ❌ — no visual board; `TaskList` is a text readback.
- R2 ✅ (in-process, no server).
- R3 ❌ — the on-disk artifacts are lock/watermark files, not markdown; the docs describe a structured record with typed fields, not a document.
- R4 ✅ (it *is* the agent's own tool).
- R5 ⚠️ (`subject` + `description` is card-with-brief-description grain, but with no visual surface), R6 ❌.
- **R7 ❌ — decisive.** State lives in `~/.claude/tasks/`, i.e. the **user's home directory keyed by session UUID, outside the repository**. It cannot be committed to git, cannot be branched with the work, and does not travel with a clone.
- R8 ⚠️ — `in_progress` + `activeForm` + `addBlockedBy`/`addBlocks` + a free-form `metadata` field is a real WIP model, and `metadata` is an interesting extension point. But being un-committable, it cannot serve as the repo's handoff baton.
- R9 ⚠️ — `status: "deleted"` gives purge; there is no groom tier and no idea backlog.

**Analysis**: the premise "expect ephemeral" is refuted — Tasks survive compaction and are written to disk. But the more important finding is that **their persistence is in the wrong place for this use case.** R7 is what kills them, not ephemerality. A board built on Claude Code Tasks would be invisible to git, which contradicts the user's entire working method (both `CONTEXT.md` files are committed artifacts, and basetwin's is explicitly stamped with branch and commit SHAs).

### C12. Dedicated session-handoff plugins — the R8-specific field

Four Claude Code plugins were found that target R8 directly. All are markdown-writing, hook-driven, and **very small projects**.

| Tool | Writes | Mechanism | Stars | Source |
|---|---|---|---|---|
| `thepushkarp/handoff` | `docs/handoff/HANDOFF.md`, appended timestamped entries | PreCompact + SessionStart(`compact`) + Stop hooks | **8** | [19] |
| `Sonovore/claude-code-handoff` | `.claude/session-state.md` (live) + `.claude/context.md`, `current-task.md`, `task-history.md`, `current-bug.md`, `bug-test-log.md`, `recent-prompts.md`, `mode` | SessionStart, UserPromptSubmit, PostToolUse(Edit/Write), PreCompact | **12** | [20] |
| `392fyc/claude-handoff` | structured handoff documents | SessionStart hook "reads the handoff document and injects it as additional context" | ? | [21] |
| `who96/claude-code-context-handoff` | context snapshots | hooks; restores "after both compact and clear lifecycle transitions" | ? | [22] |

**Evidence — `thepushkarp/handoff` template (the most specific found)**. Section structure: `Current Task State`, `Key Decisions`, `Modified Files`, `Blockers / Open Questions`, `Next Steps`, `Critical Context`, `Model Summary (8–12 bullets)`, `Handoff Context (pasteable resume instructions)`. Entries prefixed `## Handoff: [timestamp]`. Commands `/handoff:create` and `/handoff:resume --auto`. **A notable design detail**: the `Stop` hook "Blocks session termination if Model Summary or Handoff Context contain TODO placeholders (up to 3 attempts)" — i.e. it enforces that the handoff was actually filled in. MIT. Explicitly **does not** capture git branch/state or verification commands.
**Confidence: High** for the template (repo README is authoritative for its own format); **Low** for quality (8 stars, no independent evaluation).

**Evidence — `Sonovore/claude-code-handoff` maintenance model**: "**Continuously maintained.** The automated system updates `session-state.md` live during sessions. 'Every time you send a message, Claude sees a directive telling it to check if anything important happened and update `session-state.md`.'" Sections cover "task status, confirmed facts, next actions, and test results". MIT.
**Analysis**: two elements here map onto the user's practice precisely — **"confirmed facts"** is the same distinction as beatrix's `### Witnessed, not inferred` / "authored-not-run", and **"test results"** is the same idea as basetwin's falsifiable-checkpoint table. That two independent designs converged on these fields is meaningful corroboration that the L5 payloads are the right ones. **Confidence: Medium** (one small project, self-described).

**Common design pattern across all four, and the transferable finding**: every one of them uses a **`SessionStart` hook to re-inject the handoff document into the new session's context**, and most add `PreCompact` to snapshot before compaction. This is a *mechanism*, and it is the same mechanism `AppSoftwareLtd.vscode-agent-kanban` reached for with its "AGENTS.md sentinel sections that VS Code re-injects on every agent turn" [11]. **Three independent projects converging on hook-based re-injection is High-confidence evidence that this is the correct implementation strategy for R8.** The user already has `SessionStart` and `PreToolUse` hooks wired (Finding L3), so the substrate exists.

**Scoring (as a class)**: R1 ❌, R2 ✅, R3 ✅, R4 ✅, R5 ❌, R6 ⚠️, R7 ✅, **R8 ⚠️ — the best available, and still short of `CONTEXT.md`**, R9 ❌ (no backlog at all — these are pure continuity tools).

**Disposition**: **none is adoptable as-is** (8 and 12 stars are below any reasonable dependency threshold for a load-bearing workflow), **but collectively they are the strongest design input for the build path.** They validate the mechanism, the section grammar, and the enforce-completion-at-Stop trick.

## The R8 Gap

**Plain answer: no. No existing tool stores resumable in-progress story state at the fidelity the user's `CONTEXT.md` already achieves.** The expectation stated in the brief — that R8 is the requirement most likely to be unmet — is **confirmed**.

That said, the finding is more useful than a flat "nothing exists", because the field splits into three groups that each get part of it right.

### What the field actually offers

**Group 1 — per-task planning fields.** Backlog.md's "Implementation plan" + "Definition of Done" + acceptance criteria + comments + "final summary and completion notes" [1]; `kanban-md`'s `claim` ownership + `started` timestamp + "blocked status with reasons" [12]; Claude Code's `activeForm` + `addBlockedBy` + `metadata` [18]. These record **what the plan was and how far through it we are**. They are structured, agent-writable, and genuinely useful. They are also *scoped to one card* and *forward-looking only*.

**Group 2 — dependency readiness.** beads models work as a DAG so an agent can compute "ready work" and "maintain context across sessions without losing state" [5][6]. This answers *which card to pick next*, which is a real part of resumption. Steve Yegge's framing — the "50 First Dates" problem, agents "waking up with no memory of yesterday's work" — is the same problem statement the user has. But the solution is graph topology, not situational knowledge.

**Group 3 — session-continuity documents.** `thepushkarp/handoff` writes `Current Task State`, `Key Decisions`, `Modified Files`, `Blockers / Open Questions`, `Next Steps`, `Critical Context`, `Model Summary`, `Handoff Context` [19]. `Sonovore/claude-code-handoff` maintains `.claude/session-state.md` live with "task status, confirmed facts, next actions, and test results" [20]. This group is **by far the closest to `CONTEXT.md`** — it is the only group that treats the *document* as the artifact rather than a field on a card.

**Confidence: High** that these three groups exhaust what exists, based on 6+ independent projects examined. **Medium** confidence that no tool outside the searched space does better — see Gap G10.

### What `CONTEXT.md` does that none of them do

Comparing the L5 payloads against Group 3, the closest competitor:

| Payload | Best tool coverage | Verdict |
|---|---|---|
| Next steps, ordered | `Next Steps` [19]; beads DAG [5] | **Covered.** |
| Blockers | `Blockers / Open Questions` [19]; `blocked status with reasons` [12] | **Covered** — though none distinguishes *operator-gated* from *technically blocked*, which beatrix does explicitly (`**BLOCKED ON THE OPERATOR:**`). |
| Modified files / where things are | `Modified Files` [19] | **Partial.** A flat list of touched files, not beatrix's annotated `## Where the files are` map with per-entry warnings. |
| Verified vs inferred | `confirmed facts` [20] | **Partial, and the closest convergence found.** No tool has beatrix's three-way distinction between witnessed, authored-not-run, and unproven. |
| Falsifiable checkpoint values | `test results` [20] | **Weakly covered.** "Test results" is a pass/fail record. basetwin's table of seven expected kWh values *plus the invariant that validates them* ("if it ever exceeds Mains, the resolution dedup has broken") is a different artifact: a **self-check an agent runs before trusting its own understanding**. Nothing models this. |
| **Traps already paid for** | — | **NOT COVERED BY ANY TOOL.** Repo-scoped, durable, cross-referenced negative knowledge that outlives the card that produced it. `Critical Context` [19] is per-handoff and gets overwritten or appended; beatrix's numbered traps are cited *from other sections* (`§ 9 trap 8`, `trap 18`) and survive feature completion. This is a knowledge base, and no candidate has one. |
| **Anti-instructions ("what NOT to do first")** | — | **NOT COVERED BY ANY TOOL.** No tool models negative guidance. beatrix's is highly specific and expensive to rediscover: don't run the 14-minute suite to orient, don't re-plan § 5, don't deploy. |
| **Self-invalidating history markers / supersession** | — | **NOT COVERED BY ANY TOOL.** "§ 3 and § 4 are HISTORY… Both say 'start here' in places and both are wrong about that now." A card has one status; a document has regions of differing currency. Tools model the former. |
| **Sub-card, intra-step progress** | Backlog.md implementation plan [1] | **Partial, and the user has already diagnosed the failure.** |
| Orientation boot sequence | `Handoff Context (pasteable resume instructions)` [19] | **Partial** — a paste-blob, not a numbered `FIRST FIVE MINUTES` protocol with per-step rationale. |

### The user's own diagnosis is the strongest evidence

From beatrix `CONTEXT.md` § FIRST FIVE MINUTES:

> "See the phase table in § *Where we are* — **it is the only place that tracks intra-DELIVER state, because `/nw-continue` structurally cannot.**"

This is the user, in their own working file, recording that their own purpose-built continuity command cannot hold the state they need — so the markdown document holds it instead. Note the word *structurally*: not "hasn't been implemented yet" but "the model is wrong". A tool tracking steps-completed cannot express "19/19 steps committed, 40/42 scenarios green, DES integrity exit 0, **but** what is left is inside DELIVER: the Phase 4 revision pass, then the mutation gate, integrity re-run, finalize and the owed retrospective." That is a **nested state machine inside a single card**, and no board models it.

Corroborated independently by basetwin `CONTEXT.md`, where `nw-finalize` "could not run: the workspace has no `deliver/execution-log.json` or `roadmap.json` for the pre-dispatch gate to read" — and the two copies of its own instructions "contradict each other". **The pattern across both repos: the machine-readable state substrate exists (Finding L3) and repeatedly fails to hold the real state, so the human writes prose.**

### The grammar is stable across three repositories — which means it is buildable

The decisive structural finding: the same document grammar appears in **three independent instances**, two repos and this plugin repo itself.

`/home/philvanevery/Git/github/pmvanev/phil-claude-plugin/continue.md` (accessed 2026-08-10) carries: a title with resume point, `Last updated 2026-07-01`, and `Latest commit: **f881b48**`; a `> **MILESTONE (2026-07-01)…**` callout; `## What this is`; `## How it was built (the trail)`; `## Current state — DONE`; `## Key decisions (ADRs)`; `## First-run post-mortem (run wf_3138f9d2-f13, 2026-06-18)`; `## First successful run (run wf_dfe9faa4-5a4, 2026-07-01) — machinery VALIDATED` with a ✅/⧗ checklist including an explicit **`NOT yet exercised ⧗`** line; an `**Oracle note:**`; `## Two bugs found & fixed`; `## NEXT — optional follow-ups (nothing blocking)`; `## Quick file map`.

Every L5 payload reappears: falsifiable evidence with run IDs and counts ("202 tests, ~2s"; "3/3 refactors landed green"; "net −115 lines"), verified-vs-unverified labelling (the ⧗ markers), traps ("**args string-vs-object footgun** — the run-1 misfire class, *still live*"; "**Gate timeout blindness**"), a file map, and an ordered NEXT with nothing-blocking status.

**Confidence: High.** Three instances, three different projects, written months apart, converging on the same ~10 sections. **This is a specifiable format, and a specifiable format can be templated, validated, and generated. That is the central engineering finding of this research.**

*(Correction to a research-brief assumption: `/eos` in this plugin is **not** an end-of-session command — it is "Edit prose for clarity using Elements of Style principles". It is unrelated to R8. Verified by reading `commands/eos.md`, accessed 2026-08-10.)*

## Local Environment Inventory

**Method**: direct read of `/home/philvanevery/.claude/settings.json`, glob over `/home/philvanevery/.claude/plugins/`, and read of the user's own plugin tree. Accessed 2026-08-10. Reputation: N/A (primary observation of the user's machine — the highest-authority source available for "what is already installed").

### Installed marketplaces

From `~/.claude/settings.json` → `extraKnownMarketplaces`:

| Marketplace | Source |
|---|---|
| `pmvanev-plugins` | github: `pmvanev/claude-marketplace` (the user's own) |
| `knowledge-work-plugins` | github: `anthropics/knowledge-work-plugins` |
| `claude-plugins-official` | (default, implied by enabled plugins) |

### Enabled plugins

`phil@pmvanev-plugins`, `frontend-design`, `playwright`, `chrome-devtools-mcp`, `plugin-dev`, `mcp-server-dev`, `superpowers` (all `@claude-plugins-official`), and `productivity@knowledge-work-plugins`.

**Only one installed plugin addresses R1-R9 at all**: `productivity@knowledge-work-plugins` v1.3.1.

### Finding L1: The installed `productivity` plugin's `task-management` skill is a flat personal to-do list, not a story backlog

**Evidence** (verbatim, from `~/.claude/plugins/cache/knowledge-work-plugins/productivity/1.3.1/skills/task-management/SKILL.md`):

- Storage: "Tasks are tracked in a simple `TASKS.md` file that both you and the user can edit." Location is hardcoded: "**Always use `TASKS.md` in the current working directory.**"
- Fixed four-column template: `## Active`, `## Waiting On`, `## Someday`, `## Done`.
- Task grain: `- [ ] **Task title** - context, for whom, due date`. Sub-bullets for detail.
- Visual layer: "A visual dashboard is available… Check if `dashboard.html` exists in the current working directory. If not, copy it from `${CLAUDE_PLUGIN_ROOT}/skills/dashboard.html`". The board "Reads and writes to the same `TASKS.md` file", "Auto-saves changes", "Watches for external changes (syncs when you edit via CLI)", and "**Supports drag-and-drop reordering of tasks and sections**".
- Prune loop exists but is calendar-based, not ship-based: "Keep Done section for ~1 week, then clear old items."

**Source**: local file, accessed 2026-08-10. Authoritative (it is the executing artifact, not a description of it).
**Confidence**: High (primary source).

**Analysis / interpretation**: this is the closest thing already installed, and it is genuinely markdown + drag-drop + agent-writable. But its unit of work is a *commitment* ("send that over", "for [person]", "due [date]"), not a *story*. There is no per-story detail file (R6), no notion of in-progress state beyond a checkbox (R8), and no groom step (R9 partial). The `dashboard.html` is a standalone HTML file, which is promising for R2 — it needs no server, but it also is **not a VS Code panel**; it opens in a browser. Whether it can read/write `TASKS.md` from `file://` without a server is a **[GAP — see Knowledge Gaps G1]**: browsers block `fetch` on `file://` and the File System Access API requires a user gesture per session, so "auto-saves" and "watches for external changes" imply either a picked directory handle or a served origin. This must be resolved by inspecting `dashboard.html` before crediting R2.

### Finding L2: The user's own `phil` plugin already owns the per-feature documentation namespace a board would need to point at

**Evidence**: `/home/philvanevery/Git/github/pmvanev/phil-claude-plugin/` contains `commands/` (18 commands incl. `work.md`, `edd.md`, `refactor-loop.md`, `adversarial-review.md`, `eos.md`, `create-plugin-feature.md`), `agents/` (5), `skills/` (incl. `work`, `edd`, `adversarial-review`, `refactor-tests`, `redesign-tests`, each with a `self-test/` corpus of `manifest.json` fixtures), and a `docs/feature/{feature-name}/` convention with per-wave subdirectories: `discuss/`, `design/`, `distill/`, `deliver/`, plus `slices/slice-NN-*.md`, `feature-delta.md`, and `deliver/progress.md` + `deliver/roadmap.json`.
**Source**: local glob + read, accessed 2026-08-10.
**Confidence**: High (primary source).

**Analysis**: R6 (detailed per-story notes) is *already solved* by `docs/feature/*/slices/slice-NN-*.md`. A board would not need to invent story detail storage; it would need to *link to* it. Similarly `deliver/progress.md` and `deliver/roadmap.json` already hold intra-delivery state. The missing pieces are the visual overview (R1/R5) and a durable, structured handoff record (R8). Two of the user's own commands are also directly adjacent: `/eos` (end-of-session) and `continue.md` at the repo root — **[verify what these do before finalizing; they may already be a partial R8 implementation]**.

### Finding L3: nWave DES hooks already persist per-session machine state to `.nwave/`

**Evidence**: `~/.claude/settings.json` registers `SessionStart`, `SubagentStart`, `SubagentStop`, `PreToolUse` (Agent/Write/Edit/Bash) and `PostToolUse` hooks, all dispatching to `des.adapters.drivers.hooks.claude_code_hook_adapter`. One hook body reads `test -f .nwave/des/deliver-session.json || exit 0`, and another blocks Bash commands whose text names `execution-log.json` with the message "Direct modification of execution-log.json via Bash is blocked… To modify it, use `des.cli.log_phase`."
**Source**: local file, accessed 2026-08-10.
**Confidence**: High (primary source).

**Analysis**: there is already a session-state substrate (`.nwave/des/deliver-session.json`, `deliver/execution-log.json`, `roadmap.json`) with write-protection and a CLI. This is machine-grade step/phase tracking, i.e. *partial* R8 — it records which steps executed and passed. It does **not** record the narrative state the user's `CONTEXT.md` carries. Corroborated by the beatrix `CONTEXT.md` itself, which states this limitation explicitly (see Finding L5).

**Operational note (R7 hazard already observed locally)**: the same hook config exists because tooling that writes JSON state has already caused git accidents in this ecosystem — beatrix's `CONTEXT.md` records that "directory staging silently swept 15 of someone else's entries into a commit". Any board format chosen for R7 must be reviewed for this class of failure.

## De-Facto Requirements Spec: The User's Existing Artifacts

These three files are the strongest available evidence for what R8 and R9 actually mean, because they are a working implementation refined over months. All accessed 2026-08-10. Primary sources.

| File | Lines | Role |
|---|---|---|
| `/home/philvanevery/Git/ia-gitlab/basetwin/beatrix/CONTEXT.md` | 951 | per-feature handoff baton, mid-flight |
| `/home/philvanevery/Git/ia-gitlab/basetwin/beatrix/docs/feature/feature-ideas.md` | 1693 | idea backlog + standing directives |
| `/home/philvanevery/Git/ia-gitlab/basetwin/basetwin/CONTEXT.md` | 286 | same pattern, post-ship (feature finalized) |

### Finding L4: `CONTEXT.md` is a structured document with a stable, reproducible section grammar — it is a format, not free-form notes

**Evidence**: the beatrix file's top-level headings are, in order: a title carrying its own currency stamp (`# CONTEXT — where we are (rewritten 2026-08-06; **updated through 2026-08-10 — slice-03 is MID-DELIVER, § 0 N4**)`), then `## Where we are, in one paragraph`, `### Suite state`, `### What 2026-08-06 cost and bought`, `## FIRST FIVE MINUTES — if this file is all you were given`, `## 0. NEXT — in the order I would take it`, then numbered sections 1-9 (`## 1. THE CLIENT PANE IS DONE`, `## 2. THE DEPLOYMENT WINDOW`, … `## 6. Debt that is load-bearing`, `## 7. Operational (all operator-gated)`, `## 8. Standing guardrails`, `## 9. Traps already paid for — do not rediscover`), closing with `## Where the delivered work is written down`.

The basetwin file, written for a *finished* feature, uses a parallel-but-shorter grammar: `## Where this landed`, `## What the dashboard is now`, `## Open items` (with a `### Closed, so you don't go looking` subsection), `## Where the files are`, `## Running things`, `## Gotchas that will cost you an hour`, `## Background`.
**Source**: local grep + read, accessed 2026-08-10.
**Confidence**: High (two independent instances of the same grammar, different repos, different features).

**Analysis**: the recurrence of the grammar across two repos is the important signal. This is a *template* the user has converged on, which means it is specifiable — and therefore buildable as a plugin artifact. Any tool claiming R8 must be judged against this grammar, not against "has a notes field".

### Finding L5: `CONTEXT.md` carries five distinct payloads that no kanban tool models

Extracted from the two `CONTEXT.md` files:

1. **Orientation-under-amnesia** (`## FIRST FIVE MINUTES — if this file is all you were given`). An explicit boot sequence for a context-less agent: orient with four named commands; read `CLAUDE.md` for the standing contract "this file is the delta"; read § 0 because it "is the only list of what is actually next"; then a **pointer to the exact resumption coordinate**: "Pick up at § 0 N4 — slice-03, mid-DELIVER on branch `admin-field-triage`". It also contains an explicit **anti-instruction list**: "**What NOT to do first:** do not run the full backend suite to orient yourself (~14 minutes…), do not re-plan anything in § 5, and **do not deploy** — operator-gated". *No kanban tool has a concept of "what not to do when you resume".*

2. **Self-invalidating history markers.** The file annotates its own stale regions: "**§ 3 and § 4 are HISTORY** — § 3 is the lessons that shaped slice-02, § 4 is the record of building it. Both say 'start here' in places and both are wrong about that now." Likewise basetwin's "The J-SIM-CIRC feature documents are SUPERSEDED IN PART, not amended." This is a *supersession* relation between document regions — richer than a card's status field.

3. **Sub-card, intra-step progress with an explicit statement that the tooling cannot hold it.** The beatrix N4 row reads: "19/19 steps committed, 40/42 scenarios green, DES integrity exit 0. **What is left is inside DELIVER**: the Phase 4 revision pass (**D1 …**), then the mutation gate, integrity re-run, finalize and the owed retrospective." And decisively, from FIRST FIVE MINUTES: "See the phase table in § *Where we are* — **it is the only place that tracks intra-DELIVER state, because `/nw-continue` structurally cannot.**" *This is the user's own diagnosis of the R8 gap, in their own words, about their own tooling.*
   **Confidence**: High. This single quote is the most authoritative available evidence that R8 is unmet by the tooling the user already has.

4. **Traps already paid for** (`## 9. Traps already paid for — do not rediscover`; basetwin's `## Gotchas that will cost you an hour`). Durable negative knowledge, scoped to the repo rather than to a card, and explicitly framed as *cost recovery*. Examples from basetwin: "A running Grafana does NOT poll dashboard file changes"; "**Structural tests cannot see a wrong number.** This repo's dominant defect is a plausible-looking wrong value, not a crash. A syntactically *invalid* Flux query once passed all 21 acceptance tests. Execute the query."; "`MSYS_NO_PATHCONV=1` is load-bearing". Beatrix numbers its traps (`trap 8`, `trap 18`) and **cross-references them from other sections** — a citable knowledge base, not a comment thread.

5. **Falsifiable checkpoints — expected values to verify against.** basetwin ships a table of seven kWh figures ("Simulated TOTAL (electric) 1573.61", "Measured TOTAL (18 circuits) 2544.27") plus the invariant that validates them: "The measured total should land just *under* Mains — circuits sum to 99.5% of it. If it ever exceeds Mains, the resolution dedup has broken." Beatrix does the same with suite counts ("1044/0/64", "vitest 389/17 exactly on baseline"). *A resuming agent can self-verify it has not broken anything — before writing code.* No kanban tool models "the numbers you should see if the world is still as I left it".

**Additional payloads worth noting**: verified-vs-inferred labelling (`### Witnessed, not inferred`; "authored-not-run"; "**Still unproven**: no surface has been observed rendering an orphan row to anyone"); runnable command blocks with their gotchas inline (`## Running things`); a file-location map (`## Where the files are`) with per-entry warnings; and operator-gated blocking items distinguished from technical blockers (`**BLOCKED ON THE OPERATOR:**`).

### Finding L6: `feature-ideas.md` does double duty — idea backlog *and* standing-directive store — and is groomed by rewriting, not by moving cards

**Evidence**: the beatrix file's structure is a pre-title scratch list (six raw one-liners at lines 1-6, above the `# Feature Ideas` heading and separated by `---`), then the titled body with a scoping preamble ("These are **unscoped ideas**, not committed work — each is sketched against the customer reality captured in [`../customer-context/customer-context.md`]… Every idea must respect the hard constraints: **read-only at the vendor boundary** … and **audit-defensibility**"), then `## Directives`, then six domain-themed sections (`## Form automation`, `## Data flow between systems`, `## Corpus ingest`, `## Scheduling & treatment planning`, `## Visibility & provenance`, `## Access`, `## Platform / deployment`).

`## Directives` is explicitly not a backlog: "Standing decisions that govern how the ideas below get built — not themselves features, but constraints on execution." Its entries are dated, versioned in place, and carry supersession and status: "**DIRECTIVE (2026-07-14): no local `docker-compose` stack…** … **superseding** the 'stand up the `docker/` compose dev profile' posture", with a **Rationale** block, a **STATUS — fully operationalized (2026-07-15)** block naming the two `/phil:work` initiatives that delivered it and the resulting evolution docs, an inline **CORRECTION 2026-07-31** amending itself, and a **Cross-links** block pointing at three sibling ideas by name.

Individual ideas are similarly layered: a bolded title, a paragraph tying it to a numbered entry in a *failure catalogue* ("failure catalogue #2, #4"; "(#5)"), nested sub-ideas, and explicit **"Open DISCUSS points"** — e.g. for auto-save-as-you-type: "capture granularity (per-keystroke vs. debounced/blur), how long drafts are retained, PHI handling of staged drafts, and detecting 'this is the same form' on reload".
**Source**: local read, accessed 2026-08-10.
**Confidence**: High (primary source).

**Analysis (interpretation)**: the R9 loop in practice is:
- **capture** — append a raw one-liner to the top scratch zone with no ceremony (this is the *only* zero-friction step, and it lives *outside* the groomed structure);
- **groom** — promote the one-liner into a themed section, expand into a paragraph, tie it to evidence (customer context, failure catalogue), and add "Open DISCUSS points";
- **pick** — a feature graduates out into `docs/feature/{name}/` and the nWave wave commands take over;
- **track** — `CONTEXT.md` becomes the tracker for the picked item;
- **purge** — on ship, the idea is deleted from `feature-ideas.md`, `CONTEXT.md` is rewritten, and the record moves to `docs/evolution/{date}-{feature}.md`. Both `CONTEXT.md` files point at exactly this: beatrix's `## Where the delivered work is written down`, basetwin's "the feature was archived to `docs/evolution/2026-08-07-hvac-energy-sim-vs-measured.md` — read that first for the whole arc".

Two consequences for candidate evaluation:
- **R9 requires a *promotion pipeline* across three storage tiers** (scratch → groomed idea → feature workspace → evolution archive), not a single board with columns. A tool offering only `todo/doing/done` on one file satisfies the *shape* of R9 and none of its substance.
- **A card-per-idea model actively loses information.** `## Directives` are non-cards that constrain cards; failure-catalogue references are edges to an external corpus; supersession is an edge between document versions. These are graph relations, and flat card lists cannot hold them. This is the single strongest argument against adopting a generic kanban tool as the *system of record* — though not against adopting one as a *view*.

## Viable Combinations

Ranked by effort-to-fit. All four assume the R8 layer is built, because no combination avoids that.

### Combination 1 — Backlog.md format + `ysamlan.vscode-backlog-md` board + a thin `CONTEXT.md` plugin layer  ★ best fit

**Adopt** Backlog.md (`backlog/tasks/*.md`, file-per-task, MIT, 6.4k★, v1.50.1) for R3-R7 and R9's pick/track/purge; the VS Code extension for R1/R2/R5; its MCP server or plain file edits for R4.
**Build** (in the user's existing `phil` plugin): (a) a `CONTEXT.md` generator/validator implementing the three-instance grammar, wired to a `SessionStart` hook for re-injection — the pattern five independent projects converged on [11][19][20][21][22]; (b) a groom command promoting `feature-ideas.md` one-liners into `backlog/tasks/*.md`; (c) a link convention from each task to `docs/feature/{name}/slices/slice-NN-*.md`, which already exists (Finding L2).

**Satisfies**: R1-R7 and R9 from adopted tooling; R8 from roughly one command + one skill + one hook.
**Cannot satisfy without work**: the traps ledger, anti-instructions and supersession markers have no home in Backlog.md's schema — they are repo-scoped, not task-scoped, so they belong in the built `CONTEXT.md` layer, not in a card field.
**Effort**: Low-Medium. **Fit**: Highest.
**Risk**: R1/R2 rest on a 361-install, 17★, single-maintainer extension not affiliated with Backlog.md. Mitigated because the data is plain markdown owned by the 6.4k★ CLI — losing the extension costs a *view*, not the backlog. **De-risking: adopt the format first and treat the extension as replaceable.**

### Combination 2 — Keep `feature-ideas.md` + `CONTEXT.md` as system of record; build a board *view* over them

**Adopt** nothing as the source of truth. **Build** a board *projection*: parse `feature-ideas.md` and `docs/feature/*/` into a VS Code webview kanban, where dragging a card edits the underlying markdown.

**Rationale from the evidence**: the last matrix row scores 8/9. Combination 1 replaces a system that satisfies eight requirements in order to acquire the ninth, and pays for it in R8/R9 fidelity — Finding L6 shows a card-per-idea model **loses** `## Directives`, failure-catalogue edges and supersession relations. This combination acquires R1 and keeps everything else.
**Precedent that it is tractable**: the already-installed `productivity` `dashboard.html` achieves markdown + drag-drop + no-server in a single HTML file using `showOpenFilePicker` and `createWritable` (Finding C5) — and a VS Code webview has *fewer* restrictions than a `file://` page, since the extension host reads and writes freely.
**Satisfies**: all nine, at the cost of building the R1/R5 layer.
**Effort**: Medium-High. The real work is a markdown round-trip parser that does not mangle hand-authored prose — and that is the hard part, given `feature-ideas.md` carries nested sub-ideas, inline corrections and a `## Directives` section that is not a card at all.
**Fit**: Highest in principle; highest risk of a half-built board.
**Ranked second because the effort concentrates in the one requirement the user is least served by today, and a bad board is worse than no board.**

### Combination 3 — `antopolskiy/kanban-md` + the same built `CONTEXT.md` layer

**Adopt** kanban-md (markdown+frontmatter file-per-task, MIT, 187★, ships **Claude Code skills** — the same extension idiom the user's plugin already uses — with `pick --claim` / `move` verbs, claim ownership, started timestamps and blocked-with-reason). **Build** the same R8 layer as Combination 1.
**Satisfies**: R3-R7, R9 pick/track, and R4 excellently.
**Cannot satisfy**: R1 and R2 only via a TUI in the integrated terminal — ⚠️, and it occupies the terminal needed for git and tests.
**Effort**: Low-Medium. **Fit**: Good if a TUI is acceptable; otherwise it fails a hard requirement.
**Why consider it over Combination 1**: no dependency on a third-party VS Code extension, and a more idiomatic agent integration. **Run test G5 first** — whether `--mouse` drag works in VS Code's integrated terminal is the single experiment that decides between Combinations 1 and 3.

### Combination 4 — `holooooo.markdown-kanban` over a new single-file board doc

**Adopt** the highest-install pure-markdown VS Code board (2,012 installs, updated 2026-07-23, drag-drop, no server, launches Claude Code from a card via Task Terminals). **Build** the R8 layer plus a convention pointing cards at slice files.
**Cannot satisfy**: R6 properly (detail is an expanded card in the same file), R7 cleanly (single-file board — every move rewrites it), and **no cross-file linking is documented**, which is the real blocker: story detail already lives in `docs/feature/*/slices/*.md` and this tool cannot reference it.
**Effort**: Lowest to *try* — install and point it at a file. **Fit**: Lowest of the four.
**Honest use**: a one-afternoon probe to learn whether a visual board actually changes how the user works, before committing to Combination 1 or 2. Its value is as a cheap experiment, not as a destination.

### Cross-cutting recommendations

1. **Do not put the L5 payloads in card fields.** Traps, anti-instructions and supersession are repo-scoped and outlive cards. Whatever board is adopted, `CONTEXT.md` (or a successor with the same grammar) should stay a separate committed document. Evidence: the payload table shows zero tool coverage for three of them, and Finding L6 shows the card model actively loses relations.
2. **Use a `SessionStart` hook to re-inject whatever is built for R8.** Five independent projects converged on this [11][19][20][21][22], and `~/.claude/settings.json` already registers `SessionStart`.
3. **Steal `thepushkarp/handoff`'s `Stop`-hook enforcement** — block session end while the handoff still contains TODO placeholders [19]. It converts a discipline into a gate, which is this plugin's design philosophy throughout.
4. **Prefer file-per-task over single-file boards** for R7. Two concurrent edits then touch two files.
5. **Steal beads' hash-based IDs** (`bd-a3f2`) if IDs are ever generated, to avoid collision on concurrent creation [5][6].
6. **Do not take any 8-12★ handoff plugin as a dependency.** Read their templates, then implement in the user's own plugin, which is already the right vehicle (Finding L2).

## Knowledge Gaps

Each gap names the specific test or page that would resolve it.

**G1 — Can the `productivity` `dashboard.html` satisfy R2 as written?**
Established: it uses the File System Access API and no `fetch`/`XHR`, so no server is needed. Unresolved: whether it must run in an external Chromium window (Firefox and Safari lack `showDirectoryPicker`/`createWritable`), and whether the file handle must be re-picked each session. **Resolve by**: opening `~/.claude/plugins/cache/knowledge-work-plugins/productivity/1.3.1/skills/dashboard.html` in VS Code's Simple Browser and attempting a save; and checking whether it persists handles via IndexedDB.

**G2 — Backlog.md's last-publish date.**
Version 1.50.1 is confirmed from `registry.npmjs.org`, but the `time` field was not retrieved and `npmjs.com` returned HTTP 403 to WebFetch. Cadence is *inferred* from the version number, not measured. The extension's 2026-07-23 update date partially covers this. **Resolve by**: `npm view backlog.md time.modified`, or the GitHub releases page. *This matters because the brief requires a recorded last-release date for every candidate.*

**G3 — beads: is there any visual board, and what is its current maturity?**
`https://steveyegge.github.io/beads/` returned **HTTP 404** on 2026-08-10 (circuit-breaker: not retried; one alternative source used instead). R1 and R5 are therefore `?`. Its version, release date and any stability warnings are unverified. **Resolve by**: `github.com/steveyegge/beads` README and releases. *Low priority — beads already fails R3.*

**G4 — `vscode-agent-kanban` release recency.**
59★, 60 commits, and a self-noted "2026-03-12" marker; no release date or marketplace version/install count captured. **Resolve by**: its marketplace page (`AppSoftwareLtd.vscode-agent-kanban`) for last-updated and installs. Per the brief's rule, if the last release predates 2025-08, it must be flagged unmaintained.

**G5 — Does `kanban-md --mouse` drag-and-drop work inside VS Code's integrated terminal?**
This single experiment decides between Combinations 1 and 3. Documentation confirms mouse drag in a TUI; nothing confirms behaviour under VS Code's terminal mouse-event handling. **Resolve by**: `npm/go install`, run `kanban-md tui --mouse` in the integrated terminal, attempt a card drag. Five minutes.

**G6 — Does `kanban-md` have an archive/prune command and an idea tier?**
Its rich field set was captured; R9's groom and purge steps were not confirmed. **Resolve by**: `kanban-md --help` or the repo's command reference.

**G7 — Obsidian Kanban's exact markdown syntax.**
The GitHub landing page defers to separate documentation not fetched. The `##`-lanes / `- [ ]`-cards convention is inferred from format-compatible tools, not read from the spec. Release version, date and drag-drop are unverified from primary source. **Resolve by**: the plugin's docs site. *Matters only if the user wants cross-compatibility with Obsidian as a second view — which is a real option worth pricing, since it would add a mobile/tablet board for free.*

**G8 — The C9 disposal group was not individually verified.**
Focalboard, Vikunja, Plane, Huly, Wekan and Kanri were disposed on product category rather than per-tool primary sources, per the brief's instruction not to spend depth. Kanri's storage format in particular is marked `?`. **Resolve by**: per-project README, if any is to be reconsidered.

**G9 — `CLAUDE_CODE_TASK_LIST_ID` and the on-disk task format.**
The official SDK docs page confirms the Task tools, lifecycle and field shapes but says nothing about the on-disk location, the format, or cross-session sharing. `~/.claude/tasks/{uuid}/` with `.lock` and `.highwatermark` is confirmed by direct observation, but **no actual task-data file was located** — the two session directories contained only those two files. The `CLAUDE_CODE_TASK_LIST_ID` claim rests on a single medium-trust secondary source and is **[unverified]**. **Resolve by**: the Claude Code (not Agent SDK) docs, or `claude --help`. *Also note the version claim "Tasks replaced Todos in v2.1.16, 2026-01-22" conflicts with the official docs' "v2.1.142" — see Conflicting Information.*

**G10 — Search-space completeness.**
Discovery searches surfaced four candidates absent from the seed list, which is direct evidence the space is larger than enumerated. Two further leads were seen and not pursued: `ioniks/MarkdownTaskManager` ("Local-first Kanban task manager") and `wguilherme.kanban-md` / `Pd-ch.kanmark` / `jeddak.md-kanban` / `ItsCoding/KanbanCode` / `brokensandals/markheadboard` (all VS Code markdown boards). **Assessment**: they are unlikely to change the conclusion, because they are the same *class* as C3 and none is likely to satisfy R8. But "no tool satisfies R8" is a universal claim over an incompletely enumerated set, so it is stated at **Medium-High**, not High.

**G11 — No candidate was installed or executed.**
The most important gap. Every capability claim in the matrix is documentary. Notably unverified by trial: whether `ysamlan.vscode-backlog-md`'s board is pleasant to use, whether Backlog.md's MCP integration works with the user's Claude Code version, and whether Backlog.md's task schema tolerates the trap-ledger payloads. **Resolve by**: a timeboxed trial on a scratch repo — which is also the cheapest way to de-risk Combination 1.

## Conflicting Information

### Conflict 1 — Which Claude Code version replaced Todos with Tasks

**Position A**: v2.1.142 (and TypeScript Agent SDK 0.3.142). Source: [18] `code.claude.com/docs/en/agent-sdk/todo-tracking`, official first-party, reputation **1.0**. Evidence: "As of TypeScript Agent SDK 0.3.142 and Claude Code v2.1.142, sessions use the structured Task tools…"
**Position B**: "The Todo system was replaced by Tasks in v2.1.16 (January 22, 2026)." Source: secondary aggregator surfaced in search, reputation **0.6 at best**.
**Assessment**: **Position A is authoritative** — first-party documentation versus an uncredentialed aggregator. Position B may be conflating a feature-flag introduction with the default switch, but that is speculation. **The report uses v2.1.142.** The user's own environment shows Claude Code `2.1.63` on PATH (per `~/.claude/settings.json`), which is *below* 2.1.142 — so **this machine may still be on `TodoWrite`**, though the presence of `~/.claude/tasks/` and the availability of `TaskCreate`/`TaskList` in the current session suggests Tasks are active. Not material to the recommendation, since Task tools fail R7 either way.

### Conflict 2 — Does Backlog.md's board require a server?

**Position A (yes)**: "The web server is **required** to run (`backlog browser`) for drag-and-drop functionality" — [1], the project's own README.
**Position B (no)**: "No. The extension operates locally within VS Code and 'lives right in your repo,' requiring no external server infrastructure" — [3], the extension's marketplace listing.
**Assessment**: **not actually contradictory — they describe different products.** The first-party web board needs `backlog browser` on `127.0.0.1`; the third-party VS Code extension is an independent webview reimplementation reading the same files. Both are true. This is recorded as a conflict because it is the single most consequential distinction in the report: **R2 hinges entirely on which board you use**, and a careless reading of either source alone gives the wrong answer. The matrix scores the two paths as separate rows for this reason.

### Conflict 3 — Is `backlog.md`'s VS Code extension official?

The Backlog.md README describes `vscode-backlog-md` as "community-built" [1]; the marketplace lists the publisher as "Yoni Samlan" [3], distinct from the CLI's maintainer (MrLesk). **Assessment: consistent — it is third-party.** Noted because a reader skimming the Backlog.md README's feature list could reasonably assume first-party support and under-price the dependency risk.

## Source Analysis

| # | Source | Domain | Reputation | Type | Access Date | Cross-verified |
|---|---|---|---|---|---|---|
| L | `~/.claude/settings.json`, `~/.claude/plugins/**`, `~/.claude/tasks/**` | local fs | 1.0 (primary observation) | primary | 2026-08-10 | n/a |
| L | `productivity/1.3.1/skills/{task-management/SKILL.md, dashboard.html}` | local fs | 1.0 (primary) | primary | 2026-08-10 | n/a |
| L | beatrix `CONTEXT.md`, beatrix `feature-ideas.md`, basetwin `CONTEXT.md`, `continue.md`, `commands/eos.md` | local fs | 1.0 (primary) | primary | 2026-08-10 | Y (3 instances of one grammar) |
| 1 | MrLesk/Backlog.md README | github.com | 0.8 | industry/OSS | 2026-08-10 | Y (via [3], [4]) |
| 2 | npm registry, `backlog.md/latest` | registry.npmjs.org | 1.0 (existence/version only) | official registry | 2026-08-10 | Y |
| 3 | VS Code Marketplace, `ysamlan.vscode-backlog-md` | marketplace.visualstudio.com | 1.0 (existence/version/installs only) | official registry | 2026-08-10 | Y (via [4]) |
| 4 | ysamlan/vscode-backlog-md README | github.com | 0.8 | industry/OSS | 2026-08-10 | Y (via [3]) |
| 5 | steveyegge/beads (via search result summary) | github.com | 0.8 | industry/OSS | 2026-08-10 | Y (via [6],[7],[8]) |
| 6 | Better Stack, "Beads: A Git-Friendly Issue Tracker for AI Coding Agents" | betterstack.com | 0.6 | vendor blog — commercial interest noted | 2026-08-10 | Y |
| 7 | ianbull.com, "Beads — Memory for your Agent" | ianbull.com | 0.6 | practitioner blog | 2026-08-10 | Y |
| 8 | bruton.ai, "Beads (bd) — the Missing Upgrade…" | bruton.ai | 0.4 | promotional; **discounted, not relied on** | 2026-08-10 | N |
| 9 | VS Code Marketplace, `holooooo.markdown-kanban` | marketplace.visualstudio.com | 1.0 (registry facts only) | official registry | 2026-08-10 | Y (via [10]) |
| 10 | holooooo/markdown-kanban | github.com | 0.8 | industry/OSS | 2026-08-10 | Y |
| 11 | appsoftwareltd/vscode-agent-kanban README | github.com | 0.8 | industry/OSS | 2026-08-10 | N — single source |
| 12 | antopolskiy/kanban-md README | github.com | 0.8 | industry/OSS | 2026-08-10 | N — single source |
| 13 | smallhadroncollider/taskell (archive banner) | github.com | 0.8 (authoritative for own archive state) | industry/OSS | 2026-08-10 | Y (search corroborates 2024-03 last activity) |
| 14 | mgmeyers/obsidian-kanban | github.com | 0.8 | industry/OSS | 2026-08-10 | Partial — format not confirmed |
| 15 | Adafruit blog, markdown kanban for VS Code and Obsidian | blog.adafruit.com | 0.6 | industry blog | 2026-08-10 | supporting only |
| 16 | automazeio/ccpm README | github.com | 0.8 | industry/OSS | 2026-08-10 | Partial (forks are not independent) |
| 17 | aroussi.com, "How we fixed the context problem…" | aroussi.com | 0.6 | author blog — **conflict of interest: affiliated with automaze** | 2026-08-10 | N |
| 18 | **Claude Agent SDK — Todo Lists** | code.claude.com | **1.0** | official first-party | 2026-08-10 | Y (local fs observation) |
| 19 | thepushkarp/handoff README | github.com | 0.8 | industry/OSS | 2026-08-10 | Y (pattern via [20],[21],[22],[11]) |
| 20 | Sonovore/claude-code-handoff README | github.com | 0.8 | industry/OSS | 2026-08-10 | Y (same) |
| 21 | 392fyc/claude-handoff | github.com | 0.8 | industry/OSS | 2026-08-10 | Y (same) |
| 22 | who96/claude-code-context-handoff | github.com | 0.8 | industry/OSS | 2026-08-10 | Y (same) |

**Reputation distribution**: High (1.0): 8 (36%) — 5 primary local observations, 2 registries, 1 official doc. Medium-high (0.8): 11 (50%). Medium (0.6): 4 (18%). Low/discounted (0.4): 1. **Weighted average ≈ 0.83.**
**Excluded-domain check**: no source from the excluded list (`*.blogspot.com`, `wordpress.com`, `quora.com`, `pastebin.com`) was used. Two aggregator sites surfaced in search (`claudedirectory.org`, `mcpmarket.com`, `claudearchitect.com`, `claudefa.st`, `terminaldock.com`, `memedata.com`, `alternativeto.net`, `sourceforge.net`) were **not** used as evidence for any claim.
**Adversarial validation**: all fetched content was scanned per `operational-safety`. No prompt injection, authority impersonation or exfiltration attempt detected. Two bias flags recorded and applied: [6] is a vendor blog and [17] has an author conflict of interest; [8] is promotional and was discounted rather than cited for any capability claim.

**Bias note on the whole R8-plugin class**: the four handoff plugins ([19]-[22]) are single-maintainer projects whose READMEs are the only description of them. Their *templates* are cited (authoritative — the README defines the format) while their *effectiveness* is not claimed anywhere in this report.

## Full Citations

[1] MrLesk. "Backlog.md — A tool for managing project collaboration between humans and AI Agents in a git ecosystem". GitHub. https://github.com/MrLesk/Backlog.md. Accessed 2026-08-10.
[2] npm. "backlog.md — package metadata (v1.50.1)". npm Registry. https://registry.npmjs.org/backlog.md/latest. Accessed 2026-08-10.
[3] Samlan, Yoni. "Backlog.md (v0.3.9, updated 2026-07-23)". Visual Studio Marketplace. https://marketplace.visualstudio.com/items?itemName=ysamlan.vscode-backlog-md. Accessed 2026-08-10.
[4] Samlan, Yoni. "vscode-backlog-md". GitHub. https://github.com/ysamlan/vscode-backlog-md. Accessed 2026-08-10.
[5] Yegge, Steve. "beads — a memory upgrade for your coding agent". GitHub. https://github.com/steveyegge/beads. Accessed 2026-08-10. *(Docs site https://steveyegge.github.io/beads/ returned HTTP 404 on this date — see Gap G3.)*
[6] Better Stack Community. "Beads: A Git-Friendly Issue Tracker for AI Coding Agents". https://betterstack.com/community/guides/ai/beads-issue-tracker-ai-agents/. Accessed 2026-08-10.
[7] Bull, Ian. "Beads — Memory for your Agent and The Best Damn Issue Tracker You're Not Using". https://ianbull.com/posts/beads/. Accessed 2026-08-10.
[8] bruton.ai. "Beads (bd) — the Missing Upgrade Your AI Coding Agent Needs in 2026". https://bruton.ai/blog/ai-trends/beads-bd-missing-upgrade-your-ai-coding-agent-needs-2026. Accessed 2026-08-10. *[Promotional — discounted.]*
[9] holooooo. "Markdown Kanban (v2.0.0, updated 2026-07-23, 2,012 installs)". Visual Studio Marketplace. https://marketplace.visualstudio.com/items?itemName=holooooo.markdown-kanban. Accessed 2026-08-10.
[10] holooooo. "markdown-kanban". GitHub. https://github.com/holooooo/markdown-kanban. Accessed 2026-08-10.
[11] App Software Ltd. "vscode-agent-kanban — VS Code extension kanban board for agentic AI workflows". GitHub. https://github.com/appsoftwareltd/vscode-agent-kanban. Accessed 2026-08-10.
[12] Antopolskiy, Sergey. "kanban-md — File-based kanban board for autonomous agentic loop". GitHub. https://github.com/antopolskiy/kanban-md. Accessed 2026-08-10.
[13] smallhadroncollider. "taskell — Command-line Kanban board/task manager". GitHub. https://github.com/smallhadroncollider/taskell. **Archived 2024-03-25.** Accessed 2026-08-10.
[14] Meyers, Matthew. "obsidian-kanban". GitHub. https://github.com/mgmeyers/obsidian-kanban. Accessed 2026-08-10.
[15] Adafruit. "A Markdown-powered kanban task board for VS Code and Obsidian". 2026-02-17. https://blog.adafruit.com/2026/02/17/a-markdown-powered-kanban-task-board-for-vs-code-and-obsidian/. Accessed 2026-08-10.
[16] automazeio. "ccpm — Project management skill system for Agents using GitHub Issues and Git worktrees". GitHub. https://github.com/automazeio/ccpm. Accessed 2026-08-10.
[17] Aroussi, Ran. "How we fixed the context problem in AI-driven development". https://aroussi.com/post/ccpm-claude-code-project-management. Accessed 2026-08-10. *[Author affiliated with automaze — conflict of interest.]*
[18] Anthropic. "Todo Lists — Claude Agent SDK". Claude Code Documentation. https://code.claude.com/docs/en/agent-sdk/todo-tracking. Accessed 2026-08-10.
[19] Parashar, Pushkar. "handoff — Claude Code plugin to preserve and restore context between sessions". GitHub. https://github.com/thepushkarp/handoff. Accessed 2026-08-10.
[20] Sonovore. "claude-code-handoff — Interactive session handoff command for Claude Code". GitHub. https://github.com/Sonovore/claude-code-handoff. Accessed 2026-08-10.
[21] 392fyc. "claude-handoff — Session handoff & auto-continuation for Claude Code". GitHub. https://github.com/392fyc/claude-handoff. Accessed 2026-08-10.
[22] who96. "claude-code-context-handoff — Automatic context preservation for Claude Code". GitHub. https://github.com/who96/claude-code-context-handoff. Accessed 2026-08-10.

**Local primary sources** (all accessed 2026-08-10):
[L1] `/home/philvanevery/.claude/settings.json`
[L2] `/home/philvanevery/.claude/plugins/cache/knowledge-work-plugins/productivity/1.3.1/skills/task-management/SKILL.md`
[L3] `/home/philvanevery/.claude/plugins/cache/knowledge-work-plugins/productivity/1.3.1/skills/dashboard.html`
[L4] `/home/philvanevery/.claude/tasks/` (2 session directories)
[L5] `/home/philvanevery/Git/ia-gitlab/basetwin/beatrix/CONTEXT.md` (951 lines)
[L6] `/home/philvanevery/Git/ia-gitlab/basetwin/beatrix/docs/feature/feature-ideas.md` (1693 lines)
[L7] `/home/philvanevery/Git/ia-gitlab/basetwin/basetwin/CONTEXT.md` (286 lines)
[L8] `/home/philvanevery/Git/github/pmvanev/phil-claude-plugin/` — `continue.md`, `commands/eos.md`, and the `commands/`, `agents/`, `skills/`, `docs/feature/` trees

## Recommendations for Further Research

1. **Run the G5 experiment first** — `kanban-md tui --mouse` in VS Code's integrated terminal. It costs five minutes and decides between the two leading combinations.
2. **Timebox a Backlog.md trial on a scratch repo** — `backlog init`, install `ysamlan.vscode-backlog-md`, create three tasks, drag them, and inspect the resulting git diff. This resolves G11 and prices Combination 1 honestly. Specifically test whether a task file tolerates a long prose "traps" section without the tools mangling it.
3. **Prototype the R8 layer against the extracted grammar** before choosing a board. The grammar is the stable requirement; the board is the replaceable part. Deriving a `CONTEXT.md` template + validator from the three known instances is useful under every combination, including "change nothing else".
4. **Resolve G2 and G4** (last-release dates) before committing, per the fast-moving-tooling rule.
5. **Price Obsidian Kanban as a second, read-mostly view** (G7). If a Backlog.md or `##`-lane format is compatible, a tablet-friendly board comes nearly free — worth knowing before rejecting it outright.

## Research Metadata

**Duration**: ~45 turns. **Candidates examined**: 20+ (12 assessed in depth, 6 disposed briefly, 5 leads logged unpursued). **Sources cited**: 22 web + 8 local primary. **Cross-references**: Backlog.md verified across 3 independent sources; the hook-based re-injection pattern across 5; the `CONTEXT.md` grammar across 3 independent local instances.
**Confidence distribution**: High ~55% (all local findings, Backlog.md's storage/board/agent facts, taskell's archive status, Claude Code Task tools, the grammar-recurrence finding). Medium ~35% (single-source README capability claims for C4, C6; the R8-plugin class; CCPM). Low ~10% (beads' visual layer, Obsidian's format specifics, the C9 disposals).
**Tool failures affecting coverage**: `npmjs.com` HTTP 403 (Gap G2, mitigated via `registry.npmjs.org`); `steveyegge.github.io/beads/` HTTP 404 (Gap G3, mitigated via a secondary summary; circuit breaker applied, not retried).
**Output**: `docs/research/tooling/local-markdown-kanban-backlog-tooling-research.md`
