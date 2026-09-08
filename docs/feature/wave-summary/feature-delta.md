# Feature Delta — wave-summary

Forge: issue #39 · Wave: DISCUSS ✓ (2026-09-08)
Density: lean + ask-intelligent (`~/.nwave/global-config.json`; the resolver script is absent from this
install, so the documented cascade default was applied rather than computed)

**Build path:** DISCUSS here, then `plugin-dev:skill-development` and `command-development` before the
files are written, then `plugin-dev:skill-reviewer` and `plugin-dev:plugin-validator` after.

---

## Wave: DISCUSS / [REF] The card's measurement, re-taken

The card measured on 2026-09-04. Re-measured 2026-09-08, because a number four days old was the whole
evidence base and this repo writes deltas faster than it reads them.

| | Card | Now |
|---|---|---|
| Feature deltas | 12 | **15** |
| Total words | 59,544 | **81,942** |
| Median | ~4,600 | **5,539** |
| Largest | 7,080 (`decision-request-standard`) | **9,447 (`story-spans-features`)** |
| `ADR-NNN` references | 157 | 157 |
| `DDD-N` references | 53 | 54 |

**The problem grew 22,000 words in four days**, which is the strongest argument the card has and one it
could not make.

### The card is wrong about slice briefs, and it matters

> *A slice brief is ~400 words (measured on `adversarial-review`'s two briefs: 382 and 423). Summarising
> 400 words into 200 is barely worth a skill.*

**Across all 57 briefs the median is 777 words and the longest is 3,670.** The two cited are the two
shortest in the repo. The card's reason for doubting the slice half is built on its most favourable
sample, and at the real distribution the doubt does not hold.

**This is why the slice half ships** — [D2]. The card's *other* argument for it survives intact and is
better: a brief states what a slice **intended**, and the useful read is what it **landed**.

## Wave: DISCUSS / [REF] Persona ID

**`kai-session-relay`, EXTENDED with a facet — no new persona.**

Kai's standing goal is *"preserve the reasoning that was never written down."* **Here the reasoning
was written down, and that is the problem** — 5,539 median words keyed on handles that resolve nowhere.
Same person, same moment, inverted failure: the shipped session-handoff feature solved *nothing was
recorded*; this solves *it was recorded and cannot be read*.

**Rejected: `morgan-feature-owner`.** Morgan's job is a teammate taking over work **in flight**. These
artifacts are finished. **Rejected: a new persona**, on the precedent this repo has now set three times —
a new persona is earned when the *position* is orthogonal to every domain, as `ari-interrupted-decider`
is. Here the position is Kai's exactly.

## Wave: DISCUSS / [REF] JTBD one-liner

**New job: `learn-what-a-finished-stage-decided`.**

> When I come back to work whose thinking is already finished and recorded, I want to know what it
> decided in a read I can finish in one pass, so I can act on it without reconstructing an argument
> written for the wave that produced it.

**Not a facet of `carry-work-across-session-boundaries`.** That job is about state that was never
captured. This one is about a capture nobody can read. Same persona, different outcome — the precedent is
`know-a-boards-hazards-before-contact`.

## Wave: DISCUSS / [REF] Locked decisions

| # | Decision | Verdict |
|---|---|---|
| D1 | **`/phil:nwave-wave-summary`** | **Locked** — user, 2026-09-08. Matches the two sibling components that face nWave. Says the same word twice and is accepted for it: dropping the prefix would put the command inside another tool's namespace by sight |
| D2 | **Both halves ship, one command with a scale argument** | **Locked** — user, 2026-09-08. They differ in compression and not in shape. The card's case against the slice half rests on the two shortest briefs in the repo |
| D3 | Kai extended; new job | **Locked** — precedents above |
| D4 | **200 words, per summary, enforced by fixtures through `scripts/plain_language.py`** | **Locked**. The module was extracted four commits ago for exactly this kind of second consumer; re-deriving the counter would be the fourth copy it exists to prevent |
| D5 | **No internal identifiers at all — this surface permits none** | **Locked**, and it is the strictest list yet: the portable classes *plus* bare handles, with card numbers forbidden too. A wave summary has no column to put a number in, and stating a decision instead of its number is the whole feature |
| D6 | **"Prior" defaults to the most recently completed, and a name may be given** | **Locked**. Resolving a named target is a superset costing one lookup, and a reader who knows which stage they want should not have to make it the current one |
| D7 | **`mutates: false`, and mechanically so** | **Locked and verified 2026-09-08.** `git log`, `git show` and `git diff` are all on `scripts/check-readonly-commands.py`'s read-only verb allowlist. **This is the first command in the board/summary family whose read-only guarantee is enforced rather than promised** — the opposite of `board-snapshot` and `resume`, and the reason is simply that it touches no forge |
| D8 | **Never derive a status** | **Locked**. `phil:nwave-slice-status` owns every derivation over these files. Two derivations over one source drift |
| D9 | **A stage that recorded nothing is reported as recording nothing** | **Locked**. A confident 200 words about an absent artifact is the failure mode this feature would otherwise introduce |
| D10 | **The slice summary reports what LANDED, not what was intended** | **Locked**. It folds the brief together with the commits and the files that changed. Restating the brief shorter is the version the card rightly doubted |
| D11 | **Quote a decision; never a handle** | **Locked**. Where a decision matters, state the decision. This is D5 read as guidance rather than as a pattern |
| D12 | **Fixtures run against the largest real artifact, currently 9,447 words** | **Locked**. A summary that only fits because its input was small has not been tested — the card says so, and its own named example is no longer the largest |

## Wave: DISCUSS / [REF] Scope assessment

**PASS — 0 of 5 oversized signals.** Two stories, one bounded context, one driving port, no forge, no
network. The near-miss is D10: folding git history into the slice summary is the only part with an
input this feature does not fully control.

## Wave: DISCUSS / [REF] Slices and order

| # | Slice | Answers |
|---|---|---|
| 01 | The stage summary — one finished delta into 200 plain words | Can 9,447 words become 200 that a reader acts on, with no handles? |
| 02 | The slice summary — intent folded with what landed | Does the landed view say something the brief does not? |

**Two slices, not three, and the reason is stated rather than left as an omission.** The obvious third —
enforcement of the ceiling and the vocabulary — is not a slice, because `scripts/plain_language.py`
already exists and both slices consume it from their first commit. Manufacturing a slice for work that
is a two-line import would be the ceremony this repo's own slicing rules warn about.

**Ordered so the cheapest failure comes first.** Slice 01 is the clear win and the larger compression;
slice 02 carries the hypothesis that could still fail.

## Wave: DISCUSS / [REF] WS strategy

**Strategy B — slice 01 is the walking skeleton.** It runs end to end over a real 9,447-word artifact and
renders to a terminal. Nothing is stubbed; the only inputs are files already in the repo.

## Wave: DISCUSS / [REF] Driving ports

- **`/phil:nwave-wave-summary [<feature>]`** — the stage summary. Slice 01.
- **`/phil:nwave-wave-summary --slice [<feature>]`** — the slice summary. Slice 02.

`mutates: false`, per D7.

## Wave: DISCUSS / [REF] Journey

`docs/product/journeys/wave-summary.yaml`. Arc: **deterred → oriented → decided**.

Opening on `deterred` rather than `uncertain` is deliberate. Kai does not doubt the record exists — Kai
can see it, and does not open it, because opening it costs an afternoon. The failure mode is **a complete
record that goes unread**, which is the same shape as the board that is fine and goes unread, one layer in.

## Wave: DISCUSS / [REF] User stories

### S1 — Learn what a finished stage decided without reading it

**As** Kai, **I want** the decisions of a finished stage in 200 plain words, **so that** I can act on them
without reconstructing an argument written for the wave that produced it.

`job_id: learn-what-a-finished-stage-decided`

### Elevator Pitch
Before: the only record of what a stage decided is a 5,539-word median artifact, keyed on handles that resolve nowhere in this repo.
After: run `/phil:nwave-wave-summary board-snapshot` → sees 200 words or fewer, in plain English, naming what was decided and what it rules out.
Decision enabled: whether the thinking already covers the thing you were about to do.

**AC**
1. Output is at or under 200 words, counted on the rendered text, against the largest artifact in the
   repo — currently 9,447 words.
2. No file path, bracketed identifier, bare handle or card number appears in the output.
3. Where a decision matters the decision is stated, never its number.
4. Where the stage recorded nothing, the output says so and does not summarise.
5. The command names which artifact it read.

### S2 — Learn what a finished slice actually landed

**As** Kai, **I want** the slice summary to fold what was intended together with what shipped, **so that**
I learn something the brief does not already say.

`job_id: learn-what-a-finished-stage-decided`

### Elevator Pitch
Before: the brief says what a slice intended; nothing says what it landed, short of reading the commits.
After: run `/phil:nwave-wave-summary --slice board-snapshot` → sees 200 words or fewer covering what shipped, what the brief promised and did not, and what the slice learned.
Decision enabled: whether that slice's ground can be built on, or has to be re-checked.

**AC**
1. Output is at or under 200 words, per slice.
2. The output distinguishes what was intended from what landed, and says so when they agree.
3. A slice whose brief and commits disagree has the disagreement named, not smoothed.
4. Same vocabulary rule as S1.
5. **The output demonstrably says something the brief does not.** Where it cannot, it says that instead
   of padding — the card's own doubt, kept as a test rather than argued away.

## Wave: DISCUSS / [REF] Outcome KPIs

| # | KPI | Target | Method |
|---|---|---|---|
| KPI-1 | Stage summary length, against the largest artifact | **≤ 200 words** | `plain_language.over_ceiling` on the rendered output |
| KPI-2 | Internal identifiers in either output | **0** | `plain_language.identifiers_in` with the strict list |
| KPI-3 | Compression achieved on the largest artifact | **≥ 40×** (9,447 → ≤ 200) | `wc -w` before and after |
| KPI-4 | Slice summaries saying something the brief does not | **≥ 1 of 3 sampled, reported either way** | Read the brief and the summary side by side; a zero is the finding |
| KPI-5 | `mutates: false` holds mechanically | **passes** | `scripts/check-readonly-commands.py` |
| KPI-6 | Call sites of the shared plain-language module | **≥ 4** | `grep` |

**KPI-4 can fail the feature, and is the reason slice 02 is second.** If a slice summary never says
anything its brief does not, the card's doubt was right at the real distribution too, and the slice half
should be dropped rather than shipped.

## Wave: DISCUSS / [REF] Definition of Ready

| # | Item | Status | Evidence |
|---|---|---|---|
| 1 | Persona identified | ✓ | `kai-session-relay`, extended; two rejected alternatives with their precedents |
| 2 | Job traceability | ✓ | New job `learn-what-a-finished-stage-decided`; both stories carry it |
| 3 | Journey mapped | ✓ | `journeys/wave-summary.yaml`, arc upward, error paths for the empty artifact and the disagreeing brief |
| 4 | Stories with elevator pitches | ✓ | S1 and S2, both naming a real invocable entry point |
| 5 | ACs testable | ✓ | Every AC is a count, a presence check or a side-by-side comparison |
| 6 | Scope assessed | ✓ | PASS on 0 of 5; the near-miss named |
| 7 | Slice briefs exist | ✓ | Two under `slices/`, each with a learning hypothesis and IN/OUT scope |
| 8 | Outcome KPIs numeric | ✓ | KPI-1..6; KPI-4 able to fail the feature |
| 9 | Out-of-scope explicit | ✓ | Below |
| 10 | Domain examples with real data | ✓ | 15 live deltas, 57 live briefs, the 2026-09-08 re-measurement. No invented input |

**Self-graded.**

## Wave: DISCUSS / [REF] Out-of-scope

- **Deriving a status.** D8. `phil:nwave-slice-status` owns it.
- **Writing anything into `docs/feature/`.** These read and print.
- **Publishing a summary to a card.** `phil:nwave-issue-board` owns the projection.
- **The session's own *why*.** `phil:handoff` owns that, and it is a different question: what *I* was
  doing, not what the work decided.
- **Changing what the waves record.** The artifacts are the input, not the target.
- **Shortening the artifacts themselves.** A summary is not a licence to edit the source.

## Wave: DISCUSS / [REF] Pre-requisites

- `scripts/plain_language.py` exists with a `permit`-aware vocabulary check — shipped 2026-09-08.
- 15 feature deltas and 57 slice briefs are present and pushed.
- **No blocking dependency on issue #41 or #42.** Both are adjacent. Neither blocks.

## Wave: DISCUSS / [REF] Wave decisions summary

### Requirements summary
Kai returns to finished work and does not open the record, because it costs an afternoon. One command
gives two bounded reads: what a finished stage decided, and what a finished slice landed. Both are 200
words, both are plain English with no internal handles, and both consume the plain-language module rather
than re-deriving it.

### Constraints established
- No forge, no network, no writes — `mutates: false` is mechanically enforceable and is enforced.
- The vocabulary list here is the strictest in the repo: card numbers are forbidden too.
- Two derivations over one source drift, so status stays with the skill that already owns it.
- A stage that recorded nothing must be reported as such rather than summarised.

### Upstream changes
None. No DISCOVER or DIVERGE wave ran, and no prior wave asserted anything this contradicts.
