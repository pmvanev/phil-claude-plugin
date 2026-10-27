# DOCUMENT — composing the record and reviewing its prose

The prose review of `skills/edd/SKILL.md`'s DOCUMENT step. Read in full before composing the trail.

Read `${CLAUDE_PLUGIN_ROOT}/rules/writing.md` and `${CLAUDE_PLUGIN_ROOT}/rules/technical-communication.md`
before composing: every word this skill writes into the record follows them.

## 1. Draft where the review cannot reach the developer's words or the evidence

Compose each document — `expectations.md`, `verdicts.md`, `stabilize.md`, the evolution summary, and
the final report — as a draft file in a temporary directory outside the repository (`mktemp -d`), so
nothing touches the working tree before the review. In each draft:

- every `you wrote` or `you edited` field is replaced by a placeholder naming it —
  `[you wrote: expectation 2]`, `[you wrote: waiver reason, R001]` — so the review never sees the
  developer's words and no fix can reach them;
- every piece of evidence is referenced by path, never inlined: it is never passed to the review, and
  `evidence/` holds it out of the review's reach.

Tell the review that each placeholder stands for content the written document holds. Drop any
`[fitness]` finding whose only cause is a placeholder: no fix of composed text can answer it.

## 2. Review each draft

Run `phil:red-team-prose` (Skill tool) once per draft, with the draft's path, and use its Steps 1 to 5
only — its report; this skill's own ask replaces its Step 6, under SKILL.md's "Every ask". It applies
`phil:ai-eos`, `phil:eos` and `technical-communication.md` in one pass.

- **Advisory findings.** Put the `[tells]` and `[clarity]` findings marked auto-applicable to the
  developer: `apply`, `skip` or `stop`. On `apply`, apply them only to spans inside a `composed` field.
  A placeholder is never edited; a fix that would change one is dropped.
- **Fitness findings.** A `[fitness]` finding blocks done: it marks a document its reader cannot use.
  Put it to the developer with `fix`, `waive` and `stop`, each with its cost:
  - **fix** — rewrite the composed text from facts the run recorded, never inventing one; what this
    skill adds is `composed`. Review the draft again; the finding clears only when the review no
    longer reproduces it.
  - **waive** — take the developer's reason; record the finding, the reason and a timestamp in
    `verdicts.md`.
  - **stop** — end the run not done; write the trail as it stands, the finding recorded as standing.

  After a second fix round on the same document, offer only `waive` and `stop`.

After the run has ended — a stop, or two consecutive unanswered asks — compose and review the drafts,
but ask nothing: apply no fix, record every finding as standing, and write the trail.

## 3. Write, then check

Copy each reviewed draft into `docs/edd/<slug>/` (the evolution summary into `docs/evolution/`), and
restore each placeholder with the developer's words, verbatim. Then check, before reporting done:

- every restored field equals the words the developer gave, as recorded when they gave them;
- every file under `evidence/` is byte-identical to what the producer captured, checked against the
  hash recorded at capture.

A mismatch is a defect in this run: restore the recorded words or evidence, and say so in the report.

The final report carries one line on the review: how many documents it covered, how many fixes were
applied and skipped, any fitness finding fixed or waived, and that the evidence and the developer's
words are untouched.
