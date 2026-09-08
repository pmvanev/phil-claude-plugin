"""The shared plain-language rule, and specifically the half that is new.

`scripts/plain_language.py` was extracted from `hooks/decision-request/check-ask.py` so a second surface
could take the word ceiling without the vocabulary welded to it. The hook's own suite proves the move
changed nothing — it drives the hook as a subprocess and passed identically before and after.

**What that suite cannot prove is the `permit` mechanism**, because the hook permits nothing. It exists
for `phil:board-snapshot`, whose whole job includes printing card numbers that an interrupting question
must never contain. New behaviour with no consumer under test is how an abstraction ships broken, so it
is tested here rather than waited on.
"""

import importlib.util
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "plain_language.py"


@pytest.fixture(scope="module")
def pl():
    spec = importlib.util.spec_from_file_location("plain_language", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# --- the counting half: arithmetic, no vocabulary ---

@pytest.mark.parametrize("text,expected", [("", 0), (None, 0), ("one", 1), ("a b  c\nd", 4)])
def test_words_counts_whitespace_separated_tokens(pl, text, expected):
    assert pl.words(text) == expected


def test_over_ceiling_returns_the_count_not_a_bool(pl):
    """Every caller reporting a breach must say how far over it went; a bool forces a recount."""
    assert pl.over_ceiling("a b c", ceiling=2) == 3
    assert pl.over_ceiling("a b c", ceiling=3) is None, "at the ceiling is not over it"
    assert pl.over_ceiling("a b c", ceiling=5) is None


def test_the_default_ceiling_is_the_one_the_standard_states(pl):
    assert pl.DEFAULT_CEILING == 200


def test_counting_ignores_vocabulary_entirely(pl):
    """The halves are independent. A forbidden identifier changes no count."""
    assert pl.words("see #34 now") == pl.words("see this now")


# --- the vocabulary half ---

def test_the_three_portable_classes_are_detected(pl):
    found = pl.identifiers_in("see #34 in rules/writing.md per [ADR-13]")
    assert found == ["a bracketed identifier", "a file path", "an issue or ticket number"]


def test_a_url_is_a_link_and_never_an_identifier(pl):
    """A reader can open a URL. The rule is about identifiers from a system they may not share."""
    assert pl.identifiers_in("https://github.com/o/r/blob/main/rules/writing.md") == []


def test_clean_text_finds_nothing(pl):
    assert pl.identifiers_in("Say what is being decided and what turns on it.") == []


# --- `permit`: the reason the extraction happened at all ---

def test_permit_removes_a_class_from_the_scan(pl):
    """The board read must print card numbers. Without this the surface could not use the module."""
    text = "see #34 in rules/writing.md"
    assert pl.identifiers_in(text) == ["a file path", "an issue or ticket number"]
    assert pl.identifiers_in(text, permit=["an issue or ticket number"]) == ["a file path"]


def test_permit_does_not_weaken_the_classes_it_does_not_name(pl):
    """Permitting one class must not turn the check off. This is the failure that would make the
    extraction worse than the copy it replaced."""
    found = pl.identifiers_in("see #34 in rules/writing.md per [ADR-13]",
                              permit=["an issue or ticket number"])
    assert found == ["a bracketed identifier", "a file path"]


def test_permitting_everything_finds_nothing(pl):
    names = [name for name, _ in pl.PORTABLE_IDENTIFIERS]
    assert pl.identifiers_in("see #34 in rules/writing.md per [ADR-13]", permit=names) == []


def test_an_unknown_permit_name_is_inert_rather_than_an_error(pl):
    """A typo in a caller's permit list must not silently disable a real class, and must not crash a
    hook mid-question either. It matches nothing, so every class still scans."""
    assert pl.identifiers_in("see #34", permit=["a wave label"]) == ["an issue or ticket number"]


def test_the_hook_permits_nothing(pl):
    """The default must stay the strict one. A surface opts out explicitly or not at all."""
    import inspect
    sig = inspect.signature(pl.identifiers_in)
    assert sig.parameters["permit"].default == ()
    assert sig.parameters["forbid"].default is pl.PORTABLE_IDENTIFIERS
