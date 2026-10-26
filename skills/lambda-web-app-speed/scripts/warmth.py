#!/usr/bin/env python3
"""Price keeping a Lambda function warm, per month, for the app's own traffic.

Used by `/phil:lambda-web-app-speed`. Give it what `cold-path.py --json` reports, on stdin, with the
function's Region, memory and runtime and the window's length in days:

    aws logs filter-log-events … --output json \\
      | python3 cold-path.py --json - \\
      | python3 warmth.py --region us-gov-west-1 --memory-mb 1769 --runtime python3.12 \\
          --arch x86_64 --window-days 14 -

It fetches the Region's Lambda prices from AWS's public price list, which needs no credentials, or reads
them from `--prices <file>`. It writes nothing.

**The traffic** is scaled from the window to a 730-hour month: invokes, cold starts, the clock hours that
saw a request (standing in for the hours a page was open), the most environments busy in one minute, and
the time every invoke took.

A truncated fetch is refused: its traffic covers part of the window, and scaling it as the whole would
price every option too low.

**The options**, each with its monthly price, what it removes, what it leaves, and its price divided by
every cold start in the month — the least each cold start it removes can cost, since no option removes
them all:

- **Provisioned concurrency**, for one environment and for the measured peak: the memory configured,
  for every second of the month, at its own price, and invocation time at its own rate, less the
  on-demand duration it replaces (AWS Lambda pricing, read 2026-10-26).
- **SnapStart**, where the runtime and partition offer it: for Python and .NET, a cache charge on the
  memory allocated for every second the version is active, and the memory allocated for each restore;
  for Java managed runtimes, no charge (AWS's pricing page). Not available for Python or .NET in AWS
  GovCloud (US) (its user guide, read 2026-10-26). It shortens a cold start rather than removing it.
- **A heartbeat from open pages**: one request a minute, held 50 ms, during the active hours; the front
  door's own per-request charge is not priced.

Prices are the first tier, for the function's architecture, and ignore the free tier. The provisioned
duration rate is applied to all invoke time, an approximation worth cents.
"""
import argparse
import json
import re
import sys
import urllib.request

PRICE_LIST = "https://pricing.us-east-1.amazonaws.com"
MONTH_HOURS = 730
USAGE = {
    "request": "Request",
    "duration": "Lambda-GB-Second",
    "provisioned": "Lambda-Provisioned-Concurrency",
    "provisioned_duration": "Lambda-Provisioned-GB-Second",
    "snapstart_cache": "Lambda-SnapStart-Cached-GB-S",
    "snapstart_restore": "Lambda-SnapStart-Restored-GB",
}
SNAPSTART_RUNTIMES = re.compile(r"^(python3\.(1[2-9]|[2-9]\d)|dotnet([89]|\d\d)|java(1[1-9]|[2-9]\d))")


def read_prices(price_list, arch="x86_64"):
    """The six first-tier prices, by name, from one Region's Lambda price list, for one architecture."""
    terms = price_list["terms"]["OnDemand"]
    prices = {"published": price_list.get("publicationDate", "")[:10]}
    suffix = "-ARM" if arch == "arm64" else ""
    for sku, product in price_list["products"].items():
        usage = re.sub(r"^[A-Z]{2,4}\d-", "", product["attributes"].get("usagetype", ""))
        for name, wanted in USAGE.items():
            if usage != wanted + (suffix if not name.startswith("snapstart") else ""):
                continue
            for term in terms.get(sku, {}).values():
                for dimension in term["priceDimensions"].values():
                    if str(dimension.get("beginRange", "0")) == "0":
                        prices[name] = float(dimension["pricePerUnit"]["USD"])
    return prices


def fetch_prices(region, arch):
    with urllib.request.urlopen(f"{PRICE_LIST}/offers/v1.0/aws/AWSLambda/current/region_index.json",
                                timeout=30) as r:
        regions = json.load(r)["regions"]
    if region not in regions:
        raise ValueError(f"AWS's public price list holds no {region}")
    with urllib.request.urlopen(PRICE_LIST + regions[region]["currentVersionUrl"], timeout=60) as r:
        return read_prices(json.load(r), arch)


def _snapstart(region, runtime, prices):
    if not runtime:
        return False, "SnapStart does not support a container image"
    if not SNAPSTART_RUNTIMES.match(runtime):
        return False, f"SnapStart does not support {runtime}"
    if runtime.startswith("java"):
        return True, ""
    if region.startswith("us-gov-") and runtime.startswith(("python", "dotnet")):
        return False, "not available for Python or .NET in AWS GovCloud (US) (its user guide, read 2026-10-26)"
    if prices.get("snapstart_cache") is None or prices.get("snapstart_restore") is None:
        return False, "the Region's price list holds no SnapStart price"
    return True, ""


def price(traffic, prices, region, memory_mb, runtime, window_days, beats_per_minute=1, beat_ms=50):
    gb = memory_mb / 1024
    scale = MONTH_HOURS / (window_days * 24)
    month_s = MONTH_HOURS * 3600
    cold = traffic["cold"]["total"] * scale
    invoke_gb_s = traffic["duration_total_ms"] / 1000 * scale * gb
    duration_delta = invoke_gb_s * (prices["provisioned_duration"] - prices["duration"])

    def option(name, available, monthly, removes, leaves, why=""):
        per = monthly / cold if available and cold else None
        return {"name": name, "available": available, "monthly_usd": monthly, "removes": removes,
                "leaves": leaves, "why": why, "usd_per_cold_start_at_least": per}

    peak = max(traffic["peak_environments"], 1)
    options = [option("provisioned concurrency, 1 environment",
                      True, gb * month_s * prices["provisioned"] + duration_delta,
                      "the cold start of a lone request",
                      "cold starts beyond one concurrent request; it serves only the alias that holds it (LWS-7)")]
    if peak > 1:
        options.append(option(f"provisioned concurrency, {peak} environments (the peak)",
                              True, peak * gb * month_s * prices["provisioned"] + duration_delta,
                              f"cold starts up to {peak} concurrent requests, the most seen in one minute",
                              "cold starts above the measured peak"))
    snap_ok, why = _snapstart(region, runtime, prices)
    charged = snap_ok and not (runtime or "").startswith("java")
    snap_cost = (gb * month_s * prices["snapstart_cache"] + cold * gb * prices["snapstart_restore"]
                 if charged else 0.0)
    options.append(option("SnapStart", snap_ok, snap_cost, "INIT, replaced by restoring a snapshot — a cold "
                          "start shortened, not removed",
                          "a restore on every cold start, its time unmeasured until tried", why))
    beats = beats_per_minute * 60 * traffic["active_hours"] * scale
    options.append(option("heartbeat from open pages", True,
                           beats * prices["request"] + beats * beat_ms / 1000 * gb * prices["duration"],
                           "cold starts while a signed-in page stays open",
                           "a first visit after a quiet spell, cold starts beyond one concurrent request, and "
                           "Lambda's recycle every few hours"))
    return options


def _usd(amount):
    if amount == 0:
        return "$0"
    return f"${amount:.2f}" if abs(amount) >= 0.01 else f"under $0.01" if abs(amount) < 0.0001 else f"${amount:.4f}"


def report(options, traffic, prices, region, window_days):
    scale = MONTH_HOURS / (window_days * 24)
    lines = [f"Warmth for {region}, prices published {prices['published']} (AWS public price list; first tier, "
             "free tier ignored)",
             f"Traffic per month, scaled from {window_days} days: {traffic['invokes'] * scale:.0f} invokes, "
             f"{traffic['cold']['total'] * scale:.0f} cold starts, {traffic['active_hours'] * scale:.0f} active "
             f"hours, peak {traffic['peak_environments']} environments in a minute",
             f"The window held {traffic['cold']['total']} cold starts in {traffic['invokes']} invokes",
             "", "| Option | Per month | Per cold start, at least | Removes | Leaves |", "|---|---|---|---|---|"]
    for o in options:
        if not o["available"]:
            lines.append(f"| {o['name']} | not available: {o['why']} | — | | |")
            continue
        per = _usd(o["usd_per_cold_start_at_least"]) if o["usd_per_cold_start_at_least"] is not None else "—"
        lines.append(f"| {o['name']} | {_usd(o['monthly_usd'])} | {per} | {o['removes']} | {o['leaves']} |")
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--region", required=True)
    parser.add_argument("--memory-mb", type=int, required=True)
    parser.add_argument("--runtime", required=True, help="the function's Runtime; none for a container image")
    parser.add_argument("--arch", choices=["x86_64", "arm64"], default="x86_64")
    parser.add_argument("--window-days", type=float, required=True)
    parser.add_argument("--prices", help="a Lambda price-list file, instead of fetching the Region's")
    parser.add_argument("--json", action="store_true", help="print the options as JSON")
    parser.add_argument("file", help="cold-path.py --json output, or - for stdin")
    args = parser.parse_args(argv)
    try:
        traffic = json.load(sys.stdin if args.file == "-" else open(args.file))
    except (OSError, ValueError) as err:
        print(f"warmth: no traffic to price ({err}): cold-path.py stopped before it — read its message",
              file=sys.stderr)
        return 1
    if traffic.get("truncated"):
        print("warmth: the fetch was truncated, so its traffic covers part of the window; narrow the window "
              "and measure again before pricing", file=sys.stderr)
        return 1
    runtime = args.runtime if args.runtime not in ("", "None", "null") else None
    try:
        if args.prices:
            with open(args.prices) as f:
                prices = read_prices(json.load(f), args.arch)
        else:
            prices = fetch_prices(args.region, args.arch)
        options = price(traffic, prices, args.region, args.memory_mb, runtime, args.window_days)
    except (OSError, ValueError, KeyError, TypeError) as err:
        print(f"warmth: cannot price {args.region}: {err}", file=sys.stderr)
        return 1
    print(json.dumps(options, indent=2) if args.json else report(options, traffic, prices, args.region,
                                                                 args.window_days))
    return 0


if __name__ == "__main__":
    sys.exit(main())
