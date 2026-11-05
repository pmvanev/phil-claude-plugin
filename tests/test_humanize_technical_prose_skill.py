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
