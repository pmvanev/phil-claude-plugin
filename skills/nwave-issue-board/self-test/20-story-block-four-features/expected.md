# Expected outcome — fixture 20 (`STORY-BLOCK-BOUNDED`: one expanded path at four features)

**Pins:** *The mapping* story row, and the bound restated as purpose — *exactly one feature's slices and
one slice's steps are enumerated; every sibling is a row with a link.*

**Expected:** two tables. A **four-row feature roster**, then **`Current feature 02 chat-in-web-ui —
slices:`** with its **six** slice rows. **Ten rows.** No third table, because position 02 has no
`roadmap.json` — and no promise that one is coming, since `/nw-roadmap` may never run.

**The arithmetic is the assertion.** Four features × six slices is **24 rows** before a single step. The
bound yields **10**. That ratio is why question 1 was a scale choice wearing a layout choice's clothes:
both candidate answers render, and only one is readable.

**Sibling slices are not lost, they are one link away.** Positions 01, 03 and 04 each contribute one row
carrying a two-line description and a **summarised** link to their delta — not a bare URL. Six bare URLs
would consume the whole read budget the projection exists to fit inside.

**The state is `in progress` and this skill did not compute it.** It came from
`phil:nwave-slice-status --story-state chat-everywhere`. The card sits in **In Progress**.

**GitLab Free, deliberately.** The story tier must work where epics do not exist — that constraint is
what excluded epics in the first place, and a story block that needed Premium would have reintroduced it.

**Gate failures:**

- Rendering any sibling feature's slices. 24 rows, the defect this fixture exists to catch.
- Rendering a third table, or promising one arrives with the roadmap. No roadmap is coming here.
- **Folding the story state locally instead of asking `--story-state`.** This skill's recurring defect,
  committed on 2026-08-14 and reverted the same day. It renders this value; it must never compute it.
- Bare sibling links with no clause saying what they hold.
- Omitting positions 03 and 04 because they are `to do`. A sibling is a row, not a hidden thing.
- Emitting per-feature `Why` / `Next` / `Stack`. A stack belongs to a person, and one person owns the
  whole story.
- Using slice glyphs for feature rows — `→ next` cannot appear at feature level.
