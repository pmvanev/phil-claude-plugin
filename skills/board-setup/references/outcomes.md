# Decision outcomes — the per-outcome detail

`SKILL.md` lists the eight terminal outcomes and the three report lines. This file says what each one
means and who produced it. **The discriminator is who stopped the run**, because the scripts have one
failure state and the model has another.

## Terminal outcomes — exactly one per run

- **`WROTE`** — the file was created, or a section appended where none existed. Names the file and the
  field count. Nothing human was at risk.
- **`WROTE-BESIDE-PROSE`** — the region was inserted into a section a human had already written.
  Names the file, the field count, and the three drift bucket counts. Distinct from `WROTE` because
  the risk is different: `WROTE` touched a file with nothing to lose.
- **`REFRESHED`** — an existing region was regenerated because the board moved. Names **which
  constants changed**, line by line. Never a bare count: an option id that changed means
  `updateProjectV2Field` was run against the field, and a docs root that changed means every absolute
  link in every issue body is now wrong. Those need different responses.
- **`UNCHANGED`** — an existing region matched a freshly rendered one. **Zero bytes written, and the
  stamp not refreshed.** Not a failure, and not the same as `unread`.
- **`DECLARED`** — a human's answer was written into the declared region. Accompanied by `UNEVALUATED`
  for any family they declined.
- **`AMBIGUOUS-TARGET`** — resolved by the model at CONFIRM, *before* any script runs: two remotes, or
  a fork. A question, never a guess.
- **`REFUSED`** — a script returned `status: refused`. Report `refusal.reason` verbatim and
  `refusal.fix` when non-null. Covers a missing `project` scope, more than one candidate project, no
  board at all, a project with no `Status` field, a forge error, a `--forge` contradicting its host,
  and a label endpoint that would not answer. The file is byte-unchanged.
- **`MALFORMED-MARKERS`** — `begin` without `end`, `end` without `begin`, nested, or out of order, in
  **either** region. Four shapes; the enumeration is a checklist, and `classify()` returns all four.
  Refused with the file byte-unchanged, because a guessed extent deletes prose.

## The three report lines

None of these is an outcome, and none can stand alone. A run emitting one as its verdict has not
reported an outcome.

- **`DRIFT`** — the three bucket counts, on any run that reaches the drift step. That includes a
  refresh: prose can drift while the region is current, and that is the common case.
- **`UNEVALUATED`** — each label family left undeclared, so a decline is visible rather than silent.
  Without it, `phil:groom-issues` rule 4 stays dark and nothing says so.
- **`REPORTED-NOT-WRITTEN`** — a value that is neither probed nor assumable. Half-probed values are
  now *written*, as `assumed`, so this survives only for the narrower case.

## Two retirements, and why each happened

| Retired | By | Because |
|---|---|---|
| `SECTION-EXISTS` | slice 02 | It meant *"a hand-written section exists, so stop."* Slice 02 is the thing it was deferring to. |
| `REGION-PRESENT` | slice 05 | It meant *"a region exists, so stop."* Slice 05 shipped the safe re-run, so that state is now `REFRESHED` or `UNCHANGED`. |

**A run reporting either is running an old skill.** Each retirement is recorded in three places — here,
in the superseding fixture's `supersedes` field, and in that fixture's `must_not` — so a stale run is
detectable rather than merely wrong.

## Why the report lines are separate from the outcomes

The list once said *exactly one outcome* while `REPORTED-NOT-WRITTEN` was defined as something that
*accompanies a write*. Fixture 01 expected both; fixtures 03, 06 and 07, running against the same board
and therefore the same two half-probed entries, expected neither.

**A rule contradicted by the fixture that tests it is worse than no rule**, because each looks like
authority for the other. The manifests now carry `expected_decision` and `expected_report_lines` as
separate keys, and `tests/test_board_setup_fixtures.py` enforces that exactly one terminal outcome
appears and that no retired name is ever expected.
