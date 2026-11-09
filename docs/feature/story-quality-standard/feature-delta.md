<!-- markdownlint-disable MD024 -->
# Feature Delta — story-quality-standard

Wave: DISCUSS ✓ (2026-11-09) · Density: lean · Card: issue 114
Build path: DISCUSS here, then the rule and the skill edits are written directly — the deliverable is
prose, so DESIGN, DISTILL and DELIVER stay out (edd-loop DDD8). Rules are not a plugin component, so no
plugin-dev schema applies to `rules/stories.md`; `plugin-dev:skill-reviewer` reviews the skill changes.

This feature records INVEST, SMART and the 3 Cs in a new rule, `rules/stories.md`, held as guidelines
rather than a formula, and makes the two surfaces where a session composes a card read it. It is grounded
in `docs/research/stories/user-story-quality-canonical-sources.md` (33 sources, 2026-11-09).

---

## Wave: DISCUSS / [REF] The gap, measured

Measured 2026-11-09 against `main` at `65de4b2`:

- **No file in `rules/`, `skills/`, `commands/` or `agents/` names INVEST or SMART.** The only match for
  either word in those directories is `rules/cpp.md`'s "smart pointer".
- **The house card shape is unwritten.** The board's recent cards share four parts — an opening paragraph
  saying what is wrong and why it matters, `## What it does` or `## What it holds`, `## Done when`,
  `## Open questions` — and no file says so. A session drafting a card copies it from whatever cards it
  happens to read.
- **`groom-issues` checks presence, and must keep to presence.** Its standard checks that a purpose
  (rule 1), a done-condition (rule 2) and a chain (rule 5) are present, and its *Judging prose is taste*
  section forbids judging how a human's card reads. `CLAUDE.md`: "Keep `groom-issues`' scan structural:
  five items, no style item."
- **Its oversized test departs from INVEST's Small and records no source.** "Judge demonstrability, never
  size" (`skills/groom-issues/SKILL.md`, defect classes) has precedent in North's "demonstrable chunks" and
  Cockburn's "visibly different from last slice", and the file cites neither.
- **Two surfaces compose card content with no content standard.** `/phil:groom-ask` drafts a missing
  purpose or done-when as a suggestion; a session filing a card through `phil:issue-board` drafts a whole
  body. Both apply `rules/writing.md` to the words and nothing to what a card should carry.

## Wave: DISCUSS / [REF] Pre-requisites

- **Research precursor (D1), done:** `docs/research/stories/user-story-quality-canonical-sources.md`.
  `@infrastructure` — it lands with slice 01, not as a slice.
- **Existing artifacts touched:** `rules/stories.md` (new), `skills/groom-issues/references/ask.md`,
  `skills/groom-issues/SKILL.md`, `skills/groom-issues/self-test/`, `skills/issue-board/SKILL.md`,
  `README.md`, `.claude-plugin/plugin.json`, `docs/product/jobs.yaml`,
  `docs/product/personas/robin-backlog-curator.yaml`.

## Wave: DISCUSS / [REF] Persona ID

**`robin-backlog-curator`, extended with a composition facet — no new persona.** Robin owns the board and
already reads what `groom-ask` writes onto it. A card the session drafts well is a card Robin need not
groom later. Same person, same commands; the standard moves upstream from checking a card to composing one.

**Rejected: a "story author" persona.** The author of a card on this board is Robin, or a session acting
for Robin; the repo earns a new persona only for a position orthogonal to every domain.

## Wave: DISCUSS / [REF] JTBD one-liner

**A facet of `keep-a-backlog-trustworthy`, not a new job.**

> When a session drafts a card or suggests what a card should say, I want it shaped by what the canon
> says a good story carries — the why, a done-condition a stranger can check, a size that can be
> demonstrated — without a template or a gate, so I can trust a drafted card as much as one I wrote.

Recorded in `docs/product/jobs.yaml` as the composition facet.

## Wave: DISCUSS / [REF] Locked decisions

| ID | Decision | Rationale |
|----|----------|-----------|
| D1 | **Research is a precursor**, done. | The `security-standards-rule` and `ux-standards-rule` bar; "empirical design over speculation". |
| D2 | **One new rule, `rules/stories.md`.** | One standard for what a card carries, beside `writing.md` for how its words read. Neither restates the other. |
| D3 | **The rule shapes only what a session composes; it never flags a card a person wrote.** The `groom-issues` scan is unchanged. | The developer's decision, 2026-11-09. Matches *Judging prose is taste* and the `CLAUDE.md` line keeping the scan structural. Cohn: favour "guidelines rather than rules" on readiness, or it becomes a stage gate. |
| D4 | **Guidelines, not a formula, stated in the authors' own disclaimers.** Wake built INVEST from "roughly ten fuzzy clusters"; Doran wrote that "every objective written" need not meet "all five criteria". | The developer's stance is the canonical position; quoting the authors makes it a recorded fact rather than a preference. |
| D5 | **Record the house card shape as a default, not a template.** Four parts, fixed headings, prose inside them; no "As a… I want… so that…" and no job-story sentence. A project overrides it in its own `CLAUDE.md`, as it overrides `groom-issues`' standard. | The developer: the current format is "just the right level of formal". Jeffries tried a standard card format in 1998 and dropped it; fixed headings give a board the uniformity tooling needs without a sentence template. |
| D6 | **INVEST for the card, SMART for the done-when items and the tasks inside a card** — Wake's split, with Wake's letters. Doran's original letters are recorded beside them. Never demand a number. | Wake's own article: SMART is "good characteristics for tasks". Doran: forced quantification can "lose the benefit of a more abstract objective". |
| D7 | **Estimable and Time-bound are recorded and not applied.** | Each exists to rank and schedule by estimate or date; this board ranks by position and carries no dates. Their surviving proxy — "do we understand it?" — is carried by Testable and `## Open questions`. |
| D8 | **Demonstrability stays the size test; a done-list past about six items prompts a split question when the session is the author.** | North ("demonstrable chunks", split past "five or six" scenarios) and Cockburn ("visibly different from last slice") put demonstrability first; no source endorses a large card, so the prompt keeps Small's intent without a size gate. Applies only to composition, per D3. |
| D9 | **The card carries the conversation's results, because the board has no room.** The rule says why the card is more than a sticky note. | Wikipedia names distributed teams as the case where bare cards fail; Beck's original card was "a paragraph or two". Answers the one place the sources challenge the stance. |
| D10 | **`groom-ask`'s suggestions follow the rule; `issue-board`'s *Choosing what becomes an issue* names it for a drafted body; `groom-issues`' oversized clause cites it as the source of its departure.** | The three places a session composes card content or reasons about card size. `/phil:start` files a title only and stays unchanged. |
| D11 | **The rule states what is its own.** A Sources section separates the authors' words from this rule's synthesis and names the books not opened. | The `security.md` and `test-patterns.md` pattern. |
| D12 | **No `paths:` frontmatter.** | The rule governs board cards, not files; no glob matches a card. |

## Wave: DISCUSS / [REF] Driving ports

- **`/phil:groom-ask`** — drafts a suggested purpose or done-when that follows the rule.
- **A session filing or rewriting a card** — `phil:issue-board`, which every such session reads.
- **The rule file** — read by any skill that names it, and by a developer looking up what INVEST means.

## Wave: DISCUSS / [REF] WS strategy

**A — none.** Additive and brownfield: one new rule, three edited skill files. Slice 01 is the thinnest
end-to-end value: a `groom-ask` suggestion shaped by the rule.

## Wave: DISCUSS / [REF] Scope Assessment: PASS

Two slices, one context (the board skills), one new file. No oversized signal fires. Each slice runs against
this repo's own board as production data, beside a fixture.

## Wave: DISCUSS / [REF] User stories

Both stories trace to `job_id: keep-a-backlog-trustworthy` (composition facet).

### US-01 — `groom-ask` suggests a purpose and a done-when the canon would accept *(walking-skeleton slice)*

**Problem.** Robin runs `/phil:groom-ask` on a card with no way to tell when it is done. The session
suggests a done-when, but nothing says what a good one is. It may suggest "works correctly", a task list,
or a number nobody asked for.

**Solution.** `rules/stories.md` records INVEST, SMART and the 3 Cs, the house card shape, and what
a done-when item is: an observable outcome a stranger can check, in the domain's words, never a
procedure. `references/ask.md` applies it to every suggestion it drafts.

#### Elevator Pitch
Before: a suggested done-when follows no standard and may be a task list or a vague "works".
After: run `/phil:groom-ask` on a card with no done-when → sees suggestions that each name an observable
outcome, with a split question when they run past about six.
Decision enabled: accept, edit or replace a done-when knowing it meets the house standard.

#### Acceptance Criteria
- [ ] `rules/stories.md` exists and records INVEST with Wake's meanings, SMART with Wake's letters
      beside Doran's, and the 3 Cs, each with its author's disclaimer.
- [ ] The rule records the four-part house card shape as a default a project may override, and rejects
      a sentence template.
- [ ] The rule says how to compose a done-when item and a purpose, and that Estimable and Time-bound do
      not apply here, with the reason.
- [ ] The rule says it shapes composition only and never flags a card a person wrote.
- [ ] `references/ask.md` names `rules/stories.md` for every suggestion it drafts, and never applies it to
      a `you wrote` field.
- [ ] A self-test fixture fails when a suggested done-when is a procedure or a vague outcome, and supplies
      no candidate prose and asserts no word count (`CLAUDE.md`).
- [ ] `python3 -m pytest -q` and `scripts/check-invariants.py` stay green; `check-rule-reachability.py`
      finds the rule reached.

### US-02 — A drafted card carries the house shape, and the oversized test names its source

**Problem.** A session filing a card copies its shape from whatever cards it happens to read. And
`groom-issues` judges oversized cards by demonstrability, a departure from INVEST that cites nothing,
so the next session to read it may "fix" it back to size.

**Solution.** `phil:issue-board`'s *Choosing what becomes an issue* names `rules/stories.md` for a body a
session drafts; `groom-issues`' oversized clause cites the rule, and the rule cites North and Cockburn.

#### Elevator Pitch
Before: a drafted card's shape depends on which cards the session read, and the oversized test reads as
an unsourced house quirk.
After: ask a session to file a card → sees a body with an opening paragraph, what it does, done when and
open questions; read the oversized clause → sees its source.
Decision enabled: whether a drafted card is ready to file as written.

#### Acceptance Criteria
- [ ] `skills/issue-board/SKILL.md` names `rules/stories.md` where a session composes a card body.
- [ ] `groom-issues`' oversized clause cites the rule for its demonstrability test; the scan's five items
      are unchanged.
- [ ] A dogfood: a session drafts one real card for this board from a one-line ask, following the rule,
      and the draft is recorded with the version it ran against.

## Wave: DISCUSS / [REF] Out-of-scope

- Any new scan item, advisory note or flag on a card a person wrote (D3).
- A Definition of Ready, or any gate a card must pass before work starts.
- Estimates, story points or dates on cards (D7).
- Rewriting existing cards to the house shape.
- `nwave-issue-board`'s generated feature-card block — it owns its own shape.
- `/phil:start`'s filing, which writes the developer's title and an empty body by design.

## Wave: DISCUSS / [REF] Definition of Done

1. The research precursor is committed and the rule cites it.
2. `rules/stories.md` holds the stance, the house shape, INVEST, SMART, the 3 Cs, composing guidance and
   Sources, with an ownership line against `writing.md`.
3. `groom-ask`, `issue-board` and `groom-issues` name the rule where D10 places it.
4. The self-test fixture passes, and fails with the rule's citation removed.
5. A dogfood draft is recorded, naming the version or saying the prose was driven by hand.
6. README's Rules list names `stories`; the plugin version is bumped.
7. `python3 -m pytest -q`, `scripts/check-invariants.py` and `scripts/check-rule-reachability.py` pass.
8. `/phil:harden-instructions`, `phil:eos`, `plugin-dev:skill-reviewer` and `plugin-dev:plugin-validator`
   ran over the files they cover (`CLAUDE.md`, *Build path*).
9. The commit message names that `nw-discuss` ran and which passes ran.

## Wave: DISCUSS / [REF] Outcome KPIs

- **Who:** a developer whose session drafts or suggests card content.
- **Does what:** gets a done-when whose every item names an observable outcome, and a card in the house shape.
- **By how much:** every suggested done-when item in the fixture is an observable outcome (all of them);
  zero suggestions phrased as a procedure, a template sentence or a demanded number.
- **Measured by:** the `groom-ask` fixture, plus the dogfood draft.
- **Baseline:** no rule; suggestions follow `writing.md` for wording and nothing for content.

## Wave: DISCUSS / [REF] DoR validation

All nine items pass, read as guidelines (D4 holds here too): job traceable (a facet of an
existing job); persona exists (Robin, extended); ACs testable against a fixture; KPI stated; scope
assessed; evidence base done (D1) with its gaps named in the research; structure decided (D2, D5, D6);
boundaries with `writing.md` and the scan named (D2, D3); out-of-scope listed.

## Wave: DISCUSS / [REF] Slice briefs

- `docs/feature/story-quality-standard/slices/slice-01-rule-and-groom-ask.md`
- `docs/feature/story-quality-standard/slices/slice-02-drafted-cards-and-oversized-source.md`

## Wave: DISCUSS / [REF] Handoff

Order: research precursor → slice 01 → slice 02. Slice 01 carries the most uncertainty — whether a rule
held lightly still changes what a suggestion says — so it goes first. Both slices are small enough to land
in one pull request.

## Wave: DISCUSS / [REF] Delivered (2026-11-09, 1.38.0)

Both slices landed together. Passes run: `nw-discuss`, `plugin-dev:skill-development` read before the
edits, `phil:eos` over the rule and this document, `/phil:harden-instructions` over the three changed
skill passages, and `plugin-dev:skill-reviewer` and `plugin-dev:plugin-validator` over the change — the
`phil:*` passes from the released 1.34.0 copy.

**What the review changed.** The skill reviewer found the first draft of `ask.md` asking a split question
when its suggestions ran past six items. That broke the command's own invariant, *asks only about rules
the scan reported failing*. Now the session drafts no more than about six items, and splitting stays
`/phil:groom-set`'s question. `phil:eos` found the rule's scope listing "an answer it rephrases", which
contradicted `ask.md`'s exclusion of an `I rephrased your answer` rewrite; the rule now keeps a
rephrased answer the person's.

**Dogfood draft (slice 02), driven by hand from this working tree's rule — not the released copy.** The
card this feature came from was filed with a title and an empty body. Drafted to the house shape:

> No file in the plugin named INVEST or SMART, and the house card shape lived only in the cards
> themselves. A session drafting a card copied whatever cards it had read, and `/phil:groom-ask`
> suggested a done-when with nothing to say what a good one is. Stories began as sticky notes and should
> stay simple — the current format is the right level of formal — but the canon belongs in the repo, kept
> in mind rather than imposed.
>
> ## What it holds
> - `rules/stories.md`: INVEST, SMART and the 3 Cs in their authors' words, the house card shape, and how
>   to compose a purpose and a done-when item — applied only to what a session composes.
> - The research behind it, and the three skill passages that name it.
>
> ## Done when
> - `rules/stories.md` exists and cites its research document.
> - `/phil:groom-ask`'s suggestions, `phil:issue-board`'s card drafting and `groom-issues`' oversized
>   clause name the rule, and the scan keeps its five structural items.
> - A `groom-ask` fixture pins that a suggested done-when names observable outcomes — no procedure, bare
>   quality, template sentence or unasked-for number.
> - `python3 -m pytest -q` and `scripts/check-invariants.py` pass, the version is bumped, and the README
>   lists `stories`.

Four done-when items, each one outcome a stranger can check; no `## Open questions`, because nothing is
undecided. The hypothesis held: the draft follows the shape with no template sentence and no number.
