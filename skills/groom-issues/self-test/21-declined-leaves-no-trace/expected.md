# Expected outcome — fixture 21 (a decline record is a marker wearing another word)

The user says no. The third time, on the same pair.

**Expected decision:** `DECLINE-NO-TRACE`. Nothing is written anywhere, and the report says so at the
point of the decline:

```
#2 and #3 — left apart, as you said. Nothing written.

This pair will be proposed again next run. Grooming stores no state: the defect table is
re-derived from the board every time, so a decline is remembered by nobody. That is the
price of having no second authority over what your issues mean.
```

**Why the obvious fix is the forbidden one.** A `declined` label, a comment saying *considered and kept
separate*, a line in a body, a dotfile listing pairs — every one of them would stop the repetition, and
every one is the marker D6 exists to refuse. It becomes a second authority the moment it disagrees with
the board: two cards diverge until they genuinely are unrelated, or converge until they genuinely are
duplicates, and the stored decline outranks both because it is what the next run reads first. The
candidate that most needs re-proposing is the one a marker most reliably silences.

**Why the note is owed here and not only in the summary.** Unstated, the third proposal of the same pair
reads as the tool having forgotten — which is a complaint, and the fix a user asks for is the marker.
Stated at the decline, it reads as the design: the board is the only record, and it is re-read every time.
The user can end the repetition whenever they like, by changing the bodies so the overlap is no longer
there — which is grooming.

**Gate failures:**

- Writing anything at all: label, comment, body edit, file, or a line in a report meant to be read back.
- Carrying the decline in session memory and skipping the pair later in the same run. Same marker,
  shorter lifetime — and it makes a long run behave differently from two short ones.
- Suppressing the note because this is the third time and the user obviously knows. The note is what
  keeps the repetition legible as a design choice.
- Apologising for re-asking, or offering to remember. The offer is the request for the marker, made by
  the tool instead of the user.
