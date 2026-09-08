"""The plain-language rule, split into the two halves that different surfaces need separately.

`skills/shared/decision-request.md` states the rule for an interrupting question: a bounded word count,
and no identifiers from a system the reader may not share. `hooks/decision-request/check-ask.py` enforces
both on every `AskUserQuestion` call.

**Three surfaces now want that rule and they do not want the same half.** An interrupting ask must not
print `#34` — measured, and the reason the vocabulary check exists. A board read *must* print `#34`,
because the number is how a reader finds the card. Welding the ceiling to one fixed vocabulary list made
the rule unusable by the second surface without copying it, and a fourth copy was the alternative.

So the two halves are independent here:

- `words` and `over_ceiling` — arithmetic, no judgement, no vocabulary at all.
- `identifiers_in` — the vocabulary half, taking the forbidden classes as an argument and a `permit`
  list for the classes a given surface requires.

**This module changes no rule.** The hook's `PORTABLE` list moved here verbatim and the hook's behaviour
is unchanged, which `tests/test_decision_request_hook.py` proves by driving the hook as a subprocess.

**What this module cannot do, stated because the gap is invisible otherwise.** The hook enforces at
runtime because an `AskUserQuestion` payload is structured data arriving at a tool call. A command's
rendered terminal output is not a tool call and reaches no hook, so for `phil:board-snapshot` this module
is a *build-time* mechanism — used by fixtures — and the runtime half is prose in the skill. Half
enforced and half promised, on the pattern `groom-issues` already records about its own read-only claim.
"""

from __future__ import annotations

import re

DEFAULT_CEILING = 200

# Identifier classes that are jargon in ANY project. This repo's own identifiers are deliberately
# absent: denying on them would refuse a stranger's question for a local reason. Moved verbatim from
# hooks/decision-request/check-ask.py, where it was measured against 73 real asks before shipping.
PORTABLE_IDENTIFIERS = [
    ("an issue or ticket number", re.compile(r"#\d+")),
    ("a file path", re.compile(
        r"(?<!//)(?<!\.)\b[\w.-]+/[\w./-]*\.\w{1,5}\b|\b\w[\w.-]*\.(?:md|py|ya?ml|json|ts|tsx|js|go|rs)\b")),
    ("a bracketed identifier", re.compile(r"\[[A-Z]+-?\d+\]")),
]

# A URL is a link the reader can open, not an identifier from a system they may not share.
URL = re.compile(r"https?://\S+")


def words(text) -> int:
    """Whitespace-separated token count. The hook's counting rule, unchanged."""
    return len(str(text or "").split())


def over_ceiling(text, ceiling: int = DEFAULT_CEILING) -> int | None:
    """Return the word count when it exceeds `ceiling`, else None.

    Returning the count rather than a bool is deliberate: every caller that reports a breach has to say
    how far over it went, and a bool forces the caller to recount.
    """
    count = words(text)
    return count if count > ceiling else None


def identifiers_in(text, forbid=PORTABLE_IDENTIFIERS, permit=()) -> list[str]:
    """Names of the forbidden identifier classes present in `text`, sorted, minus anything permitted.

    `permit` holds class NAMES, not patterns, so a caller declares what it needs in the same vocabulary
    the finding is reported in — `permit=["an issue or ticket number"]` for a surface whose whole job is
    printing card numbers. A permitted class is not scanned for at all; it is not a finding downgraded.
    """
    scannable = URL.sub(" ", str(text or ""))
    permitted = set(permit)
    return sorted({
        name for name, pattern in forbid
        if name not in permitted and pattern.search(scannable)
    })
