# REVIEW — the curated input, the dispatches and the routing

The full REVIEW step of `skills/edd/SKILL.md`. Read in full before dispatching the reviewer.

Before any verdict, put the built work in front of an adversary — the article's second agent auditing
the first. Read `${CLAUDE_PLUGIN_ROOT}/skills/adversarial-review/SKILL.md` and compose its agents under
the contract it documents:

1. **Curate the input** as exactly `{ target, intent, standards, oracle_result? }`:
   - `target` — what the engine built: the changed source, test and prose files, and the entry points
     the evidence ran — excluding the engine's own logs, plans, notes and commit messages, which carry
     the builder's reasoning;
   - `intent` — the confirmed expectations, in risk order, each with its classification;
   - `standards` — for code, `${CLAUDE_PLUGIN_ROOT}/rules/coding.md`,
     `${CLAUDE_PLUGIN_ROOT}/rules/testing.md` and `${CLAUDE_PLUGIN_ROOT}/rules/architecture.md`, plus
     `${CLAUDE_PLUGIN_ROOT}/rules/test-patterns.md` when tests changed; for prose,
     `${CLAUDE_PLUGIN_ROOT}/rules/writing.md` and any rule the prose is about;
   - `oracle_result` — the run BUILD captured, inherited, never re-run; omitted when none exists.

   Pass the machine-produced oracle run, never the builder's reasoning, its self-assessment, or a
   claim that the tests pass.
2. **Dispatch `phil:adversarial-reviewer`** (Agent/Task) with that input. It returns a typed verdict;
   rewrite nothing in it.
3. **Verify each finding** by dispatching `phil:adversarial-verifier`, one fresh dispatch per finding,
   with `{ finding, target, intent, standards, oracle_result? }` and without the reviewer's
   justification, confidence or other findings. Keep the findings the judge confirms, applying any
   `corrected_severity`. List separately the refutes the judge marks could-not-establish with low
   `confidence`. Count the other refutes and drop them.

Route on the typed fields only, and re-judge nothing:

- **The label and verdict lead.** The developer's first ask opens its context block with the
  reviewer's `overall_label` (`sound-gate` or `draft-signal`), its `verdict`, and "raised N, confirmed
  M, refuted K", then the could-not-confirm list. Report `clean` with its label — a draft signal is not
  a verified pass — and `cannot-assess` as exactly that, never as approval.
- **Severity after the judge's `corrected_severity`.** A judge-confirmed `major` finding blocks done
  until the engine fixes it, or the developer waives it by name, with a reason the record keeps — both
  in FINDINGS. A confirmed `minor` or `nit` advises.

Attach a confirmed finding to an expectation only where its `span` or `evidence` names that
expectation's entry point or scenario; the developer sees it in that expectation's ask. Every other
confirmed finding — and every finding on a row trusted to the tests — goes to FINDINGS. The review
advises; the developer still decides every verdict.
