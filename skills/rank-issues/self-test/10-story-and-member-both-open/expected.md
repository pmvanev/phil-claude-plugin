# Expected outcome — fixture 10 (a story and its own member, both carded)

**Pins:** *"a story card and one of its own member features both open is a different defect, and it does
stop."*

**Expected:** the session stops, names `/phil:groom-set`, and ranks nothing. The member should be a row
inside the story, not a card beside it.

**Why this stops when fixture 09 does not.** 09 is two independent cards; this is **one unit on the board
twice**. Any order over it is incoherent — whichever position the member gets contradicts the story's,
and both are claims about what to work on next.

**Reuse grooming's detector; do not write a second one.** This is *features of one story, carded
separately* read from the ranking side, and the evidence is identical: a member's delta declaring the
story's slug. **Two detectors over one defect drift apart**, and the one that drifts is the one nobody
runs a fixture against.

**Stopping is right even though ranking would "work".** Both cards would take positions and the output
would look ordered. That is the characteristic failure of this whole family: a confident order over a
unit that should not exist.

**Gate failures:**

- Ranking both cards.
- Ranking the story and skipping the member, or the reverse. Silently choosing which is authoritative.
- Re-implementing grooming's detection logic here.
- Stopping without naming `/phil:groom-set`. A refusal that does not say what to do next gets worked around.
- Treating it as fixture 09's case because both are cards. The relationship between them is the defect.
