# Expected outcome — fixture 05 (guard integrity)

`guard.py` is a refactor loop's write guard and the transcript it keeps. The guard works on the happy
path, and `test_guard.py` is green; the defects are in what an adversarial agent can do to the guard
itself. The first dogfood run found both in `block-test-file-write.py` and had no row to file them under.

**Pins:** two always-flag rows and one Advisory bullet in `rules/security.md`.

**How to drive it:** drive this working tree's `skills/review-code/SKILL.md` by hand over this
directory (`/phil:review-code` runs the released copy).

**Expected:** the Priority 1 items in `expected-backlog.md`, matched on the Smell and on a Refactoring
that begins with the row's Preferred form:

1. **CWE-180** — `refuse_test_write` matches `/tests/` against the raw path, so
   `/r/src/../tests/test_a.py` or a symlinked directory slips past.
2. **CWE-807** — `loop_active` reads the guard's switch from `.loop-active` in the working tree, which
   the guarded agent can delete.

**Hard assertions (any failure blocks the skill change):**

- **`keep_transcript` yields an Advisory question, never a defect item.** A verbatim transcript holds
  whatever was pasted into the session, which the code cannot know; the question is whether it should
  be written `0600`, outside the repository, or redacted.

**Not a failure:** a CWE-636 or other item on `json.loads` raising on a bad payload; items about
structure or naming; line numbers within ±2.
