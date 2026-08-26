# Slice 03 — Every asker conforms, and a script says so

**Goal:** Reference the fragment from all remaining ask sites, and make a command that grants
`AskUserQuestion` without the reference fail the build.

**Stories:** S4 (trust that every asker conforms, without reading nineteen files)
**WS strategy:** n/a — slice 01 holds the skeleton

## Learning hypothesis

**Disproves [D10] — enforcement by script** — if conformance turns out not to be mechanically checkable.
The check can verify that a *reference exists*; it cannot verify that an ask *conforms*. If the reachable
check is so shallow that a referencing skill can still emit a bare option list and pass, then [D10]
delivers a green run that means nothing, and the honest outcome is to say so rather than to ship a check
that certifies the wrong property. This is the exact failure `CLAUDE.md` records for
`check-readonly-commands.py`: *"absence of `Write` never meant read-only"* — a shallow signal standing in
for the real one.

**Confirms**, if it passes, that the standard is in force inside a command as a fact rather than a hope —
the half of the feature that is enforceable at all.

## IN scope

- References added at the remaining **7** ask sites across 5 skills: `refactor-tests` (2),
  `redesign-tests` (2), `work`, `refactor`, `edd`.
- `scripts/check-decision-request-reference.py` — fails on a command granting `AskUserQuestion` whose
  loaded skill carries no reference to the fragment.
- Wiring into `scripts/check-invariants.py`, reporting **only** failures per *Repo invariants run
  themselves*.
- An explicit exemption mechanism, and it must be explicit — a command that legitimately needs no
  reference declares it. Silence is never conformance.
- A stated account, in the script's own header, of what the check verifies and what it does **not**: it
  verifies a reference resolves, never that an ask conforms.

## OUT of scope

- Any attempt to check ask *content* mechanically. The check is a reference check and says so; the content
  is pinned by slice 02's fixtures and by review. Conflating them is the [D10] failure this slice exists to
  test for.
- The conversational half — slice 04. A command grant is the only signal this check can read, so ordinary
  conversation is structurally invisible to it, by construction rather than by omission.
- Rewording the 7 sites' existing prompts. The reference lands; the rewording follows from it and is
  reviewed per-site, not batched blind.

## Acceptance criteria

- **AC1** The check fails on a command granting `AskUserQuestion` whose skill carries no reference.
- **AC2** **The check is proven to fail on the input that motivated it before any green run is trusted.**
  Non-negotiable: `CLAUDE.md` records that the first `check-readonly-commands.py` was written and never
  called, and silently passed — this board's recurring defect reproduced inside the fix for it.
- **AC3** All 8 skill ask sites reference the fragment; all 13 command grants are covered by a referencing
  skill or an explicit exemption.
- **AC4** The check reports only failures and is silent on a clean tree.
- **AC5** An exemption is expressible, explicit, and carries a reason in the file that claims it.
- **AC6** The script's header states the gap between what it checks and what the standard requires, in as
  many words. A check whose limits are undocumented is the shallow-signal failure again.
- **AC7** No `Bash(...)` grant introduced by this slice contains a path or a variable — `allowed-tools`
  does not interpolate `${CLAUDE_PLUGIN_ROOT}`, and such a grant matches nothing while looking narrow.

## Dependencies

**Slice 01** (the fragment must exist to reference) and **slice 02** (the fixtures are what the reference
is worth referencing — a reference to an untested standard propagates confidence, not conformance).

## Effort · reference class

**≤1 day.** Reference class: `scripts/check-readonly-commands.py` (one script, one invariant wiring, one
day — including the day lost to the uncalled function, which AC2 exists to prevent repeating).

## Pre-slice SPIKE

**Not needed.** The mechanism is a grep over frontmatter and skill bodies; the uncertainty is about what
the check *means*, not whether it can be written, and AC6 answers that in prose rather than by probe.

---

## Result — 2026-08-26

**Shipped.** All ten skills wired, `scripts/check-decision-request-reference.py` enforcing it in **two**
directions, wired into `check-invariants.py`, with ten tests and every failure mode proven red before the
green run was trusted.

### [D10] holds, and the honest reason is narrower than the AC implied

The hypothesis was that [D10] fails *"if the reachable check is so shallow that a referencing skill can
still emit a bare option list and pass"*. **A referencing skill can still do exactly that** — the check
proves a reference resolves and nothing more. So the disproof condition is literally met.

[D10] survives anyway, and not by redefining it: the value of a shallow signal depends on whether its
shallowness is *stated*. `CLAUDE.md` records the failure this would otherwise be — *"absence of `Write`
never meant read-only"* — a green check standing in for the property nobody measured. This check's header
says three times, in as many words, that it does not measure conformance; two tests assert those sentences
are present, so deleting them turns the suite red. That is the difference between a shallow check and a
misleading one, and it is the whole of AC6.

### The survey found a live defect the brief did not anticipate, and it changed the design

The brief specified one direction: a command granting the tool whose skill carries no reference. The
survey turned up the opposite shape, and it was a real bug:

**`skills/refactor/SKILL.md` called `AskUserQuestion` and `commands/refactor.md` granted no such tool.**
The skill instructs *"No test runner detected. Refactoring without tests is risky. Continue anyway?"* —
and the call could only ever be refused. The failure is silent because a refused tool looks like a
skipped step, so the loop would proceed to refactor without a runner and without asking.

This is the feature's own **E6 inverted**. There, the one skill that wrote the plain-language rule down
was the one command that could not ask a structured question. Here, the one skill whose ask is a safety
gate was the one command that could not fire it. Same defect class, opposite direction, found because the
check was being written rather than assumed.

So the check runs both directions, `commands/refactor.md` now grants the tool, and
`test_direction_b_an_ask_site_with_no_grant` names the instance — because a later reader will see
direction B as symmetry for its own sake and delete it.

### AC-by-AC

| AC | State |
|---|---|
| AC1 | ✅ fails on a grant whose skill carries no reference |
| AC2 | ✅ **five** inputs proven before any green run: no reference, reference by bare path, ask with no grant, exemption without a reason, and a valid exemption proven to *pass* |
| AC3 | ✅ 14 granting commands → 10 distinct skills → 10 references; all 8 ask sites covered |
| AC4 | ✅ silent and exit 0 on a clean tree |
| AC5 | ✅ `<!-- decision-request-exempt: <reason> -->`, valid in a command or a skill, reason of four words or more required |
| AC6 | ✅ stated in the header and asserted by two tests |
| AC7 | ✅ no `Bash(...)` grant introduced. **Its stated reason is stale** — `allowed-tools` *does* interpolate `${CLAUDE_PLUGIN_ROOT}`, measured 2026-08-21 against 2.1.239, and `CLAUDE.md` records the rule as kept on three different reasons. The AC's requirement stands; its rationale does not |

### Scope taken beyond the brief, declared

- **Direction B**, above. The brief's OUT-of-scope names ask *content*, not the reverse direction, so this
  is an addition rather than a violation — but it is an addition, and it is why the script is twice the
  size the reference class predicted.
- **One grant widened.** `commands/refactor.md` gained `AskUserQuestion`. The alternative was deleting a
  legitimate safety ask from the skill, which trades a silent defect for a real loss.
- **A reference-form check inside the script.** `tests/test_shared_fragment_registry.py` already asserts
  the form, but it is a pytest and this is a build check; a bare path in a skill body is inert at runtime,
  so the enforcement belongs where the enforcement is.
- **The fragment's *Reach* section rewritten.** It said propagation was incomplete, which slice 03 made
  false. An understated reach is as wrong as an overstated one — and the correction had to preserve the
  shallowness claim, which is now asserted.

### Exemptions: the mechanism exists and nothing uses it

Zero files claim an exemption, and that is a finding rather than an oversight. All ten skills genuinely
put questions to the human — four of them in prose without naming the tool: `adversarial-review` asks what
to review when the scope is ambiguous, `session-handoff` asks for a diversion's reason and for an unknown
owner, `board-setup` and `rank-issues` elicit what no forge can answer. Each was checked before a
reference was added rather than after, because an exemption granted wrongly is *"silence is never
conformance"* in a politer register.

The mechanism ships anyway: a check with no expressible exemption gets satisfied by a fake reference
instead.

### Test-first, and the one place it held

Genuinely test-first for the check: `tests/test_check_decision_request_reference.py` was driven by
building each failing tree before the script satisfied it, and direction B's test was written from the
real `refactor` defect while that defect was still live in the tree. The nine reference additions were
not test-first — a reference is content, and the check that reads them is what has the test.

### Dogfood scope

Nothing exercised through an installed `/phil:*` command; the plugin cache is behind this tree. What ran
is the script against this repo, the ten fixture trees, and the invariant runner. **`check-plugin-skew.py`
now reports the content gap itself**, which it could not do before this session.
