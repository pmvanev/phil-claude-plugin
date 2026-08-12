# Feature Delta — session-handoff

Forge: pmvanev/phil-claude-plugin#9 · Wave: DISCUSS (entered 2026-08-12)
Density: lean + ask-intelligent (`~/.nwave/global-config.json`)
Rendered Tier-2 expansion: `alternatives-considered` [WHY] — accepted 2026-08-12, trigger:
cross-context complexity (5 bounded contexts, threshold ≥3). Recorded here because this repo has no
`scripts/shared/telemetry.py`, so no `DocumentationDensityEvent` could be emitted.

---

## Wave: DISCUSS / [REF] Persona ID

**`kai-session-relay`** — Kai, a developer carrying multi-session AI-assisted work in a repo using
the phil plugin. Hands the baton from one session to the next, and is the one who pays when the
handoff drops.

**Registered in SSOT** at `docs/product/personas/kai-session-relay.yaml` (user-approved 2026-08-12).
No existing persona fit: Quinn owns invisible technical initiatives, Rowan wants an independent
adversary, Avery adjudicates qualitative evidence, Tess maintains tests. A new persona per feature is
this repo's established pattern (Tess ← refactor-tests, Devon ← ux-standards-rule, Quinn ← phil-work,
Avery ← edd-loop, Rowan ← adversarial-review).

Sibling to Quinn: Quinn wants discipline *within* an initiative, Kai wants continuity *across* the
session boundary that cuts through it.

## Wave: DISCUSS / [REF] JTBD one-liner

When a session ends mid-initiative, Kai wants the next session to resume with the reasoning, the
intended next action, and the right entry-point already in hand — so momentum survives the boundary
instead of being re-explained or freelanced away.

## Wave: DISCUSS / [REF] Locked decisions

- **[D1]** Feature type = **cross-cutting**. Rationale: spans session lifecycle (hooks), the forge
  board, local artifacts, `nw-continue`/`nwave-slice-status` interop, and entry-point routing.
  Matches `adversarial-review`'s classification rather than `phil-work`'s narrower
  infrastructure/tooling framing. (User, 2026-08-12)
- **[D2]** Walking skeleton = **yes**, slice 01. Rationale: 3-for-3 precedent in this repo
  (`phil-work` 5 slices, `edd-loop` 2, `adversarial-review` 3, slice 01 the WS in each), and the
  core shape is unsettled — a WS settles snapshot-vs-reconstruct empirically instead of by argument.
  (User, 2026-08-12)
- **[D3]** UX research depth = **comprehensive**. Rationale: the damaging failure mode
  (bootstrapping confidently from a stale snapshot) lives in the error path, which lightweight
  depth skips. (User, 2026-08-12)
- **[D4]** JTBD analysis = **yes** (not the infrastructure-only escape valve). Rationale: forced —
  the escape valve is permitted only for pure internal changes with no user-visible surface, and
  the reviewer rejects it for anything user-facing. This feature ships developer-invocable commands.
  (Forced by `nw-discuss` Decision 4)
- **[D5]** Five categories of lost state are in scope, including **the how**. Rationale: the user
  named a fifth category beyond the four proposed — a fresh session performing work inline that an
  nWave command or other entry-point should have driven. See *Scope Assessment* for the consequence.
  (User, 2026-08-12)

## Wave: DISCUSS / [REF] Job story

Registered against a **new** job — no job in `docs/product/jobs.yaml` covers it. Nearest neighbours
and why they do not:

| Existing job | Why it does not cover this |
|---|---|
| `deliver-invisible-work-with-discipline` (Quinn) | Owns discipline *within* one initiative; says nothing about the session boundary |
| `prove-qualitative-expectations-with-evidence` (Avery) | Proves intent was met; not about carrying state forward |
| `get-independent-adversarial-critique-of-completed-work` (Rowan) | Judges completed work; handoff is about incomplete work |

**Job story:**

> When a session ends mid-initiative — context exhausted, the day over, or compaction hit — I want
> the next session to pick up with the reasoning, the intended next action, and the correct
> entry-point already in hand, so I can keep momentum instead of re-explaining the state of play or
> watching a fresh agent freelance work that a command should have driven.

### The five categories of lost state

Ranked by whether a fresh session can recover them unaided — which is the whole design axis, because
anything recoverable that a snapshot also records becomes a second authority that can drift.

| # | Category | Recoverable from artifacts? | Who owns it today |
|---|---|---|---|
| 1 | **The why** — decisions made verbally, approaches tried and ruled out, why work stopped | **No.** Never written down anywhere | Nothing |
| 2 | **The how** — which command / skill / entry-point should drive the work | **No.** The card describes work, not method | Nothing (issue #10) |
| 3 | **The what-next** — the intended next action | Partly; guessing it wrong is worse than not guessing | `continue.md` PENDING section, by hand |
| 4 | **The board/queue position** — which card was claimed, and why it was next | The board knows the card's status, not which session claimed it | Board (partially) |
| 5 | **The where** — file, step, branch, commit | **Largely yes** | `/nw-continue`, `/phil:nwave-slice-status` — for nWave features only |

Category 5 is largely solved and must not be re-recorded. Categories 1 and 2 are unrecoverable by
any reconstruction, because they were never artifacts — that is the irreducible core of this feature.

### Dimensions

- **Functional** — Capture the state a fresh session cannot derive (the why, the how, the intended
  next action, the claimed card), surface it at session start, and route the session to the correct
  entry-point — without becoming a second authority over facts the artifacts already own.
- **Emotional** — Relief from re-explaining the state of play at the top of every session;
  confidence the next session resumes *correctly* rather than plausibly-but-wrongly; trust that a
  snapshot is either current or honestly says it is not.
- **Social** — A teammate, or a future self, can see what was in flight and why it stopped; being
  someone whose work gets picked up cleanly rather than restarted.

### Four forces

- **Push** — `continue.md` (108 lines) and `todo.md` (19 lines) are hand-maintained resume notes,
  both scoped to a single feature rather than a session, and both stale: the newest date in either
  is 2026-07-01 with roughly a dozen commits since. `/nw-continue` reconstructs only wave-managed
  nWave features. A fresh session performs work inline that a command should have driven. The *why*
  is never recorded anywhere at all.
- **Pull** — One command to put the session down and one to pick it up, such that resumption is not
  a re-briefing; and a card or snapshot that names the entry-point so the agent routes instead of
  freelancing.
- **Anxiety** —
  - **(A)** A snapshot the human must remember to update goes stale silently, and a stale handoff is
    *worse than none* because the next session trusts it. This is the force the design is built
    against — it is the observed failure of `continue.md`, not a hypothetical.
  - **(B)** Two authorities over the same state (a local file and the board) drift. `phil:issue-board`
    already forbids exactly this under *One system of record per scope*.
  - **(C)** Session scratch published to a board is visible to everyone who reads the board.
  - **(D)** Ceremony on work that did not need it — the anxiety `phil:work` (B) and `edd` (B) both
    carry, countered there by an off-ramp.
- **Habit** — Hand-writing `continue.md`; re-explaining state in the first prompt of each session;
  letting the agent start freelancing and correcting it mid-flight.

### Opportunity score

`not-scored` — single new job, priority by default. Consistent with every prior job in
`docs/product/jobs.yaml`.

## Wave: DISCUSS / [REF] Scope Assessment

**Verdict: OVERSIZED — 2 signals fired. A split is required before Phase 2 journey investment.**

| Signal | Fired? | Evidence |
|---|---|---|
| >3 bounded contexts or modules | **YES** | Five: session lifecycle/hooks · forge board · local artifacts · nWave interop (`nw-continue`, `nwave-slice-status`) · entry-point routing |
| Multiple independent user outcomes that could ship separately | **YES** | Three: (a) capture and restore the why + next action; (b) route the session to the correct entry-point; (c) link a session to a claimed board card |
| >10 user stories | not established | Stories not yet drafted — not claimed as a signal |
| WS needs >5 integration points | no | The thinnest path touches a file and a session boundary |
| Effort >2 weeks | not established | Plausible, but no reference class measured — not claimed |

Two signals is the threshold, so this is oversized on evidence rather than on a hunch. Precedent:
`phil-work` fired 4 signals and split into 5 slices.

### Consequence for issue #10

Outcome (b) — routing the session to the correct entry-point — **is** issue #10. Because D5 puts
"the how" inside this job, #10 is no longer cleanly separable as a standalone board issue: it is one
of this feature's independent outcomes, which under `phil:nwave-issue-board`'s mapping makes it a
**slice of this feature**, not a sibling issue.

This reverses the reasoning used to file it separately, and the reversal is a decision for Phase 2.5
slicing, not for now. Both readings are still live:

- **Fold in** — #10 becomes a slice card under #9, so one design covers card-side and session-side
  routing and they cannot contradict each other.
- **Keep separate** — #10 ships a one-line fix to a shipped skill without waiting on this feature's
  DISCUSS wave; the standalone-fix argument that justified filing it has not weakened.

Recorded here so the decision is made deliberately at slicing rather than defaulted into.

## Wave: DISCUSS / [REF] Journey

SSOT: `docs/product/journeys/session-handoff.yaml`. Comprehensive depth per D3.

**Happy path:** wind-down → capture → bootstrap → route → resume.

**Emotional arc:** pressured → relief → cautious confidence → trust → momentum (upward).

**The two load-bearing design rules**, both derived from the anxieties rather than from taste:

- **Freshness is a verdict, not a footnote.** Read-back computes `current` / `stale` from a tree
  fingerprint and states it *before* presenting any resume content. Anxiety A is gated here.
- **The `where` is deliberately not a shared artifact.** File, step, and branch are derived at
  read-back from the artifacts that own them. Carrying them in the snapshot would create the second
  authority anxiety B forbids.

Eight error paths are mapped in the SSOT journey. The three that shape the design: a stale
fingerprint refuses to resume silently; a session that advanced nothing writes no snapshot; an
undeterminable entry-point is stated and asked about, never defaulted to inline work.

## Wave: DISCUSS / [REF] Slices and order

Three slices, one per independent outcome from the scope assessment. Briefs in
`docs/feature/session-handoff/slices/`. All carpaccio taste tests pass — recorded per brief.

| # | Slice | Learning hypothesis — disproves… | Depends on |
|---|---|---|---|
| 01 | Snapshot and resume (**WS**) | …that recording beats reconstructing | — |
| 02 | Entry-point routing (absorbs #10) | …that a written instruction is sufficient | 01 (session-side half only) |
| 03 | Claimed-card link | …that the board already carries enough | 01 |

**Order rationale** — highest learning leverage first, per the Phase 2.5 rule:

1. **Slice 01** tests the feature's central bet. If recording does not beat reconstructing, the whole
   design pivots, and every later slice consumes its snapshot format — so a failure here is cheapest
   first.
2. **Slice 02** removes a correction the user currently repeats on every nWave pickup, and its
   card-side half can ship without slice 01 if that slips.
3. **Slice 03** is the most mechanical and tests the narrowest claim against the surface (the board)
   most likely to already cover it.

Each slice carries a same-day dogfood moment against this repo's real state — a real commit SHA, the
genuinely stale `continue.md`, and the live board including its real two-cards-In-Progress condition.

## Wave: DISCUSS / [REF] Driving ports

Inbound surfaces, provisional until the mechanism is settled in Phase 2:

- **Slash command(s)** — the snapshot and bootstrap entry points, whatever their final shape
  (two commands, one command with two modes, or a mode on an existing command).
- **Session lifecycle hooks** — a candidate, not a commitment: `Stop`, `SessionEnd`, or `PreCompact`.
  Anything requiring the user to remember to snapshot inherits `continue.md`'s staleness failure
  (anxiety A), which is the argument for a hook; the argument against is that a hook fires on every
  session end whether or not there was anything worth recording.

## Wave: DISCUSS / [REF] WS strategy

**Provisional: Strategy C (real local resources) if the snapshot target is local; Strategy B (real
local + fake costly) if it writes to the forge.** Per Mandate 5 the WS adapter strategy is the DISTILL
acceptance designer's auto-detected call with user confirmation — not a DISCUSS decision — so this is
recorded as a read, not a ruling.

The fork is real: filesystem and git are real-adapter-always per the Mandate 5 resource table, but
`gh`/`glab` is an external network dependency that the WS should not depend on, which pushes toward a
faked forge adapter plus a contract test.

Brownfield incremental (additive), as with every prior feature here: the plugin exists and this is
added alongside it. Not the env-switching configurable strategy — no expansion trigger fired.

## Wave: DISCUSS / [REF] Pre-requisites

- **None blocking.** No prior DISCOVER or DIVERGE wave ran for this feature
  (`docs/feature/session-handoff/` did not exist before this wave).
- `docs/product/jobs.yaml`, `docs/product/architecture/brief.md`, and the four existing personas were
  read as SSOT input. `docs/product/vision.md`, `docs/project-brief.md`, and `docs/stakeholders.yaml`
  do not exist in this repo.
- **SSOT writes pending confirmation** of the job story above: a new job in `jobs.yaml`, a new
  `personas/kai-session-relay.yaml`, and a new `journeys/session-handoff.yaml`.

## Wave: DISCUSS / [REF] User stories

All three carry `job_id: carry-work-across-session-boundaries`. All three are user-visible value
stories — **no slice is `@infrastructure`-only**, so the slice-composition hard gate passes.

**Command names below are provisional.** Whether this is two commands, one command with two modes, or
a mode on an existing command is an open DESIGN question (see *Driving ports*). The pitches are
restated if that changes; what they pin is the observable output, not the spelling.

### Story 1 — Snapshot and resume (slice 01, WS)

As Kai, I want to record what a fresh session cannot derive and read it back with a freshness verdict,
so resuming is not a re-briefing.

#### Elevator Pitch
Before: when a session ends mid-initiative, the reasoning and the intended next action exist only in
that session; the next one needs a re-briefing.
After: run `/phil:handoff` → sees `snapshot written · 3 decisions · next: <action> · fingerprint a1b2c3d`;
then in a fresh session run `/phil:resume` → sees `current`, or
`stale — HEAD moved a1b2c3d → e4f5g6h`, followed by the why and the next action.
Decision enabled: whether to trust the resume point and continue, or discard it and reconstruct from
artifacts.

### Story 2 — Entry-point routing (slice 02)

As Kai, I want a card and a resume point to name the command that owns the work, so a fresh session
routes instead of freelancing.

#### Elevator Pitch
Before: picking up a card, the agent reads a work description and starts doing the work inline; the
user has to say "use the nWave skill" on every pickup.
After: run `/phil:resume` on a wave-labelled feature → sees `owner: /nw-execute (wave: deliver)` and the
session invokes it rather than editing files directly.
Decision enabled: whether the work is being driven by the command that owns it, without having to
police it.

### Story 3 — Claimed-card link (slice 03)

As Kai, I want the claimed card and the basis for it being next carried across the boundary, so
resumption targets the same card.

#### Elevator Pitch
Before: the board records that a card is In Progress but not which session claimed it or why it was
next — two cards can sit In Progress with no record of which is live.
After: run `/phil:resume` → sees `card: #11 · basis: WS, everything depends on its snapshot format`,
plus `competing claim: <other snapshot>` when one exists.
Decision enabled: whether to resume the same card or deliberately switch.

Acceptance criteria are embedded per slice brief in `docs/feature/session-handoff/slices/` rather than
restated here — one authority per fact.

## Wave: DISCUSS / [REF] Outcome KPIs

| # | KPI | Target | Measurement |
|---|---|---|---|
| KPI-1 | Resumes needing a clarifying question the snapshot should have answered | **<20%** over the first 10 real resumes | Counted by hand during dogfooding; this is slice 01's hypothesis made numeric |
| KPI-2 | Pickups where the user must say "use the nWave skill" | **0** across 5 consecutive nWave pickups | Counted by hand; slice 02's hypothesis made numeric |
| KPI-3 | Resumes that proceed on a stale snapshot without stating staleness | **0 — hard** | Self-test fixture: stale fingerprint must produce a `stale` verdict before any briefing |
| KPI-4 | No-op sessions that write a snapshot anyway | **0** | Self-test fixture: session that advanced nothing writes nothing (anxiety D) |
| KPI-5 | Facts duplicated between the snapshot and an artifact that owns them | **0** | Review of the snapshot schema against the five-category table; the *where* must be absent |

KPI-3 and KPI-5 are the two that encode the anxieties rather than the features, which is why both are
hard zeros and both are fixture-measured rather than counted by hand.

## Wave: DISCUSS / [REF] Definition of Ready — validation

| # | DoR item | Status | Evidence |
|---|---|---|---|
| 1 | Job traceable | ✅ | New job `carry-work-across-session-boundaries` in `jobs.yaml`; all 3 stories carry it |
| 2 | Persona defined | ✅ | `personas/kai-session-relay.yaml` |
| 3 | Journey mapped | ✅ | `journeys/session-handoff.yaml` — 5-step happy path + 8 error paths |
| 4 | Stories have elevator pitches | ✅ | All 3, with observable output; command names flagged provisional |
| 5 | ACs testable | ✅ | Given-When-Then per slice brief, fixture-checkable, pinned to real repo state |
| 6 | Slices ≤1 day, learning hypothesis each | ✅ | 3 briefs; all carpaccio taste tests recorded per brief |
| 7 | Walking skeleton identified | ✅ | Slice 01 — snapshot + read-back, end-to-end, forge deliberately excluded |
| 8 | Outcome KPIs with targets | ✅ | KPI-1…5; two are hard zeros and fixture-measured |
| 9 | Scope right-sized / split confirmed | ✅ | OVERSIZED on 2 signals; 3-slice split confirmed by user 2026-08-12 |

**Requirements completeness: 0.95.** Stated with its residue named so the number is auditable rather
than asserted. Specified: what state is captured, what must not be captured, what verdict is required
before a briefing, what must never happen (KPI-3/4/5), and the error paths for every high-risk step.
Deferred, all mechanism rather than requirement:

- Snapshot surface — local file, board, or both partitioned by scope (DESIGN)
- Trigger — explicit command versus lifecycle hook (DESIGN; slice 01 uses explicit invocation so this
  cannot block the WS)
- Command topology — two commands, one with two modes, or a mode on an existing command (DESIGN)

One genuine **requirements-level** gap, carried from the absorbed issue: whether a card with **no** wave
label gets a routing line at all. Slice 02 covers only the wave-labelled case, and most cards on this
board are not nWave work.

**Per-wave peer review: skipped**, per the skill's default. None of the four triggers fired — the DoR
surfaced no ambiguity, the JTBD was user-confirmed, there is no vendor-neutrality surface, and no
review was requested. The mandatory consolidated review fires at the end of DISTILL with all waves
visible.

## Wave: DISCUSS / [REF] Out-of-scope

Provisional — firmed up in Phase 3.

- **Re-recording what artifacts already own.** Category 5 (the where) is `/nw-continue`'s and
  `/phil:nwave-slice-status`'s; this feature does not duplicate it.
- **Syncing a local file with the board.** Forbidden by `phil:issue-board` *One system of record per
  scope*. If both surfaces end up carrying state, they partition by scope with the issue number as
  the only join.
- **Writing back to `docs/feature/`** from a forge issue. `phil:nwave-issue-board` is one-way.
- **Cross-session concurrency control.** Multiple simultaneous sessions are routine in this repo
  (workflows, subagents); arbitrating between two live sessions' snapshots is a separate problem and
  is not solved here.

## Wave: DISCUSS / [WHY] Alternatives considered

Tier-2 expansion. What was weighed and rejected per locked decision — and, for the three questions
DESIGN inherits, the state of the argument rather than a verdict, because those are not settled.

### Per locked decision

**[D1] Feature type — cross-cutting**

| Alternative | Why rejected |
|---|---|
| infrastructure/tooling (`phil-work` D1 verbatim) | Accurate for a single tactical command. This one spans five contexts and interoperates with two existing reconstruction commands plus the board — and classifying it narrowly would have *hidden* the bounded-context signal that later fired OVERSIZED. The classification is load-bearing, not cosmetic. |
| user-facing | Truest to the literal option list, since the developer is the end user. Rejected for consistency: every prior developer-invoked command here is infrastructure or cross-cutting, and the classification sets DESIGN's expectations about what "user" means. |

**[D2] Walking skeleton — yes, slice 01**

| Alternative | Why rejected |
|---|---|
| "Depends — evaluate first" | The literally-correct answer for brownfield. Costs a round trip to reach a conclusion that 3-for-3 precedent (`phil-work`, `edd-loop`, `adversarial-review`) already predicts. |
| No skeleton | The core shape is unsettled. A WS settles record-vs-reconstruct empirically; without one, that question gets decided by argument, which is how a wrong premise survives to DELIVER. |

**[D3] Depth — comprehensive**

| Alternative | Why rejected |
|---|---|
| Lightweight | Skips error-path mapping. The failure that does real damage — a stale snapshot trusted — *is* an error path, so lightweight would have designed around the happy case only. |
| Deep-dive | One developer, one repo, one persona. Every prior persona here was bootstrapped from a single feature; multi-persona research has nothing to consume it. |

**[D4] JTBD — yes.** No alternative existed. The escape valve is structurally unavailable to a feature
shipping developer-invocable commands, and the reviewer rejects it for any user-facing surface. Recorded
as forced rather than chosen, so DESIGN does not read it as a considered judgment.

**[D5] Five categories including "the how."** The rejected alternative was my own: four categories, with
"the how" left outside the job as standalone issue #10. The user's answer overturned it. Worth recording
because the consequence was structural, not cosmetic — it converted #10 from a sibling issue into one of
three independent outcomes, and therefore into a slice.

**[D6] Three slices**

| Alternative | Why rejected |
|---|---|
| 4 slices — staleness split out | Would ship a walking skeleton whose snapshot carries a timestamp but no staleness verdict. That skeleton exhibits the exact failure the feature exists to fix (`continue.md`), so the WS would validate the wrong thing. Staleness stays inside slice 01 as AC 3. |
| 2 slices — board link folded into 01 | Pulls the forge into the walking skeleton, forcing WS strategy from C (real local) to B (faked forge adapter). A thicker skeleton bought for the *least* uncertain of the three outcomes. |

**[D7] #10 folded in.** The standalone argument — a one-line fix to a shipped skill should not wait on a
DISCUSS wave — was sound while "the how" sat outside the job, and D5 removed that premise rather than
refuting the argument. It survives in slice 02's dependency split: the card-side half is independent of
slice 01 and can land first.

### The three questions DESIGN inherits

Not decisions. Alternatives with the argument recorded so DESIGN does not re-derive it.

**Snapshot versus reconstruct** — the feature's central bet.

- **Reconstruct-only** (extend `/nw-continue`): structurally cannot go stale, because the artifacts *are*
  the truth. Fatal limit: it cannot recover what was never an artifact. The why and the how were never
  written anywhere, so no amount of scanning finds them. **Not rejected** — it is slice 01's null
  hypothesis, and if the WS resumes cleanly without the snapshot, the feature pivots here.
- **Record-only**: rejected as a whole-design stance, because recording the *where* alongside the why
  creates the second authority anxiety B forbids.
- **Hybrid — record the unrecoverable, derive the rest**: the posture the five-category table encodes,
  and what slice 01 actually tests.

**Local file versus board**

- **Board-only**: rejected for in-flight scratch — the board is world-readable (anxiety C). Not rejected
  for the outward-facing tier.
- **Local-only**: chosen *for the walking skeleton specifically*, to keep the forge out of it. This is a
  WS-scoping choice, not a verdict on the feature.
- **Both, partitioned by scope**: the likely end state, and the shape `phil:issue-board` already
  prescribes — local owns in-flight detail, the forge owns what others see, the issue number is the only
  join. Nothing duplicated means nothing can drift.

**Explicit command versus lifecycle hook**

- **Explicit command**: inherits `continue.md`'s failure directly — anything the human must remember to
  run is something they will stop running. That is the observed failure, not a predicted one.
- **Hook** (`Stop` / `SessionEnd` / `PreCompact`): fires whether or not anyone remembers, but fires on
  *every* session end including ones that advanced nothing — countered by constraint C4 (no snapshot for
  a no-op). The open unknown is whether a hook sees enough context to capture the why at all, which is
  exactly the conditional SPIKE in slice 01's brief.
- Slice 01 uses explicit invocation deliberately, so this unknown cannot block proving the payload.

## Wave: DISCUSS / [REF] Wave decisions summary

For DESIGN to read first.

### Key decisions

- **[D1]** Feature type: cross-cutting — spans session lifecycle, forge board, local artifacts, nWave
  interop, entry-point routing.
- **[D2]** Walking skeleton: slice 01 — snapshot + read-back, forge deliberately excluded to keep the
  skeleton on real local resources.
- **[D3]** UX depth: comprehensive — the damaging failure mode lives in the error path.
- **[D4]** JTBD: mandatory (forced; user-facing surface).
- **[D5]** Five categories of lost state, including **the how**, which absorbed issue #10 into slice 02.
- **[D6]** Scope OVERSIZED on 2 signals → 3 slices, one per independent outcome. User-confirmed.
- **[D7]** Issue #10 folded in as slice 02 rather than kept standalone. User-confirmed; the
  counter-argument and the card-side/session-side dependency split preserve the original speed argument.

### Requirements summary

- **Primary job:** carry the state a fresh session cannot derive across the session boundary — the why,
  the how, the next action, the claimed card — while deriving everything the artifacts already own.
- **Walking skeleton scope:** slice 01 — capture the why + next action locally with a tree fingerprint,
  read it back with a `current`/`stale` verdict.
- **Feature type:** cross-cutting; target artifacts are prose-first (commands, skills, possibly hooks),
  consistent with every prior feature in this plugin.

### Constraints established

- **C1 — Freshness is a verdict, not a footnote.** A `current`/`stale` verdict precedes any resume
  content. A confidently-followed stale snapshot is the worst available outcome, and it is the observed
  failure of `continue.md`, not a hypothetical.
- **C2 — One system of record.** Nothing an artifact owns is copied into the snapshot; the *where* is
  derived at read-back. Forbidden by `phil:issue-board` *One system of record per scope*.
- **C3 — The projection stays one-way.** Nothing read from a forge issue is written back into
  `docs/feature/`, per `phil:nwave-issue-board`.
- **C4 — No ceremony on a no-op.** A session that advanced nothing writes no snapshot.
- **C5 — Unknown owner is stated, never defaulted.** No determinable entry-point means asking, not
  falling through to inline work.
- **C6 — Detection without resolution is an acceptable boundary.** Competing claims are reported;
  arbitrating between two live sessions is out of scope for v1.

### Upstream changes

None. No DISCOVER or DIVERGE wave ran for this feature, so no prior assumption was altered.

### Downstream note for DESIGN

Three mechanism questions are deliberately left open and are DESIGN's to settle: the snapshot surface
(local / board / partitioned), the trigger (command / lifecycle hook), and the command topology. Slice
01 is specified so that none of them blocks the walking skeleton. Separately, the wave → command table
in slice 02 is assembled from command descriptions and **must be verified against a run** before it is
written into a skill.
