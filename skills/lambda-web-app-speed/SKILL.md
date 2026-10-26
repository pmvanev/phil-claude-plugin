---
name: lambda-web-app-speed
description: This skill should be used when the user asks to "measure the cold start", "count our Lambda cold starts", "is it INIT or the handler", "why is our Lambda app slow after idle", "what inside INIT takes the time", "which cold-start fix first", "what would keeping it warm cost", "what is our TTFB or LCP", or runs /phil:lambda-web-app-speed. From an AWS Lambda function's REPORT and INIT_REPORT lines it counts every cold start, including those with no Init Duration, names the layer that owns the wait and times one level inside it, ranks the fixes by time saved, prices keeping it warm, and splits one page load's first byte, citing every command. It reads AWS and changes nothing; with the person's agreement it loads one page they name. For load-time defects a file shows, use /phil:review-code.
---

# Lambda Web App Speed

Answer five questions from the function's own logs, its prices and one page load — **which layer owns
this function's cold path, what inside that layer takes the time, which fixes to make, in what order,
before stopping, what keeping it warm would cost, and where a page load's first byte goes?** The skill
measures, divides, drills one level, ranks, prices and stops. It decides no purchase and changes
nothing.

**Read the Principles in `${CLAUDE_PLUGIN_ROOT}/rules/lambda-web-app-speed.md` before measuring.** They
define what a cold start is, the two kinds that hide, and why the window starts at the last change.

## Hard rules

1. **Read AWS; change nothing.** Against AWS, run only `aws lambda list-functions`,
   `aws lambda get-function-configuration` and `aws logs filter-log-events`. Never invoke the function,
   deploy it, change its configuration or force a cold start, and do not suggest forcing one, with one
   exception: Step 7 loads one page the person names, once by `firstbyte.py` and once in a browser trace,
   after the person agrees, since each load runs the function and may meet a cold start. The role in use
   can usually do far more than
   read, so these limits rest on this prose. Read the project's code with Read, Grep and Glob to find a
   timing line; edit nothing.
2. **`python3` runs `cold-path.py`, `phases.py`, `rank.py`, `warmth.py` and `firstbyte.py`, and nothing
   else.** The scripts compute every figure, so no step needs arithmetic done by hand. Two of them read
   the network: `warmth.py` fetches AWS's public price list, and `firstbyte.py --get` loads the page the
   person names, once, as a first visit would — no cookie, no credential.
3. **Cite every number.** The report ends with a `Measured with:` block holding every command exactly as
   run, so the person can rerun them.
4. **Read no application line but a timing line**: the function's own, or a probe's the person names.
   Each filter pattern selects platform lines or a timing line's records, and each script drops any
   other line unread. Print no
   raw log event; show the scripts' reports instead.

Put `--profile` and `--region` after the subcommand (`aws logs filter-log-events --profile …`), never
before it, so each call matches its grant.

## Step 1 — Resolve the function

- **Profile and region.** Use any the person named; otherwise the CLI's defaults.
- **Function.** Take the argument. With none, run `aws lambda list-functions --query
  'Functions[].[FunctionName,Runtime,MemorySize]' --output text`. Where four or fewer could serve web
  requests, ask which one a person's first page load waits on; otherwise list them and ask the person to
  name it. **This ask follows `${CLAUDE_PLUGIN_ROOT}/skills/shared/decision-request.md`.** Load it before
  the call.
- **Configuration.** Run `aws lambda get-function-configuration --function-name <f> --output json --query
  '{FunctionArn:FunctionArn,LastModified:LastModified,MemorySize:MemorySize,Runtime:Runtime,Architectures:Architectures[0],LogGroup:LoggingConfig.LogGroup,LogFormat:LoggingConfig.LogFormat}'`.
  Take the partition, Region and account from `FunctionArn`
  (`arn:<partition>:lambda:<region>:<account>:function:<name>`).
- **Stop** where `LogFormat` is `JSON`: this version reads the text format only. Where `LogGroup` is not
  `/aws/lambda/<f>`, the group may be shared with other functions; say so in the report as a limit.

## Step 2 — Choose the window

Run `python3 -I ${CLAUDE_PLUGIN_ROOT}/skills/lambda-web-app-speed/scripts/cold-path.py --window
<LastModified>`. It prints the start and end in epoch milliseconds and ISO form, and `starts_at`: the
last change, or fourteen days ago where the change is older. `LastModified` moves on any configuration
change, not only a code deploy; either one makes a new function to measure.

## Step 3 — Fetch and measure

Run, with the Bash tool's timeout set to 600000 ms:

```
aws logs filter-log-events --log-group-name <group> --start-time <start_ms> --end-time <end_ms> \
  --max-items 200000 --filter-pattern '?"REPORT RequestId" ?INIT_REPORT' --output json \
  [--profile <p>] [--region <r>] \
  | python3 -I ${CLAUDE_PLUGIN_ROOT}/skills/lambda-web-app-speed/scripts/cold-path.py -
```

**A second window.** Where the window starts at the last change and the report shows fewer than five
cold starts with `Init Duration`, measure again with `--days 14` in place of `--window`, and report both
under their own `Window:` lines, saying the second mixes versions.

**When the script stops instead of reporting**, or reports a truncated fetch, follow its entry in
`${CLAUDE_PLUGIN_ROOT}/skills/lambda-web-app-speed/references/when-a-script-stops.md`.

The script reads each log stream in time order and reports:

- **Cold starts, in three kinds**: with `Init Duration`; after a failed INIT; and suppressed inits,
  after an invoke that timed out or crashed. Only the first carries `Init Duration`.
- **Failed INITs**, timed out and errored, and **failed invokes**, counted apart.
- **Each slice's spread** — recorded INIT, the first invoke after it, the unsplit cold starts, and warm
  invokes — at nearest-rank p50 and p95, with the maximum. Over twenty values or fewer, p95 is the
  maximum, and the table says so.
- **The owner**: the layer that took more of the cold-start time whose split the logs record. A failed
  INIT counts its logged duration to INIT; a cold start that folds INIT into `Duration` counts to
  neither.
- **`Look inside:`** — the layer to look inside first, and why. INIT where INIT reached its 10 s
  ceiling, since each person behind a timeout waited ten seconds before the retry began; no layer where
  the unsplit time outweighs the owner's share or no cold start happened; otherwise the owner.

## Step 4 — Drill one level into the layer

Skip this step where `Look inside:` names no layer, and leave the report's `Inside` block out.

**Find the layer's group.** `INIT` reads the timing line's `phase=init` records; `first invoke` reads
`phase=first_request`. Where the line writes no group for the layer, the layer has no timing line.

**Look for an instrument the function already has**: a line in CloudWatch's Embedded Metric Format,
written once per cold start, that times the layer's phases. Grep the project's code for
`CloudWatchMetrics`, `add_metric` and `put_metric` beside `Milliseconds`, and keep the line written
during INIT — at module scope or from the build — not a per-request latency line. Where the search
finds none, or the code is not in the working directory, ask the person whether such a line exists and
its metric names; **this ask follows `${CLAUDE_PLUGIN_ROOT}/skills/shared/decision-request.md`.** Where
no name is known, filter on the layer's dimension instead, `'{ $.phase = "init" }'` for INIT: `phases.py`
keeps only Embedded Metric Format records and drops any other line unread.

**Confirm the line keeps the convention `phases.py` reads**, from its code: each name without a dot is a
phase, and phases run one after another without overlapping; each name with a dot is a member that ran
concurrently inside the one phase its prefix starts. A line that writes a total beside its parts, or
phases that overlap, breaks it: treat the layer as having no timing line. Where the code is not at
hand, say the convention went unconfirmed; a line of one phase cannot break it.

**Divide the line's records** over the window Step 3 last measured — the narrowed one where it narrowed,
the first where it reported two — with the Bash tool's timeout set to 600000 ms. Filter on a phase name
every record carries, and pass the INIT row's p50 and the cold-start count from Step 3's report:

```
aws logs filter-log-events --log-group-name <group> --start-time <start_ms> --end-time <end_ms> \
  --max-items 200000 --filter-pattern '"<phase name>"' --output json [--profile <p>] [--region <r>] \
  | python3 -I ${CLAUDE_PLUGIN_ROOT}/skills/lambda-web-app-speed/scripts/phases.py \
      --init-p50 <INIT p50, seconds> --cold-starts <cold starts> -
```

`scripts/phases.py` reports, per group: each phase at p50, p95, maximum and total; the time the code
timed itself, and the untimed gap to `Init Duration`; the largest phase, by total time across the
window; and that phase's members beside it, unsummed, each marked where it waits with the phase in the
same cold starts. It names a truncated fetch as `cold-path.py` does.

**When `phases.py` stops instead of reporting**, follow its entry in
`${CLAUDE_PLUGIN_ROOT}/skills/lambda-web-app-speed/references/when-a-script-stops.md`.

**Decide from the report, in this order:**

1. **No timing line for the layer**, or a line of one undivided phase, which divides nothing →
   `Next instrument:` the cold-start line in
   `${CLAUDE_PLUGIN_ROOT}/skills/lambda-web-app-speed/references/cold-start-line.md`.
2. **"The untimed gap outweighs the largest phase"** → `Cause:` time spent outside the code's own
   clock; name it, and propose nothing in this version.
3. **The "wait alike" sentence**, or every member marked → the members share something no line times.
   Where the code shows they connect to one database the same way — one engine, one pool, one sign-in
   — → `Next instrument:` a probe timing the connection's legs, in
   `${CLAUDE_PLUGIN_ROOT}/skills/lambda-web-app-speed/references/connection-legs.md`. Where the project
   already holds such a probe, ask whether it still runs and where its readings are before proposing
   another. Otherwise → `Next instrument: none in this version`, naming what they share.
4. **Otherwise** → `Cause:` the largest phase, or, where it has members, its slowest member.

**Propose an instrument only for an unexplained slice**, as those tests find one, and say what it costs
at INIT. Show the reference adapted to the names the project's code uses, and stop: the person deploys
it, and the next run reads it. Deploy nothing yourself.

**Where `Look inside:` chose INIT because INIT timed out**, say that a timed-out attempt writes no line:
the phases describe the INITs that finished, a retry among them, and not the attempts that hit the
ceiling.

**A probe already deployed.** Where the person names a probe's log group, read it with the pipeline
above, filtering on `"ConnectSignIn"` from the probe's deployment to now, and set its `method` and
`idle` groups side by side.

## Step 5 — Rank the fixes and draw the line

Skip this step where Step 4 was skipped, or found the untimed gap. Where Step 4 named a `Cause:`, rank
the fixes that act on it. Where it proposed an instrument, rank nothing — no slice is divided yet — but
still list the experiments.

**The candidates.** For a `Cause:`, take each fix that acts on it: the Preferred form of the rule's
`LWS-n` row that names it, where one does, otherwise the Principle that does. Add the machine changes
as experiments: memory, from Step 1's `MemorySize`, and moving work from the first invoke into INIT
where the first invoke owns the path. Draw every figure from Steps 1, 3 and 4, or from a measurement
the person gives and you cite.

Write each candidate in the shape `${CLAUDE_PLUGIN_ROOT}/skills/lambda-web-app-speed/references/candidates.md`
gives — read it before the first candidate — and pass the path's figures with them:

- **`now_ms`**: the `Cold wait` row's p50 from Step 3's report — each recorded cold start's INIT plus
  its first invoke.
- **`target_ms`**: the project's own cold-path budget, where its docs or the person state one. Where
  none is stated, ask the person for one, following
  `${CLAUDE_PLUGIN_ROOT}/skills/shared/decision-request.md`; where they give none, pass `null`: the
  report then draws no stopping line. Borrow no client-side target such as TTFB's 0.8 s, which counts
  every page load and the network besides.
- **`noise_ms`**: the spread of repeated measurements of the same path, where the project has them;
  otherwise `null`.

`scripts/rank.py` computes each saving from its basis; orders the fixes by the time each saves, largest
first, effort breaking near-ties and the standard pattern first among equals; lists the experiments
apart, cheapest first; lists a range that starts at nothing or spans more than three times its bottom
as too wide to rank; drops below the line each fix whose saving stays inside the noise; and draws the
stopping line where the path meets the target, or says the ranked fixes cannot reach it. It refuses a
candidate with no evidence, or a field it cannot read.

**Stop at the line.** Recommend the ranked fixes down to it, and the experiments as experiments: make
one, measure again, keep it or revert it. After any fix the next run measures again, since the largest
slice moves. A load-time defect a file shows is `/phil:review-code`'s, under the rule's `LWS-n` rows,
whether or not it ranks here.

## Step 6 — Price the warmth

Price keeping the function warm for its own traffic — one environment and the measured peak under
provisioned concurrency, SnapStart where the runtime and partition offer it, a heartbeat from open
pages — over fourteen days, whatever window Step 3 measured: traffic does not change with the code, and
a short window scales a few hours up to a month. Run `cold-path.py --days 14` for the window, then, with
the Bash tool's timeout set to 600000 ms:

```
aws logs filter-log-events --log-group-name <group> --start-time <start_ms> --end-time <end_ms> \
  --max-items 200000 --filter-pattern '?"REPORT RequestId" ?INIT_REPORT' --output json [--profile <p>] [--region <r>] \
  | python3 -I ${CLAUDE_PLUGIN_ROOT}/skills/lambda-web-app-speed/scripts/cold-path.py --json - \
  | python3 -I ${CLAUDE_PLUGIN_ROOT}/skills/lambda-web-app-speed/scripts/warmth.py --region <region> \
      --memory-mb <MemorySize> --runtime <Runtime> --arch <Architectures> --window-days <days> -
```

Take `<days>` from that `--days 14` output, and the rest from Step 1. `scripts/warmth.py` fetches the
Region's prices from AWS's public price list, which needs no credentials, scales the traffic to a month,
and reports each option's monthly price, what it removes and what it leaves, and its price per cold
start, at least. It refuses a truncated fetch, and names `cold-path.py` where that stage stopped first;
say either, and price nothing.

Present the table as prices, not advice: keeping warm is a purchase, and the person decides. The cold
start worth buying away is the one a present person pays; the table's header names how many the window
held.

## Step 7 — Measure one page load

**The page.** Take the URL from `--url`; otherwise ask the person for the page a first visit lands on,
or whether to skip this step. Before loading it, say that each load runs the function and may meet a
cold start, and ask the person to agree. **Both asks follow
`${CLAUDE_PLUGIN_ROOT}/skills/shared/decision-request.md`.** Where the person declines or names no page,
skip this step and say the browser went unmeasured.

1. **Time the first byte.** Run `python3 -I ${CLAUDE_PLUGIN_ROOT}/skills/lambda-web-app-speed/scripts/firstbyte.py --get <url>`
   once. It prints one JSON line: the status, the GET's DNS, TCP, TLS and wait, and the window to
   fetch, `fetch_start_ms` to `fetch_end_ms`.
2. **Trace the largest paint.** Where the session offers a browser performance trace, such as the
   Chrome DevTools MCP server's, open a blank page in an isolated context, start the trace without a
   reload, navigate once to the URL, stop the trace and close the page — one load, no other interaction; it
   meets the environment step 1 warmed, so report it as a warm load, and say whether the browser was
   signed in. Otherwise ask the person, under the same standard, for the LCP of a Lighthouse run of the
   page, and cite it; failing both, say LCP went unmeasured.
3. **Split the first byte.** The trace gave CloudWatch time to receive the function's lines. Run:

   ```
   aws logs filter-log-events --log-group-name <group> --start-time <fetch_start_ms> \
     --end-time <fetch_end_ms> --max-items 200000 --filter-pattern '?"REPORT RequestId" ?INIT_REPORT' \
     --output json [--profile <p>] [--region <r>] \
     | python3 -I ${CLAUDE_PLUGIN_ROOT}/skills/lambda-web-app-speed/scripts/firstbyte.py --split '<the JSON line>' -
   ```

   It splits the first byte into the network, the function — INIT on a cold start, and the invoke —
   and the rest: the front door, placement, one round trip and, on a cold start, Lambda's setup before
   INIT. It leaves the function unsplit where the response was not 2xx, where no single `REPORT`
   matches, or where the figures cannot hold together; say which. Where it finds no `REPORT`, fetch again
   once: CloudWatch receives lines seconds late.

Set each against its target — TTFB within 0.8 s, LCP within 2.5 s — as one sample: the targets name the
75th percentile of real page loads, which one load cannot show. Say whether the GET met a cold start.

## Step 8 — Report

```
Function: <name> · account <id> · <partition>/<region> · <memory> MB · last changed <LastModified>
Window: <start> to <end> — from <starts_at>

<the script's report, ending in its Look inside: line>
<the p75 line, where it applies>

Inside <the layer>:
<phases.py's report for the layer's group>
Cause: <what the largest phase names> — or — Next instrument: <which, what it costs at INIT, and that
the person deploys it>

<rank.py's report, where Step 5 ran>

<warmth.py's table>

<firstbyte.py's split, and the LCP with its source — or that the browser went unmeasured, and why>

Measured with:
  <the configuration read, exactly as run>
  <the --window call, exactly as run>
  <each fetch pipeline, exactly as run>
  <the rank.py call, with its candidates>
  <the warmth pipeline, and each firstbyte.py call, exactly as run>
Read: <each project file a decision in Step 4 or 5 rests on>
Prices: <the price list's publication date>
```

Write each command with `${CLAUDE_PLUGIN_ROOT}` expanded, so it reruns as pasted. **The p75 line**,
where cold starts are under a quarter of invokes: `Cold starts are <share> of invokes: a p75 over all
requests cannot see them, so the cold path needs measuring as its own population, as here.`

Then stop.

## Self-test

`self-test/README.md` registers the fixtures, each driven through its script by its test:
`01-cold-path-split/` by `tests/test_lambda_cold_path.py`, `02-init-phases/` and the references by
`tests/test_lambda_init_phases.py`, `03-rank-replay/` by `tests/test_lambda_rank.py`,
`04-warmth-prices/` by `tests/test_lambda_warmth.py`, and `05-first-byte/` by
`tests/test_lambda_first_byte.py`. `tests/test_lambda_web_app_speed_command.py` holds the grant and this
file's limits.
