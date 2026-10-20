# Expected outcome — fixture 03 (trust judgement)

`board_sync.py` holds the helpers a set of board commands and hooks share. Each function poses one
question a security review must answer before any row can fire: **is this input untrusted here?**
`test_board_sync.py` is green.

**Pins:** `rules/security.md`'s definition of untrusted. Model output is untrusted where code acts on it
with more than the model's own grant; forge metadata other principals write is untrusted; a source whose
writer the code cannot show is a question, not a defect. The first dogfood run hesitated on all three.

**How to drive it:** drive this working tree's `skills/review-code/SKILL.md` by hand over this
directory (`/phil:review-code` runs the released copy).

**Expected:** the Priority 1 items in `expected-backlog.md`, matched on the Smell and on a Refactoring
that begins with the row's Preferred form:

1. **CWE-78** — `apply_fix` runs a model reply in a shell from a hook, which acts with the user's
   privileges whatever the session grants.
2. **CWE-1427** — `describe_labels` puts label names, which anyone with label rights writes, into a
   prompt that holds a shell.
3. **CWE-250** — the same call grants a bare shell to group labels.

**Hard assertions (any failure blocks the skill change):**

- **No item names `save_note`.** The path is the model's, but the command that runs it already grants
  `Write` on any path, so the script grants nothing the model lacks. A CWE-22 item here is a gate failure.
- **`ledger_context` yields an Advisory question, never a CWE-1427 item.** The code cannot show who
  writes the ledger; a cloned repository could.

**Not a failure:** items about structure or naming; line numbers within ±2.
