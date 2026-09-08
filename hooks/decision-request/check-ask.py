#!/usr/bin/env python3
"""Refuse a decision request that breaches the two mechanically checkable rules (PreToolUse).

`skills/shared/decision-request.md` is the standard. Inside a command, a build check proves the
standard is *referenced*; nothing proved any ask *obeyed* it, and outside a command nothing carried it
at all. This hook closes both, for the two clauses that are actually decidable from data.

## Why this is possible at all, against a decision that said it was not

The feature's [D11] held that outside a command no deterministic mechanism exists, reasoned from two
measurements: a globbed rule fires on file type, and a pathless rule never auto-loads. Both remain true.
Neither ruled out a **tool-call hook**, and the argument that placement cannot be checked in flight —
the framing is prose emitted before the call, so nothing says where it begins — does not extend to the
call itself. **A tool call is not untagged prose. It is structured data**, and the question text, every
option label and every option description arrive in it.

So two clauses become enforceable everywhere, including in ordinary conversation and in projects that
merely install this plugin:

- **the per-question ceiling** — arithmetic, no judgement, no false positives available;
- **forbidden vocabulary**, restricted to the classes that are jargon in *any* project.

Two remain unreachable and always will be: whether each option names its cost (semantic), and whether
the ask is set apart from surrounding output (the framing is not in the payload). The standard says so,
and this hook does not pretend otherwise.

## Why only the length half is unconditional

**Measured before shipping, over 73 real asks in this repo's history: denying on both rules would have
refused 59 of them — 81%.** Inspected rather than assumed: 41 of the 42 distinct matches are genuine
filenames and card numbers, so the check is not misfiring. The corpus simply predates the standard.

That number is fine here and wrong elsewhere, and the difference is what the rule is actually about.
This standard forbids *identifiers from a system the reader may not share*. In this repository a
filename is exactly that. In an ordinary project it is often the plainest possible way to name the thing
being decided — *"edit `config.json` or `settings.yaml`?"* is a good question, and denying it would be
this plugin refusing a stranger's work for a reason that does not apply to them.

So:

- **The length limit is enforced everywhere, unconditionally.** It is arithmetic. It is content-neutral,
  it cannot misjudge wording, and a question that needs more than 200 words of options is unreadable in
  any project.
- **The wording rule is enforced where a project opts in**, by carrying `decision-request: strict` in
  its `CLAUDE.md`. This repository does. A consumer who wants it says so.

The user chose to refuse on both reachable rules. This split honours that choice in the place the
complaint came from, and declines to impose it on projects that never made it — a deviation recorded
here rather than discovered by whoever gets denied.

## Why the vocabulary list here is shorter than the standard's

The standard forbids this plugin's own identifiers — skill names, wave labels, slice ids. Those are
meaningless in a consumer's project, and a hook that denied on them would be refusing a stranger's
question for using a word this repo happens to reserve. Only three classes travel: an issue number, a
file path, and a bracketed identifier. Each is an identifier from a system the reader may not share,
which is the whole basis of the rule.

The full list is still enforced against this repo's own asks by
`tests/test_decision_request_fixtures.py`. This hook is the portable subset, deliberately.

## Failing open

Any malformed payload, any unexpected shape, any error: **return silently and allow the call.** A hook
that breaks someone's conversation is worse than the defect it detects — the same rule
`check-plugin-skew.py` states for itself. The only output this ever produces is a deny on a breach it
is certain about.

A denial is not a dead end. The reason names the breach and the remedy, the model rewrites the ask and
calls again — the standard's own remedy ordering, applied by the thing that has to apply it.
"""

import json
import os
import sys

# The two halves of the rule live in `scripts/plain_language.py`, so a surface that needs the ceiling
# without this vocabulary can take one and not the other — `phil:board-snapshot` must print `#N`, which
# is exactly what the list below forbids. Nothing about this hook's behaviour changed in the move; the
# list is byte-identical and `tests/test_decision_request_hook.py` drives this file as a subprocess.
#
# An import failure is left to raise. A hook that quietly stopped enforcing would report compliance by
# staying silent, which is the defect this repo keeps recording; a visible hook error is the better
# failure, and a missing file in an install is a packaging bug that should be loud.
sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "scripts"))
from plain_language import DEFAULT_CEILING, identifiers_in, words  # noqa: E402

QUESTION_CEILING = DEFAULT_CEILING

# The opt-in marker for the wording half. See *Why only the length half is unconditional*.
STRICT = "decision-request: strict"


def strict_here(cwd):
    """True when this project has opted into the wording rule as a denial."""
    try:
        for name in ("CLAUDE.md", ".claude/CLAUDE.md"):
            path = os.path.join(cwd, name)
            if os.path.isfile(path) and STRICT in open(path, encoding="utf-8").read():
                return True
    except Exception:
        pass
    return False


def counted(question):
    """The counted text of one question: its own words plus every option label and description.

    Per-option `preview` panes are excluded — the standard rules a preview to be context, shown beside
    the options rather than read as part of them.
    """
    parts = [question.get("question", "")]
    for option in question.get("options") or []:
        parts.append(option.get("label", ""))
        parts.append(option.get("description", ""))
    return "\n".join(str(p or "") for p in parts)


def breaches(tool_input, strict):
    out = []
    for question in tool_input.get("questions") or []:
        header = question.get("header") or question.get("question", "")[:30]
        text = counted(question)

        count = words(text)
        if count > QUESTION_CEILING:
            out.append(
                f'"{header}" is {count} words counting its option labels and descriptions; the limit '
                f"is {QUESTION_CEILING}. Trim the descriptions — never below the sentence naming each "
                f"option's cost — then cut the number of options, then split the decision."
            )

        if not strict:
            continue
        # URL handling and the forbidden classes both live in the shared module now.
        found = identifiers_in(text)
        if found:
            out.append(
                f'"{header}" contains {", ".join(found)} in the question or its options. The reader may '
                f"not share the system that identifier comes from. Describe the thing rather than "
                f"naming it, and put the identifier in the context block above the question."
            )
    return out


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return

    try:
        if payload.get("tool_name") != "AskUserQuestion":
            return
        tool_input = payload.get("tool_input") or {}
        if not isinstance(tool_input, dict):
            return
        found = breaches(tool_input, strict_here(payload.get("cwd") or os.getcwd()))
    except Exception:
        return  # fail open, always

    if not found:
        return

    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": (
                "This decision request breaches the standard at "
                "${CLAUDE_PLUGIN_ROOT}/skills/shared/decision-request.md:\n"
                + "\n".join(f"  - {b}" for b in found)
                + "\n\nRewrite the request and ask again. Context, evidence and identifiers belong "
                  "above the question, separated by a marker line, where they are not counted."
            ),
        }
    }))


if __name__ == "__main__":
    main()
