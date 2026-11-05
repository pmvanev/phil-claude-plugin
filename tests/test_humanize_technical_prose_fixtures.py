"""Structural tests for the humanize-technical-prose self-test fixtures.

Model-driven by design: whether a rewrite reads as its author's is not automatable here, and this file
does not pretend otherwise. What it checks is that each fixture is well formed, names outcomes the skill
defines, carries the inputs it claims, and that every outcome the skill defines has a fixture.

The outcome vocabulary is read from the skill's own `## Outcomes` tables, so a token added to the skill
without a fixture, or used by a fixture without a definition, fails here.
"""
import json
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
SKILL_DIR = ROOT / "skills" / "humanize-technical-prose"
SKILL = SKILL_DIR / "SKILL.md"
FIXTURES = sorted((SKILL_DIR / "self-test").glob("*/manifest.json"))
SLICES = {1, 2, 3, 4}


def _outcome_tables():
    section = SKILL.read_text().split("## Outcomes", 1)[1].split("\n## ", 1)[0]
    terminal, lines, current = set(), set(), None
    for row in section.splitlines():
        if row.startswith("| Terminal"):
            current = terminal
        elif row.startswith("| Report line"):
            current = lines
        else:
            m = re.match(r"\| `([A-Z-]+)` \|", row)
            if m and current is not None:
                current.add(m.group(1))
    return terminal, lines


TERMINAL, REPORT_LINES = _outcome_tables()


def _m(path):
    return json.loads(path.read_text())


def test_the_outcome_tables_parse():
    """An empty parse would make every test below vacuously true."""
    assert {"WROTE", "REFUSED-UNCOMMITTED"} <= TERMINAL
    assert "TELLS-LEFT" in REPORT_LINES


def test_fixtures_exist():
    assert len(FIXTURES) >= 21, f"expected the twenty-one fixtures of slices 01-04, found {len(FIXTURES)}"


def test_every_slice_has_fixtures():
    assert {_m(m)["slice"] for m in FIXTURES} == SLICES


@pytest.mark.parametrize("manifest", FIXTURES, ids=lambda p: p.parent.name)
def test_manifest_is_well_formed(manifest):
    d = _m(manifest)
    for key in ("fixture_id", "situation", "why_this_fixture_exists", "must_not", "inputs"):
        assert d.get(key), f"{manifest.parent.name} lacks {key}"
    assert d.get("slice") in SLICES
    assert (manifest.parent / "expected.md").exists()


@pytest.mark.parametrize("manifest", FIXTURES, ids=lambda p: p.parent.name)
def test_every_input_the_fixture_names_is_present(manifest):
    for name in _m(manifest)["inputs"]:
        assert (manifest.parent / name).exists(), f"{manifest.parent.name} names a missing input {name}"


@pytest.mark.parametrize("manifest", FIXTURES, ids=lambda p: p.parent.name)
def test_exactly_one_terminal_outcome_the_skill_defines(manifest):
    d = _m(manifest)
    assert len(d["expected_decision"]) == 1
    assert d["expected_decision"][0] in TERMINAL, f"{d['expected_decision'][0]} is not defined"


@pytest.mark.parametrize("manifest", FIXTURES, ids=lambda p: p.parent.name)
def test_report_lines_are_ones_the_skill_defines(manifest):
    for line in _m(manifest).get("expected_report_lines", []):
        assert line in REPORT_LINES, f"{line} is not a report line"


@pytest.mark.parametrize("manifest", FIXTURES, ids=lambda p: p.parent.name)
def test_a_fixture_supplies_inputs_never_the_rewrite(manifest):
    """The expected rewrite is the run's to produce; handing it over turns the fixture into a copy test."""
    d = _m(manifest)
    for key in ("candidates", "suggestions", "expected_output", "rewrite"):
        assert key not in d


def test_every_outcome_has_a_fixture():
    covered_terminal = {_m(m)["expected_decision"][0] for m in FIXTURES}
    covered_lines = set()
    for m in FIXTURES:
        covered_lines |= set(_m(m).get("expected_report_lines", []))
    assert TERMINAL - covered_terminal == set(), f"uncovered outcomes: {TERMINAL - covered_terminal}"
    assert REPORT_LINES - covered_lines == set(), f"uncovered report lines: {REPORT_LINES - covered_lines}"


# --- slice 01: what the fixtures must actually contain to test what they claim ---

def _fixture(name):
    return SKILL_DIR / "self-test" / name


def test_the_code_block_fixture_puts_a_tell_inside_a_code_block():
    draft = (_fixture("03-tell-in-a-code-block") / "draft.md").read_text()
    blocks = re.findall(r"```.*?```", draft, flags=re.S)
    assert any("plays a crucial role" in b for b in blocks), "the tell must sit inside the code block"
    assert "plays a crucial role" in re.sub(r"```.*?```", "", draft, flags=re.S), \
        "and once outside it, so the run has one to rewrite and one to keep"


def test_the_uncommitted_fixture_declares_its_git_state():
    assert _m(_fixture("02-uncommitted-draft") / "manifest.json")["git_state"] == "modified since the last commit"


def test_the_needs_a_fact_fixture_holds_a_phantom_attribution():
    draft = (_fixture("04-a-rewrite-that-would-add-a-tell") / "draft.md").read_text()
    assert "Experts argue that" in draft


# --- slice 04: the kinds each slips fixture expects are the ones the script draws ---

import importlib.util

_spec = importlib.util.spec_from_file_location("measure_voice", SKILL_DIR / "scripts" / "measure_voice.py")
measure_voice = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(measure_voice)

ALLOCATIONS = [
    ("16-two-slips", "11-voice-toward-formal/profile-formal.json", 2, False,
     [("substitution", "number agreement"), ("omission", "dropped article")]),
    ("18-too-few-open-positions", "11-voice-toward-formal/profile-formal.json", 3, False,
     [("substitution", "number agreement"), ("substitution", "punctuation or case"), ("omission", "dropped article")]),
    ("19-a-profile-with-no-grammar-kinds", "19-a-profile-with-no-grammar-kinds/profile-spelling.json", 2, False, []),
    ("20-residue-in-a-reworded-sentence", "20-residue-in-a-reworded-sentence/profile-residue.json", 1, False,
     [("revision residue", "doubled word")]),
    ("21-misspellings-from-the-paper", "21-misspellings-from-the-paper/profile-paper.json", 3, True,
     [("misspelling", "dropped letter"), ("misspelling", "added letter"), ("revision residue", "doubled word")]),
]


def test_the_allocation_cases_cover_every_slips_fixture_that_draws():
    drawing = {m.parent.name for m in FIXTURES
               if _m(m)["slice"] == 4 and "--slips 0" not in _m(m)["arguments"]}
    assert drawing == {name for name, *_ in ALLOCATIONS}


@pytest.mark.parametrize("name,profile,n,misspellings,expected", ALLOCATIONS, ids=[a[0] for a in ALLOCATIONS])
def test_a_slips_fixture_expects_what_the_script_draws(name, profile, n, misspellings, expected):
    """A change to the allocation that redraws a fixture's kinds would leave its expected file wrong."""
    slips = json.loads((SKILL_DIR / "self-test" / profile).read_text())["slips"]
    drawn = measure_voice.allocate(slips, n, misspellings)["slips"]
    assert [(s["class"], s["kind"]) for s in drawn] == expected
    arguments = _m(SKILL_DIR / "self-test" / name / "manifest.json")["arguments"]
    assert f"--slips {n}" in arguments
    assert ("--misspellings" in arguments) == misspellings


def test_every_profile_a_fixture_ships_passes_the_tally_check():
    profiles = list((SKILL_DIR / "self-test").glob("*/profile-*.json"))
    assert len(profiles) >= 5
    for path in profiles:
        measure_voice.check_tally(json.loads(path.read_text())["slips"])
