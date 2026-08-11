# Expected outcome — fixture 08 (the one failure that assigns work)

**The actively harmful case.** Slices 01 and 02 are done, so positionally slice 03 is next, and every
signal except the one that matters agrees. Its own file says not to build it.

Every other failure in this suite misinforms someone. This one puts a card on a board where a person
picks it up and builds deferred work. `nwave-slice-status` treats the marker as overriding every other
source; publishing must not quietly re-admit what it excluded.

**Expected decision:** `DEFERRED-NOT-A-CARD`.

**Checkable assertions (all must hold):**

1. No issue is opened for slice 03.
2. Slice 03 is never published as next, current, or to-do.
3. If it is mentioned at all — in a roster, say — it is marked deferred, and the marker travels with
   it.
4. Its absence from `roadmap.json` is not read as an oversight to be corrected.

**Gate failure (blocks the skill change):** a card for slice 03 on the board in any column; OR slice
03 published as next because slices 01 and 02 are done.
