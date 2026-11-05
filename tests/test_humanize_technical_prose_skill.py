"""`skills/humanize-technical-prose/SKILL.md` and its command: what each pass may touch, and in what order.

The decisions these pin are in `docs/feature/humanize-technical-prose/feature-delta.md` (D1-D17). Each
test quotes the skill's own words, so rewording a rule away fails here before it ships.
"""
import re
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
SKILL = REPO / "skills" / "humanize-technical-prose" / "SKILL.md"
COMMAND = REPO / "commands" / "humanize-technical-prose.md"


def _flat(path=SKILL):
    return " ".join(path.read_text().split())


def _section(title):
    text = SKILL.read_text()
    assert f"## {title}" in text, f"no section {title!r}"
    return " ".join(text.split(f"## {title}", 1)[1].split("\n## ", 1)[0].split())


def _frontmatter(path):
    return yaml.safe_load(path.read_text().split("---", 2)[1])


# --- slice 01: the command, the committed-file gate, protected spans, the tells pass, the report ---

def test_the_command_loads_the_skill_and_declares_that_it_mutates():
    fm = _frontmatter(COMMAND)
    assert fm["mutates"] is True, "it edits the document and writes the profile (D15)"
    assert "${CLAUDE_PLUGIN_ROOT}/skills/humanize-technical-prose/SKILL.md" in COMMAND.read_text()


def test_the_command_grants_only_the_git_verbs_the_gate_needs():
    grants = {g.strip() for g in _frontmatter(COMMAND)["allowed-tools"].split(",")}
    git = {g for g in grants if g.startswith("Bash(git")}
    assert git == {"Bash(git ls-files:*)", "Bash(git status:*)"}
    assert "Bash" not in grants, "bare Bash would grant every verb"


def test_an_uncommitted_draft_is_refused_and_nothing_is_written():
    gate = _section("Step 1: Check the Draft Is Committed")
    assert "git ls-files --error-unmatch" in gate
    assert "git status --porcelain" in gate
    assert "`REFUSED-UNCOMMITTED`" in gate
    assert "write nothing" in gate


def test_the_gate_forbids_the_git_flags_that_write():
    assert "Pass neither `--output` nor `--ext-diff`" in _section("Step 1: Check the Draft Is Committed")


def test_protected_spans_include_names_and_technical_terms():
    spans = _section("Step 2: Mark the Protected Spans")
    for item in ("code", "commands", "identifiers", "links", "numbers", "quotations", "names",
                 "technical terms", "headings", "frontmatter", "tables of data"):
        assert item in spans, f"{item} is not protected"
    assert "byte-for-byte" in spans


def test_the_tells_pass_runs_ai_eos_itself_and_takes_its_fix():
    tells = _section("Step 3: Strip the Tells")
    assert "${CLAUDE_PLUGIN_ROOT}/skills/ai-eos/SKILL.md" in tells
    assert "the fix its catalogue names" in tells
    assert "ai-eos`'s report template is suppressed" in tells


def test_a_tell_whose_fix_needs_a_fact_is_left_and_listed_never_invented():
    tells = _section("Step 3: Strip the Tells")
    assert "needs a fact the draft does not hold" in tells
    assert "`TELLS-LEFT`" in tells


def test_the_tells_pass_rechecks_its_own_rewrites():
    tells = _section("Step 3: Strip the Tells")
    assert "re-run the hunt over every sentence this pass changed" in tells
    assert "restore the original sentence" in tells


def test_the_report_cites_the_writing_standard_by_plugin_root():
    report = _section("Step 7: Report")
    assert "Read `${CLAUDE_PLUGIN_ROOT}/rules/writing.md`" in report
    bare = re.findall(r"(?<!})/?\brules/writing\.md", report.replace("${CLAUDE_PLUGIN_ROOT}/rules/writing.md", ""))
    assert not bare, "a bare rules/writing.md resolves against the consumer's repo"


def test_the_standard_governs_the_report_and_never_the_document():
    report = _section("Step 7: Report")
    assert "applies to the words the report composes" in report
    assert "never to the document" in report


def test_the_report_claims_nothing_about_authorship():
    assert "claims nothing about who wrote the document" in _section("Step 7: Report")


def test_the_report_names_the_undo():
    assert "git checkout -- {file}" in _section("Step 7: Report")


# --- slice 02: build a named profile from the author's own documents ---

import importlib.util

_spec = importlib.util.spec_from_file_location(
    "measure_voice", REPO / "skills" / "humanize-technical-prose" / "scripts" / "measure_voice.py")
measure_voice = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(measure_voice)


def test_the_profile_reads_only_named_samples_and_never_a_transcript():
    build = _section("Step B: Build a Profile")
    assert "Never read a transcript" in build
    assert "`TRANSCRIPT-REFUSED`" in build


def test_the_build_runs_the_measuring_script_by_plugin_root():
    build = _section("Step B: Build a Profile")
    assert "python3 ${CLAUDE_PLUGIN_ROOT}/skills/humanize-technical-prose/scripts/measure_voice.py --measure" in build
    assert "--build {name} --slips -" in build


def test_a_thin_sample_is_named_and_left_out():
    assert "`SAMPLE-THIN`" in _section("Step B: Build a Profile")


def test_adding_samples_rebuilds_from_all_of_them():
    assert "rebuild it from every sample, old and new" in _section("Step B: Build a Profile")


def test_the_slip_vocabulary_in_the_skill_is_the_one_the_script_accepts():
    """The skill classifies and the script stores; a kind the one names and the other refuses is a run
    that fails at the last step, after every sample was read."""
    build = SKILL.read_text().split("## Step B: Build a Profile", 1)[1].split("\n## ", 1)[0]
    mechanisms = set(re.findall(r"^\| misspelling \| ([a-z ]+) \|", build, flags=re.M))
    assert mechanisms == measure_voice.MISSPELLING_MECHANISMS
    for cause, kinds in measure_voice.GRAMMAR_CAUSES.items():
        found = set(re.findall(r"^\| " + cause + r" \| ([a-z ]+) \|", build, flags=re.M))
        assert found == kinds, f"{cause}: skill names {found}, script accepts {kinds}"


def test_no_slipped_word_is_written_anywhere():
    build = _section("Step B: Build a Profile")
    assert "never write a slipped word" in build
    assert "not in the profile, the tally or the report" in build


def test_a_slip_on_a_name_or_technical_term_is_counted():
    assert "`on_name_or_term`" in _section("Step B: Build a Profile")


def test_when_unsure_a_word_is_not_a_slip():
    assert "When unsure, it is not a slip" in _section("Step B: Build a Profile")


# --- slice 03: the voice pass, and the tells check after it ---

def test_the_voice_pass_runs_only_with_a_profile_that_exists():
    voice = _section("Step 4: Reword Toward the Profile")
    assert "`VOICE-SKIPPED`" in voice
    assert "list the profiles that exist" in voice


def test_the_voice_pass_measures_the_draft_with_the_same_script():
    voice = _section("Step 4: Reword Toward the Profile")
    assert "python3 ${CLAUDE_PLUGIN_ROOT}/skills/humanize-technical-prose/scripts/measure_voice.py --draft" in voice


def test_the_voice_pass_rewords_and_adds_nothing():
    voice = _section("Step 4: Reword Toward the Profile")
    for banned in ("a claim", "a fact", "a figure of speech", "a hook", "an analogy", "a joke", "a question"):
        assert banned in voice, f"the ban on adding {banned} is missing"
    assert "Never add" in voice


def test_the_voice_pass_never_changes_who_acts_or_how_sure_a_sentence_is():
    voice = _section("Step 4: Reword Toward the Profile")
    assert "first person" in voice and "modality" in voice


def test_a_feature_that_moved_away_from_the_profile_is_undone():
    voice = _section("Step 4: Reword Toward the Profile")
    assert "farther from the profile than before" in voice
    assert "undo" in voice


def test_the_detector_wins_over_the_profile():
    again = _section("Step 5: Check the Tells Again")
    assert "every sentence the voice pass changed" in again
    assert "restore the sentence as Step 3 left it" in again
    assert "even where the author's samples hold that construction" in again


def test_the_report_shows_each_feature_before_and_after_against_the_profile():
    assert "VOICE {profile}: median sentence {before} → {after} (profile {target})" in _section("Step 7: Report")


# --- slice 04: exactly the slips asked for ---

def test_no_slips_unless_counted():
    slips = _section("Step 6: Add the Slips")
    assert "`--slips 0`, or no `--slips`, adds none" in slips


def test_the_script_divides_the_count_among_the_profile_kinds():
    slips = _section("Step 6: Add the Slips")
    assert "python3 ${CLAUDE_PLUGIN_ROOT}/skills/humanize-technical-prose/scripts/measure_voice.py --allocate {name} {N}" in slips
    assert "Add exactly the slips it returns" in slips


def test_grammar_kinds_by_default_and_misspellings_only_when_asked():
    assert "misspellings only with `--misspellings`" in _section("Step 6: Add the Slips")


def test_no_slip_lands_in_a_protected_span_or_on_a_name_or_term():
    slips = _section("Step 6: Add the Slips")
    assert "outside every protected span" in slips
    assert "never on a name or a technical term" in slips


def test_a_slip_never_changes_what_a_sentence_claims():
    slips = _section("Step 6: Add the Slips")
    for guarded in ("a negation", "a number", "a unit", "a quantifier", "a comparative", "a modal"):
        assert guarded in slips, f"a slip may touch {guarded}"


def test_a_residue_slip_lands_where_the_voice_pass_reworded():
    assert "only in a sentence the voice pass reworded" in _section("Step 6: Add the Slips")


def test_shortfall_none_of_kind_and_unmirrored_are_each_reported():
    slips = _section("Step 6: Add the Slips")
    for line in ("`SLIPS-SHORT`", "`SLIPS-NONE-OF-KIND`", "`SLIPS-UNMIRRORED`", "`SLIPS-WARNING`"):
        assert line in slips


def test_the_slips_run_last_and_the_report_warns_a_cleanup_will_fix_them():
    report = _section("Step 7: Report")
    assert "SLIPS-WARNING: a later phil:eos, phil:red-team-prose or spell-check pass will fix these slips" in report
