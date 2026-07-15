# ADR-011 — adversarial-review: hard/soft split, prose oracles, and the honesty label

Status: accepted (DESIGN wave, 2026-07-15) · Feature: adversarial-review · Resolves DISCUSS open Q (oracle types) + C2/C4

## Context

The feature's defining risk is anxiety (A): an all-soft-critic loop dressed as a sound gate —
"a graded essay presented as a verified plan" (the tri-agent / LLM-Modulo warning; tri-agent
framework = Zhao, KDD '25, read via the harebrain summary
`docs/research-summaries/tri-agent-clarification/` in the sibling `harebrain` repo). DISCUSS locked
C2 (partition findings hard-checkable vs soft) and C4 (when no oracle backs the review, label it a
soft DRAFT SIGNAL, never a sound gate). DESIGN must fix *what counts as a hard oracle* — and because
this is a Claude Code plugin, the targets are usually **prose** (skills / agents / rules / docs),
not code with a test suite. "Hard oracle = test suite" is too narrow.

## Decision

**"Hard-checkable" = any DETERMINISTIC check available for the target, generalized across target
type. The verdict carries `overall_label = sound-gate` iff ≥1 hard oracle backs it, else
`draft-signal`. Each finding is tagged `kind: hard | soft`.**

| Target type | Hard oracle → `hard` findings (run or inherit) | Soft → `soft` findings (adversarial judgment) |
|---|---|---|
| Code | test suite (reuse `skills/shared/test-runner-detection.md`); lint / types | design/intent fit, missed requirement |
| **Prose** (skill/agent/rule/doc) | self-test fixture pass, dead-link / broken skill-ref check, frontmatter validity, file-length limit, required-citation presence — the same checkable-prose taxonomy `phil:work` FRAME uses | clarity, factoring, whether it *actually* achieves the stated intent |

- The reviewer **runs** available deterministic checks (or **inherits** a result already produced —
  ADR-005 lineage, never re-implement an oracle) and reports them as `hard` findings citing the
  actual result (exit code / failing test / the broken ref), never a prediction.
- Everything requiring subjective judgment is a `soft` finding: adversarial, span-and-evidence,
  `CANNOT_ASSESS` when unsupportable (C5).
- **`overall_label`** is mechanical: `sound-gate` when at least one hard oracle backed the review,
  else `draft-signal`. A `draft-signal` verdict must never be consumed (standalone or by a future
  host) as a passed sound gate — this is C4, and it is the discipline that stops the tool becoming
  the theatre it exists to prevent.
- **Slice sequencing:** slice 01 (WS) is soft-only → always `draft-signal`; slice 02 adds the code
  oracle + the partition + `sound-gate`; the broader prose-oracle catalog (beyond the WS checks)
  lands in DISTILL.

## Alternatives considered

- **Hard oracle = test suite only** — rejected: the majority of this plugin's targets are prose;
  it would make almost every review `draft-signal` and waste the deterministic prose checks that
  genuinely exist (dead links, frontmatter, self-test pass).
- **Let the reviewer decide the label by judgment** — rejected: the label is the anti-theatre
  guarantee; a soft judgment about "am I sound?" is exactly the correlated-error trap. The label
  must be a mechanical function of "did a deterministic oracle back this?", not the reviewer's
  opinion.
- **No label; always advisory findings** — rejected: without the sound-gate/draft-signal
  distinction, a future host can't tell a verified finding from an argued one, and C4's protection
  disappears at the composition boundary.

## Consequences

- (+) Honest by construction: the label is derived, not asserted; soft reviews cannot masquerade
  as sound.
- (+) Prose targets get real hard checks, not just opinions — the plugin's actual use case is
  first-class.
- (+) The `kind` tag lets a future host route hard vs soft differently (e.g. block on a hard
  failure, advise on a soft one) with no re-judging.
- (−) The prose-oracle set is open-ended; v1 ships a bounded subset (self-test / links / frontmatter
  / length / citations) and defers catalog breadth to DISTILL. A self-test fixture asserts a
  no-oracle target is never labeled `sound-gate` (C4 regression guard).
