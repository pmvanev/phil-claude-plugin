"""`skills/ai-eos/SKILL.md` must score and report one way, and only ask for what its command grants.

Found 2026-10-13, all predating that day's hardening:
- "≥4 distinct mechanisms ... raises the verdict one band" was cancelled by the next sentence, "take the
  lower verdict", so the raise was dead text; the single-mechanism lowering could reach `clean` while
  tells were listed.
- Clustered whiffs were "`[tells]`-tier findings" in one place and never counted in three others.
- The tier rule put every bare single word in the whiff tier while tells #5 and #8 list single words;
  "boasts" sat in both.
- "say so explicitly and stop" could end the report at its first needs-a-fact finding, and "One line
  per finding" contradicted the four-line template.
- Directory mode asked for an Explore agent the `ai-eos` command does not grant.
- "This project's house style" described the plugin, not the repository under review.
- Assistant residue was "conclusive", a provenance claim Safety forbids.
"""
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SKILL = REPO / "skills" / "ai-eos" / "SKILL.md"
COMMAND = REPO / "commands" / "ai-eos.md"
RED_TEAM = REPO / "skills" / "red-team-prose" / "SKILL.md"


def _flat(path):
    return " ".join(path.read_text().split())


def _section(title):
    return " ".join(SKILL.read_text().split(f"## {title}", 1)[1].split("\n## ", 1)[0].split())


def test_the_raise_is_live_and_a_lowered_verdict_never_reaches_clean():
    density = _section("Step 3: Judge the Density")
    assert "take the lower verdict" not in density
    assert "raises the verdict one band" in density
    assert "never lowers a verdict below **a few spots** while any tell is reported" in density


def test_whiffs_never_count_in_ai_eos_or_in_red_team_prose_which_runs_it():
    skill = _flat(SKILL)
    assert "report as `[tells]`-tier findings" not in skill
    assert "Clustered whiffs go in the `WHIFFS` section" in skill
    assert "never count toward the rate or the mechanism count" in skill
    red_team = _flat(RED_TEAM)
    assert "do not affect the density count" not in red_team
    assert "whiffs never count toward the rate or the mechanism count" in red_team


def test_the_tier_rule_names_its_exceptions_and_no_word_sits_twice():
    hunt = _section("Step 2: Hunt the Tells")
    assert "except where a tell names its own single words" in hunt
    promotional = re.search(r"\*\*8\. Promotional register\*\*(.*?)\*Fix:\*", hunt).group(1)
    assert "boasts" not in promotional
    assert "A single era-vocabulary hit" in _flat(SKILL)


def test_a_needs_a_fact_finding_ends_the_fix_not_the_report():
    report = _section("Step 4: Report")
    assert "say so explicitly and stop" not in report
    assert "One line per finding" not in report
    assert "say so in that finding's Fix line" in report


def test_directory_mode_asks_only_for_tools_the_command_grants():
    granted = re.search(r"allowed-tools: (.*)", COMMAND.read_text()).group(1)
    assert "Agent" not in granted and "Task" not in granted
    assert "Explore agent" not in _flat(SKILL)
    assert "as `ai-eos` specifies" not in _flat(RED_TEAM)


def test_house_style_is_the_reviewed_document_s_not_the_plugin_s():
    for text in (_flat(SKILL), _flat(RED_TEAM)):
        assert not re.search(r"this project's (house style|own rules|deliberate house style)", text, re.I)
        assert "when reviewing this repository" not in text
    assert "single vocabulary hit" not in _flat(RED_TEAM).lower()


def test_no_provenance_claim_survives():
    assert not re.search(r"\bconclusive\b", _flat(SKILL))
