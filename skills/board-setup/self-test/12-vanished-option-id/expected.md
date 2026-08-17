# Expected — BS-SELFTEST-12

`REFRESHED`, with the change reported line by line.

## What must happen

Inside the markers, the vanished id is replaced by what the forge now returns. Outside them, the
hand-written line naming the old id is **reported and not touched** — it becomes a `contradicts` entry
in the drift report, and the retire offer applies to it as to any other contradiction.

The change report names **which constant moved**, not how many did.

## What must NOT happen

No edit outside the markers without an explicit answer. No bare count: an option id that changed means
`updateProjectV2Field` was run against the field, and a docs root that changed means every absolute
link in every issue body is now wrong. Those need different responses, and a count tells the reader
neither.

## Why this fixture exists

A vanished option id has two possible causes and they are not distinguishable from inside this command:
the option really was deleted, **or the probe was pointed at the wrong board**. Both produce exactly
this observation.

So the region is refreshed — it is generated, and regenerating it is the whole contract — while the
human's prose is left alone and the disagreement is put in front of them. Deciding which cause it was
is theirs, and it is the decision that determines whether the right answer is to update the notes or
to re-run against a different target.
