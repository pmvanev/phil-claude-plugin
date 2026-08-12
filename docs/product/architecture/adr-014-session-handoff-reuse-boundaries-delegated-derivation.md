# ADR-014 — session-handoff: reuse boundaries and delegated derivation

Status: accepted (DESIGN wave, 2026-08-12) · Feature: session-handoff · Resolves DISCUSS open questions 2 and 3

## Context

`/phil:work` already resumes. `skills/work/SKILL.md` records it plainly: with no argument it will
"resume the in-flight initiative from its `docs/work/<slug>/progress.md`: read the roadmap and the
per-wave status, and continue from the first wave not yet `done`." ADR-006 states the same intent —
`progress.md` "doubles as the resume source for an interrupted multi-wave run."

`/nw-continue` also resumes, by scanning `docs/feature/` for artifacts, and
`/phil:nwave-slice-status` derives a slice's step state read-only.

So session-handoff is **not** entering empty territory, and the DESIGN Reuse Analysis rule is
explicit: overlapping responsibility defaults to EXTEND, and CREATE NEW requires evidence that
extending is impossible or creates unacceptable coupling — "it's complex" does not qualify.

## Decision

**CREATE NEW for the capture-and-resume spine; REUSE by delegation for everything derivable.**

Two new commands over one new skill:

```
commands/handoff.md            thin loader  ->  capture
commands/resume.md             thin loader  ->  read back
skills/session-handoff/SKILL.md   spine: WIND-DOWN · CAPTURE · BOOTSTRAP · ROUTE · RESUME
```

The spine **never derives** what another component owns:

| Needed at read-back | Owner | How obtained |
|---|---|---|
| Where an nWave feature stands — wave, slice, step | the `nwave-slice-status` skill | Delegated, unmodified |
| A card's status and position | the forge, via `phil:issue-board` | Read at slice 03 |
| The why, the next action, the entry-point, the claimed card | **nothing — this feature** | Recorded at capture |

## Why CREATE NEW rather than EXTEND `progress.md`

The justification the gate demands is coupling, not complexity.

`/phil:work` resumes initiatives **it started**, from **its own** trail. Extending it to carry
session continuity would make it own continuity for nWave features and ad-hoc sessions it never
launched — which inverts its documented role as a general contractor for *invisible* work, and would
make `phil:work` depend on nwave. ADR-005 deliberately built `phil:work` to delegate to engines and
inherit their gates; making it the owner of every engine's continuity reverses that arrow.

The coverage arithmetic settles it independently: only `phil:work` initiatives have a `progress.md`
at all. An nWave feature has none, and an ad-hoc session has none. Extending `progress.md` would
serve roughly a third of the cases and still require a second mechanism for the rest — two
authorities over one fact, which is exactly DISCUSS anxiety B.

**The pattern is reused even though the component is not.** `progress.md`-as-resume-source is the
shape this feature adopts, and ADR-005's inherit-the-delegate rule is the discipline it follows.

## Why two commands rather than one

`/phil:work`'s no-argument-means-resume idiom is real in-repo precedent, and it works there because
the command drives the initiative either way — both readings do the same kind of thing.

Capture and read-back are not the same kind of thing: they happen at opposite ends of a session and
have opposite effects. A single command would need an implicit rule to disambiguate them, and
implicit state is precisely what this feature exists to eliminate. A tool whose own behaviour must be
inferred is a poor advertisement for honest, explicit state.

Rejected alternative — **fold into `/phil:work` or `/nw-continue` as a mode**: smallest surface
increase, strongest coupling, and it fails on the same coverage arithmetic as above.

## Trigger: command first, hook second

The `Stop` hook mechanism is already wired and firing in this plugin (`hooks/hooks.json` carries a
`Stop` notifier and a `PreToolUse` guard), so automation is proven infrastructure, not speculation.

It is nonetheless **deferred past slice 01**. The unknown is not whether a hook fires; it is whether
a hook sees enough context to capture *the why*, which is the entire payload. Automating first risks
shipping a mechanism that reliably captures only the derivable half — the half this design says must
not be recorded. Slice 01 uses explicit invocation so that a mechanism unknown cannot block proving
the payload; slice 01's conditional SPIKE settles the hook question once the payload is known to be
worth automating.

This leaves DISCUSS anxiety A (a snapshot the human forgets to update) live in v1. Accepted and
recorded: the staleness verdict (constraint C1) is what makes it survivable — a forgotten snapshot
reports `stale` rather than misleading the next session.

## Consequences

- (+) No existing skill is modified for slice 01; `/phil:work` and `/phil:nwave-slice-status` are
  composed unchanged.

**Correction (2026-08-12, found by the plugin-dev skill review).** This ADR originally listed
`/nw-continue` as the delegate for "where an nWave feature stands". That was wrong and dangerous:
`/nw-continue` computes the position and then *launches the next wave*, so a read-back delegating to
it would start work. `skills/nwave-slice-status/SKILL.md` exists precisely because of that side
effect — "Print the resume command as text. Never run it." The delegate is the read-only
`nwave-slice-status` skill, and **read-only is now the stated selection criterion** for anything on
the read-back path, not an incidental property.
- (+) Derivable state has exactly one authority, satisfying anxiety B structurally rather than by
  discipline.
- (+) The delegated derivation is what keeps the snapshot small — it records only what nothing else can.
- (−) Two new commands on the plugin's surface.
- (−) `continue.md` and `todo.md` are not subsumed. Out of scope per DISCUSS; worth revisiting once
  the snapshot proves itself. **Update 2026-08-12:** `continue.md` has since been retired to
  `docs/evolution/2026-07-01-refactor-loop.md` — not subsumed, but no longer competing from the root.
  `todo.md` still stands.
- (−) Anxiety A is only mitigated, not closed, until the hook lands.
- Open (→ DELIVER): slice 02 extends `skills/nwave-issue-board/SKILL.md` with the card-side routing
  line — the only planned edit to an existing skill, and its wave → command table must be verified
  against a run first.
