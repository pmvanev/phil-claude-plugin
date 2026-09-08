"""Structural tests for the nwave-wave-summary self-test fixtures.

Model-driven by design: whether a summary captured the right decisions is not automatable here, and this
file does not pretend otherwise. What it checks is that each fixture is well-formed, names outcomes the
skill defines, and that its counterexamples genuinely do what they claim.

Ships with the suite rather than after it, for the reason issue #42 records: eight suites in this repo
call themselves gates while nothing runs them, and a gate that never fires is a false negative the whole
board trusts.

The sharpest test here is `test_the_named_not_stated_counterexamples_pass_the_checker`, which asserts a
**gap**. A summary can satisfy every pattern in `scripts/plain_language.py`, sit inside the ceiling, be
entirely accurate, and still require the reader to open the artifact. Nothing mechanical catches that.
"""

import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
SKILL_DIR = ROOT / "skills" / "nwave-wave-summary"
FIXTURES = sorted((SKILL_DIR / "self-test").glob("*/manifest.json"))

TERMINAL = {"SUMMARY-RENDERED", "NOTHING-RECORDED", "TARGET-NOT-FOUND", "TARGET-AMBIGUOUS"}
REPORT_LINES = {"ARGUMENT-DROPPED", "READ-ONLY"}
CEILING = 200

_spec = importlib.util.spec_from_file_location("plain_language", ROOT / "scripts" / "plain_language.py")
plain_language = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(plain_language)
FORBIDDEN = plain_language.SUMMARY_FORBIDDEN


def _m(name):
    return json.loads((SKILL_DIR / "self-test" / name / "manifest.json").read_text())


def test_fixtures_exist():
    assert len(FIXTURES) >= 7, f"expected the seven slice-01 fixtures, found {len(FIXTURES)}"


@pytest.mark.parametrize("manifest", FIXTURES, ids=lambda p: p.parent.name)
def test_manifest_is_well_formed(manifest):
    d = json.loads(manifest.read_text())
    assert d.get("fixture_id") and d.get("situation") and d.get("why_this_fixture_exists")
    assert d.get("must_not"), f"{d['fixture_id']} forbids nothing"
    assert (manifest.parent / "expected.md").exists()


@pytest.mark.parametrize("manifest", FIXTURES, ids=lambda p: p.parent.name)
def test_exactly_one_live_terminal_outcome(manifest):
    d = json.loads(manifest.read_text())
    assert len(d["expected_decision"]) == 1
    assert d["expected_decision"][0] in TERMINAL


@pytest.mark.parametrize("manifest", FIXTURES, ids=lambda p: p.parent.name)
def test_report_lines_are_report_lines(manifest):
    d = json.loads(manifest.read_text())
    for line in d.get("expected_report_lines", []):
        assert line in REPORT_LINES, f"{line} is not a report line"
    assert "READ-ONLY" in d.get("expected_report_lines", []), "claimed on every run"


def test_every_outcome_has_a_fixture():
    covered = {json.loads(m.read_text())["expected_decision"][0] for m in FIXTURES}
    assert TERMINAL - covered == set(), f"uncovered outcomes: {TERMINAL - covered}"
    lines = set()
    for m in FIXTURES:
        lines |= set(json.loads(m.read_text()).get("expected_report_lines", []))
    assert REPORT_LINES - lines == set(), f"uncovered report lines: {REPORT_LINES - lines}"


# --- the vocabulary half, and the gap beside it ---

def test_the_summary_list_is_the_strictest_one():
    """This surface has no column for a card number, so unlike the board read it forbids that class too."""
    names = {n for n, _ in FORBIDDEN}
    board = {n for n, _ in plain_language.BOARD_DESCRIPTION_FORBIDDEN}
    assert "an issue or ticket number" in names
    assert names == board | {"an issue or ticket number"}


def test_the_handle_counterexample_carries_forbidden_classes():
    text = _m("04-handles-everywhere")["counterexamples"]["keyed_on_handles"]
    found = plain_language.identifiers_in(text, forbid=FORBIDDEN)
    assert set(found) == {"a bare decision handle", "a bracketed identifier",
                          "a file path", "an issue or ticket number"}


def test_the_permitted_example_passes():
    text = _m("04-handles-everywhere")["permitted_examples"]["stated"]
    assert plain_language.identifiers_in(text, forbid=FORBIDDEN) == []


def test_the_longhand_escape_is_invisible_to_the_checker():
    """Spelling a handle out defeats the pattern while saying nothing more. Asserted as a GAP: the rule
    covering it is prose, and the fixture's `must_not` is the only thing enforcing it."""
    d = _m("04-handles-everywhere")
    assert plain_language.identifiers_in(d["counterexamples"]["laundered"], forbid=FORBIDDEN) == []
    assert any("longhand" in c for c in d["must_not"])


def test_the_named_not_stated_counterexamples_pass_the_checker():
    """The gap this whole fixture exists for. Both counterexamples are clean by every mechanical rule,
    sit well inside the ceiling, are entirely accurate, and defeat the command's purpose.

    If either ever fails the checker, the checker has grown a rule nobody reasoned about — and this test
    is what would say so."""
    d = _m("06-named-not-stated")
    for key, text in d["counterexamples"].items():
        assert plain_language.identifiers_in(text, forbid=FORBIDDEN) == [], \
            f"{key} is caught by a pattern; this fixture is about what patterns cannot see"
        assert plain_language.over_ceiling(text, CEILING) is None, \
            f"{key} must fail on being unstated, never on length"


@pytest.mark.parametrize("manifest", FIXTURES, ids=lambda p: p.parent.name)
def test_counterexamples_are_forbidden_outputs_not_candidates(manifest):
    d = json.loads(manifest.read_text())
    if "counterexamples" in d or "permitted_examples" in d:
        assert d.get("must_not")
    if "permitted_examples" in d:
        assert d.get("counterexamples"), f"{d['fixture_id']} shows a pass with no matching failure"
    assert "candidates" not in d and "suggestions" not in d


def test_the_largest_artifact_fixture_really_is_the_largest():
    """A compression fixture sized below the real corpus tests nothing. Checked against the repo rather
    than trusted, because the corpus grew 22,000 words in the four days before this feature started."""
    biggest = max(len(p.read_text().split())
                  for p in (ROOT / "docs" / "feature").glob("*/feature-delta.md"))
    claimed = _m("01-the-largest-artifact")["artifact_words"]
    assert claimed >= biggest * 0.9, (
        f"RE-MEASURE THE FIXTURE: it claims {claimed} words and the largest real artifact is now "
        f"{biggest}. This is not a defect in the skill — the corpus grew, and a compression fixture "
        f"below the real corpus stops testing the compression. Update `artifact_words`.")



def test_the_provenance_line_names_a_feature_and_not_a_path():
    """The one line every run must print, and an earlier draft required it in a form the skill's own
    vocabulary rule forbids: `feature-delta.md` matches the file-path pattern. There is no exemption —
    the fix was to name the feature instead, and this pins both halves."""
    d = _m("01-the-largest-artifact")
    assert plain_language.identifiers_in(d["permitted_examples"]["provenance"], forbid=FORBIDDEN) == []
    assert plain_language.identifiers_in(
        d["counterexamples"]["provenance_by_path"], forbid=FORBIDDEN) == ["a file path"]


def test_a_missing_target_never_lands_on_a_claim_about_the_work():
    """`NOTHING-RECORDED` says the stage decided nothing. Reaching it from a typo is fixture 02's own
    failure by another route, and outcome-coverage cannot see it: that test quantifies over outcomes,
    and this gap was a class of INPUT landing on the wrong one."""
    d = _m("07-named-target-missing")
    assert d["expected_decision"] == ["TARGET-NOT-FOUND"]
    assert any("NOTHING-RECORDED" in c for c in d["must_not"])
    assert any("TARGET-AMBIGUOUS" in c for c in d["must_not"])


def test_fixture_06_does_not_hand_the_run_its_own_answer():
    """A permitted example covering the same decisions as the counterexamples is candidate prose on the
    one fixture whose subject is whether the run states rather than names. The driver's candidate guard
    is keyed on key names and cannot see it, so the separation is asserted here."""
    d = _m("06-named-not-stated")
    stated = d["permitted_examples"]["stated"].lower()
    for word in ("two hundred words", "most recently touched"):
        assert word not in stated, (
            f"the permitted example answers this fixture's own counterexamples ({word!r}); "
            f"choose a decision the counterexamples do not cover")
