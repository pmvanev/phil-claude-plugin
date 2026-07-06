"""Tiny SUT for the redesign-tests self-test fixtures.

The SUT is NOT the thing being reviewed for rewrites -- the *test file* is. It exists so pytest has
something green to run AND exposes a real in-memory repository so behavioural rewrites can assert on
observable persisted state. Dependency-free on purpose. `_orders` is intentionally private so a
smell test can be shown reaching into it.
"""


class InMemoryOrderRepo:
    def __init__(self):
        self._orders = {}

    def save(self, order):
        self._orders[order["id"]] = dict(order)

    def get(self, order_id):
        return self._orders.get(order_id)


class OrderService:
    def __init__(self, repo):
        self._repo = repo

    def place(self, order_id, amount):
        order = {"id": order_id, "amount": amount, "status": "placed"}
        self._repo.save(order)
        return order_id
