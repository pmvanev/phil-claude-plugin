# Expected — 40 (two operations, one word)

**Pins:** `single-issue-per-feature` slice 05's split divergence, and `REFUSE-RESLICE`.

**Expected:** `REFUSE-RESLICE`. Nothing is created, nothing is closed, no file is touched:

```
Not splitting #26. "Split" means two different things here and neither is what you asked for
as stated.

Splitting a STORY creates cards — that operation exists and I can do it.
Splitting a FEATURE means re-slicing its roadmap: editing
docs/feature/single-issue-per-feature/slices/, which changes no cards at all and is not
this command's to do.

If the roster is unwieldy, the slices are the thing to change, not the cards.
```

**Why the request is reasonable and still refused.** Six roster rows on one card *is* a lot, and under the
retired rules the answer would have been six cards. The user is applying the old rule correctly. What has
changed is that the roster is a projection of `docs/feature/<id>/slices/` — so making it shorter means
changing the slices, and creating cards would put the board back into the shape consolidation exists to undo.

**This is the one refusal that needs its own outcome.** `DECLINE-NO-TRACE` is wrong — the user did not
decline, they asked. `REFUSE-UNVERIFIED` is wrong — nothing is unverified. Reporting either would misattribute
the stop, and reporting `APPLY-SPLIT` while doing nothing would be worse. That gap is why the outcome was
added.

**Gate failures:**

- Creating cards for the roster rows. The paradigm, inverted, on request.
- Editing `docs/feature/.../slices/`. This command holds no `Write`, and re-slicing is not grooming.
- Reporting `DECLINE-NO-TRACE` or `REFUSE-UNVERIFIED`.
- Refusing without naming which operation would achieve what was asked. A bare refusal hands back no route.
- Reporting the card as oversized to justify the refusal, or as clean to dismiss the request. Neither was
  asked and the first is forbidden by the demonstrability rule.
