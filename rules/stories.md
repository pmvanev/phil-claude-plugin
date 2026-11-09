# Stories

What a card on an issue board should carry, recorded from INVEST, SMART and the 3 Cs and held as their
authors held them: as guidelines, not a formula. `writing.md` governs how a card's words read; this rule
governs what the card carries; `phil:issue-board` governs the forge. Sources:
`docs/research/stories/user-story-quality-canonical-sources.md`.

## Where it applies

- **To card content a session composes**: a card it drafts, or a purpose or done-when it suggests. A
  person's answer that the session rephrases stays the person's; tidy its words and add nothing.
- **Never to a card a person wrote.** It raises no flag, no advisory note and no scan item against one.
  Judging someone else's card is taste, which `phil:groom-issues` keeps out of its scan.
- **Never as a gate.** No card waits on it before work starts. Cohn warns that a Definition of Ready
  "becomes a huge step towards a sequential, stage-gate approach" and asks for "guidelines rather than
  rules".

## Held lightly, in the authors' own words

- **Wake** built INVEST in 2003 by listing every attribute of a good story he could think of, grouping
  them into "roughly ten fuzzy clusters", and rearranging the initials into a word.
- **Doran**, who coined SMART in 1981: "the suggested acronym doesn't mean that every objective written
  will have all five criteria". He called it "a guideline".
- **Jeffries**, who named Card, Conversation, Confirmation: his team "tried a standard format card in
  something like 1998 and realized it was a bad idea then".
- **Cohn**, who popularised "As a… I want… so that…": "There is no magic formula". **Wake**, in 2021:
  "you don't need a template to start".

So a heuristic a draft misses is a question to ask, never a defect to report.

## The card carries the conversation's results

A story began as an index card: "a token representing the requirement" (Jeffries). The conversation
happened in a room, and the confirmation lived in acceptance tests. A forge board has no room. Strangers
read it, and so does a forgetful you, weeks later. So the card carries in writing the two things the room
used to hold: why the work matters, and how anyone will know it is done. That is still Beck's "a
paragraph or two", not a specification.

## The house card shape

The default for this plugin's boards; a project overrides it in its own `CLAUDE.md`.

1. **An opening paragraph, with no heading** — what is wrong or missing, and why it matters. Name the
   measured wound where one exists.
2. **`## What it does`**, or **`## What it holds`** for a document or a rule — the change, as a short list.
   State the problem fully and the solution only as far as the problem needs.
3. **`## Done when`** — a checklist of observable outcomes.
4. **`## Open questions`** — what the card leaves undecided. Omit it when nothing is; no section means
   settled.

Add a `## Chain` line when the card blocks or relates to another, as `phil:issue-board` directs.

**Fixed headings, free prose.** No sentence template: not "As a… I want… so that…", and not the job
story's "When… I want to… so I can…". The headings give the board the uniformity a tool needs; the
prose under them stays the author's.

## INVEST — for the card

Bill Wake, "INVEST in Good Stories, and SMART Tasks" (2003).

| Letter | Wake's words | On this board |
|---|---|---|
| **Independent** | "not overlap in concept", and "schedule and implement them in any order" | Fold a card that overlaps another into it. Name an unavoidable edge in `## Chain`, with its reason. |
| **Negotiable** | "A good story captures the essence, not the details." | State the problem and leave the design to the work. Put what is undecided under `## Open questions`. |
| **Valuable** | "valuable to the customer"; "slice vertically through the layers" | The opening paragraph says who gains and why. A card holding one layer of a change — the schema alone, the UI alone — joins the slice that shows the value. |
| **Estimable** | "just enough to help the customer rank and schedule" | **Not applied.** This board ranks by position, never by estimate. Its proxy, *do we understand it?*, lives in Testable and `## Open questions`. |
| **Small** | "at most a few person-weeks" | **Replaced by *demonstrable on its own*** (below). |
| **Testable** | "I understand what I want well enough that I could write a test for it." | `## Done when`. |

### Demonstrable, not small

A card is the right size when it can be demonstrated on its own: North sizes stories in "demonstrable
chunks", and Cockburn counts a slice valid only if it is "visibly different from last slice". A split by
size alone can pass Small and fail Valuable and Independent; Wake and Lawrence both show it. A card
holding a whole feature is large and demonstrable, and passes.

The sources never endorse a large card, though, and each size they name has shrunk since 2003: weeks,
then days, then "a day or less". So a session keeps a `## Done when` list it drafts to about six items —
North's point for splitting scenarios. Where a new card it is drafting needs more, it asks whether the
card splits, and splits nothing unasked. A split nobody would work in parallel stays one card
(`phil:issue-board`).

## SMART — for done-when items and tasks

Wake applies SMART to the tasks inside a story, not to the story: "These are good characteristics for
tasks as well." On this board that means a `## Done when` item, and any task list inside a card. Wake's
letters come first; Doran's 1981 originals follow where they differ.

| Letter | Wake | Doran | On this board |
|---|---|---|---|
| **S** | Specific: "everyone can understand what's involved" | "target a specific area for improvement" | A stranger can tell what the item means without the session that wrote it. |
| **M** | Measurable: "can we mark it as done?" | "quantify or at least suggest an indicator of progress" | Someone can mark the item done or not done. **Never demand a number**: Doran warns that forcing one can "lose the benefit of a more abstract objective". |
| **A** | Achievable: the owner "should expect to be able to achieve" it | Assignable: "specify who will do it" | A doubt that it is achievable goes under `## Open questions`. Doran's owner is the forge's assignee, not the body's. |
| **R** | Relevant: "contributing to the story at hand" | Realistic | Each item serves the opening paragraph. An item that serves another purpose belongs on another card. |
| **T** | Time-boxed | Time-related: "specify when" | **Not applied.** The board carries no dates. |

## Composing a purpose

- Say what is wrong or missing, who it costs, and why it matters now. That is the job story's situation
  and motivation, written as prose.
- Make it readable without context: the next reader is a stranger, or you after a month away.
- Prefer a measured wound to an adjective: "the scan reported clean on every board it was written for"
  beats "the scan is unreliable".

## Composing a done-when item

- **Name an observable outcome a stranger can check**: a file exists, a command prints a stated line, a
  fixture fails without the change. A procedure ("run the tests") and a quality ("works well") are not
  outcomes.
- **Write it in the domain's words, not as a test script.** Adzic warns against "using technical language
  and scripts to describe how something is tested".
- **Use Given-When-Then where it helps, never because it is required.** North's point is behaviour, not
  syntax.
- **Give each item one outcome**, so each can be marked done on its own.

## Not adopted, and why

- **A sentence template.** Rejected by Jeffries, Cohn and Wake, as quoted above.
- **A Definition of Ready.** A checklist a card must pass before work starts is the stage gate Cohn warns
  against.
- **Estimates and dates.** Estimable and Time-boxed serve ranking by estimate and scheduling by date;
  this board ranks by position and sets no dates.
- **Size as a defect.** Demonstrability decides; length prompts a question.

## Sources and Synthesis

INVEST and SMART's task reading come from Wake (2003, with his 2011 postscript and his 2021 "What Is a
User Story?"); SMART's original letters from Doran's *Management Review* article (1981), read as a scan of
the printed pages; the 3 Cs and the rejected card format from Jeffries (2001, 2008, 2019); the template's
optionality and the Definition of Ready warning from Cohn's current posts; demonstrable sizing from North
("What's in a Story?", 2007) and Kniberg and Cockburn's Elephant Carpaccio guide (2013); horizontal splits
from Lawrence's splitting guide; the done-when wording from Adzic's own words on *Specification by
Example*; Beck's "a paragraph or two" from his signed entry on Cunningham's wiki.

**This rule's own synthesis:** the house card shape, which records this plugin's boards rather than any
source; the *On this board* columns; the six-item split prompt, which borrows North's scenario count for a
`## Done when` list; and the decision to apply the rule to composition only. The rule draws on the
research document, not on books in hand: Cohn's *User Stories Applied*, Patton's *User Story Mapping* and
Adzic's *Specification by Example* were not opened. Patton's often-quoted "stories are for telling, not
writing" was not found in any text the research opened, so this rule does not quote it.

---

## The Mantra

> **Say why it matters and how anyone will know it is done, in a card someone can demonstrate — and hold
> every acronym as a reminder, never a gate.**
