# Guard G10 — anti-premature-exit (Stop hook)
#
# Forces the refactor-loop to keep going until its DONE predicate is satisfied, instead of
# the model ending the turn mid-loop. Gated on the refactor-loop sentinel so it NEVER traps
# unrelated sessions: it fires only when .refactor-loop-ledger.md exists with active-run:
# true. When the loop reaches DONE/HALT it clears active-run, and this hook goes silent.
#
# Protocol: reads the hook payload as JSON on stdin; to force continuation, prints a JSON
# decision with "decision": "block" and a reason that is fed back to the model.

$ErrorActionPreference = 'Stop'

try {
    $raw = [Console]::In.ReadToEnd()
    $payload = $raw | ConvertFrom-Json
} catch {
    exit 0  # malformed payload: allow the stop
}

# Avoid an infinite loop: if this Stop was itself triggered by a prior block, allow it.
if ($payload.stop_hook_active -eq $true) { exit 0 }

$cwd = if ($payload.cwd) { $payload.cwd } else { (Get-Location).Path }
$ledger = Join-Path $cwd '.refactor-loop-ledger.md'

# Sentinel gate: no active run => not our session => allow the stop.
if (-not (Test-Path $ledger)) { exit 0 }
$ledgerText = Get-Content $ledger -Raw
if ($ledgerText -notmatch 'active-run:\s*true') { exit 0 }

# An active run is still in progress and the model tried to stop. Re-inject "continue".
$decision = @{
    decision = 'block'
    reason   = 'refactor-loop guard G10: the run is still active (.refactor-loop-ledger.md has active-run: true). Continue the state machine until the DONE predicate (green AND no unresolved >=major above threshold AND iter < max) or HALT (iter >= max) is reached, then clear active-run. Do not end the turn before the guard is satisfied.'
}
$decision | ConvertTo-Json -Depth 4
exit 0
