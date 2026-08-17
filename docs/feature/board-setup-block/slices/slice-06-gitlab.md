# Slice 06 — GitLab

**Goal:** Produce the same region on a GitLab repo, whose board is `status::` labels rather than a
Projects v2 Status field — same shape, different calls.

**Stories:** S6 (do all of it on GitLab)

## Learning hypothesis

**Disproves forge-neutrality** if the region's *shape* has to differ rather than just its values — if
GitLab needs different sections, different provenance categories, or a different marker convention, then
one command serving both forges is the wrong unit and the honest answer is two.

**Confirms**, if it passes, that `phil:issue-board`'s forge-neutral template survives being generated,
and that #32's defect is closed on both forges rather than one.

## IN scope

- Tier probe (Free vs Premium), and a **Free-shaped block on a Free instance**: no scoped-label
  convention written where scoped labels do not exist, manual `--unlabel` swaps recorded as such.
- Project and board ids; the `status::` label set; the docs root in GitLab's `/-/blob/<branch>/` form.
- `glab`'s JSON flag is `-O`; `-F` fails silently.
- Self-hosted instances: the host from the remote, and the certificate caveat `phil:issue-board`
  records.
- Projects v2 workflows recorded as **not applicable on this forge**, never as *none enabled*.

## OUT of scope

- GitLab epics, child work items, `rolledUpCountsByType`, and every other Premium/group mechanism. The
  block must be writable on Free.
- Any GitLab-only *content* in the block. If a section only makes sense on one forge, that is a finding
  about the template, which `phil:issue-board` owns.
- Reconciling a repo that has boards on both forges. One remote, one target ([D9]).

## Acceptance criteria

1. The region's shape is identical across forges; only values and the recorded calls differ — verified by
   diffing a GitHub-generated region against a GitLab one with values elided.
2. Tier is probed, and a Free instance produces a Free-shaped block.
3. `-O` is used throughout; no `-F`.
4. Projects-v2-specific facts render as *not applicable on this forge*, never as a benign default (C6).
5. A self-hosted instance unreachable over the network is reported as a connection failure and retried
   before anything is concluded — a single failure is usually the network.

## Dependencies

Slices 01–05. Everything about the shape is settled by then; this slice changes only the calls.

## Effort · reference class

≤1 day. Reference class: `phil:issue-board` itself, which carries both forges' mechanics side by side and
is the source for every call named above.

## Outcome — authored 2026-08-17

| AC | Verdict | Evidence |
|---|---|---|
| 1 | **PARTIAL** | Shape equality is verified **mechanically** — the `template_field` set is byte-identical across forges, asserted by test. The *rendered-region* diff against a real GitLab project was **not** run: `projects/<id>` reads unauthenticated but `projects/<id>/labels` returns 401, and on GitLab the label set is the board. |
| 2 | **PARTIAL** | A Free-shaped block is unit-tested, and real project metadata was read from `gitlab-org/gitlab-runner` (id 250833, `default_branch: main`, `visibility: public`). Tier on a real *Premium* instance was not exercised. |
| 3 | **PASS, and it corrected a wrong rule** | See below. |
| 4 | **PASS** | Projects-v2 facts render *not applicable on this forge*; a test forbids the claims `none enabled`, `no workflows enabled`, `0 enabled` and `empty`. |
| 5 | **PARTIAL** | The retry is unit-tested in both directions — a connectivity failure retries, a 401 does **not**. No real unreachable instance was available. |

### AC3 — the recorded rule was wrong, and this is a fold-back

`phil:issue-board` states a blanket rule: *"glab's JSON flag is `-O`; `-F` fails silently."*
**It holds for exactly one of the three calls this adapter makes.**

| Call | JSON flag | The other flag there |
|---|---|---|
| `glab api` | **none** — prints JSON natively | `-O` is rejected outright |
| `glab repo view` | **`-F` / `--output`** | `-O` does not exist |
| `glab issue list` | **`-O` / `--output`** | `-F` is `--output-format`, taking `details`/`ids`/`urls` |

So on `issue list` the rule is right, on `repo view` it is exactly inverted, and on `api` neither flag
applies. **This is the remembered-constant failure the whole feature exists to prevent, sitting inside
the skill this feature is a companion to** — which is the strongest possible confirmation of #32's
premise, arriving from the least expected direction.

**It surfaced only because a refusal message was improved.** The first `run()` reported
`failed: ERROR`, because `glab` prints a bare `ERROR` banner line before the real message and the code
took the first line of stderr. Once the extraction skipped non-informative lines, the cause appeared
immediately: `Unknown shorthand flag: 'O' in -O`. **A refusal whose reason is uninformative hides the
defect that caused it.**

### The defect the real run produced

`column-families` rendered `{"labels": [], "count": 0}` when the labels endpoint returned 401 — and on
GitLab the `status::` label set *is* the board, so that states **the project has no columns**. A reader
would conclude the board does not exist.

Fixed with a third provenance value, `unread`, which `render-block.py` refuses to write inside the
markers at all. This is C6 exactly: an absent mechanism is not an empty one, and neither is an unread
value. Pinned by two tests and fixture 11.

### Learning hypothesis — CONFIRMED on shape, UNVERIFIED end-to-end

Forge-neutrality holds where it was tested: the region's shape did not have to differ, only its values
and recorded calls, so one command serving both forges remains the right unit. What is **not** closed is
the live diff, and the honest reading is that AC1 is confirmed *structurally* and unconfirmed
*empirically*.

**What it would take:** a GitLab token with `read_api` on any project. `glab auth login`, then re-run
`--host gitlab.com`. Everything else is built.

## The review round — both reviewers, 2026-08-17

`plugin-dev:plugin-validator` returned **FAIL**; `plugin-dev:skill-reviewer` returned **Needs
Improvement**. Between them they found one systematic defect with eleven instances and three
criticals, and every one was real. This section records them because the pattern generalises past
this feature.

### The systematic defect: new prose without retiring what it invalidated

Slices 03–06 added their rules and **left the slice-deferral prose in place**, so the skill carried two
mutually exclusive accounts of itself — and the stale one sat in the places a model treats as binding:

- Three entries in *What this skill must never do* forbade shipped behaviour outright — *"write a
  half-probed value"*, *"rewrite an existing region"*, *"claim a re-run is safe"*. **Slices 04 and 05
  were switched off by their own skill.** A prohibition list is the section a model actually obeys, so
  a stale entry there is not cosmetic.
- *The flow* — the operative procedure — still had seven steps for four slices, reaching neither
  ELICIT nor REFRESH, and instructed the model to report *"the declared and assumed totals are
  necessarily zero"* on a run that had just written both.
- `references/outcomes.md`, which `SKILL.md` names as the authority to read *before* changing an
  outcome, was entirely slice-02 era: `REGION-PRESENT` documented as live, three outcomes and a report
  line missing.
- Fixture 01's `must_not` forbade writing `Done` as `assumed` and asking any question beyond the forge
  target. **A correct current run violates it twice** — the fixture had come to fail a correct
  implementation, which is worse than no fixture.

**The rule this produces:** a slice that supersedes a deferral must delete the deferral in the same
commit. Adding the new rule is the easy half, and doing only that leaves the older, more specific,
absolutely-phrased version winning.

### Critical 1 — the GitLab flow could not render at all

`gitlab_facts` emitted value shapes `render-block.py` did not accept: `KeyError 'number'`,
`KeyError 'options'`, `TypeError` on `builtin-workflows`. **A headline feature of the release was
entirely non-functional.**

The cause is a seam: `test_gitlab_probe.py` called `gitlab_facts` eight times and never passed the
result to the renderer, while `test_render_block.py` used only GitHub-shaped facts. **Both halves
green, the join untested.** Fixed by dispatching on value shape rather than forge, and by adding six
end-to-end tests that pipe a GitLab probe through the renderer.

### Critical 2 — the fix for the last critical was never called

`classify_file` was added at 0.57.0 to stop `FileNotFoundError` escaping. Its docstring explains why.
**Its only caller in the repo was its own unit test.** `main()` never invoked it, so the CLI stayed
broken while the suite went green — and the create-an-absent-file path the skill promises was doubly
unreachable, since `--place` also demanded a sha an absent file can never supply.

`CLAUDE.md` names this exact defect — *"the function was written and never called, which is this
board's recurring defect reproduced inside the fix for it"* — and prescribes the remedy: **test that a
new check fails on the input that motivated it.** A unit test asserting `classify_file` returns a dict
does not do that. `tests/test_cli_refusals.py` now runs the scripts *as scripts*, and covers six more
unhandled-exception paths found alongside.

### Critical 3 — the refuted rule shipped as a probed fact

`probe-board.py` carried, as the `note` on `forge-and-repo`, verbatim the blanket flag rule this very
slice refuted — attached to a fact whose own query uses `-F`. It would have propagated into **every
GitLab consumer's `CLAUDE.md`, labelled `probed`.**

The standard had been folded into `issue-board/SKILL.md` and into `gitlab_calls`' docstring, and missed
in the one place that reaches users. **A remembered constant written down as a probed fact, by the
feature built to prevent exactly that** — the third time this feature has caught itself, and the first
where the artefact would have shipped.

### Four more, each a wrong claim rather than a missing feature

- **`render_region` rendered a refused probe** as a well-formed, `probed`-labelled, zero-fact region
  with exit 0, which then passed the marker checks and reached disk. Fixture 02 forbids exactly that
  and was enforced only by model discipline — in the one place the design deliberately moved off it.
- **An `assumed` *fact* was silently dropped**, because only `half_probed` entries produced assumed
  lines. Flagged by the reviewer as latent; making GitLab's `tier` honest made it live, and **`Tier`
  vanished from the GitLab block**, taking a template field and part of KPI-1 with it silently.
- **The `--forge`/`--host` mismatch refusal was promised in help text and never implemented**, so a
  mismatch probed the wrong forge and reported `status: ok`.
- **`labels ... else []`** minted the one value fixture 11 bans, in the same function whose docstring
  bans it.

### And two claims in the compensating-control paragraph were false

The paragraph in `commands/board-setup.md` that carries the intent `mutates: true` cannot express —
**caught wrong for the second consecutive release.** It claimed a byte-identity check on every probed
write when `--refresh` had none, and claimed all three scripts use list-argv `subprocess` when two make
no call at all. Fixed by extending the check to `--refresh` (so the claim is true rather than
"structurally safe") and by narrowing the second sentence to the one script it describes.

**That paragraph is the single most drift-prone thing in this feature**, because it is prose asserting
a property of code and nothing validates it. It now says so about itself, and names the rule: when the
script set or its write surface changes, this list changes in the same commit.

## Note on ordering

Last by design, and the reason is recorded because "later slice" and "out of scope" become
indistinguishable once a feature ships: GitLab is **in** the feature ([D10]). It is widest in surface and
narrowest in learning — by the time it runs, nothing about the design is still in question.

## Taste tests

| Test | Result |
|---|---|
| Ships 4+ new components? | No — one probe adapter |
| Depends on a new abstraction? | Reuses everything; adds no new one |
| Disproves a pre-commitment? | Yes — forge-neutrality of the region's shape |
| Synthetic data? | No — a real GitLab project |
| Identical to another slice but for scale? | No — same shape, different forge, which is the point |
