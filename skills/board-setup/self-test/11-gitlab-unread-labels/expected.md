# Expected — BS-SELFTEST-11

`REFUSED`, naming the labels endpoint and its 401.

## What must happen

Nothing is written. The refusal names which call failed and why. The seven facts that *did* read are
reported to the human but do not become a block — a partial block reads exactly like a complete one.

## What must NOT happen

**No empty label set.** `{"labels": [], "count": 0}` is the single most misleading value this fact can
carry: on GitLab the `status::` label set *is* the board, so it states the project has no columns. A
value the forge would not return carries provenance `unread` and never enters the markers at all.

**No retry of the 401.** A connectivity failure is retried because a single timeout is usually the
network; an auth failure is not flaky, and retrying it three times only delays the real answer.

## Why this fixture exists

It is a defect this adapter actually produced. The first real run against `gitlab-org/gitlab-runner`
rendered `count: 0`, because `projects/<id>` reads unauthenticated while `projects/<id>/labels` does
not — so the failure was partial, and a partial failure is the kind that renders as a plausible value.

It also carries the `glab` flag correction: `glab api` takes **no** output flag and rejects `-O`,
`glab repo view` uses `-F`, and `glab issue list` uses `-O`. `phil:issue-board`'s blanket rule holds
for one of the three. That defect surfaced only after a refusal message was made informative — the
first version reported `failed: ERROR`, which hid it completely.
