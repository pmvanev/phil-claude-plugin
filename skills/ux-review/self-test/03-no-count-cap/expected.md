# Expected outcome — fixture 03 (Miller's number is not a cap)

**Pins:** *"A **max 7 items** (or equivalent) count cap — `ux.md` explicitly rejects it; at most advise
chunking."*

**Expected outcome:** `COUNT-CAP-NOT-FLAGGED`. No finding at all about the number of items.

**Why this one recurs.** "Seven plus or minus two" is the most-cited and most-misapplied number in
interface design. It describes short-term memory span for recall, not how many links may appear on a
page a user can see. A reviewer repeating it sounds authoritative and is wrong, and the standard it
would be citing says so in as many words.

**The menu is already chunked**, into three labelled groups — so even the legitimate advice, *advise
chunking*, has nothing to say here. A reviewer that raises chunking anyway is pattern-matching on the
count it was told not to use.

**Gate failures:**

- Any finding whose reasoning rests on the number of items.
- Advising chunking where grouping already exists. That is the count cap with better manners.
- Citing Miller, "cognitive load", or "7±2" in support of a finding.
