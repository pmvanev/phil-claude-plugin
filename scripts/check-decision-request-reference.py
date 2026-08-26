#!/usr/bin/env python3
"""Fail the build when the decision-request standard is not wired to a command that can ask.

## What this checks, and what it does NOT

It checks that a **reference resolves**. It does not check that any ask **conforms** — nothing can, and
saying so here is not modesty, it is the whole honest content of the check.

`skills/shared/decision-request.md` governs the wording, the two word limits, the vocabulary, the option
costs and the placement of a decision request. A referencing skill can still emit a bare option list in
the project's own jargon at the end of a wall of output and pass this check green. The wording is pinned
by `skills/shared/self-test/decision-request/` against recorded fixtures, and by review. Conformance in
flight is unenforced.

That gap is the reason this file says so twice. `CLAUDE.md` records the shape of the failure it would
otherwise be: *"absence of `Write` never meant read-only"* — a shallow signal standing in for the real
one, green and meaningless. This check's signal is genuinely shallow; what makes it worth having is that
it is shallow **about a stated thing**.

## The two directions, and why both

A single direction would have missed a live defect. Measured 2026-08-26:

- **Direction A — a grant with no standard.** A command granting `AskUserQuestion` whose loaded skill
  carries no reference. The command can ask, and nothing tells it how. Nine of thirteen commands were in
  this state before this check existed.
- **Direction B — a standard with no grant.** A skill containing an `AskUserQuestion` call site that no
  granting command loads. The ask is dead: the skill instructs a call the command does not permit, and
  the failure is silent because a refused tool looks like a skipped step. `skills/refactor/SKILL.md`
  asked *"Refactoring without tests is risky. Continue anyway?"* and `commands/refactor.md` granted no
  such tool — found by this check's first run, and fixed.

Direction B is the same defect the feature's own evidence recorded as E6, inverted: there, the one skill
that wrote the plain-language rule down was the one command that could not ask a structured question.

## Exemptions

A command that legitimately needs no reference declares it, in the command or in the skill it loads:

    <!-- decision-request-exempt: <reason, at least four words> -->

An HTML comment rather than a frontmatter key, so it works identically in a command and a skill and
touches nothing a loader reads. **Silence is never conformance** — an undeclared gap fails.

**No file claims an exemption today, and that is a finding rather than an oversight.** All ten skills
loaded by the thirteen granting commands genuinely put questions to the human; four do it in prose
without naming the tool (`adversarial-review` asks what to review when the scope is ambiguous;
`session-handoff` asks for a diversion's reason and for an unknown owner; `board-setup` and `rank-issues`
elicit what no forge can answer). The mechanism exists because a future command will need it, and
because a check with no expressible exemption gets satisfied by a fake reference instead.

Exit 0 clean and silent, 1 with named failures.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
FRAGMENT = "skills/shared/decision-request.md"
TOOL = "AskUserQuestion"
EXEMPT = re.compile(r"<!--\s*decision-request-exempt:\s*(.+?)\s*-->")
# The reference must be the interpolated absolute form, per skills/shared/README.md: a bare relative
# path is left literal in a skill body and resolves against the user's project, where it does not exist.
REQUIRED_FORM = "${CLAUDE_PLUGIN_ROOT}/" + FRAGMENT


def _grants_tool(text: str) -> bool:
    """True when a command's frontmatter grants the question tool."""
    for line in text.splitlines():
        if line.startswith("allowed-tools:"):
            return TOOL in line
    return False


def _loaded_skills(text: str) -> list[str]:
    return sorted(set(re.findall(r"skills/([a-z0-9-]+)/SKILL\.md", text)))


def _exemption(path: Path) -> str | None:
    m = EXEMPT.search(path.read_text())
    if not m:
        return None
    reason = m.group(1).strip()
    return reason if len(reason.split()) >= 4 else ""


def main() -> int:
    failures: list[str] = []

    if not (REPO / FRAGMENT).is_file():
        print(f"FAIL  the standard is missing: {FRAGMENT}")
        return 1

    skills = {p.parent.name: p for p in (REPO / "skills").glob("*/SKILL.md")}
    references = {name: REQUIRED_FORM in p.read_text() for name, p in skills.items()}
    asks = {name: TOOL in p.read_text() for name, p in skills.items()}

    # A skill may reference the standard with the wrong path form — present but inert at runtime.
    for name, p in skills.items():
        body = p.read_text()
        if FRAGMENT in body and not references[name]:
            failures.append(
                f"skills/{name}/SKILL.md references the standard by a path that is not "
                f"{REQUIRED_FORM} — a bare path resolves against the user's project"
            )

    granting: dict[str, list[str]] = {}
    for cmd in sorted((REPO / "commands").glob("*.md")):
        text = cmd.read_text()
        if not _grants_tool(text):
            continue
        granting[cmd.stem] = _loaded_skills(text)

        exempt = _exemption(cmd)
        if exempt:
            continue
        if exempt == "":
            failures.append(f"commands/{cmd.name} claims an exemption with no usable reason")
            continue

        loaded = [s for s in granting[cmd.stem] if s in skills]
        if not loaded:
            failures.append(
                f"commands/{cmd.name} grants {TOOL} and loads no skill in this plugin — "
                f"nothing can carry the standard to it"
            )
            continue
        if not any(references[s] for s in loaded):
            if any(_exemption(skills[s]) for s in loaded):
                continue
            failures.append(
                f"commands/{cmd.name} grants {TOOL}, loads {', '.join(loaded)}, and none of those "
                f"references {FRAGMENT}"
            )

    # Direction B — an ask site no granting command can reach.
    for name, has_ask in sorted(asks.items()):
        if not has_ask:
            continue
        if _exemption(skills[name]):
            continue
        reachable = [c for c, loaded in granting.items() if name in loaded]
        if not reachable:
            failures.append(
                f"skills/{name}/SKILL.md calls {TOOL} and no command granting it loads that skill — "
                f"the ask is dead, and a refused tool looks like a skipped step"
            )

    if failures:
        print("FAIL  decision-request standard not wired")
        for f in failures:
            print(f"      {f}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
