# phil:session-handoff — Acceptance Self-Test

The **capture + read-back spine** is the software under test. Its bugs are silent: a snapshot that
quietly records derivable state looks like a *fuller* snapshot; a stale resume point presented as
current looks like a *smooth* resume; a session that does the work inline instead of handing it to the
command that owns it looks like a *productive* session. Each failure mode is indistinguishable from
success at a glance, which is why the skill is never changed and eyeballed — it is changed and
regression-tested here.

These fixtures feed the spine known situations and assert each produces the correct **decision
outcome**:

`CAPTURE` · `NO-OP` · `REFUSE-DERIVABLE` · `RESUME-CURRENT` · `RESUME-STALE` · `RECONSTRUCT` ·
`ROUTE` · `ROUTE-LIVE-WINS` · `ASK-OWNER` · `REPORT-CLAIM-CONFLICT`

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
| `09-claim-and-basis/` | a card was claimed for a stated reason | slice-03 AC1, AC2 | the session→card link survives | `CAPTURE` carrying claim + basis |
| `10-competing-claim/` | two snapshots claim one card | slice-03 AC4 | detection without resolution (C6) | `REPORT-CLAIM-CONFLICT` — neither discarded |

## The two sharpest fixtures

**`04` is the one that matters most.** A stale resume point that presents itself as current is worse
than no resume point at all, because the next session acts on it. This is not a hypothetical failure
mode — it is the observed state of this repo's own hand-written `continue.md` (since retired to
`docs/evolution/2026-07-01-refactor-loop.md`), stamped 2026-07-01 and
a dozen commits behind. If fixture 04 passes while 01 fails, the feature is merely incomplete; if 04
fails while 01 passes, the feature is actively dangerous.

**`03` and `05` resolve in opposite directions and must not be satisfied by one rule.** In `03` the
spine is offered derivable state and must refuse it; in `05` the spine has no snapshot and must go and
derive that same class of state. A rule that gets one right by getting the other wrong — "never
derive" or "always record" — is a gate failure. The distinction is *when*: never at capture, always at
read-back.

## Running

Drive each fixture by giving the spine the situation in `manifest.json` and comparing the decision it
reaches against `expected.md`. Fixtures 01-05 cover slice 01 and should pass against the current `SKILL.md`. Fixtures 06-10 cover
slices 02 and 03, which are not built, and are expected to fail — that is genuine RED (the behaviour
is unimplemented), not BROKEN (the harness is faulty), because the fixtures are prose inputs with no
imports to resolve.

Run the whole suite whenever `SKILL.md`, either command loader, or `skills/nwave-issue-board/SKILL.md`
changes — the last because slice 02's routing line lives inside its generated block, so this skill's
correctness is partly that skill's.
