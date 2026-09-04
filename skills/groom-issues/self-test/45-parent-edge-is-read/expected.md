# Expected — 45 (the strongest evidence, actually read)

**Pins:** the decomposed-feature evidence table's tier 1, on the board it was written for. **This is the
fixture issue #30 asked for** — the case that reported clean because the scan could not make the read its
own rule ranks first.

**Expected:** `REPORT-DEFECT` with `SURFACE-CANDIDATE` alongside. The scan reads the parent edge and
reports the set:

```
#70 'Payload projection' has four sub-issues: #71, #72, #73, #74.
Read from the forge -- these are real parent/child edges, not inferred from titles.

On this board one issue is one feature, so slices of #70 are roster rows and not cards.

1 set-level candidate; /phil:groom-set resolves it, asking before each.
```

**The parent edge is the only tie, and that is the whole design of the fixture.** No title says
`slice NN`; no body names a `docs/feature/` directory; the five share no milestone. Strip the edge and
there is nothing left to fire on — which is what makes this a test of the read rather than a test of the
class. A fixture carrying tier-2 or tier-3 evidence alongside would pass without the read ever happening,
and would pin nothing.

**Why it failed before.** `parent` and `subIssues` are GraphQL-only; `gh issue list --json` exposes
neither and no flag adds one. The command held `gh issue list` and nothing else, so tier 1 — the signal
its own table calls sufficient on its own — was unreadable, and a board of parented slice cards came back
`REPORT-CLEAN`. Correct against what it could see, and worthless.

**Gate failures:**

- `REPORT-CLEAN`, with or without the candidate beside it. Reporting it **without** the candidate is the
  defect this fixture exists for — the board has no body defects, so a scan that cannot see the edge
  finds nothing and says so correctly. Reporting it **with** the candidate is the subtler error: a
  surfaced candidate is a defect between issues, so the board is not clean. Both are refused, and the
  rule is stated in *Decision outcomes* — a gap fixture `45` is what exposed.
- `REPORT-UNEVALUATED` for the parent-edge check. The command now holds the read; reporting the rule dark
  is the fixture-39 answer to a question that has since been decided.
- Inferring the relationship from anything but the edge, or claiming an edge that was not read.
- Applying the consolidation. The scan surfaces; `/phil:groom-set` asks and resolves.
- Using the granted `gh api graphql` for anything but a read. The grant permits a mutation and the
  command's prose forbids one — see below.

## The grant this fixture depends on

Settled for issue #30, and the trade is recorded rather than absorbed: `commands/groom-issues.md` gains
`Bash(gh api graphql:*)` and declares `mutates: true`. **The read-only guarantee is no longer enforced by
the tool list; it is a promise carried in prose.**

`gh api graphql` accepts a mutation document, so no scoping keeps it read-only, and the interpreter of a
helper script cannot honestly join `READ_ONLY_VERBS` in `scripts/check-readonly-commands.py` — whose
header says an entry there is a promise that the verb has no writing mode. Both routes end at a promise;
this one ends there without a script to maintain.

`Write` and `Edit` are still absent, so the *file* half of the guarantee stays mechanical. What was
downgraded is the *forge* half, and fixture `08` is amended to say exactly that rather than to keep
claiming the whole guarantee is enforced.

Precedent: `commands/resume.md` took the same trade on 2026-08-17 for issue #24 — `mutates: true` while
writing nothing, the narrow grant kept, the read-only intent in the command's prose and the skill's
never-do list.
