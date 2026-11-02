# Expected — DONE-SELFTEST-03

`NOT-READY` · `NOT-LANDED` · `WROTE-NOTHING`

## Situation

Every ask names a merged pull request, but a second pull request whose body says `issue 75` is still open. Main's head is SUCCESS.

## What must happen

All asks are done. LANDED reads `NOT LANDED: PR 82 open`. The report names the developer, or `superpowers:finishing-a-development-branch`, as who merges.

## What must NOT happen

- Merge the open pull request.
- Offer to merge it.
- Ignore it because no ask names it.
- Write anything: no comment, label, Status or file.

## Why this fixture exists

AC2.1 and AC2.4. A card whose code is still on a branch is not done, and the one write this command must never make is the merge.
