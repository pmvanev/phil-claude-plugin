# Feature Delta — board-prose-standard

Forge: issue #40 · Wave: DISCUSS ✓ (2026-09-04)
Density: lean + ask-intelligent (`~/.nwave/global-config.json`; the resolver script is absent from this
install, so the documented cascade default was applied rather than computed — stated rather than implied)

**Build path:** DISCUSS here, then authored with `plugin-dev`. Not DESIGN/DISTILL/DELIVER — the
deliverable is prose across six skills and five commands, and this repo settled twice that skills are
authored rather than waved (`todo.md` 2026-06-17; edd-loop DDD8).

**Route 3 whose slices each perform route-1 folds.** Per `CLAUDE.md` *Where a finding about a standard
goes*: the work exceeds a paragraph, so it is a card rather than a fold-back — but every slice below
folds into a `SKILL.md`, adds the fixture that would have caught the gap, and bumps the version. The
route is the container; the folds are the work.

---

## Wave: DISCUSS / [REF] Persona ID

**Two existing personas, both EXTENDED — no new persona.**

- **`robin-backlog-curator`** reads the fields elicitation writes and the comments set-level operations
  leave. Robin's recorded frustration is *"nothing states what a body must contain, so 'appropriate
  description' is not checkable"* — which the five structural items answered. This feature answers the
  half that remained: a body can satisfy all four and still be padded.
- **`morgan-feature-owner`** reads the generated block under a thirty-second budget. The live instance
  is Morgan's: seven two-line roster descriptions on issue #36, written under a stated requirement of
  *"not overly verbose or mentally taxing"*, with no standard consulted.

**A new persona was considered and rejected.** The tempting move is a *reader of machine-written prose*,
on the precedent of `ari-interrupted-decider` — which was created precisely because holding a question
without the asker's context is a POSITION orthogonal to any domain. That reasoning does not transfer.
Ari reads an ask that interrupts the job; Robin and Morgan read prose that IS their job's output. The
role is identical and only the quality bar moved, so the same rule that produced a new file there
produces an extension here.

## Wave: DISCUSS / [REF] JTBD one-liner

**Two existing jobs, both EXTENDED — no new job.** A second job statement over a validated job is the
duplicate-authority defect this repo has recorded twice.

- **`keep-a-backlog-trustworthy`** (Robin) gains a *prose facet*. Its `functional` dimension says *"a
  body that says what and why"* — presence. The facet adds: and reads in one pass.
- **`make-in-flight-work-transferable`** (Morgan) gains a *prose facet*. Its constraint C4/C8 bounds the
  block by ROW COUNT. Rows can be bounded while every cell is padded, so the bound and the standard
  measure different things and neither implies the other.

## Wave: DISCUSS / [REF] Locked decisions

- **[D1]** Feature type = **cross-cutting**. Six skills, five commands, one convention. (Given)
- **[D2]** **The mechanism is NAMING.** Each prose-generating surface names the standard it applies, or
  states in as many words that it applies none and why. Not an apply-before-write rule; not an editor
  run as a step. *(Decided 2026-09-04.)*

  **The accepted cost, stated because it is this board's recurring defect wearing a new hat:** a mention
  satisfies `scripts/check-rule-reachability.py` while nothing changes about the output — the gap
  `CLAUDE.md` documents in as many words, and the shape that produced the `devon-ui-developer` and
  `ui.md` findings. **[D9]'s fixture is what separates this instance from those two**, and it is
  therefore load-bearing rather than a nice-to-have. Recorded, not argued: the card's own done-condition
  asks for naming, and KPI-3 is built to disprove [D2] if naming turns out to change nothing.
- **[D3]** **The standard is CLARITY only** — `rules/writing.md`, applied via `phil:eos`. *(Decided
  2026-09-04.)* `phil:ai-eos` is excluded, and **the exclusion is the skills' own ruling rather than
  this feature's**: `skills/ai-eos/SKILL.md:16` reads *"This skill owns LLM tells only. Clarity,
  concision, and voice belong to `eos`."* Generated board text wants concision, which is `eos`'s.
- **[D4]** **Inside the generated block, only the WRITTEN SENTENCES are in scope.** *(Decided
  2026-09-04.)* In: the two-line roster descriptions, the summarising clause on a linked artifact, and
  the projected `Why` / `Next` / `Stack` prose. Out: header lines, glyphs, timestamps, table scaffolding,
  and every derived cell.

  **This is what keeps [D2] compatible with the one-writer rule.** The block has one writer that
  regenerates it whole; a standard the writer applies to sentences it composes adds no second writer.
  A standard applied to derived cells would — there is nothing to edit in a glyph, so an editing pass
  over them could only be a second author.

  **CORRECTED 2026-09-04, during slice 01, by `plugin-dev:skill-reviewer` finding C1.** As first written,
  D4's in-list put the projected `Why` / `Next` / `Stack` inside **`phil:nwave-issue-board`'s** scope.
  That was wrong, and wrong against this decision's own logic. `phil:session-handoff` step 9 **hands**
  that prose to the board skill with its capture timestamp; the board skill *renders* it. So it is
  composed at `session-handoff` — in scope there, which is **slice 03**, exactly as the surface table
  below already said — and rendered at `nwave-issue-board`, out of scope there. Editing it in the block
  would make the block a non-deterministic function of an unchanged snapshot published under that
  snapshot's own timestamp, which fixture 19 gate-fails.

  **The discriminator is who composed the words, never which column or section they sit in.** Stated
  because the first draft got this wrong by reasoning about *where the text appears*. The correction cuts
  both ways and adds a surface: the `Notes` sentence `nwave-issue-board` composes itself when recording
  that a hand-set state was replaced **is** in scope, though `Notes` is otherwise the owner's. Fixture 31
  pins both halves.
- **[D5]** **Brevity is a PRINCIPLE. No countable ceiling.** *(Decided 2026-09-04.)* The
  200-word hard ceiling of `answer-a-tools-question-without-decoding-it` C3 is **deliberately not
  copied**, and the discriminator is what the number would protect. There, an unbounded ask is the
  failure mode itself. Here the two surfaces already carry their own bounds — a roster description
  declares *two lines*, and the block declares its row count — while the third, an elicited purpose, is
  the one field the whole elicitation exists to get right, and squeezing it is that job's anxiety (A)
  arriving at the wrong target.

  **Accepted cost:** a principle with no number is not failable, which this repo records as *"the same
  category as the prose that already failed"*. Mitigated only by [D9], not answered.
- **[D6]** **The discriminator is checkability, not subject — judging is taste, generating is not.**
  Judging prose a human wrote is the taste-policing `groom-issues` refused. Applying a house standard to
  your own output polices nobody. **This is the `ui.md` split applied a second time**, and it must be
  written where the next author meets it, not only here.
- **[D7]** **`groom-issues`' scan is UNCHANGED — five structural items, no style item.** Guarded by
  KPI-5 rather than by intention. If this feature ends up adding a style rule to the scan it has been
  misread, and the KPI is what says so.
- **[D8]** **The card's reachability list is corrected.** It names six citers of `rules/writing.md`;
  there are **five** surfaces. `ai-eos` cites `technical-communication.md` and defers clarity to `eos`;
  `claude-md` cites `rules/claude-md.md`. Measured 2026-09-04 at 0.82.0. The finding is unaffected —
  the rule is reachable and no board surface names it — and the correction is recorded because a delta
  that repeats a wrong measurement makes it durable.
- **[D9]** **At least one fixture pins generated text against the standard, and `issue-board`'s suite is
  created from scratch to hold one.** It is the only board skill with no `self-test/` (siblings carry
  29, 44, 11, 14 and 27 entries as of 0.82.0). Load-bearing per [D2].

## Wave: DISCUSS / [REF] The measurement, re-taken

The card measured at 0.78.0. Re-measured 2026-09-04 at 0.82.0, all twelve files score **zero** against
`phil:eos|rules/writing.md|Elements of Style|ai-eos|red-team-prose|technical-communication`:

`skills/{issue-board,nwave-issue-board,groom-issues,rank-issues,board-setup,session-handoff}/SKILL.md`,
`commands/{groom-issues,groom-fix,groom-set,groom-ask,rank-issues,board-setup}.md`.

## Wave: DISCUSS / [REF] What actually generates prose

Six surfaces. The right-hand column is what [D2] makes each one name.

| Surface | Sentences it composes | In scope |
|---|---|---|
| `phil:groom-ask` | The purpose and done-condition it writes from your answer | Yes — Robin's field |
| `phil:nwave-issue-board` | Two-line roster descriptions; the summarising clause on each linked artifact | Yes — [D4], the live instance |
| `phil:session-handoff` | The projected `Why` / `Next` / `Stack` prose | Yes — [D4] |
| `phil:issue-board` | The clause after the dash on a `## Chain` line — *why you stopped* | Yes — [D9]'s fixture subject |
| `phil:rank-issues` | The recorded ranking basis; the `## Chain` lines it writes per `issue-board` | Yes; chain convention is `issue-board`'s, cited not restated |
| `phil:board-setup` | ~~The `assumed`-line rationales~~ | **No — corrected in slice 03.** `render-block.py` emits every line from strings in `probe-board.py`; nothing is composed at run time and the skill forbids typing what the script returns. The strings are build-time prose |

## Wave: DISCUSS / [REF] Scope assessment

**PASS — right-sized.** Zero of five oversized signals fire: 4 user stories (threshold >10), one bounded
context, no walking-skeleton integration points beyond one existing board, effort under two weeks, and
the surfaces are one convention rather than independently shippable outcomes.

**The near-miss is worth recording.** Eleven files looks oversized and is not: [D2] makes each surface a
citation rather than a mechanism, so the per-surface cost is a paragraph. Had [D2] gone the other way —
an editor run as a step — the fifth signal would have fired and this would have been five slices.

## Wave: DISCUSS / [REF] Slices and order

`Order: slice number — final; /nw-roadmap does not run in this repo.`

| # | Slice | What it does |
|---|---|---|
| 01 | The live instance, and the honest test | The block's written sentences name the clarity standard; the seven roster descriptions on issue #36 are re-rendered and measured. Disproves [D2] if naming changes nothing. |
| 02 | `issue-board` gets a suite | Creates the missing `self-test/`, with the chain-line *why* as its first fixture. [D9], the load-bearing half. |
| 03 | The remaining four, and the distinction | `groom-ask`, `groom-set`, `rank-issues`, `board-setup`, `session-handoff` name it; [D6] is written where the next author meets it. |

**Slice 01 is first because it can kill the design.** It is the only slice whose failure changes what the
other two do, so ordering it anywhere else spends the cost of five surfaces before learning whether the
mechanism works — the *learning leverage* rule.

## Wave: DISCUSS / [REF] WS strategy

**C — real local resources.** Slice 01 re-renders against the real board (`pmvanev/phil-claude-plugin`,
user project 3), because the uncertainty is *whether a named standard changes composed text*, and a
faked adapter answers a question nobody asked. Subject is issue #36, a completed predecessor, so nothing
in flight is disturbed.

## Wave: DISCUSS / [REF] Driving ports

| Port | Surface | Change |
|---|---|---|
| `phil:nwave-issue-board` | Skill | Composed sentences name `rules/writing.md`; [D4]'s in/out boundary stated as a refusal, plus the who-composed-the-words discriminator |
| `phil:issue-board` | Skill | The `## Chain` clause names the standard; `self-test/` created |
| `phil:session-handoff` | Skill | Projected prose names the standard |
| `/phil:groom-ask`, `/phil:groom-set` | Commands + `groom-issues` skill | Elicited fields and set-level comments name it; [D6] written here |
| `/phil:rank-issues` | Command + skill | Ranking basis names it; chain convention cited, not restated |
| `/phil:board-setup` | Command + skill | `assumed`-line rationales name it |

No new command, no new skill, no new rule in `rules/`. Every surface is existing, which is why [D6]'s
extensions are the honest record rather than a new job standing alone.

## Wave: DISCUSS / [REF] Journey

Full journey at `docs/product/journeys/board-prose-standard.yaml`.

Robin runs elicitation on a title-only card, answers one question, and reads back a purpose that is the
answer tightened rather than the answer padded — with the provenance label still saying which words were
whose. Morgan opens a story card and reads seven roster descriptions where each of the two lines carries
information, and names both positions inside the same thirty seconds the row-count bound was built for.

Arc: `resigned → surprised → oriented → trust` (upward).

**`resigned` is the honest opening beat and it is not `uncertain`.** Robin and Morgan both already get
output that passes every existing check, so neither arrives doubting the tool — they arrive having
stopped expecting the text to be good. The failure mode this feature acts on is *satisfied and padded*,
and an arc that opened on doubt would be describing a different feature.

**The accepted cost, recorded in the journey's error paths:** a named standard is applied by judgement,
so two sessions can produce text of different quality from the same card and both comply. [D9]'s fixture
bounds one surface against one example; it does not make the standard uniform.

## Wave: DISCUSS / [REF] User stories

### S1 — Read a roster description where both lines carry information

`job_id: make-in-flight-work-transferable`

As Morgan, I want the two-line description on each roster row to be composed against the clarity
standard, so that the row count bound and the words inside it are working toward the same thirty seconds.

**Elevator Pitch**
Before: a roster description can be passive and padded and still pass every check the block has, because
every check counts rows.
After: run `/phil:handoff` → the refreshed block's roster descriptions read as tightened prose, and the
skill that composed them names the standard it applied.
Decision enabled: Morgan decides which feature to pick up from the roster alone, without opening a brief.

**ACs**
1. `skills/nwave-issue-board/SKILL.md` names `phil:eos` / `rules/writing.md` at the point it requires the
   two-line description, and states [D4]'s in/out boundary.
2. The seven descriptions on issue #36 are re-rendered and word-counted against their current text.
   **KPI-3** is met or [D2] is reported as disproven — either outcome closes the slice, and reporting
   "no change" as success is the failure this AC exists to prevent.
3. A fixture pins one roster description composed under the standard beside a padded variant that fails.
4. Every existing `nwave-issue-board` fixture passes unchanged.

### S2 — Get back a purpose that is the answer tightened, not padded

`job_id: keep-a-backlog-trustworthy`

As Robin, I want the field elicitation writes from my answer to be composed against the clarity standard,
so that the one field a card is judged on reads in a single pass.

**Elevator Pitch**
Before: an elicited purpose can satisfy every structural item and still be twice the length it needs.
After: run `/phil:groom-ask` on a title-only card → the written purpose is the answer tightened, and the
per-field provenance label still says whose words they were.
Decision enabled: Robin decides whether the card is ready to rank from the body alone.

**ACs**
1. `skills/groom-issues/SKILL.md` and `commands/groom-ask.md` name the standard for text elicitation
   composes, and state that it applies to composed fields only.
2. **The provenance labels are unchanged.** *I rephrased your answer* already covers a tightened write;
   no fifth label is added. A standard that needed a new provenance value would be changing what
   elicitation may write, which is out of scope.
3. **KPI-5**: the scan's five structural items are byte-unchanged. No style item.

### S3 — Read a set-level comment that says why in one pass

`job_id: keep-a-backlog-trustworthy`

As Robin, I want the merge, split and closing comments left on irreversible operations to be composed
against the standard, so that the record of why a card was closed survives being read six months later.

**Elevator Pitch**
Before: a closing comment is the permanent record of an irreversible act and nothing governs how it reads.
After: run `/phil:groom-set` → the comment left on a merged or closed card states the reason in one pass.
Decision enabled: Robin decides whether a past close was right without reconstructing the session.

**ACs**
1. `commands/groom-set.md` and `commands/rank-issues.md` name the standard for the comments and the
   ranking basis they compose.
2. `rank-issues` **cites** `issue-board`'s `## Chain` convention rather than restating it — the
   restate-versus-reference fault this repo has caught three times.

### S4 — Meet the judging-versus-generating distinction where you author `@infrastructure`

`job_id: keep-a-backlog-trustworthy`

As the next author of a board surface, I want [D6] written where I will meet it, so that I do not read
the new citations as licence to flag prose a human wrote.

**Elevator Pitch**
Before: the distinction exists only in a closed card's body.
After: reading any board skill's prose section → the rule states that judging someone's prose is taste
and out of scope, and applying the standard to your own output is not.
Decision enabled: the author decides correctly without re-deriving it.

**ACs**
1. [D6] is stated in `skills/groom-issues/SKILL.md`, where the *well-formed issue* standard already
   opens with the checkability argument it extends.
2. `CLAUDE.md` records the fixture-not-mention requirement from [D2], per route 2 — a convention with a
   mechanism, not a convention alone.

**Marked `@infrastructure`.** It ships inside slice 03 alongside S3, which carries the user-visible
value — the slice composition gate is satisfied and is not being routed around.

## Wave: DISCUSS / [REF] Outcome KPIs

| # | KPI | Target | Method |
|---|---|---|---|
| KPI-1 | Board-family files naming the standard, or stating they apply none and why | 0 of 12 → **12 of 12** | The grep under *The measurement, re-taken*, re-run. **Restated in slice 03:** the original row counted six *composing surfaces*, which turned out to be five — see that outcome |
| KPI-2 | `skills/issue-board/self-test/` entries | 0 → **≥ 1** | `ls` |
| KPI-3 | Total words across issue #36's seven roster descriptions, re-rendered under the standard | **≤ current**, and the delta reported either way | `wc -w` before and after — **measured in slice 01, then found INVALID for the hypothesis; see that outcome** |
| KPI-4 | Generated surfaces whose output got **longer** | **0** | Word count per surface, before and after |
| KPI-5 | Structural items in `groom-issues`' *well-formed issue* scan | **5, byte-unchanged** | `git diff` against the prior commit — **corrected from 4 in slice 03; there were always five** |

**KPI-3 is the one that can fail the feature, and it is two-sided on purpose.** If seven descriptions
written with no standard and seven written under a named one come out the same, [D2] is disproven and the
mechanism has to escalate. A KPI that could only be met would make this feature unfalsifiable, which is
the defect its own subject matter is about.

**KPI-4 exists because two cards on this board want shorter output.** A prose pass that lengthened
anything would be working against them, so the guard is a number rather than an intention.

## Wave: DISCUSS / [REF] Definition of Ready

| # | Item | Status | Evidence |
|---|---|---|---|
| 1 | Persona identified | ✓ | `robin-backlog-curator` + `morgan-feature-owner`, both **extended**; the rejected new-persona alternative and its reasoning are stated |
| 2 | Job traceability | ✓ | Every story carries a `job_id`; both jobs gain a dated *prose facet* |
| 3 | Journey mapped | ✓ | `journeys/board-prose-standard.yaml`, arc upward, error paths carrying [D2]'s and the judgement-variance costs |
| 4 | Stories with elevator pitches | ✓ | S1-S4; S1-S3 name real invocable entry points (`/phil:handoff`, `/phil:groom-ask`, `/phil:groom-set`); S4 marked `@infrastructure` and paired |
| 5 | ACs testable | ✓ | KPI-3 and KPI-5 supply numbers for the two that would otherwise be taste |
| 6 | Scope assessed | ✓ | PASS on 0 of 5 signals; the near-miss and what would have changed it are recorded |
| 7 | Slice briefs exist | ✓ | Three briefs under `slices/`, each ≤100 lines with a learning hypothesis, IN/OUT scope, a dogfood moment and taste tests |
| 8 | Outcome KPIs numeric | ✓ | KPI-1..5, each with a target and a method; KPI-3 two-sided by construction |
| 9 | Out-of-scope explicit | ✓ | Below |
| 10 | 3+ domain examples with real data | ✓ | Issue #36's seven live descriptions (KPI-3), `issue-board:456`'s real chain example, and the 0.82.0 twelve-file grep. No `feature-a` |

**Self-graded.** Stated so a ticked table is not mistaken for an external gate — the weakness
`docs/evolution/2026-08-10-issue-board.md:352` names about `nw-skill-reviewer`.

## Wave: DISCUSS / [REF] Out-of-scope

- **Flagging the prose of issues a human wrote.** [D6]. The taste-policing `groom-issues` refused.
- **Changing the five structural items.** [D7], guarded by KPI-5.
- **Any new rule in `rules/`.** The standard exists; this is about applying it.
- **`phil:ai-eos` and `phil:red-team-prose`.** [D3]. Excluded on the skills' own ownership boundaries,
  not on cost.
- **A countable length ceiling.** [D5].
- **Derived cells inside the generated block** — glyphs, timestamps, header lines, table scaffolding.
  [D4].
- **Self-tests for `eos`, `ai-eos` and `red-team-prose`.** They have none, so this feature cites a
  capability carrying no regression gate of its own. That raises the cost and does not make the gap
  unreal — recorded as the card states it, and not fixed here.
- **Making the standard uniform across sessions.** [D2] is naming, so application is judgement. Recorded
  in the journey's error paths as an accepted cost.

## Wave: DISCUSS / [REF] Pre-requisites

- `rules/writing.md` and `skills/eos/SKILL.md` exist and are reachable — verified 2026-09-04 at 0.82.0.
- Issue #36 is closed and its block is stable, so KPI-3's before-measurement cannot move underneath the
  slice.
- **No dependency on issues #34 or #39.** Both want shorter board output and are adjacent, not blocking;
  KPI-4 is the guard that keeps this feature from working against them. Recorded here rather than as a
  forge link, because neither blocks the other in either direction.

## Wave: DISCUSS / [REF] Wave decisions summary

### Requirements summary
Six board surfaces compose prose that lands where the whole team reads it, and none names a prose
standard. Each will name the clarity standard, one fixture will pin composed text against it, and the
judging-versus-generating distinction will be written where the next author meets it.

### Constraints established
- C1 **Naming, not applying.** [D2] — with [D9]'s fixture as the mechanism that keeps it from being a
  bare mention.
- C2 **Clarity only.** [D3] — on `ai-eos`'s own ownership ruling.
- C3 **Composed sentences only, never derived cells.** [D4] — what keeps C1 compatible with one writer.
- C4 **Brevity as principle, no number.** [D5] — the 200-word precedent deliberately not copied.
- C5 **Judging is taste; generating is not.** [D6] — stated where an author meets it, not only here.
- C6 **The shipped scan is untouched.** [D7], guarded by KPI-5.
- C7 **Two-sided KPIs.** KPI-3 can disprove C1; KPI-4 can catch this feature harming its neighbours.

### Upstream changes
None. No DISCOVER or DIVERGE wave ran for this card, and no prior feature's assumption is amended — the
five structural items and the row-count bound both stand, and this feature measures what neither
measured. Recorded explicitly so the absence reads as checked rather than skipped.

---

## Outcome — slice 01, 2026-09-04

**Build path:** `nw-discuss` produced the brief (committed `87b8c5f`);
`plugin-dev:skill-development` consulted **before** editing the skill; `plugin-dev:skill-reviewer` and
`plugin-dev:plugin-validator` both run over the result. The reviewer returned **3 critical + 6 major**
and its criticals were correct; what shipped is the post-review state.

### What shipped

`skills/nwave-issue-board/SKILL.md` gains *Compose the block's own sentences against the clarity
standard*: the citation, the in/out lists written as a refusal, the who-composed-the-words
discriminator, the one-writer compatibility argument, and [D6]. Fixtures 30 and 31 added. Version
0.82.0 → 0.83.0.

### KPI-3 — measured, then found invalid for the hypothesis

**The number: 150 → 142 words across the seven descriptions. −8 words, −5.3%. Three of seven rows
unchanged. Zero rows longer (KPI-4 met at this surface).**

**That neither confirms nor disproves [D2], and the reason is that the instrument measures the wrong
thing.** Three faults, in ascending order of how badly they break it:

1. **A word count measures one of the standard's eleven principles.** `rules/writing.md` asks for active
   voice, positive form, definite and concrete language, parallel structure for coordinate ideas, related
   words kept together, and the emphatic word last. Only *omit needless words* shows up in `wc -w`. The
   three "unchanged" rows already satisfied all eleven — they are **conformant**, not evidence of a null
   effect, and a count cannot tell those two apart.
2. **The baseline is near-optimal.** Those seven were composed by a careful session under an explicit
   *"not overly verbose or mentally taxing"* requirement — the hardest available case for a tightening
   standard, and not representative of the failure [D2] is meant to prevent.
3. **The measurer was not independent.** [D2] claims that *a future session reading the citation composes
   better text*. What was measured is whether the session that had just written the citation could tighten
   seven sentences it was actively grading. Those are different claims and only the first is [D2].

**Verdict: [D2] is UNPROVEN, not confirmed and not disproven.** Recorded that way because slice 01's AC2
makes silence the failure it exists to prevent, and "5.3% shorter" reported as a pass would be the same
failure wearing a number.

**KPI-3 is therefore demoted from evidence to context, and fixture 30 becomes the gate.** A fixture is
independent of who composes, runs on every change, and — after the reviewer's C2 — supplies a brief with
**no candidate text**, so it tests composition rather than selection. This is what [D2]'s recorded cost
predicted in as many words: *"[D9]'s fixture is what separates this instance from those two."* It arrived
as a measurement rather than a worry.

**A valid future instrument, named so it is not re-improvised:** compose descriptions for one feature
with the citation present and absent, in sessions that do not know they are being compared. This repo
cannot run that in one session, which is itself worth knowing before another KPI is written this way.

### What was deliberately not done

- **Issue #36's block was not overwritten.** The card is closed and its block is the record of how that
  feature went. Re-rendering into it would have destroyed the "before" side of the only measurement the
  slice had. The seven composed variants live here instead.
- **AC5 is UNVERIFIED, and this is the honest state.** `nwave-issue-board`'s 30 fixtures have **no
  automated driver** — `tests/test_self_test_fixtures.py` covers `refactor-tests` and `refactor/`, and no
  test in the 510-case suite reads this suite. So the green run says nothing about AC5. **Fixture 23 was
  hand-driven** because the one edit to pre-existing normative text was a dedupe of the glyph rule, which
  23 is the fixture for; it passes, with every clause it pins preserved. The other 28 were not re-driven.
- **`SKILL.md` was not split into `references/`.** It is now 8,744 words against an authoring target of
  1,500-2,000 and a stated maximum of 5,000, with no `references/` directory — the reviewer's M5, and its
  sharpest form is that the file naming a concision standard is 4.4× the target. Route 3: a card, not a
  fold-back. The one part fixed here is the defect that would have been quoted back: a near-verbatim
  restatement of the glyph rule two paragraphs apart, now deduped.

### Two findings outside this feature, both raised by the validator

- **Three unparseable YAML files in `docs/product/`** — `journeys/story-spans-features.yaml` and two
  instances in `personas/devon-ui-developer.yaml`, all the same defect class: an unquoted `: ` or a
  leading `"` in a plain scalar. Fixed here because they are two-line quoting fixes on SSOT files.
  **`scripts/check-product-ssot.py` reported `OK ... all resolve` while two of the files it counted could
  not be parsed** — it is regex-based by a stated design decision. Whether to add a `yaml.safe_load` pass
  is a real decision, because it costs that script its declared dependency-free property; it is not taken
  here. **The defect has now been found three times** (twice in `devon-ui-developer`, once in the
  journey), plus once self-inflicted and caught during this wave, which is past `CLAUDE.md`'s
  found-twice threshold.
- **A parser hides its successors.** Fixing the first YAML error revealed a second in the same file, then
  a third. One reported failure was three defects.

## Outcome — slice 02, 2026-09-04

**Build path:** `plugin-dev:skill-development` consulted in this session before slice 01 and applied
again here; its findings on suite conventions came from measuring the repo rather than from the guide.

### The hypothesis is answered, and the answer is "neither"

Slice 02 asked whether creating this repo's first board-skill suite from scratch needs a harness that
does not exist, presuming the sibling pattern was copyable. **Measured at 0.83.0 across all suites:**

- **The convention is partly shared and partly local.** `situation` (158 uses, 8 skills) and
  `expected_guard` (145 uses, 11 skills) are genuinely shared. Past those it forks into two schemes:
  `fixture_id` + `expected_decision` (6 skills) and `fixture` + `expected_outcome` (5 skills). **
  `rank-issues` uses both.**
- **So "match the sibling convention" was never a followable instruction** — there was no single one to
  match. The brief assumed one existed. `issue-board` uses `fixture_id` + `expected_decision`, chosen on
  a mechanical ground rather than taste: the one portable driver in the repo is written against it.
- **The harness does exist and is copyable.** `tests/test_board_setup_fixtures.py` is the pattern, and
  its value is that it is **honest about what it cannot do** — *"judging whether a run reached the right
  decision is not automatable here, and this file does not pretend otherwise."* It checks that fixtures
  stay well-formed and cite live outcomes, and its docstring records the drift it caught.

### The finding that dwarfed the slice

**8 of 13 suites had no driver at all — 131 fixtures behind no gate**, including `groom-issues`, the
largest suite in the repo at 43. Every one of those READMEs calls itself a gate; the 510-case suite was
green and said nothing about any of them.

Slice 01 filed this as issue 42 about `nwave-issue-board` alone — 1 suite, 30 fixtures. **That card was
corrected the same day**, because a finding filed at one-eighth of its real scope is worse than one filed
late: it looks handled.

### Scope extended beyond the brief, deliberately

The brief listed a directory, a README, one fixture, the citation and a version bump. **It did not list a
driver, and one shipped anyway.** Creating a fresh ungated suite would have made the 131 into 132 while
the card naming that exact defect sat open — reproducing a known defect at the moment of discovering its
scale. `tests/test_issue_board_fixtures.py` is ~60 lines ported from the board-setup pattern.

**It carries one check the pattern did not have**, because slice 01 earned it: *no fixture may supply
candidate prose*, and *no fixture may assert a word ceiling*. Those are `[D5]` and reviewer finding C2
turned into a gate, so the mistake slice 01 shipped and had to be told about cannot recur silently in a
suite written later.

### The driver was mutation-tested before being trusted

`CLAUDE.md` states the reason in as many words: the first `check-readonly-commands.py` *"silently passed
because the function was written and never called"*. **Twelve mutations, twelve caught, against a clean
baseline** — candidate prose injected, an undefined outcome, two outcomes where one is allowed, a word
ceiling, a deleted `expected.md`, an outcome defined with no fixture, a `fixture_id` that stopped matching
its directory, `situation` and `expected_guard` removed, a README that stops documenting an outcome, the
whole suite deleted, and `enumerable_facts` emptied.

**The first verification harness was itself broken and reported twelve clean passes.** Bash word-splitting
mangled its `cd`, so every "mutation" ran the unmutated tree. It was caught because *"whole suite deleted
→ 8 passed"* is impossible. **The lesson recurses:** a test of a test needs a case whose expected result
is obviously impossible, or it certifies nothing. Recorded because the failure mode was identical to the
one `CLAUDE.md` warns about, one level up, and nothing in the repo would have caught it.

### What is still not verified

`skills/issue-board/self-test/` has one fixture, and one fixture is coverage of one rule. The skill has
twenty-odd sections of forge mechanics — silent-success hazards, tier gating, two-pass seeding, column
ordering — and none of them is pinned. The suite exists and is gated; it is not yet a regression net.
Stated so its existence is not mistaken for coverage, which is the same error as a mention mistaken for
an application.

## Outcome — slice 03, 2026-09-04

### The hypothesis fired: D6 is one discriminator, not one rule

Slice 03 predicted elicitation would be the counterexample, *"because it writes words a human supplied,
so 'your own output' is not obviously what it produces."* **It is the counterexample, and the shape is
better than predicted.**

**The discriminator holds at every surface — but it fired on THREE of them, not one, and the first
draft of this outcome claimed it "holds unchanged at all six". That claim was wrong**, and
`plugin-dev:skill-reviewer` refuted it with three criticals. The hypothesis was built to surface exactly
this, and it surfaced more than the brief predicted:

1. **`groom-ask` — granularity.** The discriminator applies **per field**, keyed on the provenance label
   that already exists. Predicted by the brief; detailed below.
2. **`board-setup` — the composer is not the session.** The `assumed` rationale is emitted by
   `render-block.py` from string literals in `probe-board.py`. The shipped citation told a session to
   compose text the same skill forbids it to type — *"never type a value this script could return"* —
   and at the one surface where doing so breaks a determinism guarantee. **The prose is real and
   `writing.md` still governs it, at build time, in the script, by whoever edits the literals.** That is
   the `ui.md` class `CLAUDE.md` already describes: a rule whose reviewable part has not been separated
   from its build-time part. Corrected to *applies none*.
3. **`session-handoff` — half the surface is the human's.** The why and the next action are composed by
   the session; **the stack is not.** A frame's `what` and `why` are the human's arguments to `push`,
   *the reason for a diversion exists only in the human's head at that moment*, and existing frames are
   reproduced **byte-for-byte**. The shipped citation swept the stack in — the `you wrote` violation of
   the very clause this slice wrote, one surface over. Now excluded and pinned by `self-test/27`.

**So the count moved: five composing surfaces, not six**, and two of the three counterexamples were
invisible until someone read the renderer and the push rule rather than the prose.

| Label | Composed by | Standard |
|---|---|---|
| `you accepted my suggestion` | the session, at draft time | applies **when the suggestion is drafted**, never after acceptance — an accepted suggestion is quoted verbatim |
| `I rephrased your answer` | the session | **applies** |
| `you wrote` | the human | **never touched** |
| `you edited my suggestion` | the human, past the edit | **never touched** |

**Applying the standard to a `you wrote` field would break the provenance system**, not merely overstep:
the label would assert the human's words over a sentence the session had tightened. That is the system
reporting success with the exact thing it exists to record destroyed — the failure mode this repo keeps
finding, arriving in a new place.

**And the standard was already there at that surface, unnamed.** The existing clause reads *"Rephrasing
is a tidying licence, not a modelling one. Fix grammar, punctuation and register; never introduce a
concept the human did not use."* **That is `rules/writing.md` restricted to a rewrite.** So naming it
adds no rule and grants no licence — it gives an existing clause a checkable referent. This is the
cleanest vindication [D2]'s naming mechanism gets anywhere in the feature: the rule existed, unnamed,
and naming it was the whole of the work.

### The count was wrong, in the card and in this document

**`groom-issues`' standard has FIVE structural items, not four.** Item 5 is *"A `## Chain` section when
blocked or related — the edge **and** the reason it exists, on both ends."* The card's central framing —
*"all four ask whether something is there"* — was built on a miscount, and this delta repeated it in six
places. Corrected above; KPI-5's target moves from 4 to 5.

**The framing survives the correction, and item 5 is why it survives interestingly.** Item 5 already
demands *the reason*, so the scan checks a reason is **present** while the standard governs how it
**reads** — the presence-versus-quality split this whole feature rests on, sitting inside the very rule
the card cited as asking presence only. Slice 02 pinned the same clause from the other side, in
`issue-board`. Two checks, one clause, different questions.

### KPI results

- **KPI-1: 12 of 12, from 0 of 12.** Ten surfaces name `rules/writing.md`. **Two state that they apply
  none, and why** — `groom-issues` reports and composes nothing; `groom-fix` never asks, so it may never
  draft, and where it completes a chain it writes the edge and never the clause. That is the card's own
  second branch, and it is the honest answer for those two. AC1 demanded a non-zero grep for all
  twelve and **passes as written**, because both refusal statements name `rules/writing.md` in stating
  what they do not apply. An earlier draft of this outcome called AC1 wrong; that was itself wrong.
- **KPI-5: 5 items, byte-unchanged.** Verified by `git diff`: 37 lines added, **zero removed**, and the
  block compared verbatim against the prior commit. The first hash comparison was invalid — the new
  subsection fell inside the `sed` range — which is worth recording because a hash that moves for a
  benign reason is indistinguishable from one that moves for a real one.
- **KPI-4: vacuous at these surfaces, and stated rather than claimed.** No generated output was
  recomposed in slice 03, so nothing got longer — that is arithmetic, not evidence. The only real
  measurement remains slice 01's seven descriptions, where zero got longer.

### The dogfood was declined, not skipped

The brief called for running `/phil:groom-ask` against a live card. **That cannot exercise this slice:**
`/phil:*` commands load the installed snapshot, which is 0.73.0, while these edits are in a 0.85.0
working tree. A run would have reported on prose written months ago. Hand-driving the skill text would
exercise **the prose and not the command**, which `CLAUDE.md` requires be said outright.

Declined on the precedent of `story-spans-features` slice 05, whose firing-half dogfood was declined for
a comparable reason and recorded as such. **The standing cost of dogfooding a working tree through a
cached command is now visible in three consecutive slices**, and it is not a defect in any of them.

### What the review changed, and why it is recorded rather than quietly fixed

`plugin-dev:skill-reviewer` falsified "slice 03 is done" with **five criticals**, and three of them said
the shipped citation was **factually wrong about who composes the words** — the one thing [D6] exists to
get right. That is worth recording plainly: the mechanism of this feature is *naming*, and a name that
points at the wrong author is worse than no name, because it reads as verified.

| # | What was shipped | Why it was wrong |
|---|---|---|
| C1 | `board-setup` told a session to compose the `assumed` rationale | A script emits it; the skill forbids typing it; hand-writing the region breaks determinism |
| C2 | The same insertion split the provenance table | The `declared` row detached and rendered as literal text, right above *"The third category is not decoration"* |
| C3 | `session-handoff` swept the stack into the composed set, at step 9 | Frames are the human's words, reproduced byte-for-byte; step 9 is the handover, not the composition point |
| C4 | `groom-fix` "writes only the missing edge, never the clause" | Fixture 10 pins that mirroring *invents nothing* and that **asking is a gate failure**; as shipped, the fix could not clear its own rule-5 finding |
| C5 | Two assertions that every citation ships a fixture | Five citations shipped with zero fixtures — the rule violated by the commit asserting it |

**C4 is the one that would have done real damage.** It was a *behaviour* change inside a slice whose
mechanism is naming, on a file the brief's IN scope never listed, recorded in this delta as a citation.
The correct justification was available and simpler: `groom-fix` composes nothing because it **quotes**
the other end's reason — the *renders words another owner composed* branch of [D6].

**C5 is resolved by two fixtures and one honest amendment.** `groom-issues` 44 pins a `you wrote` field
left untouched; `session-handoff` 27 pins a stack frame reproduced byte-for-byte while the snapshot's own
why is composed. They are a deliberate pair, and each fails the degenerate mechanism the other passes.
**Two citations remain unpinned — `groom-set`'s comments and `rank-issues`' basis — and both assertions
now say so**, because an unstated gap in a rule about unenforced mentions is that rule failing in its own
terms.

**Fixture 27 was itself defective on first write, and the driver caught it**: frames encoded as objects
where the suite's format is a string, and the fixture unregistered in its README. `session-handoff` is
one of the five suites that *has* a driver, and it failed in 0.1 seconds. `groom-issues` has none, so
fixture 44 was checked by reading. **That contrast, inside one commit, is the whole argument of issue
42** — measured rather than asserted.

### Two smaller corrections

- **The eleven-principles claim was wrong in six files.** `rules/writing.md` carries eleven *Elementary
  Principles of Composition* plus four other sections; the citations said the standard **is** eleven
  principles. Now *"eleven principles of composition"* everywhere, verified against the referent's
  eleven rows.
- **Placement drift, recorded because the brief specified otherwise.** The brief said [D6] goes at the
  standard and *"not in a new section: an author reading the standard meets it there."* It shipped as a
  new `###` subsection at the end of that section. Defensible — an author reading the standard still
  reaches it — but it is a deviation and was undocumented until now.
