"""Tiny SUT for the redesign-tests self-test fixtures.

The SUT is NOT the thing being rewritten -- the *test file* is. It exists so pytest has something
to run AND exposes a real in-memory repository so a behavioural rewrite can assert on observable
persisted state instead of on mock interactions. Dependency-free on purpose.

THIS COPY IS DELIBERATELY BUGGY (fixture 01 only): place() persists status="pending" instead of
"placed", so the behavioural test fails at baseline. That red baseline is the precondition.
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
        order = {"id": order_id, "amount": amount, "status": "pending"}  # BUG: should be "placed"
        self._repo.save(order)
        return order_id
