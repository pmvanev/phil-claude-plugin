# Slice 04 — The assumed category

**Goal:** Write the half-probed values as **assumptions that say so**, stating what is not knowable and
why, with an offer to confirm — so a reader can tell a fact from a guess without leaving the file.

**Stories:** S4 (tell an assumption from a fact in the written block)

## Learning hypothesis

**Disproves [D5]'s three-category taxonomy** if no reader can reliably tell an assumption from a fact in
the written block. If the labels do not survive contact with a reader, the third category is a
distinction the author can see and the user cannot, and the honest fallback is S6-style invariant advice
that names no specific value.

**Confirms**, if it passes, that the taxonomy #32 got two-thirds right is now complete and legible.

## IN scope

- The worked case: `Auto-close issue: enabled` is **probed**; the configured trigger statuses are not
  exposed by `ProjectV2Workflow`, so `Done` is written as an **assumption**.
- An assumption line states what is not knowable **and why** — not merely that it is assumed.
- The confirm offer, reusing slice 03's question machinery. A confirmed assumption becomes a
  **declaration outside the markers**, attributed to Robin — it does not become a probed fact, because
  nothing probed it.
- Every line inside the markers carries exactly one of `probed` / `assumed`. A line carrying neither
  fails the slice.
- The closing report totals the three categories separately.
- KPI-2 measured: a reader who did not run the command classifies every line correctly, under 60s.

## OUT of scope

- Enumerating every half-probed value in the API. The workflow trigger is the worked case; others are
  handled by the same rule when found.
- Reading the trigger statuses out of the GitHub UI or any unofficial endpoint. If the API does not
  expose it, it is assumed — inventing a probe for it is how an assumption gets laundered into a fact.
- Changing what `phil:issue-board` says the block should contain (#32: content is out of scope).

## Acceptance criteria

1. Every line inside the markers carries exactly one provenance label.
2. An assumption names what is not knowable and why, in the line itself.
3. Confirming an assumption moves it **outside** the markers as a declaration; it never becomes `probed`.
4. Declining to confirm leaves the assumption in place, still labelled — a declined confirmation is not
   an escalation to fact.
5. KPI-2: 100% of lines correctly classified by a fresh reader in under 60 seconds.

## Outcome — authored 2026-08-17

| AC | Verdict | Evidence |
|---|---|---|
| 1 | **PASS** | `test_every_fact_line_carries_exactly_one_provenance`. The AC's phrase *"every line"* was made mechanical rather than reinterpreted per run: **a fact line is a bullet before the `**Queries**` header**; everything after is apparatus and carries no provenance by design. Recorded because "every line" is the kind of phrase a later reader holds code to. |
| 2 | **PASS** | Each assumed line renders `not knowable: <what> — <why>`, naming `ProjectV2Workflow`'s field list. Tested. |
| 3 | **PASS by construction** | Confirming moves a family into the *declared* region via `--declare`; there is no code path from a half-probed value to a `probed` one. |
| 4 | **PASS** | Declining leaves the assumption in the probed region, still labelled `assumed`. No escalation exists to perform. |
| 5 | **PASS — KPI-2 met** | Measured on a real fresh reader who had not generated the block: both `assumed` lines identified, boundary judged correctly drawn, well under 60s. |

### Learning hypothesis — CONFIRMED

[D5]'s three-category taxonomy **survives contact with a reader.** The distinction is not one only the
author can see: a reader who had not run the command picked out the two guesses and confirmed the
boundary was drawn in the right place.

That matters because the honest fallback, had it failed, was S6-style invariant advice naming no
specific value — a strictly worse product. The taxonomy #32 got two-thirds right is now complete and
legible rather than merely complete.

### The line that carries the whole slice

```
- `Auto-close issue` is enabled on this project, and **`Done` is assumed to fire it** *(assumed · Q5)*
  not knowable: which Status option fires it — `ProjectV2Workflow` exposes createdAt, enabled,
  fullDatabaseId, id, name, number, project, updatedAt — and no field for the configured trigger statuses
```

Compare what this repo's hand-written prose said for six weeks: *"Auto-close on Done is ENABLED."* One
confident sentence spanning a fact and a guess, with nothing marking the seam.

### A third provenance value appeared, and it is not written at all

`unread` — a value the forge would not return. Found on GitLab, where `projects/<id>` reads
unauthenticated and `projects/<id>/labels` returns 401. It is neither a fact nor a guess but the
absence of both, so `render-block.py` **refuses to write it inside the markers**; it belongs in the
report, where the reader can see the read failed. Writing it as either category would launder a failed
read into content.

## Dependencies

Slices 01 (probe) and 03 (the question machinery the confirm offer reuses).

## Effort · reference class

≤1 day. Reference class: `adversarial-review`'s honesty label — `sound-gate` versus `draft-signal`,
mechanically derived and never dressed up. Same discipline, different register: there it separates a
verdict backed by an oracle from one that is not; here it separates a value the forge answered from one
nobody did.

## Taste tests

| Test | Result |
|---|---|
| Ships 4+ new components? | No — a label, a confirm offer, a report total |
| Depends on a new abstraction? | Reuses 01 and 03 |
| Disproves a pre-commitment? | Yes — the taxonomy this DISCUSS added to the card |
| Synthetic data? | No — the real `Auto-close issue` workflow on the real board |
| Identical to another slice but for scale? | No — 03 asks what nobody knows; this labels what is half known |
