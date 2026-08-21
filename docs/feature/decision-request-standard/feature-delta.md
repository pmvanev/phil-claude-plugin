# Feature Delta — decision-request-standard

Forge: #33 · Wave: DISCUSS ✓ (2026-08-21)
Density: lean + ask-intelligent (`~/.nwave/global-config.json`, read; the resolver script is absent from
this install, so the documented cascade default was applied rather than computed — stated rather than
implied)

**Build path:** DISCUSS here, then authored with `plugin-dev` — not DESIGN/DISTILL/DELIVER. The
deliverable is prose plus one check script, and this repo settled twice that skills are authored rather
than waved (`todo.md` 2026-06-17; edd-loop DDD8). Same path `groom-issues`, `session-handoff`,
`single-issue-per-feature` and `board-setup-block` took.

**Route 3 per `CLAUDE.md` *Where a finding about a standard goes*.** The finding — that nothing governs
how a command poses a question — changes no single skill's assertion, and it is not a repo convention
with a mechanism ready to hand. It is work, and it exceeds a paragraph.

---

## Wave: DISCUSS / [REF] Persona ID

**`ari-interrupted-decider`** — **new**, ninth persona. Registered at
`docs/product/personas/ari-interrupted-decider.yaml`.

Ari is the developer who was doing something else and got **stopped** by a question only they can answer.
Not the person who wanted to think about this — the person interrupted to decide it.

**A new persona rather than a facet, which is the opposite of the call `board-setup-block` made**, and
the difference is worth stating because the two look alike. There, the actor was the same human one step
earlier in the same job, so Robin gained a setup facet. Here the actor is **any of the other eight
personas at a moment orthogonal to their job**: Robin approving a merge, Tess approving a rewrite, Quinn
approving a plan, Avery adjudicating evidence, Rowan reading findings. What separates Ari is not a domain
but a **position** — holding a question, without the asker's context, unable to act until the question is
legible. A facet on one persona would imply the other seven do not hit it. All eight do, which is also
why this feature has more call sites than any other in the repo.

The load-bearing line in Ari's mental model: *"If I have to ask what you're asking, you haven't asked
yet."*

## Wave: DISCUSS / [REF] JTBD one-liner

When a command stops mid-task and hands Ari a decision only Ari can make, Ari wants the question posed in
language they can act on without first reconstructing the asker's context — so they can decide in one
pass instead of spending a turn asking what is actually being asked.

Registered as a new validated job `answer-a-tools-question-without-decoding-it` in
`docs/product/jobs.yaml`. **Orthogonal to all nine existing jobs**, not a facet of any — recorded in the
job's own comment block, because the temptation to attach it to `keep-a-backlog-trustworthy` (the job
whose commands ask the most questions) is real and wrong.

## Wave: DISCUSS / [REF] Locked decisions

- **[D1]** Feature type = **cross-cutting**. Not one new surface: a standard plus its propagation across
  every command that stops to ask. Nineteen files mention `AskUserQuestion`; thirteen commands grant it.
  (Session)
- **[D2]** **New persona, new job.** `ari-interrupted-decider` /
  `answer-a-tools-question-without-decoding-it`. The position, not the domain, is what is distinct —
  see *Persona ID*. (User)
- **[D3]** **Research depth `comprehensive`** — full journey, emotional arc, shared-artifact registry,
  error-path map. The value of this feature lives entirely in its error paths: the three failure modes
  *are* the feature, and specifying a standard without mapping them would produce fixtures with no
  failure mode behind them. (User)
- **[D4]** **200 words is a HARD CEILING on the ask, countable and failable — not a target.** A target
  cannot be measured, and an unmeasurable standard is the same category as the prose that already failed
  here. (User)
- **[D5]** **Supporting context is separated from the ask, placed ABOVE it, and bounded in practice.**
  [D4] would otherwise squeeze a genuinely complicated decision. The ceiling governs the question and
  the options; the context block is outside it.
  **AMENDED 2026-08-21, after slice 01 review.** The original wording — *"permitted, unbounded, and
  separated… it sits below"* — was unimplementable and overclaimed on two counts:
  - **Placement.** `AskUserQuestion` renders the options and *blocks*, so anything emitted after the
    call arrives only once the answer is given, where it cannot be opted into; anything emitted between
    the framing and the call reconstructs the buried-ask failure out of sanctioned parts. Context
    therefore goes **above**. (User, asked and answered 2026-08-21.)
  - **"Unbounded."** Context above the ask pushes the framing further from the prompt, so past some
    length it buries the ask by a different route. There is no countable limit, and the fragment says so
    rather than promising one. The accepted cost of the chosen option, stated in the ask that chose it.
  Two alternatives were declined with their costs recorded: a one-line pointer with detail on request
  (risks the reader never seeing evidence that would have changed the answer) and writing detail to a
  file (nobody opens it). (User)
- **[D6]** **`rules/` cannot carry this, on the mechanism — measured, not argued.** A rule with a
  `paths:` glob fires on the file being touched, and a decision request happens regardless of which file
  is open. The nearest existing standard proves it: `rules/ux.md`'s own *"no internal jargon"* line loads
  only for `**/*.{tsx,jsx,vue,svelte,css,...}` and `**/components/**`, so it is structurally dark for a
  terminal question. And a **pathless** rule is not an always-on rule — `rules/llm-inference.md` states
  the semantics in as many words: *"No `paths` frontmatter, deliberately… Consult this rule when doing
  inference work"*, with `definitions.md` named as the precedent for a **manual-reference** rule. Both
  `rules/` options are therefore dead: one fires on the wrong trigger, the other only fires if something
  already decided to consult it. (Session, evidenced — see *Evidence*)
- **[D7]** **Per-command prose is dead too, and for a measured reason.** `skills/spirit-walk/SKILL.md:66`
  already contains this rule — *"Explain in the user's terms, not the code's jargon"* — invented locally,
  propagated nowhere. And `commands/spirit-walk.md` does **not** grant `AskUserQuestion`: the one place in
  the repo that wrote the rule down is the one place that cannot ask a structured question. Meanwhile
  thirteen commands that *can* say nothing at all. (Session, evidenced)
- **[D8]** **Shape = a shared fragment under `skills/shared/`**, referenced by name from every asking
  skill. The `test-runner-detection.md` precedent is exact: one fragment, five consumers across skills and
  agents, no duplication. Chosen by elimination — [D6] killed both `rules/` options, [D7] killed per-command prose —
  and by the one property the survivors lack: inside a command the reference is **deterministic**.
  (Session)
- **[D9]** **Placement is part of the standard, not only wording.** Failure mode 3 is a placement defect;
  a conforming ask that is buried still fails. A standard governing wording alone would report success on
  a third of the problem. (Session)
- **[D10]** **The reference is enforced by a script, not by convention.** `CLAUDE.md`'s route 2 requires
  a mechanism — *"a convention with no enforcement is exactly the thing that gets noticed twice and
  written down neither time"* — so a command granting `AskUserQuestion` without the reference fails the
  build. Slice 03. (Session)
- **[D11]** **The conversational half is declared unenforceable, in as many words.** Outside a
  `/phil:*` command no deterministic mechanism exists: a skill description is probabilistic and
  `CLAUDE.md` is repo-local and does not ship to consumers. This is stated in the artifact rather than
  papered over, and it is its own slice (04) so that "later slice" and "out of scope" stay
  distinguishable — the lesson [D10] of `board-setup-block`. (Session)
- **[D12]** **Walking skeleton = yes**, WS strategy **C — real local resources**. Slice 01 wires the real
  fragment into a real skill and is dogfooded against this repo's own board the same day. A worked
  example with no live asker would prove the prose parses, which is not the uncertainty. (Session)

## Wave: DISCUSS / [REF] Evidence — measured in this repo, 2026-08-21

Gathered before any artifact was written. Every number below is a command anyone can re-run.

| # | Finding | Command |
|---|---|---|
| E1 | **26** total mentions of `AskUserQuestion` across `skills/` and `commands/` | `grep -ro AskUserQuestion skills/ commands/ \| wc -l` |
| E2 | **13** commands grant it — and **every single mention in `commands/` is the frontmatter grant**. Zero body guidance, in all thirteen. | `grep -rn AskUserQuestion commands/*.md \| grep -v allowed-tools` → **no output** |
| E3 | **8** real usage sites across **6** skills (`refactor-tests` ×2, `redesign-tests` ×2, `work`, `refactor`, `groom-issues`, `edd`); 4 further mentions in self-test fixtures | `grep -rn AskUserQuestion skills/*/SKILL.md \| wc -l` |
| E4 | **Nothing** in `skills/`, `commands/` or `rules/` mandates plain language, forbids internal vocabulary, or sets a length for a question — with exactly two near-misses, E5 and E6 | `grep -rniE "plain english\|no jargon\|word (budget\|ceiling\|limit)\|before the options" skills/ commands/ rules/` |
| E5 | `rules/ux.md:64` says *"no internal jargon"* — but its `paths:` are `.tsx/.jsx/.vue/.svelte/.css/...` plus `components/pages/layouts/styles`. Structurally dark for a terminal question. | `sed -n '1,12p' rules/ux.md` |
| E6 | `skills/spirit-walk/SKILL.md:66` says *"Explain in the user's terms, not the code's jargon"* — and `commands/spirit-walk.md` grants no `AskUserQuestion`. **The rule exists in the one place that cannot fire it.** | `sed -n '1,8p' commands/spirit-walk.md` |
| E7 | A pathless rule is a **manual-reference** rule, not an always-on one. `rules/llm-inference.md` says so explicitly and names `definitions.md` as precedent. Two of the nineteen rules are pathless. | `sed -n '1,12p' rules/llm-inference.md` |
| E8 | **The standard is satisfiable — measured on this wave's own ask.** The three DISCUSS decisions ([D3], [D2], [D4]) were put to the user with a framing of **143 words** and **zero** forbidden tokens, followed by options each naming its own cost. Under the ceiling with 57 words spare, on a three-part question. | `wc -w` on the emitted framing; `grep -oiE` for wave labels, issue numbers, slice ids, D-numbers, tool and path tokens → no matches |

**E8 is the cheapest and most load-bearing number here.** [D4]'s stated risk is that a hard ceiling
squeezes a genuinely complicated decision. The first real test of that was this wave's own elicitation —
three simultaneous decisions, one of them the meta-question about the ceiling itself — and it fit in 143
words. One instance is not a distribution, and slice 02 is where it meets the harder input. But the
ceiling is not obviously wrong, which is what it needed to survive DISCUSS.

**E2 and E6 together are the whole argument for [D8].** Thirteen commands were handed a question-asking
tool with no instructions, and the single author who thought to write instructions put them where the tool
is absent. That is not thirteen oversights; it is a missing artifact.

**E7 is the finding that closed [D6].** The pathless-rule option looked like the obvious home for an
always-on standard right up to the moment the repo's own precedent was read.

## Wave: DISCUSS / [REF] Scope assessment

**PASS — right-sized.** One oversized signal of five fires:

| Signal | Result |
|---|---|
| >10 user stories | ✗ — five |
| >3 bounded contexts or modules | ✗ — one fragment, one script, N referencing skills |
| Walking skeleton needs >5 integration points | ✗ — two: the fragment, one referencing skill |
| Estimated effort >2 weeks | ✗ |
| Multiple independent outcomes that could ship separately | **✓** — the enforced half (inside a command) and the unenforceable half (ordinary conversation) |

The firing signal is answered by [D11] and slice 04 rather than by a split: they are two reaches of one
standard, and splitting them into two features would let the unreachable half quietly become nobody's.

## Wave: DISCUSS / [REF] Story map — backbone

```
A question arrives  →  Read what it is  →  Weigh the options  →  Get detail if wanted  →  Answer  →  Resume
       │                     │                    │                      │                  │         │
  set apart from        what is being       each option names       unbounded, below,    answer /   the ask
  the output that       decided, and        its own cost, not       separated — the      decline /  named what
  preceded it          what turns on it,    only its benefit       escape hatch that     defer     it was
  (placement is        in plain English,                            makes the ceiling               interrupting
  part of asking)      under 200 words                              affordable
```

## Wave: DISCUSS / [REF] Slices and order

| # | Slice | Ships | Hypothesis it can disprove |
|---|---|---|---|
| 01 | The standard, one asker, one countable fixture *(skeleton)* | `skills/shared/decision-request.md` + the groom family referencing it + a word-count fixture | **the whole shape ([D8])**, if a referenced fragment does not change how the question actually comes out |
| 02 | The three failure modes become fixtures | three self-test fixtures — bare list, jargon wall, buried ask | **[D4]**, if the hard ceiling cannot be counted on a real request, and **[D9]**, if "buried" cannot be pinned at all |
| 03 | Every asker conforms, and a script says so | the remaining references + `scripts/check-decision-request-reference.py` | **[D10]**, if conformance turns out not to be mechanically checkable and the mechanism collapses to a convention |
| 04 | The reach outside a command | the declared limit, plus whichever probabilistic mechanism is chosen | **[D11]**, if the conversational half turns out to be reachable after all — which would be good news, recorded |

**Order rationale — highest learning leverage first.** 01 is first because every later slice assumes a
referenced fragment actually changes the output, and nothing has measured that; a failure there costs one
slice rather than four. 02 second because [D4] is the largest untested commitment in the feature — the
hard ceiling is the decision most likely to be wrong, and the fixtures are what would prove it. 03 third
because it needs something to propagate and a fixture set to propagate against. 04 last: widest in
surface, narrowest in learning, and the one whose honest answer may be *"it cannot be enforced"* — which
is worth knowing after the enforceable half is banked, not before.

`Order: slice number — final; /nw-roadmap does not run in this repo.`

**Carpaccio taste tests.** No slice ships four or more new components — 01 ships two, 02 ships three
fixtures, 03 ships one script plus references, 04 ships prose. The abstraction everything depends on —
the fragment — ships **first, as its own slice**, rather than being assumed by all four. Three slices can
disprove a locked decision (01→[D8], 02→[D4]/[D9], 03→[D10]), so the slicing is discipline rather than
decoration. No slice runs on synthetic data: every one is exercised against this repo's real commands.

**One taste test needed an answer rather than a tick.** *"If 2+ slices are identical except for scale,
merge them"* — 01 (one asker) and 03 (all askers) look like exactly that. They are not merged because
their hypotheses differ in kind: 01 asks *does the fragment change the output at all*, 03 asks *can
conformance be enforced mechanically*, and 03's artifact is a script that 01 does not need. Recorded
rather than waved, because a scale-only pair is the failure this test exists to catch and this pair is
one honest reading away from being one.

## Wave: DISCUSS / [REF] WS strategy

**C — real local resources** ([D12]). Slice 01 writes the real fragment and wires it into the real
`groom-issues` skill, then is dogfooded against this repo's own board — the work already in flight, so
the dogfood moment lands the same day rather than being scheduled.

The target is chosen for a reason: the groom family holds the repo's only **elicitation** ask (`groom-ask`
asks what an issue is *for*), which is the hardest case for a 200-word ceiling. Starting on the hardest
asker means [D4] gets its worst input on the slice with the least machinery protecting it, which is where
a wrong ceiling is cheapest to discover.

## Wave: DISCUSS / [REF] Driving ports

| Port | Surface | Change |
|---|---|---|
| `skills/shared/decision-request.md` | **New** fragment (knowledge-only) | The standard itself. No frontmatter, no grant — it is referenced, never invoked |
| `phil:groom-issues` skill | Skill | References the fragment; the elicitation ask in *Resolving the set-level candidates* is the WS site (slice 01) |
| `refactor-tests`, `redesign-tests`, `work`, `refactor`, `edd` skills | Skill | Reference the fragment at their 7 remaining ask sites (slice 03) |
| `scripts/check-decision-request-reference.py` | **New** script | Fails the build when a command grants `AskUserQuestion` and its skill carries no reference ([D10], slice 03) |
| `scripts/check-invariants.py` | Script | Gains the new check, per `CLAUDE.md`'s *"Repo invariants run themselves"* — reports **only** failures |
| `rules/` | — | **No change.** [D6] closed this by measurement; recorded here so a later reader does not re-open it |

The fragment's filename is provisional — `plugin-dev:skill-development` owns naming and layout for
anything under `skills/`, and is consulted before the file is written, per the build path.

## Wave: DISCUSS / [REF] Journey

Full journey at `docs/product/journeys/decision-request-standard.yaml`.

Ari is interrupted, and can *see* that a question exists without hunting for it — the ask is set apart
from the output that preceded it. It opens with what is being decided and what turns on it, in plain
English, no internal vocabulary, inside a countable ceiling. Options follow the framing, never replace
it, and each names its own cost. Supporting detail sits below, separated and unbounded, so it is
available and never in the way. Ari answers, declines or defers — all three first-class — and the ask
named what it was interrupting, so the way back is not reconstructed.

Arc: `jolted-but-oriented → relief → control → trust → confidence → continuity` (upward).

**The arc starts negative and must.** An interruption is a cost; a journey that opened at *neutral* would
design away the one quantity worth minimising. `relief` is the turn — everything downstream follows from
the ask being legible on the first read.

**The accepted risk**, recorded in the journey's error paths: the supporting detail below the ask is
unbounded, so it can grow into the wall of text the ceiling was meant to kill — the ask conforms while
the turn does not. The separation is enforceable; the length below it is not. Naming that is the point.
An unenforced half presented as enforced is the defect this repo has now recorded three times
(`check-readonly-commands.py`'s uncalled function, `devon-ui-developer`'s populated-but-absent field,
rule 4's dark declaration).

## Wave: DISCUSS / [REF] User stories

Every story traces to `job_id: answer-a-tools-question-without-decoding-it`.

### S1 — Answer a command's question without spending a turn on what it means

As Ari, I want the ask to state what is being decided and what turns on it, in plain English, before any
option, so I can answer on the first read.

### Elevator Pitch
Before: a command stops with a numbered list and no statement of what the choice changes, so answering
costs a follow-up turn asking what was asked.
After: run `/phil:groom-set` on this board → sees the ask open with the decision and its consequence in
plain English, under 200 words, options after the framing.
Decision enabled: whether to sanction the irreversible merge, decided in one pass instead of two.

- **AC1** The ask states what is being decided **and** what changes depending on the answer, both before
  the first option appears.
- **AC2** The ask contains no wave label, issue number, slice id, skill name or artifact path.
- **AC3** The ask is ≤200 words, counted mechanically. Over is a failure, not a warning ([D4]).
- **AC4** Each option names its own cost or risk, not only its benefit.
- **AC5** The `groom-issues` skill references `skills/shared/decision-request.md` by name at its ask site.

### S2 — Get the detail without getting the wall

As Ari, I want the jargon-bearing detail available below the ask rather than inside it, so the ceiling
never costs me information I wanted.

### Elevator Pitch
Before: detail and question arrive fused — either the ask is a jargon wall, or the evidence is missing.
After: run `/phil:groom-set` → sees the plain-English ask, then a separated detail section carrying the
issue numbers, paths and evidence.
Decision enabled: whether to answer from the summary or open the evidence first — Ari's call, not the
asker's.

- **AC1** Supporting detail is visibly separated from the ask, not interleaved with it.
- **AC2** Detail is excluded from the 200-word count, and the count is stated as applying to the ask
  alone.
- **AC3** Internal vocabulary forbidden in the ask by S1/AC2 is **permitted** here.
- **AC4** The ask is answerable without reading the detail; the detail is never the only place a
  consequence is stated.

### S3 — See a malformed ask actually fail

As Ari, I want the three ways this goes wrong pinned as fixtures, so a regression is caught rather than
rediscovered.

### Elevator Pitch
Before: the standard is prose, so a bare list, a jargon wall and a buried ask all pass silently.
After: run the `decision-request` self-test → sees three named fixtures fail on the three failure modes
and pass on the conforming ask.
Decision enabled: whether a change to any asking skill regressed the standard, answered by a test rather
than by reading.

- **AC1** Fixture *bare-option-list* fails: options present, framing absent.
- **AC2** Fixture *jargon-wall* fails: internal vocabulary inside the ask.
- **AC3** Fixture *buried-ask* fails on **placement** with wording that would otherwise pass — this is
  the fixture that proves [D9] is a real clause and not a sentence.
- **AC4** A conforming ask passes all three.
- **AC5** The word count is asserted on a real request from slice 01, not a synthetic one.

### S4 — Trust that every asker conforms, without reading nineteen files

As Ari, I want a command that grants the question tool and ignores the standard to fail the build, so
conformance is a fact rather than a hope.

### Elevator Pitch
Before: thirteen commands grant `AskUserQuestion` and not one references any guidance — a gap invisible
unless someone greps for it.
After: run `python3 scripts/check-invariants.py` → sees a named failure for each command that grants the
tool with no reference in its skill, and silence when all conform.
Decision enabled: whether the standard is actually in force, without auditing by hand.

- **AC1** The check fails on a command granting `AskUserQuestion` whose skill carries no reference.
- **AC2** The check is proven to fail on the input that motivated it **before** a green run is trusted —
  `CLAUDE.md`'s standing rule, written after the first `check-readonly-commands.py` silently passed
  because the function was never called.
- **AC3** All 8 existing ask sites across 6 skills reference the fragment.
- **AC4** It reports only failures, per *Repo invariants run themselves*.
- **AC5** An intentional exemption is expressible and must be explicit — silence is never conformance.

### S5 — Know where the standard cannot reach

As Ari, I want the unenforceable half named rather than implied, so a conforming command and an ordinary
conversation are not confused for each other.

### Elevator Pitch
Before: the standard's reach is unstated, so it reads as covering every question when it covers only the
ones inside a command.
After: read `skills/shared/decision-request.md` → sees a section stating that outside a `/phil:*` command
no deterministic mechanism exists, and naming what is used instead.
Decision enabled: whether to trust the standard is in force in a given moment, or to ask for plain
English by hand as before.

- **AC1** The fragment states plainly that the conversational case has no deterministic trigger.
- **AC2** Whichever probabilistic mechanism is chosen is named, with its failure mode.
- **AC3** `CLAUDE.md`'s repo-local reach and its non-shipping to consumers are stated, not assumed.
- **AC4** No claim of coverage the mechanism cannot deliver ([D11]).

## Wave: DISCUSS / [REF] Outcome KPIs

| # | KPI | Target | Method |
|---|---|---|---|
| KPI-1 | Follow-up turns spent asking what was asked, per 10 decision requests | **0** (from a standing ~1-per-ask baseline, the workaround Ari types) | Count over the next 10 asks in real sessions; recorded pass or fail |
| KPI-2 | Asks over the 200-word ceiling | **0** | Mechanical word count in the self-test |
| KPI-3 | Ask sites referencing the fragment | 8 of 8 skills sites; 13 of 13 command grants covered | `scripts/check-decision-request-reference.py` |
| KPI-4 | A reader with no context can state what is being decided and what turns on it | 100% of asks, under 15s | Timed read by someone who did not run the command |
| KPI-5 | Failure modes reproducible as fixtures | 3 of 3 | The self-test; mode 3 is the one at risk, being placement rather than wording |
| KPI-6 | Conformance in ordinary conversation, outside any command | **Not measurable, by construction** | Stated rather than fabricated. [D11] makes this probabilistic; a number here would be theatre |

KPI-6 is the one that matters most to Ari's actual complaint and the one that cannot be measured,
because the mechanism that would measure it is the mechanism that does not exist. Recording it as
unmeasurable is the honest form — `single-issue-per-feature` recorded a *failed* KPI rather than dropping
it, and `board-setup-block` recorded an unmeasurable one; same discipline.

KPI-1's baseline is worth naming: the workaround exists **because** the current rate is near 1.0. That is
the strongest number in this table and it came from the user's own report, not from instrumentation.

## Wave: DISCUSS / [REF] Definition of Ready

| # | Item | Status | Evidence |
|---|---|---|---|
| 1 | Persona identified | ✓ | `ari-interrupted-decider`, new; facet-vs-persona reasoned in *Persona ID* against `board-setup-block`'s opposite call |
| 2 | Job traceability | ✓ | New job `answer-a-tools-question-without-decoding-it`; orthogonality to all nine existing jobs recorded in the job comment |
| 3 | Journey mapped | ✓ | `journeys/decision-request-standard.yaml` — 6 steps, arc upward from a negative start, 11 error paths incl. all three measured failure modes |
| 4 | Stories with elevator pitches | ✓ | S1–S5, each naming a real invocable entry point (`/phil:groom-set`, the self-test, `check-invariants.py`, the fragment itself) |
| 5 | ACs testable | ✓ | Every AC names an observable; KPI-2 and KPI-4 supply numbers for the two that would otherwise be vibes |
| 6 | Scope assessed | ✓ | PASS, one signal of five, answered by [D11] and slice 04 rather than by a split |
| 7 | Slice briefs exist | ✓ | Four briefs under `slices/`, each with a taste-test table |
| 8 | Outcome KPIs numeric | ✓ | KPI-1..6; KPI-6 declared unmeasurable by construction rather than fabricated |
| 9 | Out-of-scope explicit | ✓ | Below |

Requirements completeness: **0.95**. The shortfall is the two items under *Open (→ authoring)*.

**Slice composition hard gate: PASS.** No slice contains only `@infrastructure` stories. 01 carries S1 and
S2, 02 carries S3, 03 carries S4, 04 carries S5 — each user-visible, each with an observable output.

**These nine items were authored for this feature, not taken from a canonical list**, because none is
recorded in this repo — the same self-graded weakness `single-issue-per-feature` and `board-setup-block`
both recorded. Treat the ticked table as a structure check, not an external gate.

## Wave: DISCUSS / [REF] Open (→ authoring)

Two items, both genuinely open and both deliberately left to authoring rather than guessed here.

1. **The fragment's exact filename and whether it is one file or two.**
   `skills/shared/decision-request.md` is provisional. `plugin-dev:skill-development` owns layout under
   `skills/`, and is consulted before the file is written. The live question is whether the standard and
   its three fixtures belong in one fragment or in a fragment plus a `self-test/` directory alongside —
   `skills/shared/` currently holds no fixtures at all, so slice 02 sets that precedent either way and
   should set it knowingly.

2. **Which probabilistic mechanism slice 04 uses for the conversational half.**
   The candidates are a skill whose *description* triggers on the moment (reaches ordinary conversation,
   fires unreliably, ships to consumers) and a line in `CLAUDE.md` (always loaded, fires reliably,
   repo-local, does **not** ship). They are not exclusive and the honest answer may be both, with the
   split stated. Deferred because [D11] already fixes the part that matters — that the limit is declared
   — and choosing the mechanism before slice 03 has measured what enforcement actually catches would be
   speculative design.

## Wave: DISCUSS / [REF] Pre-requisites

- **None blocking.** No prior wave for this feature; `docs/product/` exists so the migration gate passes.
- Slice 03 touches `scripts/check-invariants.py`, which already runs at `SessionStart` — no new wiring.
- Slice 01's dogfood target is the groom family, which is complete and installed. Per `CLAUDE.md`'s
  *Which copy is under test*, any dogfood claim must name the plugin version it exercised, or say plainly
  that the loop was driven by hand against the working tree.

## Wave: DISCUSS / [REF] Out-of-scope

- **Rewording any individual command's existing prompts ahead of the standard.** From #33. The order
  matters: reworded prompts without a standard is exactly the state E6 describes.
- **Changing which decisions get escalated.** This governs how a question is posed, never whether it
  should have been asked — with one deliberate exception carried in the journey's error paths: an ask
  with no stated consequence is a request for reassurance and should not be an ask at all. That is a
  clause of the standard, not a change to the escalation policy.
- **`rules/`.** Closed by [D6] on measurement, not left open. A future reader who wants to re-open it
  should read E5 and E7 first.
- **Issue #34's 200-word board snapshot.** It shares the bounded-output idea and nothing else — a
  different persona, a different job, a different mechanism. Related, not merged.
- **A general output-length standard for the plugin.** Failure mode 3 is about the ask's *placement*
  relative to other output, not about how verbose the rest of the turn is. Widening this into "all
  output should be shorter" would produce a standard nothing can fail.

## Wave: DISCUSS / [REF] Wave decisions summary

### Requirements summary

Primary need: a decision request Ari can answer on the first read — what is being decided and what turns
on it, in plain English with no internal vocabulary, under a countable 200-word ceiling, set apart from
surrounding output, with unbounded detail available below and separate. Delivered as one shared fragment
referenced by every asking skill, enforced by a build check inside a command and declared unenforceable
outside one.

Walking skeleton scope: the fragment plus the `groom-issues` elicitation ask plus one word-count fixture,
dogfooded on this repo's board the same day.

Feature type: cross-cutting.

### Constraints established

- **C1** What is being decided, and what turns on it, both appear before the first option.
- **C2** No internal vocabulary in the ask. Not *explained* jargon — absent jargon; an explained label is
  still a label Ari must hold.
- **C3** 200 words is a hard ceiling on the ask. Countable, failable, not a target.
- **C4** Supporting detail is unbounded, separated, and outside the count. C3 is unaffordable without it.
- **C5** Placement is part of the asking. A conforming ask that is buried still fails.
- **C6** The mechanism is named, and where it cannot be enforced that is stated rather than implied.
- **C7** Silence is not consent. An ambiguous reply is unanswered, and a deferral is recorded as one —
  inherited verbatim from `board-setup-block` C7, same failure, different question.
- **C8** An ask with no stated consequence is not an ask. Decide it and state the assumption instead.

### Upstream changes

None. No DISCOVER or DIVERGE artifacts exist for this feature, so no prior assumption was revised.

### Also found, out of scope

- **`docs/product/personas/devon-ui-developer.yaml` does not parse as YAML.** `yaml.safe_load` raises at
  line 25 — an unquoted list item containing `": "`, parsed as a mapping key. It is the only one of the
  nine persona files that fails. This is the third recorded appearance of the same persona's traceability
  defect (`CLAUDE.md`: *"referenced by `jobs.yaml` with no file for six weeks, noticed three times and
  recorded as out-of-scope twice — a shallow check passes because the field is populated"*). The file now
  exists **and still cannot be read by a parser**, which is the same defect one layer down: the invariant
  script checks the reference resolves to a path, not that the path holds valid YAML. Worth its own card;
  a one-line fix plus a parse check in `check-invariants.py`. Recorded here as the **fourth** notice,
  which by `CLAUDE.md`'s *"add a check here when a defect is found twice"* is overdue.
- The same class of YAML error was hit and fixed in this feature's own new persona file during authoring,
  which is how it was noticed — a parser was run because the file had just been written.
