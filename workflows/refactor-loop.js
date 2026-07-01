export const meta = {
  name: 'refactor-loop',
  description: 'Gated closed-loop refactoring: propose -> critique -> apply -> test, with a bounded fix sub-loop before revert, looped until convergence. The JS is the cage (deterministic loop/gate/stop); agents are the only LLM leaves.',
  phases: [
    { title: 'Init' },
    { title: 'Loop' },
    { title: 'Report' },
  ],
}

// ---------------------------------------------------------------------------
// phil:refactor-loop — Workflow orchestrator (v1, ADR-008 + ADR-009)
//
// The cage owns control flow in JS: the loop, counters, guard routing, the
// stop/HALT predicate. The model never sees the loop condition and cannot
// decide it is done. LLM judgment lives only in the agent() leaves.
//
// JS cannot run Bash/FS, so gate/apply/commit/revert/ledger are delegated to
// thin agents; the hard DECISION stays in JS (routes on schema-validated
// exit_code). Safety: the proposer returns a diff as TEXT (no Edit), the cage
// scans the diff for test paths before apply, and the G2 PreToolUse hook is
// defense-in-depth.
//
// ADR-009 changes after the first run:
//  - fail fast if repo/test_cmd absent (never default REPO to the session cwd);
//  - HALT if the baseline collects zero tests (decorative-gate prevention);
//  - commit-on-green (durable green + audit trail + surgical revert);
//  - red -> bounded FIX sub-loop (repair the same refactor) before REVERT;
//  - REVERT is scoped (restore only the diff's files), never `git checkout -- .`;
//  - a node that can't be made to pass is marked `undoable` with findings.
//
// Canonical spec: docs/design/refactor-loop/architecture.md.
// ---------------------------------------------------------------------------

// --- Config ---
// args may arrive as a JSON STRING on some invocation paths (the first-run and
// second-run misfire: args.repo was undefined -> HALT-CONFIG). Normalize to a
// real object so the string-vs-object footgun can never default the target repo.
let A = {}
if (args && typeof args === 'object') A = args
else if (typeof args === 'string' && args.trim()) { try { A = JSON.parse(args) } catch (e) { A = {} } }

const MAX_ITER = A.max_iterations || 10
const MAX_FIX = (typeof A.max_fix_attempts === 'number') ? A.max_fix_attempts : 2
const THETA = A.theta || 0.6
const SCOPE = A.scope || '.'
const FOCUS = A.focus || '' // optional: narrow to a single function/class within SCOPE
const REPO = A.repo // REQUIRED — no default (ADR-009 D)
const TEST_CMD = A.test_cmd // REQUIRED — no default
const LEDGER_PATH = '.refactor-loop-ledger.md'
const RULES = '~/.claude/rules'
const PINNED = ['preserve-public-api', 'no-test-file-writes']
const WORKDIR = `Work inside the repository at \`${REPO}\` — cd into it first; all paths below are relative to it.`

// --- Schemas (agent I/O is schema-validated => sound, not advisory) ---
const PROPOSAL_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  properties: {
    no_actionable: { type: 'boolean', description: 'true => nothing left worth refactoring (PROPOSE) or this refactor is infeasible (FIX); ends the attempt' },
    node_id: { type: 'string' },
    named_refactoring: { type: 'string' },
    target_span: { type: 'string', description: 'file:start-end' },
    stated_intent: { type: 'string', description: 'one line; NOT a reasoning trace' },
    depends_on: { type: 'array', items: { type: 'string' } },
    diff: { type: 'string', description: 'a single unified diff, one refactoring, no test-file changes, paths relative to the repo root' },
    predicted_fixes: { type: 'array', items: { type: 'string' } },
    predicted_regressions_risk: { type: 'array', items: { type: 'string' } },
    public_api_touched: { type: 'boolean' },
    findings: { type: 'string', description: 'when no_actionable in a FIX context: why the refactor is infeasible' },
  },
  required: ['no_actionable'],
}

const VERDICT_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  properties: {
    justification: { type: 'string' },
    verdict: { type: 'string', enum: ['accept', 'revise', 'reject'] },
    confidence: { type: 'number' },
    per_criterion: {
      type: 'array',
      items: {
        type: 'object',
        additionalProperties: false,
        properties: {
          criterion: { type: 'string' }, met: { type: 'boolean' },
          severity: { type: 'string', enum: ['major', 'minor', 'nit'] },
          type: { type: 'string' }, mechanism: { type: 'string' },
          span: { type: 'string' }, evidence: { type: 'string' },
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
    tests_collected: { type: 'integer', description: 'number of tests the runner collected/ran' },
    stdout: { type: 'string', description: 'tail of runner output (failures verbatim)' },
    public_api_changed: { type: 'boolean' },
    runner: { type: 'string' },
  },
  required: ['exit_code'],
}

const APPLY_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  properties: { applied: { type: 'boolean' }, error: { type: 'string' } },
  required: ['applied'],
}

// --- Prompt builders ---
function gatePrompt(kind) {
  return `You are the gate-runner for /phil:refactor-loop. ${WORKDIR} Run the test gate and report results. Do NOT modify any files.
1. Run exactly this test command: \`${TEST_CMD}\`. Capture its exit code and how many tests were collected/run. This suite may take several minutes — set your Bash timeout to the maximum (600000 ms) so a slow-but-passing run is never mistaken for a failure. If the command is killed by a timeout (no real exit code), report exit_code:-1 and say so verbatim in stdout; do NOT report it as a test failure.
2. ${kind === 'post-apply'
      ? 'Also determine whether the PUBLIC API changed vs HEAD: Python compare `__all__` + top-level def/class names; TypeScript compare exported declarations. Set public_api_changed (false/omit for other languages).'
      : 'Baseline run; public_api_changed is not relevant.'}
Return exit_code (0 = green), tests_collected, the tail of stdout (failing test names/messages verbatim), and the runner. Read the exit code yourself; never narrate past a non-zero exit.`
}

function proposerPrompt(ledger, lastFailure) {
  const decided = ledger.nodes.filter(n => ['resolved', 'reverted', 'invalid', 'undoable'].includes(n.status))
  return `You are the refactor-proposer for /phil:refactor-loop. ${WORKDIR} Propose the SINGLE next-best refactoring in scope \`${SCOPE}\` (relative to the repo)${FOCUS ? `, narrowed to \`${FOCUS}\` (refactor only that function/class)` : ''}, as a named refactoring from ${RULES}/refactoring-catalog.md. Apply ${RULES}/refactoring.md and ${RULES}/coding.md. Structure-only: change structure, preserve behavior. You never run tests and never decide safety. Emit the diff with paths relative to the repo root so \`git apply\` works from there.

Pinned constraints (never violate): ${PINNED.join(', ')}. Produce NO test-file changes; do not broaden the public API unless you set public_api_touched:true.

Already-decided nodes — do NOT re-propose these (especially \`undoable\`, with the recorded reason):
${decided.length ? decided.map(n => `- ${n.node_id} [${n.status}] ${n.smell} @ ${n.span}${n.note ? ' — ' + n.note : ''}`).join('\n') : '- (none yet)'}
${lastFailure ? `\nContext from the previous node:\n${lastFailure}` : ''}

If nothing in scope is worth refactoring (or only weak/cosmetic items remain), set no_actionable:true. Otherwise provide: a single unified diff (one refactoring, no test edits), node_id (R001, R002, … sequentially), named_refactoring, target_span, one-line stated_intent, depends_on (node_ids of applied refactors this builds on, or []), predicted_fixes, predicted_regressions_risk, public_api_touched.`
}

function fixPrompt(candidate, failure) {
  return `You are the refactor-proposer for /phil:refactor-loop, in FIX mode. ${WORKDIR} Your previous diff for refactoring "${candidate.named_refactoring}" @ ${candidate.target_span} was applied and the gate went RED (or the API check failed). The change has already been reverted, so propose a CORRECTED diff for the SAME refactoring that preserves behavior.

Failing-gate evidence:
${failure}

Diagnose the failure, then emit a corrected manifest (same fields as a normal proposal) for the SAME refactoring intent. Keep paths relative to the repo root; no test-file edits. If you conclude this refactoring is genuinely infeasible without changing behavior (or the tests encode a contract the refactor would break), set no_actionable:true and put a one-paragraph explanation in \`findings\` — it will be recorded so the loop never re-attempts this.`
}

function criticPrompt(p) {
  return `You are the refactor-critic-correctness for /phil:refactor-loop. ${WORKDIR} (read-only — to inspect surrounding code if needed). Judge the proposed diff against the behavior-preservation slice of the frozen rubric (${RULES}/refactoring.md "tests pass before and after", ${RULES}/testing.md). Read-only and independent: you do not see the proposer's reasoning, you do not edit code, you do not run tests.

Proposed: ${p.named_refactoring} @ ${p.target_span}
Intent: ${p.stated_intent}
Diff:
\`\`\`diff
${p.diff}
\`\`\`

Justification FIRST, then verdict. Each criterion = (criterion, met, severity major|minor|nit, type, mechanism, span as file:line, evidence = rubric clause + offending lines). A met:false with no span is not allowed. Anti-flattery: generic praise with no span ⇒ CANNOT_ASSESS, never accept. Overall verdict (accept|revise|reject) + confidence in [0,1].`
}

function applyPrompt(p) {
  return `${WORKDIR} Apply a single refactoring diff to the working tree for /phil:refactor-loop. Steps:
1. \`git apply --recount --check\` the diff; if it does not apply cleanly, return applied:false + the error. Do NOT hand-edit to force it.
2. If the check passes, \`git apply --recount\`.
3. Never write to test files (also blocked by a PreToolUse hook).
Return applied:true on success, else applied:false + error.

Diff:
\`\`\`diff
${p.diff}
\`\`\``
}

function revertScopedPrompt(p) {
  return `${WORKDIR} Revert ONLY the current uncommitted refactoring for /phil:refactor-loop. The prior green refactors are committed, so restore just the files this diff touched back to HEAD: identify the files in the diff below and run \`git checkout -- <those files>\` (do NOT run \`git checkout -- .\` or touch anything else). Confirm those files match HEAD. Return applied:true when restored.

Diff:
\`\`\`diff
${p.diff}
\`\`\``
}

function commitPrompt(p, nodeId) {
  return `${WORKDIR} Commit the refactoring that just passed the gate for /phil:refactor-loop. Stage only the files changed by this refactoring and commit them with this message:

Refactor [${nodeId}]: ${p.named_refactoring} — ${p.stated_intent}

Use \`git add <changed files>\` then \`git commit\`. Do not stage unrelated files. Return applied:true on a successful commit.`
}

function writeLedgerPrompt(md) {
  return `${WORKDIR} Write the following content verbatim to \`${LEDGER_PATH}\` in the repo root (create or overwrite). Return applied:true.\n\n\`\`\`markdown\n${md}\n\`\`\``
}

function ledgerMarkdown(ledger, iter, status, activeRun) {
  const rows = ledger.nodes.map(n =>
    `| ${n.node_id} | ${n.smell || ''} | ${n.span || ''} | ${(n.depends_on || []).join(',') || '-'} | ${n.status} | ${(n.note || '').replace(/\n/g, ' ')} |`
  ).join('\n')
  return `# Refactor-Loop Ledger
status: ${status}
active-run: ${activeRun}
iter: ${iter} / max ${MAX_ITER}
theta: ${THETA}
max_fix_attempts: ${MAX_FIX}
pinned: [${PINNED.join(', ')}]

## Nodes
| id | smell | span | depends_on | status | note |
|----|-------|------|------------|--------|------|
${rows}
`
}

// Deterministic test-file lockbox under the Workflow substrate (git apply via Bash
// bypasses the Edit/Write PreToolUse matcher). The G2 hook is defense-in-depth.
function touchesTestPath(diff) {
  const patterns = [/\/tests?\//, /\/spec\//, /\/__tests__\//, /_test\./, /\.test\./, /\.spec\./, /(^|\/)test_[^/]*\.py/, /conftest\.py/]
  const headers = (diff.match(/^[+-]{3} .*/gm) || [])
  return headers.some(line => patterns.some(p => p.test(line)))
}

function invalidateDependents(ledger, revertedId) {
  let changed = true
  while (changed) {
    changed = false
    for (const n of ledger.nodes) {
      if (n.status === 'pending' || n.status === 'resolved') {
        const deps = n.depends_on || []
        const broken = deps.some(d => {
          const dep = ledger.nodes.find(x => x.node_id === d)
          return d === revertedId || (dep && (dep.status === 'reverted' || dep.status === 'invalid' || dep.status === 'undoable'))
        })
        if (broken) { n.status = 'invalid'; n.note = `auto: prerequisite ${revertedId} not landed`; changed = true }
      }
    }
  }
}

function tail(s, n) { return s ? String(s).slice(-(n || 1200)) : '' }

// ===========================================================================
// INIT
// ===========================================================================
phase('Init')

// Fail fast: the cage must not guess its target (ADR-009 D). Also catches the
// "args passed as a string" footgun (then args.repo is undefined).
if (!REPO || !TEST_CMD) {
  log('Missing required args. Pass a real JSON OBJECT: { repo, test_cmd, scope?, max_iterations?, max_fix_attempts?, theta? }.')
  return { status: 'HALT-CONFIG', reason: 'repo and test_cmd are required (no defaults)', applied: [] }
}

const baseline = await agent(gatePrompt('baseline'), { schema: GATE_SCHEMA, label: 'baseline', phase: 'Init' })
if (!baseline || baseline.exit_code !== 0) {
  log('Baseline suite is RED — refusing to refactor on a red suite (G1 -> HALT).')
  return { status: 'HALT', reason: 'baseline-red', baseline: baseline ? tail(baseline.stdout) : 'gate agent failed', applied: [] }
}
if (typeof baseline.tests_collected === 'number' && baseline.tests_collected === 0) {
  log('Baseline collected ZERO tests — a green from no tests is not a valid oracle (ADR-009 E -> HALT).')
  return { status: 'HALT', reason: 'no-tests-collected', applied: [] }
}
log(`Baseline green (runner: ${baseline.runner || 'detected'}, tests: ${baseline.tests_collected != null ? baseline.tests_collected : '?'}). Loop: max_iter=${MAX_ITER}, max_fix=${MAX_FIX}, theta=${THETA}.`)

const ledger = { nodes: [] }
const applied = []
let lastFailure = null
await agent(writeLedgerPrompt(ledgerMarkdown(ledger, 0, 'running', true)), { schema: APPLY_SCHEMA, label: 'sentinel-on', phase: 'Init' })

// ===========================================================================
// LOOP
// ===========================================================================
phase('Loop')
let iter = 0
while (iter < MAX_ITER) {
  iter++

  // --- PROPOSE ---
  const p = await agent(proposerPrompt(ledger, lastFailure), { schema: PROPOSAL_SCHEMA, label: `propose#${iter}`, phase: 'Loop' })
  if (!p || p.no_actionable) { log(`No actionable proposal at iter ${iter} -> DONE.`); break }

  const node = { node_id: p.node_id || `R${String(iter).padStart(3, '0')}`, smell: p.named_refactoring, span: p.target_span, depends_on: p.depends_on || [], status: 'pending' }
  ledger.nodes.push(node)

  // --- REVIEW ---
  const v = await agent(criticPrompt(p), { schema: VERDICT_SCHEMA, label: `review#${iter}`, phase: 'Loop' })
  const blockingMajor = !!v && Array.isArray(v.per_criterion) && v.per_criterion.some(c => c.met === false && c.severity === 'major') && (v.confidence >= THETA)
  if (!v || v.verdict === 'reject' || blockingMajor) { // GUARD: back-prompt
    node.status = 'invalid'; node.note = `critic ${v ? v.verdict : 'no-verdict'}`
    lastFailure = v ? `The critic rejected node ${node.node_id}. Issues:\n` + v.per_criterion.filter(c => c.met === false).map(c => `- [${c.severity}] ${c.criterion} @ ${c.span || '?'}: ${c.mechanism || ''}`).join('\n') : 'Critic produced no valid verdict.'
    log(`iter ${iter}: critic blocked ${node.node_id} -> re-propose.`)
    continue
  }

  // --- LAND: apply -> test, with a bounded FIX sub-loop (ADR-009 A) ---
  let candidate = p
  let landed = false
  let lastGate = null
  let infeasibleFindings = null
  for (let attempt = 0; attempt <= MAX_FIX; attempt++) {
    // G2 cage guard: never apply a diff that touches a test path
    if (touchesTestPath(candidate.diff || '')) {
      infeasibleFindings = 'Proposed diff modifies a test file; the suite is the oracle. Rejected by the cage.'
      break
    }
    const ap = await agent(applyPrompt(candidate), { schema: APPLY_SCHEMA, label: `apply#${iter}.${attempt}`, phase: 'Loop' })
    if (!ap || !ap.applied) {
      lastGate = { stdout: `diff did not apply: ${ap ? ap.error : 'agent failed'}` }
    } else {
      const g = await agent(gatePrompt('post-apply'), { schema: GATE_SCHEMA, label: `test#${iter}.${attempt}`, phase: 'Loop' })
      lastGate = g
      const mismatch = !!g && g.public_api_changed === true && candidate.public_api_touched !== true
      if (g && g.exit_code === 0 && !mismatch) { landed = true; break } // green!
      // red / mismatch: scoped-revert this attempt before trying a fix
      await agent(revertScopedPrompt(candidate), { schema: APPLY_SCHEMA, label: `revert#${iter}.${attempt}`, phase: 'Loop' })
    }
    if (attempt < MAX_FIX) {
      const evidence = lastGate ? ((lastGate.public_api_changed && !candidate.public_api_touched ? 'Public API changed but you predicted it would not.\n' : '') + tail(lastGate.stdout)) : 'unknown failure'
      const fix = await agent(fixPrompt(candidate, evidence), { schema: PROPOSAL_SCHEMA, label: `fix#${iter}.${attempt + 1}`, phase: 'Loop' })
      if (!fix || fix.no_actionable) { infeasibleFindings = (fix && fix.findings) || 'Proposer judged the refactor infeasible during the fix sub-loop.'; break }
      candidate = fix
    }
  }

  if (landed) {
    await agent(commitPrompt(candidate, node.node_id), { schema: APPLY_SCHEMA, label: `commit#${iter}`, phase: 'Loop' })
    node.status = 'resolved'; node.note = 'green, committed'
    applied.push(node.node_id); lastFailure = null
    log(`iter ${iter}: landed ${node.node_id} (${node.smell}) — green & committed.`)
  } else {
    // ensure tree is clean, then mark undoable + findings, invalidate dependents
    await agent(revertScopedPrompt(candidate), { schema: APPLY_SCHEMA, label: `revert-final#${iter}`, phase: 'Loop' })
    node.status = 'undoable'
    node.note = `findings: ${infeasibleFindings || `could not restabilize after ${MAX_FIX} fix attempt(s). Last: ${tail(lastGate && lastGate.stdout, 400)}`}`
    invalidateDependents(ledger, node.node_id)
    lastFailure = null // do not poison the next fresh proposal
    log(`iter ${iter}: ${node.node_id} undoable -> reverted, findings recorded, dependents invalidated.`)
  }
}

// ===========================================================================
// REPORT
// ===========================================================================
phase('Report')
const status = iter >= MAX_ITER ? 'HALT-INCOMPLETE' : 'DONE'
await agent(writeLedgerPrompt(ledgerMarkdown(ledger, iter, status, false)), { schema: APPLY_SCHEMA, label: 'persist-ledger', phase: 'Report' })
log(`${status}: ${applied.length} landed over ${iter} iteration(s). Ledger -> ${REPO}/${LEDGER_PATH}`)
return {
  status, iterations: iter, applied,
  undoable: ledger.nodes.filter(n => n.status === 'undoable').map(n => ({ id: n.node_id, findings: n.note })),
  invalid: ledger.nodes.filter(n => n.status === 'invalid').map(n => n.node_id),
}
