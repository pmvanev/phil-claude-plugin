# Expected outcome — fixture 16 (the story fold is the feature fold, one level up)

**Pins:** *The story-level state, on request* — membership discovery, the substitution table, and the
`in progress` row reached over members in different states.

**Expected output**, one line, with the count:

```
Story: the-boards-unit-of-work — in progress · 1 of 2 features done · current feature story-spans-features
```

**How each member folds.** The story fold does not read slices. It reads each member's **feature**
state, which is itself the feature fold over that member's roster:

| Position | Feature | Feature fold | Why |
|---|---|---|---|
| 01 | `single-issue-per-feature` | `done` | every slice that is not `deferred` is `done`; slice 06 is retired |
| 02 | `story-spans-features` | `in progress` | slice 01 is current |

Then *"any feature is `done` or `in progress`"* fires: **`in progress`**.

**The eleven other feature directories are not in the roster.** A feature with no `Story:` line is in no
story. Discovery is a scan for the slug, not a scan of `docs/feature/`.

**Slice 06 is the trap this fixture carries, and it is not about the story tier at all.** It declares no
`**Status:**` line and no `DEFERRED` marker — the two forms *Step 2* names. Its retirement lives in the
H1 (`— SUBSUMED BY SLICE 07`) and in the commit that closed the feature. A reader matching only the two
documented markers counts slice 06 as not-done, position 01 folds to `in progress` instead of `done`, and
the story line becomes `0 of 2 features done`. **The story answer is still `in progress`, so the story
fold looks correct while its input is wrong** — the count is the only thing that moves, and a count is
what a reader trusts. Found live 2026-09-04 building the card on #36.

**Gate failures:**

- `0 of 2 features done`, from missing slice 06's retirement. The defect above.
- Reading position 01's *slice* statuses into the story fold. Two vocabularies; the story fold consumes
  feature states, never slice statuses.
- Returning `done` because position 01 is done. `done` requires **every** non-deferred member.
- Naming position 01 as the current feature. `current feature` is the first member not `done`.
- Ordering the roster by directory name, mtime, or discovery order. `position` decides.
- Including features that declare no story.
- Folding this in `phil:nwave-issue-board`. It renders this line and must not compute it.
- Reading the forge to learn what the story contains. Membership is declared in `docs/feature/`.
