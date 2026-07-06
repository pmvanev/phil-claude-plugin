import datetime
from unittest.mock import Mock

from orders import InMemoryOrderRepo, OrderService


# --- SMELL A: implementation-coupling (asserts save() was CALLED, not the observable result) ---
# Smell family: implementation-coupling. Rewrite intent: assert on the retrieved order instead.
def test_place_saves_order():
    repo = Mock()
    OrderService(repo).place("A1", 100)
    repo.save.assert_called_once()


# --- SMELL B: testing private state (reaches into repo._orders instead of the public get()) ---
# Smell family: implementation-coupling. Rewrite intent: assert via repo.get(order_id).
def test_repo_internal_dict_has_order():
    repo = InMemoryOrderRepo()
    OrderService(repo).place("A1", 100)
    assert "A1" in repo._orders


# --- SMELL C: flakiness (assertion depends on the wall clock / current time) ---
# Smell family: flakiness/determinism. Rewrite intent: inject a fixed clock or drop the time coupling.
def test_order_year_is_current():
    repo = InMemoryOrderRepo()
    OrderService(repo).place("A1", 100)
    assert datetime.date.today().year == datetime.datetime.now().year


# --- SMELL D: excessive mocking (mocks the only collaborator, asserts solely on the mock) ---
# Smell family: excessive-mocking. Rewrite intent: use the real InMemoryOrderRepo and assert state.
def test_place_everything_mocked():
    repo = Mock()
    OrderService(repo).place("A1", 100)
    repo.save.assert_called_once()
    assert repo.save.call_args[0][0]["id"] == "A1"
