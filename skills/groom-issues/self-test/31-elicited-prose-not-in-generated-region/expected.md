# Expected outcome — fixture 31 (the scribe has nowhere legitimate to write)

**Pins:** `REFUSE-GENERATED` on `/phil:groom-ask`, added 2026-08-14.

**Expected decision:** `ASK-CONTENT` then `REFUSE-GENERATED`. The questions are asked — the findings
are real — and then the write is refused because the body offers no space the generator does not own:

```
#31 — asked, answered, NOT written.

  The whole body is a generated region (nwave:status, published by
  phil:nwave-issue-board). Elicited prose written inside it is overwritten at the
  next refresh, and disagrees with its source until then.

  Your answers, kept so they are not lost:
    Purpose    "the retry backoff is hard-coded and cannot be tuned per endpoint"
    Done when  "each endpoint's backoff comes from config, with a test that a
                changed value takes effect"

  Rules 1 and 2 remain open on this card. The finding returns next run.
```

**Why this is not the same fixture as `15`.** `15` refuses a *mechanical* fix inside the markers —
right content, wrong owner, and the correct content already exists in the generator's source. Here the
content exists **nowhere**: a purpose is not derivable from any artifact, which is the whole premise of
elicitation. So `15`'s remedy — fix it at the generator — is unavailable, and the honest outcome is a
refusal that hands the answers back rather than a redirection.

**Why the case is ordinary rather than contrived.** A generated block is published from the artifacts
and states position, never intent. A card can therefore be fully projected and still fail rules 1 and 2.
The paradigm change proposed in `docs/feature/single-issue-per-feature/` makes this the common shape
rather than the rare one, because every feature card will carry a block — but the case is reachable
today, on any slice card whose body was never written by hand.

**Gate failures:**

- Writing the answers inside the markers. Overwritten at the next refresh, and wrong in the meantime.
- Appending them immediately after `<!-- nwave:status:end -->` to get the content in. Forbidden in the
  same words as `/phil:groom-fix`'s version, and for the same reason: the placement is a workaround for
  a refusal, not a resolution of it.
- Reporting `DECLINE-NO-TRACE`. The user did not decline — they answered. Recording a refusal as a
  decline blames the wrong party and loses the answers.
- Discarding the answers. The same defect `27` pins for a moved body, arriving by a different route:
  a refused write must not also cost the user what they just dictated.
- Editing the generator's source to add a purpose. That is not this command's, and a purpose is not a
  thing the generator has.
