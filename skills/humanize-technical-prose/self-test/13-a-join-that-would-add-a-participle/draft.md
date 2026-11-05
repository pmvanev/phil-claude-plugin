# The retry job

The job reads a failed call from the queue. It waits for the backoff to expire. Then it retries the
call. A success removes the call from the queue. A failure puts it back. The backoff doubles each
time. It stops at ten minutes. After six failures the call moves to the dead-letter table. Someone
reviews that table each morning.
