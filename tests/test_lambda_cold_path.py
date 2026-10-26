"""`skills/lambda-web-app-speed/scripts/cold-path.py`, which `/phil:lambda-web-app-speed` measures with.

Lambda logs a cold start three ways, and only one of them carries `Init Duration`. After an INIT
timeout the first `REPORT` has no `Init Duration`: the retried INIT runs inside its `Duration`. After
an invoke that timed out or crashed, Lambda resets the environment and the next `REPORT` again folds
INIT into `Duration` — a suppressed init. A count of `Init Duration` misses both, and their durations
land among the warm invokes. Both were found in a real function's logs on 2026-10-26 (V2).

This file holds the script to the three kinds, read per log stream in time order; to keeping the
folded ones out of the warm numbers; and to naming the layer that owns the cold path only from cold
starts whose split the logs record.

Written 2026-10-26, with slice 02 of `docs/feature/lambda-web-app-speed/`.
"""
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SKILL_DIR = REPO / "skills" / "lambda-web-app-speed"
SCRIPT = SKILL_DIR / "scripts" / "cold-path.py"
RECORDED = SKILL_DIR / "self-test" / "01-cold-path-split" / "events.json"


def _module():
    spec = importlib.util.spec_from_file_location("cold_path", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _report(stream, t, duration, init=None, status=None, memory=1769):
    message = (f"REPORT RequestId: r{t}\tDuration: {duration:.2f} ms\tBilled Duration: {int(duration) + 1} ms"
               f"\tMemory Size: {memory} MB\tMax Memory Used: 160 MB\t")
    if init is not None:
        message += f"Init Duration: {init:.2f} ms\t"
    if status:
        message += f"Status: {status}\n"
    return {"logStreamName": stream, "timestamp": t, "message": message}


def _init_report(stream, t, duration, status="timeout"):
    return {"logStreamName": stream, "timestamp": t,
            "message": f"INIT_REPORT Init Duration: {duration:.2f} ms\tPhase: init\tStatus: {status}\n"}


def _summary(events):
    m = _module()
    return m.summarize(m.load({"events": events}))


def test_a_report_with_init_duration_is_a_cold_start_and_the_rest_are_warm():
    s = _summary([_report("a", 1, 120.0, init=900.0), _report("a", 2, 20.0), _report("a", 3, 30.0)])
    assert s["invokes"] == 3
    assert s["cold"]["recorded"] == 1
    assert s["init"]["p50"] == 900.0 and s["first_invoke"]["p50"] == 120.0
    assert s["warm"]["count"] == 2


def test_the_report_after_an_init_timeout_is_cold_though_it_has_no_init_duration():
    s = _summary([_init_report("a", 1, 9999.95), _report("a", 2, 2004.21), _report("a", 3, 18.0)])
    assert s["cold"]["after_failed_init"] == 1
    assert s["init_failures"] == {"timeout": 1, "error": 0}
    assert s["warm"]["count"] == 1, "the retried INIT's duration must stay out of the warm numbers"


def test_the_report_after_a_failed_invoke_in_the_same_stream_is_a_suppressed_init():
    s = _summary([
        _report("a", 1, 100.0, init=1000.0),
        _report("a", 2, 29000.0, status="timeout"),
        _report("b", 3, 40.0),  # another environment: its order says nothing about stream a
        _report("a", 4, 5237.66),
        _report("a", 5, 30.0),
    ])
    assert s["cold"]["suppressed"] == 1
    assert s["invoke_failures"] == 1
    assert s["warm"]["count"] == 3  # the failed invoke itself was warm


def test_an_init_that_errored_is_counted_apart_from_one_that_timed_out():
    s = _summary([_init_report("a", 1, 412.0, status="error"), _report("a", 2, 900.0)])
    assert s["cold"]["after_failed_init"] == 1
    assert s["init_failures"] == {"timeout": 0, "error": 1}
    assert s["owner"]["init_ms"] == 412.0, "a failed INIT counts its logged duration"


def test_a_report_line_with_no_duration_is_skipped_not_a_crash():
    malformed = {"logStreamName": "a", "timestamp": 1, "message": "REPORT RequestId: x\tBilled Duration: 3 ms"}
    s = _summary([malformed, _report("a", 2, 20.0)])
    assert s["invokes"] == 1


def test_streams_are_read_in_time_order_whatever_order_the_file_holds():
    s = _summary([_report("a", 4, 5237.66), _report("a", 2, 29000.0, status="timeout"),
                  _report("a", 1, 100.0, init=1000.0)])
    assert s["cold"]["suppressed"] == 1


def test_a_successful_init_report_is_not_a_cold_start_a_person_waited_for():
    """Provisioned concurrency and SnapStart log INIT_REPORT for inits done ahead of any request."""
    s = _summary([_init_report("a", 1, 1500.0, status="success"), _report("a", 2, 20.0)])
    assert s["cold"]["total"] == 0 and s["init_failures"] == {"timeout": 0, "error": 0}


def test_percentiles_are_nearest_rank_the_value_a_line_carries():
    """V2: Logs Insights' pct() matched nearest rank exactly over 96 INIT durations."""
    m = _module()
    assert m.percentile([1152.56, 2199.98, 8066.70, 8936.06], 50) == 2199.98
    assert m.percentile([1152.56, 2199.98, 8066.70, 8936.06], 95) == 8936.06
    assert m.percentile([5.0], 95) == 5.0


def test_the_owner_is_named_only_from_cold_starts_whose_split_is_recorded():
    s = _summary([
        _report("a", 1, 3000.0, init=500.0),
        _report("b", 2, 2500.0, init=400.0),
        _init_report("c", 3, 10000.0), _report("c", 4, 9000.0),
    ])
    # First invoke 5.5 s against INIT 0.9 s + the 10 s that timed out: INIT owns it.
    assert s["owner"]["layer"] == "INIT"
    assert s["owner"]["unsplit_ms"] == 9000.0, "the retried INIT and its invoke are one number"


def test_the_first_invoke_owns_the_path_when_the_handler_outweighs_init():
    s = _summary([_report("a", 1, 9072.70, init=1213.69), _report("b", 2, 2895.97, init=1342.13)])
    assert s["owner"]["layer"] == "first invoke"


def test_the_layer_to_look_inside_is_init_when_init_hit_its_ceiling():
    s = _summary([_report("a", 1, 9000.0, init=500.0), _init_report("b", 2, 10000.0), _report("b", 3, 2000.0)])
    assert s["look_inside"]["layer"] == "INIT"
    assert "10 s ceiling 1 time" in s["look_inside"]["because"]


def test_the_layer_cannot_be_named_when_unsplit_time_outweighs_the_owner():
    s = _summary([_report("a", 1, 100.0, init=900.0), _report("a", 2, 29000.0, status="timeout"),
                  _report("a", 3, 6000.0)])
    assert s["look_inside"]["layer"] is None
    assert "1 failed invoke" in s["look_inside"]["because"]


def test_the_layer_is_the_owner_otherwise():
    s = _summary([_report("a", 1, 9072.70, init=1213.69), _report("b", 2, 40.0)])
    assert s["look_inside"]["layer"] == "first invoke"


def test_no_cold_start_names_no_layer():
    s = _summary([_report("a", 1, 40.0)])
    assert s["look_inside"]["layer"] is None
    assert "no cold start" in s["look_inside"]["because"]


def test_more_than_one_memory_size_in_the_window_is_reported():
    s = _summary([_report("a", 1, 20.0, memory=1024), _report("b", 2, 20.0, memory=1769)])
    assert s["memory_sizes"] == [1024, 1769]


def test_application_lines_are_ignored():
    s = _summary([{"logStreamName": "a", "timestamp": 1, "message": "INFO report ready: REPORT RequestId"},
                  _report("a", 2, 20.0)])
    assert s["invokes"] == 1


def _run(*args, stdin=None):
    return subprocess.run([sys.executable, str(SCRIPT), *args], input=stdin, capture_output=True, text=True)


def test_json_log_format_is_refused_rather_than_read_as_no_cold_starts(tmp_path):
    f = tmp_path / "events.json"
    f.write_text(json.dumps({"events": [{"logStreamName": "a", "timestamp": 1,
                                         "message": '{"time":"x","type":"platform.report","record":{}}'}]}))
    result = _run(str(f))
    assert result.returncode == 1 and "JSON log format" in result.stderr


def test_snapstart_restores_are_refused_rather_than_counted_warm(tmp_path):
    line = _report("a", 1, 120.0)
    line["message"] = line["message"].rstrip("\t") + "\tRestore Duration: 300.00 ms\tBilled Restore Duration: 120 ms\t"
    f = tmp_path / "events.json"
    f.write_text(json.dumps({"events": [line]}))
    result = _run(str(f))
    assert result.returncode == 1 and "SnapStart" in result.stderr


def test_a_fetch_stopped_by_its_item_cap_is_named_with_where_it_stopped(tmp_path):
    f = tmp_path / "events.json"
    f.write_text(json.dumps({"events": [_report("a", 1792873799277, 20.0, init=800.0)], "NextToken": "abc"}))
    result = _run(str(f))
    assert result.returncode == 0
    assert "truncated" in result.stdout and "2026-10-24T" in result.stdout


def test_a_cut_off_response_says_to_move_the_start_later(tmp_path):
    f = tmp_path / "events.json"
    f.write_text('{"events": [{"logStreamName": "a", "timest')
    result = _run(str(f))
    assert result.returncode == 1 and "start later" in result.stderr


def test_the_window_starts_at_the_last_change_when_that_is_recent():
    result = _run("--window", "2026-10-26T14:37:09.000+0000", "--now", "2026-10-26T18:00:00Z")
    w = json.loads(result.stdout)
    assert w["start_ms"] == 1793025429000 and w["end_ms"] == 1793037600000
    assert w["starts_at"] == "last change"


def test_the_window_is_fourteen_days_when_the_last_change_is_older():
    result = _run("--window", "2026-09-01T00:00:00.000+0000", "--now", "2026-10-26T18:00:00Z")
    w = json.loads(result.stdout)
    assert w["start_ms"] == 1793037600000 - 14 * 86400 * 1000
    assert w["starts_at"] == "14 days ago"


def test_no_report_line_is_an_error_not_an_empty_report(tmp_path):
    f = tmp_path / "events.json"
    f.write_text(json.dumps({"events": []}))
    result = _run(str(f))
    assert result.returncode == 1 and "no REPORT line" in result.stderr


def test_it_reads_the_cli_output_from_stdin():
    result = _run("-", stdin=json.dumps({"events": [_report("a", 1, 20.0, init=800.0)]}))
    assert result.returncode == 0, result.stderr


# --- the recorded fixture: real lines from one function, 2026-10-21 and 2026-10-24 -----------

def test_the_recorded_lines_yield_the_expected_split():
    m = _module()
    s = m.summarize(m.load(json.loads(RECORDED.read_text())))
    assert s["invokes"] == 29
    assert s["cold"] == {"recorded": 4, "after_failed_init": 2, "suppressed": 2, "total": 8}
    assert s["init_failures"] == {"timeout": 2, "error": 0} and s["invoke_failures"] == 2
    assert s["warm"]["count"] == 21
    assert s["init"]["p50"] == 2199.98 and s["init"]["p95"] == 8936.06
    assert s["first_invoke"]["p50"] == 127.53 and s["first_invoke"]["p95"] == 4874.40
    assert s["owner"]["layer"] == "INIT"
    assert s["look_inside"]["layer"] == "INIT"
    assert s["memory_sizes"] == [1024, 1769]


def test_the_report_names_each_hidden_kind_of_cold_start():
    result = _run(str(RECORDED))
    assert result.returncode == 0, result.stderr
    for phrase in ("after a failed INIT", "suppressed init", "INIT owns the cold path", "1024 MB and 1769 MB",
                   "Look inside: INIT", "p95 is the max"):
        assert phrase in result.stdout, phrase


def test_a_window_of_given_days_ignores_the_last_change():
    """The wider window the skill measures when too few cold starts followed the last change."""
    result = _run("--days", "30", "--now", "2026-10-26T18:00:00Z")
    w = json.loads(result.stdout)
    assert w["start_ms"] == 1793037600000 - 30 * 86400 * 1000
    assert w["starts_at"] == "30 days ago"


def test_an_init_within_a_second_of_the_ceiling_is_counted():
    """A 9.97 s INIT made its person wait almost as long as a timeout, and no other line says so."""
    s = _summary([_report("a", 1, 100.0, init=9970.0), _report("b", 2, 100.0, init=2400.0)])
    assert s["near_ceiling"] == 1
    m = _module()
    assert "1 within a second of the 10 s ceiling" in m.report(s)


def test_the_cold_wait_is_each_recorded_cold_starts_init_plus_its_first_invoke():
    """Medians do not add: the p50 of INIT plus the p50 of the first invoke is not the p50 of either's sum."""
    s = _summary([_report("a", 1, 100.0, init=3000.0), _report("b", 2, 4000.0, init=500.0),
                  _report("c", 3, 200.0, init=1000.0)])
    assert s["cold_wait"]["p50"] == 3100.0  # sums 3100, 4500, 1200
    assert "Cold wait" in _module().report(s)


def test_the_traffic_figures_warmth_is_priced_from():
    """Active hours, the most environments busy in one minute, and the time every invoke took."""
    hour = 3_600_000
    s = _summary([_report("a", 10, 100.0, init=900.0), _report("a", 20, 50.0), _report("b", 30, 30.0),
                  _report("a", 2 * hour + 5, 20.0), _report("c", 5 * hour, 40.0, init=800.0)])
    assert s["active_hours"] == 3
    assert s["peak_environments"] == 2
    assert s["duration_total_ms"] == 240.0


def test_the_window_reports_its_length_in_days_for_the_warmth_price():
    w = json.loads(_run("--window", "2026-10-26T14:37:09.000+0000", "--now", "2026-10-26T18:00:00Z").stdout)
    assert w["days"] == round((1793037600000 - 1793025429000) / 86_400_000, 4)
