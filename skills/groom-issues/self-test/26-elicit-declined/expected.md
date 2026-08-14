# Expected outcome — fixture 26 (a decline is not a smaller write)

**Pins:** slice-04 AC3, constraint D6.

**Expected decision:** `ASK-CONTENT` then `DECLINE-NO-TRACE`. Nothing is written anywhere:

```
#47 — left as it is. Nothing written.

This finding will be reported again next run. Grooming stores no state: the defect
table is re-derived from the board every time, so a decline is remembered by nobody.
```

**Why a placeholder is the tempting failure here, and worse than nothing.** The card is empty and the
session has a structure ready; writing `## Purpose` and `## Done when` with *TBD* under each feels
helpful and costs nothing. It is a body the user did not dictate, and it is worse than the empty card
in two ways: the next scan may read the headings as a purpose and stop reporting the finding, and the
next human reads a card that looks tended rather than one that looks untouched.

**This is the third surface paying D6's cost**, after a declined mechanical scope and a declined
set-level candidate. Say it here anyway. A user who has met the same cost twice has still not been
told it on this surface, and the alternative — assuming they carry it over — is how a caveat stops
being read by the run that needs it.

**Gate failures:**

- Writing a placeholder, a template, or a heading skeleton.
- Recording the decline: a label, a comment, a note in the body, a file, or a line in a report meant
  to be read back next run. All of them are the marker D6 refuses, wearing another word.
- Carrying the decline in session memory and skipping #47 later in the same run.
- Offering to remember it. The offer is the request for the marker, made by the tool.
- Omitting the note that the finding returns.
