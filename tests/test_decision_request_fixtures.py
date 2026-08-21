"""Mechanical tests for the `decision-request` shared standard and its fixtures.

Most of what `skills/shared/decision-request.md` asserts is a reading — whether an ask is *well
framed* cannot be counted, and this file does not pretend otherwise. Two things can be counted, and
they are the two the standard makes load-bearing:

  - the 200-word ceiling on the ask (hard, per the feature's [D4]);
  - the absence of internal vocabulary in the ask (per C2).

Both are RE-DERIVED here on every run rather than read out of the manifest. A fixture that recorded a
count and never recomputed it would drift the first time anyone edited `ask.md` — the same shape as
`check-product-ssot.py` reporting "all resolve" for a persona file that does not parse.

The reference check (`test_the_fragment_is_actually_referenced`) is deliberately shallow and says so:
it proves a skill loads the standard, never that the skill's asks conform. Slice 03 owns the
build-level version of that check and inherits the same limitation.
"""

import json
import re
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
FRAGMENT = REPO / "skills" / "shared" / "decision-request.md"
FIXTURES = sorted((REPO / "skills" / "shared" / "self-test" / "decision-request").glob("*/manifest.json"))

# The one live outcome as of slice 01. Slice 02 adds the failing ones; a fixture naming an outcome
# that does not appear here is drift, not a new case.
LIVE_OUTCOMES = {"CONFORMS"}

# C2 — internal vocabulary forbidden in the ask. The rule is ABSENCE, not explanation, so these are
# matched on sight and not excused by surrounding prose.
FORBIDDEN = {
    "wave label": re.compile(r"\bwave:\s*\w+", re.I),
    "issue number": re.compile(r"#\d+"),
    "slice id": re.compile(r"\bslice\s*\d+\b", re.I),
    "decision number": re.compile(r"\[D\d+\]|\bD\d+\b"),
    "skill or command name": re.compile(r"/phil:|\bAskUserQuestion\b|\bnw-\w+|\bplugin-dev\b"),
    "artifact path": re.compile(r"\S+/\S+\.(?:md|py|ya?ml|json)|\$\{CLAUDE_PLUGIN_ROOT\}"),
}


def _words(text):
    """Word count, matching `wc -w` — whitespace-separated tokens."""
    return len(text.split())


def test_the_fragment_exists():
    assert FRAGMENT.is_file(), f"the standard is missing: {FRAGMENT}"


def test_the_fragment_carries_no_frontmatter():
    """`skills/shared/` deliberately holds no SKILL.md, per its README — a fragment with frontmatter
    would read as a registrable skill. `test-runner-detection.md` is the precedent."""
    assert not FRAGMENT.read_text().startswith("---"), (
        "a shared fragment must not carry YAML frontmatter"
    )


def test_the_fragment_states_the_ceiling_and_what_enters_the_count():
    """[D4] made unambiguous. The first version said "Count the framing" and then offered "cut
    options" as the remedy — cutting something the count excluded. Three readers, three counts.
    A ceiling whose scope is undefined is not countable, whatever it calls itself."""
    body = FRAGMENT.read_text()
    assert "200 words, hard" in body, "the ceiling must be stated as hard, not as a target"
    assert "option label and option description" in body, (
        "the count's scope must name option labels AND descriptions — the ambiguity that shipped first"
    )
    assert "wc -w" in body, "a countable ceiling must name its counting method"
    assert "What does not:" in body, "the exclusions must be stated, not implied"


def test_the_remedy_never_sacrifices_the_framing():
    """The ordering that keeps the ceiling from being applied backwards."""
    body = FRAGMENT.read_text()
    assert "Never cut items 3–5 to fit" in body


def test_context_goes_above_and_the_reason_is_stated():
    """[D5] as amended 2026-08-21. "Sits below" was unimplementable: the tool call blocks, so anything
    after it arrives once the answer is already given. Detail goes ABOVE, and the fragment must say why
    — otherwise the next author 'tidies' it back below."""
    body = FRAGMENT.read_text()
    assert "Context goes **above**, not below" in body
    assert "blocks" in body, "the reason the ordering is forced must be stated"
    assert "bounded in practice, not unbounded" in body, (
        "the accepted cost of context-above must be stated: length above the ask buries it too"
    )


def test_placement_has_an_observable():
    """[D9]. Placement was declared failable and given no observable — two instances would emit
    different separators and both believe they conformed. The marker line is that observable."""
    body = FRAGMENT.read_text()
    assert "A marker line" in body
    assert "Nothing between the framing and the call" in body


def test_the_two_ask_cap_is_stated():
    """Without it the fragment licensed an unbounded re-ask loop that `groom-issues` calls "the nagging
    that teaches people to stop running the tool" — duplication with drift, on day one."""
    body = FRAGMENT.read_text()
    assert "After a second unanswered ask" in body
    assert "Two asks is the limit" in body


def test_no_command_name_exception():
    """The prose once permitted "naming a command the reader is about to run" while FORBIDDEN matches
    command names on sight. Prose and oracle must not disagree: one reader follows each."""
    body = FRAGMENT.read_text()
    assert "no command names" in body
    assert "not a violation" not in body, (
        "an exception in the prose that the oracle does not honour is a contradiction, not a nuance"
    )
    # And the claim the fragment makes about the oracle must be true of the oracle.
    assert FORBIDDEN["skill or command name"].search("run /phil:groom-set next"), (
        "the fragment tells readers command names are matched on sight — the regex must actually do it"
    )


def test_the_fragment_does_not_overclaim_its_reach():
    """[D11], and the one sentence that should not have shipped: "in force deterministically" claimed
    compliance where only DELIVERY is guaranteed. Both new-line tests below are quotes from the repo's
    own test docstrings, which said it correctly before the fragment did."""
    body = FRAGMENT.read_text()
    assert "Delivery is deterministic" in body and "compliance is not" in body
    assert "must not be described as covered" in body
    assert "Propagation is incomplete" in body, (
        "Reach named the gap outside a command and stayed silent on the larger gap on its own side"
    )


def test_fixtures_exist():
    assert FIXTURES, "slice 01 ships one conforming baseline fixture"


@pytest.mark.parametrize("manifest", FIXTURES, ids=lambda p: p.parent.name)
def test_manifest_parses_and_has_its_companions(manifest):
    d = json.loads(manifest.read_text())
    assert d.get("fixture_id"), "every fixture names itself"
    assert (manifest.parent / "expected.md").exists()
    assert (manifest.parent / d["ask_file"]).exists()


@pytest.mark.parametrize("manifest", FIXTURES, ids=lambda p: p.parent.name)
def test_expected_decision_is_exactly_one_live_outcome(manifest):
    d = json.loads(manifest.read_text())
    dec = d["expected_decision"]
    assert len(dec) == 1, f"{d['fixture_id']} expects {dec} — exactly one outcome"
    assert dec[0] in LIVE_OUTCOMES, f"{dec[0]} is not a live outcome"


@pytest.mark.parametrize("manifest", FIXTURES, ids=lambda p: p.parent.name)
def test_the_ask_is_within_the_ceiling(manifest):
    """[D4] made countable. This is the assertion the whole hard-ceiling decision rests on."""
    d = json.loads(manifest.read_text())
    ask = (manifest.parent / d["ask_file"]).read_text()
    ceiling = d["mechanical_assertions"]["word_ceiling"]
    count = _words(ask)
    assert count <= ceiling, (
        f"{d['fixture_id']}: ask is {count} words, ceiling is {ceiling}. "
        "Over is a failure, not a warning — cut options or split the decision, never the framing."
    )


@pytest.mark.parametrize("manifest", FIXTURES, ids=lambda p: p.parent.name)
def test_the_recorded_count_still_matches_the_file(manifest):
    """Catches manifest drift. Recording a number and never re-deriving it is how a fixture starts
    certifying a file it no longer describes."""
    d = json.loads(manifest.read_text())
    ask = (manifest.parent / d["ask_file"]).read_text()
    recorded = d["mechanical_assertions"]["measured_words"]
    actual = _words(ask)
    assert recorded == actual, (
        f"{d['fixture_id']}: manifest records {recorded} words, {d['ask_file']} has {actual}"
    )


@pytest.mark.parametrize("manifest", FIXTURES, ids=lambda p: p.parent.name)
def test_the_ask_contains_no_internal_vocabulary(manifest):
    """C2 — absence, not explanation. An explained label is still a label the reader must hold."""
    d = json.loads(manifest.read_text())
    ask = (manifest.parent / d["ask_file"]).read_text()
    hits = {kind: pat.findall(ask) for kind, pat in FORBIDDEN.items() if pat.search(ask)}
    assert not hits, f"{d['fixture_id']}: forbidden vocabulary in the ask — {hits}"
    expected_zero = d["mechanical_assertions"]["forbidden_token_count"]
    assert expected_zero == 0, "a fixture expecting forbidden tokens is a slice-02 failing fixture"


def test_the_fragment_is_actually_referenced():
    """Slice 01 AC2 — and the shallowest assertion in this file, deliberately.

    It proves a skill LOADS the standard. It does not and cannot prove that skill's asks conform.
    Slice 03's build check inherits exactly this limitation and its header says so too; recording the
    gap in both places is what keeps a green run from reading as conformance.
    """
    referencing = [
        p for p in (REPO / "skills").glob("*/SKILL.md")
        if "shared/decision-request.md" in p.read_text()
    ]
    assert referencing, "no skill references the standard — the fragment is inert"
