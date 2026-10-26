"""`skills/lambda-web-app-speed/scripts/rank.py`, which orders the fixes `/phil:lambda-web-app-speed` finds.

Ranked by time saved, decided 2026-10-26 (D17): the largest measured saving first, effort breaking
near-ties, the standard pattern first among equals (D13). A fix no measurement predicts — more memory,
work moved into INIT — is an experiment, listed apart. Each saving is computed by the script from a stated
basis — a call removed, calls made concurrent, a batch, a time scaled by a measured fraction — so no
range is worked out by hand. A saving inside the run-to-run noise falls below the line; the stopping line
falls where the path meets a target the project states, and nowhere when it states none.

The replay fixtures are beatrix issue 254's record at two points, each figure from a measurement taken
before the fix. Where the measurement divides the time, the real gains fell in the order estimated. The
replay is after the fact: D17 was chosen knowing this record, and no held-out case exists yet.

Written 2026-10-26, with slice 04 of `docs/feature/lambda-web-app-speed/` (issue 59).
"""
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SCRIPT = REPO / "skills" / "lambda-web-app-speed" / "scripts" / "rank.py"
REPLAY = REPO / "skills" / "lambda-web-app-speed" / "self-test" / "03-rank-replay"


def _module():
    spec = importlib.util.spec_from_file_location("rank", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _plan(candidates, now=5000, target=800, noise=300):
    return _module().plan({"path": {"name": "cold", "now_ms": now, "target_ms": target, "noise_ms": noise},
                           "candidates": candidates})


def _fix(name, lo, hi, effort="S", standard=True):
    return {"name": name, "kind": "removes", "effort": effort, "standard": standard, "evidence": "measured",
            "saves": [{"basis": "removes", "low": lo, "high": hi}]}


def _names(items):
    return [c["name"] for c in items]


def test_each_basis_turns_measured_figures_into_a_saving():
    m = _module()
    assert m.saving([{"basis": "removes", "low": 100, "high": 200}]) == (100, 200)
    assert m.saving([{"basis": "concurrent", "sum": {"low": 1210, "high": 1320},
                      "slowest": {"low": 100, "high": 285}}]) == (925, 1220)
    assert m.saving([{"basis": "batch", "calls": 5, "low": 40, "high": 60}]) == (160, 240)
    assert m.saving([{"basis": "scaled", "low": 1000, "high": 2000, "fraction": [0.4, 0.5]}]) == (400, 1000)
    assert m.saving([{"basis": "removes", "low": 100, "high": 200},
                     {"basis": "removes", "low": 50, "high": 60}]) == (150, 260)


def test_the_largest_saving_ranks_first_whatever_its_effort():
    p = _plan([_fix("bytecode", 730, 990, "S"), _fix("checks", 2130, 2470, "M")])
    assert _names(p["ranked"]) == ["checks", "bytecode"]


def test_effort_breaks_a_near_tie():
    p = _plan([_fix("slow", 1000, 1200, "L"), _fix("quick", 950, 1150, "S")])
    assert _names(p["ranked"]) == ["quick", "slow"]


def test_the_standard_pattern_goes_first_among_equals():
    p = _plan([_fix("clever", 1000, 1100, "S", standard=False), _fix("documented", 1000, 1100, "S")])
    assert _names(p["ranked"]) == ["documented", "clever"]


def test_a_fix_no_measurement_predicts_is_an_experiment_listed_by_effort():
    p = _plan([{"name": "build at INIT", "kind": "experiment", "effort": "M", "standard": True, "evidence": "x"},
               {"name": "memory", "kind": "experiment", "effort": "S", "standard": True, "evidence": "x"}])
    assert p["ranked"] == [] and _names(p["experiments"]) == ["memory", "build at INIT"]


def test_a_range_from_nothing_or_too_wide_to_rank_on_is_listed_with_its_reason():
    p = _plan([_fix("unknown", 0, 2000), _fix("wide", 300, 1500), _fix("known", 900, 1100)])
    assert _names(p["ranked"]) == ["known"]
    assert sorted(_names(p["too_wide"])) == ["unknown", "wide"]
    assert "range too wide to rank: 0.30 s to 1.50 s" in _module().report(p)


def test_a_saving_inside_the_noise_falls_below_the_line():
    p = _plan([_fix("tiny", 45, 58), _fix("real", 900, 1100)], noise=300)
    assert _names(p["ranked"]) == ["real"] and _names(p["inside_noise"]) == ["tiny"]


def test_the_stopping_line_falls_after_the_fix_that_meets_the_target():
    p = _plan([_fix("a", 2000, 2200), _fix("b", 1400, 1600), _fix("c", 900, 1100)], now=4000, target=1000)
    assert p["stop_after"] == 2 and p["reaches_target"] is True


def test_a_path_already_within_its_target_needs_no_fix():
    p = _plan([_fix("a", 2000, 2200)], now=700, target=800)
    assert p["stop_after"] == 0 and p["reaches_target"] is True
    assert "already within the target" in _module().report(p)


def test_the_report_says_when_the_ranked_fixes_cannot_reach_the_target():
    p = _plan([_fix("a", 900, 1100)], now=6000, target=800)
    assert p["reaches_target"] is False and p["stop_after"] == 1


def test_with_no_target_there_is_no_stopping_line_rather_than_a_borrowed_one():
    p = _plan([_fix("a", 900, 1100)], target=None)
    assert p["reaches_target"] is None
    assert "no target stated" in _module().report(p)


def _refused(candidate):
    f = Path(__import__("tempfile").mkdtemp()) / "c.json"
    f.write_text(json.dumps({"path": {"name": "cold", "now_ms": 5000}, "candidates": [candidate]}))
    return subprocess.run([sys.executable, str(SCRIPT), str(f)], capture_output=True, text=True)


def test_a_candidate_with_no_evidence_or_a_bad_field_is_refused():
    good = _fix("x", 1, 2)
    for broken, word in ((dict(good, evidence=""), "evidence"), (dict(good, kind="remove"), "kind"),
                         (dict(good, standard="false"), "standard"),
                         (dict(good, saves=[{"basis": "guess", "low": 1, "high": 2}]), "basis"),
                         (dict(good, saves=[{"basis": "removes", "low": 5, "high": 2}]), "low")):
        result = _refused(broken)
        assert result.returncode == 1 and word in result.stderr, (word, result.stderr)


def test_it_reads_the_candidates_from_stdin():
    spec = json.loads((REPLAY / "after-memory.json").read_text())
    result = subprocess.run([sys.executable, str(SCRIPT), "-"], input=json.dumps(spec), capture_output=True,
                            text=True)
    assert result.returncode == 0, result.stderr


# --- the replay: beatrix 254, every figure from a measurement taken before its fix ------------

def test_replay_before_the_init_move_ranks_nothing_and_lists_both_large_gains_as_experiments():
    """Building during INIT, with smaller changes, cut first byte 5.3 s, and memory 1.2-1.5 s; no
    measurement then predicted either."""
    p = _module().plan(json.loads((REPLAY / "before-init-move.json").read_text()))
    assert p["ranked"] == []
    assert _names(p["experiments"]) == ["raise memory from 512 MB to 1769 MB", "build the app during INIT"]


def test_replay_after_memory_ranks_the_largest_real_gain_first():
    """Checks saved 2.3-2.4 s off INIT, bytecode 0.69-0.86 s off imports; the estimates ranked them so."""
    m = _module()
    p = m.plan(json.loads((REPLAY / "after-memory.json").read_text()))
    assert _names(p["ranked"]) == ["startup checks run concurrently and Bedrock checked on first chat",
                                   "compiled bytecode for the runtime's Python"]
    assert m.saving(p["ranked"][0]["saves"]) == (2125, 2470)
    assert m.saving(p["ranked"][1]["saves"]) == (743.58, 1023.76)
    assert _names(p["experiments"]) == ["raise memory past 1769 MB"]
    assert sorted(_names(p["inside_noise"])) == ["drop the Secrets Manager read", "trim the app's own module imports"]
    assert p["reaches_target"] is None, "beatrix stated no cold-path budget"


def test_the_report_names_each_fix_its_range_and_its_evidence():
    result = subprocess.run([sys.executable, str(SCRIPT), str(REPLAY / "after-memory.json")],
                            capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    for phrase in ("1. startup checks", "−2.30 s", "Experiments", "Inside the noise", "note 14518"):
        assert phrase in result.stdout, phrase


def test_the_candidates_reference_names_every_basis_the_script_computes_and_no_other():
    """The skill writes candidates from the reference; a basis the script lacks is refused at run time."""
    import re
    text = (REPO / "skills" / "lambda-web-app-speed" / "references" / "candidates.md").read_text()
    documented = set(re.findall(r"^\| `(\w+)` \|", text, re.M)) - {"basis"}
    m = _module()
    for basis in documented:
        part = {"basis": basis, "low": 1, "high": 2, "calls": 2, "fraction": [0.5, 0.5],
                "sum": {"low": 3, "high": 4}, "slowest": {"low": 1, "high": 1}}
        m.saving([part])
    assert documented == {"removes", "concurrent", "batch", "scaled"}
