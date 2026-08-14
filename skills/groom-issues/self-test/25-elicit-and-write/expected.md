# Expected outcome — fixture 25 (provenance, per field)

**Pins:** slice-04 AC1, AC2 and AC2b as amended 2026-08-14 (scribe → editor).

> **Rewritten 2026-08-14.** This fixture previously pinned the opposite rule — that the body is composed
> from the answers *verbatim* and that polishing into house style is a gate failure. See the foot of this
> file for what changed and why the replacement is stricter rather than looser.

**Expected decision:** `ASK-CONTENT` then `WRITE-ELICITED`. The card is presented first, suggestions are
offered marked as the session's, and the write reports provenance for both fields:

```
#47 — presented, asked, answered, written.

  Purpose      [you accepted my suggestion]
    "retries fire on 4xx responses and burn the rate limit"

  Done when    [I rephrased your answer]
    you said:  "when 4xx stops retrying at all and theres a test proving 5xx still does"
    written:   "4xx responses are no longer retried, and a test proves 5xx still is."

  Nothing else was added. The title was not used as a source, and no context was taken
  from sibling cards or the repository.
```

**Why the labels carry the guarantee.** "Wrote the body for #47" cannot be contradicted by a reader. The
block above can: the user knows which suggestion they accepted and what they typed, so a third sentence
appearing from nowhere, or a "rephrasing" that changed the meaning, is visible on the page. **This is the
same job the verbatim rule used to do, extended to cover the two paths verbatim never reached** — an
accepted suggestion, and a sanctioned rewrite.

**Gate failures:**

- **Any field without a provenance label.** The body may read perfectly; the outcome still fails.
- Claiming `I rephrased your answer` without printing the answer beside the written form. An
  uninspectable rewrite is an assertion.
- Labelling the accepted suggestion `you wrote`. The user chose it; the session composed it, and the
  distinction is the whole mechanism.
- Rephrasing so far that the meaning moves — "4xx stops retrying" becoming "non-retryable statuses are
  skipped" imports a concept the user never used. The house voice is a tidying licence, not a modelling one.
- Adding a section nobody asked for: a `## Context`, a `## Chain`, acceptance criteria inferred from the
  done-condition.
- Writing before the card was presented, or before both fields were resolved.
- Offering the suggestions as though they were the user's own options rather than the session's.

## Changed Assumptions

**Original, verbatim** from this fixture's first version:

> **Expected decision:** `ASK-CONTENT` then `WRITE-ELICITED`. Both questions asked before anything is
> written; the body composed from the two answers and nothing else

and from its gate failures:

> - Polishing the answers into house style. Tightening "burn the rate limit" into something more formal
>   substitutes the session's voice for the user's, and the user can no longer recognise their own card.

**New assumption.** The session may suggest and may rewrite, provided every field says which it was.

**Why the replacement is stricter.** Verbatim had a hole: a session that offered a draft and received a nod
satisfied it completely, while producing a body the user never composed. Nothing in the old fixture set
could catch that, because none of them contemplated a suggestion. Per-field provenance closes it, and adds
a failure mode the old rule had no name for — the unlabelled field.
