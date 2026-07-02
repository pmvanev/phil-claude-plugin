# Expected outcome — fixture 05 (`--review` seeds a backlog)

`test_cart_smells.py` carries one instance of each D5 structure-only smell. Running
`/phil:refactor-tests --review .` must detect them and write a `.test-refactoring-backlog.md`
in `review-code`'s backlog format (by convention, DD3), listing every item with `file:line`,
the named move, and a priority.

**Pins:**
- AC1.1 — the backlog is written, one row per detected smell with `file:line`, named move, priority.
- AC1.2 — **only** the D5 set appears: no behaviour-changing items (determinism fixes,
  assertion tightening, assert-splitting) and no deletion suggestions.
- AC1.3 — only test files matching `rules/testing.md`'s globs are scanned (`cart.py`, the SUT,
  is ignored).

**How the loop drives it:** run `--review` over the fixture dir; compare the written backlog
against `expected-backlog.md`.

**Expected gate outcome:** a backlog whose rows match `expected-backlog.md` — four rows, one
per smell, each naming a D5 move.

**Gate failures (block the skill change):**
- **False positive** — any row that is not one of the four D5 smells (e.g. flagging `cart.py`,
  or proposing a behaviour change / deletion). KPI: ≤ 20% reject rate on a real suite.
- **False negative** — a D5 smell present in the file but missing from the backlog.
- **Wrong move** — a smell detected but mapped to the wrong D5 move.

> Detection heuristics are prose, not an AST, so exact `file:line` may drift by a line or two
> as the file is edited. The **match criterion is the (smell, named move) pair per test
> function**, not a byte-exact line number.
