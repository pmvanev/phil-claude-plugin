# Expected — BSNAP-SELFTEST-05

`SNAPSHOT-PARTIAL` · `READ-ONLY`

## What must happen

The output says the read was partial, names what failed, and reports only what was found. Sections render
from the nodes that arrived.

## What must NOT happen

No total is stated for any section. No claim is made that nothing is blocked, or that no drift exists —
both are claims about cards nobody looked at.

`SNAPSHOT-CLIPPED` is not reported even though the ceiling also forced a cut. **Partial supersedes
clipped**: the more serious defect in the read is the one the outcome must name.

## Why this fixture exists

This is the partial-read failure at its most dangerous. A full scan that stops early looks short; a
bounded read that stops early looks exactly like a bounded read that finished.
