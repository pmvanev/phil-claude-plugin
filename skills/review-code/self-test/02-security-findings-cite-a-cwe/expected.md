# Expected outcome — fixture 02 (security findings cite a CWE)

`ingest.py` mirrors forge issues into a cache and triages them with a model. It holds ten security
defects, each on a line an always-flag row of `rules/security.md` describes, beside six look-alikes
that row or the Do-not-flag list clears. `test_ingest.py` is green and holds one look-alike of its own.

**Pins:** a security finding names the CWE id of its row and takes the row's Preferred form as its fix.
Before the rule existed, `review-code` had one bullet — "Security vulnerabilities (injection,
unsanitized input)" — that named no id, no fix and no exemption.

**How to drive it:** drive this working tree's `skills/review-code/SKILL.md` by hand over this
directory (`/phil:review-code` runs the released copy).

**Expected:** a `.refactoring-backlog.md` holding the ten Priority 1 items in `expected-backlog.md`,
matched on the Smell and on a Refactoring that begins with the row's Preferred form (a concrete
instance may follow it):

1. **CWE-798** — `DB_PASSWORD`, a production password assigned in source.
2. **CWE-89** — `cards_for` formats the caller's `owner` into SQL.
3. **CWE-338** — `reset_code` draws a reset code from `random`.
4. **CWE-502** — `load_snapshot` unpickles a request body.
5. **CWE-295** — `fetch_issue` turns certificate verification off.
6. **CWE-297** — the same context turns hostname verification off; one item per id that fires.
7. **CWE-78** — `commits_mentioning` builds a shell string from an issue title.
8. **CWE-1427** — `triage` puts an issue body into a prompt that holds a shell.
9. **CWE-250** — `triage` grants the model a bare shell to apply a label.
10. **CWE-78** — `triage` runs the model's reply in a shell (the model-output row, LLM05:2025).

**Hard assertions (any failure blocks the skill change):**

- **No security item names a look-alike:**
  - `cards_sorted` formats SQL from a closed set — the injection rows need untrusted data.
  - `cache_key` uses MD5 as a cache key — a non-security purpose.
  - `display_order` shuffles with `random` — non-security work.
  - `hash_password` uses scrypt — a password-hashing scheme, not a fast hash.
  - `login` compares with `hmac.compare_digest` — the constant-time compare the row asks for.
  - `password123` in `test_ingest.py` — a test credential.
- **No item demands a prompt-injection filter or guardrail** for `triage`. The rule flags the
  capability, never a missing filter.
- Every security item carries `Route: report only` and names its CWE id in the Smell field.
- Advisory items are counted under Advisory, never under Priority 1.

**Not a failure:** an Advisory question about `login`'s rate limit or `cards_for`'s ownership check —
each guard can live in code this directory does not hold, which is the case the rule sends to
Advisory; items about structure or naming; line numbers within ±2.

**Driven 2026-10-20** against this working tree's `SKILL.md` at 1.2.0, by a fresh agent that read only
`ingest.py` and `test_ingest.py`: eight of the eight items then listed, no look-alike, both Advisory
questions above. It also filed CWE-297 and CWE-250, both correct, and both now pinned as items 6 and 9.
