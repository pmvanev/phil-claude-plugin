# Expected outcome — fixture 06 (an arrival is not a re-rank)

**Expected decision:** `INCREMENTAL-PLACE`. Ask which goal it belongs to, ask where inside that goal,
write one milestone assignment and one position. Two questions, two writes.

**Gate failure:** re-running the whole session — re-eliciting goals, re-ordering goals, re-ordering
every goal's contents. It produces a correct board and destroys the property the design was built
for: an order that survives new issues arriving. It also silently discards ranking decisions the user
made previously and may not remember making.

Read this fixture with `03`. Together they bound the scheme from opposite ends — `03` stops a
dependency being flattened into an order; `06` stops an arrival flattening the structure back into
one list. A session that satisfies one by a rule that breaks the other has not understood the design.
