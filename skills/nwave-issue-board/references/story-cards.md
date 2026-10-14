# Story cards

Part of the `nwave-issue-board` skill. Read it whole before writing to a card where several features declare one story. Its `SKILL.md` governs this file too; where a rule here names a story-tier exception, the exception wins on a story card.

## The wave label on a story card

**On a story card the label is the CURRENT FEATURE's wave** — still exactly one, still swapped never
added. A story does not have a wave of its own; its members do, and the current one is the only member
whose wave a reader can act on.

**So the label steps backwards — DELIVER to DISCUSS — when one feature finishes and the next begins.**
That is correct output: a new feature starts at the beginning.

**Every story block carries this clause, verbatim, on its own header line — not only the blocks where a
backwards step just happened:**

```
Wave note: a story's wave is its current feature's, so it moves backwards when one feature finishes and
the next begins. That is correct.
```

The reader who "corrects" the label forwards comes later, and a clause emitted only at the transition
is gone by then. Use the fixed wording: a clause each run invents drifts.

**One wave value per story card — never `wave: mixed`, never several values.** `mixed` names no command
and hides which member is moving; several values resurrect four wave labels accumulating on one card and
break the single-valued declaration `phil:groom-issues` rule 4 reads.

## Card order at the story tier

- **At the story tier the order is the declared `position`, and the line says so:**
  `Order: feature position as declared · slice order <as *The order of the cards is the order of the work* in `SKILL.md` words it>`. Where a member declares no position it
  **sorts last and the line says that too** — `phil:nwave-slice-status` returns it that way and never
  invents one. Where two members claim one position the owner returns `contested`; see below.

## The story block

At the story tier the bound in `SKILL.md`'s *Generate into a delimited block* yields the feature roster, the current feature's slice roster, and —
where a `roadmap.json` exists — the current slice's steps.

**The current feature is bolded *and* linked, exactly like a sibling.** Only its slices are enumerated.

**Every sibling link is summarised, not bare** — one clause saying what it holds.

**A story block additionally carries `Story:` and `State:` above them and the `Wave note:` clause below
`Wave:`** — five header lines rather than three, and all five are mandatory there.

**A story card carries one more table and one more header line.** Same markers, same generation
discipline, same refusals (under *Generate into a delimited block* in `SKILL.md`):

```
<!-- nwave:status:begin -->
Story: chat-everywhere · 4 features · generated 2026-09-04T17:30Z
State: in progress — from `phil:nwave-slice-status --story-state chat-everywhere`
Wave: DESIGN · current feature chat-in-web-ui
Wave note: a story's wave is its current feature's, so it moves backwards when one feature finishes and
the next begins. That is correct.
Work this with: /nw-design · feature chat-in-web-ui
Order: feature position as declared · slice order by slice number — provisional until /nw-roadmap

| # | Feature | What it does | State | Notes |
|---|---|---|---|---|
| 01 | [aws-bedrock-setup](…) | Stands up the model endpoint the other three call.<br>Nothing else can be demoed until this answers. | ✓ done | |
| 02 | **chat-in-web-ui** — [delta](…) | Puts a chat surface in the web client.<br>The first feature a user can see. | ▶ in progress | |
| 03 | [saved-sessions](…) | Persists a conversation across reloads.<br>Depends on 02's transcript shape. | · to do | |
| 04 | [chat-ui-in-extension](…) | Ports the web surface into the extension.<br>Last, because it consumes 02's settled shape. | · to do | no wave declared yet |

Current feature 02 chat-in-web-ui — slices:

| Slice | What it does | Status | Notes |
|---|---|---|---|
| 01 | Renders a transcript from a canned response.<br>Disproves the streaming assumption if it fails. | ✓ done | |
| 02 | Streams a live response into the transcript. | ▶ current | |
| 03 | Handles a mid-stream disconnect.<br>The first error path a user can hit. | · not started | |
| 04 | Persists the transcript for the session's life. | · not started | |
| 05 | Renders markdown in a streamed response. | · not started | |
| 06 | Adds the stop-generating control. | · not started | |
<!-- nwave:status:end -->
```

**Ten rows for a four-feature story** — four features plus the current feature's six slices, and no
third table because this feature has no `roadmap.json`. Fixture `20` pins this scenario, and the two
must agree.

**`State:` carries what `--story-state` returned, verbatim.** It is a header line rather than a column
because it describes the card, not a row. Two of the six states — `deferred` and `unknown` — write **no
column**, and the block is where that gets said, exactly as at feature tier.

**Where the owner returns a contested or absent current feature, render that and enumerate nothing.**
`phil:nwave-slice-status` refuses to resolve a position collision, and where every member is `done` it
omits the current feature entirely. Both cases reach here, and in both the heading becomes a statement
instead of a subject:

```
Current feature: contested — position 02 claimed by chat-in-web-ui and saved-sessions. No slice roster.
Current feature: none — every member is done.
```

**No current feature, no wave label and no routing line**: both derive from the current feature
alone, so the card writes neither and the block says which case it is. Pick no contender — not for the
slice roster, not for the wave; the renderer would invent the fact the deriver withheld.

## Routing a story card

- **On a story card there is no member label to read, so the source is the member's own artifact.** A
  story member has no card — it is a roster row — so it carries no label and the roster has no wave
  column. Take the wave from the current feature's `docs/feature/<id>/feature-delta.md` header, which is
  where an nWave feature records it. **`phil:nwave-slice-status` does not return a wave**; asking it for
  one gets a state. And never derive the routing line from the *story card's own* label, which is this
  rule's output.
- **A story card with no wave says why it has none**: it is nWave work by definition, so silence there
  explains nothing.
- **On a story card the line names the command AND the feature it applies to** —
  `Work this with: /nw-design · feature chat-in-web-ui`. A bare command on a multi-feature card asserts
  the command owns the *story*, and none of them does.
- **No line ever names a command for the story.** There is no story-scoped wave command, and inventing
  one — or letting a bare command imply it — sends a reader to run something over a scope it was never
  written for. Three rules apply unchanged at this tier: the label is still the source, no label
  still means no line, and no row still means no line **with the reason stated**.
- **Where two members are `in progress` at once, the label is still the current feature's wave — and
  this skill does not decide which that is.** `phil:nwave-slice-status`'s `references/states.md` § *The story-level state, on request* already
  defines it: **the first member, in `position` order, whose state is not `done`** — which is not
  necessarily the first member that is `in progress`. **Every other in-flight member's Notes cell carries
  `⚠ also in flight`.**

  **Take the current feature from the owner, never as "the first in-flight member".** On `01 to do ·
  02 in progress · 03 in progress` the owner answers **01** and a first-in-flight rule answers **02**
  (fixture `29`).

  The block neither hides the ambiguity nor resolves it: two features in flight is a card defect, which
  `phil:groom-issues` reports from this evidence.
