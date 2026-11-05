# Retry budget for the ingest worker

The ingest worker plays a crucial role in keeping the warehouse current. When an upstream call fails,
the worker retries it up to `MAX_RETRIES` times with exponential backoff, ensuring a seamless
experience for downstream consumers.

The retry budget serves as a guard against retry storms. It is not just a limit, but a contract with
the upstream team: once a minute's budget of 120 retries is spent, the worker stops retrying and parks
the batch in `ingest.deadletter`.

To change the budget, set `INGEST_RETRY_BUDGET` and restart the worker:

```sh
INGEST_RETRY_BUDGET=200 systemctl restart ingest-worker
```

Despite these challenges, the retry budget remains well positioned to support the platform's growth.
