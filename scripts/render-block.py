#!/usr/bin/env python3
"""Render both regions from probe JSON — deterministically, and with every line labelled.

Two properties make this code rather than prose:

- **Slice 01 AC1** — *no value inside the markers was typed by a human*. While the region was
  assembled by a model reading the JSON, that held only by after-the-fact matching, and a remembered
  id is indistinguishable from a probed one in the finished file.
- **Slice 05 KPI-3** — *a second run on an unchanged board writes zero bytes*. Determinism is
  unreachable while a model renders: ordering, spacing and wording drift run to run, every run
  produces a diff, and the diffs stop being read. That is issue #31's decay wearing the look of
  maintenance.

So `render_region` is a pure function of `(probe, stamp)`, and the stamp is the only input allowed to
differ between runs of an unchanged board.

Three provenance categories, and **every line inside the markers carries exactly one**:

- `probed` — the forge returned it.
- `assumed` — the forge returned *half* of it. The line says what is not knowable and why.
- `declared` — only a human can say it. Rendered into a **separate region** by
  `render_declarations`, because a human's answer must survive the probed region's regeneration.
"""

import argparse
import json
import re
import sys
from pathlib import Path

BEGIN = "<!-- phil:board-setup:v1:begin -->"
END = "<!-- phil:board-setup:v1:end -->"
DECL_BEGIN = "<!-- phil:board-setup:declared:v1:begin -->"
DECL_END = "<!-- phil:board-setup:declared:v1:end -->"

STAMP_RE = re.compile(r"^generated .*$", re.M)

LABELS = {
    "forge-and-repo": "Forge",
    "project-and-board-ids": "Board",
    "status-mechanism": "Status mechanism",
    "column-families": "Columns",
    "builtin-workflows": "Workflows",
    "tier": "Tier",
    "docs-root": "Docs root",
    "nwave-mapping": "nWave",
    "default-branch": "Default branch",
    "fork": "Fork",
    "project-discovery": "How the board was found",
    "board-view": "Views",
    "other-single-select-fields": "Other single-select fields",
}

# Fixed order, so rendering does not depend on the probe's key order. Template-shaped facts first,
# then the five that carry no `template_field` and are written anyway.
ORDER = ["forge-and-repo", "project-and-board-ids", "status-mechanism", "column-families",
         "builtin-workflows", "tier", "docs-root", "nwave-mapping",
         "default-branch", "fork", "project-discovery", "board-view",
         "other-single-select-fields"]


def strip_stamp(text: str) -> str:
    """The region with its `generated …` line blanked, for comparing two runs.

    Slice 05 AC2: **a timestamp refresh is never reported as a change.** Comparing stripped text is
    how that is enforced rather than promised.
    """
    return STAMP_RE.sub("generated <stamp>", text)


def _split_compound(query: str) -> list[str]:
    """A compound query is two calls joined because the first returned nothing.

    Rendered as two named entries, so the call that returned nothing stays visible: on this repo
    `repository.projectsV2` being empty is itself a board constant, since it means a card only ever
    arrives via an explicit `gh project item-add`.
    """
    m = re.match(r"^(.*?)\s*#\s*returned\s*(\S+)\s*—\s*then:\s*(.*)$", query, re.S)
    if m:
        return [f"{m.group(1).strip()}  → returned {m.group(2)}", m.group(3).strip()]
    return [query]


def _body(field: str, value) -> str:
    """Render one fact's value.

    **Dispatch is on the value's shape, not on the forge.** GitLab and GitHub return different shapes
    for the same `template_field` — `project-and-board-ids` carries `number`/`title` on GitHub and
    `slug` on GitLab; `column-families` carries `options` on GitHub and `labels` on GitLab. Keying on
    the shape rather than a `forge` field means a new forge cannot crash this by forgetting to set a
    flag, and an unrecognised shape degrades to JSON rather than raising.

    This was a seam defect: `test_gitlab_probe.py` called `gitlab_facts` eight times and never fed the
    result to the renderer, while `test_render_block.py` used only GitHub-shaped facts. Both halves
    green, the join broken, and `--host gitlab.com` could not complete at all.
    """
    if field == "project-and-board-ids":
        if isinstance(value, dict) and "number" in value:            # GitHub: Projects v2
            return (f'project `{value["id"]}` · number {value["number"]} · '
                    f'"{value["title"]}" · {value["url"]}')
        if isinstance(value, dict) and "slug" in value:              # GitLab: a project
            return f'project `{value["id"]}` · {value["slug"]} · {value["url"]}'
    if field == "column-families":
        if isinstance(value, dict) and "options" in value:            # GitHub: single-select options
            opts = " · ".join(f'{o["name"]} `{o["id"]}`' for o in value["options"])
            return (f'Status options ({value["option_count"]}) on field '
                    f'`{value["field_id"]}` — {opts}')
        if isinstance(value, dict) and "labels" in value:             # GitLab: status:: labels
            labels = value.get("labels")
            if labels is None:
                # Should be unreachable — an `unread` fact is filtered before rendering — but stating
                # it beats emitting `count: None` if that filter ever moves.
                raise Refusal("an unread label set cannot be rendered as a fact")
            return (f'{value["mechanism"]} ({value["count"]}) — '
                    + (" · ".join(f'`{l}`' for l in labels) if labels
                       else "none defined on this project"))
    if field == "builtin-workflows":
        if isinstance(value, dict):                                   # GitHub
            out = "enabled — " + " · ".join(value["enabled"])
            if value.get("disabled"):
                out += " · disabled: " + " · ".join(value["disabled"])
            return out
        return str(value)                                             # GitLab: not applicable
    if field == "board-view":
        return " · ".join(f'{v["number"]} "{v["name"]}" {v["url"]}' for v in value)
    if isinstance(value, (dict, list)):
        return json.dumps(value, sort_keys=True)
    return str(value)


class Refusal(Exception):
    def __init__(self, reason: str, fix: str | None = None):
        super().__init__(reason)
        self.reason = reason
        self.fix = fix


def render_region(probe: dict, stamp: str) -> str:
    """The probed-and-assumed region. Pure function of its two arguments.

    **A probe that did not succeed cannot render.** Without this guard a refusal produced a
    well-formed, marker-carrying, `probed`-labelled region with zero facts and exit 0, which then
    passed `region-place`'s marker checks and reached disk. Self-test fixture 02 forbids exactly that
    and was enforced only by model discipline — in the one place this design deliberately moved off
    model discipline.
    """
    status = probe.get("status")
    if status != "ok":
        raise Refusal(f"the probe did not succeed (status: {status!r}) — nothing to render",
                      fix=(probe.get("refusal") or {}).get("fix"))
    # `probed` and `assumed` reach the markers; nothing else does. `unread` is neither a fact nor a
    # guess — it is the absence of both, and writing it as either would launder a failed read into
    # content. It belongs in the report, outside the region.
    #
    # **A fact may itself be `assumed`, not only a `half_probed` entry.** Filtering to `probed` here
    # dropped such facts silently: GitLab's `tier` is derived from two proxies rather than returned,
    # so making it honest made `Tier` disappear from the GitLab block altogether — a template field
    # vanishing, and KPI-1 quietly falling with it. A filter that discards what it cannot categorise
    # is the same defect as a default that invents one.
    facts = {f["field"]: f for f in probe.get("facts", [])
             if f.get("provenance", "probed") in ("probed", "assumed")}

    queries: dict[str, str] = {}

    def qref(query: str) -> str:
        if query.startswith("(see "):
            return qref(facts[query[5:-1].strip()]["query"])
        parts = _split_compound(query)
        for part in parts:
            queries.setdefault(part, f"Q{len(queries) + 1}")
        return "+".join(queries[p] for p in parts)

    # Assign Q-numbers in render order, not probe order, so the numbering is deterministic too.
    for field in ORDER:
        if field in facts:
            qref(facts[field]["query"])
    for h in probe.get("half_probed", []):
        qref(h["query"])

    lines = [f"generated {stamp} · do not edit inside these markers", "",
             "Every line below carries its provenance and the query that produced it. Nothing here",
             "was typed by a human; `assumed` lines say what is not knowable and why.", ""]

    for field in ORDER:
        f = facts.get(field)
        if not f:
            continue
        label = LABELS.get(field, field)
        provenance = f.get("provenance", "probed")
        lines.append(f"- {label}: {_body(field, f['value'])} "
                     f"*({provenance} · {qref(f['query'])})*")
        if f.get("note"):
            # An `assumed` fact's note is not decoration — slice 04 AC2 requires the line to state
            # what is not knowable and why, and for these facts the note is where that lives.
            prefix = "not knowable: " if provenance == "assumed" else ""
            lines.append(f"  {prefix}{f['note']}")

    # --- slice 04: the assumed category ---------------------------------------------------
    for h in probe.get("half_probed", []):
        lines.append(
            f"- {h['known']}, and **`{h['assumed_value']}` is assumed to fire it** "
            f"*(assumed · {qref(h['query'])})*")
        lines.append(f"  not knowable: {h['unknown']} — {h['why']}")

    lines += ["", "**Queries**", ""]
    for query, q in queries.items():
        lines.append(f"- `{q}` — `{query}`")

    np = probe.get("not_probeable", [])
    if np:
        lines += ["", "**Not probeable — only a human can declare these.** "
                  + " · ".join(f'`{n["field"]}` ({n["owner"]})' for n in np)
                  + ". Any answer appears in the *declared* region below, never here."]

    return BEGIN + "\n" + "\n".join(lines) + "\n" + END


def render_declarations(answers: dict, evidence: dict, stamp: str) -> str | None:
    """The declared region — a human's answers, attributed, never inferred.

    `answers` maps family name to the declared valuedness. **A family absent from `answers` is
    absent from the output**: a decline writes nothing, because a line reading "declined" is still a
    line, and `phil:groom-issues` rule 4 would then read a declaration no human made.

    Where a declaration disagrees with observed use, the declaration is written **as given** and the
    disagreement is recorded beside it. Never resolved — the human's answer is the authority, and the
    observation is what a later reader needs to understand why it looked odd.
    """
    if not answers:
        return None

    fams = {f["name"]: f for f in evidence.get("families") or []}
    lines = [f"generated {stamp} · declarations, not probed facts — a human's answers",
             "",
             "Nothing here was probed or inferred. `phil:groom-issues` rule 4 reads this region.",
             ""]

    for name in sorted(answers):
        value = answers[name]
        fam = fams.get(name, {})
        members = ", ".join(f"`{m}`" for m in fam.get("members", []))
        lines.append(f"- Label family **{name}**{f' ({members})' if members else ''}: "
                     f"**{value}** *(you declared · {stamp[:10]})*")

        multiple = fam.get("issues_with_multiple") or []
        if value.startswith("single") and multiple:
            lines.append(
                f"  ⚠ this **disagrees with observed use**: {len(multiple)} issue(s) currently carry "
                f"more than one member — {', '.join('#' + str(n) for n in sorted(multiple))}. "
                f"Recorded, not resolved: the declaration is the authority and the observation is "
                f"kept so a later reader knows it was seen.")
        elif value.startswith("multi") and not multiple:
            lines.append(
                "  ⚠ this **disagrees with observed use**: no issue currently carries more than one "
                "member, so nothing on the board demonstrates the family being multi-valued. "
                "Recorded, not resolved.")

    return DECL_BEGIN + "\n" + "\n".join(lines) + "\n" + DECL_END


def main() -> int:
    ap = argparse.ArgumentParser(description="Render the board-setup regions from probe JSON.")
    ap.add_argument("--probe", type=Path, required=True)
    ap.add_argument("--stamp", required=True, help="UTC, minute precision, e.g. 2026-08-17T21:00Z")
    ap.add_argument("--declarations", type=Path,
                    help="JSON object mapping family name to declared valuedness; omit for none")
    ap.add_argument("--declared-only", action="store_true")
    args = ap.parse_args()

    def read_json(path):
        try:
            return json.loads(path.read_text())
        except OSError as e:
            raise Refusal(f"could not read {path}: {e.strerror}")
        except json.JSONDecodeError as e:
            raise Refusal(f"{path} is not valid JSON: {e}")

    try:
        probe = read_json(args.probe)
        if args.declared_only:
            answers = read_json(args.declarations) if args.declarations else {}
            out = render_declarations(answers, probe.get("elicitation_evidence") or {}, args.stamp)
            if out is None:
                raise Refusal("no declarations to render — a decline writes nothing",
                              fix="omit the declared region entirely; report what stays unevaluated")
            print(out)
            return 0
        print(render_region(probe, args.stamp))
    except Refusal as r:
        print(json.dumps({"schema": "board-setup-render/v1", "status": "refused",
                          "refusal": {"reason": r.reason, "fix": r.fix}}, indent=2))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
