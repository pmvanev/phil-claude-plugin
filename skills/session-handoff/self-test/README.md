# phil:session-handoff — Acceptance Self-Test

The **capture + read-back spine** is the software under test. Its bugs are silent: a snapshot that
quietly records derivable state looks like a *fuller* snapshot; a stale resume point presented as
current looks like a *smooth* resume; a session that does the work inline instead of handing it to the
command that owns it looks like a *productive* session. Each failure mode is indistinguishable from
success at a glance, which is why the skill is never changed and eyeballed — it is changed and
regression-tested here.

These fixtures feed the spine known situations and assert each produces the correct **decision
outcome**:

`CAPTURE` · `NO-OP` · `REFUSE-DERIVABLE` · `PROJECTED` · `PROJECTION-UNREFRESHED` · `RESUME-CURRENT` ·
`RESUME-STALE` · `RECONSTRUCT` · `ROUTE` · `ROUTE-LIVE-WINS` · `ASK-OWNER` · `BOARD-AGREES` ·
`BOARD-DIVERGES` · `BOARD-UNREADABLE` · `REPORT-CLAIM-CONFLICT` · `PUSHED` · `POPPED` · `SHOWN` ·
`STACK-EMPTY` · `STACK-UNKNOWN` · `WRITE-REFUSED`

This suite is the acceptance + regression gate for `skills/session-handoff/SKILL.md`. Format and intent mirror `skills/edd/self-test/`, `skills/work/self-test/`, and
`skills/refactor-tests/self-test/` — this plugin's established way to test a skill.

Delegate results (the read-only `nwave-slice-status` skill — never `/nw-continue`, which launches a
wave) and forge state are **supplied by
`manifest.json`** so the suite runs unattended. In live use they come from the real delegates and the
real board. Those own their own gates; this suite does not re-test them — it tests the spine around
them.

## What the fixtures pin

| Fixture | Situation | Pins | Guard under test | Expected outcome |
|---|---|---|---|---|
| `01-capture-and-resume/` | a session decided something and named a next action (**walking skeleton**) | slice-01 AC1, AC2 | the loop closes end to end | `CAPTURE` then `RESUME-CURRENT` |
| `02-no-op-session/` | the session advanced nothing | slice-01 AC5, **KPI-4** | no ceremony on a no-op (C4) | `NO-OP` — nothing written, and said so |
| `03-refuse-derivable/` | state offered that an artifact already owns | slice-01 AC6, **KPI-5** | one system of record (C8, DDD-5) | `REFUSE-DERIVABLE` — pointer kept, value derived later |
| `04-stale-refuses-to-resume/` | the tree moved after capture | slice-01 AC3, **KPI-3 (hard zero)** | freshness is a verdict, not a footnote (C1) | `RESUME-STALE` — delta stated, briefing withheld |
| `05-no-resume-point/` | no snapshot exists | slice-01 AC4 | reconstruction is labelled as such | `RECONSTRUCT` |
| `06-route-to-owner/` | work carries a wave label | slice-02 AC1, AC2, **KPI-2** | route, never freelance | `ROUTE` — names the owner and hands over |
| `07-live-wins-over-recorded/` | recorded owner disagrees with the live label | slice-02 AC3 | live beats recorded, disagreement surfaced | `ROUTE-LIVE-WINS` |
| `08-unknown-owner-asks/` | no owner determinable | slice-02 AC4 | unknown is stated, never defaulted (C5) | `ASK-OWNER` — work not begun |
| `09-claim-and-basis/` | a card was claimed for a stated reason | slice-03 AC1, AC2 — **slice not built** | the session→card link survives | `CAPTURE` carrying claim + basis |
| `10-competing-claim/` | two snapshots claim one card | slice-03 AC4 — **slice not built** | detection without resolution (C6) | `REPORT-CLAIM-CONFLICT` — neither discarded |
| `11-local-write-precedes-projection/` | the forge is unreachable mid-capture | single-issue-per-feature slice-04 AC1 | the snapshot is written first, so a forge failure never costs the authority | `CAPTURE` + `PROJECTION-UNREFRESHED` |
| `12-absent-stack-renders-unknown/` | a teammate inherits a card whose owner never captured | slice-04 AC2 | absent renders `unknown`; empty asserts there were no diversions | `RECONSTRUCT` — three sections `unknown` |
| `13-board-diverges-from-snapshot/` | the tree matches the snapshot exactly, but the board's in-flight card is different work | **#24** done-when | the freshness verdict cannot see the board; detect and do **not** resolve | `RESUME-CURRENT` + `BOARD-DIVERGES` |
| `14-board-agrees-with-snapshot/` | snapshot and the In Progress card name the same work, while a *different* card tops Todo | **#24** done-when | agreement is reported out loud; `In Progress` outranks top Todo | `RESUME-CURRENT` + `BOARD-AGREES` |
| `15-board-unreadable-says-so/` | the repo has no board — the common case in the wild | **#24** | a check that cannot run says so, and never defaults to agreement | `RESUME-CURRENT` + `BOARD-UNREADABLE` |
| `16-push-preserves-payload/` | a push onto a snapshot a **previous** session wrote | live-work-stack slice-01 AC1, AC3 | payload **and header** survive byte-identical, **and the primary path is not refused** | `PUSHED` |
| `17-competing-write-refused/` | the file changes between read and write | slice-01 AC3 | compare-and-swap refuses, reports both hashes, never retries | `WRITE-REFUSED` |
| `18-show-at-depth/` | three deep, snapshot the only input | slice-01 AC2, **KPI-3** | every frame ages from a full timestamp; **nothing is judged stale** | `SHOWN` |
| `19-unknown-is-not-none/` | no snapshot vs. a snapshot with no diversions | slice-01 AC5 | `unknown` is about the record, `none` is about the work | `STACK-UNKNOWN` / `STACK-EMPTY` |
| `20-push-with-no-resume-point/` | a push is the first thing ever recorded | slice-01 AC4 | the snapshot is created; `Why`/`Next` absent not empty; `captured: never` | `PUSHED` |
| `21-pop-to-the-parent/` | the innermost detour closes | slice-02 AC1 | depth drops by one, the parent is **named**, payload and header untouched | `POPPED` |
| `22-never-popped-frame-is-stale/` | three old frames, `crossed` 2 / 1 / 0 | slice-02 AC3/AC4, **#29 done-when** | mark at `crossed`≥2 only — one wind-down is normal, and **age is never the oracle** | `SHOWN` |
| `23-push-onto-an-open-frame/` | pushing while a frame is already open | **#29 done-when** | the nesting case: indent, elbow, innermost-last, parent untouched | `PUSHED` |
| `24-capture-carries-the-stack-forward/` | a wind-down through an open stack, with a **wrong** session account | `CAPTURE` step 5 | the **file** is authoritative for existing frames; `crossed` increments; `open since` never re-derived | `CAPTURE` |
| `25-pop-nothing-two-ways/` | pop with no snapshot, vs pop with no stack | slice-02 AC2 | the two nothings do not collapse, and neither writes | `STACK-UNKNOWN` / `STACK-EMPTY` |
| `26-pop-refuses-and-reports-stale/` | pop against a changed file; pop of a stale frame | pop's CAS + step 5 | the two branches fixture `21` asserts but cannot detect | `WRITE-REFUSED` / `POPPED` |

## The two sharpest fixtures

**`04` is the one that matters most.** A stale resume point that presents itself as current is worse
than no resume point at all, because the next session acts on it. This is not a hypothetical failure
mode — it is the observed state of this repo's own hand-written `continue.md` (since retired to
`docs/evolution/2026-07-01-refactor-loop.md`), stamped 2026-07-01 and
a dozen commits behind. If fixture 04 passes while 01 fails, the feature is merely incomplete; if 04
fails while 01 passes, the feature is actively dangerous.

**`13` and `14` are the same kind of pair, one paradigm later.** A spine that always reports
`BOARD-AGREES` passes `14` and fails `13`; one that always reports `BOARD-DIVERGES` passes `13` and
fails `14`. Only an actual comparison passes both — which is the whole point of adding the agreeing
case, since a detector silent on agreement is indistinguishable from one that never runs.

**`16` and `17` are a third such pair, and `16` is the counter-intuitive one.** A spine that refuses
every write it did not originate passes `17` and fails `16`; one that writes unconditionally passes `16`
and fails `17`. Only a content comparison passes both. `16` exists because the tempting wrong guard —
*is this snapshot mine?* — reads as the more careful design while breaking the primary path: resuming a
previous session's snapshot is what the file is for, so an authorship check blocks every session after
the first on its first push.

**The `crossed` fixtures pin a state machine, and `tests/test_session_handoff_fixtures.py` now enforces
its two invariants** — `crossed` never increases with depth, and `crossed 0` means pushed since the last
capture. Four fixtures violated one or the other and passed everything, because nothing was checking. `26`
was the worst: it encoded a child outranking its parent — unreachable under the rule — and its prose then
drew the opposite lesson, so a **correct** implementation would have failed its gate. A fixture pinning an
unreachable state is worse than no fixture; it teaches the inverse of the rule.

**`19` pins a distinction both cases render as nothing.** An absent record and an empty stack look
identical on screen, so the cheap implementation satisfies both with one branch and looks correct.

**`22`'s middle frame is the whole fixture.** All three frames are more than a day old and one is marked.
The frame at `crossed 1` has survived a wind-down — which is what carrying a diversion across a boundary
*means* — and must not be marked. An earlier rule compared `open since` against `captured:` and marked
every carried frame, firing on the designed behaviour and the abandoned frame alike. A near-constant
alarm is one people stop reading, which is this board's recurring defect wearing a different hat.

**`24` is the counterpart on the capture side, and its input is deliberately wrong.** The session's own
account of the stack paraphrases one frame and omits another; the file must win. A capture that trusts
the account deletes a frame with no mechanism beyond an omission, on a path that regenerates the whole
file.

**`03` and `05` resolve in opposite directions and must not be satisfied by one rule.** In `03` the
spine is offered derivable state and must refuse it; in `05` the spine has no snapshot and must go and
derive that same class of state. A rule that gets one right by getting the other wrong — "never
derive" or "always record" — is a gate failure. The distinction is *when*: never at capture, always at
read-back.

## Running

Drive each fixture by giving the spine the situation in `manifest.json` and comparing the decision it
reaches against `expected.md`.

| Fixtures | Status against the current `SKILL.md` |
|---|---|
| `01`–`08` | slices 01 and 02 — **must pass** |
| `09`–`10` | slice 03, tested and deliberately **not built** — expected to fail, permanently |
| `11`–`12` | the board projection — **must pass** |
| `13`–`15` | the board divergence check, #24 — **must pass** |
| `16`–`20` | the live stack, #29 slice 01 — **must pass** |
| `21`–`26` | pop and staleness, #29 slice 02 — **must pass** |

A failure in `09`–`10` is genuine RED (the behaviour is unimplemented and will stay so), not BROKEN
(the harness is faulty) — the fixtures are prose inputs with no imports to resolve. Do not "fix" them
by building slice 03; its hypothesis was tested and held.

**Fixtures `01`, `04`, `06`, `07`, `08` and `10` predate the board triple and supply no `board_state`,
so a read-back over them reports `BOARD-UNREADABLE`. That is a pass, not a failure.** It is also what
the spine should do — a fixture that says nothing about a board is a situation with no board in it.
Recorded here because the alternative failure modes are both silent: a driver that scores the extra
outcome as a mismatch retires six working fixtures, and one that ignores the triple on any fixture not
expecting it stops testing the triple at all. `05` and `12` are `RECONSTRUCT`, which reports no triple
by design. **`16`–`23` and `25`–`26` are stack-path fixtures and report no capture or read-back outcome at all** —
no freshness verdict, no board triple. A driver expecting one of those on every fixture scores all nine
as failures. `24` is a WIND-DOWN fixture and reports `CAPTURE` normally.

Run the whole suite whenever `SKILL.md`, either command loader, or `skills/nwave-issue-board/SKILL.md`
changes — the last because slice 02's routing line lives inside its generated block, so this skill's
correctness is partly that skill's. Add `phil:issue-board` to that list for `13`–`15`: they depend on
how a board is read, and on `In Progress` and top-Todo meaning what that skill says they mean.

## Fixture 27 — the prose standard stops at the stack

Added 2026-09-04 (issue #40, `board-prose-standard` slice 03). That slice brought the **why** and the
**next action** under `${CLAUDE_PLUGIN_ROOT}/rules/writing.md`, because this session composes them. **A
frame's `what` and `why` are the human's arguments to `push`** and are reproduced byte-for-byte, so the
standard must not reach them.

`27-stack-frame-not-tightened` supplies a frame whose why is genuinely wordy and would tighten well —
the tempting edit is the forbidden one. It asserts both directions at once: the frames survive verbatim
with `crossed` incremented rather than recomputed, **and** the snapshot's own why and next action are
composed against the standard. A run applying the standard everywhere fails the first half; one applying
it nowhere fails the second.

Its pair is `skills/groom-issues/self-test/44-you-wrote-field-not-tightened/`, which is the same rule at
an elicited field — the discriminator is per field, not per surface.

