# Evolution — session-handoff (`/phil:handoff`, `/phil:resume`)

Shipped 2026-08-12. Slices 01 and 02 of three; slice 03 deliberately deferred pending evidence.
Board: [#9](https://github.com/pmvanev/phil-claude-plugin/issues/9) with slices #11, #10, #12.

## Feature summary

Two commands carrying work across the session boundary. `/phil:handoff` records what a fresh session
cannot derive; `/phil:resume` reads it back, states a `current`/`stale` verdict **before** presenting
anything, and names the command that owns the work without running it.

The snapshot is `.session-handoff.md` at the repo root — git-ignored runtime state, reusing the
convention `.refactor-loop-ledger.md` already established.

## Business context (JTBD)

Job `carry-work-across-session-boundaries`, persona `kai-session-relay` — both new; no existing job
or persona covered the session boundary. Quinn owns discipline *within* an initiative; Kai wants
continuity *across* the boundary that cuts through it.

The push force was observed, not predicted: this repo's own `continue.md` was a 108-line
hand-maintained resume point stamped 2026-07-01, a dozen commits stale. It has since been retired to
`docs/evolution/2026-07-01-refactor-loop.md`.

## The design axis

Five categories of lost state, sorted by whether a fresh session can derive them unaided. That sort
decided the architecture, because **anything recoverable that a snapshot also records becomes a
second authority that drifts**.

| Category | Recoverable? | Disposition |
|---|---|---|
| The **why** — decisions, ruled-out approaches | No — never an artifact | Recorded |
| The **how** — which command owns the work | No — cards describe work, not method | Recorded (slice 02) |
| The **next action** | Partly; a wrong guess is costly | Recorded |
| The **claimed card** + basis | Board knows status, not claimant | **Deferred** (slice 03) |
| The **where** — file, step, branch | Largely yes | **Refused at capture**, derived at read-back |

## Key decisions

- **[D5]** "The how" is a fifth category of lost state (user). This absorbed standalone issue #10 into
  the feature as slice 02.
- **[ADR-013]** Snapshot is a git-ignored root dotfile — deliberately breaking ADR-006/009's
  committed lean. Those trails have one writer; a per-session snapshot has concurrent ones.
  Committing would convert a concurrency problem into a merge conflict on the resume path, and dirty
  the tree its own fingerprint reads.
- **[ADR-014]** CREATE NEW spine, REUSE by delegation. `/phil:work` already resumes, so the gate's
  default was EXTEND; the justification is coupling (it would own continuity for work it never
  launched, inverting ADR-005's arrow) plus coverage (only `phil:work` initiatives have a
  `progress.md` at all).
- **Left the nWave sequence after DESIGN.** The deliverable is prose, and this repo had already
  decided twice that skills+agents are authored, not TDD'd — `todo.md` 2026-06-17 and edd-loop DDD8.
  Built with `plugin-dev:skill-development`; DISTILL's fixtures were kept as the verification
  contract because DESIGN's own decomposition names `self-test/` as a component.
- **Routing names the owner; it never runs it** (user). Running `/nw-execute` from a read-back would
  route around resume's no-`Write`, no-`Edit`, read-only-`Bash` posture and make acting on a stale
  resume point automatic.

## Work completed

| Slice | Ships | State |
|---|---|---|
| 01 — snapshot and resume | `SKILL.md` spine, `commands/handoff.md`, `commands/resume.md`, `.gitignore` rule | **done** |
| 02 — entry-point routing | `Work this with:` line in `nwave-issue-board`'s generated block + `ROUTE`/`ROUTE-LIVE-WINS`/`ASK-OWNER` | **done** |
| 03 — claimed-card link | — | **deferred**, see below |

Also: `nwave-issue-board` gained fixture 16 (sixteen total); ADR-013 and ADR-014 added; `jobs.yaml`,
`personas/kai-session-relay.yaml`, `journeys/session-handoff.yaml` registered in SSOT.

## Verification

Acceptance contract: `skills/session-handoff/acceptance.feature` + ten golden fixtures. Fixtures
**01–08** cover the shipped slices; **09–10** cover slice 03 and are expected to fail.

Dogfooded against real state rather than paper-walked — `RESUME-CURRENT`, then `RESUME-STALE` across
a real commit with the distance quantified, the unreachable-commit branch confirmed against a bogus
SHA, and `ASK-OWNER` confirmed against the live board, which carries **zero** wave labels across 12
open issues.

Reviewed by `plugin-dev:skill-reviewer` and `plugin-dev:plugin-validator`. Both found real defects;
see below.

## What the reviews caught

Worth recording because both were defects a self-review missed:

- **The RECONSTRUCT path called `/nw-continue`, which *launches the next wave*.** A read-back that
  starts work — the worst thing this feature could do. `skills/nwave-slice-status/SKILL.md` exists
  because of that exact side effect. Corrected in the skill **and at source in ADR-014**, which had
  specified the dangerous delegate and would otherwise have kept teaching the bug.
- **The read-only guarantee was theatre.** `resume.md` withheld `Write`/`Edit` while granting bare
  `Bash`, which permits `rm` and `git checkout`. Now scoped to four read-only git verbs.
- **`agents/adversarial-reviewer.md` had invalid YAML frontmatter** — an unquoted colon-space — so
  the agent could not register. Pre-existing and unrelated; found and fixed.

Also corrected before shipping: the wave → command table, verified against nWave's wave declarations
rather than command descriptions, had **omitted DEVOPS entirely** (wave 4 of 6) and would have cited
`nw-design`'s internal agent dispatch as the user entry point.

## Known v1 boundaries / follow-ups

- **Slice 03 deferred, not abandoned** (#12). Its own hypothesis is that the board already carries
  enough, and across every dogfood run the `Next` field carried the work identity in prose. Its
  supporting evidence — two cards In Progress — turned out to be substantially board hygiene, since
  #3 had simply been left there. Building it now would answer the question by assumption. It ships
  when a real resume leaves someone asking "which card was I on?"
- **Anxiety A is mitigated, not closed.** Capture is explicitly invoked, so a forgotten snapshot is
  still possible — it reports `stale` rather than misleading, which is what makes it survivable. The
  `Stop`/`SessionEnd` hook is deferred behind a SPIKE: the unknown is not whether a hook fires, but
  whether it can see the *why*, which is the entire payload.
- **Cards with no wave label get no routing line.** The one genuine requirements-level gap carried
  from #10, and the common case on a mixed board.
- ~~`todo.md` still stands at the root~~ — **retired 2026-08-12**, folded into
  `docs/evolution/2026-07-01-refactor-loop.md` as an appendix. Every one of its items was already
  marked `DONE`; nothing in it was live. The repo root now carries no hand-maintained resume or
  backlog file, which is the condition this feature argued for.
- **Competing claims are neither detected nor resolved** in v1 — detection was slice 03's.
- Open (→ whenever slice 03 lands): whether the snapshot should be per-repo or per-worktree, given
  worktree isolation can put several trees on one initiative (ADR-013).

## Finalization notes

`/nw-finalize`'s pre-dispatch gate could not run: it verifies every step is `DONE` from
`deliver/execution-log.json`, and no DELIVER wave produced one. Finalized on the actual completion
evidence — fixtures, dogfood, review, git history — rather than a fabricated log.

Phase B migration was a no-op. Its destination map targets `docs/adrs/`, `docs/architecture/`,
`docs/ux/`, `docs/scenarios/` — none of which exist here, because the SSOT model already places ADRs,
journeys, and personas under `docs/product/` permanently.

The workspace `docs/feature/session-handoff/` is **preserved**, per Phase C step 3 and the repo's
actual practice: all four previously finalized features kept theirs. The skill's own Success Criteria
say to remove it, which contradicts its Phase C — the preserve half is the correct one.
