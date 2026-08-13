# Feature Delta — groom-issues

Forge: pmvanev/phil-claude-plugin#5 · Wave: DISCUSS ✓ (2026-08-12)
Density: lean + ask-intelligent (`~/.nwave/global-config.json`)

**Build path:** DISCUSS here, then authored with `plugin-dev` — not DESIGN/DISTILL/DELIVER. The
deliverable is a skill plus a thin command, and this repo settled twice that skills are authored
rather than waved (`todo.md` 2026-06-17; edd-loop DDD8). Same path `session-handoff` took.

---

## Wave: DISCUSS / [REF] Persona ID

**`robin-backlog-curator`** — Robin owns a board that other people, and a past self, also file into,
and pays when a card turns out to mean something other than what it said. Registered at
`docs/product/personas/robin-backlog-curator.yaml`.

Curator rather than steward: Quinn holds stewardship of the codebase; Robin holds the board that
decides what gets worked on it.

## Wave: DISCUSS / [REF] JTBD one-liner

When a board has accumulated half-finished cards, Robin wants it brought into shape with the
judgement calls put to a human rather than guessed — so the board can be trusted, and ranked over
understood work.

## Wave: DISCUSS / [REF] Locked decisions

- **[D1]** Feature type = **infrastructure/tooling**. One surface (a board) plus a mapping, not a
  concern spanning layers — narrower than `session-handoff`, matching `phil-work`. (User)
- **[D2]** Walking skeleton = **yes**, and it is **read-only**: scan and report, change nothing.
  #5 forbids applying any set-level operation unasked, so a read-only first slice delivers most of
  the value with none of the blast radius. (User)
- **[D3]** UX depth = **comprehensive**. The damaging failures here are irreversible and live in the
  error paths. (User)
- **[D4]** JTBD = **yes**, forced — a developer-invocable command has a user-visible surface.
- **[D5]** Loop pacing = **scan → report → user scopes → fix**. Chosen over report-only-backlog
  because a defect backlog file would be a second authority over issue state; chosen over
  issue-at-a-time because #5 is explicit that duplicate detection "cannot run inside a per-issue
  loop". (User)
- **[D6]** **No `groomed` marker** — no label, no timestamp block. Re-derive the defect table every
  run. Carried from #5 and confirmed: a stored marker lies the moment a human edits the issue.
- **[D7]** The **house-default body standard** ships with the skill and is overridable per project in
  `CLAUDE.md`. Without it, "appropriate description" is not checkable and grooming is taste. This is
  the gap #5 says must close first.

## Wave: DISCUSS / [REF] Resolved before design

Two positions #5 asked for, both answerable from work completed today:

- **Session state in an issue body is a groomable defect.** ADR-013 placed the session snapshot in a
  git-ignored root dotfile precisely because a board is world-readable. Scratch in a body is
  misplaced state, and grooming should say so.
- **A missing `Work this with:` line is *not* a body defect.** It is generated into the delimited
  `nwave:status` block by `phil:nwave-issue-board`. Grooming must never hand-write one — that is
  typing into a generated region, which the next refresh overwrites.

And #5's open risk is closed: **the cheap scan works on both forges.** The flag in the issue was
wrong (`-F` is `--output-format`); it is `-O/--output json`. Verified — one call returned 5 issues,
39 fields, **5/5 populated descriptions**, plus labels and milestone. `gh issue list --json body`
likewise. No N+1, so D6's scan-every-run design stands.

## Wave: DISCUSS / [REF] Scope Assessment

**OVERSIZED — 2 signals. Split confirmed by user.**

| Signal | Fired? | Evidence |
|---|---|---|
| >3 bounded contexts | **YES** | Four: the body standard · per-issue mechanical fixes · cross-issue set operations · consuming the milestone/nWave mapping |
| Multiple independently shippable outcomes | **YES** | Three: scan+report (read-only) · mechanical fixes · set-level operations |
| >10 user stories | not established | not claimed |
| WS needs >5 integration points | no | the skeleton is a read-only scan |
| Effort >2 weeks | not established | not claimed |

## Wave: DISCUSS / [REF] Slices and order

| # | Slice | Learning hypothesis — disproves… | Depends on |
|---|---|---|---|
| 01 | Scan and report (**WS**, read-only) | …that a defect oracle can be stated at all | — |
| 02 | Mechanical fixes within a scope | …that any fix is safe unasked | 01 |
| 03 | Set-level operations, all ask-first | …that set-level defects are detectable with actionable evidence | 01 |

Ordered by learning leverage. Slice 01 carries the feature's central bet: if the report reads as
taste rather than checkable findings, the house-default standard (D7) is insufficient and everything
downstream rests on nothing. It is also read-only, so a failed bet costs nothing but the reading.

## Wave: DISCUSS / [REF] Driving ports

| Port | Surface | Slice |
|---|---|---|
| `/phil:groom-issues` | Slash command — scan and report, holds no write tool | 01 |
| `/phil:groom-fix` | Slash command — applies the mechanical column inside a chosen scope | 02 |
| `/phil:groom-set` | Slash command — resolves merge, split, close and group, asking before each | 03 |

**Revised at slice 02, and again at 03.** DISCUSS planned one port, on the reasoning that scoping and
every judgement call happen inside the session through `AskUserQuestion` rather than as separate
commands. That held for the *decisions* and failed for the *tools*: a single command must carry every
write tool the feature will ever need, which destroys the scan's read-only guarantee (slice 02) and puts
a reversible label edit behind the same consent as an irreversible close (slice 03). The judgement calls
are still made in-session by `AskUserQuestion`; what the extra ports buy is that the tools a command
lacks are unreachable from it. Three ports, each holding the narrowest grant its job needs.

## Wave: DISCUSS / [REF] Journey

SSOT: `docs/product/journeys/groom-issues.yaml`. Comprehensive depth per D3.

**Happy path:** invoke → scan → scope → fix-mechanical → decide-set-level → report.
**Emotional arc:** wary → relief → control → momentum → confidence → trust (upward).

**The cost D6 buys, named plainly.** Because the defect table is re-derived every run and nothing is
stored, **a declined set-level candidate will be proposed again next run**. That is the price of
having no second authority. It is not a bug, and the report must say so — otherwise it reads as the
tool forgetting, and the user starts wanting the marker that D6 exists to refuse.

Six error paths are mapped in the SSOT journey. The two that shape the design: a partial scan must
never report "N clean", because a completeness claim over a partial read is the one output that
actively misleads; and a fix that would edit inside a generated region is refused outright.

## Wave: DISCUSS / [REF] Out-of-scope

- **Ranking.** `phil:rank-issues` owns it. Grooming settles what a card means; ranking settles order.
- **Deriving status.** `phil:nwave-slice-status` owns that, and `nwave-issue-board` already forbids a
  second derivation.
- **Writing inside generated blocks.** Ever.
- **Any set-level operation without asking** — merge, split, close, group.
- **A groomed marker**, in any form. D6.

## Wave: DISCUSS / [REF] Pre-requisites

- No DISCOVER or DIVERGE wave ran (`docs/feature/groom-issues/` did not exist before this wave).
- SSOT read: `jobs.yaml` (7 jobs), 5 personas, 6 journeys. `vision.md`, `project-brief.md`, and
  `stakeholders.yaml` do not exist in this repo.
- Depends on decisions already landed: **#7** (a milestone is a goal — grooming consumes this
  convention for the "ungrouped effort" defect rather than inventing a second one) and **#8**
  (ranking exists, and runs after grooming by advice rather than gate).

## Wave: DISCUSS / [REF] Wave decisions summary

### Requirements summary

- **Primary job:** make a board trustworthy — every card says what it means, defects between cards
  are surfaced with evidence, and every irreversible call is the human's.
- **Walking skeleton:** slice 01 — scan and report, read-only.
- **Feature type:** infrastructure/tooling; deliverable is prose (a skill + one command loader).

### Constraints established

- **C1 — No stored grooming state.** Re-derive every run; a marker is a second authority.
- **C2 — Nothing irreversible without asking.** Merge, split, close, group are all human calls.
- **C3 — Never write inside a generated region.**
- **C4 — A partial scan may not make a completeness claim.**
- **C5 — A clean board is reported clean.** No manufactured work.
- **C6 — The body standard is stated, not implied**, and is overridable per project.

### Upstream changes

None. No prior wave ran for this feature.
