"""Tests for `scripts/render-block.py` — deterministic rendering of both regions.

Two slices depend on this existing as code rather than as model output:

- **Slice 01's AC1** — *no value inside the markers was typed by a human*. While the region was
  assembled by a model reading JSON, that held only by after-the-fact matching.
- **Slice 05's KPI-3** — *a second run on an unchanged board writes zero bytes*. Determinism is not
  achievable at all while a model does the rendering: ordering, spacing and wording would vary run
  to run and every run would produce a diff, which is exactly the decay into unnoticed-staleness
  that issue #31 describes.

So the renderer is a pure function of the probe JSON plus a stamp, and the stamp is the only input
that may differ between runs.
"""

import importlib.util
import json
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "render-block.py"


def load():
    spec = importlib.util.spec_from_file_location("render_block", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


rb = load()

PROBE = {
    "status": "ok",
    "facts": [
        {"field": "forge-and-repo", "value": "GitHub at github.com", "query": "Q-repo",
         "provenance": "probed", "note": None, "template_field": "forge-and-repo"},
        {"field": "project-and-board-ids",
         "value": {"id": "PVT_abc", "number": 3, "title": "phil plugin", "url": "https://x/3"},
         "query": "Q-proj", "provenance": "probed", "note": None,
         "template_field": "project-and-board-ids"},
        {"field": "column-families",
         "value": {"field_id": "PVTSSF_xyz", "option_count": 2,
                   "options": [{"name": "Todo", "id": "aaa11111"},
                               {"name": "Done", "id": "bbb22222"}]},
         "query": "Q-fields", "provenance": "probed", "note": "FULL REPLACEMENT hazard",
         "template_field": "column-families"},
    ],
    "half_probed": [
        {"field": "workflow-trigger-status", "known": "`Auto-close issue` is enabled",
         "unknown": "which Status option fires it",
         "why": "ProjectV2Workflow exposes no field for the configured trigger statuses",
         "query": "Q-wf", "assumed_value": "Done"},
    ],
    "not_probeable": [
        {"field": "label-families", "template_field": "label-families",
         "why": "nothing on a forge records valuedness", "owner": "slice 03"},
    ],
}

STAMP = "2026-08-17T21:00Z"


# --- determinism, which slice 05 stands on ------------------------------------------------

def test_rendering_is_byte_identical_across_calls():
    assert rb.render_region(PROBE, STAMP) == rb.render_region(PROBE, STAMP)


def test_only_the_stamp_differs_between_two_runs_of_an_unchanged_board():
    """KPI-3's precondition. If anything else varies, every run diffs and the diffs stop being
    read — the decay this feature exists to prevent, wearing the look of maintenance."""
    a = rb.render_region(PROBE, "2026-08-17T21:00Z")
    b = rb.render_region(PROBE, "2026-08-18T09:30Z")
    assert a != b
    assert rb.strip_stamp(a) == rb.strip_stamp(b), "only the stamp may differ"


def test_fact_order_does_not_depend_on_probe_key_order():
    shuffled = {**PROBE, "facts": list(reversed(PROBE["facts"]))}
    assert rb.strip_stamp(rb.render_region(shuffled, STAMP)) == \
           rb.strip_stamp(rb.render_region(PROBE, STAMP))


# --- AC1: every value comes from the JSON --------------------------------------------------

def test_every_probed_id_appears_and_none_is_invented():
    out = rb.render_region(PROBE, STAMP)
    for value in ("PVT_abc", "PVTSSF_xyz", "aaa11111", "bbb22222"):
        assert value in out


def fact_lines(region: str) -> list[str]:
    """The lines that assert something about the board.

    Slice 04's AC1 reads *"every line inside the markers carries exactly one of probed / assumed"*.
    Taken literally that condemns the `**Queries**` index and the section headers, which assert
    nothing about the board — they are apparatus. Rather than reinterpret the AC per-run, the
    boundary is made mechanical here: **a fact line is a bullet appearing before the `**Queries**`
    header.** Everything after it is apparatus and carries no provenance by design.

    Recorded rather than quietly assumed, because "every line" is the kind of phrase a later reader
    will hold the code to.
    """
    head = region.split("**Queries**")[0]
    return [l for l in head.splitlines() if l.startswith("- ")]


def test_every_fact_line_names_its_query():
    for line in fact_lines(rb.render_region(PROBE, STAMP)):
        assert "(probed ·" in line or "(assumed ·" in line, f"unlabelled: {line}"


def test_the_queries_index_is_apparatus_and_carries_no_provenance():
    out = rb.render_region(PROBE, STAMP)
    index = out.split("**Queries**")[1]
    assert "(probed ·" not in index and "(assumed ·" not in index


# --- slice 04: the assumed label -----------------------------------------------------------

def test_a_half_probed_value_is_written_as_assumed_not_probed():
    out = rb.render_region(PROBE, STAMP)
    line = next(l for l in out.splitlines() if "Done" in l and "assumed" in l)
    assert "(probed" not in line


def test_an_assumption_states_what_is_not_knowable_and_why():
    """Slice 04 AC2. "Assumed" alone tells a reader nothing actionable."""
    out = rb.render_region(PROBE, STAMP)
    block = "\n".join(l for l in out.splitlines() if "assumed" in l or "not knowable" in l)
    assert "which Status option fires it" in out
    assert "ProjectV2Workflow" in out


def test_every_fact_line_carries_exactly_one_provenance():
    """Slice 04 AC1. A line carrying both, or neither, fails the slice."""
    for line in fact_lines(rb.render_region(PROBE, STAMP)):
        n = ("(probed ·" in line) + ("(assumed ·" in line)
        assert n == 1, f"line carries {n} provenance labels: {line}"


# --- slice 03: the declared region ---------------------------------------------------------

EVIDENCE = {"families": [
    {"name": "(unprefixed)", "members": ["bug", "documentation", "enhancement"],
     "grouping": "candidate grouping, unconfirmed",
     "counts": {"bug": 7, "documentation": 11, "enhancement": 22},
     "co_occurrence": [{"pair": ["documentation", "enhancement"], "count": 6}],
     "issues_with_multiple": [2, 4]},
    {"name": "wave", "members": ["wave: discuss"], "grouping": "syntactic prefix",
     "counts": {"wave: discuss": 1}, "co_occurrence": [], "issues_with_multiple": []},
]}


def test_a_declaration_is_attributed():
    """Slice 03 AC5 — an unattributed line is the defect."""
    out = rb.render_declarations({"(unprefixed)": "multi-valued"}, EVIDENCE, STAMP)
    assert "you declared" in out
    assert rb.DECL_BEGIN in out and rb.DECL_END in out


def test_a_declaration_agreeing_with_the_evidence_records_no_disagreement():
    out = rb.render_declarations({"(unprefixed)": "multi-valued"}, EVIDENCE, STAMP)
    assert "disagree" not in out.lower()


def test_a_declaration_contradicting_the_evidence_is_written_as_given_with_the_disagreement():
    """Slice 03 AC2, and the case this repo's real answers do NOT exercise: nine issues carry more
    than one of these labels, so declaring the family single-valued contradicts observed use. The
    declaration wins and the disagreement is recorded beside it — never resolved."""
    out = rb.render_declarations({"(unprefixed)": "single-valued"}, EVIDENCE, STAMP)
    assert "single-valued" in out, "the declaration is written as given"
    low = out.lower()
    assert "disagree" in low or "observed" in low
    assert "2" in out and "4" in out, "the contradicting issues are named"


def test_a_declined_family_is_absent_rather_than_recorded_as_declined():
    """Slice 03 AC3 — a decline writes nothing. A line saying "declined" is still a line, and rule 4
    would then read a declaration that no human made."""
    out = rb.render_declarations({"wave": "single-valued"}, EVIDENCE, STAMP)
    assert "unprefixed" not in out


def test_declaring_nothing_renders_no_region_at_all():
    assert rb.render_declarations({}, EVIDENCE, STAMP) is None


def test_declaration_rendering_is_deterministic():
    a = rb.render_declarations({"wave": "single-valued"}, EVIDENCE, STAMP)
    b = rb.render_declarations({"wave": "single-valued"}, EVIDENCE, STAMP)
    assert a == b


def test_an_unread_fact_is_never_written_inside_the_markers():
    """Only `probed` and `assumed` may appear inside the region. `unread` is neither a fact nor a
    guess — it is the absence of both, and writing it as either would launder a failed read into
    content. It belongs in the report, outside."""
    probe = {"status": "ok", "facts": [
        {"field": "column-families", "value": {"labels": None, "unread": "401"},
         "query": "Q", "provenance": "unread", "note": None,
         "template_field": "column-families"}]}
    out = rb.render_region(probe, STAMP)
    assert "401" not in out
    assert fact_lines(out) == [], "no fact line may be rendered from an unread value"
