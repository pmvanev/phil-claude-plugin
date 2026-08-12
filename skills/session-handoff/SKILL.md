---
name: session-handoff
description: Skill bundle for the phil:handoff and phil:resume commands — carries work across the session boundary. Records only what a fresh session cannot derive (the reasoning, the intended next action), stamps a tree fingerprint, and on read-back states a current/stale verdict before presenting anything. Refuses to record state an artifact already owns.
---

# Session handoff — capture and resume

Two commands over one spine. `/phil:handoff` puts a session down; `/phil:resume` picks the work up.

The value is narrow and specific: **record only what a fresh session cannot work out for itself.**
Everything else is derived at read-back from whatever already owns it. A snapshot that also records
the derivable becomes a second authority over the same fact, and the two drift.

Slice 01 scope. Entry-point routing is slice 02; the claimed-card link is slice 03. Neither is
implemented here — do not improvise them.

## What is worth recording

| Category | Recordable? | Why |
|---|---|---|
| **The why** — decisions made, approaches ruled out, why work stopped | **Yes** | It was never an artifact. No reconstruction can recover it. |
| **The next action** — what the session was about to do | **Yes** | Partly inferable, and a wrong inference is costlier than none. |
| The where — file, step, branch, commit, wave | **No** | Owned by `/nw-continue` and `/phil:nwave-slice-status`. Derive at read-back. |
| The entry point that owns the work | **No — slice 02** | Not built. |
| The claimed card and its basis | **No — slice 03** | Not built. |

## The snapshot

One file, `.session-handoff.md`, at the repository root. Git-ignored — it is runtime state, not
history. Never commit it; never write it anywhere under `docs/`.

```markdown
<!-- session-handoff:v1 -->
captured: 2026-08-12T17:30Z
commit: 083c953
dirty: no
<!-- /session-handoff:v1 -->

## Why

- Rejected the hook for v1 — it cannot see the why, and the why is the payload.
- The card-side half can ship before the session-side half.

## Next

Verify the wave-to-command table against a real run.
```

The delimited header is machine-readable with `grep`/`sed`; the body is prose for a human. Read the
fingerprint from the header, never by parsing the prose.

## CAPTURE — `/phil:handoff`

1. **Decide whether anything happened.** Establish whether the session advanced work: decisions
   reached, files changed, a next action formed. If none of these hold, take the `NO-OP` path below.
2. **Collect the why.** State the decisions reached and, critically, the approaches **ruled out and
   why**. A decision without its discarded alternatives invites the next session to re-propose them.
3. **Collect the next action** — one sentence, concrete enough to start from.
4. **Refuse the derivable.** If wave, slice, step, branch, or file position comes up, leave it out.
   Say plainly that it is left out because it is derived at read-back. This is not an optimisation;
   recording it is the defect.
5. **Stamp the fingerprint.** `git rev-parse --short HEAD` for `commit`; `git status --porcelain`
   non-empty means `dirty: yes`.
6. **Write `.session-handoff.md`**, overwriting any previous snapshot.
7. **Report** `CAPTURE`, and echo what was recorded so a mistake is visible immediately.

### NO-OP

A session that advanced nothing writes **no** file. Report `NO-OP` and say that nothing was
recorded and why.

Do not write an empty or placeholder snapshot. A resume point that says "no decisions, next action
unknown" is worse than none: the next session finds one, reads nothing in it, and learns to distrust
resume points generally.

Saying nothing was recorded is part of the outcome, not politeness — silence is indistinguishable
from the command having failed.

## BOOTSTRAP — `/phil:resume`

**Compute the verdict before presenting anything.** This ordering is the whole safety property.

1. **No `.session-handoff.md`?** Take the `RECONSTRUCT` path below.
2. **Read the fingerprint** from the delimited header.
3. **Compare against the tree now** — current short HEAD, and current dirty state.
4. **Branch on the comparison**, and state the verdict *first*:

**`RESUME-CURRENT`** — commit matches and the tree is as clean as it was. Say the resume point is
current, then present the why and the next action.

**`RESUME-STALE`** — commit differs, or the tree is dirty when the snapshot was clean. Say so
**before** any content, and quantify it:

```
STALE — snapshot at 4a91c02, HEAD is now e17bd55 (6 commits), working tree dirty.
The recorded next action may no longer apply.
```

The shape is what matters, not these values: both fingerprints, the distance between them, and the
tree state. Report the distance in whatever unit is available — commit count is best; a bare
"different" is acceptable; silence is not.

Then, and only then, show the recorded content clearly marked as historical. Do **not** present the
recorded next action as the thing to do now; offer it as what was intended at the time, for the
reader to judge.

A confidently-followed stale snapshot is the worst outcome this skill can produce. It is worse than
having no snapshot, because the next session acts on it. Never soften the verdict to "may be out of
date" when the fingerprint proves it is.

**`RECONSTRUCT`** — no snapshot exists. Derive the position from whatever owns it: `/nw-continue`
for an nWave feature, `/phil:nwave-slice-status` for a slice's step state, git for the branch and
recent commits. Present that, and **label it as reconstructed rather than recorded** — including
that the *why* is unavailable, because nothing derives it.

A recorded briefing carries reasoning that was witnessed. A reconstructed one carries position
inferred from files. They have different warranties; blurring them invents confidence.

## Deriving, not duplicating

At read-back, fetch the derivable from its owner rather than the snapshot:

| Wanted | Ask |
|---|---|
| Where an nWave feature stands | `/nw-continue` |
| A slice's step state | `/phil:nwave-slice-status` |
| Branch, HEAD, working-tree state | `git` |

Delegate; do not re-derive. These own their answers and have their own correctness gates.

Note the asymmetry, which is deliberate: at **capture** this state must be refused, and at
**read-back** it must be actively fetched. The rule is not "never touch position" — it is *never at
capture, always at read-back*.

## Decision outcomes

Report exactly one, by name, every run:

`CAPTURE` · `NO-OP` · `REFUSE-DERIVABLE` · `RESUME-CURRENT` · `RESUME-STALE` · `RECONSTRUCT`

`REFUSE-DERIVABLE` is reported alongside `CAPTURE` when derivable state was offered and left out.

## What this skill must never do

- Write the snapshot anywhere but the repo root, or commit it.
- Present a stale snapshot as current, or bury the verdict beneath the content.
- Record wave, slice, step, branch, or file position.
- Write a snapshot for a session that advanced nothing.
- Invent a next action that was not stated.
- Route work, name an owning command, or record a claimed card — slices 02 and 03, not built.

## Acceptance

`acceptance.feature` is the scenario SSOT; `self-test/` holds ten golden fixtures. Slice 01 must pass
fixtures **01–05**. Fixtures 06–10 cover slices 02 and 03 and are expected to fail until those ship.

Run the suite whenever this file or either command loader changes. Every failure mode here is
silent — a snapshot that records too much looks more complete, and a stale one presented as current
looks like a smooth resume.
