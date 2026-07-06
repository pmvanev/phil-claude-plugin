"""Tiny SUT for the redesign-tests self-test fixtures (fixture 06 variant).

Here OrderService depends on TWO collaborators: a repository AND a payment gateway. The repo has a
real in-memory implementation, but the gateway does NOT — there is no FakePaymentGateway and no
gateway safe to call for real. This is on purpose: a behavioural rewrite of an over-mocked test
would need a fake that does not exist, so the loop must SKIP rather than invent one.
"""


class InMemoryOrderRepo:
    def __init__(self):
        self._orders = {}

    def save(self, order):
        self._orders[order["id"]] = dict(order)

    def get(self, order_id):
        return self._orders.get(order_id)


# NOTE: no in-memory / fake PaymentGateway ships. The only real gateway would hit an external
# payment provider, which is not safe to call in a test. A behavioural rewrite has nothing to
# assert charges against.


class OrderService:
    def __init__(self, repo, gateway):
        self._repo = repo
        self._gateway = gateway

    def place(self, order_id, amount):
        self._gateway.charge(amount)
        order = {"id": order_id, "amount": amount, "status": "placed"}
        self._repo.save(order)
        return order_id
