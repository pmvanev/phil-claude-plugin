# Expected outcome — fixture 01 (walking skeleton)

**Expected decision:** `REPORT-DEFECT`. Two findings, each naming the rule and quoting the evidence:

- `#31` — **no purpose stated.** Body is "fix the thing". Rule 1: a title is not a purpose.
- `#34` — **relative file link.** `[the ADR](docs/adr/016.md)`. Rule 3: GitHub emits relative paths
  verbatim, so this resolves against the issue URL and 404s.

Classified: `#34` **mechanical** (one right answer — the absolute URL), `#31` **semantic** (only the
author knows the purpose). Slice 02 will act on the first and never the second.

Summary line first: `7 issues read · 5 clean · 2 with body defects`.

**Gate failures:**

- A finding with no rule cited, or no evidence quoted. That is an opinion, and this skill does not
  report opinions — it is also precisely how a defect table becomes something a user argues with
  rather than acts on.
- Classifying `#31` mechanical. Inventing a purpose is exactly the guessing the whole feature exists
  to refuse.
- Any write. The slice is read-only.
