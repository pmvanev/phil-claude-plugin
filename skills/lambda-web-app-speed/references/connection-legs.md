# Timing a Connection's Legs

Where the phase that owns INIT waits on one connection — several checks that touch the same database
waiting alike — time that connection one leg at a time. A first connection is DNS, then TCP, then TLS,
then the sign-in, then the first query; each can own the wait, and each has a different fix.

## Run a probe, not the function

Time the legs from a **separate probe function** in the same subnets and security group as the function
under study, so it crosses the same network and meets the same server. A probe costs the function's
INIT nothing, and it can repeat one connection at chosen idle gaps without waiting for real cold
starts. The person deploys it, invokes it and removes it; the skill only reads its lines.

Take readings **first, then after idle gaps** — at once, after 5, 10 and 40 minutes — since a leg slow
only after idle points at something the server lets go cold. Where the database supports two sign-in
methods, time both in the same reading: a fast password sign-in beside a slow IAM sign-in clears the
network and the server's startup, and leaves the IAM check.

## The legs, as phases

Write one EMF record per sign-in, each leg a phase (no dot), so `phases.py` reads it as it reads the
cold-start line:

| Phase | Starts | Ends |
|---|---|---|
| `ConnectDns` | the lookup | an address |
| `ConnectTcp` | the connect call | the socket open |
| `ConnectTls` | the protocol's TLS request | the handshake done |
| `ConnectToken` | signing an IAM token | the token in hand; omit for a password |
| `ConnectSignIn` | the driver's connect, given the address and the secret | an authenticated session |
| `ConnectFirstQuery` | `SELECT 1` | its row |

Give each record a `method` dimension (`iam` or `password`) and an `idle` dimension (the gap before it,
as a string: EMF drops a metric whose dimension value is not one), so `phases.py` groups the readings
by both.

**What the probe needs**: `psycopg[binary]` in its package, since Lambda ships no libpq;
`rds-db:connect` on its role for each user it signs in as; the database user granted `rds_iam`; the
Region's RDS certificate bundle in its package; and the function's subnets and security group. Sign in
with the function's own `sslmode`, so the sign-in leg times what the function pays: the reference's
`verify-full` where the function verifies, `require` where it does not.

**Cost.** Nothing at the function's INIT: the probe is a separate function. In CloudWatch, each leg with
each `method` and `idle` value is one custom metric — six legs over two methods and four gaps make 48 —
billed monthly while the probe's lines keep arriving.

## Reference, Python with psycopg

```python
import json, os, socket, ssl, struct, time
import boto3, psycopg

HOST, PORT, NAME = os.environ["DATABASE_HOST"], 5432, os.environ["DATABASE_NAME"]
CA_BUNDLE = os.environ["RDS_CA_BUNDLE"]  # the path of the Region's RDS certificate bundle
rds = boto3.client("rds")


def _ms(since):
    return (time.perf_counter() - since) * 1000


def reading(user, password=None, idle="first"):
    legs = {}
    t = time.perf_counter(); address = socket.getaddrinfo(HOST, PORT, proto=socket.IPPROTO_TCP)[0][4][0]
    legs["ConnectDns"] = _ms(t)
    t = time.perf_counter(); raw = socket.create_connection((address, PORT), timeout=20)
    legs["ConnectTcp"] = _ms(t)
    t = time.perf_counter(); raw.sendall(struct.pack("!ii", 8, 80877103))
    if raw.recv(1) != b"S":
        raise RuntimeError("the server refused TLS")
    # Timing only: this socket carries no secret, so it skips the certificate check the sign-in makes.
    context = ssl.create_default_context(); context.check_hostname = False; context.verify_mode = ssl.CERT_NONE
    context.wrap_socket(raw, server_hostname=HOST).close()
    legs["ConnectTls"] = _ms(t)
    if password is None:
        t = time.perf_counter(); password = rds.generate_db_auth_token(DBHostname=HOST, Port=PORT, DBUsername=user)
        legs["ConnectToken"] = _ms(t)
    t = time.perf_counter()
    with psycopg.connect(host=HOST, hostaddr=address, port=PORT, dbname=NAME, user=user,
                         password=password, sslmode="verify-full", sslrootcert=CA_BUNDLE,
                         connect_timeout=20) as connection:
        legs["ConnectSignIn"] = _ms(t)
        t = time.perf_counter(); connection.execute("SELECT 1").fetchone()
        legs["ConnectFirstQuery"] = _ms(t)
    method = "password" if "ConnectToken" not in legs else "iam"
    print(json.dumps({"_aws": {"Timestamp": int(time.time() * 1000), "CloudWatchMetrics": [{
        "Namespace": "connection-probe", "Dimensions": [["method", "idle"]],
        "Metrics": [{"Name": leg, "Unit": "Milliseconds"} for leg in legs]}]},
        "method": method, "idle": idle, **legs}))


def handler(event, context):
    # Invoked by hand: {"user": "app_reader", "idle": "10m"}, adding "password" for the comparison.
    reading(event["user"], event.get("password"), idle=str(event.get("idle", "first")))
```

The TLS leg times Postgres's SSL request and the handshake on the TCP leg's socket. The sign-in then
opens a socket of its own and pays TCP and TLS again — a few milliseconds the rows above already show.

## Read it back

Where the person names the probe's log group, Step 4 of the skill runs, from the probe's deployment to
now:

```
aws logs filter-log-events --log-group-name <probe's group> --start-time <ms> --end-time <ms> \
  --max-items 200000 --filter-pattern '"ConnectSignIn"' --output json [--profile <p>] [--region <r>] \
  | python3 -I ${CLAUDE_PLUGIN_ROOT}/skills/lambda-web-app-speed/scripts/phases.py -
```

Lineage: modive's `listing-cold-connect-probe` (2026-10-26). In its subnets DNS took 31–65 ms, TCP
1–5 ms, TLS 42–69 ms and a password sign-in 45–109 ms, while the first IAM sign-in after 5 to 40 minutes
idle took 2,295–4,604 ms. Raising Aurora's capacity floor, the memory explanation, did not shorten it.
The legs named the cause's place, the IAM check; they did not explain it.
