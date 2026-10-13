"""`skills/red-team-prose/SKILL.md`: what Step 6 may apply, and what the passes may touch.

Found 2026-10-13, all predating that day's hardening:
- The clarity pass imports `eos`'s rewrites, whose own examples insert facts ("Caches for 5 minutes",
  "We wrote tests"); nothing marked such a rewrite NEEDS YOU, and Step 6 applied it.
- Step 6 asked "Apply the 0 auto-applicable fixes?" whenever every finding needed the author.
- `ai-eos`'s formatting-tell fixes rewrite headings and markup, which `eos`'s Safety — honoured here —
  forbids, and Step 6 applied them.
- The illustrative-span exemption reached the tells pass only, so the clarity pass rewrote quoted
  examples.
- No-argument mode reviews prose with no file behind it, while Step 6 edits files.
- Directory mode handed reading to an Explore agent, whose summary cannot supply exact spans or the
  read Edit requires.
- The TELLS line had no room for why a modifier moved the verdict, and `ai-eos`'s template, which did,
  is suppressed.
- A file-and-range argument (`docs/setup.md:12-30`) had no split rule, unlike both sibling skills.
"""
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SKILL = REPO / "skills" / "red-team-prose" / "SKILL.md"


def _flat():
    return " ".join(SKILL.read_text().split())


def test_a_rewrite_that_adds_a_fact_needs_the_author():
    assert "adds a number, a name, an actor or a claim the text does not hold is `[NEEDS YOU]`" in _flat()


def test_no_ask_when_nothing_is_auto_applicable():
    assert "Ask only when at least one finding is `[auto-applicable]`" in _flat()


def test_formatting_fixes_go_to_the_author():
    assert "A formatting-tell fix is `[NEEDS YOU]`" in _flat()


def test_illustrative_spans_are_exempt_from_every_pass():
    assert "exempt from the clarity pass too" in _flat()


def test_no_argument_mode_offers_text_not_edits():
    assert "With no file behind the prose, Step 6 offers the rewritten text" in _flat()


def test_explore_agents_only_locate_files():
    body = _flat()
    assert "use an Explore agent to parallelize reading" not in body
    assert "read each file yourself before its passes" in body


def test_the_tells_line_says_why_a_modifier_moved_the_verdict():
    assert "{, moved by: <modifier and why>}" in SKILL.read_text()


def test_a_file_and_range_argument_is_split():
    assert "If the argument contains both a file and a line range" in _flat()
