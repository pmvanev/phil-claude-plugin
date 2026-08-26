"""Mechanical tests for the `decision-request` shared standard and its fixtures.

Four clauses of `skills/shared/decision-request.md` are countable, and this file counts them:

  - **OVER-CEILING** — the framing over 200 words, or any single question (its own text plus its
    option labels and descriptions) over 200. Two limits, not one; the single combined limit that
    shipped in slice 01 was refuted by measurement and the numbers are in the fragment.
  - **JARGON-WALL** — internal vocabulary anywhere in the counted ask (per C2). Absence, not
    explanation.
  - **BARE-LIST** — one or more of items 3–5 absent from the framing. The failure names the missing
    element, never a count: a bare list is not a length defect, and fixture 02 proves it by passing
    both ceilings with room while carrying no decision and no consequence at all.
  - **BURIED-ASK** — a placement defect: no marker before the framing, text interposed between the
    framing and the call, or the regions out of order.

**Every number is re-derived here on every run**, never read out of the manifest, and
`test_the_manifest_still_describes_the_files` asserts the two agree. A fixture that recorded a count
and never recomputed it would drift the first time anyone edited it — the same shape as
`check-product-ssot.py` reporting "all resolve" for a persona file that does not parse.

## What these checks do NOT do, stated once

They read **fixtures**, never a live ask, and no check could read a live ask. A fixture's regions are
tagged by hand once (see `skills/shared/self-test/decision-request/README.md`); inside an untagged turn
there is nothing that says where the framing begins, and position does not reveal it either — measured
across 72 real asks in this repo's history, the paragraph immediately before the call runs 82 words or
fewer in 70 of them. So a green run here means *the standard and its recorded examples still agree*. It
does not mean any ask in flight conforms, and the fragment's *Reach* section says so in the same words.

BARE-LIST inherits one further limit worth naming: it fires on an element that is **absent**, not on one
that is present and weak. A tagged `consequence` region saying "this matters" would pass. The tag is a
reading; only its presence is mechanical.
"""

import json
import re
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
FRAGMENT = REPO / "skills" / "shared" / "decision-request.md"
SELFTEST = REPO / "skills" / "shared" / "self-test" / "decision-request"
FIXTURES = sorted(SELFTEST.glob("*/manifest.json"))

FRAMING_CEILING = 200
QUESTION_CEILING = 200

# The live outcomes. A fixture naming anything else is drift, not a new case.
LIVE_OUTCOMES = {"CONFORMS", "BARE-LIST", "JARGON-WALL", "BURIED-ASK", "OVER-CEILING"}
FAILURE_MODES = LIVE_OUTCOMES - {"CONFORMS"}

# The three counted framing elements, in the order the fragment mandates.
FRAMING_REGIONS = ("interrupted", "decision", "consequence")
# decision and consequence share a rank: they repeat, alternating, once per question, so ranking them
# separately would read every legitimate multi-question emission as out of order. Their alternation is
# checked on its own.
REGION_ORDER = {"context": 0, "marker": 1, "interrupted": 2, "decision": 3, "consequence": 3}

# C2 — internal vocabulary forbidden in the counted ask. Matched on sight, never excused by
# surrounding prose, and NEVER applied to the context block, which exists to carry exactly these.
def _local_names():
    """This plugin's own identifiers — skill and command names, job ids, persona names — longest first.

    Derived from disk rather than listed. The first version hard-coded four spellings, so
    `groom-issues`, `board-setup`, `single-issue-per-feature` and `adversarial-review` passed clean
    through the rule that forbids skill names, inside the very fixture whose job is to demonstrate
    them.

    **Only hyphenated names are matched, and that is a deliberate floor.** Derived unfiltered, this
    list holds `work`, `resume`, `refactor`, `stack`, `design` and `run` — real skill and command
    names that are also ordinary English words. Matching those turned three genuinely clean fixtures
    into vocabulary failures on the word "work". A hyphenated compound is unmistakably an identifier;
    a bare English word is indistinguishable from prose, so it is left to the reader.

    What that floor costs, stated rather than discovered: a single-word skill name used AS a name —
    "run `work` next" — is not caught. The rule in the fragment is wider than this check, and the
    fragment says so.
    """
    names = {d.name for d in (REPO / "skills").iterdir() if (d / "SKILL.md").exists()}
    names |= {p.stem for p in (REPO / "commands").glob("*.md")}
    names |= {p.stem for p in (REPO / "docs" / "product" / "personas").glob("*.yaml")}
    jobs = (REPO / "docs" / "product" / "jobs.yaml")
    if jobs.exists():
        names |= set(re.findall(r"^\s*-\s*id:\s*([\w-]+)", jobs.read_text(), re.M))
    return sorted((n for n in names if "-" in n), key=len, reverse=True)


FORBIDDEN = {
    "wave label": re.compile(r"\bwave:\s*\w+|\bwave\b(?=\s+(?:discuss|design|distill|deliver|discover|diverge|devops))", re.I),
    "issue number": re.compile(r"#\d+"),
    "slice id": re.compile(r"\bslice\s*\d+\b", re.I),
    "decision number": re.compile(r"\[D\d+\]|\bD\d+\b"),
    "skill or command name": re.compile(
        r"/phil:|\bAskUserQuestion\b|\bnw-\w+|\bplugin-dev\b|\b(?:"
        + "|".join(re.escape(n) for n in _local_names()) + r")\b"),
    "artifact path": re.compile(
        r"\S*/\S*\.(?:md|py|ya?ml|json)|\b\w[\w.-]*\.(?:md|py|ya?ml|json)\b"
        r"|\$\{CLAUDE_PLUGIN_ROOT\}|\b(?:scripts|skills|commands|agents|rules|docs)/"),
}

BANNER = "<!-- decision-request-emission:v1 -->"
CALL = "<!-- call -->"
# Content may sit on the tag's own line or start on the next one — the register documents the first
# spelling and every recorded fixture uses the second. A parser that accepted only one of them made
# the register's own worked example parse to a single region.
REGION_RE = re.compile(r"<!-- (\w+) -->[ \t]*\n?(.*?)\n?[ \t]*<!-- /\1 -->", re.S)


def _prose(path=None):
    """The fragment as one whitespace-collapsed line.

    Every prose assertion below reads this rather than the raw text. Asserting exact substrings
    against wrapped markdown makes a re-wrap turn the suite red for a reason unrelated to the
    standard — and it did, three times in one commit. Line breaks are not part of any claim here.
    """
    return " ".join((path or FRAGMENT).read_text().split())


def _words(text):
    """Word count, matching `wc -w` — whitespace-separated tokens."""
    return len(text.split())


def _parse_emission(text):
    """Split a tagged emission into (before, after, trailing).

    `before` is an ordered list of `(region, body)` **from before the call**, repeats preserved;
    `after` names any region emitted past it; `trailing` is the text between the last region and the
    call.

    Three things this signature exists to get right, each of which the first version got wrong:

    - **Partition before parsing.** Parsing the whole file and only then splitting on the call meant a
      `consequence` emitted AFTER the blocking call counted as present — the ask scored `CONFORMS`
      while its consequence was unreachable, which is the precise failure the context-goes-above
      amendment exists to prevent.
    - **Keep repeats.** A turn putting three questions needs three decision/consequence pairs. A dict
      kept the last of each, so an empty region followed by a filled one hid.
    - **Validate the frame.** The banner is part of the documented format and the call sentinel must
      appear exactly once; neither was checked, so a `v2` emission or one with two calls parsed
      silently.
    """
    if not text.lstrip().startswith(BANNER):
        raise AssertionError(f"a tagged emission must open with {BANNER}")
    if text.count(CALL) != 1:
        raise AssertionError(f"expected exactly one {CALL} sentinel, found {text.count(CALL)}")
    head, _, tail = text.partition(CALL)
    before = [(m.group(1), m.group(2)) for m in REGION_RE.finditer(head)]
    after = [m.group(1) for m in REGION_RE.finditer(tail)]
    closes = [head.rindex(f"<!-- /{n} -->") for n, _ in before]
    trailing = head[max(closes):].split("-->", 1)[1] if closes else head
    return before, after, trailing


def _bodies(before, name):
    """Every body tagged `name`, in order, stripped. Empty bodies are dropped — an empty region is
    an absent one, and BARE-LIST must not be satisfied by a tag with nothing inside it."""
    return [b.strip() for n, b in before if n == name and b.strip()]


def _counted_text(ask, options):
    """The counted ask: the framing, plus every question's own text and option label/description.

    Per-option `preview` panes are excluded — the fragment rules them context, shown beside the
    options rather than read as part of them.
    """
    parts = [ask]
    for q in options["questions"]:
        parts.append(q["question"])
        for o in q["options"]:
            parts.append(o["label"])
            parts.append(o["description"])
    return "\n".join(parts)


def _question_groups(options):
    return [
        _words(q["question"]) + sum(_words(o["label"]) + _words(o["description"]) for o in q["options"])
        for q in options["questions"]
    ]


def framing_matches_ask(fixture_dir):
    """True when ask.md is the tagged framing regions, word for word.

    **Word sequence, not bytes.** A decision and its consequence can fall either side of a clause
    break inside one recorded sentence — fixture 05 does, three times — so a byte comparison would
    force either a rewritten recording or a region boundary in the wrong place. Comparing the word
    sequence keeps the recording verbatim while still proving the counted text and the read text are
    the same text, which is the only thing this invariant is for.

    Lifted out of its test so a deliberately-inconsistent fixture can prove the rule fires. Asserted
    only where every fixture already complies, it was a rule nothing exercised.
    """
    manifest = json.loads((fixture_dir / "manifest.json").read_text())
    before, _, _ = _parse_emission((fixture_dir / manifest["emission_file"]).read_text())
    rebuilt = " ".join(" ".join(b.split()) for n, b in before
                       if n in FRAMING_REGIONS and b.strip())
    ask = " ".join((fixture_dir / manifest["ask_file"]).read_text().split())
    return rebuilt == ask


def evaluate(fixture_dir):
    """Apply the four countable clauses. Returns {mode: human-readable reason}.

    Placement and framing-presence are skipped where no emission is recorded, and the manifest must
    say so — a silently skipped check is the defect this repo keeps finding.
    """
    manifest = json.loads((fixture_dir / "manifest.json").read_text())
    ask = (fixture_dir / manifest["ask_file"]).read_text()
    options = json.loads((fixture_dir / manifest["options_file"]).read_text())
    findings = {}

    # --- OVER-CEILING: two limits, counted separately.
    framing = _words(ask)
    breaches = []
    if framing > FRAMING_CEILING:
        breaches.append(f"framing is {framing} words, limit is {FRAMING_CEILING}")
    breaches += [f"question {q['header']!r} is {g} words with its options, limit is {QUESTION_CEILING}"
                 for q, g in zip(options["questions"], _question_groups(options))
                 if g > QUESTION_CEILING]
    if breaches:
        findings["OVER-CEILING"] = "; ".join(breaches)

    # --- JARGON-WALL: the counted ask only. The context block is exempt by design.
    hits = {kind: pat.findall(_counted_text(ask, options))
            for kind, pat in FORBIDDEN.items() if pat.search(_counted_text(ask, options))}
    if hits:
        findings["JARGON-WALL"] = f"internal vocabulary in the counted ask — {hits}"

    emission_file = manifest.get("emission_file")
    if not emission_file:
        return findings

    before, after, trailing = _parse_emission((fixture_dir / emission_file).read_text())
    order = [n for n, _ in before]
    n_questions = len(options["questions"])

    # --- BARE-LIST: names the missing element, never a count.
    #
    # One `interrupted` for the turn, then a decision AND a consequence for EVERY question. The
    # per-question shape is what catches "three questions, one framed" — the defect the singular
    # first version could not see, because one tagged pair satisfied a three-decision ask.
    missing = []
    if not _bodies(before, "interrupted"):
        missing.append("line naming what this interrupted")
    for region, label in (("decision", "statement of what is being decided"),
                          ("consequence", "statement of what turns on it")):
        got = len(_bodies(before, region))
        if got < n_questions:
            missing.append(f"{label} for {n_questions - got} of {n_questions} question(s)")
    if missing:
        findings["BARE-LIST"] = (
            "framing incomplete — no " + "; no ".join(missing)
            + f" (the ask is {framing} words and inside both ceilings, so no count would catch this)")

    # --- BURIED-ASK: placement, four ways.
    reasons = []
    if not _bodies(before, "marker"):
        reasons.append("no marker line before the framing")
    if trailing.strip():
        reasons.append(f"text between the framing and the call: {trailing.strip()[:60]!r}")
    if after:
        reasons.append(f"framing emitted AFTER the call, where it cannot be read: {after}")
    ranked = [REGION_ORDER[r] for r in order if r in REGION_ORDER]
    if ranked != sorted(ranked):
        reasons.append(f"regions out of order: {order}")
    pairs = [n for n in order if n in ("decision", "consequence")]
    if pairs and pairs != ["decision", "consequence"] * (len(pairs) // 2):
        reasons.append(f"decision/consequence pairs do not alternate: {pairs}")
    if reasons:
        findings["BURIED-ASK"] = "; ".join(reasons)

    return findings


# --------------------------------------------------------------------------- the fragment


def test_the_fragment_exists():
    assert FRAGMENT.is_file(), f"the standard is missing: {FRAGMENT}"


def test_the_fragment_carries_no_frontmatter():
    """`skills/shared/` deliberately holds no SKILL.md, per its README — a fragment with frontmatter
    would read as a registrable skill. `test-runner-detection.md` is the precedent."""
    assert not FRAGMENT.read_text().startswith("---"), (
        "a shared fragment must not carry YAML frontmatter"
    )


def test_the_fragment_states_the_multi_decision_shape():
    """The contradiction that shipped: items 4 and 5 read "One sentence" while the ceiling sanctioned
    three-question turns, and nothing reconciled them. It cost fixture 05 a correct tagging — one pair
    for three decisions, so its `consequence` region held an unrelated third decision — and the
    diagnosis was filed against the fixture format instead of against this file.
    """
    body = _prose()
    assert "Items 4 and 5 repeat, as a pair, once per question" in body
    assert "Item 3 is not repeated" in body
    assert "nothing after it" in body, (
        "the emission order must forbid emitting framing past the call, not only before it"
    )


def test_the_fragment_states_two_ceilings_and_what_enters_each():
    """[D4] as amended 2026-08-26. One combined 200 was unsatisfiable: the three real asks it was
    written from measured 564, 324 and 441 against it, and its own remedy deleted the option cost
    statements the same file mandates. Two limits, each countable, each with a stated scope."""
    body = _prose()
    assert "Two limits, both 200 words, both hard" in body, (
        "the ceiling must be stated as two hard limits, not one and not a target"
    )
    assert "The framing — 200 words" in body
    assert "Each question — 200 words" in body
    assert "counted per question and never summed across them" in body, (
        "the per-question scope is the whole repair; summing them restores the unsatisfiable limit"
    )
    assert "wc -w" in body, "a countable ceiling must name its counting method"
    assert "Outside both counts:" in body, "the exclusions must be stated, not implied"


def test_the_fragment_records_that_the_combined_limit_was_refuted():
    """The refutation is measured, so it must not be re-derivable as an opinion. A later author who
    reads only 'two limits' will tidy them back into one."""
    body = _prose()
    assert "refuted by measurement" in body
    assert "564" in body and "324" in body and "441" in body, (
        "the three measurements that killed the combined limit must be in the file"
    )
    assert "leaves six words per option" in body, (
        "the arithmetic must state the framing subtraction: 200/9 is 22, not 6. The first version "
        "omitted it and was wrong by a factor of three, in the paragraph carrying the refutation — "
        "and this assertion pinned the wrong sentence in place, so correcting it turned the suite red"
    )


def test_the_fragment_rules_on_preview_panes():
    """The count named labels and descriptions and was silent on `preview`, which the reader also
    sees. Silence is how the first ceiling acquired three readings."""
    body = _prose()
    assert "preview or mock-up pane" in body
    assert "never be the only place a consequence is stated" in body
    assert "Outside the count is not a licence to be long" in body, (
        "a region outside both counts and governed by no bound is the unbounded detail the "
        "context-above amendment struck, re-entering through the preview pane"
    )


def test_the_remedy_never_sacrifices_the_framing():
    """The ordering that keeps the ceiling from being applied backwards.

    Its first move used to be "cut option descriptions" — the identical move the file uses two
    paragraphs earlier to refute the combined limit, because it deletes the cost statements § Options
    mandates. Only the magnitude differed, and nothing said so. It now trims with a floor.
    """
    body = _prose()
    assert "Never cut items 3–5 to fit" in body
    assert "never below the sentence naming that option's cost" in body, (
        "the remedy must not prescribe deleting the thing the refutation defends"
    )


def test_context_goes_above_and_the_reason_is_stated():
    """[D5] as amended 2026-08-21. "Sits below" was unimplementable: the tool call blocks, so anything
    after it arrives once the answer is already given. Detail goes ABOVE, and the fragment must say why
    — otherwise the next author 'tidies' it back below."""
    body = _prose()
    assert "Context goes **above**, not below" in body
    assert "blocks" in body, "the reason the ordering is forced must be stated"
    assert "bounded in practice, not unbounded" in body, (
        "the accepted cost of context-above must be stated: length above the ask buries it too"
    )


def test_placement_has_an_observable():
    """[D9]. Placement was declared failable and given no observable — two instances would emit
    different separators and both believe they conformed. The marker line is that observable, and
    fixture 04 is the instance that fails on it alone."""
    body = _prose()
    assert "A marker line" in body
    assert "Nothing between the framing and the call" in body


def test_the_two_ask_cap_is_stated():
    """Without it the fragment licensed an unbounded re-ask loop that `groom-issues` calls "the nagging
    that teaches people to stop running the tool" — duplication with drift, on day one."""
    body = _prose()
    assert "After a second unanswered ask" in body
    assert "Two asks is the limit" in body


def test_no_command_name_exception():
    """The prose once permitted "naming a command the reader is about to run" while FORBIDDEN matches
    command names on sight. Prose and oracle must not disagree: one reader follows each."""
    body = _prose()
    assert "no command names" in body
    # The first version also asserted the string "not a violation" was ABSENT. A negative substring
    # test over free prose is satisfied by any rewording — "does not violate", "permitted here" — so
    # it could not detect the class of defect it existed for. Dropped rather than kept as decoration.
    assert FORBIDDEN["skill or command name"].search("run /phil:groom-set next")


def test_the_fragment_does_not_overclaim_its_reach():
    """[D11], and the sentence that should not have shipped: "in force deterministically" claimed
    compliance where only DELIVERY is guaranteed. Slice 02 widens what is checked from two clauses to
    four, which makes the reach claim MORE tempting to overstate, not less."""
    body = _prose()
    assert "Delivery is deterministic" in body and "compliance is not" in body
    assert "must not be described as covered" in body
    # Slice 03 closed the propagation gap, so Reach must not still claim it is open — an understated
    # reach is as wrong as an overstated one, and this section has now been corrected in both
    # directions. What must NOT disappear is the shallowness of the check that closed it.
    assert "Propagation is complete, and enforced" in body
    assert "shallowness is the point" in body, (
        "an enforced reference check reads as enforced conformance unless the file says otherwise"
    )
    assert "can still emit a bare option list" in body
    # Slice 04 closed delivery outside a command too, so the remaining gap had to be restated rather
    # than deleted. Two clauses are structurally unreachable — option costs are semantic, and the
    # framing never enters the payload — and an enforcer that stops naming what it misses reads as a
    # complete one. That is the failure this whole section exists to prevent, twice over now.
    assert "The gap that remains is compliance, not delivery" in body
    assert "stay unreachable and always will be" in body, (
        "the two clauses no mechanism can reach must be named where the reach is claimed"
    )
    assert "One of the six skills" not in body and "Propagation is incomplete" not in body, (
        "a hardcoded consumer count, and a stale claim that propagation is unfinished"
    )
    assert "The fixtures read recordings, not live asks" in body, (
        "the fixture suite must not read as a check over live asks"
    )
    # The sentence this replaces said no check reads a live ask AND NONE CAN. Slice 04 refuted it the
    # same day: a tool call is structured data, and a PreToolUse hook reads it. The impossibility claim
    # must stay gone, and the correction must stay visible — a decision reversed silently is one the
    # next reader re-derives from the same wrong premise.
    assert "and none can" not in body, (
        "the impossibility claim must stay gone. It is quoted nowhere in this file either — a naked "
        "absent-string assertion cannot tell a claim from a quotation of it, so the correction is "
        "worded to keep this guard meaningful"
    )
    assert "written before anyone looked" in body, (
        "the reversal must be recorded as a reversal, not tidied away"
    )
    assert "Two clauses ARE read live" in body
    assert "self-test/decision-request" in body, "the reach claim must name what it was checked against"
    assert "wider than any check of it" in body


# --------------------------------------------------------------------------- the fixtures


def test_fixtures_exist():
    assert len(FIXTURES) >= 6, "slice 02 ships five fixtures beside slice 01's baseline"


@pytest.mark.parametrize("manifest", FIXTURES, ids=lambda p: p.parent.name)
def test_manifest_parses_and_has_its_companions(manifest):
    d = json.loads(manifest.read_text())
    assert d.get("fixture_id"), "every fixture names itself"
    assert (manifest.parent / "expected.md").exists()
    assert (manifest.parent / d["ask_file"]).exists()
    assert (manifest.parent / d["options_file"]).exists()
    if d.get("emission_file"):
        assert (manifest.parent / d["emission_file"]).exists()
    else:
        assert d.get("placement_not_asserted"), (
            f"{d['fixture_id']}: no emission means BARE-LIST and BURIED-ASK are skipped — "
            "the manifest must say so rather than skipping them silently"
        )


@pytest.mark.parametrize("manifest", FIXTURES, ids=lambda p: p.parent.name)
def test_every_fixture_names_its_real_source(manifest):
    """These are recordings, not inventions. The slice that wrote them could reach a real corpus, so
    a synthetic fixture here would be a choice — and the provenance is what lets anyone re-extract."""
    src = json.loads(manifest.read_text())["source"]
    assert src["log"].endswith(".jsonl") and src["timestamp"].endswith("Z")


@pytest.mark.parametrize("manifest", FIXTURES, ids=lambda p: p.parent.name)
def test_expected_decision_is_exactly_one_live_outcome(manifest):
    d = json.loads(manifest.read_text())
    dec = d["expected_decision"]
    assert len(dec) == 1, f"{d['fixture_id']} expects {dec} — exactly one primary outcome"
    assert dec[0] in LIVE_OUTCOMES, f"{dec[0]} is not a live outcome"


@pytest.mark.parametrize("manifest", FIXTURES, ids=lambda p: p.parent.name)
def test_the_findings_are_exactly_what_the_manifest_declares(manifest):
    """The whole suite in one assertion: the exact SET, not "at least one failure".

    A real ask is rarely single-mode — 02, 03 and 06 each fail three or four ways — so a test that
    accepted "some finding fired" would pass with three checks broken.
    """
    d = json.loads(manifest.read_text())
    found = evaluate(manifest.parent)
    assert set(found) == set(d["expected_findings"]), (
        f"{d['fixture_id']}: expected {sorted(d['expected_findings'])}, "
        f"got {sorted(found)} — {found}"
    )
    primary = d["expected_decision"][0]
    if primary == "CONFORMS":
        assert not found, f"{d['fixture_id']} claims CONFORMS but {sorted(found)} fired"
    else:
        assert primary in found, f"{d['fixture_id']}'s primary mode {primary} did not fire"


@pytest.mark.parametrize("manifest", FIXTURES, ids=lambda p: p.parent.name)
def test_the_manifest_still_describes_the_files(manifest):
    """Catches manifest drift. Recording a number and never re-deriving it is how a fixture starts
    certifying a file it no longer describes."""
    d = json.loads(manifest.read_text())
    a = d["mechanical_assertions"]
    ask = (manifest.parent / d["ask_file"]).read_text()
    options = json.loads((manifest.parent / d["options_file"]).read_text())
    assert a["measured_framing_words"] == _words(ask), (
        f"{d['fixture_id']}: manifest records {a['measured_framing_words']} framing words, "
        f"{d['ask_file']} has {_words(ask)}"
    )
    assert a["measured_question_words"] == _question_groups(options), (
        f"{d['fixture_id']}: manifest records {a['measured_question_words']}, "
        f"derived {_question_groups(options)}"
    )
    assert a["framing_ceiling"] == FRAMING_CEILING and a["question_ceiling"] == QUESTION_CEILING

    # The three fields the first version recorded and never recomputed. Setting `forbidden_token_count`
    # to 99 and `context_words` to 9999 both left the suite green — in a file whose own header claims
    # every number is re-derived, and whose fixture 01 lists "recording a count and never recomputing
    # it" as a gate failure. The count was also misnamed: it held a count of CATEGORIES.
    kinds = sorted(k for k, pat in FORBIDDEN.items() if pat.search(_counted_text(ask, options)))
    assert a["forbidden_token_kinds"] == kinds, (
        f"{d['fixture_id']}: manifest records {a['forbidden_token_kinds']}, derived {kinds}"
    )
    assert "forbidden_token_count" not in a, (
        "renamed to forbidden_token_kinds — the values were category counts under a token name"
    )
    previews = sum(_words(o.get("preview", ""))
                   for q in options["questions"] for o in q["options"])
    assert a.get("preview_words", 0) == previews, (
        f"{d['fixture_id']}: manifest records {a.get('preview_words', 0)} preview words, "
        f"derived {previews}"
    )
    if d.get("emission_file"):
        before, _, _ = _parse_emission((manifest.parent / d["emission_file"]).read_text())
        context = "\n".join(_bodies(before, "context"))
        assert a["context_words"] == _words(context), (
            f"{d['fixture_id']}: manifest records {a['context_words']} context words, "
            f"derived {_words(context)}"
        )
        assert a["framing_pairs"] == len(_bodies(before, "decision"))


@pytest.mark.parametrize("manifest", FIXTURES, ids=lambda p: p.parent.name)
def test_the_tagged_regions_reproduce_the_counted_framing(manifest):
    """The invariant that stops the two halves of a fixture drifting apart.

    Placement is read from `emission.md`; wording and the count are read from `ask.md`. If those can
    disagree, a fixture can claim conforming wording while its emission holds something else — and
    fixture 04's whole value is the claim that its wording passes and only its placement fails.
    """
    d = json.loads(manifest.read_text())
    if not d.get("emission_file"):
        pytest.skip("no emission recorded; the manifest declares placement not asserted")
    assert framing_matches_ask(manifest.parent), (
        f"{d['fixture_id']}: ask.md is not the concatenation of its tagged framing regions"
    )


def test_the_context_block_is_exempt_from_the_vocabulary_rule():
    """C4/S2-AC3, and the clause the whole two-limit design rests on: if the context block were
    checked too, there would be nowhere for a path or a card number to go, and the ask would have to
    carry them. Fixture 05's context carries an artifact path and the fixture still CONFORMS."""
    d = SELFTEST / "05-the-context-block"
    manifest = json.loads((d / "manifest.json").read_text())
    assert manifest["mechanical_assertions"]["context_carries_forbidden_tokens"] is True
    assert manifest["mechanical_assertions"]["framing_pairs"] == 3, (
        "fixture 05 asks three questions, so it must carry three decision/consequence pairs — "
        "one pair for three decisions was the mis-tagging the singular first version could not see"
    )
    before, _, _ = _parse_emission((d / "emission.md").read_text())
    context = "\n".join(_bodies(before, "context"))
    hits = {k for k, p in FORBIDDEN.items() if p.search(context)}
    assert hits, "fixture 05 is supposed to prove the exemption is used, and its context is clean"
    assert not evaluate(d), "a forbidden token in the CONTEXT must never be a finding"


@pytest.mark.parametrize("mode", sorted(FAILURE_MODES))
def test_every_mode_has_a_failing_and_a_passing_fixture(mode):
    """A check with no red instance is `check-readonly-commands.py`'s first version: written, never
    called, silently green. A check with no green instance is a check that always fires."""
    results = {m.parent.name: evaluate(m.parent) for m in FIXTURES}
    fails = [n for n, f in results.items() if mode in f]
    # A fixture that records an emission is one the placement/framing checks actually ran against.
    evaluated = [n for n, _ in results.items()
                 if json.loads((SELFTEST / n / "manifest.json").read_text()).get("emission_file")
                 or mode in {"OVER-CEILING", "JARGON-WALL"}]
    passes = [n for n in evaluated if mode not in results[n]]
    assert fails, f"{mode} never fires on any fixture — nothing proves the check works"
    assert passes, f"{mode} fires on every fixture it is evaluated against — the check is stuck on"


def test_placement_is_isolated_by_exactly_one_fixture():
    """[D9]'s decisive evidence, asserted rather than described.

    Slice 02's brief allowed for the possibility that "correct wording, wrong placement" could not be
    expressed at all, in which case [D9] was a sentence rather than a clause. Fixture 04 is a real ask
    that fails on placement and nothing else, so the clause stands — and this test is what keeps it
    standing, because a later widening of any other check would quietly take the isolation away.
    """
    isolated = [m.parent.name for m in FIXTURES if set(evaluate(m.parent)) == {"BURIED-ASK"}]
    assert isolated == ["04-the-buried-ask"], (
        f"expected exactly 04 to fail on placement alone, got {isolated}"
    )


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


# --------------------------------------------------------------------------- the oracle itself
#
# The fixtures above are RECORDINGS of real asks, and they leave three parts of the oracle
# unexercised: no real ask in the corpus interposes text between its framing and the call, none emits
# its regions out of order, and none is pushed over a ceiling by a preview pane alone. Disabling any
# of those three left the suite green — proven by mutation, 2026-08-26 — which is
# `check-readonly-commands.py`'s first version exactly: written, never called, silently passing.
#
# So these three are UNIT tests of the checking mechanism, with hand-built inputs. They are labelled
# synthetic on purpose: a constructed emission is the right input for testing a parser, and the wrong
# input for measuring a standard.


def _emission(*, context=None, marker=True, order=FRAMING_REGIONS, trailing="", after=()):
    """Build a minimal tagged emission. Synthetic — for testing the oracle, never for measurement."""
    body = {"interrupted": "It stopped here.", "decision": "Whether to do the thing.",
            "consequence": "Doing it cannot be undone."}
    out = [BANNER]
    if context:
        out += ["<!-- context -->", context, "<!-- /context -->"]
    if marker:
        out += ["<!-- marker -->", "---", "<!-- /marker -->"]
    for r in order:
        out += [f"<!-- {r} -->", body[r], f"<!-- /{r} -->"]
    if trailing:
        out.append(trailing)
    out.append(CALL)
    for r in after:
        out += [f"<!-- {r} -->", body[r], f"<!-- /{r} -->"]
    return "\n\n".join(out) + "\n", "\n\n".join(body[r] for r in FRAMING_REGIONS)


def _write_fixture(tmp_path, emission, ask, options):
    (tmp_path / "emission.md").write_text(emission)
    (tmp_path / "ask.md").write_text(ask)
    (tmp_path / "options.json").write_text(json.dumps(options))
    (tmp_path / "manifest.json").write_text(json.dumps(
        {"fixture_id": "SYNTHETIC", "ask_file": "ask.md", "options_file": "options.json",
         "emission_file": "emission.md"}))
    return tmp_path


ONE_CLEAN_QUESTION = {"questions": [{"header": "H", "question": "Which way?", "options": [
    {"label": "This way", "description": "Cheap, and it loses the audit trail."},
    {"label": "That way", "description": "Slower, and nothing is lost."}]}]}


def test_a_synthetic_clean_emission_fires_nothing(tmp_path):
    """The control. Without it, the three tests below could pass because the builder is broken."""
    em, ask = _emission()
    assert not evaluate(_write_fixture(tmp_path, em, ask, ONE_CLEAN_QUESTION))


def test_text_between_the_framing_and_the_call_is_a_placement_defect(tmp_path):
    """The second half of the fragment's placement rule — *"Nothing between the framing and the call"*.

    This is the buried-ask failure rebuilt out of sanctioned parts: correct framing, correct marker, and
    then one more remark that pushes the options away from the question. No real ask in the corpus does
    it, so only this test holds the clause up.
    """
    em, ask = _emission(trailing="Oh, and one more thing about the thing.")
    found = evaluate(_write_fixture(tmp_path, em, ask, ONE_CLEAN_QUESTION))
    assert set(found) == {"BURIED-ASK"}
    assert "between the framing and the call" in found["BURIED-ASK"]


def test_regions_out_of_order_are_a_placement_defect(tmp_path):
    """*"Emit in this order"* — an emission that states the consequence before naming the decision has
    the right elements in the wrong sequence, and reads as commentary rather than as a question."""
    em, ask = _emission(order=("consequence", "interrupted", "decision"))
    found = evaluate(_write_fixture(tmp_path, em, ask, ONE_CLEAN_QUESTION))
    assert "BURIED-ASK" in found
    assert "out of order" in found["BURIED-ASK"]


def test_a_preview_pane_never_enters_the_count(tmp_path):
    """The fragment rules a preview to be context. The rule is only real if the count honours it, and
    no recorded fixture is pushed over a limit by its preview alone."""
    huge = json.loads(json.dumps(ONE_CLEAN_QUESTION))
    huge["questions"][0]["options"][0]["preview"] = "word " * 500
    em, ask = _emission()
    assert not evaluate(_write_fixture(tmp_path, em, ask, huge)), (
        "500 words of preview must not breach a 200-word question limit"
    )


def test_the_preview_exclusion_is_load_bearing_on_a_real_fixture():
    """And the same ruling against a real ask rather than a constructed one: fixture 06 carries three
    preview panes, and counting them would change the number this repo published as its worst case."""
    d = SELFTEST / "06-over-the-ceiling"
    options = json.loads((d / "options.json").read_text())
    previews = sum(_words(o.get("preview", ""))
                   for q in options["questions"] for o in q["options"])
    assert previews > 0, "fixture 06 is the preview instance; if it has none, pick another"
    counted = _question_groups(options)[0]
    manifest = json.loads((d / "manifest.json").read_text())
    assert manifest["mechanical_assertions"]["measured_question_words"] == [counted]
    assert previews > counted * 0.4, (
        f"the exclusion is only worth a rule if it changes the number materially: "
        f"{counted} counted, {previews} in previews"
    )


def test_an_over_long_framing_breaches_the_framing_limit(tmp_path):
    """The framing half of the ceiling. Every recorded framing is 148 words or fewer, so disabling this
    half left the suite green — proven by mutation. The corpus cannot supply a red here: an ask whose
    framing runs past 200 words is the failure the standard was written to prevent, and nobody in this
    repo's history has emitted one.
    """
    em, ask = _emission()
    long_ask = ask + " " + "and another consideration entirely " * 60
    (tmp_path / "x").mkdir()
    em = em.replace("Doing it cannot be undone.", "Doing it cannot be undone. " + "and another consideration entirely " * 60)
    d = _write_fixture(tmp_path / "x", em, long_ask.strip(), ONE_CLEAN_QUESTION)
    found = evaluate(d)
    assert "OVER-CEILING" in found
    assert "framing is" in found["OVER-CEILING"] and str(FRAMING_CEILING) in found["OVER-CEILING"]


def test_a_forbidden_token_in_a_preview_is_not_a_jargon_wall(tmp_path):
    """The other half of the preview ruling: a preview is context, so it may carry what the ask may not.

    Real previews in this repo hold command names, card numbers and file paths — fixture 06's do — but
    that fixture already fails the vocabulary rule for its own ask, so it cannot show the exemption
    working. This can.
    """
    with_preview = json.loads(json.dumps(ONE_CLEAN_QUESTION))
    with_preview["questions"][0]["options"][0]["preview"] = (
        "allowed-tools: Bash(gh api graphql:*)\nsee CLAUDE.md and #24 for why"
    )
    em, ask = _emission()
    assert not evaluate(_write_fixture(tmp_path, em, ask, with_preview)), (
        "a path, a card number and a tool grant inside a preview pane must not fire the ask's rule"
    )


def test_the_coherence_rule_fires_on_an_inconsistent_fixture(tmp_path):
    """Proof that `framing_matches_ask` is a rule and not a decoration.

    It guards fixture 04's central claim — conforming wording, failing placement — by making the
    wording that is counted and the emission that is read the same bytes. Asserted only over compliant
    fixtures, it was unfalsifiable.
    """
    em, ask = _emission()
    assert framing_matches_ask(_write_fixture(tmp_path, em, ask, ONE_CLEAN_QUESTION))
    (tmp_path / "ask.md").write_text("Something else entirely.")
    assert not framing_matches_ask(tmp_path)


def test_framing_emitted_after_the_call_is_unreachable(tmp_path):
    """The worst bug the first version shipped: it parsed regions from the WHOLE file and only then
    split on the call, so a consequence emitted after the blocking call counted as present. Measured
    before the fix — an emission with `consequence` past the call returned NO findings at all, and the
    coherence invariant passed too.

    This is exactly the failure the context-goes-above amendment exists to prevent: anything after the
    call arrives once the answer is already given. The suite asserted that the fragment SAYS so and
    never that the oracle honoured it.
    """
    em, ask = _emission(order=("interrupted", "decision"), after=("consequence",))
    found = evaluate(_write_fixture(tmp_path, em, ask, ONE_CLEAN_QUESTION))
    assert "BURIED-ASK" in found and "AFTER the call" in found["BURIED-ASK"]
    assert "BARE-LIST" in found, "a consequence past the call is an absent consequence"


def test_a_three_question_turn_needs_three_pairs(tmp_path):
    """The per-question shape. One tagged pair used to satisfy a three-decision ask — which is how
    fixture 05 shipped with a `consequence` region holding an unrelated third decision.

    The root cause was in the standard, not the fixture format: items 4 and 5 read "One sentence"
    while the ceiling sanctioned three-question turns, and nothing reconciled them.
    """
    three = {"questions": [dict(ONE_CLEAN_QUESTION["questions"][0], header=h) for h in "ABC"]}
    em, ask = _emission()
    found = evaluate(_write_fixture(tmp_path, em, ask, three))
    assert "BARE-LIST" in found
    assert "2 of 3" in found["BARE-LIST"], found["BARE-LIST"]


def test_the_registers_documented_format_actually_parses():
    """The register documents the emission format with region content on the tag's own line. The first
    parser required a newline after the tag, so the register's own worked example parsed to ONE region
    of five — and an ask written exactly as documented would score BARE-LIST and BURIED-ASK while
    conforming. Prose-and-oracle disagreement, inside the section that defines the interface.
    """
    register = (SELFTEST / "README.md").read_text()
    block = [b for b in register.split("```") if BANNER in b]
    assert block, "the register must carry a worked example of the format it documents"
    documented = block[0].replace("markdown\n", "", 1)
    before, after, trailing = _parse_emission(documented)
    assert [n for n, _ in before] == ["context", "marker", "interrupted", "decision", "consequence"], (
        f"the register's own example parses to {[n for n, _ in before]}"
    )
    assert not after and not trailing.strip()


@pytest.mark.parametrize("kind,positive,negative", [
    ("wave label", "the wave: discuss label is set", "a wave of complaints"),
    ("issue number", "see #33 for context", "issue thirty-three"),
    ("slice id", "slice 02 ships this", "a slice of the problem"),
    ("decision number", "recorded as [D4]", "decision four"),
    ("skill or command name", "run groom-issues first", "run it first"),
    ("artifact path", "written in CLAUDE.md", "written down"),
])
def test_every_forbidden_pattern_is_independently_failable(kind, positive, negative):
    """Deleting the `wave label` and `slice id` patterns outright left the suite green.

    The mode-set assertion checks WHICH MODE fired, never which pattern produced it, so a redundant
    pattern — `slice id` on a fixture that already trips `issue number` — was unfalsifiable, and
    `wave label` matched nothing in the whole fixture set. Twelve checks were mutation-proven; the six
    patterns inside one of them were not.
    """
    pat = FORBIDDEN[kind]
    assert pat.search(positive), f"{kind} must match {positive!r}"
    assert not pat.search(negative), f"{kind} must not match {negative!r}"


@pytest.mark.parametrize("manifest", FIXTURES, ids=lambda p: p.parent.name)
def test_the_prose_finding_set_matches_the_manifest(manifest):
    """`expected.md` restates each fixture's finding set in prose, and nothing read it. Proven: a set
    rewritten to `CONFORMS, OVER-CEILING, NONSENSE` left the suite green.

    That is the shape this repo's own registry test condemns — "three hand-maintained registries,
    three answers" — shipped again in the slice that cites it.
    """
    d = json.loads(manifest.read_text())
    prose = (manifest.parent / "expected.md").read_text()
    m = re.search(r"finding set:\*\*(.*?)\n\s*\n", prose, re.S | re.I)
    assert m, f"{d['fixture_id']}: expected.md must state its finding set"
    claimed = set() if "empty" in m.group(1).lower() else set(re.findall(r"`([A-Z-]+)`", m.group(1)))
    assert claimed == set(d["expected_findings"]), (
        f"{d['fixture_id']}: expected.md claims {sorted(claimed)}, "
        f"manifest declares {sorted(d['expected_findings'])}"
    )
    assert claimed <= LIVE_OUTCOMES


def test_the_register_table_matches_the_manifests():
    """The register's fixture table restates every expected outcome. Nothing parsed it either, and
    `test_fixtures_exist` only asserts a count, so a seventh fixture would need no row."""
    rows = {}
    for line in (SELFTEST / "README.md").read_text().splitlines():
        m = re.match(r"\|\s*`(\d\d-[\w-]+)/`\s*\|.*\|\s*(.+?)\s*\|$", line)
        if m:
            rows[m.group(1)] = set(re.findall(r"`([A-Z-]+)`", m.group(2)))
    assert set(rows) == {m.parent.name for m in FIXTURES}, (
        f"the register table lists {sorted(rows)}; the directory holds "
        f"{sorted(m.parent.name for m in FIXTURES)}"
    )
    for name, claimed in rows.items():
        d = json.loads((SELFTEST / name / "manifest.json").read_text())
        expected = set(d["expected_findings"]) or {"CONFORMS"}
        assert claimed == expected, f"{name}: register says {sorted(claimed)}, manifest {sorted(expected)}"


def test_a_partial_conformance_is_not_reported_as_full(tmp_path):
    """`CONFORMS` meant two things: fixture 01 passes two of four checks (no emission recorded), and
    fixture 05 passes four of four. Both returned an empty finding set, so both read as full
    conformance. The distinction is now a manifest field the register annotates."""
    partial = [json.loads(m.read_text()) for m in FIXTURES
               if not json.loads(m.read_text()).get("emission_file")]
    assert partial, "fixture 01 is the partial case; if it gains an emission, drop this test"
    for d in partial:
        assert d["expected_decision"] == ["CONFORMS"] and d.get("placement_not_asserted")
    register = (SELFTEST / "README.md").read_text()
    assert "CONFORMS (partial)" in register, (
        "the register's outcome list must distinguish two-of-four from four-of-four"
    )


def test_the_banner_and_a_single_call_are_required(tmp_path):
    """Both are part of the documented format and neither was validated, so a `v2` emission or one
    with two calls parsed silently as a conforming v1."""
    em, _ = _emission()
    with pytest.raises(AssertionError, match="must open with"):
        _parse_emission(em.replace(BANNER, "<!-- decision-request-emission:v2 -->"))
    with pytest.raises(AssertionError, match="exactly one"):
        _parse_emission(em + "\n" + CALL + "\n")


def test_a_duplicate_empty_region_cannot_hide_a_missing_one(tmp_path):
    """The parser kept the LAST match per region name, so an empty region followed by a filled one
    vanished and the reverse fired spuriously. Bodies are now collected in order and empties dropped."""
    em, ask = _emission()
    em = em.replace("<!-- decision -->", "<!-- decision -->\n\n\n\n<!-- /decision -->\n\n<!-- decision -->", 1)
    before, _, _ = _parse_emission(em)
    assert len(_bodies(before, "decision")) == 1, "an empty region is an absent one"


def test_a_missing_interruption_line_is_named(tmp_path):
    """Item 3's own red. Every recording that omits it also omits its pairs, so the mode fired either
    way and disabling this sub-check alone left the suite green — an isolating instance was missing.

    Item 3 is the line that makes the ask resumable: it names what the reader was pulled out of.
    """
    em, ask = _emission(order=("decision", "consequence"))
    found = evaluate(_write_fixture(tmp_path, em, ask, ONE_CLEAN_QUESTION))
    assert set(found) == {"BARE-LIST"}
    assert "naming what this interrupted" in found["BARE-LIST"], found["BARE-LIST"]
