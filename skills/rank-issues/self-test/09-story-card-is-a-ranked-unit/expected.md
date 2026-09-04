# Expected outcome — fixture 09 (a story card is a ranked unit)

**Pins:** *"the ranked unit is **the card** — a feature card **or** a story card, whichever the board
carries."*

**Expected:** the session runs to completion. Both cards receive a goal and exactly one position each.
The story card's four member features receive **no** position — they are rows inside a card, not cards on
the board.

**Why the stop condition had to narrow rather than widen.** It fires on a unit *that is going away* —
slice cards, left by the retired mapping. A story card is the opposite: a unit the mapping just
introduced. Stopping on it would have made the board's **largest** cards unrankable, which is the failure
the stop condition exists to prevent, inverted.

**Four features, one position.** Giving members positions would put one unit in the queue five times and
make the story's own position meaningless. The order *inside* a story is its declared `position`, which
lives in the members' artifacts and is not a board fact.

**Gate failures:**

- Stopping the session because a card is not a feature card.
- Assigning positions to member features.
- Ranking the story card by counting its members. Position is a claim about what to work on next, not a
  size.
- Requiring the story card to carry a milestone before ranking. A goal and a story coexist; neither is a
  precondition for the other.
