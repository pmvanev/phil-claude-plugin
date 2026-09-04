# Expected outcome — fixture 23 (a state with no glyph fails; it never becomes `·`)

**Pins:** *"a value with no glyph must fail, never degrade to `·`"* — the property the slice vocabulary
already carries, now required to hold over **two** vocabularies.

**Expected: fail**, naming the value and the skill that returned it. Emit no row for that feature and no
block. Do not invent a glyph, and do not publish the other three rows as though the roster were complete.

**Why `·` is the specific wrong answer.** `·` means `to do` — *nobody has started this*. Rendering an
uncovered value as `·` converts a fact about the **renderer's** vocabulary into a claim about the
**work**, which is this skill family's cardinal defect: unknown published as not started. At feature
scale the misreported unit is a whole feature; a reader sees three features moving and one untouched,
and the untouched one may be finished, blocked, or withdrawn.

**Why failing beats `?`.** `?` (`unknown`) is honest about the work but dishonest about the cause — it
says *nobody assessed this*, when in fact the owner assessed it and the renderer could not read the
answer. That misdirects the fix: the reader goes looking at the feature's artifacts instead of at the
version skew between two skills.

**This is a coupling test between two skills, and that is the point.** The owner defines the vocabulary
and this skill renders it, so adding a value there without adding a glyph here is a silent break. Failing
loudly is what makes the coupling visible on the first render rather than on the first misread card.

**Gate failures:**

- Rendering `·`. The defect, stated.
- Rendering `?`. Honest about the work, wrong about the cause, and it sends the fix to the wrong place.
- Rendering the value as bare text with no glyph. The column becomes unscannable and the break is
  invisible to anyone not diffing.
- Skipping the row and rendering the other three. A roster missing a declared member is a false roster.
- Publishing the block with a warning appended. A warning outside the markers is destroyed by the next
  regeneration; the failure must stop the write.
