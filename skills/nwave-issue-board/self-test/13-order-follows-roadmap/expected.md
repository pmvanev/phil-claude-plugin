# Expected outcome — fixture 13 (the order that looks decided)

The board reads 01, 02, 03, 04. Slice numbers ascend, issue numbers ascend, and nothing on the page
suggests a problem. The roadmap says 03 is worked before 02, so a person taking the top card after
01 closes picks up the slice a spike already moved behind another.

No one chose that order. It is what the forge renders when no position was ever written, and it is
indistinguishable from a position someone set on purpose.

**Expected decision:** `ORDER-FOLLOWS-ROADMAP`.

**Checkable assertions (all must hold):**

1. The to-do column is positioned `#101, #103, #102, #104` — `phases[]` array order.
2. The order comes from the array, not from the slice file numbers and not from the issue numbers,
   which agree with each other and disagree with the roadmap.
3. A position is written for every card in the column, not only for the two that changed places. A
   partial pass leaves an order that is neither the old one nor the intended one.
4. Positions are written top-down in one pass, each anchored to a card already placed.
5. The resulting order is read back and compared against `phases[]`.
6. This being GitHub, the parent's sub-issue list and the column are treated as two orders. Fixing
   one is not reported as having fixed the other.
7. Nothing about the ordering pass changes a card's column, status, or step table.

**Gate failure (blocks the skill change):** the column left as the forge rendered it; OR reordered
by slice number or issue number; OR a position written for some cards and not others; OR the
sub-issue list reordered and the column reported as ordered.
