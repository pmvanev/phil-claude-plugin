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

# Slice 03 must write a human's declaration *outside* the probed markers, which collides with slice
# 02's AC1. A second delimited region resolves it: bytes outside **both** regions stay
# byte-identical, the probed region is regenerated freely, and the declared region is written once on
# an answer and never regenerated. Loose prose would have satisfied "outside the markers" and left
# slice 05 no way to know what it must not touch.
DECL_BEGIN = "<!-- phil:board-setup:declared:v1:begin -->"
DECL_END = "<!-- phil:board-setup:declared:v1:end -->"

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


def _declared_positions(text: str):
    lines = text.splitlines()
    b = next((i for i, l in enumerate(lines, 1) if l.strip() == DECL_BEGIN), None)
    e = next((i for i, l in enumerate(lines, 1) if l.strip() == DECL_END), None)
    return b, e


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
    dbegin, dend = _declared_positions(text)
    base = {"heading_line": heading, "region_begin": None, "region_end": None,
            "declared_begin": dbegin, "declared_end": dend,
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
    if (dbegin is None) != (dend is None):
        return {**base, "state": "markers-malformed",
                "malformed_reason": ("a declared-region begin marker with no end marker"
                                     if dend is None else
                                     "a declared-region end marker with no begin marker")}
    if dbegin is not None and dend is not None and dend < dbegin:
        return {**base, "state": "markers-malformed",
                "malformed_reason": "the declared-region end marker precedes its begin marker"}

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
    """The file with **both** generated regions removed — the hand-written prose, and nothing else.

    Placement is built so that excising the probed region returns the original text exactly, which is
    what makes the drift report immune to whether that region has been placed yet.

    The declared region is excised too, and that is a correctness fix rather than symmetry. A
    declaration is a human's answer to a question no forge can answer — it is not prose to be audited
    against the probe, and leaving it in fed declared lines to `drift()` as though they were
    hand-written. Two consequences, both real: the tautology rule broke (placing a declared region
    shifted line numbers and added lines to `cannot_evaluate`), and a declared line carrying an id- or
    URL-shaped token that did not match the probe was filed as `contradicts` — making it
    **retire-eligible, and therefore deletable**. That is a never-regenerated human answer destroyed
    through the one sanctioned mutation.
    """
    # The probed region contributes no newline of its own (the line after the heading donates one),
    # so excising it must not consume one. The declared region *does* contribute its terminator, so
    # excising it consumes that newline too — otherwise every prose line below it shifts by one and
    # the drift report is no longer identical before and after placement.
    for begin, end, owns_terminator in ((BEGIN, END, False), (DECL_BEGIN, DECL_END, True)):
        if begin in text and end in text:
            b = text.index(begin)
            e = text.index(end) + len(end)
            if owns_terminator and text[e:e + 1] == "\n":
                e += 1
            text = text[:b] + text[e:]
    return text


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
                "region_end": None, "declared_begin": None, "declared_end": None,
                "malformed_reason": None, "sha256": None}
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


def place_declaration(text: str, declaration: str) -> str:
    """Insert the declared region — a human's answer, attributed, never regenerated.

    Placed after the probed region when one exists, so the file reads probed-then-declared and a
    later regeneration of the probed block cannot reach it. When no probed region exists yet, it goes
    directly after the heading; the probed region will later insert above it.
    """
    if DECL_BEGIN not in declaration or DECL_END not in declaration:
        raise Refusal("the declaration to place does not carry both declared-region markers")
    if DECL_BEGIN in text or DECL_END in text:
        raise Refusal("a declared region is already present — a human's answer is not regenerated",
                      fix="edit it by hand, or remove it first; this command will not overwrite it")

    state = classify(text)
    if state["state"] == "markers-malformed":
        raise Refusal(state["malformed_reason"])

    chunk = declaration.rstrip("\n")
    lines = text.splitlines(keepends=True)

    if state["state"] == "region-present":
        at = state["region_end"]          # 1-based line of the probed `end` marker
    elif state["heading_line"] is not None:
        at = state["heading_line"]
    else:
        prefix = text if text.endswith("\n") else text + "\n"
        return f"{prefix}\n{HEADING}\n{chunk}\n"

    tail = lines[at:]
    head = "".join(lines[:at])
    if not head.endswith("\n"):
        head += "\n"
    return head + chunk + "\n" + "".join(tail)


def replace_region(text: str, region: str) -> str:
    """Regenerate the probed region in place, leaving every other byte alone.

    Slice 05's primitive. The declared region and the hand-written prose are both outside what this
    touches, which is the property that makes habitual re-running safe rather than merely quiet.
    """
    if BEGIN not in region or END not in region:
        raise Refusal("the region to place does not carry both markers")
    state = classify(text)
    if state["state"] == "markers-malformed":
        raise Refusal(state["malformed_reason"])
    if state["state"] != "region-present":
        raise Refusal("no probed region to replace — use --place to insert one")

    b = text.index(BEGIN)
    e = text.index(END) + len(END)
    return text[:b] + region.rstrip("\n") + text[e:]


STAMP_RE = re.compile(r"^generated .*$", re.M)


def _strip_stamp(text: str) -> str:
    return STAMP_RE.sub("generated <stamp>", text)


def region_changes(old_region: str, new_region: str) -> dict:
    """What the forge now says that the file did not — line by line, not a count.

    A count hides which constant moved, and constants are not interchangeable: an option id that
    changed means `updateProjectV2Field` was run against the field, and a docs root that changed
    means every absolute link in every issue body is now wrong.
    """
    old_lines = _strip_stamp(old_region).splitlines()
    new_lines = _strip_stamp(new_region).splitlines()
    removed = [l for l in old_lines if l not in new_lines]
    added = [l for l in new_lines if l not in old_lines]
    stamp_only = not removed and not added and old_region != new_region
    return {"changed": bool(removed or added), "stamp_only": stamp_only,
            "removed": removed, "added": added}


def refresh_region(path: Path, region: str, expect_sha: str) -> dict:
    """Slice 05's re-run: regenerate the probed region, writing **zero bytes** when nothing moved.

    The timestamp question, decided: **the stamp is not refreshed on a no-change run.** KPI-3 demands
    a second run write zero bytes, and refreshing a stamp writes bytes — so excluding the stamp from
    the comparison while still writing it would fail KPI-3 while looking correct. A run that rewrites
    the file to move a clock produces a diff every time, the diffs stop being read, and the block
    decays into issue #31's unnoticed-stale state wearing the look of maintenance.
    """
    if BEGIN not in region or END not in region:
        # Never `unchanged`. Slice 05 AC5: a probe that could not be read must not render as a board
        # that did not move.
        raise Refusal("no rendered region supplied — cannot distinguish `unchanged` from `unread`",
                      fix="render the region from a successful probe first")

    text = path.read_text()
    if sha256_of(text) != expect_sha:
        raise Refusal("the file changed between read and write",
                      fix="re-run --classify and refresh again against the current file")

    state = classify(text)
    if state["state"] != "region-present":
        raise Refusal("no probed region to refresh — use --place to insert one")

    b, e = text.index(BEGIN), text.index(END) + len(END)
    current = text[b:e]
    report = region_changes(current, region)

    if not report["changed"]:
        return {"status": "unchanged", "bytes_written": 0, "stamp_only": report["stamp_only"],
                "changes": report}

    out = text[:b] + region.rstrip("\n") + text[e:]
    # The same pre-write guard `write_region` runs. Splicing by marker index is structurally safe, but
    # "safe by construction" and "checked" are different claims, and the command's intent paragraph
    # promises the latter for every write of the probed region.
    if _excise(out) != _excise(text):
        raise Refusal("refreshing would alter content outside the regions — refusing")
    path.write_text(out)
    return {"status": "ok", "bytes_written": len(out.encode()), "stamp_only": False,
            "changes": report, "sha256_after": sha256_of(out)}


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
        raise Refusal("that line is inside the probed markers — the region is generated, not retired")
    if state["declared_begin"] and state["declared_end"] and \
            state["declared_begin"] <= lineno <= state["declared_end"]:
        # A declaration is never regenerated, so deleting one loses it outright — the worst outcome
        # this function can produce, and reachable before this guard existed.
        raise Refusal("that line is inside the declared markers — a human's declaration is never "
                      "retired by this command",
                      fix="edit or remove the declared region by hand if the answer has changed")

    return "".join(lines[:lineno - 1] + lines[lineno:])


def _read_text(path: Path) -> str:
    try:
        return path.read_text()
    except OSError as e:
        raise Refusal(f"could not read {path}: {e.strerror}")


def _read_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text())
    except OSError as e:
        raise Refusal(f"could not read {path}: {e.strerror}")
    except json.JSONDecodeError as e:
        raise Refusal(f"{path} is not valid JSON: {e}")


def _require_present(path: Path, state: dict, mode: str) -> None:
    if state["state"] == "file-absent":
        raise Refusal(f"{path} does not exist — {mode} needs an existing file",
                      fix="run --place first to create it")


def _require_sha(args, text: str, mode: str) -> None:
    if not args.expect_sha:
        raise Refusal(f"{mode} requires --expect-sha from a --classify run")
    if sha256_of(text) != args.expect_sha:
        raise Refusal("the file changed between read and write",
                      fix="re-run --classify and pass back the sha it returns")


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
    ap.add_argument("--declare", metavar="DECL_FILE", type=Path,
                    help="insert the declared region — a human's answer, never regenerated; "
                         "requires --expect-sha")
    ap.add_argument("--refresh", metavar="REGION_FILE", type=Path,
                    help="regenerate the probed region in place, leaving the declared region and "
                         "all prose untouched; requires --expect-sha")
    ap.add_argument("--expect-sha", help="the sha256 --classify returned for this file")
    args = ap.parse_args()

    try:
        # Every read of a caller-supplied path goes through these, so a missing or malformed file is
        # a JSON refusal rather than a traceback. Callers parse stdout; a traceback is not parseable,
        # so an unhandled exception here is a contract break and not a rough edge.
        state = classify_file(args.file)
        text = "" if state["state"] == "file-absent" else args.file.read_text()

        if args.classify:
            print(json.dumps({"schema": "board-setup-classify/v1", **state}, indent=2))
        elif args.drift:
            if state["state"] == "file-absent":
                raise Refusal(f"{args.file} does not exist — nothing to diff")
            print(json.dumps({"schema": "board-setup-drift/v1",
                              **drift(text, _read_json(args.drift))}, indent=2))
        elif args.place:
            # An absent file has no sha to supply, so the create path cannot require one. It was
            # doubly unreachable before: `main()` crashed before dispatch, and this check demanded a
            # sha the state can never produce.
            if state["state"] != "file-absent" and not args.expect_sha:
                raise Refusal("--place requires --expect-sha from a --classify run")
            r = write_region(args.file, _read_text(args.place), args.expect_sha)
            print(json.dumps({"schema": "board-setup-place/v1", "status": "ok", **r}, indent=2))
        elif args.declare:
            _require_present(args.file, state, "--declare")
            _require_sha(args, text, "--declare")
            out = place_declaration(text, _read_text(args.declare))
            args.file.write_text(out)
            print(json.dumps({"schema": "board-setup-declare/v1", "status": "ok",
                              "written": str(args.file),
                              "sha256_after": sha256_of(out)}, indent=2))
        elif args.refresh:
            _require_present(args.file, state, "--refresh")
            _require_sha(args, text, "--refresh")
            r = refresh_region(args.file, _read_text(args.refresh), args.expect_sha)
            print(json.dumps({"schema": "board-setup-refresh/v1", **r}, indent=2))
        elif args.retire is not None:
            _require_present(args.file, state, "--retire")
            _require_sha(args, text, "--retire")
            args.file.write_text(retire_line(text, args.retire))
            print(json.dumps({"schema": "board-setup-retire/v1", "status": "ok",
                              "retired_line": args.retire}, indent=2))
        else:
            raise Refusal("one of --classify, --drift, --place, --declare, --refresh or "
                          "--retire is required")
    except Refusal as r:
        print(json.dumps({"status": "refused",
                          "refusal": {"reason": r.reason, "fix": r.fix}}, indent=2))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
