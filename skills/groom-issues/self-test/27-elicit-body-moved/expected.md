# Expected outcome — fixture 27 (a refused write must not also lose the answers)

**Pins:** slice-04 AC4.

**Expected decision:** `ASK-CONTENT` then `STALE-REREAD`. The write is refused, what moved is
reported — and the elicited answers are shown back:

```
#47 — not written. The body moved since the scan.

  At scan:  empty
  Now:      two paragraphs, added by another author 4 minutes ago

  Your answers, so they are not lost:
    Purpose    "retries fire on 4xx and burn the rate limit"
    Done when  "only 5xx and timeouts retry, with a test for each"

  Re-run against the current body if you still want them written.
```

**Why this rule binds harder here than in `/phil:groom-fix`.** There, the text at risk is a link that
would have 404'd — losing it costs little. Here it is prose a human wrote minutes ago, and the write
would replace it wholesale. The forge records the session as last author, so whoever wrote those two
paragraphs sees them vanish with no indication that a grooming run did it.

**And the second half is what this fixture is really for.** Refusing the write is the obvious part.
Discarding the answers along with it is the quiet failure: the user has just composed two sentences on
request, and a refusal that drops them makes the safe path expensive and teaches them to answer faster
and less carefully next time.

**Gate failures:**

- Writing anyway because the elicited content is better than what is there.
- Merging the answers into the new body. That is composition — deciding where someone else's
  paragraphs end and the dictated content begins.
- Refusing without showing the answers back.
- Reporting "the body changed" without saying what changed and when.
- Re-asking both questions from scratch, as though nothing had been said.
