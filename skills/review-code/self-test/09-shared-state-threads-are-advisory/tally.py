"""Order-event tallies for the fulfilment dashboard."""

import threading
from collections import Counter
from concurrent.futures import ThreadPoolExecutor

MAX_CARRIER_CALLS = 8


def count_by_status(events, workers=4):
    """Count events by status, spreading the work over several threads."""
    counts = {}
    lock = threading.Lock()

    def tally(chunk):
        for event in chunk:
            with lock:
                counts[event["status"]] = counts.get(event["status"], 0) + 1

    chunks = [events[i::workers] for i in range(workers)]
    threads = [threading.Thread(target=tally, args=(chunk,)) for chunk in chunks]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    return counts


def count_by_carrier(events, workers=4):
    """Count events by carrier, spreading the work over several threads."""
    counts = {}

    def tally(chunk):
        for event in chunk:
            counts[event["carrier"]] = counts.get(event["carrier"], 0) + 1

    chunks = [events[i::workers] for i in range(workers)]
    with ThreadPoolExecutor(max_workers=workers) as pool:
        list(pool.map(tally, chunks))
    return counts


def fetch_carrier_statuses(carrier_ids, fetch):
    """Ask each carrier's API for its status; the calls are independent network waits."""
    with ThreadPoolExecutor(max_workers=MAX_CARRIER_CALLS) as pool:
        return dict(zip(carrier_ids, pool.map(fetch, carrier_ids)))


def count_by_region(events, workers=4):
    """Count events by region: each worker counts its own chunk, and the counts merge once at the end."""
    chunks = [events[i::workers] for i in range(workers)]
    with ThreadPoolExecutor(max_workers=workers) as pool:
        partials = pool.map(lambda chunk: Counter(e["region"] for e in chunk), chunks)
    return dict(sum(partials, Counter()))
