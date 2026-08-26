# Slice 04 — The reach outside a command

**Goal:** Address the case the enforceable half cannot reach — a decision request in ordinary
conversation — and declare plainly what mechanism covers it and how well.

**Stories:** S5 (know where the standard cannot reach)
**WS strategy:** n/a — slice 01 holds the skeleton

## Learning hypothesis

**Disproves [D11] — that the conversational half is unenforceable** — if it turns out to be reachable
after all. That would be good news and is recorded as a hypothesis precisely so it gets tested rather than
assumed: [D11] was reasoned from two measurements ([D6] on `rules/`, E2/E6 on per-command prose) and a
third mechanism may exist that neither ruled out. A `SessionStart` hook, a skill description that fires
reliably, or something in the harness that nobody here has checked.

**Confirms**, if it holds, that the standard covers the command case deterministically and the
conversational case probabilistically — and that the difference is stated in the artifact rather than
discovered by a user whose question arrived as a bare list anyway.

**The honest failure mode of this slice is silence.** Shipping a probabilistic mechanism and describing it
as coverage is worse than shipping nothing, because it converts a known gap into an invisible one.

## IN scope

- A section in `skills/shared/decision-request.md` stating that outside a `/phil:*` command no
  deterministic trigger exists, naming what is used instead and how it fails.
- Whichever mechanism is chosen — the two candidates, not exclusive:
  - a **skill description** that triggers on the moment: reaches ordinary conversation, ships to
    consumers, fires unreliably;
  - a line in **`CLAUDE.md`**: always loaded, fires reliably, repo-local, does **not** ship to consumers.
- The choice recorded with its cost, and the split stated if both are used.
- KPI-6 restated in the fragment as unmeasurable by construction, so a later reader does not mistake its
  absence for an oversight.

## OUT of scope

- Putting the standard in `rules/`. Closed by [D6] on measurement: a globbed rule fires on file type
  (`ux.md` is the worked example), and a pathless rule is a manual-reference rule that never auto-loads
  (`rules/llm-inference.md` states this in as many words, naming `definitions.md` as precedent). A future
  reader wanting to reopen it should read E5 and E7 first.
- Any claim of coverage the chosen mechanism cannot deliver.
- Fabricating a number for KPI-6.

## Acceptance criteria

- **AC1** The fragment states plainly that the conversational case has no deterministic trigger.
- **AC2** The chosen mechanism is named, with its failure mode, in the fragment itself — not only in this
  brief.
- **AC3** `CLAUDE.md`'s repo-local reach and its non-shipping to consumers are stated explicitly wherever
  that route is used. A standard that silently depends on a file consumers never receive would report
  coverage it does not have.
- **AC4** No coverage claim exceeds the mechanism ([D11]).
- **AC5** If a deterministic mechanism **is** found, [D11] is amended in the feature delta and this slice's
  hypothesis is recorded as disproved — a reversal recorded as a reversal, per this repo's standing habit
  of naming which decision moved.
- **AC6** KPI-6 is restated as unmeasurable by construction, with the reason.

## Dependencies

**Slice 03** — the mechanism chosen here should be informed by what enforcement actually caught, and
choosing before that is measured would be the speculative design the repo's own principles forbid.

## Effort · reference class

**≤1 day**, and likely half of one — the deliverable is prose plus one small mechanism. Reference class:
`board-setup-block` slice 04 (a taxonomy and its labels, prose-dominant).

## Pre-slice SPIKE

**Yes — timeboxed to an hour, before the slice.** The one open question is whether a third mechanism
exists that [D6] and [D7] did not rule out. That is a *search*, not a build, and doing it as a spike keeps
a negative result cheap: if nothing is found, [D11] stands unchanged and the slice ships the declaration.

---

## Result — 2026-08-26

**[D11] is disproved.** The slice's hypothesis fired, which the brief called good news and required be
recorded as a reversal rather than absorbed.

### The SPIKE found the third mechanism, and it was already in this repo

The brief timeboxed an hour to search for a mechanism [D6] and [D7] had not ruled out. Both of their
measurements still hold — a globbed rule fires on file type, a pathless rule never auto-loads — and
neither has anything to say about a **tool-call hook**.

`plugin-dev:hook-development` confirms `PreToolUse` receives `tool_name` and `tool_input` and may return
`permissionDecision: deny` with a reason the model reads; `matcher` is a regex over the tool name. And
this plugin **already ships one** — `hooks/hooks.json`, matcher `Edit|Write`, the refactor-loop
write-block — so the mechanism was proven in-repo before it was proposed, which is why the SPIKE closed
in well under its hour.

The argument that stopped anyone looking is in slice 02's own evidence: E11 showed placement cannot be
found in live output, because the framing is prose and nothing marks where it begins. True, and it does
not generalise. **A tool call is not prose. It is structured data**, and the question text, every option
label and every option description arrive inside it.

### What is now enforced, and where

| Clause | Inside a command | Ordinary conversation | Consumers' projects |
|---|---|---|---|
| per-question ceiling | ✅ hook | ✅ hook | ✅ hook, unconditional |
| plain language (3 portable classes) | ✅ hook | ✅ hook | ⚙️ opt-in |
| every option names its cost | ❌ semantic | ❌ | ❌ |
| placement / framing present | ❌ not in the payload | ❌ | ❌ |
| the reference is loaded at all | ✅ build check | — | ✅ ships |

Two clauses are unreachable for structural reasons rather than missing effort, and both the hook's header
and the fragment say so — a partial enforcer that hides what it misses reads as a complete one.

### The measurement that changed the design after the decision was made

Put to the user with four options; **"refuse on both reachable rules"** was chosen. Then measured before
shipping, over 73 real requests in this repo's history:

- **Denying on both, everywhere: 59 of 73 refused — 81%.**
- Inspected rather than assumed: **41 of the 42 distinct matches are genuine** filenames and card
  numbers. The check is not misfiring; the corpus predates the standard. The one false match was a URL,
  now excluded — a link a reader can open is not an identifier from a system they may not share.

81% is the right answer here and the wrong one elsewhere, and the difference is what the rule is about.
This standard forbids *identifiers from a system the reader may not share*. In this repository a filename
is exactly that. In an ordinary project, *"edit `config.json` or `settings.yaml`?"* is the clearest way to
name a decision, and denying it would be this plugin refusing a stranger's work for a local reason.

**So the two halves ship differently, and this is a declared deviation from the answer given:**

- the **ceiling** is unconditional — arithmetic, content-neutral, nothing it can misjudge;
- the **wording rule** is enforced where a project carries `decision-request: strict` in its `CLAUDE.md`.
  This repo does, which is where the complaint originated.

Measured at that setting: **81% here, 10% in a project that never opted in** — and the 10% is length
alone, which no project wants either way. One line in `CLAUDE.md` flips a consumer to strict; deleting it
here flips this repo out, and a test asserts the marker is present so the removal cannot be silent.

### AC-by-AC

| AC | State |
|---|---|
| AC1 | ✅ **inverted, honestly.** The fragment no longer says the conversational case has no deterministic trigger, because it now has one. It says which clauses that trigger reaches and which it structurally cannot |
| AC2 | ✅ the hook is named in the fragment with its failure mode and its opt-in split |
| AC3 | ✅ `CLAUDE.md`'s repo-local reach is stated where the marker lives — and the mechanism deliberately does **not** depend on `CLAUDE.md` shipping: the hook ships, the marker is per-project |
| AC4 | ✅ nothing claims what the mechanism cannot deliver; the two unreachable clauses are named in three places |
| AC5 | ✅ [D11] amended as **DISPROVED** in the feature delta, with what survives of it stated |
| AC6 | ✅ KPI-6 amended from "not measurable by construction" to partly measurable, with the structural reason the remainder stays unmeasurable |

### The correction this slice forced on slice 02's own work

Slice 02 shipped, hours earlier, the sentence *"No check reads a live ask, and none can."* A reviewer had
already softened it once from an impossibility claim to a conditional one, on exactly the grounds that the
evidence did not support impossibility. **It was still wrong, and this slice refuted it the same day.**

Corrected in place rather than deleted, with the reason it was wrong — a decision reversed silently is one
the next reader re-derives from the same premise. `test_the_fragment_does_not_overclaim_its_reach` now
asserts the reversal is visible.

One further defect fell out of fixing it: the test guarded with `"and none can" not in body`, and the
correction *quotes* the refuted claim — so the guard fired on the quotation. That is the negative-substring
weakness the reviewer named in slice 02, appearing again. The correction is worded to avoid reproducing the
string, and the test says why.

### Test-first, and where it held

Test-first for the hook: the failure trees were written before the script satisfied them, and the
fail-open cases were driven from nine malformed payloads before any denial logic existed. **33 tests, and
more of them assert the hook stays out of the way than assert it fires** — the weighting a shipped denial
deserves. The opt-in split's tests were written after its measurement, which is the honest order for a
design that a measurement caused.

One test defect found and fixed in the same pass: the first version let `cwd` default to the ambient
working directory, so it passed only because pytest happens to run from the one repository that has opted
in. Every case now states its project explicitly.

### Dogfood scope

Nothing exercised through an installed `/phil:*` command — the cache is behind this tree, and
`check-plugin-skew.py` now reports that itself. **The hook has not fired in a live session**, because it
ships in the plugin and this tree's edits are not installed. What ran: 33 tests, and the hook executed
over all 73 recorded requests under both settings. The decision that authorised it was posed under the
standard — context above a marker, 178-word framing, zero forbidden tokens, four options each naming its
cost.
