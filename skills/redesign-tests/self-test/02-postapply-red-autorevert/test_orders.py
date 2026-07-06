from unittest.mock import Mock

from orders import OrderService


# SMELL: implementation-coupling — asserts that save() was CALLED (a mock interaction),
# not that the order is actually persisted with the right fields. Green, but couples to HOW.
def test_place_saves_order():
    repo = Mock()
    svc = OrderService(repo)
    svc.place("A1", 100)
    repo.save.assert_called_once()
