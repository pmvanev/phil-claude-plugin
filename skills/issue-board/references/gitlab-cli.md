# `glab` traps and self-hosted instances

Part of the `issue-board` skill. Read it before asking any `glab` command for JSON, reporting a `glab` error, reading a GitLab schema, or connecting to a self-hosted instance, and on any certificate error from either CLI. Its `SKILL.md` governs this file too.

## Self-hosted certificates

Two failure modes look alike and are not:

- **Unknown certificate authority** — import the CA into the OS trust store. `glab` and `gh` are Go
  binaries and read it. This is the fix:
  `sudo cp ca.pem /usr/local/share/ca-certificates/gitlab.crt && sudo update-ca-certificates`
- **Expired certificate** — no CA import helps. Renew it. There is no safe workaround.

Disabling verification is not a fallback an agent may choose. It exposes an `api`-scope token to
anyone on the network path, and a private-IP instance on a shared or home network is exactly where
that matters. If the developer decides to accept that risk, it is scoped to the single host
(`glab config set skip_tls_verify true --host <host>` — confirm the flag against your `glab`
version), it is temporary, and it must be stated out loud in the transcript every time it is used.

An expired certificate is a defect to fix, not a setting to work around.

## `glab`'s JSON flag differs per subcommand — check before you type it

**There is no blanket rule; check each subcommand.**

| Subcommand | JSON flag | What the other flag does there |
|---|---|---|
| `glab issue list` | **`-O` / `--output`** `json` | `-F` is `--output-format`, taking `details\|ids\|urls` |
| `glab repo view` | **`-F` / `--output`** `json` | `-O` **does not exist** |
| `glab api` | **none** — prints JSON natively | `-O` is **rejected**: `Unknown shorthand flag: 'O' in -O` |

```sh
glab issue list -R <group/project> --output json --per-page 100   # correct
glab issue list -R <group/project> -F json                       # silently returns a table
glab repo view <group/project> -F json                           # correct — -O is not a flag here
glab api projects/<url-encoded-path>                             # correct — no output flag at all
```

**On `issue list`, `-F json` does not error**: it returns the human-readable table. A caller that
parses the result finds no JSON and concludes the issues have no bodies, or that the list is empty.
That is the characteristic shape of every trap in this skill — a wrong guess that reports success.

**Verify a flag against `glab <subcommand> --help`, never from memory**: a flag verified on one
subcommand is evidence about that subcommand only. Wound: a blanket "`-O` everywhere" rule stood here
until 2026-08-17, right about one subcommand of three.

**Read past `glab`'s first error line.** It prints a bare `ERROR` banner before the real message, so a
caller that reports only the first line hides the defect behind an uninformative refusal.

## `glab api graphql` answers introspection with the whole schema

This skill sends readers to live schemas to confirm mutation signatures. On `glab` 1.112.0, that
route has a trap: **any query containing `__type` or `__schema` is discarded and answered with a full
schema dump** — 7.4 MB against an 18.9.1-ee instance. The response is valid JSON with a `data` key,
so it looks like a success; only `data.__type` is missing, and a naive parse raises a `KeyError`
rather than reporting what happened.

Verified on 1.112.0 — the discriminator is introspection, not syntax:

| Query | Result |
|---|---|
| `--raw-field query='{currentUser{username}}'` | correct response |
| `--raw-field query='query{currentUser{username}}'` | correct response |
| `--raw-field query='{__type(name:"Issue"){name}}'` | full schema dump |
| `--raw-field query='query{__type(name:"Issue"){name}}'` | full schema dump |
| `--raw-field query='query Foo{__type(name:"Issue"){name}}'` | full schema dump |

Ordinary queries pass through untouched, so this affects schema reading only. Two neighboring forms
fail differently and are not workarounds: `--input <file>` with a `{"query": "..."}` body arrives as
an empty document (`Unexpected end of document`), and `-f query=@<file>` sends the literal string
`@<file>` rather than reading it.

**Capture the dump once and query it locally** — `jq`, or a few lines of Python over
`data.__schema.types` — rather than fighting the flag. It contains every type, so one dump answers
every later question. Write it to a scratch path, never into the repository: it is megabytes of
generated content that dates the moment the instance is upgraded. Going around `glab` with `curl`
needs the instance's CA and its own token handling, and on an IP-addressed instance the certificate
may carry no matching SAN.
