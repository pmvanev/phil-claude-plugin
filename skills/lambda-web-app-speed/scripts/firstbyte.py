#!/usr/bin/env python3
"""Divide one page load's first byte: the network, the front door, and the function.

Used by `/phil:lambda-web-app-speed`, in two calls. First one GET of the page, timed leg by leg:

    python3 firstbyte.py --get https://app.example/

prints one JSON line: when it started and ended (epoch milliseconds), the window to fetch the function's
lines for (`fetch_start_ms`, `fetch_end_ms`), the HTTP status, and DNS, TCP, TLS, the wait for the first
byte, and the first byte itself, in milliseconds. Then the function's platform lines for that window,
matched to it:

    aws logs filter-log-events --log-group-name /aws/lambda/<function> \\
        --start-time <fetch_start_ms> --end-time <fetch_end_ms> --max-items 200000 \\
        --filter-pattern '?"REPORT RequestId" ?INIT_REPORT' --output json \\
      | python3 firstbyte.py --split '<the first call's JSON line>' -

Fetch the lines a few seconds after the GET: CloudWatch receives them late. The window reaches three
seconds either side of the GET, since this machine's clock and AWS's can differ.

**The match.** A `REPORT` is stamped when its invoke ends, so its invoke — the stamp less its
`Duration` and any `Init Duration` — must begin after the GET began, and the stamp must fall before the
GET's first byte, each within three seconds of clock difference. Exactly one `REPORT` must match;
otherwise the function's slice is left unsplit. A response that is not 2xx is not split: a redirect or a
refusal may never have reached the function.

**The split.** The network is DNS, TCP and TLS, as the GET timed them. The function is the `REPORT`'s
`Init Duration` on a cold start plus its `Duration`. The remainder holds the front door — API Gateway or
the load balancer — Lambda placing the request, one round trip of the request and its first byte, and,
on a cold start, Lambda's setup before INIT, which `Init Duration` leaves out. A remainder below zero
means the match was wrong, and the split is refused. A SnapStart restore is refused, as `cold-path.py`
refuses it.

One load is one sample: the targets — TTFB within 0.8 s, LCP within 2.5 s — are the 75th percentile of
page loads (web.dev), which one GET cannot show. The GET sends no cookie and no credential; it loads
what a first visit loads. It writes nothing.
"""
import argparse
import json
import socket
import ssl
import sys
import time
from urllib.parse import urlsplit

TTFB_TARGET_MS = 800
SKEW_MS = 3000  # this machine's clock and AWS's can differ: a REPORT was stamped 285 ms before its GET began


def _ms(since):
    return (time.perf_counter() - since) * 1000


def fetch_window(got):
    """The platform lines to fetch for a GET: its span, widened by the clocks' possible difference."""
    return got["started_ms"] - SKEW_MS, got["ended_ms"] + SKEW_MS


def get(url):
    """One GET, timed: DNS, TCP, TLS, the wait for the first byte, and the first byte from the start."""
    parts = urlsplit(url)
    secure = parts.scheme == "https"
    port = parts.port or (443 if secure else 80)
    path = (parts.path or "/") + (f"?{parts.query}" if parts.query else "")
    started_ms = time.time() * 1000
    start = time.perf_counter()
    t = time.perf_counter()
    address = socket.getaddrinfo(parts.hostname, port, proto=socket.IPPROTO_TCP)[0][4]
    dns_ms = _ms(t)
    t = time.perf_counter()
    sock = socket.create_connection(address[:2], timeout=30)
    connect_ms = _ms(t)
    tls_ms = 0.0
    if secure:
        t = time.perf_counter()
        sock = ssl.create_default_context().wrap_socket(sock, server_hostname=parts.hostname)
        tls_ms = _ms(t)
    host = parts.netloc.rsplit("@", 1)[-1]
    request = (f"GET {path} HTTP/1.1\r\nHost: {host}\r\nAccept: text/html,*/*\r\n"
               "Accept-Encoding: gzip, br\r\nUser-Agent: phil-lambda-web-app-speed\r\nConnection: close\r\n\r\n")
    t = time.perf_counter()
    sock.sendall(request.encode())
    first = sock.recv(1)
    wait_ms = _ms(t)
    ttfb_ms = _ms(start)
    ended_ms = time.time() * 1000
    head = first + sock.recv(64)
    sock.close()
    fields = head.split(b" ", 2)
    status = int(fields[1]) if head.startswith(b"HTTP/") and len(fields) > 1 and fields[1].isdigit() else None
    got = {"url": url, "status": status, "started_ms": int(started_ms), "ended_ms": int(ended_ms) + 1,
           "dns_ms": round(dns_ms, 1), "connect_ms": round(connect_ms, 1), "tls_ms": round(tls_ms, 1),
           "wait_ms": round(wait_ms, 1), "ttfb_ms": round(ttfb_ms, 1)}
    got["fetch_start_ms"], got["fetch_end_ms"] = fetch_window(got)
    return got


def _field(message, name):
    for part in message.split("\t"):
        part = part.strip()
        if part.startswith(f"{name}: "):
            return float(part[len(name) + 2:].split()[0])
    return None


def _invoke_began(event):
    message = event["message"]
    return event["timestamp"] - (_field(message, "Duration") or 0) - (_field(message, "Init Duration") or 0)


def split(got, payload):
    network = got["dns_ms"] + got["connect_ms"] + got["tls_ms"]
    result = {"network_ms": network, "ttfb_ms": got["ttfb_ms"], "function_ms": None, "front_door_ms": None,
              "cold": None, "init_ms": None, "why": ""}
    status = got.get("status")
    if status is None or not 200 <= status < 300:
        result["why"] = f"the response was {status}, not 2xx: it may never have reached the function"
        return result
    reports = [e for e in payload.get("events", []) if e["message"].startswith("REPORT RequestId:")
               and e["timestamp"] <= got["ended_ms"] + SKEW_MS
               and _invoke_began(e) >= got["started_ms"] - SKEW_MS]
    if any("Restore Duration" in e["message"] for e in reports):
        result["why"] = "a SnapStart restore: this version does not divide restores"
        return result
    if len(reports) != 1:
        result["why"] = (f"{len(reports)} REPORT lines in the request's window: the request cannot be told "
                         "apart" if reports else "no REPORT line in the request's window")
        return result
    message = reports[0]["message"]
    init = _field(message, "Init Duration")
    function = (init or 0.0) + _field(message, "Duration")
    remainder = got["ttfb_ms"] - network - function
    if remainder < 0:
        result["why"] = (f"the matched invoke, {function:.0f} ms, is longer than the first byte less the network: "
                         "it cannot be this request's")
        return result
    result.update(cold=init is not None, init_ms=init, function_ms=function, front_door_ms=remainder)
    return result


def _s(ms):
    return f"{ms / 1000:.2f} s"


def report(s):
    lines = [f"First byte: {_s(s['ttfb_ms'])}, against TTFB's 0.8 s target — one load, not the 75th percentile "
             "the target names"]
    lines.append(f"  network (DNS, TCP, TLS): {_s(s['network_ms'])}")
    if s["function_ms"] is None:
        lines.append(f"  the function and the front door: {_s(s['ttfb_ms'] - s['network_ms'])}, unsplit — {s['why']}")
    else:
        kind = f"a cold start, INIT {_s(s['init_ms'])}" if s["cold"] else "a warm invoke"
        lines.append(f"  the function: {_s(s['function_ms'])} ({kind})")
        setup = "; on a cold start, Lambda's setup before INIT" if s["cold"] else ""
        lines.append(f"  the rest: {_s(s['front_door_ms'])} — the front door, placement and one round trip{setup}")
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--get", metavar="URL", help="GET the page once, timed, and print the timings as JSON")
    mode.add_argument("--split", metavar="JSON", help="the --get output, to split against the platform lines")
    parser.add_argument("--json", action="store_true", help="print the split as JSON")
    parser.add_argument("file", nargs="?", help="a filter-log-events response, or - for stdin (with --split)")
    args = parser.parse_args(argv)
    try:
        if args.get:
            print(json.dumps(get(args.get)))
            return 0
        payload = json.load(sys.stdin if args.file in (None, "-") else open(args.file))
        result = split(json.loads(args.split), payload)
    except (OSError, ValueError, KeyError, TypeError, IndexError) as err:
        print(f"firstbyte: {err}", file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2) if args.json else report(result))
    return 0


if __name__ == "__main__":
    sys.exit(main())
