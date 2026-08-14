# Expected — 09 (the roster is generated; no sub-issue is created)

> **Rewritten 2026-08-14.** This fixture was `09-native-hierarchy-no-roster` and pinned the opposite
> rule: open a slice issue per brief, attach it as a sub-issue, and *never* hand-write a roster because
> the forge computes it. The paradigm inverted; the fixture inverted with it.

**Expected outcome:** `GENERATED-ROSTER`. **One issue exists.** Four roster rows are generated into its
delimited block, each with a glyph and a two-line description. **No sub-issue is created**, and
`subIssuesSummary` stays `{0, 0}`.

**Why the availability of native hierarchy is the trap here.** GitHub *will* give an exact, free rollup
if you create the children — that mechanism is real and `phil:issue-board` documents it. It is the wrong
thing to reach for, because the children would be cards nobody but the feature's owner can pick up, and
the count they buy is not the question a teammate is asking.

**Why the old ban on a written roster does not apply.** It was scoped to the case where the forge already
computed the roster, making a written copy a second tally that would disagree. Nothing computes it now, so
a generated, delimited, timestamped roster carries the same guarantees as the step table.

**Gate failures:**

- Creating a slice issue, for any reason, including "to get the bar".
- Reading `subIssuesSummary` or `trackedIssues` and publishing either.
- Writing the roster as `- [ ]` checkboxes to manufacture a count — see 15.
- A roster row with a name but no two-line description. The name is a label the owner recognises; the
  description is what a teammate needs.
- Omitting glyphs, or inventing one outside `✓ ▶ · ⊘ ?`.
