---
name: lambda-web-app-speed
description: This skill should be used when the user asks to "measure the cold start", "count our Lambda cold starts", "is it INIT or the handler", "why is the first load of our Lambda app slow", "why does our Lambda app take a while after idle", "read Init Duration or INIT_REPORT from CloudWatch", or runs /phil:lambda-web-app-speed. It measures an AWS Lambda function's cold path from its REPORT and INIT_REPORT lines, including the cold starts that carry no Init Duration, names the layer to look inside, and cites every command. Read-only; it recommends no fix. For load-time defects a file shows, use /phil:review-code.
---

# Lambda Web App Speed

Answer one question — **which layer owns this function's cold path?** — from the function's own logs,
and stop. This version measures and divides. It does not yet drill into the largest slice, rank fixes,
price the warmth options or measure the browser.

**Read the Principles in `${CLAUDE_PLUGIN_ROOT}/rules/lambda-web-app-speed.md` before measuring.** They
define what a cold start is, the two kinds that hide, and why the window starts at the last change.

## Hard rules

1. **Read AWS; change nothing.** Run only `aws lambda list-functions`,
   `aws lambda get-function-configuration` and `aws logs filter-log-events`. Never invoke the function,
   deploy it, change its configuration or force a cold start, and do not suggest forcing one: this
   version measures the cold starts that already happened. The role in use can usually do far more than
   read, so these limits rest on this prose.
2. **`python3` runs `cold-path.py` and nothing else.** The script computes the window, so no step needs
   arithmetic done by hand.
3. **Cite every number.** The report ends with a `Measured with:` block holding every command exactly as
   run, so the person can rerun them.
4. **Read no application line.** The filter pattern below selects platform lines, and the script drops
   any other line unread. Print no raw log event; show the script's report instead.

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
  '{FunctionArn:FunctionArn,LastModified:LastModified,MemorySize:MemorySize,Runtime:Runtime,LogGroup:LoggingConfig.LogGroup,LogFormat:LoggingConfig.LogFormat}'`.
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

**When the script stops instead of reporting:**

- *Not a complete response*: the fetch was cut off. Move the window's start later by half its length, refetch, and
  say the window was narrowed.
- *SnapStart restores*: stop and say this version does not divide restores.
- *No REPORT line*: the function served nothing in the window. Where the window starts at the last
  change, measure `--days 14` and say it mixes versions; otherwise report that it served nothing.
- *Truncated*, in the report itself: the fetch hit its item cap, and the report names where it stopped.
  Say so beside the numbers; they cover the window up to that moment.

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

## Step 4 — Report

```
Function: <name> · account <id> · <partition>/<region> · <memory> MB · last changed <LastModified>
Window: <start> to <end> — from <starts_at>

<the script's report, ending in its Look inside: line>
<the p75 line, where it applies>

Measured with:
  <the configuration read, exactly as run>
  <the --window call, exactly as run>
  <the fetch pipeline, exactly as run>
```

Write each command with `${CLAUDE_PLUGIN_ROOT}` expanded, so it reruns as pasted. **The p75 line**:
where cold starts are under a quarter of invokes, say that a p75 over all requests cannot see them, so
the cold path needs measuring as its own population, as here.

Then stop. Recommend no fix: choosing among fixes needs the next level of timing inside the layer,
which this version does not take. A load-time defect a file shows is `/phil:review-code`'s, under the
rule's `LWS-n` rows.

## Self-test

`self-test/README.md` registers the fixtures. `tests/test_lambda_cold_path.py` drives
`self-test/01-cold-path-split/` through the script, and `tests/test_lambda_web_app_speed_command.py`
holds the grant and this file's limits.
