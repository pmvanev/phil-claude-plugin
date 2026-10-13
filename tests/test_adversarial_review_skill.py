"""`skills/adversarial-review/SKILL.md` must agree with the two agents it drives and with itself.

Found 2026-10-13, all predating that day's hardening:
- VERIFY said the judge "defaults to `refuted` when it cannot independently confirm" and dropped every
  refute. `agents/adversarial-verifier.md` (since 3a68293) tries to confirm charitably first, refutes on
  uncertainty only as a last resort, and marks that refute so "the orchestrator can flag low-confidence
  refutes for a second look". The skill counted them away with confident refutes.
- PRESENT had no wording for a review whose every finding the judge refuted.
- FRAME's standards line named `eos`, a skill, and left out architecture and test-patterns, which the
  opening paragraph lists.
- ORACLE and the reviewer agent counted "self-test pass" as deterministic, though some suites, this
  skill's own among them, are driven by a model.
- Invariant 1 said the reviewer gets target, intent and standards "only", while CURATE passes the
  oracle result too.
"""
import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SKILL_DIR = REPO / "skills" / "adversarial-review"
SKILL = SKILL_DIR / "SKILL.md"
SELF_TEST = SKILL_DIR / "self-test"
VERIFIER = REPO / "agents" / "adversarial-verifier.md"
REVIEWER = REPO / "agents" / "adversarial-reviewer.md"


def _flat(path):
    return " ".join(path.read_text().split())


def _section(title):
    text = SKILL.read_text()
    return " ".join(text.split(f"## {title}", 1)[1].split("\n## ", 1)[0].split())


def test_the_verifier_still_marks_an_uncertainty_refute():
    """The premise the skill's filter rests on; if the agent drops it, the filter has nothing to read."""
    verifier = _flat(VERIFIER)
    assert "neither side is the default" in verifier
    assert "flag low-confidence refutes for a second look" in verifier


def test_verify_describes_the_judge_as_the_verifier_does():
    verify = _section("VERIFY")
    assert "defaults to `refuted` when it cannot independently confirm" not in verify
    assert "tries to confirm charitably, then to refute" in verify


def test_every_refute_is_either_listed_or_dropped_and_counted():
    """No confidence threshold exists to split on, so the filter sorts by the judge's basis: either
    branch catches every refute."""
    verify = _section("VERIFY")
    assert "Sort every `refuted` finding by the judge's `basis`" in verify
    assert "could not be confirmed either way" in verify
    assert "**Drop** every other refuted finding, and count it" in verify
    assert "could not be confirmed either way" in _section("PRESENT")


def test_all_refuted_excludes_the_uncertain():
    assert "refuted every finding and none is uncertain" in _section("VERIFY")
    assert "refuted all of them and none is uncertain" in _section("PRESENT")


def test_frame_maps_code_and_prose_to_real_rules():
    frame = _section("FRAME")
    assert not re.search(r"\beos\b", frame)
    code = re.search(r"code → (.*?); prose →", frame).group(1)
    for rule in ("coding.md", "testing.md", "architecture.md", "test-patterns.md"):
        assert rule in code, rule
    assert "`writing.md`" in re.search(r"prose → (.*?);", frame).group(1)


def test_a_model_driven_fixture_suite_is_no_oracle_in_skill_or_agent():
    assert "a fixture suite a model drives is not one" in _section("ORACLE").lower()
    assert "A fixture suite a model drives is judgment, not an oracle" in _flat(REVIEWER)


def test_invariant_one_admits_the_oracle_result():
    assert "the target, intent, standards and any `oracle_result` **only**" in _section("Invariants")


def test_every_fixture_is_listed_in_the_readme_and_the_skill():
    fixtures = sorted(p.name for p in SELF_TEST.iterdir() if p.is_dir() and p.name[:2].isdigit())
    readme = (SELF_TEST / "README.md").read_text()
    listed = _section("Self-test (regression gate)")
    for name in fixtures:
        outcome = json.loads((SELF_TEST / name / "manifest.json").read_text())["expected_outcome"]
        assert f"`{name}/`" in readme, name
        assert f"`{outcome}`" in readme, outcome
        assert re.search(rf"\({name[:2]}[,)]", listed), name
