from unittest.mock import Mock

from orders import OrderService


# SMELL: excessive-mocking — both collaborators are mocked and the test asserts solely on the mock
# interactions. The repo half could be rewritten against the real InMemoryOrderRepo, but the
# gateway.charge assertion has no real/fake gateway to observe — so the rewrite is blocked.
def test_place_charges_and_saves():
    repo = Mock()
    gateway = Mock()
    OrderService(repo, gateway).place("A1", 100)
    gateway.charge.assert_called_once_with(100)
    repo.save.assert_called_once()
