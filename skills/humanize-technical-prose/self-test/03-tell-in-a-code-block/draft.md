# Logging the request id

The request id plays a crucial role in tracing a failed call across services. Every handler logs it
before doing anything else:

```python
def handle(request):
    # The request id plays a crucial role in tracing; log it first.
    log.info("start", request_id=request.headers["X-Request-Id"])
    return route(request)
```

Search for the id in the log viewer to see every service the call touched.
