# Expected outcome — fixture 11 (capture checks coverage, size and risk)

The developer's draft has two expectations. The first packs two behaviours into one breath. The second —
"the JSON export is unchanged" — covers must-not-happen: it says existing behaviour stays unchanged.
No expectation covers a past edge case, though the repository's history records one: a CSV writer
broken by records containing commas.

**Pins:** edd-article-alignment slice 01, AC1.1–AC1.4 — the article's capture guidance.

**Expected decision:** `CAPTURE-GAPS`. Before the developer confirms, the tool shows:
- **Coverage:** past edge cases named as missing, with a suggestion labelled `composed` and drawn
  from the history it searched — e.g. "a record containing a comma or a quote round-trips through
  the CSV export". Must-not-happen is **not** named: the JSON line covers it.
- **Size:** a proposed split of the first expectation into a content expectation and a speed
  expectation, both `composed`, with the original line kept beside them, labelled `you wrote`.
- **Risk:** the list ordered JSON export first (a miss hits every existing user and is hard to undo),
  then CSV content, then speed.
- **Provenance:** both original lines labelled `you wrote` and kept word for word; composed lines
  follow `rules/writing.md`; the list sits in the ask's context block.

The developer accepts, edits or declines each suggestion; an edited suggestion becomes `you edited`.
Nothing proceeds until the developer confirms the list.

**Gate failure (blocks the skill change):** past edge cases go unnamed; a past bug is invented rather
than found in the history or asked of the developer; must-not-happen is named as missing although
the JSON line covers it; the double expectation goes unsplit, or its original line is dropped; the
list is not risk-ordered; or a `you wrote` line is reworded.
