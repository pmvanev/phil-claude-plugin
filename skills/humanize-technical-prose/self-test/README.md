# Self-test — humanize-technical-prose

The acceptance and regression gate for `../SKILL.md`, driven structurally by
`tests/test_humanize_technical_prose_fixtures.py`. The counting script has its own unit tests in
`tests/test_humanize_measure_voice.py`.

**What the driver can and cannot check.** Whether a rewrite reads as its author's is not automatable,
so the fixtures are model-driven: a run follows the skill on each fixture's inputs and is judged
against its `expected.md` and `must_not`. The driver checks what can be checked mechanically:

- each manifest is well formed, and its inputs exist;
- it names outcomes the skill defines, which the driver reads from the skill's `## Outcomes` tables;
- every outcome has a fixture;
- no fixture hands the run its own rewrite;
- every slips fixture expects the kinds the allocation script actually draws.

**Manifest scheme:** `fixture_id`, `slice`, `inputs`, `git_state`, `arguments`, `expected_decision`
(one terminal outcome), `expected_report_lines`, `expected_guard`, `must_not`,
`why_this_fixture_exists`.

**No sample text.** Every draft and sample here was written for the fixture. The profiles carry real
counts measured from the developer's thesis, essay and co-written paper. Counts are not passages, so
the developer had no passage to approve one by one.

| Fixture | Slice | Terminal | Alongside | Pins |
|---|---|---|---|---|
| `01-tells-rewritten` | 1 | `WROTE` | `VOICE-SKIPPED` | Each tell takes its catalogue fix; protected spans beside them stay |
| `02-uncommitted-draft` | 1 | `REFUSED-UNCOMMITTED` | — | The committed version is the only undo |
| `03-tell-in-a-code-block` | 1 | `WROTE` | `VOICE-SKIPPED` | The same phrase in a code comment is code |
| `04-a-rewrite-that-would-add-a-tell` | 1 | `WROTE` | `VOICE-SKIPPED` `TELLS-LEFT` | The re-check catches a swapped tell; no citation is invented |
| `05-a-clean-draft` | 1 | `NOTHING-CHANGED` | `VOICE-SKIPPED` | A clean verdict is the answer |
| `06-an-argument-that-does-not-parse` | 1 | `REFUSED-ARGUMENT` | — | No guessing what an argument meant |
| `07-profile-from-two-samples` | 2 | `PROFILE-BUILT` | — | Own prose only; no name, quotation or slipped word stored |
| `08-every-sample-thin` | 2 | `PROFILE-NOT-BUILT` | `SAMPLE-THIN` | No profile from too little prose |
| `09-a-transcript-named` | 2 | `PROFILE-NOT-BUILT` | `SAMPLE-REFUSED` | Prompts are no voice sample |
| `10-adding-a-sample-rebuilds` | 2 | `PROFILE-BUILT` | — | Rebuild from all samples; never overwrite or sum |
| `11-voice-toward-formal` | 3 | `WROTE` | — | The voice pass's allowed moves, each measured |
| `12-voice-toward-essay` | 3 | `WROTE` | — | Another profile, another output; no added attitude |
| `13-a-join-that-would-add-a-participle` | 3 | `WROTE` | — | The detector wins over the profile |
| `14-terms-code-and-a-quotation-stay` | 3 | `WROTE` | — | The voice pass leaves terms, code and quotations alone |
| `15-a-profile-that-does-not-exist` | 3 | `WROTE` | `VOICE-SKIPPED` `SLIPS-SKIPPED` | No fallback profile, and no slips without one |
| `16-two-slips` | 4 | `WROTE` | `SLIPS-UNMIRRORED` `SLIPS-WARNING` | Exactly N, of the profile's kinds, each reported |
| `17-zero-slips` | 4 | `WROTE` | — | Zero adds none |
| `18-too-few-open-positions` | 4 | `WROTE` | `SLIPS-SHORT` `SLIPS-UNMIRRORED` `SLIPS-WARNING` | The count is a ceiling; no slip in code or a claim |
| `19-a-profile-with-no-grammar-kinds` | 4 | `WROTE` | `SLIPS-NONE-OF-KIND` | No fallback to misspellings |
| `20-residue-in-a-reworded-sentence` | 4 | `WROTE` | `SLIPS-WARNING` | Residue lands where the run reworded |
| `21-misspellings-from-the-paper` | 4 | `WROTE` | `SLIPS-UNMIRRORED` `SLIPS-WARNING` | Mechanisms followed; terms never misspelled |
