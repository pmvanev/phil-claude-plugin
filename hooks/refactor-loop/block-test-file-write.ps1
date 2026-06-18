# Guard G2 — test-file write-block (PreToolUse on Edit/Write)
#
# Blocks any Edit/Write whose target path matches a test-file glob, but ONLY while a
# refactor-loop run is active (the .refactor-loop-ledger.md sentinel with active-run: true
# exists in the project root). Outside an active run it is a no-op, so it never traps
# unrelated editing.
#
# Protocol: reads the hook payload as JSON on stdin; to block, prints a JSON decision and
# exits 0. Test-path globs match architecture.md s3.4; a project may override them via a
# CLAUDE.md "test runner" / test-path key (read here if present).

$ErrorActionPreference = 'Stop'

try {
    $raw = [Console]::In.ReadToEnd()
    $payload = $raw | ConvertFrom-Json
} catch {
    exit 0  # malformed payload: do not block
}

$cwd = if ($payload.cwd) { $payload.cwd } else { (Get-Location).Path }
$ledger = Join-Path $cwd '.refactor-loop-ledger.md'

# Sentinel gate: only enforce during an active refactor-loop run.
if (-not (Test-Path $ledger)) { exit 0 }
$ledgerText = Get-Content $ledger -Raw
if ($ledgerText -notmatch 'active-run:\s*true') { exit 0 }

$toolInput = $payload.tool_input
$path = if ($toolInput.file_path) { $toolInput.file_path } else { $toolInput.path }
if (-not $path) { exit 0 }

$leaf = Split-Path $path -Leaf
$norm = ($path -replace '\\', '/')

# Default test-path patterns (architecture.md s3.4). Override list lives per-project.
$patterns = @(
    '/tests?/', '/spec/', '/__tests__/',
    '_test\.', '\.test\.', '\.spec\.',
    '^test_.*\.py$', 'conftest\.py$'
)

$isTestPath = $false
foreach ($p in $patterns) {
    if ($norm -match $p -or $leaf -match $p) { $isTestPath = $true; break }
}

if ($isTestPath) {
    $decision = @{
        hookSpecificOutput = @{
            hookEventName      = 'PreToolUse'
            permissionDecision = 'deny'
            permissionDecisionReason =
                "refactor-loop guard G2: writes to test files are blocked during an active run ($leaf). The proposer never edits the oracle."
        }
    }
    $decision | ConvertTo-Json -Depth 6
    exit 0
}

exit 0
