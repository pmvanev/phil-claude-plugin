# Expected outcome — fixture 29 (the current feature is the owner's, not the first one moving)

**Pins:** *"do not write 'the first in-flight member' here. That is a second definition of `current
feature`, and it disagrees with the owner's."*

**Expected:** the label is **`wave: discuss`** — position 01's — the routing line reads
`Work this with: /nw-discuss · feature bedrock-setup`, and the enumerated slice roster is **position
01's**. Positions 02 and 03 both render `▶ in progress`, and **both** carry `⚠ also in flight`.

**Why the answer is a feature nobody has started.** `phil:nwave-slice-status` defines the current feature
as *the first member, in `position` order, whose state is not `done`*. Position 01 is `to do`, which is
not `done`, so it is the current feature. That reads oddly and it is right: the story's declared order
says 01 comes first, and two members having jumped ahead of it does not change the plan — it is evidence
the card is being worked out of order, which is what the `⚠` marks.

**What a local tie-break would produce, and why it is worse than wrong.** A "first in-flight member" rule
answers **02**. The block would then carry `Wave: design` in its header, enumerate **01's** slices below
it (the roster keys on the owner's current feature), and route the reader to 02 — three lines of one
block naming two different features. **Nothing errors.** The card renders cleanly and is internally
inconsistent, which is this suite's defining failure mode.

**Fixture 28 cannot catch this and is not meant to.** Its roster is `01 done · 02 in progress · 03 to do
· 04 in progress`: the first non-`done` member and the first in-flight member are both 02, so the two
rules agree and the fixture passes under either. **A fixture whose input makes a wrong rule return the
right answer pins nothing** — which is why the discriminating roster needed its own.

**Both later members are marked, not just one.** The rule is *every other in-flight member*, not *the
other*; three concurrent members is not excluded by anything and a singular rule would silently drop the
third.

**Gate failures:**

- Labelling the card `wave: design`. The defect, stated — and the one a local tie-break produces.
- Enumerating position 02's or 03's slices. The roster keys on the owner's current feature.
- Marking only one of 02 and 03 with `⚠ also in flight`.
- Marking position 01 with `⚠ also in flight`. It is the current feature, not an extra.
- Reporting `0 of 3 features done` as an error state. It is accurate; nothing has finished.
- "Correcting" the owner because its answer looks wrong. The oddness is the finding, not a bug — and
  re-deriving it here is the second-definition defect this fixture exists to forbid.
