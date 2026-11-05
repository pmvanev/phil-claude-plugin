"""`skills/humanize-technical-prose/scripts/measure_voice.py`: the counts a voice profile stores.

The script counts; the skill judges. What counts as a slip, and its mechanism or cause, is read by the
skill and handed over as a tally. The script's part is to measure only the author's own prose, to keep a
phrase only when it recurs (D3), to store no sentence and no slipped word, and to refuse a transcript (D2).
"""
import collections
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "skills" / "humanize-technical-prose" / "scripts" / "measure_voice.py"

_spec = importlib.util.spec_from_file_location("measure_voice", SCRIPT)
mv = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(mv)

FILLER = ("The scheduler assigns each job to the least loaded worker. It checks the queue every second. "
          "A worker that misses three checks is marked idle and loses its jobs to the others. ")


def _write(tmp_path, name, text):
    p = tmp_path / name
    p.write_text(text)
    return p


def _run(*args, stdin=None, env=None):
    r = subprocess.run([sys.executable, str(SCRIPT), *map(str, args)], input=stdin,
                       capture_output=True, text=True, env=env)
    return r.returncode, r.stdout, r.stderr


# --- what counts as the author's own prose ---

def test_markdown_code_quotations_headings_tables_and_lists_are_not_measured():
    text = ("---\ntitle: x\n---\n# A heading of several words here\n\n"
            "The parser reads the file.\n\n"
            "```\nthis code block holds many many words that must not count\n```\n\n"
            "> a blockquote of borrowed words that must not count\n\n"
            "| a | table | row |\n|---|---|---|\n\n"
            "- a list item fragment\n\n"
            "She said \"these quoted words are not the author's own\" and left.\n")
    prose = mv.own_prose(text, "md")
    assert "code block" not in prose and "blockquote" not in prose and "table" not in prose
    assert "heading" not in prose and "list item" not in prose and "title" not in prose
    assert "quoted words" not in prose
    assert "The parser reads the file." in prose


def test_latex_environments_math_citations_and_comments_are_not_measured():
    text = (r"\section{Introduction}" "\n"
            r"We measure $x^2 + y$ here \cite{knuth}. % a comment of many words" "\n"
            r"\begin{figure}caption words that must not count\end{figure}" "\n"
            r"\begin{quote}borrowed words\end{quote}" "\n"
            r"The \textit{kernel} boots first." "\n")
    prose = mv.own_prose(text, "tex")
    assert "comment" not in prose and "caption" not in prose and "borrowed" not in prose
    assert "knuth" not in prose and "Introduction" not in prose and "x^2" not in prose
    assert "The kernel boots first." in prose


def test_latex_bookkeeping_commands_leave_no_arguments_behind():
    """Found on the developer's own essay, 2026-11-05: `toc subsection` came back as a favoured phrase."""
    text = (r"\addcontentsline{toc}{subsection}{The Outbreak}\setcounter{page}{3}"
            r"\vspace{2em}\input{chapter}The worm spread overnight." "\n")
    prose = mv.own_prose(text, "tex")
    assert "toc" not in prose and "subsection" not in prose and "chapter" not in prose
    assert "The worm spread overnight." in prose


def test_a_name_is_never_stored_as_an_opener():
    """Found on the developer's own essay, 2026-11-05: `spafford` was stored as a sentence opener."""
    text = ("Spafford wrote the first analysis. The worm spread fast. Later, Spafford revised it. "
            "Spafford also named the bug. ") * 5
    assert "spafford" not in mv.measure_text(text)["openers"]


def test_a_named_directory_is_one_sample(tmp_path):
    """Found on the developer's own essay, 2026-11-05: its abstract, one file of seven, was dropped as thin."""
    essay = tmp_path / "essay"
    essay.mkdir()
    _write(essay, "abstract.tex", FILLER * 2)
    _write(essay, "body.tex", FILLER * 30)
    m = mv.build_measures([essay])
    assert [s["path"] for s in m["samples"]] == [str(essay)] and m["thin"] == []


def test_decimals_and_abbreviations_do_not_split_a_sentence():
    sents = mv.sentences("The value rose to 3.5 percent, e.g. in May. Then it fell.")
    assert len(sents) == 2


def test_possessives_are_not_contractions():
    m = mv.measure_text("The kernel's scheduler isn't fair. It's slow. Linux's queue can't wait. " * 5)
    # isn't, It's and can't: 3 contractions in every 11 words; kernel's and Linux's are possessives
    assert m["contractions_per_1000"] == pytest.approx(3 / 11 * 1000, rel=0.01)


# --- favoured phrases: kept only when they recur, never a sentence, never a name ---

def test_a_phrase_that_occurs_once_in_one_sample_is_not_stored(tmp_path):
    a = _write(tmp_path, "a.md", FILLER * 30 + "Our quarterly retainer covers this.\n")
    b = _write(tmp_path, "b.md", FILLER * 30)
    phrases = {p["phrase"] for p in mv.build_measures([a, b])["phrases"]}
    assert not any("quarterly retainer" in p for p in phrases)


def test_a_phrase_in_two_samples_is_stored(tmp_path):
    a = _write(tmp_path, "a.md", FILLER * 30)
    b = _write(tmp_path, "b.md", FILLER * 30)
    phrases = {p["phrase"] for p in mv.build_measures([a, b])["phrases"]}
    assert any("least loaded worker" in p for p in phrases)


def test_a_phrase_holding_a_name_is_not_stored_however_often_it_recurs(tmp_path):
    text = FILLER * 30 + "We shipped it to Acme Logistics on time. " * 5
    a = _write(tmp_path, "a.md", text)
    b = _write(tmp_path, "b.md", text)
    phrases = {p["phrase"] for p in mv.build_measures([a, b])["phrases"]}
    assert not any("acme" in p for p in phrases)


def test_no_stored_string_is_longer_than_four_words(tmp_path):
    a = _write(tmp_path, "a.md", FILLER * 30)
    b = _write(tmp_path, "b.md", FILLER * 30)
    m = mv.build_measures([a, b])
    assert all(len(p["phrase"].split()) <= 4 for p in m["phrases"])
    assert all(len(k.split()) <= 4 for k in m["openers"]) and all(len(k.split()) <= 4 for k in m["connectives"])


# --- samples: thin ones are named and left out; transcripts are refused ---

def test_a_thin_sample_is_named_and_left_out(tmp_path):
    a = _write(tmp_path, "a.md", FILLER * 30)
    thin = _write(tmp_path, "thin.md", FILLER)
    m = mv.build_measures([a, thin])
    assert [s["path"] for s in m["thin"]] == [str(thin)]
    assert m["words"] == next(s["words"] for s in m["samples"] if s["path"] == str(a))


def test_a_transcript_is_refused(tmp_path):
    t = _write(tmp_path, "session.jsonl", '{"type": "user"}\n')
    code, out, _ = _run("--measure", t)
    assert code == 2 and "transcript" in json.loads(out)["refused"][0]["why"]


def test_a_path_under_claude_projects_is_refused(tmp_path):
    d = tmp_path / ".claude" / "projects" / "x"
    d.mkdir(parents=True)
    t = _write(d, "notes.md", FILLER * 30)
    code, out, _ = _run("--measure", t)
    assert code == 2


# --- the profile file: counts only ---

TALLY = {
    "misspelling": {"dropped letter": 6, "added letter": 4, "swapped letters": 2, "wrong vowel": 1,
                    "wrong doubling": 1, "other": 0},
    "grammar": {"revision residue": {"doubled word": 1, "words out of order": 1, "stray word": 1},
                "omission": {"dropped word": 1, "dropped article": 1},
                "substitution": {"wrong word": 1, "wrong article": 1}},
    "on_name_or_term": 6,
}


def test_build_writes_the_profile_where_the_environment_says(tmp_path):
    a = _write(tmp_path, "a.md", FILLER * 30)
    b = _write(tmp_path, "b.md", FILLER * 30)
    env = {"HTP_PROFILE_DIR": str(tmp_path / "profiles"), "PATH": "/usr/bin:/bin"}
    code, out, err = _run("--build", "formal", "--slips", "-", a, b, stdin=json.dumps(TALLY), env=env)
    assert code == 0, err
    profile = json.loads((tmp_path / "profiles" / "formal.json").read_text())
    assert profile["name"] == "formal" and profile["slips"] == TALLY
    assert json.loads(out)["path"] == str(tmp_path / "profiles" / "formal.json")


def test_the_default_profile_directory_is_outside_every_repo():
    assert mv.profile_dir({}) == Path.home() / ".claude" / "humanize-technical-prose" / "profiles"


def test_a_tally_carrying_a_word_is_refused():
    bad = json.loads(json.dumps(TALLY))
    bad["misspelling"]["dropped letter"] = "occuring"
    with pytest.raises(ValueError):
        mv.check_tally(bad)


def test_a_tally_with_an_unknown_kind_is_refused():
    bad = json.loads(json.dumps(TALLY))
    bad["grammar"]["omission"]["occuring"] = 1
    with pytest.raises(ValueError):
        mv.check_tally(bad)


def test_a_profile_name_outside_the_pattern_is_refused(tmp_path):
    a = _write(tmp_path, "a.md", FILLER * 30)
    code, _, _ = _run("--build", "../escape", "--slips", "-", a, stdin=json.dumps(TALLY),
                      env={"HTP_PROFILE_DIR": str(tmp_path), "PATH": "/usr/bin:/bin"})
    assert code == 2


def test_a_draft_is_measured_without_the_thin_floor_or_phrases(tmp_path):
    d = _write(tmp_path, "draft.md", FILLER)
    code, out, _ = _run("--draft", d)
    m = json.loads(out)
    assert code == 0 and m["words"] > 0 and "phrases" not in m


def test_additionally_counts_as_a_connective():
    """Found measuring fixture 11, 2026-11-05: the commonest connective in Claude's drafts went uncounted."""
    m = mv.measure_text("Additionally, the close path releases the lock. The open path takes it first. " * 3)
    assert "additionally" in m["connectives"]


# --- slice 04: dividing N slips among the profile's kinds ---

def _profile(tmp_path, name, slips):
    d = tmp_path / "profiles"
    d.mkdir(exist_ok=True)
    (d / f"{name}.json").write_text(json.dumps({"name": name, "slips": slips}))
    return {"HTP_PROFILE_DIR": str(d), "PATH": "/usr/bin:/bin"}


def test_n_slips_are_exactly_n():
    for n in (1, 2, 5, 9):
        assert len(mv.allocate(TALLY, n, False)["slips"]) == n


def test_zero_slips_are_none():
    assert mv.allocate(TALLY, 0, False)["slips"] == []


def test_without_misspellings_every_slip_is_a_grammar_kind():
    assert all(s["class"] != "misspelling" for s in mv.allocate(TALLY, 5, False)["slips"])


def test_with_misspellings_the_draw_follows_the_proportions():
    """The paper's tally: 14 misspellings against 7 grammar slips, so three slips are two and one."""
    out = mv.allocate(TALLY, 3, True)
    classes = collections.Counter(s["class"] == "misspelling" for s in out["slips"])
    assert classes[True] == 2 and classes[False] == 1
    assert out["slips"][0]["kind"] == "dropped letter", "the largest share comes first"


def test_an_unrecorded_mechanism_is_never_drawn():
    slips = {"misspelling": {"other": 9}, "grammar": {}, "on_name_or_term": 0}
    out = mv.allocate(slips, 2, True)
    assert out["slips"] == [] and out["none_of_kind"] is True


def test_a_profile_with_none_of_the_asked_for_kinds_draws_none_and_names_what_it_holds():
    slips = {"misspelling": {"wrong vowel": 9}, "grammar": {}, "on_name_or_term": 0}
    out = mv.allocate(slips, 2, False)
    assert out["slips"] == [] and out["none_of_kind"] is True
    assert out["held"] == ["misspelling: wrong vowel"]


def test_slips_on_names_or_terms_are_reported_as_unmirrored():
    out = mv.allocate(TALLY, 2, False)
    assert out["unmirrored"] == 6 and out["profile_total"] == 21


def test_allocate_reads_the_named_profile(tmp_path):
    env = _profile(tmp_path, "paper", TALLY)
    code, out, _ = _run("--allocate", "paper", "2", env=env)
    assert code == 0 and len(json.loads(out)["slips"]) == 2


def test_allocate_refuses_a_missing_profile_and_lists_the_ones_that_exist(tmp_path):
    env = _profile(tmp_path, "paper", TALLY)
    code, out, _ = _run("--allocate", "memo", "2", env=env)
    assert code == 2 and json.loads(out)["profiles"] == ["paper"]
