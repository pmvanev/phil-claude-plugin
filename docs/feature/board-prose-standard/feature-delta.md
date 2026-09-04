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
  description' is not checkable"* — which the four structural items answered. This feature answers the
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
- **[D7]** **`groom-issues`' scan is UNCHANGED — four structural items, no style item.** Guarded by
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
| `phil:board-setup` | The `assumed`-line rationales in the delimited `CLAUDE.md` region | Yes — the `assumed` clause is composed, the probed lines are not |

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
| `phil:nwave-issue-board` | Skill | Written sentences name `phil:eos`; [D4]'s in/out boundary stated |
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
Before: an elicited purpose can satisfy all four structural items and still be twice the length it needs.
After: run `/phil:groom-ask` on a title-only card → the written purpose is the answer tightened, and the
per-field provenance label still says whose words they were.
Decision enabled: Robin decides whether the card is ready to rank from the body alone.

**ACs**
1. `skills/groom-issues/SKILL.md` and `commands/groom-ask.md` name the standard for text elicitation
   composes, and state that it applies to composed fields only.
2. **The provenance labels are unchanged.** *I rephrased your answer* already covers a tightened write;
   no fifth label is added. A standard that needed a new provenance value would be changing what
   elicitation may write, which is out of scope.
3. **KPI-5**: the scan's four structural items are byte-unchanged. No style item.

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
| KPI-1 | Prose-generating board surfaces naming the standard | 0 of 6 → **6 of 6** | The grep under *The measurement, re-taken*, re-run |
| KPI-2 | `skills/issue-board/self-test/` entries | 0 → **≥ 1** | `ls` |
| KPI-3 | Total words across issue #36's seven roster descriptions, re-rendered under the standard | **≤ current**, and the delta reported either way | `wc -w` on before and after |
| KPI-4 | Generated surfaces whose output got **longer** | **0** | Word count per surface, before and after |
| KPI-5 | Structural items in `groom-issues`' *well-formed issue* scan | **4, byte-unchanged** | `diff` against 0.82.0 |

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
- **Changing the four structural items.** [D7], guarded by KPI-5.
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
four structural items and the row-count bound both stand, and this feature measures what neither
measured. Recorded explicitly so the absence reads as checked rather than skipped.
