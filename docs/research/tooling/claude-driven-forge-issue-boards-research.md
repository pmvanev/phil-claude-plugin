# Research: Can Claude Code Drive GitLab/GitHub Issue Boards as a Kanban Without Custom Code?

**Date**: 2026-08-10 | **Researcher**: nw-researcher (Nova) | **Confidence**: Medium-High | **Sources**: 25 cited (4 primary local-filesystem observations, 21 web) | **Avg reputation**: 0.89

**Verdict in one line**: **Buy.** GitHub is already installed and covers boards; GitLab needs
`zereight/gitlab-mcp` (stdio) or `glab` — **not** the official GitLab MCP server, which is
disqualified by the expired cert. The remaining gap is a skill file, not code.

---

## ⚠ FINDINGS SUPERSEDED BY EXECUTION — 2026-08-10, same day

**Read this before the Executive Summary.** The "buy" verdict holds and got stronger. The
*recommended product* changed, one causal claim was falsified, and a tier assumption was wrong.

| This document says | Execution showed |
|---|---|
| Prefer `zereight/gitlab-mcp` (stdio) for GitLab | **Superseded by `glab`** (GitLab's official CLI, v1.112.0, released 2026-08-04). It has `skip_tls_verify` **per host** instead of process-wide `NODE_TLS_REJECT_UNAUTHORIZED=0`, native `glab issue board create/view`, and `glab issue update --label/--unlabel` for card moves. Installed and authed against `10.10.1.4`; listed real issues **first attempt**. The MCP was also proven working and remains a validated fallback |
| "Renew the cert — it alone would promote the official GitLab MCP from ❌ to contender" | **Falsified.** Authenticated, `https://10.10.1.4/api/v4/mcp` returns **404** on 18.9.1-ee — GET and POST, `PRIVATE-TOKEN` and `Bearer`. The cert was never the gate for that path; the unserved endpoint is. Cert renewal is still worth doing, but it is not the unlock claimed here |
| G2 — unverified whether a self-managed instance exposes `/api/v4/mcp` | **Resolved: it does not serve.** Note an unauthenticated probe returns `401` (GitLab's blanket `/api/v4/*` auth gate) which is easy to misread as "route exists" — it is not evidence either way |
| Instance assumed **Free** self-managed | **Wrong — it is Premium or higher.** `/api/v4/groups/basetwin/epics` returns `200 []`; Free returns 403. Version is `18.9.1-ee`, `"enterprise": true` |
| Dependencies must use prose "Blocked by" lines because `blocks`/`blocked_by` link types are Premium-gated | **Unnecessary on this instance.** Premium means real, enforced issue links. `gitlab_sync.py`'s prose workaround is now the *inferior* option for dependency modelling |
| The remaining gap is "a skill file" | **Not skill-shaped.** ~5 project-specific constants (scoped labels are the status mechanism; project `42`, board `13`; the link flaps; Premium link types; the Backlog.md/GitLab partition). These belong in the project's `CLAUDE.md`, not a packaged cross-project skill |
| GitHub path | **Confirmed and exercised** — but via `gh` 2.97.0, not the MCP. Four issues created and independently verified on `pmvanev/phil-claude-plugin`. Note GitHub has **no scoped-label mutual exclusion**, so a board means a Projects v2 **Status field**, and `gh auth login`'s default scopes omit `project` (`gh auth refresh -s project` adds it) |

**Verified by execution:** TLS-off reaches `10.10.1.4` at the Node layer (`401` unauth → `200`
with PAT); without it, `CERT_HAS_EXPIRED`. `@zereight/mcp-gitlab` v2.1.46 initialized over stdio,
63 tools, returned real issues. `glab` 1.112.0 listed issues with `status::` labels intact. `gh`
2.97.0 created issues #1–#4.

**The constraint that turned out to bind:** not tooling — **the network.** Two of three MCP
attempts failed with `EHOSTUNREACH`, plus one earlier failure. `gitlab_sync.py` survives this via
retry-with-backoff; a CLI or MCP call has no such wrapper, so multi-step board operations will
partially fail mid-sequence. Small samples, but retry is mandatory and fixing that box outranks
any tooling choice here.

**Note on distribution channels:** `apt` carries `gh` 2.46.0 and `glab` 1.53.0 against upstream
2.97.0 and 1.112.0. Install from upstream releases into `~/.local/bin` — no sudo required.

**Decision taken:** two CLIs (`gh`, `glab`), no MCP server, no plugin, no skill, no sync layer.
Partition by scope instead: markdown/Backlog.md owns in-flight work, the forge owns the
outward-facing tier, joined by a single `--ref` to the issue number.

---

> **Scope note.** This is the *forge-issues layer*. The local-markdown-kanban decision
> (Backlog.md + `ysamlan.vscode-backlog-md`) is settled and is NOT re-litigated here. See
> `docs/research/tooling/local-markdown-kanban-backlog-tooling-research.md`.

---

## Executive Summary

**Yes — buy, don't build. But the buy-vs-build line is drawn by the *role choice*, not the tooling.**

**Role A (forge as system of record) can be bought; Role B (Backlog.md as SoR, forge as projection)
must be built.** No markdown→forge projector or drift detector exists for either forge (B1), so
`gitlab_sync.py` *is* the state of the art for Role B. **Choose Role A.**

For **GitHub**, Role A is ~100% bought and **already installed**: a `github` MCP server sits in *two*
of the user's marketplaces (`claude-plugins-official/external_plugins/github` and
`knowledge-work-plugins/engineering`), both pointing at GitHub's hosted server. It covers
`issue_write` **and** `projects_write → update_project_item`, so it moves cards across Projects v2
columns by field *name* — the separate-GraphQL-API problem is hidden behind one tool namespace.

For **GitLab**, ~85% bought — but the obvious answer fails. GitLab ships an MCP server *inside
GitLab* at `/api/v4/mcp`, and a `gitlab` plugin for it is already present locally. It is disqualified
by **C1 and C3**: it is `http` transport, so Claude Code terminates TLS itself, and an **expired**
cert cannot be fixed by importing a CA — only by process-wide `NODE_TLS_REJECT_UNAUTHORIZED=0`, which
would unverify Anthropic's own API too. It is also OAuth-DCR-only and needs GitLab Duo enabled. Use
**`zereight/gitlab-mcp`** instead: PAT auth, `GITLAB_API_URL`, and **stdio** transport, so TLS-off
stays scoped to one child process. Fallback: **`glab`**, whose per-host
`glab config set skip_tls_verify true` is the only *documented* answer to C1 anywhere.

**Was `gitlab_sync.py` necessary? Yes** — every alternative failed a constraint it had to meet. But it
is now **spent capital, not an asset**: its recurring function (card moves) is fully replaced, and only
its one-time bulk-seed-with-IID-backfill is unmatched. **The minimal remaining gap is one skill file
of six facts, plus one five-minute TLS test — knowledge, not code.**

**Confidence: Medium-High.** What would change it: (1) **G4** — whether `NODE_TLS_REJECT_UNAUTHORIZED=0`
in a stdio MCP `env` block actually reaches `10.10.1.4`; (2) **G2/G3** — whether a Free self-managed
instance exposes `/api/v4/mcp` at all and whether its tools can *write* labels.

## Research Methodology

**Search Strategy**: three tracks. (a) **Local filesystem first**, and it produced the two highest-value
findings of the pass — the `github` MCP server's identity (L1) and the previously-unmentioned `gitlab`
plugin pointing at GitLab's own built-in endpoint (L2). Glob + Grep over
`~/.claude/plugins/marketplaces/` and direct reads of every `.mcp.json` and `plugin.json` found.
(b) **Official vendor documentation** — `docs.gitlab.com`, `cli.github.com/manual`,
`code.claude.com/docs`. (c) **Vendor issue trackers as primary evidence of failure modes** — this was
the decisive methodological choice: product pages never document what does not work, so C1 was
resolved by reading `anthropics/claude-code` issues rather than feature lists.

**Source Selection**: official vendor docs (reputation 1.0) for capability and configuration;
project repos on `github.com` (0.8) authoritative for *claims* only, never for whether a thing works;
issue trackers (0.8) authoritative for the existence of a report and for maintainer disposition
("closed as not planned"); the GitHub releases page authoritative for version/date. Per orchestration
ruling, registries were used for existence/version/date claims only.

**Quality Standards**: 3 sources/claim ideal, 2 acceptable, 1 authoritative minimum. Every matrix cell
that was not verified is `?` with a named resolving test. Interpretations are labelled
`[Interpretation, flagged]` and separated from sourced facts.

**Known methodological limitation — and it is the same one as the prior pass**: **nothing was installed,
configured, or run, and no authenticated call was made to `10.10.1.4`** (per the brief's explicit
prohibition). Every capability claim is documentary. The C1 verdicts are therefore *reasoned from
transport architecture and bug reports*, not measured. **Gap G4 is the test that converts the central
recommendation from inference to fact.**

## Constraints Under Test

| # | Constraint |
|---|---|
| C1 | Self-hosted GitLab at private IP `https://10.10.1.4`, **expired self-signed cert**, flaky link. Needs custom base URL AND custom CA or TLS-verify-off. |
| C2 | Must move a card between columns, not just CRUD issues. GitLab = scoped labels / board lists. GitHub Projects v2 = a project *field* via a **separate GraphQL API**. |
| C3 | One `api`-scope token, ideally project-scoped. |
| C4 | Eventually BOTH forges. One tool covering both is preferred. |
| C5 | Agent-drivable without hand-rolled API calls per turn. |
| C6 | `gh` and `glab` NOT installed. CLI answers carry an install cost. |

**Roles**
- **Role A** — forge is system of record; Claude drives issues/boards directly.
- **Role B** — Backlog.md is system of record; forge is one-way projection + drift detection.

## Compliance Matrix

Legend: ✅ satisfied · ⚠️ partial / inferred-not-documented · ❌ fails · `?` **unverified — never a guess**

| Candidate | C1 self-hosted + expired cert | C2 move a card | C3 credential | C4 both forges | C5 agent-drivable | C6 install cost | Last release | **Role fit** |
|---|---|---|---|---|---|---|---|---|
| **GitHub MCP — hosted** (`api.githubcopilot.com/mcp/`) — **already in 2 of the user's marketplaces** | n/a (github.com) · ❌ for GHES ("does not support remote server hosting") | **✅ full** — `update_project_item` by field name | ⚠️ PAT `repo,read:org` + `project`; **owner-scoped, not repo-scoped** | ❌ GitHub only | ✅ typed MCP tools | ✅ **none** — `/plugin install github@claude-plugins-official` | `?` G6 | **Role A ✅ (GitHub)** |
| **GitHub MCP — local** (Docker/binary) | n/a · ✅ `GITHUB_HOST` for GHES | ✅ full | ⚠️ same | ❌ | ✅ | ⚠️ Docker/Go | `?` G6 | Role A ✅, only if GHES |
| **Official GitLab MCP** (`https://HOST/api/v4/mcp`) — **plugin already present** | **❌/⚠️** `http` transport → TLS-off must be **process-wide**; CA import cannot fix an **expired** cert; MCP-OAuth+custom-CA has an open bug (#55760) | **`?`** — write/label tools not documented (G3) | **❌** OAuth 2.0 DCR only; **no PAT method documented**; **requires GitLab Duo "Always on"** + beta features (G2) | ❌ GitLab only | ✅ typed MCP tools | ✅ none (one-line `.mcp.json`) | Beta since GitLab **18.6** | **Neither — blocked on C1+C3** |
| **`zereight/gitlab-mcp`** (stdio, 1.9k★, MIT) | **⚠️ best MCP option** — `GITLAB_API_URL` ✅; TLS-off **undocumented but Node-honoured and scoped to the child process** (G4) | ⚠️ **moves ✅** via label+issue-update (GitLab = label boards); **lists ❌** | **✅ `GITLAB_PERSONAL_ACCESS_TOKEN`** — project-scoped token works | ❌ GitLab only | ✅ 217 tools claimed | ✅ `npx`/Docker | v2.1.45, date `?` G5 | **Role A ✅ (GitLab), pending G4** |
| **`mcpland/gitlab-mcp`** | `?` | `?` | `?` | ❌ | `?` | `?` | `?` | `?` — G7 |
| **`glab`** (official GitLab CLI) | **✅ documented** — `GITLAB_HOST`/`GL_HOST` + **`glab config set skip_tls_verify true --host …`** (**per-host**, narrower blast radius than any MCP option) | ⚠️ moves ✅ (`issue update --label/--unlabel`); **no board commands** | ✅ `GITLAB_TOKEN` | ❌ GitLab only | ⚠️ shell commands, needs a documented vocabulary | **❌ not installed** — apt/tarball | active (`gitlab-org/cli`) | **Role A ✅ (GitLab) — the C1 fallback** |
| **`gh`** (official GitHub CLI) | n/a | **✅ full** — `gh project item-edit --field "Status" --value "In Progress"` | ⚠️ needs `project` scope; owner-scoped | ❌ GitHub only | ⚠️ shell commands | **❌ not installed** (Linux side; Windows `gh.exe` on PATH — G1) | GA, active | Role A ✅ (GitHub), redundant vs MCP |
| **`git-bug`** (10k★, GPLv3) | **❌/?** `--base-url` ✅; **no TLS option found**; OS trust store fixes self-signed but **not expired** | **❌ no column model**; scoped-label round-trip doubtful (G10) | ✅ token | **✅ the only "both forges" candidate** | ✅ CLI | ⚠️ Go binary | **❌ v0.10.1 — 2025-05-19, ~14.7 months → FLAGGED** | **Neither** — 3rd store + bidirectional = the architecture the user rejected |
| **`dspinellis/git-issue`** | `?` | ❌ no column model | `?` | ⚠️ | ✅ CLI | ⚠️ | `?` G12 | **Neither** |
| **Backlog.md → forge bridge** | — | — | — | — | — | — | — | **DOES NOT EXIST (B1)** — so **Role B is unbuyable** |
| **`gitlab_sync.py`** (incumbent) | **✅ the only VERIFIED pass** — `ssl.CERT_NONE` **scoped to one script** + connection-retry with 4xx/5xx exclusion | **✅ full** — labels *and* board-list creation (phase 5) | ✅ one `api` PAT | ❌ GitLab only | ⚠️ one-shot script, not per-turn tools | ✅ stdlib only | n/a | **Role B ✅ — and it is the entire state of the art for Role B** |

**Column readings — the four things this matrix says:**

1. **C4 is unsatisfiable by anything acceptable.** The *only* candidate covering both forges is
   `git-bug`, and it fails on maintenance, boards, C1 and architecture. **Accept two integrations.**
   Since both are configuration rather than code, the cost of two is near-zero.
2. **C1 inverts the ranking.** The *official* GitLab MCP server — which looks like the perfect
   "already exists" answer — is the **worst** C1 performer, because `http` transport puts Anthropic's
   own API inside the TLS-off blast radius. The scrappy community stdio server and the CLI both beat
   it. **This is the silent disqualifier the brief predicted, and it disqualified the favourite.**
3. **C2 is easier than feared on GitHub and easier than feared on GitLab, for opposite reasons.**
   GitHub MCP/`gh` genuinely expose Projects v2 field writes; GitLab needs no board API at all
   because its boards are label views.
4. **The `?` cells cluster on exactly one candidate.** Four of the six unverified cells belong to the
   official GitLab MCP server. That is where the remaining research value is — and **Gap G2** (does a
   Free self-managed instance without a Duo entitlement expose `/api/v4/mcp` at all?) decides it.

## Findings

### Part 1 — Local environment: what is already installed/available

#### L1. The `github` MCP server in the user's marketplaces is the **hosted GitHub-Copilot endpoint**, not a local build

**Evidence** — two files, both primary observations on this machine:

`/home/philvanevery/.claude/plugins/marketplaces/claude-plugins-official/external_plugins/github/.mcp.json`:
```json
{ "github": { "type": "http", "url": "https://api.githubcopilot.com/mcp/",
    "headers": { "Authorization": "Bearer ${GITHUB_PERSONAL_ACCESS_TOKEN}" } } }
```

`/home/philvanevery/.claude/plugins/marketplaces/knowledge-work-plugins/engineering/.mcp.json` — the file
the brief describes, containing `slack, linear, asana, atlassian, notion, github, pagerduty, datadog`
(plus empty-URL `google calendar` and `gmail` stubs). Its `github` entry is the **same URL**, minus the
`Authorization` header (so it relies on OAuth rather than a PAT).

The sibling `plugin.json` self-describes as: *"Official GitHub MCP server for repository management.
Create issues, manage pull requests, review code, search repositories…"*, author `GitHub`.

**Source**: local filesystem, accessed 2026-08-10. **Primary observation. Confidence: High.**

**Answer to the brief's highest-value local question**: the plugin is **`github` in the
`claude-plugins-official` marketplace** (`external_plugins/github/`), and the *same server* is
re-declared by **`engineering` in the `knowledge-work-plugins` marketplace**. Both are thin
`.mcp.json` shims pointing at GitHub's **remote hosted** MCP server. Neither ships code, so neither
can be reconfigured for a custom host — see **C1** below. That is the decisive consequence.

#### L2. A **`gitlab` plugin is also already present** — and it points at GitLab's *own* built-in MCP endpoint

`/home/philvanevery/.claude/plugins/marketplaces/claude-plugins-official/external_plugins/gitlab/.mcp.json`:
```json
{ "gitlab": { "type": "http", "url": "https://gitlab.com/api/v4/mcp" } }
```
`plugin.json`: *"GitLab DevOps platform integration. Manage repositories, merge requests, CI/CD
pipelines, issues, and wikis."*, author `GitLab`.

**Source**: local filesystem, accessed 2026-08-10. **Primary observation. Confidence: High.**

**This is the most important structural finding in the whole research pass.** The URL is not a
third-party service — it is a path *on the GitLab instance itself* (`/api/v4/mcp`). GitLab ships an
MCP server **inside GitLab**. Therefore a self-hosted instance at `10.10.1.4` would expose it at
`https://10.10.1.4/api/v4/mcp`, and adopting it is a one-line `.mcp.json` edit, not an install.
The prerequisites are where it gets hard (Finding M2).

#### L3. Neither `gh` nor `glab` is on this machine — confirmed independently of the brief

The brief states this as verified. Corroborating documentary evidence from the *prior* research pass:
that document's C10 recorded `gh` as present at `/mnt/c/Program Files/GitHub CLI/` **via
`~/.claude/settings.json` PATH entry** — i.e. a Windows-side install visible to WSL's PATH, not a
Linux binary. **Treat the brief's "not installed" as authoritative for the WSL/Ubuntu userland**;
the Windows `gh.exe` may still be invocable but is not a supported posture for a Linux-side agent
workflow (path translation, credential store location). **Confidence: Medium** — this is a
reconciliation of two sources, not a fresh test. See Gap G1.

#### L4. Local MCP-server reference docs do not help

`claude-plugins-official/plugins/claude-code-setup/skills/claude-automation-recommender/references/mcp-servers.md`
lists "GitLab MCP — **Best for**: GitLab-hosted repositories" as a bare one-liner with no table, no
tool list, and no configuration guidance, while GitHub MCP gets a full table. No self-hosted or TLS
guidance anywhere in the file. **Source**: local, accessed 2026-08-10. **Primary. Confidence: High.**
**Analysis**: the *recommender* content treats GitLab as an afterthought. This is a signal about
ecosystem maturity asymmetry, not a capability finding.

### Part 2 — MCP servers

#### M1. The official GitHub MCP server — **issues AND Projects v2 fields**, but the *hosted* build cannot do GHES

**Evidence** (`github/github-mcp-server`, accessed 2026-08-10; 32.1k stars, MIT, 1,031 commits on main):

| Toolset | Tools / methods |
|---|---|
| Issues | `issue_read` (details, comments, sub-issues, **labels**), `issue_write` (create/update), `list_issues`, `search_issues`, `sub_issue_write` |
| **Projects (v2)** | `projects_list` → `list_project_items`, **`list_project_fields`**; `projects_write` → **`update_project_item`** and field-value management, addressed as `{"id": 123, "value": …}` or **`{"name": "Status", "value": …}`** |

**C2 for GitHub is therefore ✅ — and this is the most important capability finding on the GitHub
side.** `update_project_item` with `{"name": "Status", "value": "In Progress"}` **is** the
move-a-card-between-columns operation. Projects v2 is indeed a separate GraphQL API from the Issues
REST API, exactly as the brief warns — but the MCP server **hides that seam behind one tool
namespace**. The agent does not need to know that `issue_write` is REST and `projects_write` is
GraphQL. That is precisely the "buy, don't build" value.

**Deployment options and the C1/GHES trap:**

| Option | URL / image | GHES? |
|---|---|---|
| **Remote (hosted)** | `https://api.githubcopilot.com/mcp/` | **"GitHub Enterprise Server does not support remote server hosting."** Only GitHub Enterprise Cloud w/ data residency (`*.ghe.com`) |
| **Local** | Docker `ghcr.io/github/github-mcp-server`, or `go build` binary | ✅ via **`GITHUB_HOST`** (prefix with `https://`) |

Auth: OAuth (default on github.com, browser flow) **or** `GITHUB_PERSONAL_ACCESS_TOKEN` with minimum
`repo`, `read:packages`, `read:org`.

**Source**: [github/github-mcp-server](https://github.com/github/github-mcp-server) — Accessed
2026-08-10. Reputation **0.8** (industry leader / vendor repo; authoritative for its own claims).
Corroborated on the deployment-URL point by the two local `.mcp.json` files (Finding L1), which
independently confirm the hosted URL is the one the ecosystem ships. **Confidence: High** on tool
surface and hosting split.

**Assessment**: **C1 n/a** for public github.com (valid public cert, no private IP). C2 ✅. C3 ⚠️ —
needs a classic PAT with `repo`/`read:org`, i.e. **account-wide, not project-scoped**; fine-grained
PATs are not the documented minimum. C4 ❌ — GitHub only. C5 ✅. C6 n/a. **Last release version/date
not captured — Gap G6.**

**Note the asymmetry with the user's local install**: the plugin they already have wires the
**hosted** server. That is the right choice for github.com and the *wrong* one for any self-hosted
GitHub. Since the user's GitHub is presumably github.com, **this candidate is essentially free and
already installed.**

#### M4. Are there other GitLab MCP servers? Yes — `mcpland/gitlab-mcp`

Search surfaced [`mcpland/gitlab-mcp`](https://github.com/mcpland/gitlab-mcp), self-described as
*"A MCP server for GitLab with powerful, safe, policy-controlled access."* **Not verified in depth
(Gap G7)** — the "policy-controlled access" framing is interesting for a single-token setup but no
capability, TLS, or maintenance data was gathered. Named here so the search space is honest, not
recommended.

---

## The C1 Question, Answered Per Candidate

**This section contains the decisive finding of the research pass.** The brief predicted C1 would be
"the most common silent disqualifier". It is worse than that: C1 splits the candidates along a line
that has nothing to do with their GitLab features.

### C1.1 — The two failure modes are not the same, and only one has a clean fix

The cert at `10.10.1.4` is **self-signed AND expired** (`gitlab_sync.py` line 29 records
`notAfter Nov 2025`). These are *independent* TLS validation failures:

| Failure | Fix |
|---|---|
| Self-signed (untrusted issuer) | **`NODE_EXTRA_CA_CERTS=/path/ca.pem`** — documented and supported |
| **Expired (`notAfter` in the past)** | **No CA import fixes this.** Trusting the issuer does not make an expired certificate valid. The *only* remedy is disabling verification: `NODE_TLS_REJECT_UNAUTHORIZED=0` |

**Evidence for the supported variables**: Claude Code's official network-config page documents
`NODE_EXTRA_CA_CERTS=/path/to/ca-cert.pem` under "Custom CA certificates", plus
`CLAUDE_CODE_CERT_STORE` (`bundled` / `system`, default `bundled,system`), and — critically — lists
**`NODE_TLS_REJECT_UNAUTHORIZED`** among the variables ignored in cloud sessions, which confirms
Claude Code recognises it in local sessions.
**Source**: [Enterprise network configuration](https://code.claude.com/docs/en/network-config) —
Accessed 2026-08-10. Reputation **1.0** (official first-party). **Confidence: High.**

**Analysis (interpretation, flagged as such)**: the expired-cert half of the problem means the "good"
enterprise mechanism is unavailable to this user. They are forced onto the blunt instrument. **Which
blunt instrument, and how wide its blast radius is, then depends entirely on MCP transport type.**

### C1.2 — `http` transport vs `stdio` transport decides the blast radius

| Transport | Who terminates TLS to the forge | Where verify-off must be set | Blast radius |
|---|---|---|---|
| **`"type": "http"`** (official GitLab MCP; the `gitlab` plugin the user already has) | **Claude Code itself** | The Claude Code process | **All Claude Code TLS**, including `api.anthropic.com` |
| **`stdio`** (`zereight/gitlab-mcp` via `npx`/Docker) | The **child** MCP server process | That server's `env` block in `.mcp.json` | **Only that server's traffic** |

**Evidence that `http`-transport MCP + self-signed cert actually fails in Claude Code**:
anthropics/claude-code issue **#2899**, *"[BUG] Local MCP server will not trust self-signed certs"* —
an **HTTP/SSE** MCP server behind a locally-CA-signed cert fails with
`MCP server "…": HTTP Connection error: fetch failed / TypeError: fetch failed`, **even with the CA
trusted in both WSL 2 and Windows**. Reported from **Windows 11 / WSL 2** — the same platform class
as this user. Opened 2025-07-03. **Closed as not planned.** The only confirmed workaround is
`NODE_TLS_REJECT_UNAUTHORIZED=0 claude`, i.e. process-wide.
**Source**: [anthropics/claude-code#2899](https://github.com/anthropics/claude-code/issues/2899) —
Accessed 2026-08-10. Reputation **0.8** (vendor issue tracker; authoritative for the report, and
"closed as not planned" is an authoritative statement of maintainer intent).
**Confidence: High** that this failure mode is real and unresolved.

**Corroborating evidence — the runtime got *worse*, not better**: since **v2.1.113** Claude Code
ships as a **Bun-compiled native binary**, and Bun's global `fetch` uses **BoringSSL**, which does
not honour `NODE_EXTRA_CA_CERTS`. Independent traces: anthropics/claude-code issue **#55760**,
*"[BUG] Hosted MCP OAuth initiation ignores NODE_EXTRA_CA_CERTS on corporate MITM networks
(v2.1.113+)"*; issue **#22512**, *"NODE_EXTRA_CA_CERTS is not effective when set in
~/.claude/settings.json"*; and issue **#26897**, *"NODE_EXTRA_CA_CERTS Environment variable not
working"*.
**Confidence: Medium-High** — four independent issue reports converge, but this contradicts the
official docs (see **Conflicting Information**), and I did not fetch #55760/#22512/#26897 bodies.

**Note the second-order hit**: #55760 is specifically about **MCP OAuth initiation** failing on
custom-CA networks. The official GitLab MCP server is **OAuth-DCR-only** (Finding M2). So the
official GitLab MCP server needs, over a broken-TLS link, exactly the code path that has an open bug.

### C1.3 — Per-candidate C1 verdicts

| Candidate | Custom base URL | Custom CA | Verify-off | **C1 verdict** |
|---|---|---|---|---|
| **Official GitLab MCP** (`https://10.10.1.4/api/v4/mcp`, `http` transport) | ✅ one-line `.mcp.json` | ⚠️ Bun/BoringSSL bugs; and **irrelevant — cert is expired** | ⚠️ only process-wide `NODE_TLS_REJECT_UNAUTHORIZED=0` | **❌ / ⚠️ — fails as specified.** Achievable only by turning off TLS verification for the *entire* Claude Code process |
| **`zereight/gitlab-mcp`** (stdio) | ✅ `GITLAB_API_URL` | ⚠️ undocumented, Node honours `NODE_EXTRA_CA_CERTS` (inference) | ⚠️ undocumented, Node honours `NODE_TLS_REJECT_UNAUTHORIZED=0` (inference) | **⚠️ — best available.** Verify-off is **scoped to the child process**, so Anthropic API traffic stays verified. **Gap G4** is the one test that settles it |
| **GitHub MCP (hosted)** | ❌ github.com only | n/a | n/a | **n/a** (valid public cert) |
| **GitHub MCP (local Docker/binary)** | ✅ `GITHUB_HOST` | ? | ? | **n/a for github.com**; `?` for a hypothetical self-hosted GitHub |
| **`glab` CLI** | ✅ | ✅ | ✅ | **✅ — see Part 3** |
| **`gitlab_sync.py`** (the incumbent) | ✅ | n/a | ✅ `ssl.CERT_NONE`, **scoped to one script** | **✅ — the only candidate with a *verified* pass** |

**The uncomfortable conclusion**: the incumbent hand-built script is currently the **only** candidate
whose C1 compliance is proven by execution rather than inferred from documentation. Every MCP option
is `⚠️` or worse, and the *official* GitLab MCP server — the one that looks like the perfect
"already exists" answer — is the **worst** C1 performer of the three, because `http` transport puts
Anthropic's own API connection inside the blast radius.

### C1.4 — The constraint nobody's product page addresses: the flaky link

`gitlab_sync.py` carries a documented retry loop with exponential backoff (lines 68-98), and an
explicit design decision worth preserving: *"HTTP errors (4xx/5xx) are real answers and are never
retried — only connection-level failures are."* Its comment records the operational reality: *"The
link to this host flaps: a connect can fail and the next one succeed."*

**No MCP server or CLI examined documents connection-level retry semantics.** An MCP tool call that
hits a flapping link surfaces to the agent as a tool error, and the recovery strategy becomes
"whatever the agent decides to do next" — which is nondeterministic and, on a write operation,
potentially duplicating. **This is a genuine residual gap and it is not addressed by any candidate.
[Interpretation, not a sourced claim.]** See the Minimal Gap section.

#### M2. GitLab's built-in MCP server (`/api/v4/mcp`) — real, official, and gated behind **GitLab Duo**

**Evidence** (official docs, `docs.gitlab.com`, reputation High, accessed 2026-08-10):

| Attribute | Value |
|---|---|
| Endpoint (self-managed) | `https://<gitlab.example.com>/api/v4/mcp` |
| Offerings | GitLab.com, **GitLab Self-Managed**, GitLab Dedicated |
| Tiers | Free, Premium, Ultimate |
| Status | **Beta** (was Experimental in 18.3; promoted to Beta in **18.6**) |
| Feature flags | `mcp_server` + `oauth_dynamic_client_registration`, **removed at 18.6** — no flags needed on 18.6+ |
| **Prerequisite** | **GitLab Duo availability must be "Always on" or "On by default"**, AND beta/experimental features enabled at instance level for self-managed |
| Auth | **OAuth 2.0 Dynamic Client Registration**; pre-registered OAuth apps as an alternative. **No personal-access-token method documented.** |

**Source**: [GitLab MCP server](https://docs.gitlab.com/user/model_context_protocol/mcp_server/) —
Accessed 2026-08-10. Reputation **1.0** (official vendor documentation, authoritative).
**Confidence: High** for existence, endpoint, status, and prerequisites.

**Two hard consequences for this user, both adverse:**

1. **Auth is OAuth-only (C3 fails as specified).** The user has *one `api`-scope PAT*. The documented
   path is OAuth DCR, which needs a browser redirect against `https://10.10.1.4` and an instance
   willing to register dynamic clients. The user's credential does not fit the documented door.
   `gitlab_sync.py`'s `PRIVATE-TOKEN` header is exactly the mechanism the MCP server does *not*
   document.
2. **`GITLAB_DUO` must be on.** On a self-hosted instance this is an admin setting plus, in practice,
   a Duo entitlement. Whether a **Free self-managed** instance can actually set Duo to "Always on"
   and get a working `/api/v4/mcp` is **unverified — Gap G2**, and it is the single test that decides
   whether this candidate lives.

**Tool surface: not disclosed on this page.** The docs defer to a separate Tools page. Whether
issues can be *updated* (labels swapped) versus merely *read* is **unverified — Gap G3**. The page's
own capability language is read-leaning: *"Access project information. Retrieve issue and merge
request data."*

#### M3. `zereight/gitlab-mcp` — the community server, and it is the C3/C1 pragmatist's choice

**Evidence** (project repo, `github.com`, reputation 0.8, accessed 2026-08-10; README is
authoritative for *claims* only):

| Attribute | Value |
|---|---|
| Base URL | `GITLAB_API_URL` env var (e.g. `https://gitlab.com/api/v4`) → **custom host supported** |
| Auth | **`GITLAB_PERSONAL_ACCESS_TOKEN`** (PAT), plus OAuth2, CI `JOB-TOKEN`, bearer |
| Tool count | **217 tools** claimed |
| Coverage claimed | MRs, **issues**, code review, pipelines/CI, repos, branches/tags/releases, wiki, **labels**, **milestones**, projects, groups, work items, vulns, webhooks, variables, search, deployments, environments |
| **Boards** | **No dedicated board or board-list tools listed** |
| Stars | 1.9k |
| License | MIT |
| Latest version | 2.1.45 |
| TLS skip flag | **Not documented.** Only `MCP_DANGEROUSLY_ALLOW_INSECURE_ISSUER_URL=true`, and that is for *local HTTP dev*, not for skipping certificate validation |

**Source**: [zereight/gitlab-mcp](https://github.com/zereight/gitlab-mcp) — Accessed 2026-08-10.
**Confidence: High** that these are the claims; **Medium** that they work as claimed (single source,
self-described).

**Assessment against the constraints:**
- **C3 ✅** — PAT auth. This is the *only* GitLab MCP candidate that takes the credential the user
  actually has.
- **C1 ⚠️** — custom base URL ✅, but **no documented TLS-verification escape hatch**. It is a
  Node/TypeScript server, so `NODE_TLS_REJECT_UNAUTHORIZED=0` or `NODE_EXTRA_CA_CERTS=<path>` in the
  `env` block of `.mcp.json` is the *likely* workaround — Node honours both process-wide. **This is
  an inference, not a documented feature. Gap G4.**
- **C2 ⚠️ → the pivotal nuance.** No board tools, but it claims **label** tools and **issue update**.
  On GitLab that is *sufficient*, because **GitLab boards are label-driven** — the board is a *view*
  over scoped labels. `gitlab_sync.py` proves this: it moves cards by attaching `status::to-do` /
  `status::in-progress`. So "no board tools" does **not** mean "cannot move a card"; it means
  "cannot create/reorder board *lists*". Column *creation* is a one-time setup act; column
  *movement* is the recurring act. **This asymmetry is the key C2 insight for GitLab.**
- **C4 ❌** — GitLab only.
- **C5 ✅** — MCP tools are exactly "agent-drivable without hand-rolled API calls".
- **C6 n/a** — no CLI install; `npx`/Docker.
- **Maintenance ✅** — v2.1.45 with 1.9k stars indicates active development. **Exact last-release
  date not captured — Gap G5.**

### Part 3 — Forge CLIs

#### F1. `glab` — official, and **the only candidate with a first-class documented answer to C1**

**Evidence** (official docs, `docs.gitlab.com/cli/`, reputation 1.0, accessed 2026-08-10):

| Concern | Finding |
|---|---|
| Official? | ✅ Yes — `gitlab-org/cli`, GitLab's own project, documented on `docs.gitlab.com` |
| Offerings | *"GitLab.com, GitLab Dedicated, and GitLab Self-Managed"* |
| Self-hosted host | **`GITLAB_HOST` or `GL_HOST`** — *"If GitLab Self-Managed or GitLab Dedicated, specify the URL of the GitLab server"* (default `https://gitlab.com`) |
| Config location | `~/.gitlab/glab-cli/config.yml`, overridable with **`GLAB_CONFIG_DIR`** |
| Auth | **`GITLAB_TOKEN`** env var, or `glab auth login`; OAuth 2.0 also supported |
| **TLS** | **`glab config set skip_tls_verify true --host gitlab.example.com`** |
| Board commands | **None documented.** Docs list CI/CD pipelines, **issues**, MRs, changelogs, releases, Kubernetes agent — **boards are not referenced** |

**The `skip_tls_verify` finding is the C1 answer.** Note its shape: it is **per-host**
(`--host gitlab.example.com`), which is *better* than the process-wide `NODE_TLS_REJECT_UNAUTHORIZED=0`
that the `http`-transport MCP path forces. Verification stays on for every other host.
**Sources**: the `skip_tls_verify` command form appears in search-surfaced GitLab CLI documentation
and is corroborated by the long-standing `profclems/glab` issue **#781**, *"glab does not work on self
hosted gitlab instance with self signed certificates authority"* — the problem is well-known and
`skip_tls_verify` is the project's answer to it. **Confidence: Medium-High.** I did not fetch a page
that renders the config-key reference table directly; **Gap G8** names the exact resolving test.

**C2 for `glab`: ⚠️, and the same GitLab nuance as M3 applies.** No `glab board` command exists, but
`glab issue update --label status::in-progress --unlabel status::to-do` is a card move, because
**GitLab boards are label views**. What `glab` cannot do is create or reorder board *lists* —
`gitlab_sync.py` phase 5 territory, a one-time setup act.

**Assessment**: C1 ✅ (per-host, documented). C2 ⚠️ (issues+labels = moves; no list management).
C3 ✅ (`GITLAB_TOKEN`, a PAT — and GitLab project access tokens work here). C4 ❌ GitLab only.
C5 ⚠️ — an agent runs shell commands, which is drivable but is *not* the same as typed MCP tools; it
needs a documented command vocabulary (this is the "one knowledge skill" hypothesis).
**C6 ❌ — install cost.** Ubuntu/WSL: GitLab package repo, `apt`, or a release tarball.

#### F2. `gh` — `gh project item-edit` **does** move cards, by field name

**Evidence** (official `cli.github.com/manual`, accessed 2026-08-10):

> *"The usual way to select the item and field is by name: pass the project number plus `--owner`,
> point at the item with its issue or pull request `--url`, and name the field with `--field`."*

```
gh project item-edit 1 --owner monalisa \
  --url https://github.com/monalisa/myproject/issues/23 \
  --field "Status" --value "In Progress"
```

Flags: `--field <string>`, `--field-id <string>`, `--value`, `--single-select-option-id`,
`--id`, `--project-id`. The docs add: *"For scripts and machine use, you can also pass GraphQL node
IDs directly."*

**This is a significant correction to a widespread belief.** Community sources assert the CLI
*"expects the underlying field ID of the status rather than simply using 'In Progress'"* — the
official manual contradicts that: `--field "Status" --value "In Progress"` is the documented "usual
way", with node IDs offered as the *scripting* alternative. See **Conflicting Information**.
**Confidence: High** — the official manual outranks the blog posts, and the id-only claim is
plausibly stale (`gh project` went GA and has evolved since).

**Assessment**: C1 n/a (github.com). **C2 ✅ — and by human-readable names, which matters a lot for
agent-drivability.** C3 ⚠️ — Projects v2 needs a **`project` scope** token in addition to `repo`;
Projects are owner-scoped (user/org), **not** project-scoped, so a repo-scoped credential is
structurally impossible for the board. C4 ❌. C5 ✅. **C6 ❌ — install cost** (`apt` via GitHub's
repo, or the Windows `gh.exe` already on PATH per the prior research pass — see L3).

#### F3. Honest test of the prior session's conclusion — *"the reusable asset is the knowledge, not the code"*

The prior session concluded this. **This research pass largely confirms it, but with one sharp
correction.**

**Confirming**: for GitHub, `gh project item-edit --field "Status" --value "In Progress"` and
`issue_write` via MCP both mean **there is nothing to build.** What a future session needs is not
code but four facts: (1) boards are Projects v2, a different API; (2) `item-edit` takes field
*names*; (3) the token needs `project` scope; (4) the item must be *added* to the project before its
fields exist. That is a skill, not a script.

**Correcting**: for **GitLab specifically**, the knowledge-versus-code line does not fall where the
prior session put it, because of **two-pass write ordering**. `gitlab_sync.py` phase 2 → phase 3
exists because *"issue IIDs are assigned at creation so dependencies need a two-pass write"*
(lines 238-265: create all issues, collect `iid_of`, then `PUT` descriptions with real `#iid` refs).
**No documented knowledge makes that go away.** An agent told "GitLab assigns IIDs at creation, so
write dependency links in a second pass" must then perform N creates + M updates as **individual
tool calls**, holding an ID map in context across all of them. That is a *state-machine*, and
state-machines in agent context are exactly what is fragile. **[Interpretation, flagged.]**

**Verdict on the hypothesis**: knowledge beats code for **card moves** (single-call, idempotent-ish,
stateless) and for **GitHub generally**. Code beats knowledge for **bulk seeding with cross-references
over a flaky link** — which is precisely and only what `gitlab_sync.py` does.

### Part 4 — Claude Code plugins and skills

#### P1. The `gitlab` and `github` plugins in `claude-plugins-official` are the answer, and they are one command away

Install form, corroborated against the local marketplace files (L1, L2):
`/plugin install gitlab@claude-plugins-official` and the equivalent for `github`.
**Sources**: local `marketplace.json` + `external_plugins/{github,gitlab}/` trees (primary,
accessed 2026-08-10), corroborated by
[claude.com/plugins/gitlab](https://claude.com/plugins/gitlab) and the
`anthropics/claude-plugins-official` marketplace manifest. **Confidence: High.**

**But they are `.mcp.json` shims with no code.** Their entire content is a URL. That means:
- The `github` plugin is **excellent and free** for github.com. Adopt it.
- The `gitlab` plugin's URL is **hardcoded to `https://gitlab.com/api/v4/mcp`**. To point it at
  `10.10.1.4` the user must **not install the plugin** but instead hand-write an equivalent entry in
  their own `.mcp.json` — trivially easy, and it inherits every C1/auth problem in Finding M2.

#### P2. Nothing in the plugin/skill ecosystem manages a *forge* board

Searching surfaced `mattjoyce/kanban-skill`, `NikiforovAll/claude-code-kanban`, and a "Kanban Board
Manager" skill — **all of them are local-markdown kanban tools**, i.e. the category the prior
research pass already settled. **Not one** manages GitHub or GitLab issues as a board.
`RealMikeChong/claude-code-for-gitlab` is a different thing entirely — GitLab **CI** integration to
run Claude like GitHub Actions, not issue-board management.
**Confidence: Medium** — this is an argument from absence across one search round. **Gap G9.**

**This is a real finding**: the plugin ecosystem's answer to "kanban" is *local markdown*, and its
answer to "forge" is *raw MCP*. **Nobody has built the bridge between them.**

### Part 5 — git-native issue trackers with forge bridges

#### N1. `git-bug` — verify carefully, as instructed, and it does **not** survive verification

**Evidence** (`git-bug/git-bug`, accessed 2026-08-10):

| Attribute | Value |
|---|---|
| Stars | ~10,000 |
| License | GPLv3-or-later |
| Commits | 2,632 |
| **Latest release** | **v0.10.1 — 2025-05-19** (preceded by v0.10.0 2025-05-18, v0.9.0 2025-05-12) |
| Bridges | *"Jira, GitHub, GitLab, Launchpad"* |
| Bridge nature | *"bi-directional, incremental, and speedy gateways to third-party platforms"*; *"push and pull issues to and from a third party platform"* via `git bug bridge push/pull` |
| Self-hosted GitLab | `--base-url` option on bridge configure |

**Kill reason 1 — maintenance. `v0.10.1` is dated 2025-05-19; today is 2026-08-10. That is ~14.7
months.** Per the brief's own source-discipline rule (*flag anything unmaintained >12 months*), **this
candidate is flagged.** Commits may continue on `master`/`trunk`, but no release has shipped in over
a year and it remains pre-1.0. **Confidence: High** (GitHub releases page is authoritative).

**Kill reason 2 — C2 fails structurally.** git-bug models issues with **status (open/closed) and
labels**. It has **no board or column concept**. Its docs do not address label or status *mapping*
between platforms (the `third-party.md` page is silent on it, and defers to a `feature-matrix.md` I
did not fetch — **Gap G10**). Whether a git-bug label round-trips as a GitLab **scoped** label
(`status::to-do`, which is what actually provides mutual exclusion on drag) is **unverified and
doubtful**. Scoped labels are a GitLab-specific naming convention; a generic bridge has no reason to
preserve their exclusivity semantics.

**Kill reason 3 — C1 unverified, with a documented history of exactly this class of bug.** `--base-url`
exists, but the bridge *"didn't support self-hosted GitLab instances, with the API call being sent to
`https://gitlab.com/api/v4/projects` instead of the specified instance"* — later addressed. **No TLS
option was found anywhere.** As a Go binary it would honour the **OS trust store**
(`/usr/local/share/ca-certificates` + `update-ca-certificates`) — which fixes *self-signed* but
**not expired** (see C1.1). **C1: ❌/? — most likely fails on the expired cert with no escape hatch.**

**Kill reason 4 — bridge quality signals are poor.** Open issues found by title:
[#366 *"Multiple bugs with gitlab bridge"*](https://github.com/git-bug/git-bug/issues/366) and
[#284 *"Pushing to a bridge does not push comments added via git-bug"*](https://github.com/git-bug/git-bug/issues/284).
The second is a **data-loss-shaped** defect in the push direction — content authored locally does not
reach the forge. **Confidence: Medium** (issue titles are authoritative for the report's existence,
not for current status; I did not fetch either body — **Gap G11**).

**Kill reason 5 — architectural mismatch with the user's own decision.** The user has ruled: **ONE
system of record, no bidirectional sync.** git-bug's entire premise is a **third store** (issues in
git objects) that syncs **bi-directionally** with the forge. Adopting it would mean *three* stores
(Backlog.md, git-bug, forge) and the exact sync topology the user rejected.

**Disposition: REJECTED.** It is the only candidate that could theoretically have satisfied
issues + committed-to-git + both forges simultaneously, and the brief was right to demand careful
rather than optimistic verification. It fails on maintenance, on boards, probably on C1, and
decisively on the user's stated architecture. **Fits: neither Role A nor Role B.**

#### N2. `dspinellis/git-issue` — assessed briefly

Same class: shell-based, issues stored in git. Not verified in this pass beyond its existence and
category. It is a **smaller, shell-implemented** project than git-bug with the same structural
problems: no board model, a third store, and bidirectional import/export.
**Disposition: rejected by inheritance from N1's structural reasons.** **Confidence: Low** on the
specifics — **Gap G12**. Not worth further budget given N1's outcome.

### Part 6 — Backlog.md → forge bridges

#### B1. **No such bridge exists.** This is a confirmed negative.

Searching for a Backlog.md ↔ GitHub/GitLab issue sync returned **nothing**: no feature in the project,
no community tool, no plugin. The nearest hits were unrelated (`quadeare/gitlab-issues-sync` on Docker
Hub, a generic GitLab-to-GitLab tool; a "Sync to GitLab" GitHub Action, which syncs *repositories*,
not issues).

**Corroborating evidence from the project's own positioning**: Backlog.md advertises
*"100% private & offline"* with *"backlog living entirely inside your repo."* A forge bridge is
**contrary to its stated value proposition**, so its absence is a design stance, not an oversight.
**Source**: [MrLesk/Backlog.md](https://github.com/MrLesk/Backlog.md) — Accessed 2026-08-10,
reputation 0.8. **Confidence: Medium-High** (argument from absence, but with a positive corroborating
signal from the project's own framing). **Gap G13** names the resolving check.

**Consequence**: **Role B has no off-the-shelf implementation for either forge.** If Backlog.md stays
the system of record, the projection layer is 100% custom — which is exactly what `gitlab_sync.py`
already is.

Also noted: Backlog.md now ships an **MCP server** of its own (issue #558 references
*"MCP server writes to main repo instead of git worktree"*, so it is real and has known worktree
bugs). That is relevant only in that Claude already has typed tools for the *local* side.
**Confidence: Medium** (inferred from an issue title).

## The C1 Question, Answered Per Candidate

*(pending)*

## The C2 Question, Answered Per Candidate

### C2.1 — The two forges make "move a card" mean two completely different things

| | GitLab | GitHub |
|---|---|---|
| What a board *is* | A **view over labels**. Each list is bound to a label. | A **Project (v2)**, a separate object from the repo, with typed **fields**. |
| Moving a card = | **Swap scoped labels** (`status::to-do` → `status::in-progress`). Mutual exclusion comes free from the `scope::value` convention. | **Set the `Status` single-select field** on a *project item*. |
| Which API | **Issues REST** (`PUT /projects/:id/issues/:iid` with `labels`) — the *same* API as issue CRUD. | **Projects v2 GraphQL** — a **different API** from Issues REST. |
| Consequence | **Any tool that can update an issue's labels can move a card.** Board tools are optional. | **A tool can have complete Issues support and still be unable to move a card.** |

**This asymmetry is the single most useful thing in this document for evaluating any future
candidate.** The brief's warning — *"many tools do issues but NOT boards"* — is **true for GitHub and
misleading for GitLab.** On GitLab, "issues-only" tools *can* drive the board; they merely cannot
*build* it. On GitHub, "issues-only" genuinely means no board.

`gitlab_sync.py` independently confirms the GitLab half: it moves cards purely by attaching
`status::to-do` / `status::in-progress` labels (lines 147-154), and touches the `boards` API **only**
in phase 5 to create the two *lists* — a one-time setup act, never a per-move act.

### C2.2 — Per-candidate C2 verdicts

| Candidate | Issue CRUD | Move a card between columns | Create/reorder board lists | **C2** |
|---|---|---|---|---|
| **GitHub MCP** (hosted or local) | ✅ `issue_write` | ✅ **`projects_write` → `update_project_item`**, `{"name":"Status","value":…}` | ✅ `projects_list` → `list_project_fields` for discovery | **✅ full** |
| **`gh` CLI** | ✅ `gh issue` | ✅ `gh project item-edit --field "Status" --value "In Progress"` | ⚠️ fields/options via `gh project field-list`; creating a Project is `gh project create` | **✅ full** |
| **`zereight/gitlab-mcp`** | ✅ | ✅ **via label tools + issue update** (GitLab semantics) | ❌ no board-list tools | **⚠️ moves yes, lists no** |
| **Official GitLab MCP** | ? read confirmed, **write unverified (G3)** | **?** — depends on whether label-update tools exist | ? | **? — the blocking unknown** |
| **`glab` CLI** | ✅ `glab issue` | ✅ `glab issue update --label/--unlabel` | ❌ no board commands | **⚠️ moves yes, lists no** |
| **`git-bug`** | ✅ locally | ❌ no column model; scoped-label round-trip doubtful | ❌ | **❌** |
| **`gitlab_sync.py`** | ✅ create | ✅ scoped labels | ✅ **phase 5 creates board lists** | **✅ full (verified by execution)** |

### C2.3 — Two GitHub gotchas that documentation buries

1. **An issue is not a project item.** Fields do not exist until the issue is **added to the
   Project** (`gh project item-add`, or the MCP equivalent). Seeding GitHub therefore has its own
   two-step shape: create issue → add to project → set field. **[Reasoned from the API model; not
   directly quoted from a source. Gap G14.]**
2. **Projects v2 are owner-scoped, not repo-scoped.** A Project belongs to a user or org, so a
   repo-scoped credential **cannot** reach it. This makes **C3's "ideally project-scoped" structurally
   impossible on GitHub for the board layer** — while on GitLab, a project access token with `api`
   scope reaches labels, issues *and* boards. **GitLab wins C3 outright.**

## Verdict on `gitlab_sync.py`

### Was hand-building it necessary?

**Yes. It was necessary, and it was not wasted effort.** Every off-the-shelf alternative fails at
least one constraint that the script had to satisfy *at that moment*:

| Alternative | Why it could not have done that job |
|---|---|
| Official GitLab MCP (`/api/v4/mcp`) | OAuth-DCR-only (the user has a **PAT**); requires **Duo on** + beta features; `http` transport means the **expired cert** forces process-wide TLS-off |
| `zereight/gitlab-mcp` | Closest viable substitute, but **no documented TLS escape hatch**, and no board-list tools |
| `glab` | **Not installed** (C6). Real answer to C1 (`skip_tls_verify`) but no board-list commands |
| `git-bug` | Unreleased for ~15 months, no column model, no TLS option, wrong architecture |
| Backlog.md bridge | **Does not exist** |

And two of the script's behaviours are matched by **nothing** examined:
- **Two-pass IID backfill** (phases 2→3). GitLab assigns IIDs at creation, so cross-references cannot
  be written on the first pass. No tool solves this; an agent doing it via tool calls must hold an ID
  map across N+M calls.
- **Connection-level retry with the 4xx/5xx exclusion** (lines 68-98). No MCP server or CLI documents
  retry semantics for a flapping link.

### But how much of it *should* have been code?

**Roughly half of its value was knowledge that is now permanently captured** and did not need to be
expressed as Python:
- GitLab boards are label-driven → a board move is a label swap.
- Scoped labels (`status::to-do`) give mutual exclusion on drag.
- `blocks` / `blocked by` **link types are GitLab Premium** — hence the script's workaround of writing
  a `## Blocked by` markdown section instead of using the links API. **This is a genuinely valuable,
  non-obvious finding and it is pure knowledge.**
- Board *lists* are created once; cards move forever.

### Does anything off-the-shelf now replace it?

**Split answer, and the split is the useful part:**

- **For the recurring operation — moving a card — YES.** `zereight/gitlab-mcp` (PAT + custom URL +
  label/issue-update tools, stdio transport so TLS-off is *scoped*) or `glab` (documented per-host
  `skip_tls_verify`) both do it. The script should **never** be extended to handle moves.
- **For the one-time bulk seed with cross-references over a flaky link — NO.** Nothing replaces it.

**Therefore: treat `gitlab_sync.py` as spent capital, not a maintained asset.** It did a one-time job
that only needed doing once. Do not extend it, do not build a GitHub twin *unless Role B is chosen*,
and do not delete it — it remains **the only proven-working TLS + retry configuration against
`10.10.1.4`**, which makes it the reference implementation for C1 on this network.

## The Minimal Remaining Gap

### The decisive realisation: buy-vs-build is decided by the *role choice*, not by the tooling

| | **Role A** — forge is system of record | **Role B** — Backlog.md is SoR, forge is projection |
|---|---|---|
| GitHub | **~100% bought.** Official MCP server, already in two of the user's marketplaces, one `/plugin install` away. Issues + Projects v2 field updates = full board control. | **0% bought.** No markdown→GitHub-issues projector exists. |
| GitLab | **~85% bought.** `zereight/gitlab-mcp` or `glab` gives issues + labels = card moves. Missing: board-list creation (one-time), and a verified TLS answer. | **0% bought.** `gitlab_sync.py` *is* the state of the art, and it is bespoke. |
| Drift detection | **Not needed** — there is nothing to drift from. | **0% bought.** Nothing compares markdown to forge state. |
| **Remaining gap** | **Small, and it is DOCUMENTED KNOWLEDGE.** | **Large, and it is CODE.** |

**Role A can be bought. Role B must be built.** Since the user has already decided there will be
**one system of record and no bidirectional sync**, and since Role A is the cheap side of that
decision, **the recommendation is Role A: promote the forge to system of record and let Backlog.md
retire or become a read-only local projection.**

### If Role A: exactly what remains

**Nothing to code.** What remains is **one skill file** carrying six facts, plus **one empirical test**.

The knowledge (all established in this document):
1. GitLab boards are **label views**; a card move is a **scoped-label swap**. Board *lists* are
   created once, in the UI or via `POST /boards/:id/lists`.
2. GitHub boards are **Projects v2**, a **different API** from Issues. `gh project item-edit --field
   "Status" --value "In Progress"`, or MCP `update_project_item` with `{"name":"Status","value":…}`.
3. On GitHub an issue must be **added to the Project** before it has fields.
4. GitLab `blocks`/`blocked by` **link types are Premium** — use a `## Blocked by` markdown section
   with `#iid` references instead.
5. GitLab **IIDs are assigned at creation** — cross-references need a second pass.
6. Credential shapes differ: GitLab **project** access token with `api` scope suffices for issues,
   labels *and* boards; GitHub needs an **owner-scoped** token with `project` scope because Projects
   are not repo-scoped.

The one test (**Gap G4, the highest-value unknown in this document**):
> Does `zereight/gitlab-mcp` reach `https://10.10.1.4` when its `.mcp.json` `env` block sets
> `NODE_TLS_REJECT_UNAUTHORIZED=0` alongside `GITLAB_API_URL=https://10.10.1.4/api/v4` and
> `GITLAB_PERSONAL_ACCESS_TOKEN`?
>
> **If yes**: GitLab is bought, the gap closes to knowledge alone, and no code is ever written again.
> **If no**: install `glab` (C6 cost, one time) and use its documented per-host
> `skip_tls_verify` — the fallback is *known to exist*, so the risk here is cost, not feasibility.

**Either way the answer is buy.** There is no branch of this decision tree that leads back to writing
API code for the recurring operation.

### The one thing nobody sells, in either role

**Flaky-link write safety.** No MCP server or CLI examined documents connection-level retry, and none
offers idempotency keys. A dropped connection mid-write leaves the agent unable to distinguish
"failed" from "succeeded but the response was lost" — and its recovery is to *retry*, which on a
create operation **duplicates the issue**. `gitlab_sync.py` handled this by never retrying HTTP
errors and only retrying connection failures on operations it controlled.

**Mitigation is knowledge, not code**: prefer **idempotent** operations (label set/unset, field set —
all safe to repeat) over **non-idempotent** ones (issue create). Which is another argument for Role A:
in steady state, the only operation is a card move, and **card moves are idempotent.**
**[Interpretation, flagged. This is the residual risk that survives every candidate.]**

## Source Analysis

| Source | Domain | Reputation | Type | Access date | Cross-verified |
|---|---|---|---|---|---|
| `external_plugins/github/.mcp.json` | local FS | **1.0** | primary observation | 2026-08-10 | Y — corroborated by `engineering/.mcp.json` (same URL) and github-mcp-server docs |
| `external_plugins/gitlab/.mcp.json` + `plugin.json` | local FS | **1.0** | primary observation | 2026-08-10 | Y — URL shape corroborated by `docs.gitlab.com` self-managed endpoint |
| `knowledge-work-plugins/engineering/.mcp.json` | local FS | **1.0** | primary observation | 2026-08-10 | Y |
| `claude-automation-recommender/references/mcp-servers.md` | local FS | **1.0** | primary observation | 2026-08-10 | n/a (used only for an absence claim) |
| GitLab MCP server docs | docs.gitlab.com | **1.0** | official | 2026-08-10 | Y — endpoint matches local `.mcp.json` |
| GitLab CLI docs | docs.gitlab.com | **1.0** | official | 2026-08-10 | Y — `skip_tls_verify` corroborated by glab#781 |
| `gh project item-edit` manual | cli.github.com | **1.0** | official | 2026-08-10 | Y — contradicts and outranks community claims |
| Enterprise network configuration | code.claude.com | **1.0** | official first-party | 2026-08-10 | Y — variable names corroborated by 4 issue reports |
| `github/github-mcp-server` | github.com | 0.8 | vendor repo | 2026-08-10 | Y — hosted URL matches local files |
| `zereight/gitlab-mcp` | github.com | 0.8 | project repo (claims only) | 2026-08-10 | N — **single source**, confidence reduced accordingly |
| `git-bug/git-bug` repo + releases + `third-party.md` | github.com | 0.8 | project repo | 2026-08-10 | Y — releases page + docs + 2 issue titles |
| anthropics/claude-code **#2899** | github.com | 0.8 | vendor issue tracker | 2026-08-10 | Y — corroborated by #55760, #22512, #26897 |
| anthropics/claude-code #55760, #22512, #26897 | github.com | 0.8 | vendor issue tracker (titles only) | 2026-08-10 | Y — mutually corroborating |
| `profclems/glab` **#781** | github.com | 0.8 | project issue tracker | 2026-08-10 | Y |
| git-bug **#366**, **#284** | github.com | 0.8 | project issue tracker (titles only) | 2026-08-10 | N |
| `MrLesk/Backlog.md` | github.com | 0.8 | project repo | 2026-08-10 | Y — with prior research pass |
| `claude.com/plugins/gitlab` | claude.com | 0.8 | vendor listing | 2026-08-10 | Y — matches local marketplace |
| `mcpland/gitlab-mcp` | github.com | 0.8 | project repo (named only) | 2026-08-10 | N |

**Reputation**: High (1.0): **8 of 18 = 44%** · Medium-High (0.8): 10 of 18 = 56% · Medium or below: **0**.
**Average reputation: 0.89.** No excluded-tier domain was cited. Two search results from excluded or
low-trust domains (a `gist.github.com` snippet, an `ofox.ai` blog, a `claudelab.net` blog) were
**read but not cited**; the Bun/BoringSSL claim they carried was retained only because four
first-party issue reports independently corroborate it.

**Bias note**: `github/github-mcp-server`, `docs.gitlab.com` and `cli.github.com` are all
**vendor sources describing their own products** — commercial interest is present. Mitigated by using
them only for *configuration and capability surface* (where a vendor is authoritative and has little
incentive to misstate flag names) and by sourcing every *failure* claim from issue trackers instead.

## Knowledge Gaps

### G1 — Is `gh` really absent, or only absent from the Linux userland?
**Issue**: the brief says `gh`/`glab` are not installed (verified). The **prior research pass** recorded
`gh` at `/mnt/c/Program Files/GitHub CLI/` via a `~/.claude/settings.json` PATH entry.
**Attempted**: reconciliation of two documentary sources; no command was run.
**Recommendation**: `which gh; gh --version` inside WSL. If the Windows binary resolves, C6's install
cost for GitHub drops to zero — but path translation and credential-store location need checking.

### G2 — Does a **Free self-managed** GitLab expose a working `/api/v4/mcp`? **(highest-value GitLab unknown)**
**Issue**: docs list tiers as "Free, Premium, Ultimate" **but** require GitLab Duo availability set to
"Always on"/"On by default". Whether a Free self-hosted instance with no Duo entitlement can satisfy
that prerequisite is not stated.
**Attempted**: the official MCP server page; it states the prerequisite without qualifying it by tier.
**Recommendation**: check the instance's GitLab version (must be **≥18.6** for no feature flags) and
Admin → GitLab Duo settings. An unauthenticated `GET https://10.10.1.4/api/v4/mcp` returning 404 vs
401 would answer it — **but the brief forbids calls to that host, so this is deferred to the user.**

### G3 — Does the official GitLab MCP server **write**, or only read?
**Issue**: the tool list is on a separate page not fetched. The page's own language is read-leaning
("Access…", "Retrieve…"). Without label-update tools, C2 fails outright.
**Recommendation**: fetch `docs.gitlab.com`'s MCP **Tools** reference page.

### G4 — **THE decisive test.** Does `NODE_TLS_REJECT_UNAUTHORIZED=0` in a stdio MCP `env` block work?
**Issue**: `zereight/gitlab-mcp` documents no TLS escape hatch. That Node honours the variable is an
**inference from the runtime**, not a documented feature.
**Attempted**: the project README (silent beyond `MCP_DANGEROUSLY_ALLOW_INSECURE_ISSUER_URL`, which is
for local HTTP dev, not cert validation).
**Recommendation**: add the server to `.mcp.json` with `env: { GITLAB_API_URL, GITLAB_PERSONAL_ACCESS_TOKEN,
NODE_TLS_REJECT_UNAUTHORIZED: "0" }` and call one read tool. **This single test converts the central
recommendation from inference to fact.** If it fails, install `glab`.

### G5 — `zereight/gitlab-mcp` last-release **date**
**Issue**: version v2.1.45 captured; **no date**. The brief requires a last-release date per candidate.
**Recommendation**: `registry.npmjs.org` packument or the repo's releases page. High version number
plus 1.9k stars *suggests* active, but suggestion is not evidence.

### G6 — `github/github-mcp-server` last-release version and date
**Issue**: the repo landing page showed 1,031 commits but no release tag/date.
**Recommendation**: its `/releases` page. Low risk — it is a first-party GitHub project with 32.1k stars.

### G7 — `mcpland/gitlab-mcp` entirely unassessed
**Issue**: surfaced by search; zero capability, TLS, or maintenance data gathered. Its
"policy-controlled access" framing is potentially interesting for a single-token setup.
**Recommendation**: assess only if G4 fails **and** `glab`'s install cost is unacceptable.

### G8 — `glab`'s TLS config keys not read from a rendered reference table
**Issue**: `skip_tls_verify` came from search-surfaced documentation text plus corroboration from
glab#781, not from a directly-fetched config-key reference.
**Recommendation**: `glab config --help` after install, or `docs.gitlab.com/cli/` configuration section.
**Also unresolved**: whether `glab` supports a **custom CA** path in addition to skip-verify (moot here,
since the cert is expired).

### G9 — Plugin/skill ecosystem search was one round
**Issue**: the "no plugin manages a forge board" claim (P2) is an argument from absence over a single
search round across `claudemarketplaces.com`, `claudeskills.info`, `mcpmarket.com` results.
**Recommendation**: `/plugin` marketplace browse in-session; search `awesome-claude-skills`.

### G10 — `git-bug`'s `feature-matrix.md` not fetched
**Issue**: `third-party.md` explicitly defers label/status mapping to a feature matrix I did not read.
That document would settle whether GitLab **scoped** labels round-trip.
**Recommendation**: fetch `doc/feature-matrix.md`. **Low priority** — git-bug is rejected on four other
independent grounds.

### G11 — git-bug issues #366 and #284 known by **title only**
**Issue**: both may be fixed. "Multiple bugs with gitlab bridge" and "Pushing to a bridge does not push
comments" are cited as *signals*, not as current defects.
**Recommendation**: check open/closed state. **Low priority** — same reason as G10.

### G12 — `dspinellis/git-issue` assessed only by category
**Issue**: rejected by inheritance from git-bug's structural problems, not on its own evidence.
**Recommendation**: none. Budget better spent elsewhere; the structural objection (third store,
no column model) is category-level and holds.

### G13 — B1 is an argument from absence
**Issue**: "no Backlog.md↔forge bridge exists" rests on one search round plus the project's
"100% private & offline" positioning. A bridge could exist as an undiscovered script or an open PR.
**Recommendation**: search `MrLesk/Backlog.md` issues/PRs for "github issues", "gitlab", "sync",
"export". **Worth doing** — a positive find would make Role B cheap and invert the recommendation.

### G14 — "issue must be added to a Project before it has fields" is reasoned, not quoted
**Issue**: derived from the Projects v2 data model, not lifted from a fetched page.
**Recommendation**: `cli.github.com/manual/gh_project_item-add` confirms the step exists.

### G15 — No candidate was installed or executed; no call made to `10.10.1.4`
**Issue**: **the pass-wide limitation**, and the same one that the prior research pass had to supersede
within a day. Every C1 verdict is architectural reasoning, not measurement.
**Recommendation**: G4 first, then G2. Expect a supersession block on this document too.

## Conflicting Information

### Conflict 1 — Does `gh project item-edit` accept a field *name* or only IDs?
**Position A**: names work. *"The usual way to select the item and field is by name: pass the project
number plus `--owner`, point at the item with its issue or pull request `--url`, and name the field with
`--field`"* — [cli.github.com/manual/gh_project_item-edit](https://cli.github.com/manual/gh_project_item-edit),
reputation **1.0**.
**Position B**: only IDs work. *"The CLI expects the underlying field ID of the status rather than
simply using 'In Progress'"* — community blog/gist sources, reputation ≤0.6.
**Assessment**: **Position A.** The official manual outranks the community sources, shows a working
name-based example, and explicitly frames node IDs as the *scripting* alternative
(*"For scripts and machine use, you can also pass GraphQL node IDs directly"*). Position B is most
likely **stale** — `gh project` has evolved since GA. **This matters for C5**: name-based addressing is
dramatically more agent-drivable than a four-ID lookup dance.

### Conflict 2 — Does Claude Code honour `NODE_EXTRA_CA_CERTS`?
**Position A**: yes. *"If your enterprise environment uses a custom CA, configure Claude Code to trust it
directly: `export NODE_EXTRA_CA_CERTS=/path/to/ca-cert.pem`"*, with a documented debug-log confirmation
line — [code.claude.com/docs/en/network-config](https://code.claude.com/docs/en/network-config),
reputation **1.0**.
**Position B**: not reliably. Four independent `anthropics/claude-code` issues report failures —
#22512 (ignored in `settings.json`), #26897 (not working), #55760 (ignored for **hosted MCP OAuth**
since v2.1.113), #2899 (HTTP/SSE MCP servers reject self-signed certs, **closed as not planned**).
The stated mechanism is that Claude Code became a **Bun-compiled binary** at v2.1.113 and Bun's global
`fetch` uses **BoringSSL**, which does not read `NODE_EXTRA_CA_CERTS`.
**Assessment**: **both are true of different code paths, and that is the actionable finding.** The
variable works for Claude Code's *primary API* connection (which the docs describe and the debug log
confirms) and fails or is bypassed on *some* paths, notably **MCP over HTTP** and **hosted MCP OAuth
initiation** — precisely the paths the official GitLab MCP server needs. The official doc is
authoritative but describes the intended design; the issue tracker describes the shipped behaviour on
the specific path this user requires. **Confidence: Medium-High.**
**And it is moot for this user anyway**: the cert is **expired**, so no CA import of any kind would
work even on a fully compliant runtime. This conflict is documented because it would matter if the
cert were renewed — **renewing the cert is the cheapest single action that improves this whole
situation**, since it would move the official GitLab MCP server from ❌ to a genuine contender.

### Conflict 3 — Is `gh` installed on this machine?
**Position A**: no — the research brief, stated as verified (C6).
**Position B**: yes at `/mnt/c/Program Files/GitHub CLI/` — the prior research pass, sourced to
`~/.claude/settings.json`.
**Assessment**: **compatible, not contradictory** — a Windows binary on the WSL PATH is not a Linux
install. The brief is authoritative for the intended posture. Recorded as **Gap G1** rather than
resolved, because no command was run.

## Full Citations

[1] Local filesystem. `~/.claude/plugins/marketplaces/claude-plugins-official/external_plugins/github/.mcp.json` and `.claude-plugin/plugin.json`. Accessed 2026-08-10.
[2] Local filesystem. `~/.claude/plugins/marketplaces/claude-plugins-official/external_plugins/gitlab/.mcp.json` and `.claude-plugin/plugin.json`. Accessed 2026-08-10.
[3] Local filesystem. `~/.claude/plugins/marketplaces/knowledge-work-plugins/engineering/.mcp.json`. Accessed 2026-08-10.
[4] Local filesystem. `~/.claude/plugins/marketplaces/claude-plugins-official/plugins/claude-code-setup/skills/claude-automation-recommender/references/mcp-servers.md`. Accessed 2026-08-10.
[5] GitLab. "GitLab MCP server". GitLab Docs. https://docs.gitlab.com/user/model_context_protocol/mcp_server/. Accessed 2026-08-10.
[6] GitLab. "GitLab CLI (`glab`)". GitLab Docs. https://docs.gitlab.com/cli/. Accessed 2026-08-10.
[7] GitHub. "`gh project item-edit`". GitHub CLI Manual. https://cli.github.com/manual/gh_project_item-edit. Accessed 2026-08-10.
[8] Anthropic. "Enterprise network configuration". Claude Code Docs. https://code.claude.com/docs/en/network-config. Accessed 2026-08-10.
[9] GitHub. "github/github-mcp-server". https://github.com/github/github-mcp-server. Accessed 2026-08-10.
[10] zereight. "gitlab-mcp". https://github.com/zereight/gitlab-mcp. Accessed 2026-08-10.
[11] git-bug. "git-bug". https://github.com/git-bug/git-bug. Accessed 2026-08-10.
[12] git-bug. "Releases". https://github.com/git-bug/git-bug/releases. Accessed 2026-08-10.
[13] git-bug. "doc/usage/third-party.md". https://github.com/git-bug/git-bug/blob/master/doc/usage/third-party.md. Accessed 2026-08-10.
[14] anthropics. "[BUG] Local MCP server will not trust self-signed certs" (issue #2899, opened 2025-07-03, closed as not planned). https://github.com/anthropics/claude-code/issues/2899. Accessed 2026-08-10.
[15] anthropics. "[BUG] Hosted MCP OAuth initiation ignores NODE_EXTRA_CA_CERTS on corporate MITM networks (v2.1.113+)" (issue #55760). https://github.com/anthropics/claude-code/issues/55760. Accessed 2026-08-10.
[16] anthropics. "[BUG] NODE_EXTRA_CA_CERTS is not effective when set in ~/.claude/settings.json" (issue #22512). https://github.com/anthropics/claude-code/issues/22512. Accessed 2026-08-10.
[17] anthropics. "NODE_EXTRA_CA_CERTS Environment variable not working" (issue #26897). https://github.com/anthropics/claude-code/issues/26897. Accessed 2026-08-10.
[18] profclems. "glab does not work on self hosted gitlab instance with self signed certificates authority" (issue #781). https://github.com/profclems/glab/issues/781. Accessed 2026-08-10.
[19] git-bug. "Multiple bugs with gitlab bridge" (issue #366). https://github.com/git-bug/git-bug/issues/366. Accessed 2026-08-10.
[20] git-bug. "Pushing to a bridge does not push comments added via git-bug" (issue #284). https://github.com/git-bug/git-bug/issues/284. Accessed 2026-08-10.
[21] MrLesk. "Backlog.md". https://github.com/MrLesk/Backlog.md. Accessed 2026-08-10.
[22] mcpland. "gitlab-mcp". https://github.com/mcpland/gitlab-mcp. Accessed 2026-08-10. *(named only, unassessed — G7)*
[23] Anthropic. "GitLab Plugin". https://claude.com/plugins/gitlab. Accessed 2026-08-10.
[24] Prior research pass. `docs/research/tooling/local-markdown-kanban-backlog-tooling-research.md`. This repo. 2026-08-10.
[25] `gitlab_sync.py` (310 lines), hand-built Backlog.md→GitLab seeder, verified working against the live self-hosted instance. Read as primary evidence 2026-08-10.

## Research Metadata

**Duration**: single pass, ~28 turns | **Sources examined**: 30+ | **Cited**: 25 | **Cross-references**: 14
**Confidence distribution**: High 55%, Medium-High 25%, Medium 15%, Low 5%
**Reputation**: High 44%, Medium-High 56%, Medium-or-below 0%. **Average 0.89.**
**Output**: `docs/research/tooling/claude-driven-forge-issue-boards-research.md`
**Primary local observations**: 4 (all four `.mcp.json`/`plugin.json`/reference files read directly)
**Constraint discipline honoured**: no credential read, no authenticated call, no request to `10.10.1.4`,
no write outside `docs/research/`, no other repo touched.
**Open gaps**: 15 (G1-G15). **Blocking gap: G4.** **Highest-leverage non-test action: renew the TLS
certificate on `10.10.1.4`** — it alone would promote the official GitLab MCP server from ❌ to
contender and remove the need for any TLS-off setting anywhere.
