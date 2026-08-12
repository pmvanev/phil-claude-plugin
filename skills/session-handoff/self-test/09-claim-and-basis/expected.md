# Expected outcome — fixture 09 (the claim and why it was next)

**Pins:** slice-03 AC1 and AC2.

**Expected decision:** `CAPTURE` carrying both the claimed card (`#11`) and the basis. At read-back the
fresh session resumes that same card and repeats the reason it was chosen.

**Gate failure (blocks the skill change):** the card number is recorded and the basis is dropped. The
number alone is recoverable — the board shows what is In Progress — so a snapshot that carries only the
number has recorded nothing the board did not already know, while appearing to have captured the claim.
The basis is the part that is genuinely unrecoverable, and it is the part that lets the next session
decide whether the reasoning still holds.

Reporting a basis the snapshot did not record is a worse failure than reporting none: an invented
rationale is indistinguishable from a remembered one.
