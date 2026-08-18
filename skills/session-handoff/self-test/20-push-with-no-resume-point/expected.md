# Expected — 20 (the first thing ever recorded is a diversion)

**Pins:** slice-01 AC4, and the header rule that AC4 is the only path to exercise.

**Expected decision:** `PUSHED`. A snapshot is created carrying the stack alone:

```markdown
<!-- session-handoff:v1 -->
captured: never
commit: 7e63578
dirty: yes
<!-- /session-handoff:v1 -->

## Stack

1. deploy script · the blocker's fix cannot be tested until deploys work · open since 2026-08-18T14:05Z
```

**`Why` and `Next` are absent, not empty.** No section, no heading, no placeholder. A `## Why` with nothing
under it asserts that the session reached no decisions; absence asserts that nobody was asked. This is the
`unknown` / `none` distinction the stack path already carries, applied to the other two payloads.

**`captured: never` is the load-bearing token and the reason this fixture exists.** The header cannot simply
be omitted: BOOTSTRAP reads the fingerprint from it, and a snapshot with no header is a file `/phil:resume`
has no defined behaviour over — not `RECONSTRUCT`, because a file exists; not a freshness verdict, because
there is nothing to compare. So `commit:` and `dirty:` are stamped from the tree at creation and the
fingerprint works normally.

But `captured:` must **not** be stamped, because **a push is not a capture**. `captured:` means *when the
payload was captured*. Writing a time there would assert a state of play was recorded when none was, and
would start the clock the staleness rule will eventually read. `never` says: there is a fingerprint, and
nothing has ever been captured against it.

**What a later `/phil:resume` does with this** — stated here because it is the half a `push` fixture cannot
show: it reports `RESUME-CURRENT` or `RESUME-STALE` on the fingerprint as usual, presents the stack, and
says the reasoning and the next action were **never recorded**. Not that they were empty.

**Gate failures:**

- Stamping `captured:` with a real time. This is the failure this fixture exists for, and it will look like
  completeness.
- Omitting the header entirely, leaving `/phil:resume` undefined over the file.
- Inventing a `Why` or a `Next` — including deriving one from the diff, the branch name, or the push reason.
- Emitting empty `## Why` / `## Next` headings.
- Taking the `NO-OP` path. A diversion is payload; a session that took one advanced something worth recording.
- Failing to stamp `dirty:` because `git status` was not run. The grant exists for this.
