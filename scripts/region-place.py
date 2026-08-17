#!/usr/bin/env python3
"""Slice 02's reader, placer and drift report — put a generated region inside a file of prose.

Slice 01 wrote into a `CLAUDE.md` with no `## Issue board` section, so nothing human was at risk.
This script handles the case that repo does not have: a section already full of hazards recorded
after contact, **none of it reproducible by any probe**, several lines stating facts the region is
about to own.

The guarantee is narrow and absolute: **content outside the markers is byte-identical on every
path**, including failure and refusal. That is why placement and line arithmetic live here rather
than in prose. It is the same reasoning slice 01 used for the probe — a property code holds beats
one a model is asked to honour — applied to the property that makes coexistence safe at all.

Three refusals, and each exists because guessing is worse than stopping:

- **Malformed markers.** A `begin` with no `end` is refused, never resolved by scanning to the next
  heading. The region's extent is never guessed, because a wrong guess deletes prose.
- **A region already present.** Slice 05 owns re-run. Rewriting one here would be undefined
  behaviour that reports success.
- **The file changed since it was read.** Classification returns a sha; the write re-checks it.

Reads and writes one local file. Makes no forge call and runs no other program.
"""

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

BEGIN = "<!-- phil:board-setup:v1:begin -->"
END = "<!-- phil:board-setup:v1:end -->"
HEADING = "## Issue board"

# Shapes whose *wrongness* is mechanically decidable: if a token of this shape appears in the prose
# and does not equal any probed value, the prose disagrees with the forge. Anything not of a known
# shape is `cannot evaluate` — never `contradicts`, because a probe that says nothing about a line
# is not evidence against it.
SHAPES = {
    "project-id": re.compile(r"\bPVT_[A-Za-z0-9_-]+"),
    "status-field-id": re.compile(r"\bPVTSSF_[A-Za-z0-9_-]+"),
    "docs-root": re.compile(r"https://github\.com/[^\s`)]+/blob/[^\s`)]+"),
}


class Refusal(Exception):
    """A stop with a reason. Nothing is written on any path that raises this."""

    def __init__(self, reason: str, fix: str | None = None):
        super().__init__(reason)
        self.reason = reason
        self.fix = fix


def sha256_of(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def _marker_positions(text: str):
    begins = [i for i, l in enumerate(text.splitlines(), 1) if l.strip() == BEGIN]
    ends = [i for i, l in enumerate(text.splitlines(), 1) if l.strip() == END]
    return begins, ends


def _heading_line(text: str) -> int | None:
    """The `## Issue board` heading, at h2 exactly.

    `### Issue board` is a subsection of something else and must not be adopted as the section —
    inserting into it would put board constants under an unrelated parent.
    """
    for i, line in enumerate(text.splitlines(), 1):
        if line.rstrip() == HEADING:
            return i
    return None


def classify(text: str) -> dict:
    """Read the file and name its state. Never modifies anything."""
    begins, ends = _marker_positions(text)
    heading = _heading_line(text)
    base = {"heading_line": heading, "region_begin": None, "region_end": None,
            "malformed_reason": None, "sha256": sha256_of(text)}

    if len(begins) > 1 or len(ends) > 1:
        return {**base, "state": "markers-malformed",
                "malformed_reason": f"{len(begins)} begin and {len(ends)} end markers — "
                                    "a region's extent is never guessed"}
    if begins and not ends:
        return {**base, "state": "markers-malformed",
                "malformed_reason": "a begin marker with no end marker"}
    if ends and not begins:
        return {**base, "state": "markers-malformed",
                "malformed_reason": "an end marker with no begin marker"}
    if begins and ends:
        if ends[0] < begins[0]:
            return {**base, "state": "markers-malformed",
                    "malformed_reason": "the end marker precedes the begin marker"}
        return {**base, "state": "region-present",
                "region_begin": begins[0], "region_end": ends[0]}
    if heading is None:
        return {**base, "state": "no-section"}
    return {**base, "state": "section-no-markers"}


def _excise(text: str) -> str:
    """The file with the region removed — what AC1 says must never change.

    Placement is built so that excising the region returns the original text exactly, which is what
    makes the drift report immune to whether the region has been placed yet.
    """
    if BEGIN not in text or END not in text:
        return text
    b = text.index(BEGIN)
    e = text.index(END) + len(END)
    return text[:b] + text[e:]


def place(text: str, region: str) -> str:
    """Return `text` with `region` inserted. Raises Refusal rather than guessing."""
    if BEGIN not in region or END not in region:
        raise Refusal("the region to place does not carry both markers")

    state = classify(text)
    if state["state"] == "markers-malformed":
        raise Refusal(state["malformed_reason"])
    if state["state"] == "region-present":
        raise Refusal("a region is already present — slice 05 owns re-run and staleness",
                      fix=None)

    if state["state"] == "no-section":
        prefix = text if text.endswith("\n") else text + "\n"
        body = region if region.endswith("\n") else region + "\n"
        return f"{prefix}\n{HEADING}\n{body}"

    # Immediately after the heading line, contributing **no newline of its own**. The line that
    # followed the heading supplies the terminator for the `end` marker, so excising the region
    # restores the original byte-for-byte. Appending even one "\n" here is a byte outside the
    # markers that was not there before — AC1 forbids it, and the pre-write check in
    # `write_region` catches it if this is ever got wrong again.
    lines = text.splitlines(keepends=True)
    at = state["heading_line"]  # 1-based; insert after it
    tail = lines[at:]
    chunk = region.rstrip("\n")
    if not tail:
        # The heading was the last line, so nothing follows to terminate the marker.
        return "".join(lines[:at]) + chunk + "\n"
    return "".join(lines[:at]) + chunk + "".join(tail)


def classify_file(path: Path) -> dict:
    """Classify a path rather than a string, so an absent file is a state and not a traceback.

    The skill's PLACE step says to create the file if it is absent and say which happened, and it
    forbids placing by hand. Letting `FileNotFoundError` escape leaves the caller no route but the
    `Write` grant — hand placement, prohibited by the skill it is following.
    """
    if not path.exists():
        return {"state": "file-absent", "heading_line": None, "region_begin": None,
                "region_end": None, "malformed_reason": None, "sha256": None}
    return classify(path.read_text())


def write_region(path: Path, region: str, expect_sha: str | None) -> dict:
    """Place and write, refusing if the file moved since it was read.

    The outside-bytes check runs on the produced text *before* anything reaches disk, so a bug in
    `place` is caught here rather than discovered in a diff later.

    `expect_sha=None` means "this file does not exist and I intend to create it". It is not a way
    to skip the guard: a file that does exist is refused when no sha is supplied.
    """
    if not path.exists():
        # Validate before creating, so a refusal leaves no partial file behind.
        if BEGIN not in region or END not in region:
            raise Refusal("the region to place does not carry both markers")
        body = region if region.endswith("\n") else region + "\n"
        out = f"{HEADING}\n{body}"
        path.write_text(out)
        return {"written": str(path), "created": True,
                "sha256_before": None, "sha256_after": sha256_of(out)}

    text = path.read_text()
    actual = sha256_of(text)
    if expect_sha is None:
        raise Refusal("the file exists, so --expect-sha is required",
                      fix="run --classify and pass back the sha256 it returns")
    if actual != expect_sha:
        raise Refusal("the file changed between read and write",
                      fix="re-run --classify and place again against the current file")

    out = place(text, region)
    if _excise(out) != _excise(text):
        raise Refusal("placement would alter content outside the markers — refusing")

    path.write_text(out)
    return {"written": str(path), "created": False,
            "sha256_before": actual, "sha256_after": sha256_of(out)}


def _section_lines(text: str):
    """(lineno, line) for the board section's content, over the text with any region excised.

    Numbering the excised text is what makes the report identical before and after placement: the
    generated region agreeing with the probe is a tautology, not a confirmation.
    """
    clean = _excise(text)
    heading = _heading_line(clean)
    if heading is None:
        return []
    out = []
    for i, line in enumerate(clean.splitlines(), 1):
        if i <= heading:
            continue
        if line.startswith("## "):
            break
        if line.strip():
            out.append((i, line))
    return out


# A probed scalar is evidence only if it is discriminating. The first real dogfood run matched the
# project number `3` and an option count `4` as bare substrings and produced nineteen "confirms",
# one of them resting entirely on a line containing the digit 2. A false confirm asserts the prose
# was checked and found sound, which is worse than reporting nothing about it.
MIN_EVIDENCE_LEN = 6


def _flatten(value, into: list) -> None:
    """Walk a fact's value to arbitrary depth, collecting scalars.

    Depth matters: `column-families` nests its option ids as a list of dicts inside the value, and
    a one-level walk stringifies that list and matches nothing — silently turning the board's most
    dangerous constants into `cannot evaluate`.
    """
    if isinstance(value, dict):
        for v in value.values():
            _flatten(v, into)
    elif isinstance(value, (list, tuple)):
        for v in value:
            _flatten(v, into)
    elif value is not None and not isinstance(value, bool):
        into.append(str(value))


def _probed_values(probe: dict):
    """Every scalar a probe fact asserts, flattened. Only `probed` facts count as evidence."""
    values: list[str] = []
    for f in probe.get("facts", []):
        if f.get("provenance") != "probed":
            continue
        _flatten(f.get("value"), values)
    return [v for v in values if v and len(v) >= MIN_EVIDENCE_LEN]


def drift(text: str, probe: dict) -> dict:
    """Compare the hand-written prose against the probe. Reports; never edits.

    Three buckets, and the third is the honest one: a line the probe says nothing about is
    `cannot evaluate`, never `contradicts`. Calling such a line wrong would be the board's habits
    auditing themselves, which is what this feature exists to prevent.
    """
    probed = _probed_values(probe)
    confirms, contradicts, cannot = [], [], []

    for lineno, line in _section_lines(text):
        bad = None
        for shape, pattern in SHAPES.items():
            for token in pattern.findall(line):
                if not any(token in v or v in token for v in probed):
                    bad = {"line": lineno, "shape": shape, "found": token, "text": line.strip()}
                    break
            if bad:
                break
        if bad:
            # Contradiction wins the line outright. A line carrying one right id and one wrong one
            # is a wrong line, and filing it under `confirms` too would bury that.
            contradicts.append(bad)
            continue

        hit = next((v for v in probed if v and v in line), None)
        if hit:
            confirms.append({"line": lineno, "value": hit, "text": line.strip()})
        else:
            cannot.append({"line": lineno, "text": line.strip(),
                           "why": "no probed fact bears on this line"})

    return {"confirms": confirms, "contradicts": contradicts, "cannot_evaluate": cannot}


def retire_line(text: str, lineno: int) -> str:
    """Delete exactly one whole line — the only change permitted outside the markers.

    Called only on an explicit answer. Silence is not an answer, and the caller, not this function,
    owns that distinction.
    """
    lines = text.splitlines(keepends=True)
    if lineno < 1 or lineno > len(lines):
        raise Refusal(f"line {lineno} is out of range (file has {len(lines)} lines)")

    state = classify(text)
    if state["state"] == "region-present" and \
            state["region_begin"] <= lineno <= state["region_end"]:
        raise Refusal("that line is inside the markers — the region is generated, not retired")

    return "".join(lines[:lineno - 1] + lines[lineno:])


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Classify, place into, and diff a CLAUDE.md that already contains prose.")
    ap.add_argument("--file", type=Path, required=True)
    ap.add_argument("--classify", action="store_true",
                    help="name the file's state and return its sha; writes nothing")
    ap.add_argument("--drift", metavar="PROBE_JSON", type=Path,
                    help="report confirms / contradicts / cannot-evaluate; writes nothing")
    ap.add_argument("--place", metavar="REGION_FILE", type=Path,
                    help="insert the region; requires --expect-sha")
    ap.add_argument("--retire", metavar="LINE", type=int,
                    help="delete one whole line, on an explicit answer; requires --expect-sha")
    ap.add_argument("--expect-sha", help="the sha256 --classify returned for this file")
    args = ap.parse_args()

    try:
        text = args.file.read_text()
        if args.classify:
            print(json.dumps({"schema": "board-setup-classify/v1", **classify(text)}, indent=2))
        elif args.drift:
            print(json.dumps({"schema": "board-setup-drift/v1",
                              **drift(text, json.loads(args.drift.read_text()))}, indent=2))
        elif args.place:
            if not args.expect_sha:
                raise Refusal("--place requires --expect-sha from a --classify run")
            r = write_region(args.file, args.place.read_text(), args.expect_sha)
            print(json.dumps({"schema": "board-setup-place/v1", "status": "ok", **r}, indent=2))
        elif args.retire:
            if not args.expect_sha:
                raise Refusal("--retire requires --expect-sha from a --classify run")
            if sha256_of(text) != args.expect_sha:
                raise Refusal("the file changed between read and write")
            args.file.write_text(retire_line(text, args.retire))
            print(json.dumps({"schema": "board-setup-retire/v1", "status": "ok",
                              "retired_line": args.retire}, indent=2))
        else:
            raise Refusal("one of --classify, --drift, --place or --retire is required")
    except Refusal as r:
        print(json.dumps({"status": "refused",
                          "refusal": {"reason": r.reason, "fix": r.fix}}, indent=2))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
