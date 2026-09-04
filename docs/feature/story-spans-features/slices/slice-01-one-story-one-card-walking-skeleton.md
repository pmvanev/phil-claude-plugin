# Slice 01 — One real story as one card (walking skeleton)

**Goal:** Build, by hand, a story card carrying two stacked rosters on the real board, and measure
whether a reader names **both** positions in under thirty seconds — and can tell the story from the goal
without being told.

**Stories:** S1 (read both positions from one card), S6 (tell a story from a goal on sight)
**WS strategy:** C — real local resources (the real board; not a faked adapter)

## Learning hypothesis

**Disproves the whole feature** if two stacked rosters read as a wall, or if the reader gets one position
and loses the other — for the price of one issue edit and no skill changes.
**Confirms**, if it passes, that the two-table bound is worth making normative in slice 03.

Highest uncertainty by a distance: the predecessor measured a thirty-second read against **one** roster,
and this feature's entire premise is that a second one fits above it. Nothing has ever rendered two.

## IN scope

- Edit **issue #36** in place: a hand-built `nwave:status` block over the story
  *the board's unit of work*, whose members are `single-issue-per-feature` and `story-spans-features`
  ([D14]). In this order:
  - `Story:` line with the feature count, and a generation timestamp
  - `Wave:` line naming the current feature, and the `Work this with:` line or the stated reason there
    is none
  - `Order: position declared per feature — final; /nw-roadmap does not run in this repo`
  - the **feature roster** — one row per feature, with a two-line description, a state glyph from the
    six-value vocabulary, and Notes
  - `Current feature NN <id> — slices:`
  - the **current feature's slice roster** — as the shipped block already renders it
- The timed read, by someone who is not the author: name the current feature's position, name where that
  feature sits in the story, and say which of the two groupings on screen is the story and which is the
  goal. Result recorded here, pass or fail, with the time.
- A row count, recorded against KPI-3.

## OUT scope

- Any edit to any skill or command. The block is hand-built on purpose — this slice tests the **design**,
  not an implementation of it. Slices 02-05 own the rules.
- The fold. The card's column is hand-placed; `--story-state` is slice 02.
- Grooming and ranking. `/phil:rank-issues` will stop on this card and `/phil:groom-issues` will pass it
  clean; both are expected here and are slice 05's to fix.
- A four-feature story. Domain example 1 is the scale case and is slice 03's fixture; two features is the
  smallest thing that can fail the way this slice is asking about.
- GitLab. See the limitation below.

## Acceptance criteria

1. The block renders on #36, delimited by `<!-- nwave:status:begin -->` / `<!-- nwave:status:end -->`,
   with both rosters and a timestamp.
2. **KPI-1:** the timed read completes in ≤30 s and names **both** positions. Recorded with the time.
3. **KPI-5:** the same reader identifies which grouping is the story and which is the goal, unprompted,
   first time. **This needs a goal to be visible, and #36 has none** — `milestone: null`, probed
   2026-09-04. Assign #36 to the open milestone `Board and session tooling` (due 2026-09-15) before the
   read. **A test run with only one of the two groupings on screen measures nothing** and would pass
   trivially.
4. **KPI-3:** rows rendered ≤12, counted and recorded.
5. Only `story-spans-features`'s slices are enumerated. `single-issue-per-feature`'s seven slices appear
   nowhere — its row links its delta ([D6]).
6. Slices appear in a second table, never as indented sub-rows of the feature roster ([D7]).
7. Every feature-state glyph comes from the six-value vocabulary; no value is rendered as `·` because it
   had no glyph.

## Dogfood moment

The reader opens #36 in a browser and is timed. **The reader is not the author** — the grader problem the
`nwave-issue-board` suite already names about itself applies to the card, and the predecessor's slice 01
handled it the same way.

## Stated limitation (do not let this pass as covered)

The requirement is to read the card **in GitLab**; this board is GitHub. This slice verifies the layout's
legibility, not its GitLab rendering, and KPI-1 is measured on the wrong forge. The evidence must say
"GitHub, `gh` <version>" explicitly, and the GitLab re-measurement stays on the open list.

**Second limitation, and it is the one that could invalidate the result:** the two-feature story is the
*small* case. A reader who manages two rosters may not manage a four-feature one, and example 1 is four.
Slice 03 must re-measure at that scale rather than inheriting this number.

## Dependencies

- `gh auth` holds the `project` scope, to read the card's Status back.
- #36 assigned to the `Board and session tooling` milestone, for AC3.
- **Not a dependency, checked rather than assumed:** #26 is CLOSED (probed 2026-09-04), so declaring
  `single-issue-per-feature` a member of this story creates no open duplicate card.
- Plugin skew: this slice is hand-driven, so it exercises **the prose, not the command**, which must be
  said in the evidence per `CLAUDE.md`.

## Effort

~2-3 hours. Reference class: the predecessor's slice 01, which built a real card and ran a real timed
read in one sitting.

## No pre-slice SPIKE

The uncertainty is entirely about how a rendered page reads. A SPIKE would build the same card and call
it a probe.

## Carpaccio taste tests

| Test | Result |
|---|---|
| Ships 4+ new components? | No — one issue edit. No skill or command touched. |
| Depends on a new abstraction? | **This slice IS the abstraction.** The two-table layout ships here before any slice assumes it — the taste test's own prescribed remedy. |
| Disproves a pre-commitment? | Yes, the largest: that two stacked rosters read in seconds. KPI-1 and KPI-3 are numbers, not judgements. |
| Synthetic data only? | No — the real board, two real feature directories, a real timed read. |
| Duplicate of another slice at scale? | No. 03 makes the layout normative; this discovers whether the layout is worth asserting. |

---

## Result — 2026-09-04

Card built on #36. Evidence forge: **GitHub, `gh` 2.97.0**. **Hand-driven throughout — this exercised
the prose, not any command**; the installed plugin is 0.73.0 and the working tree is 0.78.0, and the
`nwave-slice-status` fold was read from the **working tree**, which carries two guard fixes 0.73.0
lacks.

| AC | Verdict |
|---|---|
| 1 — block with both rosters, delimited, timestamped | **met** — 3 tables render via the GFM markdown API; markers present; prose outside them fully retained (byte-compared before/after) |
| 2 — KPI-1, ≤30 s naming both positions | **NOT MEASURED** — requires a reader who is not the author. Open. |
| 3 — KPI-5, story told from goal unprompted | **NOT MEASURED** — same reader constraint. Its *dependency* is discharged: #36 assigned to `Board and session tooling` (due 2026-09-15), so two groupings are now on screen. |
| 4 — KPI-3, rows ≤ 12 | **met** — 7 rows (2 features + 5 slices) |
| 5 — only the current feature's slices enumerated | **met** — `single-issue-per-feature`'s seven slices appear nowhere; its row links its delta |
| 6 — slices in a second table, not indented sub-rows | **met** |
| 7 — every feature-state glyph from the six-value vocabulary | **met**, see finding 4 |

### Build-path compliance, stated rather than inferable

`CLAUDE.md` requires a commit to say which of the two build-path tools ran. For this slice:

- **`nw-discuss`: RAN**, 2026-09-04, producing this brief and its siblings.
- **`plugin-dev`: NOT DUE, and that is a claim to check, not an excuse.** Verified by
  `git status`: the working tree's only changes are under `docs/`. **No file under `skills/`,
  `commands/`, `agents/`, `hooks/` or the manifest was touched**, so `skill-development`,
  `command-development` and `plugin-structure` had no target and `skill-reviewer` had no subject.
  A `plugin-validator` baseline was run anyway, before slices 02-05 begin editing five skills and
  four commands, so any regression they introduce is attributable.

**Slices 02-05 all author plugin components, and for them the consults are mandatory BEFORE the
file is written** — not after. Slice 02 opens `skills/nwave-slice-status/SKILL.md`, which is where
that obligation first bites. Recorded here because the standing failure in this repo is a build-path
deviation that nobody can see afterwards.

### Finding 1 — the predicted non-monotonicity did not occur, and the prediction went stale inside its own wave

Domain example 2 predicted the routing line steps **backwards**, from *no line* (position 01, past
DISCUSS) to `/nw-discuss` (position 02, at DISCUSS). By the time the card was built, position 02 had
**also** completed DISCUSS. Both features are past it, the card carries **no routing line at all**, and
the backwards step never happened.

The example was written mid-DISCUSS and was wrong before the wave that wrote it finished. It is not a
bad prediction — it is evidence that **a worked example naming a wave is stale the moment that wave
ends**. Slice 04 owns the mixed-wave case and must build it from features that are genuinely in
different waves, not from these two.

### Finding 2 — a retired slice is invisible to the marker scan, and it changes a feature's fold

`slice-06-consolidate-existing-board.md` is retired. `nwave-slice-status` looks for a `**Status:**`
line or a `DEFERRED` / `OUT of v<N>` marker; **slice 06 carries none of those.** Its retirement lives
in the H1 (`— SUBSUMED BY SLICE 07`) and in the closing commit.

A scan reading only the documented markers counts slice 06 as not-done, which fails *"every slice that
is not deferred is done"* and folds `single-issue-per-feature` to **`in progress`** — a shipped, closed
feature reported as live work, on the card the whole team reads. Correct answer (`done`) was only
reachable by reading the heading and the git history.

**This is a defect in the marker vocabulary, not in this slice.** Route: it changes what a skill
asserts, so it folds into `nwave-slice-status` with a fixture, and slice 02 is where that lands since
it is already opening that skill's fold. Recorded here rather than fixed here — slice 01 touches no
skill.

### Finding 3 — "every sibling is a row with a link" is unachievable before the artifacts are pushed

[D6] requires every non-current feature to be a row **with a link**. Position 02's delta is
uncommitted, so a link to it renders correctly, passes a local read-back, and **404s for every other
reader** — the trap `phil:issue-board` names under *Link what the forge cannot resolve*. The row
therefore carries no link and says why.

Slice 03 must write the rule as *link where the path is pushed, and say so where it is not*, rather
than as an unconditional requirement it cannot keep.

### Finding 4 — `in progress` had no glyph; this slice chose one

The delta already flagged that the feature vocabulary's six values include one with no glyph. Chosen
here, for slice 03 to make normative or overturn:

`✓ done` · `▶ in progress` · `· to do` · `! blocked` · `⊘ deferred` · `? unknown`

`▶` is reused from the slice vocabulary's `current`. The two never share a table, and every row prints
the state word beside the glyph, so the reuse is not ambiguous in place.

### Owner review, 2026-09-04 — and why it is not KPI-1

The owner read #36 and reported it **looks good**. Recorded as what it is: a qualitative approval of
the layout by someone who did not build it. It establishes that the two stacked rosters carry no
obvious defect, and that the design is sanctioned to continue.

**It is not KPI-1 and must not be recorded as it.** KPI-1 is a *time* against a *named pair of
positions*; KPI-5 is an *unprompted* discrimination of the story from the goal. Neither number exists.
Rounding an approval up to a met KPI is the defect the predecessor refused when it recorded its own
KPI-3 as failed rather than rounding it off.

**The cold-read opportunity on this reader is now spent, and that is a real cost.** KPI-1 measures a
*first* read. The owner has read the card, so any timed re-read now measures recall, not legibility,
and no instrument recovers the difference. Two consequences:

- KPI-1 and KPI-5 stay **unmeasured on the two-feature case, permanently**. Not deferred — unavailable.
- **Slice 03 becomes the only place either number can be obtained**, since it re-measures at four
  features with a reader who has not seen the layout. Its brief already refuses to inherit slice 01's
  number; it now also carries the only chance to produce one. That is a load increase on slice 03 and
  is recorded here rather than discovered there.

**Process finding, worth more than the number:** this slice specified a timed read but shipped the card
to the reader without the stopwatch. An acceptance criterion that depends on a first impression is
consumed by the first impression, so the instrument has to be in place *before* the artifact is shown.
Slice 03 must brief its reader before showing them anything.

### Still open

- **KPI-1 and KPI-5 are unmeasured and now unobtainable at this scale** — see the owner-review
  section above. The learning hypothesis is undischarged: whether two stacked rosters read *in seconds*
  is still unknown. The owner's approval says the layout is not broken, which is weaker and is all we
  have. Slice 03 inherits the measurement.
- **GitLab, inherited and unaddressed.** The requirement is to read the card in GitLab; this is GitHub.
