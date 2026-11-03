from tally import count_by_carrier, count_by_region, count_by_status, fetch_carrier_statuses

EVENTS = [
    {"status": "shipped", "region": "west", "carrier": "ups"},
    {"status": "shipped", "region": "east", "carrier": "dhl"},
    {"status": "held", "region": "west", "carrier": "ups"},
]


def test_counts_events_by_status():
    assert count_by_status(EVENTS) == {"shipped": 2, "held": 1}


def test_counts_events_by_carrier():
    assert count_by_carrier(EVENTS) == {"ups": 2, "dhl": 1}


def test_counts_events_by_region():
    assert count_by_region(EVENTS) == {"west": 2, "east": 1}


def test_fetches_one_status_per_carrier():
    statuses = {"ups": "up", "dhl": "degraded"}

    assert fetch_carrier_statuses(["ups", "dhl"], statuses.get) == statuses
