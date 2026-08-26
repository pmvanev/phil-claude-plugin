# Expected outcome — fixture 04, the buried ask

**Primary mode:** `BURIED-ASK`. **Full finding set:** `BURIED-ASK` — and nothing else.

**This is the fixture the slice was built to obtain.** Slice 02's brief allowed for the possibility that
"correct wording, wrong placement" could not be expressed as a fixture at all, in which case placement
was a sentence in the standard rather than a clause of it. This is a real ask, recorded verbatim, whose
wording conforms in every respect and whose placement does not.

## What passes, and it is everything except placement

- All three framing elements present and tagged: what was interrupted, what is being decided, what turns
  on it.
- Zero forbidden tokens in the counted ask.
- Framing 142 words against 200; the one question with its three options 182 against 200.

## What fails

No marker line. The 142-word framing arrives at the end of a verification report and a six-row findings
table — 237 words of context — with nothing to separate the report from the question. The reader has to
notice that the prose stopped reporting and started asking.

`test_placement_is_isolated_by_exactly_one_fixture` asserts that this fixture, and only this fixture,
fails on placement alone. That assertion is what keeps the isolation from being lost later: widen any
other check and this test goes red, which is the intended alarm.

## What the check actually sees, which is less than the description

**One absent marker line.** Add `---` to this emission and it CONFORMS — with the same 237 words of
report and six-row table still standing between the reader and the question.

That is not a hole in the fixture; it is the fragment's own position, stated in *The context block*:
context length is bounded in practice and countable by nothing. So the described defect is
length-plus-no-separator and the asserted defect is one typographic token. `context_words: 237` is now
recorded and re-derived in the manifest so the uncheckable half is at least visible, and [D9] rests on
the marker alone.

## What is NOT claimed

The placement check reads a **tagged** emission. Nothing here shows that a buried ask can be detected in
live output — it cannot, and the standard's *Reach* section says so. This fixture proves the clause is
expressible and failable, which is what [D9] needed.

## Gate failures

- Adding a marker to "fix" the fixture. The defect is the fixture.
- Letting a second fixture fail on placement alone. The isolation test exists so that happens loudly.
