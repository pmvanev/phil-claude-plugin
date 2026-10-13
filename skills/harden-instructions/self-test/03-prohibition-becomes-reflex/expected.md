# Expected outcome — fixture 03 (prohibitions become reflexes)

**Situation.** One bullet holds three prohibitions about how work reaches `main`.

**Pass.** The bullet states what holds: work reaches `main` through a pull request that someone other
than its author reviews and merges. Each of the three constraints survives in positive form. The
bullet may split into one instruction per line.

**Fail.**
- `never`, `don't` or `do not` remains with no alternative named beside it. Each of these three has a
  positive form that keeps its scope, so none may stay bare.
- A constraint disappears — the self-merge ban and the review requirement are distinct.
- A constraint the file never held appears, such as a required approval count or a CI gate.

This fixture states properties, not a target sentence: a fixture that supplies the rewrite turns a
composition test into "emit this string".
