# Rolling back a bad deploy

When a deploy raises the error rate above the alert threshold, roll it back with
`kubectl rollout undo deployment/api` rather than pushing a fix forward, because a rollback restores
a version that has already served traffic while a fix forward ships code that nobody has run in
production, and the on-call engineer is the only person awake to judge it.

The runbook's first line says "roll back first, debug second", and the readiness probe, the canary
weight and the error budget all assume you follow it, so a fix forward during an incident needs the
incident commander's approval and a note in the incident channel saying why.
