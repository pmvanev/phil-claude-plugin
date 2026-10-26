"""`skills/lambda-web-app-speed/scripts/warmth.py`, which prices keeping a Lambda function warm.

Keeping warm is a purchase (Principle 9, D9), priced for the app's own traffic. The script reads the
traffic `cold-path.py --json` reports — invokes, cold starts, active hours, the most environments busy in
one minute, the time every invoke took — and prices each option per month from AWS's public price list
for the function's Region: provisioned concurrency for one environment and for the measured peak;
SnapStart where the runtime and partition offer it; a heartbeat from open pages. Each option says what
it removes, and what a removed cold start costs.

The fixtures are AWS's price lists for us-gov-west-1 (whole) and us-east-1 (trimmed to the six prices
used), published 2026-10-22, and fourteen days of a real web API's traffic. The arithmetic follows AWS's
pricing page, read 2026-10-26: provisioned concurrency bills the memory configured for every second it is
on, and invocation time at its own rate; SnapStart bills a cache charge on the memory allocated for every
second the version is active, and the memory allocated for each restore.

Written 2026-10-26, with slice 04b of `docs/feature/lambda-web-app-speed/` (issue 59).
"""
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
SCRIPT = REPO / "skills" / "lambda-web-app-speed" / "scripts" / "warmth.py"
FIXTURE = REPO / "skills" / "lambda-web-app-speed" / "self-test" / "04-warmth-prices"
TRAFFIC = json.loads((FIXTURE / "traffic-14d.json").read_text())
GB = 1769 / 1024
MONTH_S = 730 * 3600
SCALE = 730 / (14 * 24)


def _module():
    spec = importlib.util.spec_from_file_location("warmth", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _prices(region):
    m = _module()
    return m.read_prices(json.loads((FIXTURE / f"prices-{region}.json").read_text()))


def _options(region, runtime="python3.12", **kw):
    m = _module()
    return {o["name"]: o for o in m.price(TRAFFIC, _prices(region), region=region, memory_mb=1769,
                                         runtime=runtime, window_days=14, **kw)}


def test_the_price_list_yields_the_six_prices_warmth_needs():
    p = _prices("us-east-1")
    assert p["request"] == 2e-7 and p["duration"] == 1.66667e-5
    assert p["provisioned"] == 4.1667e-6 and p["provisioned_duration"] == 9.7222e-6
    assert p["snapstart_cache"] == 1.5046e-6 and p["snapstart_restore"] == 1.397998e-4


def test_govcloud_has_no_snapstart_price_and_the_option_says_so():
    assert _prices("us-gov-west-1").get("snapstart_cache") is None
    snap = _options("us-gov-west-1")["SnapStart"]
    assert snap["available"] is False and "GovCloud" in snap["why"]


def test_provisioned_concurrency_for_one_environment_bills_its_memory_all_month():
    pc = _options("us-gov-west-1")["provisioned concurrency, 1 environment"]
    idle = GB * MONTH_S * 5.2729e-6
    delta = TRAFFIC["duration_total_ms"] / 1000 * SCALE * GB * (1.23033e-5 - 1.66667e-5)
    assert pc["monthly_usd"] == pytest.approx(idle + delta, abs=0.01)
    assert round(pc["monthly_usd"]) == 24


def test_provisioned_concurrency_for_the_measured_peak_multiplies_it():
    o = _options("us-gov-west-1")
    peak = o["provisioned concurrency, 4 environments (the peak)"]
    assert peak["monthly_usd"] == pytest.approx(4 * GB * MONTH_S * 5.2729e-6
                                                 + TRAFFIC["duration_total_ms"] / 1000 * SCALE * GB
                                                 * (1.23033e-5 - 1.66667e-5), abs=0.01)


def test_snapstart_bills_its_cache_all_month_and_each_restore():
    snap = _options("us-east-1")["SnapStart"]
    cold_per_month = TRAFFIC["cold"]["total"] * SCALE
    assert snap["available"] is True
    assert snap["monthly_usd"] == pytest.approx(GB * MONTH_S * 1.5046e-6 + cold_per_month * GB * 1.397998e-4,
                                                abs=0.01)


def test_snapstart_is_unavailable_on_a_runtime_that_lacks_it():
    assert _options("us-east-1", runtime="nodejs22.x")["SnapStart"]["available"] is False


def test_a_heartbeat_bills_its_pings_while_pages_are_open():
    beat = _options("us-gov-west-1")["heartbeat from open pages"]
    pings = 60 * TRAFFIC["active_hours"] * SCALE
    assert beat["monthly_usd"] == pytest.approx(pings * 2e-7 + pings * 0.05 * GB * 1.66667e-5, abs=0.001)
    assert "a first visit after a quiet spell" in beat["leaves"]


def test_each_option_prices_a_cold_start_at_least():
    """Divided by every cold start, the price is the least each one it removes can cost."""
    pc = _options("us-gov-west-1")["provisioned concurrency, 1 environment"]
    assert pc["usd_per_cold_start_at_least"] == pytest.approx(pc["monthly_usd"] / (TRAFFIC["cold"]["total"] * SCALE),
                                                             abs=0.001)


def test_snapstart_for_java_carries_no_charge_and_is_not_barred_in_govcloud():
    """AWS's pricing page, read 2026-10-26: SnapStart pricing does not apply to Java managed runtimes."""
    for region in ("us-east-1", "us-gov-west-1"):
        snap = _options(region, runtime="java21")["SnapStart"]
        assert snap["available"] is True and snap["monthly_usd"] == 0


def test_an_arm64_function_is_priced_at_the_arm_rates():
    m = _module()
    arm = m.read_prices(json.loads((FIXTURE / "prices-us-gov-west-1.json").read_text()), arch="arm64")
    assert arm["provisioned"] == 3.3334e-6 and arm["duration"] == 1.33334e-5 and arm["request"] == 2e-7


def test_a_container_image_function_has_no_snapstart():
    assert "container image" in _options("us-east-1", runtime=None)["SnapStart"]["why"]


def _run(*args, stdin=""):
    return subprocess.run([sys.executable, str(SCRIPT), "--region", "us-gov-west-1", "--memory-mb", "1769",
                           "--runtime", "python3.12", "--window-days", "14",
                           "--prices", str(FIXTURE / "prices-us-gov-west-1.json"), *args, "-"],
                          input=stdin, capture_output=True, text=True)


def test_a_truncated_fetch_is_not_priced_as_a_whole_window():
    result = _run(stdin=json.dumps(TRAFFIC | {"truncated": True}))
    assert result.returncode == 1 and "truncated" in result.stderr


def test_no_traffic_on_stdin_names_the_stage_that_stopped():
    result = _run(stdin="")
    assert result.returncode == 1 and "cold-path.py stopped" in result.stderr


def test_the_report_cites_the_price_list_and_its_date():
    result = subprocess.run([sys.executable, str(SCRIPT), "--region", "us-gov-west-1", "--memory-mb", "1769",
                             "--runtime", "python3.12", "--window-days", "14",
                             "--prices", str(FIXTURE / "prices-us-gov-west-1.json"), "-"],
                            input=json.dumps(TRAFFIC), capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    for phrase in ("published 2026-10-22", "provisioned concurrency, 1 environment", "not available",
                   "Per cold start, at least", "free tier", "$0.0085"):
        assert phrase in result.stdout, phrase


def test_the_report_names_the_cold_starts_the_window_held():
    """Step 6 names them; working them back from the monthly figure would be arithmetic by hand."""
    result = _run(stdin=json.dumps(TRAFFIC))
    assert "The window held 105 cold starts in 7876 invokes" in result.stdout
