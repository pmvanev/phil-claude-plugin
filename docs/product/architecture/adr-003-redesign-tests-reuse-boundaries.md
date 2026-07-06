# ADR-003 — redesign-tests: new command + reuse boundaries

Status: accepted (DESIGN wave, 2026-07-06) · Feature: redesign-tests

## Context

`redesign-tests` deliberately changes what tests verify (implementation → behavior), gated by
human approval — the behavior-changing sibling of `refactor-tests` (DISCUSS D1–D5). Its loop is
~90% identical to the shipped `refactor-tests` loop: never-on-red baseline → propose → apply →
suite sanity check → human gate → commit/revert → prune → repeat. The differences are only the
**move set** (behavior-changing vs assertion-preserving), the **smell taxonomy** (behavioral
anti-patterns vs D5 structural smells), and the **backlog file**.

The packaging question: reuse the loop as a shared module, overload `refactor-tests` with a mode,
or ship a new command that copies the loop shape.

## Decision

Ship a **new** `commands/redesign-tests.md` + `skills/redesign-tests/SKILL.md` (command→skill
split, matching the plugin). Reuse boundaries:

- **REUSE as-is:** `skills/shared/test-runner-detection.md`.
- **REUSE read-only:** `review-code`'s Priority 6 (Test Quality) taxonomy for detection. `review-code`
  is left UNCHANGED (same posture ADR-001 took).
- **EXTEND (pattern-copy, not import):** copy `refactor-tests`' loop shape and safety mechanics —
  exactly as `refactor-tests` itself copied `phil:refactor`'s loop. Swap the move set for the
  behavioral rewrite catalog and the taxonomy for behavioral smells.
- **CREATE NEW:** the behavioral-smell detector + behavioral rewrite catalog, living in the skill.
  It writes `.test-redesign-backlog.md` (separate file, `review-code` backlog format by convention)
  so `redesign-tests` and `refactor-tests` never collide.

## Alternatives considered

- **`--behavioral` mode on `refactor-tests`** — rejected: overloads one command with two safety
  *contracts*. `refactor-tests` promises "coverage cannot shrink" (assertion-preserving);
  `redesign-tests` explicitly may change coverage. Hiding both behind one command muddies the single
  most safety-critical distinction and invites footguns — a user reaching for the safe tool could
  land in behavior-changing mode. This is the same overloading ADR-001 rejected for `--tests` on
  `review-code`.
- **Extract a shared `skills/shared/gated-approval-loop.md`** — best DRY, but refactors WORKING,
  shipped code (`refactor-tests` passed its self-test gates) and couples two deliverables. ADR-001
  explicitly deferred shared extraction until the two consumers "drift." We now have the second
  consumer — so this becomes a **documented follow-up**, extracted later from two known-good copies,
  not as part of this feature.

## Consequences

- (+) `refactor-tests` and `review-code` untouched; zero regression risk to shipped code.
- (+) The two safety contracts stay legible and separately invocable.
- (+) New command auto-discovered; no manifest change.
- (−) Loop mechanics now exist in two copies (`refactor-tests` + `redesign-tests`). If the shared
  safety mechanics change, both update. Accepted for v1; triggers the ADR-001 shared-extraction
  revisit (now that two consumers exist).
