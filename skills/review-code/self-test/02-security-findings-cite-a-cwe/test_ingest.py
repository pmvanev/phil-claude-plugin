import os
import pickle

import ingest


def _cache():
    db = ingest.open_cache()
    db.executemany(
        "INSERT INTO cards (owner, title, created_at) VALUES (?, ?, ?)",
        [("ada", "Fix login", "2026-01-02"), ("bob", "Add export", "2026-01-01")],
    )
    return db


def test_cards_for_returns_only_the_owner_s_cards():
    assert ingest.cards_for(_cache(), "ada") == [(1, "Fix login")]


def test_cards_sorted_by_title():
    assert ingest.cards_sorted(_cache(), "title") == [(2, "Add export"), (1, "Fix login")]


def test_cache_key_is_stable_for_the_same_body():
    assert ingest.cache_key(b"body") == ingest.cache_key(b"body")


def test_display_order_keeps_every_card():
    assert sorted(ingest.display_order([3, 1, 2])) == [1, 2, 3]


def test_reset_code_is_six_digits():
    code = ingest.reset_code()
    assert len(code) == 6 and code.isdigit()


def test_login_accepts_the_right_password_and_refuses_another():
    salt = os.urandom(16)
    users = {"ada": (salt, ingest.hash_password("password123", salt))}
    assert ingest.login(users, "ada", "password123")
    assert not ingest.login(users, "ada", "password124")


def test_a_snapshot_round_trips():
    assert ingest.load_snapshot(pickle.dumps({"cards": 2})) == {"cards": 2}


def test_triage_returns_the_model_s_reply():
    assert ingest.triage("Crash on save", lambda prompt, tools: "true") == "true"
