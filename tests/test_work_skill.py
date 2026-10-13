"""`skills/work/SKILL.md`: the defects with an obvious answer, fixed 2026-10-13. The delegate-contract
redesign — who commits, what each delegate's success and failure mean — is a board card, not this file.

- FRAME offered a preservation-only basis, but the two-gate spine, VERIFY and the Safety rules all
  demanded a goal metric, so an accepted preservation-only run could never be reported done.
- Resume had no rule for zero or several initiatives under `docs/work/`, and `progress.md` did not
  exist until a wave finished, so a run stopped on its first wave left nothing to resume.
- Only the FRAME confirmation followed the decision-request standard; the skill asks four other things.
- The self-test paragraph and the evolution summary named paths in the plugin's own repository.
- The standards were named but never said to be read.
"""
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SKILL = REPO / "skills" / "work" / "SKILL.md"


def _flat():
    return " ".join(SKILL.read_text().split("---", 2)[2].split())


def _section(title):
    text = SKILL.read_text()
    return " ".join(text.split(f"## {title}", 1)[1].split("\n## ", 1)[0].split())


def test_a_preservation_only_run_can_be_done():
    assert "On an accepted preservation-only basis, the preservation floor is the only gate" in _flat()
    assert "On a preservation-only basis, skip the goal gate" in _section("VERIFY & DOCUMENT")
    assert "declared goal always" not in _section("Safety rules")


def test_resume_names_its_initiative_and_has_a_progress_file_to_read():
    body = _flat()
    assert "With several in-flight initiatives under `docs/work/`, ask which" in body
    assert "write `docs/work/<slug>/progress.md` with every wave `pending`" in _section("MAP — plan the waves")
    assert "ask before re-running the wave that stopped it" in body


def test_every_ask_follows_the_decision_request_standard():
    body = _flat()
    assert "Every question this skill puts to the developer follows" in body
    assert "${CLAUDE_PLUGIN_ROOT}/skills/shared/decision-request.md" in body


def test_paths_resolve_in_a_user_s_repository():
    """A backticked plugin path must carry the root; a bare one resolves against the user's repo."""
    body = _flat()
    assert "the plugin's existing `docs/evolution/` convention" not in body
    assert not re.findall(r"`(?:skills|commands|self-test)/", body)


def test_the_standards_are_read():
    assert "Read the standards to work under" in _flat()
