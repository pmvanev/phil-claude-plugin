# Slice 06 — GitLab

**Goal:** Produce the same region on a GitLab repo, whose board is `status::` labels rather than a
Projects v2 Status field — same shape, different calls.

**Stories:** S6 (do all of it on GitLab)

## Learning hypothesis

**Disproves forge-neutrality** if the region's *shape* has to differ rather than just its values — if
GitLab needs different sections, different provenance categories, or a different marker convention, then
one command serving both forges is the wrong unit and the honest answer is two.

**Confirms**, if it passes, that `phil:issue-board`'s forge-neutral template survives being generated,
and that #32's defect is closed on both forges rather than one.

## IN scope

- Tier probe (Free vs Premium), and a **Free-shaped block on a Free instance**: no scoped-label
  convention written where scoped labels do not exist, manual `--unlabel` swaps recorded as such.
- Project and board ids; the `status::` label set; the docs root in GitLab's `/-/blob/<branch>/` form.
- `glab`'s JSON flag is `-O`; `-F` fails silently.
- Self-hosted instances: the host from the remote, and the certificate caveat `phil:issue-board`
  records.
- Projects v2 workflows recorded as **not applicable on this forge**, never as *none enabled*.

## OUT of scope

- GitLab epics, child work items, `rolledUpCountsByType`, and every other Premium/group mechanism. The
  block must be writable on Free.
- Any GitLab-only *content* in the block. If a section only makes sense on one forge, that is a finding
  about the template, which `phil:issue-board` owns.
- Reconciling a repo that has boards on both forges. One remote, one target ([D9]).

## Acceptance criteria

1. The region's shape is identical across forges; only values and the recorded calls differ — verified by
   diffing a GitHub-generated region against a GitLab one with values elided.
2. Tier is probed, and a Free instance produces a Free-shaped block.
3. `-O` is used throughout; no `-F`.
4. Projects-v2-specific facts render as *not applicable on this forge*, never as a benign default (C6).
5. A self-hosted instance unreachable over the network is reported as a connection failure and retried
   before anything is concluded — a single failure is usually the network.

## Dependencies

Slices 01–05. Everything about the shape is settled by then; this slice changes only the calls.

## Effort · reference class

≤1 day. Reference class: `phil:issue-board` itself, which carries both forges' mechanics side by side and
is the source for every call named above.

## Note on ordering

Last by design, and the reason is recorded because "later slice" and "out of scope" become
indistinguishable once a feature ships: GitLab is **in** the feature ([D10]). It is widest in surface and
narrowest in learning — by the time it runs, nothing about the design is still in question.

## Taste tests

| Test | Result |
|---|---|
| Ships 4+ new components? | No — one probe adapter |
| Depends on a new abstraction? | Reuses everything; adds no new one |
| Disproves a pre-commitment? | Yes — forge-neutrality of the region's shape |
| Synthetic data? | No — a real GitLab project |
| Identical to another slice but for scale? | No — same shape, different forge, which is the point |
