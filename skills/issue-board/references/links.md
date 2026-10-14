# Linking from an issue body

Part of the `issue-board` skill. Read it before writing a link into an issue body. Its `SKILL.md` governs this file too.

## Link what the forge cannot resolve

An issue is read on its own page, away from the repo and away from you. Every reference a reader
might need to follow — a file, an ADR, a sibling issue — should be traversable by clicking. Two
rules, and they pull in opposite directions.

**Do not wrap what the forge already autolinks.** A bare `#12` becomes a live reference carrying the
issue's title and state — on GitHub, as a hovercard on the rendered link. `[#12](https://…/issues/12)`
renders as an ordinary link with none of that, and adds a URL to maintain. Leave these bare:

| | Autolinked without markdown |
|---|---|
| Both | `#12`, `@user`, commit SHAs |
| GitHub also | `owner/repo#12` |
| GitLab also | `group/project#12`, `!34` (MR), `%2` (milestone), `~label` |

A forge autolinks an issue reference **only when the issue exists**, which makes a read-back a
free wrong-number check — verified on GitHub (`#3` renders an href, `#999` stays plain text), and
on GitLab only in the negative direction, where a reference to a non-existent issue stayed plain.
It works only against *rendered* output. `gh issue view --json body` returns
the raw markdown, where `#12` is literal text whether or not it resolves, so checking there proves
nothing either way. Render it:

```sh
gh api -X POST /markdown -f mode=gfm -f context=<owner>/<repo> \
  -f text="$(gh issue view 12 -R <owner>/<repo> --json body -q .body)"
# GitLab: POST /api/v4/markdown with gfm=true and project=<group/project>
```

Plain text means the number is wrong **or** you cannot read the target — a confidential issue or a
private project renders identically. GitHub shares one number space between issues and pull
requests, so `#12` may resolve to a PR.

**Write an absolute URL for everything else.** Relative paths are the trap, because the two forges
disagree and both render a link either way:

| `[adr](docs/adr/016.md)` in an issue body | Result |
|---|---|
| GitLab | expands to `<host>/<project>/-/blob/<default-branch>/docs/adr/016.md` |
| GitHub | emitted verbatim, resolved against the *issue* URL → **404** |

Verified by rendering the same body through both forges' markdown APIs (`POST /markdown`). A
leading slash does not save it: GitLab resolves `/docs/…` identically, GitHub emits it verbatim and
it resolves to `github.com/docs/…`. Absolute URLs work on both — write those and the question never
comes up.

- **Docs and ADRs** — link at the default branch, so the reader gets current content:
  `https://<host>/<owner>/<repo>/blob/<default-branch>/docs/adr/ADR-016.md` on GitHub,
  `https://<host>/<project>/-/blob/<default-branch>/…` on GitLab. Note the `/-/` — GitLab needs it,
  GitHub has no such segment.
- **A specific line of code** — use a commit-SHA permalink, never a branch. A line anchor against a
  moving branch drifts onto unrelated code and stays plausible while doing it. Anchor syntax
  differs: GitHub `#L40-L52`, GitLab `#L40-52` *(GitLab form unverified — confirm by clicking a line
  number on any file in your instance; GitLab writes the anchor into the address bar)*.
- **Confirm the path is pushed** before linking it. A file that exists only in your working tree
  produces a link that renders correctly, passes your read-back, and 404s for every other reader.
  Resolve it against the branch you are linking, not your checkout:
  `git ls-tree origin/<default-branch> -- <path>` prints nothing if the file is not there.

On GitHub only, a repository can map a prefix to a URL template, so every bare `ADR-016` becomes a
link — including ones a human types, with no markdown:

```sh
gh api --method POST repos/<owner>/<repo>/autolinks \
  -f key_prefix='ADR-' -f url_template='https://…/docs/adr/ADR-<num>.md'
```

The same path without `--method POST` lists what is already configured. It needs admin, is
configured per repository, and has no GitLab equivalent, so treat it as a bonus on top of writing
real links, never as the mechanism you rely on.
