export const meta = {
  name: 'refactor-loop',
  description: 'Gated closed-loop refactoring: propose -> critique -> apply -> test, looped until convergence. The JS is the cage (deterministic loop/gate/stop); agents are the only LLM leaves.',
  phases: [
    { title: 'Init' },
    { title: 'Loop' },
    { title: 'Report' },
  ],
}

// ---------------------------------------------------------------------------
// phil:refactor-loop — Workflow orchestrator (v1, ADR-008)
//
// The cage owns control flow here in JS: the loop, the iteration counter, the
// guard routing, the stop/HALT predicate. The model never sees the loop
// condition and cannot decide it is done. LLM judgment lives only in the
// agent() leaves: propose (what to refactor) and critique (is it sound).
//
// The JS sandbox cannot run Bash/FS, so gate execution, diff apply, revert,
// and ledger persistence are delegated to thin agents. The hard DECISION stays
// in JS (it routes on a schema-validated exit_code integer); only EXECUTION is
// delegated. Safety invariant #2 (proposer can't touch tests) is enforced by
// the G2 PreToolUse hook, which fires on any agent's write regardless of
// substrate — the proposer here also never receives Edit (it returns a diff as
// text), so it structurally cannot reach disk.
//
// Canonical spec: docs/design/refactor-loop/architecture.md (§1 state machine,
// §2 agent I/O schemas, §4 DAG ledger). Agent prompts below mirror
// agents/refactor-proposer.md and agents/refactor-critic-correctness.md.
// ---------------------------------------------------------------------------

// --- Locked config (architecture §11) ---
const MAX_ITER = (args && args.max_iterations) || 10
const THETA = (args && args.theta) || 0.6
const SCOPE = (args && args.scope) || '.'
const LEDGER_PATH = '.refactor-loop-ledger.md'
const RULES = '~/.claude/rules' // refactoring.md, coding.md, testing.md, refactoring-catalog.md, {cpp,python,typescript,react}.md
const PINNED = ['preserve-public-api', 'no-test-file-writes']

// --- Schemas (agent I/O is schema-validated => sound, not advisory) ---
const PROPOSAL_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  properties: {
    no_actionable: { type: 'boolean', description: 'true => nothing left worth refactoring; loop reaches DONE' },
    node_id: { type: 'string' },
    named_refactoring: { type: 'string', description: 'a named refactoring from refactoring-catalog.md' },
    target_span: { type: 'string', description: 'file:start-end' },
    stated_intent: { type: 'string', description: 'one line; NOT a reasoning trace' },
    depends_on: { type: 'array', items: { type: 'string' }, description: 'node_ids this refactor builds on' },
    diff: { type: 'string', description: 'a single unified diff, one refactoring, no test-file changes' },
    predicted_fixes: { type: 'array', items: { type: 'string' } },
    predicted_regressions_risk: { type: 'array', items: { type: 'string' } },
    public_api_touched: { type: 'boolean' },
  },
  required: ['no_actionable'],
}

const VERDICT_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  properties: {
    justification: { type: 'string', description: 'reasoning, written FIRST' },
    verdict: { type: 'string', enum: ['accept', 'revise', 'reject'] },
    confidence: { type: 'number' },
    per_criterion: {
      type: 'array',
      items: {
        type: 'object',
        additionalProperties: false,
        properties: {
          criterion: { type: 'string' },
          met: { type: 'boolean' },
          severity: { type: 'string', enum: ['major', 'minor', 'nit'] },
          type: { type: 'string' },
          mechanism: { type: 'string' },
          span: { type: 'string' },
          evidence: { type: 'string' },
        },
        required: ['criterion', 'met', 'severity'],
      },
    },
  },
  required: ['justification', 'verdict', 'confidence', 'per_criterion'],
}

const GATE_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  properties: {
    exit_code: { type: 'integer', description: '0 = green' },
    stdout: { type: 'string', description: 'tail of runner output (failures verbatim)' },
    public_api_changed: { type: 'boolean', description: 'Python(__all__/top-level defs) or TS(exports) signature diff; null-ish if unknown language' },
    runner: { type: 'string' },
  },
  required: ['exit_code'],
}

const APPLY_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  properties: {
    applied: { type: 'boolean' },
    error: { type: 'string' },
  },
  required: ['applied'],
}

// --- Prompt builders (mirror the agent specs) ---
function gatePrompt(kind) {
  return `You are the gate-runner for /phil:refactor-loop. Run the project's test gate and report results. Do NOT modify any files.
1. Detect the test runner: read the project CLAUDE.md for a declared test command first; else auto-detect (package.json scripts, pytest/pyproject, Makefile, go test, cargo test).
2. Run, in order, whichever exist: lint, type-check, then the test suite. Capture the FIRST non-zero exit code.
3. ${kind === 'post-apply'
      ? 'Also determine whether the PUBLIC API changed vs HEAD: for Python compare `__all__` + top-level def/class names; for TypeScript compare exported declarations. Set public_api_changed accordingly (omit/false if the language is neither).'
      : 'This is the baseline run; public_api_changed is not relevant.'}
Return exit_code (0 = all green), the tail of stdout (include failing test names/messages verbatim), and the runner used. Read exit codes yourself; never narrate past a non-zero exit.`
}

function proposerPrompt(ledger, lastFailure) {
  const open = ledger.nodes.filter(n => ['resolved', 'reverted', 'invalid'].includes(n.status))
  return `You are the refactor-proposer for /phil:refactor-loop. Propose the SINGLE next-best refactoring in scope \`${SCOPE}\`, as a named refactoring from ${RULES}/refactoring-catalog.md. Apply the standards in ${RULES}/refactoring.md and ${RULES}/coding.md. This is structure-only work: change structure, preserve behavior. You do NOT decide whether your change is safe and you never run tests.

Pinned constraints (never violate): ${PINNED.join(', ')}. In particular, produce NO changes to test files and do not broaden the public API unless you set public_api_touched:true.

Already-decided nodes (do NOT re-propose these spans/smells):
${open.length ? open.map(n => `- ${n.node_id} [${n.status}] ${n.smell} @ ${n.span}`).join('\n') : '- (none yet)'}
${lastFailure ? `\nThe previous attempt FAILED the gate. Evidence (learn from it, propose something different or smaller):\n${lastFailure}` : ''}

Output the predicted-impact manifest. If nothing in scope is worth refactoring (or only weak/cosmetic items remain), set no_actionable:true and omit the rest. Otherwise provide a single unified diff (one refactoring only, no test-file edits), node_id (e.g. R001 sequentially), named_refactoring, target_span, a one-line stated_intent, depends_on (node_ids of applied refactors this builds on, or []), predicted_fixes, predicted_regressions_risk, and public_api_touched.`
}

function criticPrompt(p) {
  return `You are the refactor-critic-correctness for /phil:refactor-loop. Judge the proposed diff against the behavior-preservation slice of the frozen rubric (${RULES}/refactoring.md "tests pass before and after", ${RULES}/testing.md). You are read-only and independent: you do not see the proposer's reasoning, you do not edit code, you do not run tests.

Proposed refactoring: ${p.named_refactoring} @ ${p.target_span}
Stated intent (one line): ${p.stated_intent}
Diff:
\`\`\`diff
${p.diff}
\`\`\`

Write your justification FIRST, then the verdict. For each criterion you check, emit a typed item (criterion, met, severity major|minor|nit, type, mechanism, span as file:line, evidence = the rubric clause + the offending diff lines). A met:false with no span is not allowed. Anti-flattery: generic praise with no span is coerced to CANNOT_ASSESS, never accept — if you cannot ground a judgement in specific diff lines, say so rather than approving. Give an overall verdict (accept | revise | reject) and a confidence in [0,1].`
}

function applyPrompt(p) {
  return `Apply a single refactoring diff to the working tree for /phil:refactor-loop. Steps:
1. Run \`git apply --recount --check\` on the diff below; if it does not apply cleanly, return applied:false with the error. Do NOT improvise or hand-edit to make it fit.
2. If the check passes, run \`git apply --recount\` to apply it.
3. Never write to test files (this is also blocked by a PreToolUse hook).
Return applied:true on success, else applied:false + error.

Diff:
\`\`\`diff
${p.diff}
\`\`\``
}

function revertPrompt() {
  return `Revert the most recent uncommitted refactoring in the working tree for /phil:refactor-loop: run \`git checkout -- ${SCOPE}\` to restore tracked files to HEAD (the loop applies one refactor at a time, uncommitted, so this discards exactly the failed change). Confirm the working tree matches HEAD. Return applied:true when restored.`
}

function ledgerMarkdown(ledger, iter, status, activeRun) {
  const rows = ledger.nodes.map(n =>
    `| ${n.node_id} | ${n.smell || ''} | ${n.span || ''} | ${(n.depends_on || []).join(',') || '-'} | ${n.status} | ${n.note || ''} |`
  ).join('\n')
  return `# Refactor-Loop Ledger
status: ${status}
active-run: ${activeRun}
iter: ${iter} / max ${MAX_ITER}
theta: ${THETA}
pinned: [${PINNED.join(', ')}]

## Nodes
| id | smell | span | depends_on | status | note |
|----|-------|------|------------|--------|------|
${rows}
`
}

function writeLedgerPrompt(md) {
  return `Write the following content verbatim to the file \`${LEDGER_PATH}\` in the project root (create or overwrite). Return applied:true.\n\n\`\`\`markdown\n${md}\n\`\`\``
}

// G2 enforced in the cage (ADR-008): `git apply` (Bash) bypasses the Edit/Write PreToolUse
// matcher, so the deterministic test-file lockbox under the Workflow substrate is this scan of
// the diff's file headers. The G2 hook remains defense-in-depth for stray Edit/Write.
function touchesTestPath(diff) {
  const patterns = [/\/tests?\//, /\/spec\//, /\/__tests__\//, /_test\./, /\.test\./, /\.spec\./, /(^|\/)test_[^/]*\.py/, /conftest\.py/]
  const headers = (diff.match(/^[+-]{3} .*/gm) || [])
  return headers.some(line => patterns.some(p => p.test(line)))
}

// --- DAG helper: invalidate transitive dependents of a reverted node ---
function invalidateDependents(ledger, revertedId) {
  let changed = true
  while (changed) {
    changed = false
    for (const n of ledger.nodes) {
      if (n.status === 'pending' || n.status === 'resolved') {
        const deps = n.depends_on || []
        const broken = deps.some(d => {
          const dep = ledger.nodes.find(x => x.node_id === d)
          return d === revertedId || (dep && (dep.status === 'reverted' || dep.status === 'invalid'))
        })
        if (broken) { n.status = 'invalid'; n.note = `auto: prerequisite ${revertedId} reverted`; changed = true }
      }
    }
  }
}

// ===========================================================================
// INIT — baseline gate (G1). Never refactor on red.
// ===========================================================================
phase('Init')
const baseline = await agent(gatePrompt('baseline'), { schema: GATE_SCHEMA, label: 'baseline', phase: 'Init' })
if (!baseline || baseline.exit_code !== 0) {
  log('Baseline suite is RED — refusing to refactor on a red suite (G1 stop -> HALT).')
  return { status: 'HALT', reason: 'baseline-red', baseline: baseline ? baseline.stdout : 'gate agent failed', applied: [] }
}
log(`Baseline green (runner: ${baseline.runner || 'detected'}). Entering loop, max_iterations=${MAX_ITER}, theta=${THETA}.`)

const ledger = { nodes: [] }
const applied = []
let lastFailure = null

// Write the active-run sentinel so the G2 PreToolUse hook (defense-in-depth) engages for the
// duration of the run. The in-JS touchesTestPath() scan is the primary lockbox; this is belt
// and suspenders. Cleared at Report.
await agent(writeLedgerPrompt(ledgerMarkdown(ledger, 0, 'running', true)), { schema: APPLY_SCHEMA, label: 'sentinel-on', phase: 'Init' })

// ===========================================================================
// LOOP — the cage. JS owns the condition; the model cannot exit early.
// ===========================================================================
phase('Loop')
let iter = 0
while (iter < MAX_ITER) {
  iter++

  // --- PROPOSE ---
  const p = await agent(proposerPrompt(ledger, lastFailure), { schema: PROPOSAL_SCHEMA, label: `propose#${iter}`, phase: 'Loop' })
  if (!p || p.no_actionable) { log(`No actionable proposal at iter ${iter} -> DONE.`); break } // T2 -> DONE

  const node = { node_id: p.node_id || `R${String(iter).padStart(3, '0')}`, smell: p.named_refactoring, span: p.target_span, depends_on: p.depends_on || [], status: 'pending' }
  ledger.nodes.push(node)

  // --- REVIEW ---
  const v = await agent(criticPrompt(p), { schema: VERDICT_SCHEMA, label: `review#${iter}`, phase: 'Loop' })

  // --- GUARD (pure boolean; cage, no LLM) ---
  const hasBlockingMajor = !!v && Array.isArray(v.per_criterion) &&
    v.per_criterion.some(c => c.met === false && c.severity === 'major') && (v.confidence >= THETA)
  const blocked = !v || v.verdict === 'reject' || hasBlockingMajor
  if (blocked) { // T5 -> back to PROPOSE (llm_self_examine via lastFailure)
    node.status = 'invalid'
    node.note = `critic ${v ? v.verdict : 'no-verdict'} (conf ${v ? v.confidence : '?'})`
    lastFailure = v ? `Critic rejected the previous proposal (${v.verdict}, conf ${v.confidence}). Issues:\n` +
      v.per_criterion.filter(c => c.met === false).map(c => `- [${c.severity}] ${c.criterion} @ ${c.span || '?'}: ${c.mechanism || ''}`).join('\n')
      : 'Critic produced no valid verdict.'
    log(`iter ${iter}: critic blocked the proposal -> re-propose.`)
    continue
  }

  // --- G2 cage guard: refuse any diff that touches a test path (sound; substrate-native) ---
  if (touchesTestPath(p.diff || '')) {
    node.status = 'invalid'; node.note = 'G2 cage: diff touches a test path'
    lastFailure = 'Your diff modifies a test file. The pre-existing suite is the oracle — refactor production code only. Propose again without touching any test file.'
    log(`iter ${iter}: diff touches a test path -> rejected (G2 cage).`)
    continue
  }

  // --- APPLY (cage executes via thin agent; G2 hook is defense-in-depth on stray Edit/Write) ---
  const ap = await agent(applyPrompt(p), { schema: APPLY_SCHEMA, label: `apply#${iter}`, phase: 'Loop' })
  if (!ap || !ap.applied) {
    node.status = 'invalid'; node.note = `apply failed: ${ap ? ap.error : 'agent failed'}`
    lastFailure = `The diff did not apply cleanly: ${ap ? ap.error : 'unknown'}. Propose a fresh diff against current code.`
    log(`iter ${iter}: diff did not apply -> re-propose.`)
    continue
  }

  // --- TEST (hard gate; decision in JS on schema-validated exit_code) ---
  const g = await agent(gatePrompt('post-apply'), { schema: GATE_SCHEMA, label: `test#${iter}`, phase: 'Loop' })
  const manifestMismatch = !!g && g.public_api_changed === true && p.public_api_touched !== true
  if (!g || g.exit_code !== 0 || manifestMismatch) { // T8 -> REVERT
    await agent(revertPrompt(), { schema: APPLY_SCHEMA, label: `revert#${iter}`, phase: 'Loop' })
    node.status = 'reverted'
    node.note = manifestMismatch ? 'manifest mismatch: public API changed but predicted false (G4)' : `tests red (G3)`
    invalidateDependents(ledger, node.node_id) // DAG: dependents auto-invalid
    lastFailure = manifestMismatch
      ? 'Your refactor changed the public API but predicted public_api_touched:false. Either preserve the API or declare it.'
      : `Tests went red after applying:\n${g ? g.stdout : 'gate agent failed'}`
    log(`iter ${iter}: ${node.note} -> reverted, dependents invalidated.`)
    continue
  }

  // --- LEDGER green ---
  node.status = 'resolved'; node.note = 'green'
  applied.push(node.node_id)
  lastFailure = null
  log(`iter ${iter}: applied ${node.node_id} (${node.smell}) — green.`)
}

// ===========================================================================
// REPORT — persist the ledger (JS can't write files; delegate).
// ===========================================================================
phase('Report')
const status = iter >= MAX_ITER ? 'HALT-INCOMPLETE' : 'DONE'
// Clear the active-run sentinel (active-run:false) so the gated hooks go silent after the run.
await agent(writeLedgerPrompt(ledgerMarkdown(ledger, iter, status, false)), { schema: APPLY_SCHEMA, label: 'persist-ledger', phase: 'Report' })
log(`${status}: ${applied.length} refactor(s) applied over ${iter} iteration(s). Ledger -> ${LEDGER_PATH}`)
return { status, iterations: iter, applied, reverted: ledger.nodes.filter(n => n.status === 'reverted').map(n => n.node_id) }
