from orders import InMemoryOrderRepo, OrderService


def test_placed_order_is_retrievable_with_its_details():
    repo = InMemoryOrderRepo()
    svc = OrderService(repo)
    order_id = svc.place("A1", 100)
    assert repo.get(order_id) == {"id": "A1", "amount": 100, "status": "placed"}
