# Slice 04 — The wave label under mixed waves

**Goal:** Settle what one single-valued wave label says about a card holding features in three waves,
and what `Work this with:` says then — including the case where the answer is that the card is wrong.

**Stories:** S2 (know which command to run when the features are in different waves)
**Answers:** issue #36's question 3

## Learning hypothesis

**Disproves the one-label design** if a single-valued label cannot serve a multi-wave card honestly: if
the current-feature reading misleads in a state grooming does not already flag, the label has to go
multi-valued — which breaks the declaration `groom-issues` rule 4 reads — or disappear from story cards,
which takes the board's biggest cards out of wave filtering.
**Confirms**, if it passes, that the approximation degrades only where the card is already a defect.

## IN scope

- **The label rule** ([D10]): single-valued, equal to the current feature's wave, swapped never added.
  The shipped failure this preserves — four accumulated wave labels and an unreadable record while every
  command reported success — is cited, not restated from memory.
- **Non-monotonicity, stated in the skill and in the block.** The label steps backwards when the next
  feature begins. This reads as an error to anyone who has only seen feature cards, and an unexplained
  backwards step invites someone to "correct" it forwards.
- **The routing line** ([D11]): `Work this with: <command> · feature <id>`. The three shipped rules
  survive verbatim — the wave label is the source, no label means no line, no row means no line **with
  the reason stated**. A fourth is added: **no line ever names a command for the story.**
- **The two-in-flight case, as far as this slice owns it:** where the fold reports two features
  `in progress`, the label takes the first in roster order and the roster's Notes column carries
  `⚠ also in flight` on the other. **The block does not hide it and does not resolve it.** Grooming's
  finding is slice 05's.
- Fixtures: three waves, one label; a backwards step rendered with its explanation; this repo's own
  no-row case on a story card; two in flight, both visible.

## OUT scope

- The grooming finding for two-in-flight — slice 05. This slice makes the state *visible*; that one makes
  it *reported*.
- Wave columns. Settled and unchanged: the wave is never a column
  (`nwave-issue-board` § *Wave is a label on the feature card*), and nothing here reopens it.
- A `wave: mixed` value. Rejected in the delta and not revisited.

## Acceptance criteria

1. A four-feature story spanning three waves carries exactly **one** wave label, and it is the current
   feature's. Pinned by a fixture.
2. The routing line names a command **and** the feature it applies to; a fixture pins a bare
   story-scoped command as a failure.
3. A fixture pins the backwards step as **correct output**, with the explanatory clause present. Without
   that fixture the next reader fixes the non-monotonicity and reintroduces accumulation.
4. This repo's own case still holds: a story whose current feature's wave has no routing row emits no
   line **and says the table does not cover the build path**. The shipped rule is exercised at the new
   tier, not re-derived.
5. Two features in flight render two `▶` rows and a `⚠` note; the label is not silently ambiguous.
6. `groom-issues` rule 4's single-valued declaration for `wave: *` is **untouched**. If this slice needs
   to change it, the design is wrong.

## Dogfood moment

Slice 01's card exhibits the case, but **as a reconstruction, not a live observation** — and the brief
must not claim otherwise. `single-issue-per-feature` finished past DISCUSS on a build path with **no
routing row**; `story-spans-features` sits at DISCUSS, which has one. So the current feature moving from
the first to the second takes the label from *no line* to `/nw-discuss`, which is backwards in wave
order. Position 01 was already done when the card was built, so nobody watched it happen.

**The honest dogfood is therefore the forward half:** advance `story-spans-features` out of DISCUSS and
watch the label and the routing line both change on a real card. The backwards case needs a fixture, and
saying so is the point — the predecessor's rule that a dogfood claim must name what it actually exercised.

## Why this is a slice and not a paragraph in 03

The question has a real open decision behind it and four candidates, three of which fail on shipped,
measured evidence rather than on taste. It also carries the only rule in this feature whose *correct*
behaviour looks like a bug — and a rule like that needs its own fixture and its own explanation, or it
gets helpfully undone.

## Dependencies

- Slice 03's block layout, which the label and routing lines sit above.
- Slice 02's fold, which identifies the current feature.

## Effort

~0.5-1 day. Reference class: the `Work this with:` routing line added on 2026-08-12, which was one table,
three rules and one fixture.

## Carpaccio taste tests

| Test | Result |
|---|---|
| Ships 4+ new components? | No — two header lines and their rules, in one skill. |
| Depends on a new abstraction? | On 02's fold naming a current feature. Shipped. |
| Disproves a pre-commitment? | Yes — that one single-valued label can serve a multi-wave card. |
| Synthetic data only? | No — the backwards step is exercised on #36 for real; the three-wave case is a fixture, since no three-wave story exists here. |
| Duplicate of another slice at scale? | No. 03 owns the tables; this owns the header lines above them, which derive from a different source and fail differently. |

---

## Result — 2026-09-04

**Hand-driven; exercised the prose, not the command** (installed 0.73.0, tree 0.81.0).

### Acceptance criteria

| AC | Verdict |
|---|---|
| 1 — three waves, exactly one label, the current feature's | **met** — fixture 25, including the stale label removed in the same call |
| 2 — routing line names command **and** feature; bare story command fails | **met** — rule plus fixture 27; the one bare routing line in the skill is in the *feature*-tier example, where the qualifier rule does not apply |
| 3 — backwards step pinned as **correct output**, with the clause | **met** — fixture 26 |
| 4 — this repo's no-routing-row case holds at the story tier | **met, and for real** — see below |
| 5 — two in flight render two `▶` and a `⚠`; label not silently ambiguous | **met** — fixture 28 |
| 6 — `groom-issues` rule 4's declaration untouched | **met, verified by `git diff`** — no change under `skills/groom-issues/` |

### AC6 is the one worth showing the work for

`groom-issues` does not merely depend on the wave rule, it **quotes it verbatim**: *"the wave label is
single-valued and must be swapped, not added."* The story-tier rule was therefore written **before** that
sentence rather than rewriting it, so the quotation still resolves — confirmed by grepping both files for
the exact string. Had the story tier needed that sentence changed, the design would have been wrong by
AC6's own test, and the breakage would have surfaced in a *different skill* than the one being edited.

### The dogfood: both halves were unobservable, for different reasons

The brief anticipated one gap and got two.

- **The backwards half** was already known to be a reconstruction: position 01 was done before the card
  existed, so nobody watched the step. The brief says so, and fixture 26 covers it.
- **The forward half was also unavailable, and this was not anticipated.** The brief proposed *"advance
  `story-spans-features` out of DISCUSS and watch the label and the routing line both change on a real
  card."* It **left DISCUSS before this slice ran** — slice 01's finding 2. So the transition the brief
  reserved as the honest live observation had already happened, unwatched, one slice earlier.

**What was exercised for real is fixture 27's case**, and that is genuine: both members are past DISCUSS
on a build path the routing table has no row for, so #36 carries **no wave label and no routing line, and
says why**. The shipped `no row, no line — and say why` rule reached the new tier without being
re-derived, which is AC4 discharged against a real card rather than a fixture.

**The generalisable lesson:** a dogfood that depends on watching a *transition* has to be set up before
the transition, and a slice ordered fourth cannot observe a change its own feature made in slice one. Two
slices in this feature have now lost a measurement to the same shape — slice 01 spent the cold read by
showing the card before the stopwatch existed.

### The card had fallen behind its own rules inside the same session

Regenerating #36 found it **missing the `State:` line slice 03 had made mandatory hours earlier**, and
carrying the pre-story-tier `Order:` form. Neither was wrong when written; both were wrong by the time
they were read.

**Third staleness instance today**, and the pattern is now specific enough to be worth carding rather
than noting: a block goes stale not only when the *work* moves but when the *rule* moves, and
`refresh at boundaries` lists only work events. **"The rule that generates the block changed" is not a
boundary**, and it is the one boundary a self-hosting feature crosses constantly. Belongs on issue #31
alongside "branch pushed".

### Open, pending review

Fixture 28 breaks a two-in-flight tie by **roster order**, while fixture 24 (slice 03) forbids
tie-breaking a **contested position**. If two members are in flight *and* their positions collide, the
two rules meet and this slice did not consider the interaction. Raised with the reviewer rather than
resolved by guess.

### Review round — `plugin-dev:skill-reviewer`, 2026-09-04

**Verdict: Needs revision before ship, 3 critical + 4 major.** All fixed. Fourth consecutive round to
find real defects, and the reviewer was asked to hunt the four shapes slice 03 had already produced. It
found three of them again.

**C1 — I wrote a second definition of `current feature`, and it disagrees with the owner's.** The rule
read *"the label takes the FIRST in roster order"*. `phil:nwave-slice-status` already defines the current
feature as **the first member whose state is not `done`** — not the first member that is in flight. On a
roster `01 to do · 02 in progress · 03 in progress` the owner answers **01** and my rule answers **02**,
and the block would then name one feature in its header, enumerate another's slices, and route to a
third. Nothing errors.

**And my fixture could not have caught it.** Fixture 28's roster is `01 done · 02 in progress · 03 to do
· 04 in progress`, where the first non-`done` member and the first in-flight member are **both 02** — so
it passes under either rule. *A fixture whose input makes a wrong rule return the right answer pins
nothing.* The tie-break is deleted and replaced by a pointer to the owner; fixture **29** carries the
discriminating roster. This is the same defect class as slice 03's, in the file that documents it.

**C2 — the contested case governed the tables and not the header lines.** Slice 03 fixed the renderer
inventing a current feature to *expand*; I left it free to invent one to *label*. Both header lines
derive from the current feature and nothing else, so where the owner withholds it the card now writes
neither. A wave taken from a contender is the same invention one line higher up and easier to miss.

**C3 — I delegated to a check that does not exist**, in the present tense: *"two features in flight is a
defect, **reported by** `phil:groom-issues`"*. Grep for "in flight" in that skill returns **nothing** —
it lands in slice 05. This is verbatim the hazard this same file documents: *"a delegation to a
capability that does not exist reads exactly like a delegation that works."* De-tensed, and the
correction is a *stronger* argument for rendering the state: until slice 05 the block is the only place
it is visible at all.

**M1 — the non-monotonicity clause was in the skill and not in the block**, which is where the rule says
it must be. The worked example therefore failed fixture 26. Worse, *"say so every time"* had two readings
that differ materially, and the natural one fails: a clause emitted only at the transition is gone by the
next refresh, and the reader who "corrects" the label forwards is by construction a **later** reader.
Resolved to *every story block*, with fixed wording and a defined slot — a generated clause with no
specified text is one each run invents.

**M2 — fixture 27 gate-failed behaviour the shipped rule permits.** With no label the branch that fires
is *no label, no line*, which licenses silence; I applied the *no row* branch's "say why" obligation to
it and then gate-failed silence. The finding underneath is better than the fixture was: **rule 2's
justification does not transfer.** It permits silence because the card may not be nWave work — and a
story card is nWave work by definition. So it is a real change at this tier, and my claim that all three
rules "apply unchanged" was false.

**M3 — the input to this whole slice had no named source.** A story member has no card, so it carries no
label; the roster has no wave column; and `nwave-slice-status` returns state, never a wave. The wave now
comes from the member's own `feature-delta.md` header, which is the only artifact that holds one.

**M4 and minors:** the header enumeration was wrong by three lines; fixture 25 justified a stale label
with a chronology its own timeline makes impossible (position 03 was never current) — the same fabricated
warrant shape as slice 03's "budget measured at seven"; fixture 25 pointed at 27 to demonstrate a
distinction 27 cannot show; `[D12]` was cited in fixtures whose readers cannot resolve it; *"the other
member"* was singular where three concurrent members are not excluded; stale line references replaced
with section names, and the delta given a provenance note rather than renumbered — it is a dated record
of what the skills said, and renumbering would make it a record of something else.

**Clean on independent check:** AC6 holds — `groom-issues` still quotes the wave sentence verbatim and
that sentence is unchanged; the wave-is-never-a-column ruling is untouched; the fixture counts and the
routing table are consistent.
