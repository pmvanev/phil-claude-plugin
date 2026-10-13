# Widget Service

## Gotchas

- Set `TZ=UTC` before running the integration tests. On 2026-03-02 the nightly run failed for six
  hours because the runner moved to a host in `America/Denver`, the fixture timestamps shifted by
  seven hours, and every date-boundary assertion broke. We spent a morning suspecting the ORM before
  anyone checked the host clock, and the same thing happened again in May when a contractor ran the
  suite from a laptop.
