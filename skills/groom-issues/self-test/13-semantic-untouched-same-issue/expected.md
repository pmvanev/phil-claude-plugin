# Expected outcome — fixture 13 (two columns, one card)

#33 holds a relative link and a missing done-when. Scope is everything.

**Expected decision:** both, additively — `APPLY-MECHANICAL` on the link, `LEAVE-SEMANTIC` on the
done-when:

```
#33 — rewrote rules/testing.md as <absolute URL>. No judgement: the form 404s either way,
      target confirmed on origin/main.
#33 — states no way to tell when it is done (rule 2). Needs your decision; not touched.
```

**The column is a property of the defect, not of the card.** An issue with one of each gets one of
each treatment, in the same pass, and the report says so on both lines. Nothing about a semantic defect
contaminates the mechanical one sitting beside it.

**Gate failures:**

- Skipping #33 entirely because it also has a semantic defect. That makes the semantic column
  contagious, and on a real board almost every card would catch it — the mechanical column would empty
  itself through proximity rather than through measurement.
- Drafting acceptance criteria while already editing the body. "While I am here" is how a slice that
  promised to fix only the underivable-free defects starts inventing content. Rule 2 defects are the
  user's to answer; the brief puts them explicitly out of scope.
- Reporting the semantic defect in a way that implies it was handled. `LEAVE-SEMANTIC` is an outcome
  that must appear in the report, not an omission.
- Asking about the semantic defect *before* applying the mechanical one, so the mechanical fix waits on
  an unrelated answer. The two are independent; blocking one on the other reintroduces the
  conversational gate this slice exists to remove.
