---
name: lambda-web-app-speed
description: This skill should be used when the user asks to "measure the cold start", "count our Lambda cold starts", "is it INIT or the handler", "why is the first load of our Lambda app slow", "why does our Lambda app take a while after idle", "read Init Duration or INIT_REPORT from CloudWatch", "what inside INIT takes the time", "which startup check makes the cold start slow", or runs /phil:lambda-web-app-speed. It measures an AWS Lambda function's cold path from its REPORT and INIT_REPORT lines, including the cold starts that carry no Init Duration, names the layer that owns it and times one level inside it, citing every command. Read-only; it recommends no fix. For load-time defects a file shows, use /phil:review-code.
---

# Lambda Web App Speed

Answer two questions from the function's own logs — **which layer owns this function's cold path, and
what inside that layer takes the time?** — and stop. This version measures, divides and drills one
level. It does not yet rank fixes, price the warmth options or measure the browser.

**Read the Principles in `${CLAUDE_PLUGIN_ROOT}/rules/lambda-web-app-speed.md` before measuring.** They
define what a cold start is, the two kinds that hide, and why the window starts at the last change.

## Hard rules

1. **Read AWS; change nothing.** Run only `aws lambda list-functions`,
   `aws lambda get-function-configuration` and `aws logs filter-log-events`. Never invoke the function,
   deploy it, change its configuration or force a cold start, and do not suggest forcing one: this
   version measures the cold starts that already happened. The role in use can usually do far more than
   read, so these limits rest on this prose. Read the project's code with Read, Grep and Glob to find a
   timing line; edit nothing.
2. **`python3` runs `cold-path.py` and `phases.py`, and nothing else.** `cold-path.py` computes the
   window and `phases.py` the gap to INIT, so no step needs arithmetic done by hand.
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

## Step 4 — Drill one level into the layer

Skip this step where `Look inside:` names no layer, and leave the report's `Inside` block out.

**Find the layer's group.** `INIT` reads the timing line's `phase=init` records; `first invoke` reads
`phase=first_request`. Where the line writes no group for the layer, the layer has no timing line.

**Look for an instrument the function already has**: a line in CloudWatch's Embedded Metric Format,
written once per cold start, that times the layer's phases. Grep the project's code for
`CloudWatchMetrics`, `add_metric` and `put_metric` beside `Milliseconds`, and keep the line written
during INIT — at module scope or from the build — not a per-request latency line. Where the search
finds none, or the code is not in the working directory, ask the person whether such a line exists and
its metric names; **this ask follows `${CLAUDE_PLUGIN_ROOT}/skills/shared/decision-request.md`.**

**Confirm the line keeps the convention `phases.py` reads**, from its code: each name without a dot is a
phase, and phases run one after another without overlapping; each name with a dot is a member that ran
concurrently inside the one phase its prefix starts. A line that writes a total beside its parts, or
phases that overlap, breaks it: treat the layer as having no timing line.

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

**When `phases.py` stops instead of reporting:** *not a complete response* — move the start later by
half the window's length and refetch; *no Embedded Metric Format line* — check the filter names one of
the line's phases, then treat the layer as having no timing line; *breaks the phase convention* — treat
the layer as having no timing line, and say why.

**Decide from the report, in this order:**

1. **No timing line for the layer** → `Next instrument:` the cold-start line in
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

## Step 5 — Report

```
Function: <name> · account <id> · <partition>/<region> · <memory> MB · last changed <LastModified>
Window: <start> to <end> — from <starts_at>

<the script's report, ending in its Look inside: line>
<the p75 line, where it applies>

Inside <the layer>:
<phases.py's report for the layer's group>
Cause: <what the largest phase names> — or — Next instrument: <which, what it costs at INIT, and that
the person deploys it>

Measured with:
  <the configuration read, exactly as run>
  <the --window call, exactly as run>
  <each fetch pipeline, exactly as run>
Read: <each project file a decision in Step 4 rests on>
```

Write each command with `${CLAUDE_PLUGIN_ROOT}` expanded, so it reruns as pasted. **The p75 line**,
where cold starts are under a quarter of invokes: `Cold starts are <share> of invokes: a p75 over all
requests cannot see them, so the cold path needs measuring as its own population, as here.`

Then stop. Recommend no fix: ranking fixes by what they save is not in this version. A load-time
defect a file shows is `/phil:review-code`'s, under the rule's `LWS-n` rows.

## Self-test

`self-test/README.md` registers the fixtures. `tests/test_lambda_cold_path.py` drives
`self-test/01-cold-path-split/` through `cold-path.py`, `tests/test_lambda_init_phases.py` drives
`self-test/02-init-phases/` through `phases.py` and holds the references, and
`tests/test_lambda_web_app_speed_command.py` holds the grant and this file's limits.
