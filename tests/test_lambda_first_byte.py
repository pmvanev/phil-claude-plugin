"""`skills/lambda-web-app-speed/scripts/firstbyte.py`, which divides one page load's first byte.

A person's first byte is the network — DNS, TCP, TLS — then the front door, then the function: its INIT
on a cold start, and its invoke. The script times the network legs of one GET itself, then matches the
function's `REPORT` for that request from the platform lines of its time window, and splits the first
byte three ways; what neither the client nor the `REPORT` holds is the front door's: API Gateway or the
load balancer, and Lambda placing the request. The fixture is a real cold load of a production page on
2026-10-26: first byte 4.21 s, of which INIT 3.31 s.

Written 2026-10-26, with slice 04b of `docs/feature/lambda-web-app-speed/` (issue 59).
"""
import http.server
import importlib.util
import json
import subprocess
import sys
import threading
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SCRIPT = REPO / "skills" / "lambda-web-app-speed" / "scripts" / "firstbyte.py"
FIXTURE = REPO / "skills" / "lambda-web-app-speed" / "self-test" / "05-first-byte"


def _module():
    spec = importlib.util.spec_from_file_location("firstbyte", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_one_get_is_timed_leg_by_leg():
    class Slow(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            __import__("time").sleep(0.2)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"ok")

        def log_message(self, *args):
            pass

    server = http.server.HTTPServer(("127.0.0.1", 0), Slow)
    threading.Thread(target=server.handle_request, daemon=True).start()
    get = _module().get(f"http://127.0.0.1:{server.server_port}/")
    assert get["status"] == 200 and get["tls_ms"] == 0
    assert get["wait_ms"] >= 190 and get["ttfb_ms"] >= get["wait_ms"]
    assert get["ended_ms"] >= get["started_ms"]


def test_the_first_byte_splits_into_network_function_and_front_door():
    m = _module()
    split = m.split(json.loads((FIXTURE / "get.json").read_text()), json.loads((FIXTURE / "events.json").read_text()))
    assert split["cold"] is True
    assert round(split["network_ms"], 1) == 267.6
    assert round(split["function_ms"], 2) == 3327.75
    assert round(split["front_door_ms"], 1) == 619.5


def test_a_warm_report_splits_with_no_init():
    m = _module()
    get = json.loads((FIXTURE / "get.json").read_text()) | {"ttfb_ms": 400.0}
    events = {"events": [{"logStreamName": "s", "timestamp": 1793040000390,
                          "message": "REPORT RequestId: x\tDuration: 30.00 ms\tBilled Duration: 30 ms\tMemory Size: 1769 MB\tMax Memory Used: 170 MB\t"}]}
    split = m.split(get, events)
    assert split["cold"] is False and split["function_ms"] == 30.0


def test_several_reports_in_the_window_cannot_be_told_apart():
    m = _module()
    get = json.loads((FIXTURE / "get.json").read_text())
    line = json.loads((FIXTURE / "events.json").read_text())["events"][0]
    split = m.split(get, {"events": [line, dict(line, timestamp=line["timestamp"] - 100)]})
    assert split["function_ms"] is None and "2 REPORT lines" in split["why"]


def test_the_report_names_each_slice_and_the_targets():
    result = subprocess.run([sys.executable, str(SCRIPT), "--split", (FIXTURE / "get.json").read_text(),
                             str(FIXTURE / "events.json")], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    for phrase in ("cold start", "INIT 3.31 s", "front door", "0.8 s", "one load, not the 75th percentile"):
        assert phrase in result.stdout, phrase


def test_a_report_logged_before_the_clients_start_still_matches():
    """2026-10-26: a real REPORT was stamped 285 ms before the client's start; the clocks differ."""
    m = _module()
    got = json.loads((FIXTURE / "get.json").read_text())
    warm = {"logStreamName": "s", "timestamp": got["started_ms"] - 285,
            "message": "REPORT RequestId: 24ab\tDuration: 6.97 ms\tBilled Duration: 7 ms\tMemory Size: 1769 MB\t"}
    split = m.split(got | {"ttfb_ms": 476.3}, {"events": [warm]})
    assert split["function_ms"] == 6.97


def test_the_get_names_the_window_to_fetch_so_no_one_works_it_out():
    got = json.loads((FIXTURE / "get.json").read_text())
    m = _module()
    assert m.fetch_window(got) == (got["started_ms"] - 3000, got["ended_ms"] + 3000)


def test_a_report_whose_invoke_began_before_the_get_could_not_be_this_requests():
    """A REPORT is stamped when its invoke ends; its invoke must begin after the GET began, within skew."""
    m = _module()
    got = json.loads((FIXTURE / "get.json").read_text())
    line = json.loads((FIXTURE / "events.json").read_text())["events"][0]
    early = dict(line, timestamp=got["started_ms"] + 100)  # ended 100 ms in, after an INIT of 3.3 s
    split = m.split(got, {"events": [early]})
    assert split["function_ms"] is None and "no REPORT line" in split["why"]


def test_a_split_the_figures_cannot_hold_is_refused():
    m = _module()
    got = json.loads((FIXTURE / "get.json").read_text()) | {"ttfb_ms": 1000.0}
    split = m.split(got, json.loads((FIXTURE / "events.json").read_text()))
    assert split["function_ms"] is None and "longer than the first byte" in split["why"]


def test_a_response_that_is_not_2xx_is_not_split():
    m = _module()
    got = json.loads((FIXTURE / "get.json").read_text()) | {"status": 302}
    split = m.split(got, json.loads((FIXTURE / "events.json").read_text()))
    assert split["function_ms"] is None and "302" in split["why"]


def test_the_front_door_slice_names_everything_it_holds():
    result = subprocess.run([sys.executable, str(SCRIPT), "--split", (FIXTURE / "get.json").read_text(),
                             str(FIXTURE / "events.json")], capture_output=True, text=True)
    assert "one round trip" in result.stdout and "Lambda's setup before INIT" in result.stdout
