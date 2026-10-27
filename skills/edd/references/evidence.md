# EVIDENCE — the steps, in order

The full EVIDENCE step of `skills/edd/SKILL.md`. Read in full before gathering any evidence.

Skip every expectation trusted to the tests. Gather evidence for the rest in the risk order CAPTURE
set.

**An expectation not executable in the loop** dispatches nothing: handle it in its place in the risk
order, skipping the steps below. Tell the developer the confirmed blocker and ask them to spot-check
it by hand or stop. Record which they chose and, for a spot-check, what they observed, in their own
words, labelled `you wrote`. A spot-check goes to ADJUDICATE like any other evidence.

For every other expectation, do the least that yields real evidence:

1. **Reuse if it already exists.** If the engine already produced relevant executed evidence — a
   DELIVER demo, a captured transcript of the behaviour itself — the builder made it. Dispatch the
   producer (step 2) with that artifact as `context`, to re-run its reproduce command and capture
   what that emits: one run, and the evidence stays out of the builder's hands. A test-suite run is
   not reusable evidence: re-running it yields a pass count, which step 3 rejects. The developer
   judges relevance at ADJUDICATE; if they say the evidence is irrelevant, commission fresh evidence
   and rebuild nothing: the thing itself was never judged.
2. **Otherwise commission it — from a non-builder.** Dispatch `phil:edd-evidence-producer` (Agent/Task)
   with the `expectation`, its `classification`, the `target`, any named `scenario` and any `context`
   its contract names, to run or render the thing and capture the raw output **verbatim** with the
   command that reproduces it. The producer is a **different actor than whatever built the thing** —
   it has no Edit or Write tool, and its contract forbids changing what it runs against. This
   separation of powers is the whole reason the gate exists.
   - For a **checkable** expectation, the evidence is one scenario run: its inputs and the verbatim
     output, with the reproduce command.
   - For a **qualitative** expectation, it is the thing run or rendered, captured verbatim.
   - For a row the classification table marks `approval test`, send `classification: approval test`:
     the evidence is the test's output alone, which STABILIZE later matches byte for byte.
   - A **partially verifiable** run — a Terraform plan, a dry run, a migration against a test
     database — is executed evidence of what it shows. The producer says in its return what the run
     leaves unshown, so the developer judges the gap, not only the output.
   - For a checkable expectation an **approval test** pins, it is the test's first output.
3. **Reject narration.** If what comes back (from either path) is a description, a summary, or a
   claim with no reproducible artifact, it is **narration, not evidence** — the article calls it
   *generative* evidence. Reject it and re-commission a real run. A test runner's `"all tests passed"`,
   or a pass count, is narration for this gate: it reports a verdict without showing the behaviour.
   Never adjudicate against narration. When re-commissioning, name the scenario to run as `scenario`
   and send no `context`, so the producer runs the behaviour, not the suite. On a second narrated
   return for the same expectation, stop re-commissioning and put both returns to the developer, who
   names the scenario to try, spot-checks it by hand, or stops.
4. **A producer that cannot run it.** A producer that reports it *cannot produce executed evidence*
   has given neither evidence nor narration: report it to the developer rather than re-commissioning,
   since the same run fails the same way. Act on its cause:
   - **the build is missing** — an entry point not found, a build absent: route the expectation back
     to the engine — a rebuild, under BUILD's rule — then gather evidence again; after a second cannot-run for the same expectation, ask
     the developer to send it back again, spot-check it by hand, or stop;
   - **the environment cannot run it** — a browser, a paid API, a production-only condition: tell the
     developer, who confirms it as a blocker and spot-checks it by hand or stops, as above.

Record a hash of each captured artifact when it arrives: DOCUMENT checks `evidence/` against it.

The output, per expectation, is an **executed artifact + its reproduce command**, a recorded opt-out,
or a recorded hand spot-check — ready for the developer.
