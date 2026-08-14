# ADR-013 — session-handoff: snapshot surface is a git-ignored runtime artifact

Status: accepted (DESIGN wave, 2026-08-12) · Feature: session-handoff · Resolves DISCUSS open question 1

## Context

`/phil:handoff` must persist the state a fresh session cannot derive — the why, the intended next
action, the entry-point, and the claimed card. DISCUSS deliberately left the surface open, naming
three candidates: a local file, the forge board, or both partitioned by scope.

The repo already namespaces per-initiative working trails under `docs/work/<initiative>/` (ADR-006)
and per-intent trails under `docs/edd/<slug>/` (ADR-009). **Both ADRs left "git-ignore while in
flight versus commit" open, and both leaned committed.** Following that lean is the obvious move and
it is wrong here.

## Decision

**A single git-ignored runtime artifact at the repo root: `.session-handoff.md`.**

Not a fourth `docs/*/` namespace, and not committed.

```
.session-handoff.md      # the snapshot: why · next action · entry-point · claimed card
                         #  + timestamp + tree fingerprint (commit sha + dirty-state)
.gitignore               # one added line
```

This is not a new convention. It is the convention `.refactor-loop-ledger.md` already
established — a root dotfile, git-ignored, carrying runtime state for an in-flight run, described in
`.gitignore` as "created in target repos, never committed."

## Why the ADR-006 / ADR-009 lean does not carry

The two prior trails and this snapshot differ on the axis that decides the question:

| | `docs/work/`, `docs/edd/` | `.session-handoff.md` |
|---|---|---|
| Lifetime | Durable — outlives the run | Ephemeral — consumed by the next session |
| Audience | Shared; a teammate reads the trail | Private working state |
| Writers | One initiative, one writer | **Concurrent sessions** |
| Value if committed | Reviewable history | History pollution |

The concurrency row is decisive. This repo runs workflows and subagents, so simultaneous sessions
are routine rather than hypothetical, and DISCUSS names multi-session arbitration as out of scope
for v1. Committing the snapshot converts an application-level concurrency problem into a git-level
merge conflict — on the one file whose entire job is to be trusted on sight. A snapshot a reader has
to resolve a merge in is a snapshot that has already failed.

Committing also fights constraint C4 (no ceremony on a no-op): every session end would otherwise
produce a commit, or a dirty tree that the *next* session's own fingerprint check then reads as
drift. The snapshot would corrupt the staleness signal it depends on.

## Alternatives considered

- **A fourth `docs/session/<slug>/` namespace, committed** — consistent with ADR-006 and ADR-009, and
  self-documenting alongside the three existing orchestrator namespaces. Rejected on the four
  differences above, chiefly concurrency. Consistency with a precedent is worth less than not
  shipping merge conflicts into the resume path.
- **The forge board (issue body)** — rejected for in-flight scratch: the board is world-readable
  (DISCUSS anxiety C), and `phil:nwave-issue-board` is explicitly one-way, so a snapshot read back
  from an issue would invert a rule the repo already relies on. Not rejected for the outward-facing
  tier — see the next item.
- **Partitioned local + board**, per `phil:issue-board`'s *One system of record per scope* — local
  owns in-flight detail, the forge owns what others see, the issue number is the only join. This is
  the likely end state and is **deferred, not rejected**. Adopting it in v1 would pull the forge into
  the walking skeleton, forcing WS strategy from C (real local resources) to B (faked forge adapter
  plus a contract test) for the least uncertain of the three outcomes.
- **One file per session (`.session/<id>.md`)** — rejected for v1: it removes the write race but
  replaces it with a selection problem (which snapshot does resume pick?), and answering that is
  arbitration, which DISCUSS placed out of scope. A single file with **detection** of a competing
  claim (slice 03) is the honest v1 boundary.

## Consequences

- (+) Zero history pollution; no merge conflicts on the resume path.
- (+) Reuses an existing plugin convention rather than minting a fourth namespace.
- (+) The fingerprint stays a clean staleness oracle, because capturing does not itself dirty the tree.
- (−) The snapshot is lost on a fresh clone or a cleaned tree — accepted: it is by definition
  ephemeral, and everything durable already lives in `docs/`.
- (−) Nothing is shared with a teammate. Accepted for v1; the partitioned option above is the
  documented path if that need appears.
- Open (→ DELIVER): whether `.session-handoff.md` should be per-repo or per-worktree, given
  `EnterWorktree` and workflow isolation put multiple trees on one initiative.

## Amendment — the partitioned option is adopted (2026-08-14)

Status: accepted · Feature: `single-issue-per-feature`, slice 04 · **Amends, does not supersede.** The
decision stands: the snapshot remains a single git-ignored root dotfile. What changes is that the second
half of this ADR's own alternatives list now ships.

### The trigger is this ADR's own consequence line

Quoted verbatim from *Consequences* above:

> (−) Nothing is shared with a teammate. Accepted for v1; the partitioned option above is the documented
> path if that need appears.

And from *Alternatives considered*:

> **Partitioned local + board**, per `phil:issue-board`'s *One system of record per scope* — local owns
> in-flight detail, the forge owns what others see, the issue number is the only join. This is the likely
> end state and is **deferred, not rejected**.

The need appeared. On 2026-08-14 the owner confirmed that teammates are real or imminent, which validated a
premise no persona or job in `docs/product/` had carried — every one of them described a single developer
working with AI agents. `make-in-flight-work-transferable` and `morgan-feature-owner` were registered to
close that gap, and this ADR's deferred path is the surface they need.

### What is adopted, exactly as written

**Local owns in-flight detail; the forge carries what others need; the join is the issue number.**
`/phil:handoff` writes `.session-handoff.md` **first**, then refreshes a generated, delimited, timestamped
projection of the why, the next action, and the work stack onto the feature's card. `/phil:resume` is
unchanged and reads only the local file.

### Why the original anxieties do not fire

- **Anxiety C — session scratch is world-readable.** Still true, and now a **deliberate trade** rather than
  a force avoided. The local file keeps in-flight scratch; the projection carries only what a teammate needs
  to resume. Recorded as a facet on `carry-work-across-session-boundaries` in `docs/product/jobs.yaml`.
- **Anxiety B — two authorities drift.** Answered *structurally*, not by discipline: the projection is
  **write-only**. Nothing reads it back, at capture or at read-back, so there is no second authority to
  disagree. This is also why the original rejection of the board *for in-flight scratch* still holds — what
  was rejected was reading state back from an issue, and that is not what this does.
- **The concurrency argument that decided this ADR is untouched.** The snapshot stays uncommitted, so no
  merge conflict enters the resume path and the fingerprint remains a clean staleness oracle.

### Accepted cost

A teammate sees only what the last `/phil:handoff` projected. A projection can lag only if work continued
after the handoff, so the window is narrow — but where no capture ever ran, the card must render the stack
as `unknown` and never as empty. Empty asserts there were no diversions; `unknown` asserts nobody wrote them
down.

### Still out of scope

Multi-session and multi-person arbitration. Competing claims are **detected, not resolved** — the v1
boundary, inherited unchanged. Two people claiming one feature is more likely now, and detection is still
the honest limit.
