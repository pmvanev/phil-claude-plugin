"""Tests for `scripts/region-place.py` — slice 02's reader, placer and drift report.

These are written BEFORE the script, deliberately. Slice 01 recorded a deviation from
`CLAUDE.md`'s "test first" rule, and its stated reason was that the probe's shape could not be
known until the live forge had answered. Nothing here touches a forge: classification, placement
and line arithmetic are local text operations whose shape is knowable in advance, so the exemption
does not carry over.

What these pin is the slice's whole safety property. S2's AC1 — content outside the markers is
byte-identical on **every** path, including the failure and refusal paths — is the one guarantee
that lets a generated region live inside a file full of prose no probe can reproduce. Every
failure mode is silent: a region placed one line off still looks placed, and a reflowed bullet
still reads as English.
"""

import hashlib
import importlib.util
import json
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "region-place.py"


def load():
    """Import a module whose filename contains a hyphen."""
    spec = importlib.util.spec_from_file_location("region_place", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


rp = load()


BEGIN = "<!-- phil:board-setup:v1:begin -->"
END = "<!-- phil:board-setup:v1:end -->"

REGION = f"{BEGIN}\ngenerated 2026-08-17T20:00Z · do not edit inside these markers\n\n- Forge: GitHub *(probed · Q1)*\n\n{END}"

# The hard case, in miniature: a section that is mostly hazards recorded after contact, none of it
# reproducible by any probe, with several lines stating facts the region will now own.
PROSE_SECTION = """# Project

Some preamble a human wrote.

## Issue board

- Forge: GitHub — pass `-R pmvanev/phil-claude-plugin` on every `gh` call.
- IDs: project `PVT_kwHOANPp-M4Bf-px` · Status field `PVTSSF_lAHOANPp-M4Bf-pxzhaNnGs`
- **Auto-close on Done is ENABLED.** Post the closing comment first, then set Status.

## Something else

Trailing content.
"""

NO_SECTION = """# Project

Just prose. No board section at all.
"""

PROBE = {
    "status": "ok",
    "facts": [
        {"field": "project-and-board-ids",
         "value": {"id": "PVT_kwHOANPp-M4Bf-px", "number": 3, "title": "phil plugin",
                   "url": "https://github.com/users/pmvanev/projects/3"},
         "query": "Q2", "provenance": "probed"},
        {"field": "status-mechanism",
         "value": "a project single-select FIELD named `Status` (id PVTSSF_lAHOANPp-M4Bf-pxzhaNnGs)",
         "query": "Q3", "provenance": "probed"},
    ],
}


def outside(text):
    """Everything not between the markers, as bytes. The thing AC1 is about."""
    if BEGIN not in text:
        return text.encode()
    b = text.index(BEGIN)
    e = text.index(END) + len(END) if END in text else len(text)
    return (text[:b] + text[e:]).encode()


# --- classification (the reader) ---------------------------------------------------------

def test_no_section_is_classified_as_such():
    assert rp.classify(NO_SECTION)["state"] == "no-section"


def test_section_without_markers_is_classified_as_such():
    c = rp.classify(PROSE_SECTION)
    assert c["state"] == "section-no-markers"
    assert c["heading_line"] == 5


def test_existing_region_is_classified_present_with_its_extent():
    text = PROSE_SECTION.replace("## Issue board\n", f"## Issue board\n\n{REGION}\n")
    c = rp.classify(text)
    assert c["state"] == "region-present"
    assert c["region_begin"] < c["region_end"]


def test_begin_without_end_is_malformed_not_guessed():
    """AC4. The region's extent is never guessed — a missing `end` is a refusal, not a scan
    to the next heading."""
    text = PROSE_SECTION.replace("## Issue board\n", f"## Issue board\n\n{BEGIN}\nstuff\n")
    c = rp.classify(text)
    assert c["state"] == "markers-malformed"
    assert "end" in c["malformed_reason"].lower()


def test_nested_begin_markers_are_malformed():
    text = PROSE_SECTION.replace(
        "## Issue board\n", f"## Issue board\n\n{BEGIN}\n{BEGIN}\nx\n{END}\n")
    c = rp.classify(text)
    assert c["state"] == "markers-malformed"


def test_end_before_begin_is_malformed():
    text = PROSE_SECTION.replace("## Issue board\n", f"## Issue board\n\n{END}\nx\n{BEGIN}\n")
    assert rp.classify(text)["state"] == "markers-malformed"


def test_a_heading_deeper_than_h2_is_not_the_section():
    """`### Issue board` is a subsection of something else, not the board section."""
    text = NO_SECTION + "\n### Issue board\n\n- not the section\n"
    assert rp.classify(text)["state"] == "no-section"


# --- placement (the placer) --------------------------------------------------------------

def test_placing_into_a_prose_section_leaves_every_other_byte_identical():
    """AC1, the whole point of the slice."""
    out = rp.place(PROSE_SECTION, REGION)
    assert outside(out) == outside(PROSE_SECTION)


def test_placing_preserves_every_hand_written_line_verbatim():
    out = rp.place(PROSE_SECTION, REGION)
    for line in PROSE_SECTION.splitlines():
        assert line in out.splitlines(), f"lost or reflowed: {line!r}"


def test_placement_is_deterministic():
    """AC5 — two runs against the same file put the region in the same place."""
    assert rp.place(PROSE_SECTION, REGION) == rp.place(PROSE_SECTION, REGION)


def test_region_lands_immediately_after_the_heading():
    lines = rp.place(PROSE_SECTION, REGION).splitlines()
    h = lines.index("## Issue board")
    assert BEGIN in lines[h + 1:h + 3], "region must follow the heading, not the prose"


def test_placing_into_a_file_with_no_section_appends_the_section():
    out = rp.place(NO_SECTION, REGION)
    assert "## Issue board" in out
    assert NO_SECTION.rstrip() in out, "prior content must survive byte-intact"


def test_placing_refuses_when_a_region_is_already_present():
    """Slice 05 owns re-run. Slice 02 must not rewrite one."""
    text = rp.place(PROSE_SECTION, REGION)
    with pytest.raises(rp.Refusal):
        rp.place(text, REGION)


def test_placing_refuses_on_malformed_markers_and_changes_nothing():
    """AC4."""
    text = PROSE_SECTION.replace("## Issue board\n", f"## Issue board\n\n{BEGIN}\nstuff\n")
    with pytest.raises(rp.Refusal):
        rp.place(text, REGION)


def test_placing_refuses_a_region_whose_own_markers_are_wrong():
    with pytest.raises(rp.Refusal):
        rp.place(PROSE_SECTION, "no markers here at all")


# --- the concurrency guard ---------------------------------------------------------------

def test_write_refuses_when_the_file_changed_since_it_was_read(tmp_path):
    f = tmp_path / "CLAUDE.md"
    f.write_text(PROSE_SECTION)
    stale = hashlib.sha256(b"something else entirely").hexdigest()
    with pytest.raises(rp.Refusal):
        rp.write_region(f, REGION, expect_sha=stale)
    assert f.read_text() == PROSE_SECTION, "a refused write must not touch the file"


def test_write_succeeds_on_a_matching_sha_and_preserves_outside_bytes(tmp_path):
    f = tmp_path / "CLAUDE.md"
    f.write_text(PROSE_SECTION)
    sha = hashlib.sha256(PROSE_SECTION.encode()).hexdigest()
    rp.write_region(f, REGION, expect_sha=sha)
    assert outside(f.read_text()) == outside(PROSE_SECTION)


# --- the drift report --------------------------------------------------------------------

def test_a_probed_value_present_verbatim_in_the_prose_confirms():
    d = rp.drift(PROSE_SECTION, PROBE)
    hits = [c for c in d["confirms"] if "PVT_kwHOANPp-M4Bf-px" in c["value"]]
    assert hits, "the project id is stated in the prose and probed identically"
    assert hits[0]["line"] == 8


def test_a_differing_id_of_a_known_shape_contradicts():
    text = PROSE_SECTION.replace("PVTSSF_lAHOANPp-M4Bf-pxzhaNnGs", "PVTSSF_lAHOANPp-M4Bf-pxWRONG1")
    d = rp.drift(text, PROBE)
    assert any("PVTSSF_" in c["found"] for c in d["contradicts"])


def test_prose_bearing_no_probed_value_cannot_be_evaluated():
    """The `Auto-close on Done` line is the case that matters: the workflow is probed, but which
    Status fires it is not, so nothing here may call the line wrong."""
    d = rp.drift(PROSE_SECTION, PROBE)
    lines = [c["line"] for c in d["cannot_evaluate"]]
    assert 9 in lines


def test_a_short_scalar_is_not_evidence_of_anything():
    """Found by the first real dogfood run, 2026-08-17.

    The probe returns `number: 3` and `option_count: 4`. Substring-matching those against prose
    made nineteen lines "confirm" the board — including a line whose only claim to agreement was
    containing the digit 2. A false confirm is worse than no report: it says the prose was checked
    and found sound, which is the one thing the drift report exists to establish honestly.
    """
    probe = {"status": "ok", "facts": [
        {"field": "project-and-board-ids", "value": {"number": 3, "count": 4},
         "provenance": "probed", "query": "Q2"}]}
    text = "# T\n\n## Issue board\n\n- Seven wave columns are noise to 2 or 3 readers.\n"
    d = rp.drift(text, probe)
    assert d["confirms"] == [], f"a bare digit is not evidence: {d['confirms']}"
    assert len(d["cannot_evaluate"]) == 1


def test_a_long_numeric_id_is_still_evidence():
    """The fix must not throw out option ids, which are numeric and discriminating."""
    probe = {"status": "ok", "facts": [
        {"field": "column-families", "value": {"id": "39094273"},
         "provenance": "probed", "query": "Q3"}]}
    text = "# T\n\n## Issue board\n\n- Blocked `39094273`.\n"
    assert len(rp.drift(text, probe)["confirms"]) == 1


def test_option_ids_nested_inside_a_fact_are_evidence():
    """Also found by the first dogfood run.

    `column-families` nests its option ids one level down, as a list of dicts inside the fact's
    value. A flattener that only walks the top level stringifies that list and matches nothing —
    so the line stating all four option ids, the single most dangerous constant on the board,
    reported as `cannot evaluate` while looking like a clean result.
    """
    probe = {"status": "ok", "facts": [
        {"field": "column-families", "provenance": "probed", "query": "Q3",
         "value": {"field_id": "PVTSSF_lAHOANPp", "option_count": 4,
                   "options": [{"name": "Todo", "id": "f75ad846"},
                               {"name": "Blocked", "id": "39094273"}]}}]}
    text = "# T\n\n## Issue board\n\n- Todo `f75ad846`, Blocked `39094273`.\n"
    d = rp.drift(text, probe)
    assert len(d["confirms"]) == 1, d
    assert d["cannot_evaluate"] == []


def test_drift_never_reports_a_line_in_two_buckets():
    d = rp.drift(PROSE_SECTION, PROBE)
    seen = [c["line"] for bucket in ("confirms", "contradicts", "cannot_evaluate")
            for c in d[bucket]]
    assert len(seen) == len(set(seen))


def test_drift_reads_only_outside_the_markers():
    """The generated region agreeing with the probe is not a `confirms` — it is a tautology."""
    text = rp.place(PROSE_SECTION, REGION)
    assert rp.drift(text, PROBE) == rp.drift(PROSE_SECTION, PROBE)


def test_drift_edits_nothing():
    """AC2 — a contradicting hand-written line is reported and not edited."""
    text = PROSE_SECTION.replace("PVTSSF_lAHOANPp-M4Bf-pxzhaNnGs", "PVTSSF_WRONG")
    before = text
    rp.drift(text, PROBE)
    assert text == before


# --- the retire offer ---------------------------------------------------------------------

def test_retire_removes_exactly_one_whole_line():
    """AC3 — the only permitted change outside the markers, and only on an explicit call."""
    out = rp.retire_line(PROSE_SECTION, 8)
    assert len(out.splitlines()) == len(PROSE_SECTION.splitlines()) - 1
    assert "PVT_kwHOANPp-M4Bf-px" not in out


def test_retire_leaves_every_other_line_untouched():
    out = rp.retire_line(PROSE_SECTION, 8).splitlines()
    kept = [l for i, l in enumerate(PROSE_SECTION.splitlines(), 1) if i != 8]
    assert out == kept


def test_retire_refuses_a_line_inside_the_markers():
    text = rp.place(PROSE_SECTION, REGION)
    begin_line = text.splitlines().index(BEGIN) + 1
    with pytest.raises(rp.Refusal):
        rp.retire_line(text, begin_line + 1)


def test_retire_refuses_an_out_of_range_line():
    with pytest.raises(rp.Refusal):
        rp.retire_line(PROSE_SECTION, 9999)


def test_retire_refuses_line_zero_rather_than_falling_through():
    """`if args.retire:` is falsy for 0, which would report the wrong refusal. Line numbers are
    1-based, so 0 must be refused as out of range, not as a missing argument."""
    with pytest.raises(rp.Refusal):
        rp.retire_line(PROSE_SECTION, 0)


# --- slice 03: the declared region --------------------------------------------------------
#
# Slice 03 must write a human's declaration OUTSIDE the probed markers, which collides head-on with
# slice 02's AC1. Resolved with a second delimited region rather than loose prose: bytes outside
# *both* regions stay byte-identical, the probed region is regenerated freely (slice 05), and the
# declared region is written only on an answer and never regenerated.

DECL = (f"{rp.DECL_BEGIN}\ngenerated 2026-08-17T21:00Z · declarations, not probed facts\n\n"
        f"- Label family `wave`: single-valued *(you declared · 2026-08-17)*\n\n{rp.DECL_END}")


def outside_both(text):
    for b, e in ((BEGIN, END), (rp.DECL_BEGIN, rp.DECL_END)):
        if b in text and e in text:
            text = text[:text.index(b)] + text[text.index(e) + len(e):]
    return text.encode()


def surviving_lines(before, after):
    """Every pre-existing line still present, verbatim.

    This — not byte-identity of the concatenation — is the right invariant for the declared region,
    and the distinction was bought by a real defect. Inserting a region between two non-blank lines
    cannot both preserve byte-identity *and* leave the markers on their own lines: the probed region
    gets away with it only because a blank line follows the heading and donates its newline.

    The declared region is a **one-time insertion the human sanctioned**, not a block regenerated on
    every run, so contributing its own newline is legitimate. What must never happen is an existing
    line being altered, reflowed or dropped.
    """
    return all(l in after.splitlines() for l in before.splitlines())


def test_a_declaration_goes_in_its_own_region():
    out = rp.place_declaration(PROSE_SECTION, DECL)
    assert rp.DECL_BEGIN in out
    assert surviving_lines(PROSE_SECTION, out)


def test_both_declared_markers_sit_alone_on_their_lines():
    """The defect the first real run produced: `declared:v1:end` merged onto the following bullet,
    leaving the region unterminated and invisible to the classifier — a dangling `begin` written by
    the very command whose rule is that an extent is never guessed."""
    for host in (PROSE_SECTION, rp.place(PROSE_SECTION, REGION)):
        out = rp.place_declaration(host, DECL)
        lines = out.splitlines()
        assert rp.DECL_BEGIN in lines, "begin marker is not alone on its line"
        assert rp.DECL_END in lines, "end marker is not alone on its line"
        c = rp.classify(out)
        assert c["declared_begin"] and c["declared_end"], c


def test_a_dangling_declared_marker_is_malformed():
    """`classify` checked only the probed markers, so a broken declared region passed as healthy."""
    broken = PROSE_SECTION.replace("## Issue board\n",
                                   f"## Issue board\n{rp.DECL_BEGIN}\nstuff\n")
    assert rp.classify(broken)["state"] == "markers-malformed"


def test_placing_into_a_file_with_a_dangling_declared_marker_refuses():
    broken = PROSE_SECTION.replace("## Issue board\n",
                                   f"## Issue board\n{rp.DECL_BEGIN}\nstuff\n")
    with pytest.raises(rp.Refusal):
        rp.place(broken, REGION)


def test_a_declaration_lands_after_the_probed_region_not_inside_it():
    placed = rp.place(PROSE_SECTION, REGION)
    out = rp.place_declaration(placed, DECL)
    assert out.index(END) < out.index(rp.DECL_BEGIN), "declared region follows the probed one"
    assert surviving_lines(placed, out)


def test_placing_a_declaration_twice_refuses():
    """Re-declaring is not this slice's; a human's answer is not regenerated."""
    out = rp.place_declaration(PROSE_SECTION, DECL)
    with pytest.raises(rp.Refusal):
        rp.place_declaration(out, DECL)


def test_a_declaration_must_carry_its_own_markers():
    with pytest.raises(rp.Refusal):
        rp.place_declaration(PROSE_SECTION, "- family wave: single-valued")


def test_regenerating_the_probed_region_never_touches_the_declared_one():
    """The property slice 05 depends on. A declaration is a human's, and whole-region regeneration
    of the probed block must not be able to reach it."""
    text = rp.place_declaration(rp.place(PROSE_SECTION, REGION), DECL)
    declared = text[text.index(rp.DECL_BEGIN):text.index(rp.DECL_END) + len(rp.DECL_END)]
    refreshed = rp.replace_region(text, REGION.replace("20:00Z", "23:59Z"))
    assert declared in refreshed, "the declared region survived verbatim"


def test_classify_reports_the_declared_region_separately():
    text = rp.place_declaration(rp.place(PROSE_SECTION, REGION), DECL)
    c = rp.classify(text)
    assert c["state"] == "region-present"
    assert c["declared_begin"] is not None


def test_a_file_with_only_a_declaration_is_not_region_present():
    """A declared region is not a probed region. Confusing the two would make slice 05 refuse to
    write a block that was never written."""
    c = rp.classify(rp.place_declaration(PROSE_SECTION, DECL))
    assert c["state"] == "section-no-markers"
    assert c["declared_begin"] is not None


# --- slice 05: safe re-run ----------------------------------------------------------------
#
# The brief requires the timestamp question be DECIDED, not left open. Decision: **the stamp is not
# refreshed on a no-change run.** KPI-3 demands a second run write zero bytes, and refreshing a stamp
# writes bytes — so the two are the same requirement, and excluding the stamp from the comparison
# while still writing it would fail KPI-3 while looking correct.

STAMPED = (f"{BEGIN}\ngenerated 2026-08-17T20:00Z · do not edit inside these markers\n\n"
           f"- Forge: GitHub *(probed · Q1)*\n\n{END}")
RESTAMPED = STAMPED.replace("20:00Z", "23:59Z")
CHANGED = STAMPED.replace("GitHub", "GitLab").replace("20:00Z", "23:59Z")


def test_a_restamp_alone_writes_zero_bytes(tmp_path):
    """KPI-3. A run that rewrites the file just to move a clock produces a diff every time, the
    diffs stop being read, and the block decays into issue #31's unnoticed-stale state while looking
    maintained."""
    f = tmp_path / "CLAUDE.md"
    f.write_text(rp.place(PROSE_SECTION, STAMPED))
    before = f.read_text()
    result = rp.refresh_region(f, RESTAMPED, expect_sha=rp.sha256_of(before))
    assert result["status"] == "unchanged"
    assert result["bytes_written"] == 0
    assert f.read_text() == before, "not one byte, including the stamp"


def test_a_real_change_is_written_and_the_new_stamp_comes_with_it(tmp_path):
    f = tmp_path / "CLAUDE.md"
    f.write_text(rp.place(PROSE_SECTION, STAMPED))
    result = rp.refresh_region(f, CHANGED, expect_sha=rp.sha256_of(f.read_text()))
    assert result["status"] == "ok"
    assert result["bytes_written"] > 0
    assert "GitLab" in f.read_text()
    assert "23:59Z" in f.read_text(), "a real change carries the fresh stamp"


def test_refresh_never_touches_prose_or_the_declared_region(tmp_path):
    f = tmp_path / "CLAUDE.md"
    f.write_text(rp.place_declaration(rp.place(PROSE_SECTION, STAMPED), DECL))
    before = f.read_text()
    rp.refresh_region(f, CHANGED, expect_sha=rp.sha256_of(before))
    after = f.read_text()
    assert outside_both(after) == outside_both(before)
    declared = before[before.index(rp.DECL_BEGIN):before.index(rp.DECL_END) + len(rp.DECL_END)]
    assert declared in after


def test_refresh_refuses_when_the_file_moved(tmp_path):
    f = tmp_path / "CLAUDE.md"
    f.write_text(rp.place(PROSE_SECTION, STAMPED))
    before = f.read_text()
    with pytest.raises(rp.Refusal):
        rp.refresh_region(f, CHANGED, expect_sha="deadbeef")
    assert f.read_text() == before


def test_refresh_refuses_when_there_is_no_region_to_refresh(tmp_path):
    f = tmp_path / "CLAUDE.md"
    f.write_text(PROSE_SECTION)
    with pytest.raises(rp.Refusal):
        rp.refresh_region(f, STAMPED, expect_sha=rp.sha256_of(PROSE_SECTION))


def test_unchanged_is_distinguishable_from_unread(tmp_path):
    """Slice 05 AC5 — a probe failure must never render as `unchanged`. `refresh_region` is only
    reachable with a rendered region in hand, so the guard is that a caller cannot ask for a refresh
    without one: an empty or markerless region is refused, not treated as "nothing changed"."""
    f = tmp_path / "CLAUDE.md"
    f.write_text(rp.place(PROSE_SECTION, STAMPED))
    with pytest.raises(rp.Refusal):
        rp.refresh_region(f, "", expect_sha=rp.sha256_of(f.read_text()))


def test_the_change_report_names_what_moved(tmp_path):
    """Slice 05's change report: a line-by-line account of what the forge now says that the file did
    not. A count alone hides which constant changed, and an option id is not interchangeable."""
    report = rp.region_changes(STAMPED, CHANGED)
    assert report["changed"] is True
    assert any("GitHub" in line for line in report["removed"])
    assert any("GitLab" in line for line in report["added"])
    assert report["stamp_only"] is False


def test_the_change_report_calls_a_restamp_stamp_only():
    report = rp.region_changes(STAMPED, RESTAMPED)
    assert report["changed"] is False
    assert report["stamp_only"] is True


# --- the absent file ----------------------------------------------------------------------

def test_an_absent_file_is_a_state_not_a_traceback(tmp_path):
    """The skill says "Create the file if absent, and say which happened", and forbids placing by
    hand. A raw FileNotFoundError leaves the model with no route but the `Write` grant — hand
    placement, which the skill it is following prohibits."""
    missing = tmp_path / "nosuch.md"
    c = rp.classify_file(missing)
    assert c["state"] == "file-absent"
    assert c["sha256"] is None


def test_placing_into_an_absent_file_creates_it_and_says_so(tmp_path):
    missing = tmp_path / "nosuch.md"
    result = rp.write_region(missing, REGION, expect_sha=None)
    assert result["created"] is True
    assert missing.read_text().startswith(f"# ")or "## Issue board" in missing.read_text()
    assert BEGIN in missing.read_text()


def test_creating_still_refuses_a_region_without_markers(tmp_path):
    missing = tmp_path / "nosuch.md"
    with pytest.raises(rp.Refusal):
        rp.write_region(missing, "no markers", expect_sha=None)
    assert not missing.exists(), "a refused create must not leave a partial file"


def test_an_existing_file_still_requires_its_sha(tmp_path):
    """The create path takes `expect_sha=None`; that must not become a way to skip the guard on a
    file that does exist."""
    f = tmp_path / "CLAUDE.md"
    f.write_text(PROSE_SECTION)
    with pytest.raises(rp.Refusal):
        rp.write_region(f, REGION, expect_sha=None)
    assert f.read_text() == PROSE_SECTION


# --- C5: the declared region must be invisible to drift and untouchable by retire ---------

def test_drift_does_not_walk_the_declared_region():
    """A human's declaration is not hand-written prose to be audited against the probe. Feeding it
    to `drift()` also breaks the tautology rule the skill states: placing a declared region would
    shift line numbers and add lines to `cannot_evaluate`."""
    plain = rp.place(PROSE_SECTION, REGION)
    withdecl = rp.place_declaration(plain, DECL)
    assert rp.drift(withdecl, PROBE) == rp.drift(plain, PROBE)


def test_a_declared_line_is_never_offered_for_retirement():
    """The data-loss case. A declared line carrying an id- or URL-shaped token that does not match
    the probe files as `contradicts`, becomes retire-eligible, and gets deleted — destroying a
    never-regenerated human answer through the one sanctioned mutation."""
    decl = (f"{rp.DECL_BEGIN}\ngenerated 2026-08-17T21:00Z · declarations\n\n"
            f"- Docs root override: https://github.com/other/repo/blob/main/ "
            f"*(you declared · 2026-08-17)*\n\n{rp.DECL_END}")
    text = rp.place_declaration(rp.place(PROSE_SECTION, REGION), decl)
    d = rp.drift(text, PROBE)
    offered = [c["line"] for c in d["contradicts"]]
    declared_lines = range(rp.classify(text)["declared_begin"],
                           rp.classify(text)["declared_end"] + 1)
    assert not (set(offered) & set(declared_lines)), \
        "a declared line was offered as a contradiction and is now retire-eligible"


def test_retire_refuses_a_line_inside_the_declared_region():
    text = rp.place_declaration(rp.place(PROSE_SECTION, REGION), DECL)
    c = rp.classify(text)
    for lineno in range(c["declared_begin"], c["declared_end"] + 1):
        with pytest.raises(rp.Refusal):
            rp.retire_line(text, lineno)
