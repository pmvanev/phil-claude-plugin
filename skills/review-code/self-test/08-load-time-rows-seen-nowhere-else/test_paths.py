import pytest

from paths import resolve


def test_the_root_is_the_shell():
    assert resolve("/").name == "index.html"


def test_a_path_outside_dist_is_refused():
    with pytest.raises(FileNotFoundError):
        resolve("/../app.py")
