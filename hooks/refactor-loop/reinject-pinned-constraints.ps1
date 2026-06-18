# Guard G7 — pinned-constraint re-inject (UserPromptSubmit hook)
#
# Re-asserts the durable, compaction-immune pinned constraints from the ledger header at
# every prompt boundary, so context compaction can never silently evict a safety rule.
# Decay belongs on world state, never on rules. Gated on the refactor-loop sentinel so it
# only adds context during an active run.
#
# Protocol: reads the hook payload as JSON on stdin; to inject context, prints a JSON object
# with hookSpecificOutput.additionalContext (UserPromptSubmit).

$ErrorActionPreference = 'Stop'

try {
    $raw = [Console]::In.ReadToEnd()
    $payload = $raw | ConvertFrom-Json
} catch {
    exit 0
}

$cwd = if ($payload.cwd) { $payload.cwd } else { (Get-Location).Path }
$ledger = Join-Path $cwd '.refactor-loop-ledger.md'

if (-not (Test-Path $ledger)) { exit 0 }
$ledgerText = Get-Content $ledger -Raw
if ($ledgerText -notmatch 'active-run:\s*true') { exit 0 }

# Pull the pinned/iter/baseline header lines straight from the durable source.
$header = ($ledgerText -split "`n" |
    Where-Object { $_ -match '^(pinned|iter|baseline|runner):' }) -join '; '
if (-not $header) { exit 0 }

$context = "refactor-loop pinned constraints (re-asserted from .refactor-loop-ledger.md, the durable source): $header. These hold for every iteration regardless of context compaction."

$out = @{
    hookSpecificOutput = @{
        hookEventName     = 'UserPromptSubmit'
        additionalContext = $context
    }
}
$out | ConvertTo-Json -Depth 4
exit 0
