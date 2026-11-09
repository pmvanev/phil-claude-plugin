"""`rules/stories.md` and the three skill files that read it.

The rule shapes card content a session composes, and never a card a person wrote (decision D3 of
docs/feature/story-quality-standard/). So it must reach exactly the composing surfaces — `groom-ask`'s
suggestions and a body drafted through `issue-board` — plus the oversized clause it is the source for,
and it must stay out of the scan, whose five items are structural by the `CLAUDE.md` line "Keep
`groom-issues`' scan structural: five items, no style item."

**What this cannot check.** It proves the rule is named where it should be and absent where it must
not be, not that a suggestion follows it. Whether a drafted done-when names an observable outcome is
model judgement, which fixture 46's `expected.md` carries and a human drives.

Written 2026-11-09, when the rule landed.
"""
import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
RULE = REPO / "rules" / "stories.md"
GROOM = REPO / "skills" / "groom-issues"
ASK = GROOM / "references" / "ask.md"
SCAN = GROOM / "references" / "scan.md"
GROOM_SKILL = GROOM / "SKILL.md"
ISSUE_BOARD = REPO / "skills" / "issue-board" / "SKILL.md"
FIXTURE = GROOM / "self-test" / "46-suggested-done-when-follows-the-story-standard"
CITATION = "${CLAUDE_PLUGIN_ROOT}/rules/stories.md"


def _section(text, heading):
    return text.split(heading, 1)[1].split("\n## ", 1)[0]


def _bare(text):
    return re.findall(r"(?<!})/?\brules/stories\.md", text.replace(CITATION, ""))


def test_rule_records_invest_smart_and_the_three_cs_with_their_authors():
    text = RULE.read_text()
    for letter in ("Independent", "Negotiable", "Valuable", "Estimable", "Small", "Testable"):
        assert f"**{letter}**" in text, letter
    for name in ("Wake", "Doran", "Jeffries", "North", "Cockburn"):
        assert name in text, name
    assert "Card, Conversation, Confirmation" in text
    # Wake's split: SMART fits the tasks inside a story, not the story.
    assert "These are good characteristics for\ntasks as well." in text or "tasks as well" in text


def test_rule_holds_itself_lightly_in_the_authors_words():
    text = RULE.read_text()
    assert "fuzzy clusters" in text
    assert "a guideline" in text
    assert "never a defect to report" in text


def test_rule_records_the_house_card_shape_and_rejects_a_sentence_template():
    shape = _section(RULE.read_text(), "## The house card shape")
    for heading in ("## What it does", "## Done when", "## Open questions"):
        assert heading in shape, heading
    assert "No sentence template" in shape
    assert "overrides it in its own `CLAUDE.md`" in shape


def test_rule_applies_to_composition_only():
    where = _section(RULE.read_text(), "## Where it applies")
    assert "a card a session composes" in where or "content a session composes" in where
    assert "Never to a card a person wrote" in where
    assert "Never as a gate" in where


def test_rule_says_why_estimable_and_time_bound_are_not_applied():
    text = RULE.read_text()
    assert text.count("**Not applied.**") == 2
    assert "Never demand a number" in text


def test_groom_ask_reads_the_rule_for_what_it_drafts_and_never_for_a_you_wrote_field():
    ask = ASK.read_text()
    assert f"Read `{CITATION}`" in ask
    assert not _bare(ask), "a bare rules/stories.md resolves against the consumer's repo"
    paragraph = next(p for p in ask.split("\n\n") if CITATION in p)
    assert "`you wrote`" in paragraph, "the citation must exclude a `you wrote` field where it is made"


def test_issue_board_names_the_rule_where_a_session_drafts_a_card():
    section = _section(ISSUE_BOARD.read_text(), "## Choosing what becomes an issue")
    assert CITATION in section
    assert not _bare(ISSUE_BOARD.read_text())


def test_oversized_clause_cites_the_rule_and_the_scan_stays_structural():
    skill = GROOM_SKILL.read_text()
    oversized = skill.split("- **Oversized**", 1)[1].split("\n- **", 1)[0]
    assert CITATION in oversized
    assert "stories.md" not in SCAN.read_text(), "the scan judges no card a person wrote (D3)"
    standard = _section(skill, "## The standard — what a well-formed issue contains")
    items = re.findall(r"^(\d)\. \*\*", standard, flags=re.M)
    assert items == ["1", "2", "3", "4", "5"], "the scan keeps five structural items"


def test_fixture_46_pins_the_rule_and_supplies_no_candidate_prose():
    manifest = json.loads((FIXTURE / "manifest.json").read_text())
    assert manifest["command"] == "groom-ask"
    assert "rules/stories.md" in manifest["expected_guard"]
    # CLAUDE.md: a fixture supplies no candidate prose and asserts no word count.
    assert "suggestions" not in manifest and "candidates" not in manifest
    expected = (FIXTURE / "expected.md").read_text()
    assert not re.search(r"\b\d+\s+words\b", expected)
    assert "rules/stories.md" in expected
    assert "fixture 46" in (GROOM / "self-test" / "README.md").read_text().lower() or \
        "46-suggested-done-when" in (GROOM / "self-test" / "README.md").read_text()
