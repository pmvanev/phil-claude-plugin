"""Tests for slice 03's label evidence — `derive_label_evidence` in `scripts/probe-board.py`.

Slice 03 exists to make one thing impossible: **inferring whether a label family is single- or
multi-valued from the labels in use** ([D6]). Inferring it makes the board's habits audit themselves
and mints the very declaration `phil:groom-issues` rule 4 exists to read.

So the probe's job here is narrow and adversarial to itself: gather the evidence a human needs to
answer, and return **no answer**. These tests pin the boundary — every one of them is checking that
something is *absent* from the output as much as present.

The evidence is `elicitation_evidence`, deliberately not a `fact`. Facts go inside the markers; this
goes beneath a question and, once answered, outside them attributed to a human.
"""

import importlib.util
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "probe-board.py"


def load():
    spec = importlib.util.spec_from_file_location("probe_board", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


pb = load()


# This repo's real shape: three unprefixed labels that co-occur BY DECISION, plus a prefixed family
# that is single-valued on another skill's authority.
ISSUES = [
    {"number": 2, "labels": ["bug", "documentation", "enhancement"]},
    {"number": 4, "labels": ["documentation", "enhancement"]},
    {"number": 30, "labels": ["enhancement"]},
    {"number": 32, "labels": ["documentation", "enhancement", "wave: discuss"]},
    {"number": 31, "labels": ["bug"]},
]


def ev():
    return pb.derive_label_evidence(ISSUES)


# --- what it must NOT do ------------------------------------------------------------------

def test_no_family_carries_a_valuedness_verdict():
    """The whole slice. Not `single`, not `multi`, not `likely`, not a confidence score."""
    forbidden = {"single_valued", "multi_valued", "valuedness", "verdict", "likely",
                 "confidence", "inferred", "suggested_answer", "default"}
    for fam in ev()["families"]:
        assert not (set(fam) & forbidden), f"{fam.get('name')} carries a verdict: {fam}"


def test_nothing_is_preselected():
    for fam in ev()["families"]:
        assert fam.get("preselected") in (None, False)


def test_the_output_says_outright_that_it_holds_no_answer():
    e = ev()
    assert "note" in e
    assert "never" in e["note"].lower() or "not" in e["note"].lower()


# --- the evidence it must gather ----------------------------------------------------------

def test_a_prefixed_family_is_grouped_by_its_prefix():
    """`wave: discuss` groups under `wave`. This is a SYNTACTIC fact about the label's name, not an
    inference about how the family behaves."""
    fam = {f["name"]: f for f in ev()["families"]}
    assert "wave" in fam
    assert fam["wave"]["members"] == ["wave: discuss"]
    assert fam["wave"]["grouping"] == "syntactic prefix"


def test_double_colon_scoped_labels_group_too():
    """GitLab's `status::doing` convention, which slice 06 will meet."""
    e = pb.derive_label_evidence([{"number": 1, "labels": ["status::doing", "status::done"]}])
    fam = {f["name"]: f for f in e["families"]}
    assert "status" in fam
    assert sorted(fam["status"]["members"]) == ["status::doing", "status::done"]


def test_unprefixed_labels_are_offered_as_one_candidate_marked_as_such():
    """They cannot be grouped syntactically, so the grouping is explicitly a question."""
    fam = {f["name"]: f for f in ev()["families"]}
    key = next(k for k, v in fam.items() if v["grouping"] != "syntactic prefix")
    assert set(fam[key]["members"]) == {"bug", "documentation", "enhancement"}
    assert "candidate" in fam[key]["grouping"]


def test_co_occurrence_counts_are_reported_per_pair():
    fam = {f["name"]: f for f in ev()["families"]}
    key = next(k for k, v in fam.items() if v["grouping"] != "syntactic prefix")
    pairs = {tuple(p["pair"]): p["count"] for p in fam[key]["co_occurrence"]}
    # #2, #4 and #32 each carry both.
    assert pairs[("documentation", "enhancement")] == 3
    assert pairs[("bug", "documentation")] == 1


def test_the_whole_payload_is_json_serialisable():
    """The first real run died on `TypeError: keys must be str … not tuple`, because co-occurrence
    was keyed by a pair. The payload's only purpose is to be serialised and read, so a shape that
    cannot round-trip is not a detail.

    Worth recording: the pair-count test that should have caught it was written as
    `assert pairs[k] == 3 if isinstance(pairs, dict) else True`, which is vacuously true whenever
    the guard is false. A test with a conditional in its assertion can pass by not testing."""
    import json
    round_tripped = json.loads(json.dumps(ev()))
    assert round_tripped["families"]


def test_the_issues_carrying_more_than_one_are_named():
    """AC2's evidence: #2 and #4 carry more than one by decision, and a human answering the question
    needs the issue numbers to check that for themselves."""
    fam = {f["name"]: f for f in ev()["families"]}
    key = next(k for k, v in fam.items() if v["grouping"] != "syntactic prefix")
    assert 2 in fam[key]["issues_with_multiple"]
    assert 4 in fam[key]["issues_with_multiple"]
    assert 31 not in fam[key]["issues_with_multiple"], "#31 carries only `bug`"


def test_a_family_that_never_co_occurs_reports_zero_rather_than_being_dropped():
    """Absence of co-occurrence is evidence FOR single-valued, and it is the human's to weigh. A
    family dropped for having no co-occurrence would silently answer the question by omission."""
    e = pb.derive_label_evidence([{"number": 1, "labels": ["wave: discuss"]},
                                  {"number": 2, "labels": ["wave: design"]}])
    fam = {f["name"]: f for f in e["families"]}
    assert "wave" in fam
    assert fam["wave"]["issues_with_multiple"] == []


def test_label_counts_are_reported():
    fam = {f["name"]: f for f in ev()["families"]}
    key = next(k for k, v in fam.items() if v["grouping"] != "syntactic prefix")
    assert fam[key]["counts"]["enhancement"] == 4
    assert fam[key]["counts"]["bug"] == 2


def test_an_empty_board_yields_no_families_and_still_carries_the_note():
    e = pb.derive_label_evidence([])
    assert e["families"] == []
    assert e["note"]
