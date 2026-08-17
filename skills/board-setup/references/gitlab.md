# GitLab — the calls, and the rule that was wrong

`SKILL.md` states the shape guarantee and the two never-defaults. This file records the call-level
detail and the fold-back, because one of the constants involved was wrong in this plugin's own skill.

## The JSON flag differs per subcommand

`phil:issue-board` records a blanket rule: *"glab's JSON flag is `-O`; `-F` fails silently."*
**It holds for exactly one of the three calls this adapter makes.**

Discovered 2026-08-17 when `glab api projects/… -O json` failed with
`Unknown shorthand flag: 'O' in -O`, then confirmed against `glab --help`:

| Call | JSON flag | What the other flag means there |
|---|---|---|
| `glab api` | **none** — prints JSON natively | `-O` is rejected outright |
| `glab repo view` | **`-F` / `--output`** (`text`, `json`) | `-O` does not exist |
| `glab issue list` | **`-O` / `--output`** (`text`, `json`) | `-F` is `--output-format`, taking `details` / `ids` / `urls` |

So on `issue list` the recorded rule is right; on `repo view` it is exactly inverted; on `api` neither
flag applies. **This is the remembered-constant failure the whole feature exists to prevent, found
inside the skill this feature is a companion to.**

It surfaced only because a refusal message was improved. The first version of `run()` reported
`failed: ERROR` — `glab` prints a bare `ERROR` banner before the real message, and taking the first
line of stderr got the banner. Once the extraction skipped non-informative lines, the real cause
appeared immediately. **A refusal whose reason is uninformative hides the defect that caused it.**

## Unread is not empty, and on GitLab it matters more

`projects/<id>` reads unauthenticated. `projects/<id>/labels` returns **401**. The first real run
against `gitlab-org/gitlab-runner` therefore rendered:

```
column-families: {"mechanism": "status:: labels", "labels": [], "count": 0}
```

On GitHub an empty option list would be odd. On GitLab it is catastrophic: **the `status::` label set
*is* the board**, so `count: 0` states that the project has no columns. A reader would conclude the
board does not exist.

`labels=None` now means unread and renders with `provenance: "unread"`, which `render-block.py`
refuses to write inside the markers at all — `unread` is neither a fact nor a guess, and writing it as
either launders a failed read into content.

## Tier, and why a Free-shaped block matters

Scoped labels and real `blocks` links are Premium. Writing a scoped-label convention on a Free
instance documents a workflow the reader cannot perform, so the tier fact carries the *consequence*
rather than the tier alone: on Free, board state is a `status::` label swapped by hand with
`glab issue update --unlabel old --label new`.

## What remains unverified

- **AC1/AC2 end-to-end** — a real GitLab region diffed against a real GitHub one. Blocked by the 401
  on labels; the *shape* equality is verified mechanically (identical `template_field` sets) but the
  rendered-region diff has not been run.
- **AC5** — a real self-hosted connection failure. The retry logic is unit-tested, including that a
  401 is **not** retried, but no unreachable instance was available.
