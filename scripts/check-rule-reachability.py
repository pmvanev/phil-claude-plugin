#!/usr/bin/env python3
"""Fail when a rule in `rules/` is reachable by nothing.

Plugin-shipped rules do NOT auto-load. Measured 2026-08-31 against Claude Code 2.1.252: the plugin
manifest's component list carries no `rules` key, and every call site of the rules-directory loader
passes `~/.claude/rules`, the managed directory, or `<projectRoot>/.claude/rules` — never a plugin
root. So a rule reaches a session only because a skill, command or agent names it and reads it.

That makes an unnamed rule inert, and inert in the worst way: it ships to every consumer, it looks
like a standard, and nothing reports that nobody applies it. A standard nobody runs reports
compliance by staying quiet.

Reachability is transitive. A rule named by a loader is reachable; a rule cited by a reachable rule
is reachable too, because the citing rule is in context when it points at it.

**What this cannot check.** It verifies a rule is *mentioned*, not that anything *applies* it. Every
one of `ui.md`'s mentions is an exclusion — `ux.md` and `ux-review` name it four times to say
aesthetics are NOT reviewed there — and the check counts that as reachable. Distinguishing "go read
this" from "do not apply this here" is prose judgement, and a check that faked it would pass because
the field is populated, which is this repo's recorded shallow-check defect. Stated here rather than
hidden, on the pattern of the decision-request hook's header.

`KNOWN_UNREACHED` is the honest escape hatch, and it is checked in BOTH directions: an entry naming
a rule that no longer exists fails, and so does an entry for a rule that has since been wired up —
otherwise the list rots into a permanent excuse.
"""

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
LOADERS = ("skills", "commands", "agents")

# Deliberately applied by nobody. Each entry states why, and is removed the day something names it.
KNOWN_UNREACHED = {
    "llm-inference": "documents itself as manual reference material with no honest glob",
    "definitions": "a glossary for the other rules; only `llm-inference.md` cites it, and that is "
                   "unreachable too, so nothing puts it in context on its own",
}


def _cited(text: str) -> set[str]:
    """A loader names a rule by path: `rules/coding.md`."""
    return set(re.findall(r"rules/([A-Za-z0-9._-]+)\.md", text))


def _cited_sibling(text: str) -> set[str]:
    """Inside `rules/`, a sibling is cited bare — ``definitions.md``, not ``rules/definitions.md``."""
    return set(re.findall(r"`([A-Za-z0-9._-]+)\.md`", text))


def main() -> int:
    rules_dir = REPO / "rules"
    rules = {p.stem for p in rules_dir.glob("*.md")}
    if not rules:
        print("no rules/*.md found — is the layout right?")
        return 1

    reachable = set()
    for area in LOADERS:
        for path in (REPO / area).rglob("*.md"):
            reachable |= _cited(path.read_text(errors="ignore")) & rules

    # transitive: a reachable rule that cites another puts it in context too
    frontier = set(reachable)
    while frontier:
        nxt = set()
        for name in frontier:
            f = rules_dir / f"{name}.md"
            if f.exists():
                body = f.read_text(errors="ignore")
                nxt |= ((_cited(body) | _cited_sibling(body)) & rules) - reachable
        reachable |= nxt
        frontier = nxt

    problems = []
    for name in sorted(rules - reachable - set(KNOWN_UNREACHED)):
        problems.append(f"rules/{name}.md is named by nothing and is not a declared exception")
    for name in sorted(set(KNOWN_UNREACHED) - rules):
        problems.append(f"KNOWN_UNREACHED names rules/{name}.md, which does not exist")
    for name in sorted(set(KNOWN_UNREACHED) & reachable):
        problems.append(f"rules/{name}.md is now reachable — drop it from KNOWN_UNREACHED")

    if problems:
        for p in problems:
            print(p)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
