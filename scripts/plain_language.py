"""The plain-language rule, split into the two halves that different surfaces need separately.

`skills/shared/decision-request.md` states the rule for an interrupting question: a bounded word count,
and no identifiers from a system the reader may not share. `hooks/decision-request/check-ask.py` enforces
both on every `AskUserQuestion` call.

**Three surfaces now want that rule and they do not want the same list.** Welding the ceiling to one
fixed vocabulary made it unusable by the second surface without copying it, and a fourth copy was the
alternative.

**The lists diverge in both directions, which is the part that survived measurement.** The board list
*drops* the card-number class and *adds* `BARE_HANDLE`, which the hook omits deliberately — denying a
stranger's question over their own vocabulary would refuse real work for a local reason, while a composed
summary leaning on a handle has passed the reader a lookup instead of an answer.

*An earlier version of this header argued the split was needed because "a board read must print `#34`".
Measured 2026-09-08 and refuted: no hand-composed description used `#N` at all, because the number has
its own column. The permission survives for a better reason — forbidding `#34` renames it to `card 34`
rather than removing it — and the split survives on the divergence above, not on that claim.*

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

# A handle of the shape LETTERS then DIGITS, hyphen optional — `ADR-013`, `DDD-7`, `Mandate-12`, and
# bare `D11`, which is how this repo actually writes its decision numbers. Opaque in any project: it
# names a record the reader has to resolve before the sentence containing it means anything.
#
# **The first draft required two or more letters and missed `D11` entirely** — the one spelling the repo
# uses, so the guard was blind to its own house style while its fixture tested shapes nobody writes.
#
# Known false positives, recorded rather than discovered: `Python-3`, `COVID-19`, `Section-4`, `K8`. The
# class name says *decision handle* and the pattern says *letters then digits*, which are not the same
# thing. Tolerated because this check is build-time only and a false positive costs a rephrase, never a
# denial. A runtime consumer would need a narrower pattern, and should not reuse this one unexamined.
BARE_HANDLE = ("a bare decision handle", re.compile(r"\b[A-Z][A-Za-z]*-?\d+\b"))

# What a COMPOSED board description may not contain. Built from the portable classes rather than
# beside them, so the two lists cannot drift apart.
#
# Two differences from the hook's list, and both are the point of taking `forbid` as an argument:
#
#   - **A card number is permitted**, by being absent here — because forbidding it would only launder
#     it. A composer told not to write `#34` writes `card 34`, which no pattern catches and which means
#     the same thing. An interrupting question is different: there the reader was doing something else a
#     second ago, and the number is noise rather than a column heading.
#   - **A bare handle is added.** The hook omits it deliberately — denying a stranger's question over
#     their own vocabulary would refuse real work for a local reason. A composed *summary* is different:
#     the text is this tool's, not the filer's, and a summary that leans on a handle has passed the
#     reader a lookup instead of an answer.
#
# What is NOT here, recorded so the absence is not read as an oversight: wave labels, slice ids and
# other project-local vocabulary. They are jargon in this repo and are ordinary domain words elsewhere,
# so machine-forbidding them would repeat the failure the hook's header already documents. The skill
# names them as prose guidance instead, and says they are unenforced.
BOARD_DESCRIPTION_FORBIDDEN = [
    (name, pattern) for name, pattern in PORTABLE_IDENTIFIERS
    if name != "an issue or ticket number"
] + [BARE_HANDLE]


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
