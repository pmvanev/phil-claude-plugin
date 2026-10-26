"""`skills/lambda-web-app-speed/scripts/phases.py`, which reads a cold-start timing line one level below
the split `cold-path.py` makes.

The line is CloudWatch's Embedded Metric Format: one JSON record per cold start, one metric per timed
part. Its parts are of two kinds. A phase runs after the one before it, so the phases together divide
the slice. A check runs beside the others on a thread pool, so the checks overlap: on a real function
on 2026-10-26, ten checks' medians summed to 4.99 s inside a phase the clock timed at 0.92 s. Summing
them would invent four seconds. This file holds the script to adding phases, never members; to naming
the largest phase by its total time across the window; and to reporting each phase's members beside
it, unsummed.

Written 2026-10-26, with slice 03 of `docs/feature/lambda-web-app-speed/` (issue 59).
"""
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SCRIPT = REPO / "skills" / "lambda-web-app-speed" / "scripts" / "phases.py"
RECORDED = REPO / "skills" / "lambda-web-app-speed" / "self-test" / "02-init-phases" / "events.json"


def _module():
    spec = importlib.util.spec_from_file_location("phases", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _emf(t, phase="init", **metrics):
    record = {"_aws": {"Timestamp": t, "CloudWatchMetrics": [{
        "Namespace": "app", "Dimensions": [["function", "phase"]],
        "Metrics": [{"Name": name, "Unit": "Milliseconds"} for name in metrics]}]},
        "function": "api", "phase": phase, **metrics}
    return {"logStreamName": "s", "timestamp": t, "message": json.dumps(record)}


def _summary(events):
    m = _module()
    return m.summarize(m.load({"events": events}))


def _group(summary, phase="init"):
    return summary[f"function=api phase={phase}"]


def test_phases_add_up_and_members_do_not():
    g = _group(_summary([_emf(1, Import=900.0, Checks=1000.0, **{"Check.a": 950.0, "Check.b": 900.0})]))
    assert g["timed_ms"]["p50"] == 1900.0, "the code's own time is its phases, not its checks"
    assert [p["name"] for p in g["phases"]] == ["Checks", "Import"]


def test_members_sit_under_the_phase_their_prefix_names():
    g = _group(_summary([_emf(1, Import=900.0, Checks=1000.0, **{"Check.a": 950.0, "Check.accounts.rows": 10.0})]))
    checks = next(p for p in g["phases"] if p["name"] == "Checks")
    assert [m["name"] for m in checks["members"]] == ["Check.a", "Check.accounts.rows"]
    assert checks["members_concurrent"] is True


def test_the_largest_phase_is_the_one_with_most_time_across_the_window():
    """Import wins at p50 here, checks in the tail; a person pays the total."""
    events = [_emf(1, Import=1100.0, Checks=400.0), _emf(2, Import=1000.0, Checks=350.0),
              _emf(3, Import=1200.0, Checks=6000.0)]
    g = _group(_summary(events))
    assert g["largest"] == "Checks"


def test_each_set_of_dimension_values_is_its_own_group():
    s = _summary([_emf(1, Import=900.0), _emf(2, phase="first_request", Import=50.0)])
    assert set(s) == {"function=api phase=init", "function=api phase=first_request"}


def test_lines_that_are_not_emf_or_not_milliseconds_are_ignored():
    plain = {"logStreamName": "s", "timestamp": 1, "message": "INFO ColdStartImport took a while"}
    seconds = _emf(2, Import=900.0)
    record = json.loads(seconds["message"])
    record["_aws"]["CloudWatchMetrics"][0]["Metrics"][0]["Unit"] = "Seconds"
    seconds["message"] = json.dumps(record)
    assert _summary([plain, seconds]) == {}


def _run(*args):
    return subprocess.run([sys.executable, str(SCRIPT), *args], capture_output=True, text=True)


def test_a_member_waits_with_its_phase_record_by_record_not_by_two_unrelated_tails():
    """Its p95 and the phase's p95 can come from different cold starts; a shared wait shows in the same one."""
    events = [_emf(1, Checks=8000.0, **{"Check.a": 7900.0, "Check.b": 100.0}),
              _emf(2, Checks=7000.0, **{"Check.a": 6900.0, "Check.b": 200.0}),
              _emf(3, Checks=500.0, **{"Check.a": 400.0, "Check.b": 7990.0 / 16}),
              _emf(4, Checks=9000.0, **{"Check.a": 100.0, "Check.b": 8950.0})]
    checks = _group(_summary(events))["phases"][0]
    marks = {m["name"]: m["waits_with_phase"] for m in checks["members"]}
    assert marks == {"Check.a": True, "Check.b": False}


def test_a_group_with_members_and_no_phase_is_reported_not_a_crash(tmp_path):
    f = tmp_path / "events.json"
    f.write_text(json.dumps({"events": [_emf(1, **{"Api.latency": 40.0}), _emf(2, Import=900.0)]}))
    result = _run(str(f))
    assert result.returncode == 0, result.stderr
    assert "no phase" in result.stdout


def test_a_metric_with_no_name_is_skipped():
    event = _emf(1, Import=900.0)
    record = json.loads(event["message"])
    record["_aws"]["CloudWatchMetrics"][0]["Metrics"].append({"Unit": "Milliseconds"})
    event["message"] = json.dumps(record)
    assert _group(_summary([event]))["lines"] == 1


def test_a_phase_that_spans_the_others_breaks_the_convention_and_is_refused(tmp_path):
    """A total written beside its parts would be summed with them, and named the largest phase."""
    events = [_emf(t, InitTotal=a + b + 5, Import=a, Build=b) for t, a, b in ((1, 900, 400), (2, 1100, 500))]
    f = tmp_path / "events.json"
    f.write_text(json.dumps({"events": events}))
    result = _run(str(f))
    assert result.returncode == 1 and "InitTotal" in result.stderr and "convention" in result.stderr


def test_a_member_prefix_that_two_phases_share_is_named_not_guessed():
    g = _group(_summary([_emf(1, DbConnect=100.0, Dbx=50.0, **{"Db.query": 40.0})]))
    assert [m["name"] for m in g["unattached"]] == ["Db.query"]


def test_a_fetch_stopped_by_its_item_cap_is_named(tmp_path):
    f = tmp_path / "events.json"
    f.write_text(json.dumps({"events": [_emf(1792873799277, Import=900.0)], "NextToken": "x"}))
    result = _run(str(f))
    assert result.returncode == 0 and "truncated" in result.stdout and "2026-10-24T" in result.stdout


def test_the_gap_to_init_duration_is_reported_as_a_slice_of_its_own(tmp_path):
    f = tmp_path / "events.json"
    f.write_text(json.dumps({"events": [_emf(1, Import=900.0, Checks=1000.0)]}))
    result = _run(str(f), "--init-p50", "7.0", "--cold-starts", "4")
    assert result.returncode == 0, result.stderr
    assert "untimed: 5.10 s" in result.stdout, "INIT p50 7.0 s against 1.90 s the code timed"
    assert "outweighs the largest phase" in result.stdout
    assert "1 line for 4 cold starts" in result.stdout


def test_p95_over_twenty_lines_or_fewer_is_called_the_maximum():
    assert "p95 is the max" in _run(str(RECORDED)).stdout


def test_no_timing_line_is_an_error_naming_what_was_looked_for(tmp_path):
    f = tmp_path / "events.json"
    f.write_text(json.dumps({"events": []}))
    result = _run(str(f))
    assert result.returncode == 1 and "no Embedded Metric Format line" in result.stderr


# --- the recorded fixture: twelve cold-start lines from one function, 2026-10-25 and 26 --------

def test_the_recorded_lines_name_the_checks_and_keep_their_members_apart():
    m = _module()
    g = m.summarize(m.load(json.loads(RECORDED.read_text())))["function=api phase=init"]
    assert g["lines"] == 12
    phases = {p["name"]: p for p in g["phases"]}
    assert round(phases["ColdStartChecks"]["total_ms"], 2) == 35655.17
    assert round(phases["ColdStartImport"]["total_ms"], 2) == 12803.91
    assert round(phases["ColdStartBuild"]["total_ms"], 2) == 5675.85
    assert g["largest"] == "ColdStartChecks"
    assert round(phases["ColdStartImport"]["p50"], 2) == 1109.93
    assert round(g["timed_ms"]["p50"], 2) == 2329.36
    members = phases["ColdStartChecks"]["members"]
    assert len(members) == 10 and members[0]["name"] == "ColdStartCheck.accounts.reader"
    assert round(phases["ColdStartChecks"]["members_p50_sum_ms"], 2) == 4991.75


def test_the_report_says_the_members_ran_concurrently():
    result = _run(str(RECORDED))
    assert result.returncode == 0, result.stderr
    for phrase in ("Largest phase: ColdStartChecks", "66%", "ran concurrently", "4.99 s", "0.92 s"):
        assert phrase in result.stdout, phrase


def test_members_whose_tail_reaches_the_phase_are_marked_as_waiting_alike():
    """Six checks that wait with the phase while four finish within 0.21 s share a dependency: the next level
    to time."""
    m = _module()
    g = m.summarize(m.load(json.loads(RECORDED.read_text())))["function=api phase=init"]
    checks = next(p for p in g["phases"] if p["name"] == "ColdStartChecks")
    alike = sorted(x["name"].split(".", 1)[1] for x in checks["members"] if x["waits_with_phase"])
    assert alike == ["access", "accounts.reader", "accounts.rows", "database", "model_versions", "version_catalog"]
    assert "wait alike" in _run(str(RECORDED)).stdout


# --- the reference instruments the skill proposes ---------------------------------------------

import ast
import re

REFERENCES = REPO / "skills" / "lambda-web-app-speed" / "references"
SKILL = REPO / "skills" / "lambda-web-app-speed" / "SKILL.md"


def _python_blocks(path):
    return re.findall(r"```python\n(.*?)```", path.read_text(), re.S)


def test_every_reference_snippet_is_valid_python():
    for name in ("cold-start-line.md", "connection-legs.md"):
        blocks = _python_blocks(REFERENCES / name)
        assert blocks, f"{name} holds no Python"
        for block in blocks:
            ast.parse(block)


def test_the_cold_start_line_names_phases_without_a_dot_and_checks_with_one():
    text = (REFERENCES / "cold-start-line.md").read_text()
    for phase in ("ColdStartImport", "ColdStartBuild", "ColdStartChecks"):
        assert f'"{phase}"' in text
    assert 'f"ColdStartCheck.{name}"' in text, "a check must be a member of the phase its prefix names"
    m = _module()
    assert m._parent("ColdStartCheck.database", ["ColdStartBuild", "ColdStartChecks", "ColdStartImport"]) \
        == "ColdStartChecks"


def test_the_connection_legs_are_phases_the_script_adds():
    text = (REFERENCES / "connection-legs.md").read_text()
    legs = ("ConnectDns", "ConnectTcp", "ConnectTls", "ConnectToken", "ConnectSignIn", "ConnectFirstQuery")
    for leg in legs:
        assert f'"{leg}"' in text and "." not in leg


def test_each_reference_states_its_cost_at_init():
    assert "Cost at INIT" in (REFERENCES / "cold-start-line.md").read_text()
    assert "costs the function's INIT nothing" in " ".join((REFERENCES / "connection-legs.md").read_text().split())


def test_the_skill_proposes_an_instrument_only_for_an_unexplained_slice():
    body = " ".join(SKILL.read_text().split())
    for phrase in ("Look for an instrument the function already has", "references/cold-start-line.md",
                   "references/connection-legs.md", "what it costs at INIT", "the person deploys it",
                   "scripts/phases.py"):
        assert phrase in body, phrase


def test_more_lines_than_cold_starts_is_explained_too(tmp_path):
    f = tmp_path / "events.json"
    f.write_text(json.dumps({"events": [_emf(1, Import=900.0, Checks=100.0), _emf(2, Import=800.0, Checks=90.0)]}))
    result = _run(str(f), "--init-p50", "2.0", "--cold-starts", "1")
    assert "more lines than cold starts" in result.stdout


def test_a_line_of_one_undivided_phase_is_named_as_dividing_nothing(tmp_path):
    f = tmp_path / "events.json"
    f.write_text(json.dumps({"events": [_emf(1, cold_start=2400.0), _emf(2, cold_start=2500.0)]}))
    result = _run(str(f))
    assert "divides nothing" in result.stdout
