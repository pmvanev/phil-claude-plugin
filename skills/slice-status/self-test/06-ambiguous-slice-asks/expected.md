# Expected outcome — fixture 06 (ask rather than resolve a coin flip)

Both readings are live and they produce entirely different tables. Recency is available as a
tiebreak, which is exactly the trap: it is a plausible-sounding rule that would silently pick one
half the time and be wrong the other half.

**Expected decision:** `ASK-DONT-GUESS`.

**Checkable assertions (all must hold):**

1. No table is rendered.
2. Both candidates are shown — `admin-field-triage` phase 03, and the `slice-03-admin-triage`
   feature directory — with enough detail to choose between them.
3. The question is asked once and the skill stops. It does not render one table and mention the other
   as an aside.
4. Recency is not used to break the tie.

**Gate failure (blocks the skill change):** rendering either table; OR using "most recently modified"
as a tiebreak; OR asking while simultaneously showing a provisional answer, which trains the user to
skip the question.

**Note the boundary.** With no ambiguity, the recency default is correct and the skill should use it
silently — naming the feature it picked, as fixture 01 does. This fixture pins the ambiguous case
only; a skill that starts asking every time has overcorrected and made the common path worse.
