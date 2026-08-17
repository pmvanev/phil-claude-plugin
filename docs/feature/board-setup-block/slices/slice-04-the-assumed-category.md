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
