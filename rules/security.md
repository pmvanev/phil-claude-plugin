---
paths:
  - "**/*.{ts,tsx,js,jsx,py,go,rs,java,cs,rb,kt,swift,cpp,c,h,hpp,scala,clj,ex,exs,hs,ml,fs,fsx}"
  - "**/*.{sh,bash}"
  - "**/.github/workflows/**"
  - "**/.gitlab-ci*"
  - "**/Dockerfile*"
  - "**/{package.json,.npmrc,pyproject.toml,pip.conf}"
  - "**/requirements*.txt"
---

# Security Guide

Guidelines extracted from Jerome Saltzer and Michael Schroeder's "The Protection of Information in Computer Systems" (1975), with Richard Smith's 2012 reassessment; Dan Bergh Johnsson, Daniel Deogun and Daniel Sawano's *Secure by Design*; Adam Shostack's *Threat Modeling: Designing for Security*; Loren Kohnfelder's *Designing Secure Software*; Heather Adkins et al.'s *Building Secure and Reliable Systems*; and Ken Thompson's "Reflections on Trusting Trust". Andrew Hoffman's *Web Application Security* (2nd ed., 2024) and Neil Madden's *API Security in Action* (2020) are named for web and API depth. The reviewer tables are keyed to MITRE's CWE and cite OWASP ASVS 5.0.0, the OWASP Cheat Sheet Series and NIST SP 800-63B-4. The agent rows draw on Greshake et al.'s "Not What You've Signed Up For" (AISec 2023), Simon Willison's "lethal trifecta", Debenedetti et al.'s CaMeL and Beurer-Kellner et al.'s "Design Patterns for Securing LLM Agents against Prompt Injections" (both 2025), and the OWASP Top 10 for LLM Applications 2025. Research: `docs/research/security/software-security-canonical-sources.md`.

This rule owns **what a reviewer flags as a security defect, what it must not flag, and the principles behind both**. Neighbouring rules keep what they already own: `react.md` the `dangerouslySetInnerHTML` idiom, `architecture.md` injecting secrets as runtime config, `continuous-delivery.md` pinning versions for reproducible builds, `test-architecture.md` the boundary test that holds a third-party dependency honest. Complement those — do not restate them.

**The two halves divide on checkability, not on subject.** The reviewer half — Always-flag, Advisory, Do not flag — names defects a diff shows, each by its CWE id. The Principles half is design: almost none of it shows on a line, and a review that files a principle as a defect lends it unearned authority. Both are here, labelled, so neither borrows the other's.

**"Untrusted" means data that crossed a trust boundary to reach this code**: request input; files, environment and arguments another principal controls; tool and model output; issue, PR and commit text; and the forge metadata other principals write — label, project, view, option, workflow and branch names. A value the code chooses from a closed set is trusted.

**Model output is untrusted where code acts on it with more than the model's own grant** — a hook, a CI job, a script that runs outside the session's permissions. A script that writes a path the model could already write grants nothing new, and no row fires on it.

---

## Principles — design, not review criteria

### Core Philosophy

> **"Base access decisions on permission rather than exclusion."** — Saltzer and Schroeder

Security is a property of the design, not a layer on top of it. Code that validates at the boundary, grants the least it can and fails closed is secure as a side effect; code that bolts checks on afterwards misses the one path nobody listed.

---

### What survived from 1975

Saltzer and Schroeder named eight principles; Smith sorted them by what practice kept. Cite the survivors and read the rest as advice.

| Principle | Status (Smith 2012) | What it rules out |
|---|---|---|
| **Least privilege** | Thrived — "almost every textbook recognizes" it | A process, token or agent holding rights its task never uses |
| **Fail-safe defaults** — deny by default | Thrived | A catch-all branch, error path or missing rule that grants access |
| **Complete mediation** — check every access | The central monitor faded; **the per-access check survived** | An authorization decision made once and reused across objects or requests |
| **Open design** | Thrived | Security that depends on an attacker not reading the code |
| **Compromise recording** | Thrived | A security decision that leaves no trace |
| **Economy of mechanism** | Faded in the market, not in the code | Authorization logic too intricate to review |

Smith's "complete mediation is obsolete" and OWASP's ranking of missing authorization as the most common web flaw are both right: the single reference monitor is gone, and the duty to check every request against every object remains.

### Validate at the boundary, then trust a type

*Secure by Design* treats security as a by-product of domain modelling. **Turn untrusted input into a domain primitive at the trust boundary** — a type that holds only valid values — and pass the primitive inward, never the raw string. Validate cheapest-first: origin, size, lexical content, syntax, then semantics, so the code refuses a ten-megabyte "username" before anything parses it. Inside the boundary, code trusts the type and validates nothing again.

### Know your trust boundaries

Shostack's four questions make threat modelling a conversation, not a document: **What are we working on? What can go wrong? What are we going to do about it? Did we do a good job?** A trust boundary is wherever data changes owner — a request arriving, a file read, a subprocess spawned, a model's reply returned. Every always-flag row below sits on one. Kohnfelder, co-author of STRIDE, supplies the threat vocabulary: spoofing, tampering, repudiation, information disclosure, denial of service, elevation of privilege.

### Make the safe thing the easy thing

*Building Secure and Reliable Systems* argues for APIs that are **safe by construction**: a query builder that cannot concatenate, a template engine that escapes by default, a subprocess call that takes an argument list. Prefer the framework's mechanism to a hand-rolled one — Microsoft's SDL calls this using "proven security features, languages and frameworks". A defect a type makes impossible needs no reviewer.

### Never compose cryptography

Use a maintained library's highest-level authenticated construction, with its defaults. Choosing a mode, generating an IV or comparing a MAC by hand designs a protocol, and protocols are hard to get right.

### You inherit the trust of everything that built your code

Thompson showed that a trojaned compiler survives a clean reading of its source. **Every dependency, build step, CI action and base image runs with your privileges.** Advisory asks the questions a new dependency must answer; Always-flag names the defects a build shows.

### Prompt injection is designed around, not filtered out

Greshake et al. showed that **any text an LLM reads can issue instructions** — a retrieved page, a tool's output, an issue body. Willison, the CaMeL authors and the design-patterns authors — three independent groups — agree that no filter reliably stops it. So constrain capability: once an agent has read untrusted text, that text must not be able to trigger a consequential action. Separate control flow, which comes from the trusted user, from data flow, which may come from anyone. **Never let one context hold private data, untrusted content and a way to send data out** — Willison's lethal trifecta.

---

## Always-flag — objective defects

Name each finding by its CWE id and take the fix from the row. ASVS citations are chapter-level and carry the version, because ASVS warns its item ids "may change between versions". OWASP Top 10 categories group findings; a category name is never a finding.

**A row fires only on what the review read.** Where the guard a row asks for can live outside the code read — middleware, a decorator, the router, a gateway, the framework's config — and that place went unread, raise the row as an Advisory question instead. The same holds where the code cannot show who writes a source — a file in the working tree that a cloned repository can carry: raise the trust-boundary question rather than an injection row. **A guard is code that exists to refuse the input.** An earlier call that happens to fail on hostile input is not one, so the row still fires on the sink after it.

### Injection and untrusted input

| Violation | Preferred form | Cite |
|---|---|---|
| SQL, NoSQL or LDAP query built by concatenating or formatting untrusted data | Parameterized query or the driver's builder | CWE-89 (SQL), CWE-90 (LDAP), CWE-943 (other query languages) · v5.0.0 V1 |
| Shell command string built from untrusted data | Argument list, no shell (`subprocess.run([...])`, `execFile`) | CWE-78, CWE-77 · v5.0.0-1.2.5 |
| Untrusted value placed in an argument list where it can be read as an option | End options with `--`, or reject a leading `-` | CWE-88 · v5.0.0 V1 |
| `eval`, `exec`, dynamic import or template compilation on untrusted data | A parser for the data's format; a fixed dispatch table | CWE-94, CWE-95, CWE-1336 · v5.0.0 V1 |
| Untrusted data rendered into HTML or JS without encoding for its context, or auto-escaping turned off | The template engine's auto-escaping; an encoder for the exact context | CWE-79 · v5.0.0 V1, V3 |
| File path built from untrusted input without canonicalising it and checking it stays inside its root | Resolve, then check containment; better, map an id to a path | CWE-22 · v5.0.0 V5 |
| Native deserialisation of untrusted bytes — pickle, unsafe YAML load, Java or .NET binary serialisers | A data-only format (JSON) with a schema; `yaml.safe_load` | CWE-502 · v5.0.0 V1 |
| XML from untrusted input parsed with external entities or DTDs enabled | Disable DTDs and external entities; a hardened parser | CWE-611 · v5.0.0 V1 |
| Server fetches a caller-supplied URL with no destination allow-list | Allow-list hosts and schemes; block private and link-local ranges | CWE-918 · v5.0.0 V1 |
| Redirect to a caller-supplied URL with no allow-list | Redirect to a known path or an id mapped to one | CWE-601 · v5.0.0 V3 |
| Unbounded work from untrusted input — no size, count, depth or time limit; a pattern with nested or overlapping quantifiers (`(a+)+`, `(a\|a)*`), or a quantified class beside a literal the class also matches (`[\w.]*\.`), run on untrusted text of unbounded length | Limits at the boundary; a pattern without nested quantifiers, or a linear-time engine | CWE-770 (no limit), CWE-1333 (the pattern) · v5.0.0 V2 |

### Access control

| Violation | Preferred form | Cite |
|---|---|---|
| Handler or endpoint that changes or reveals data, with no authorization check in the handler, its decorators or the router that mounts it | Check authorization in every handler, deny by default | CWE-862 · v5.0.0 V8 |
| Object loaded by a caller-supplied id with no ownership or tenant check | Scope the lookup to the caller (`WHERE owner_id = :caller`) | CWE-639 · v5.0.0 V8 |
| Critical function reachable without authentication | Authenticate before the function, not inside some of its branches | CWE-306 · v5.0.0 V6 |
| Error, timeout or exception path in a security control — an access check, an authentication step, a guard that keeps an agent from its own oracle — that grants access, skips the check or returns "allow" | Fail closed: an unexpected path denies | CWE-636 · v5.0.0 V16 |
| A guard that checks a path before resolving it — a substring or prefix match that `../`, a symlink or a case change slips past | Resolve the path first — `os.path.realpath`, `Path.resolve()` — then check it | CWE-180 · v5.0.0 V5 |
| A guard that reads its own switch from a source the guarded party can write — a file in the agent's working tree, an environment variable the agent sets | Keep the switch where the guarded party cannot write it | CWE-807 · v5.0.0 V8 |
| Privilege broader than the task — world-writable files, running as root, wildcard scopes, a CI token with `write-all` | The narrowest grant that works, stated where it is granted | CWE-732, CWE-250 · v5.0.0 V13 |

### Secrets, authentication and sessions

| Violation | Preferred form | Cite |
|---|---|---|
| Credential literal in source or committed config: a provider-format key (`AKIA…`, `ghp_…`, `sk-…`), a PEM private-key block, or a password or token assigned outside an example or test file | Load from a secrets manager, or the runtime environment where none exists; rotate the leaked value | CWE-798 · v5.0.0 V13 |
| Secret, token, password or session id written to a log, error message or exception text | Redact at the logger; log an identifier, never the secret | CWE-532, CWE-209 · v5.0.0 V16 |
| Password stored in plain text, reversibly encrypted, or as a single unsalted or un-iterated hash pass (MD5, SHA-*) | Argon2id, scrypt, bcrypt or PBKDF2, salted, via a maintained library | CWE-256, CWE-916 · v5.0.0 V6; NIST 800-63B-4 §3.1.1.2 |
| Password policy NIST forbids — composition rules, forced periodic rotation, truncation, hints, knowledge questions, a maximum below 64 | Minimum length (15 single-factor), a blocklist check, accept the whole password and paste | v5.0.0 V6; NIST 800-63B-4 §3.1.1.2 |
| Login or token check with no rate limit or lockout | Limit failed attempts per account | CWE-307 · v5.0.0 V6; NIST 800-63B-4 §3.2.2 |
| Signed token accepted without verifying its signature, or with the algorithm read from the token (`alg: none`) | Verify against a fixed algorithm and key | CWE-347 · v5.0.0 V9 |
| Session cookie set without `Secure` or `HttpOnly` | Set both, and `SameSite` | CWE-614, CWE-1004 · v5.0.0 V3 |
| Session id not rotated at login | Issue a new session id when privilege changes | CWE-384 · v5.0.0 V7 |
| Cookie-authenticated state change with the framework's CSRF protection disabled or absent | The framework's CSRF protection, or `SameSite=Strict` | CWE-352 · v5.0.0 V3 |

### Cryptography

| Violation | Preferred form | Cite |
|---|---|---|
| Non-cryptographic RNG for a token, key, session id, nonce or reset code | The platform CSPRNG (`secrets`, `crypto.randomBytes`, `SecureRandom`) | CWE-338, CWE-330 · v5.0.0 V11 |
| Hand-rolled cipher, MAC, KDF or protocol; primitives composed by hand where the library offers an authenticated construction | The library's AEAD (AES-GCM, ChaCha20-Poly1305) or a high-level box API | CWE-327 · v5.0.0 V11 |
| Broken or NIST-disallowed algorithm or mode for a security purpose — MD5 or SHA-1 for signatures or integrity an attacker could forge, DES, 3DES, RC4, ECB, RSA below 2048 bits | A current algorithm at a current key size | CWE-327, CWE-328 · v5.0.0 V11 |
| Constant or predictable IV, a reused nonce, or a hard-coded encryption key | Let the library generate the IV or nonce; keys from a key store | CWE-329, CWE-323, CWE-321 · v5.0.0 V11 |
| TLS certificate or hostname verification disabled (`verify=False`, `rejectUnauthorized: false`, `curl -k`, `InsecureSkipVerify`) | Verify; for a private CA, trust that CA explicitly | CWE-295, CWE-297 · v5.0.0 V12 |
| MAC, token or password-hash comparison with ordinary equality | A constant-time compare (`hmac.compare_digest`, `crypto.timingSafeEqual`) | CWE-208 · v5.0.0 V11 |

### Supply chain and build

A pipeline defect that is not a security defect — duplicate pipelines, a tolerated test failure, a deploy that rebuilds — is `ci-pipelines.md`'s, by `PIPE-n` id.

| Violation | Preferred form | Cite |
|---|---|---|
| Code run, or a CA bundle trusted, with no integrity check — `curl … \| sh`, a script or CA bundle fetched at build time, a third-party CI action or base image pinned by a mutable tag | Pin by digest or commit SHA; verify a checksum or signature before running or trusting it | CWE-494 (fetched code, and a CA bundle, which decides what code is trusted), CWE-829 (a CI action or image) · v5.0.0 V15 |
| CI workflow that checks out untrusted code under a privileged trigger (`pull_request_target` running the PR's head) | Run untrusted code without secrets or write tokens | CWE-829 · v5.0.0 V15 |
| Package resolution that lets a public registry answer for an internal package's name — `--extra-index-url` beside a private index, an unscoped internal npm name | One index per name: a scoped name (`@org/…`) bound to the private registry, or a single proxy index that serves internal names first | CWE-427 · v5.0.0 V15 |
| An application's build that installs without its lockfile, or without the lockfile's hashes — `npm install` where `npm ci` would enforce it, a lockfile deleted or git-ignored, requirements exported with `--no-hashes` or `--without-hashes` | Commit the lockfile and install from it, its hashes checked | CWE-1357 · v5.0.0 V15 |

### Agents and hooks

The sinks reuse the rows above; CWE-1427 names the injection itself. OWASP LLM ids carry their year; expect them to change.

| Violation | Preferred form | Cite |
|---|---|---|
| Untrusted text — tool output, file, web page, issue or PR body — inserted into a prompt whose context also holds tools or secrets | Read it in a context with no tools (Dual LLM); fix the plan before reading it (Plan-Then-Execute) | CWE-1427 · LLM01:2025 |
| Untrusted text written into a file a model later loads as instructions — `CLAUDE.md`, `AGENTS.md`, a skill, a rule — where every later session reads it as the developer's | Render it as inert data — an allow-listed character set, a length cap, no newlines, backticks or marker text — or keep it out and record only ids | CWE-1427 · LLM01:2025 |
| Model output passed to a shell, SQL, `eval`, HTML or a file path without the treatment untrusted input gets | Treat model output as untrusted input: the injection rows above apply | CWE-78, CWE-94, CWE-79, CWE-22 · LLM05:2025 |
| One agent context holds private data, untrusted content and an outbound channel — network, email, a public write, a rendered image URL | Remove one leg of the trifecta, and name the design pattern that removes it: Action-Selector, Plan-Then-Execute, LLM Map-Reduce, Dual LLM, Code-Then-Execute or Context-Minimization | CWE-1427 · LLM01, LLM02, LLM06:2025 |
| Code that starts an agent or registers a hook with tools beyond its task — bare shell, any-path write, network — including a subagent definition that narrows a shell with a command pattern such as `Bash(git log:*)`, which grants the whole shell | Only the tools the task needs; a shell or a write bounded by a hook that allows its exact commands or paths and refuses the rest | CWE-250 · LLM06:2025 |
| Secret or credential placed in a system prompt or agent instructions | Keep secrets in the tool's runtime, out of the model's context | CWE-798 · LLM07:2025 |
| Agent loop with no step, token, time or cost bound | A hard bound that stops the loop and reports | CWE-770 · LLM10:2025 |

**A command pattern in a subagent's `tools` picks the tool, not the command.** Measured on Claude Code 2.1.305, 2026-10-20: a subagent granted only `Bash(echo:*)` wrote files through `touch`, a redirect, `&&` and `$( )` in bypass mode, while a `PreToolUse` hook keyed on the payload's `agent_type` refused all four. A pattern in a slash command's `allowed-tools` was not measured; this row does not reach it.

Checked against CWE 4.20 (2026-04-30), OWASP ASVS 5.0.0, NIST SP 800-63B-4 (2025-07-31) and the OWASP Top 10 for LLM Applications 2025, on 2026-10-20. Every CWE id above resolved in MITRE's CWE database that day.

---

## Advisory — judgment calls, not hard blocks

A reviewer raises these; the author decides. Each needs context the diff lacks.

- **A new trust boundary** — a new endpoint, input source, tool, or hook that reads external text — with no answer to Shostack's "what can go wrong?"
- **A new dependency.** Is it needed at all? Is the name the authentic project, not a lookalike one edit from a popular one? Does more than one person maintain it (CWE-1104)? (OpenSSF *Concise Guide for Evaluating Open Source Software*; the event-stream, dependency-confusion and xz-utils incidents.)
- **A new dependency that runs code at install** — an npm `preinstall` or `postinstall` script, a Python package built from source at install. It runs with the developer's and CI's privileges before any test does (CWE-829).
- **A binary committed** where the build could produce it from source — nobody reviews what a binary does.
- **Validation scattered through layers** instead of once at the boundary, or a security-relevant value passed as a bare string where a domain primitive would hold its invariants.
- **A deny-list** where an allow-list is feasible.
- **An authentication or authorization decision with no audit record.**
- **Detail in a user-facing error** beyond what the user can act on.
- **A shell invoked on a constant string** where an argument list would do — safe today, one edit from CWE-78.
- **Secrets in environment variables** where a secrets manager is available. Twelve-Factor's test — could you publish this code now without leaking a credential? — governs separation from code; it does not make the environment a vault.
- **A verbatim transcript written to disk** — prompts, replies or tool output kept for a later session. It holds whatever was pasted in, which no code can know: write it `0600`, outside the repository, or redacted (CWE-312).
- **Security code too intricate to review** — economy of mechanism.
- **Version ranges against exact pins.** A library declares ranges and lets the application's lockfile pin; an application pins exactly. Always-flag covers mutable CI and image tags.
- **A missing security header** — `Content-Security-Policy`, `frame-ancestors` — on a new HTML surface.
- **A vulnerable dependency a scanner flagged** (CWE-1395), when the change or its author cites the finding and the vulnerable code is unreachable. Triage reachability before demanding the upgrade.

## Do not flag

- **MD5 or SHA-1 for a non-security purpose** — a cache key, deduplication, an ETag, a git object id.
- **A non-cryptographic RNG for non-security work** — shuffling, jitter, sampling, test data.
- **Placeholders and test credentials** — `.env.example`, `password123` in a login test, a documented example key. Flag only a value that could authenticate somewhere.
- **A query or command built from constants or a closed set.** The injection rows need untrusted data to reach the sink.
- **No authorization on a deliberately public route** — a health check, static assets, the login endpoint itself.
- **No validation on an internal call that crosses no trust boundary.** Validate at the boundary; demanding it at every layer adds noise, not safety.
- **The absence of composition rules, forced rotation or a short maximum** — NIST forbids them. A project that must keep a stricter policy says so beside the policy, citing the authority that requires it.
- **Paste and password-manager support** — NIST requires allowing it.
- **Unpublished internals as "security through obscurity".** Open design forbids *relying* on secrecy; it does not require publishing.
- **The absence of a prompt-injection detector or guardrail.** Flag the trifecta or the grant instead; the evidence says filters fail.
- **An OWASP Top 10 category as a finding.** "This is A05" names no defect; name the CWE and the line.
- **TLS verification turned off in a test against a local or loopback server.**
- **A gate that enforces a standard rather than a security property, and fails open by stated design** — a word-count or lint hook. CWE-636 is about security controls.
- **`dangerouslySetInnerHTML` on content that never crossed a trust boundary** — `react.md`'s idiom. When untrusted data reaches it, file CWE-79 once, citing `react.md`.

---

## Review Checklist

- [ ] Where does untrusted data enter this change, and does it become a type before it travels inward?
- [ ] Does any untrusted value — model output included — reach a query, shell, `eval`, template, path or URL fetch?
- [ ] Does every handler check authorization for this caller and this object, and does every unexpected path deny?
- [ ] Is there a secret in the source, a log line or a prompt?
- [ ] Is any cryptography composed by hand, or any random value for a secret drawn from a non-cryptographic RNG?
- [ ] Does anything run code it fetched without checking its integrity?
- [ ] Is each grant — file mode, IAM scope, CI token, agent tool — the narrowest that works?
- [ ] Does any agent context hold private data, untrusted content and a way out, all at once?
- [ ] Did I name each finding by CWE id, and leave every Do-not-flag case alone?

---

## Anti-Patterns to Avoid

Each anti-pattern restates an Always-flag row or an Advisory bullet; file a finding under that row or bullet, never under the name here.

| Anti-pattern | Fix |
|---|---|
| **Sanitize everywhere** — escaping input on the way in, again in each layer | Validate once at the boundary; encode once at the sink, for its context |
| **The deny-list** — refusing the bad characters you thought of | Allow-list the good ones |
| **Fail-open error handling** — `except: return True` | An unexpected path denies |
| **The bolted-on check** — authorization added to the handlers someone remembered | Deny by default, so a forgotten handler is closed, not open |
| **Home-grown crypto** | The library's authenticated construction, with its defaults |
| **Trusting the model** — treating its output as the developer's | Model output is untrusted input |
| **The guardrail as defence** — a classifier between the agent and the injection | Remove a leg of the trifecta; narrow the grant |
| **Scanner as verdict** — fixing every finding, or none | Triage by reachability and by the Do-not-flag list |
| **Category as finding** — "OWASP A01" in a review | The CWE id, the line and the fix |

---

## Sources and Synthesis

The Principles half quotes or paraphrases these works, citing each by title: Saltzer and Schroeder for the eight principles, Smith for which survived, *Secure by Design* for domain primitives and the validation order, Shostack for the four questions, Kohnfelder for STRIDE, *Building Secure and Reliable Systems* for safe-by-construction APIs, Thompson for inherited trust, Greshake, Willison and the two 2025 papers for prompt injection, Birsan's 2021 dependency-confusion disclosure for the package-resolution row. Hoffman and Madden shaped no row: they are named as the current books on web applications and APIs, the ground the injection, access-control and session rows cover, and the rule knows them from their publishers' descriptions only. **Three things are this rule's own:** the choice and wording of the always-flag rows, which the research distilled from CWE, ASVS and the Cheat Sheets rather than copied from any one; the split into Always-flag, Advisory and Do not flag, which follows `ux.md`; and the reading that reconciles Smith's "obsolete" complete mediation with OWASP's per-request check. This rule draws on the research document, not on the books in hand; its quotations rest on the sources the research reached, and the research lists what it could not open under Knowledge Gaps. **Two claims come from knowledge of the books, not from the research:** *Secure by Design*'s validation order and STRIDE's six threats. Check those two against a copy first.

---

## The Mantra

> **Validate at the boundary, grant the least that works, fail closed, never compose crypto, and treat every byte you did not write — model output included — as an attacker's.**
