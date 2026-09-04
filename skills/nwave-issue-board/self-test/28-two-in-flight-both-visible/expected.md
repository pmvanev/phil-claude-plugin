# Expected outcome — fixture 28 (two in flight: pick first, and show the other)

**Pins:** *"where two members are `in progress` at once, the label takes the first in roster order and
the roster says so."*

**Expected:** two `▶ in progress` rows in the feature roster. The label is **`wave: design`** — position
02 is the current feature *because `phil:nwave-slice-status` says so*, being the first member in position
order that is not `done`, and **not** because it is the first member that is in flight. Here the two
readings coincide; fixture `29` is the roster where they do not. The routing line reads
`Work this with: /nw-design · feature chat-in-web-ui`. Position 04's Notes cell carries
**`⚠ also in flight`**.

**The label resolves without this skill deciding anything; the evidence must not be consumed by that
resolution.** The current feature is already defined by the deriving skill, so no tie-break belongs here
— inventing one produces a second definition that disagrees with the owner's. What matters at this tier
is that naming a current feature does not *erase* the other member's state: a card showing one
`▶` and a confident label is indistinguishable from a correctly sequenced story.

**Why the block reports and does not refuse.** Two features genuinely in flight is a defect in the card
under this feature's locked decision that a story is worked sequentially by one owner — a story is worked sequentially by one owner, and two concurrent members means it should
be two feature cards under a goal. But **that finding is `phil:groom-issues`'s**, and grooming reads the
board. A block that refused to render would remove the evidence the finding is made from. Slice 04 makes
the state visible; slice 05 makes it reported. Rendering the defect faithfully is what makes the report
possible.

**The `⚠` is on the row, not in the header.** Header lines are about the card; this is a fact about one
member. Putting it in the header would say the *story* is in a warning state, when what is true is that
one member is somewhere it should not be.

**This is also the state in which the label's approximation degrades**, and the two facts are connected:
the current-feature label is honest exactly while one member is current. It stops being honest precisely
here — in a state grooming now flags. That is the argument that the one-label design holds, and it is
why this fixture belongs to the label slice rather than the grooming one.

**Gate failures:**

- One `▶` row. Rendering the story as though it were correctly sequenced.
- Both labels, or `wave: mixed`. The single-valued rule does not bend for a defective card.
- Omitting the `⚠ also in flight` note. The label then silently picks a winner and the evidence is gone.
- Refusing to render the block. It removes the input `phil:groom-issues` needs.
- Emitting a grooming-style finding in the block. Slice 05 owns the report; the block owns the state.
- Taking the label from position 04 because DELIVER is further along. The owner's current feature
  decides, not wave order.
- Applying a local "first in-flight member" tie-break. It agrees with the owner here and disagrees on
  fixture `29`'s roster, which is why agreeing here proves nothing.
