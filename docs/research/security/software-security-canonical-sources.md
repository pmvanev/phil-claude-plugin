# Research: Canonical Software Security Works for a Vendor-Neutral Secure-Coding Rule

**Date**: 2026-10-20 | **Researcher**: nw-researcher (Nova) | **Confidence**: High for the spine and the always-flag list; Medium for edition dates and the agent standards | **Sources**: 48

> Input to a future `rules/security.md` with two halves: **Principles** (book-extracted, design/process)
> and an **always-flag reviewer table** (objective, diff-checkable defects, each citing a standard id).
> Each finding uses: **Work** / **Evidence** / **Canonicity** / **Contributes** / **Checkable in a diff?** / **Caveats**.
> Access date for every web source: 2026-10-20 unless stated.

## Executive Summary

Secure-coding guidance splits along the line this repo already draws. **Durable principles** come from a
few named works: Saltzer & Schroeder's 1975 paper (least privilege, fail-safe defaults, complete
mediation, open design; 1,431 Crossref citations), restated by NIST SP 800-160 and triaged by Smith
(2012); *Secure by Design* (Johnsson, Deogun, Sawano 2019), which treats security as a property of domain
design; Shostack's *Threat Modeling* (2014; a 2nd edition is announced for late 2026 or 2027);
Kohnfelder's *Designing Secure Software* (2021); and Google's *Building Secure and Reliable Systems*
(2020). Thompson's "Reflections on Trusting Trust" (1984) supplies the supply-chain principle in one
idea. These belong in the rule's Principles half; almost none of their content can be checked in a diff.

**Flaggable defects** come from versioned standards with item ids. CWE is the identifier space every
other standard maps into and should key every row; OWASP ASVS 5.0.0 (May 2025, 17 chapters, ids such as
`v5.0.0-1.2.5`) supplies testable requirements; the OWASP Cheat Sheet Series supplies the preferred fix;
NIST SP 800-63B-4 (July 2025) supplies password rules as SHALL/SHALL NOT, and also removes common false
flags (composition rules, forced rotation). OWASP Top 10:2025 is useful only for grouping: it calls itself
an awareness document, and its ids change with each edition. Thirty language-agnostic always-flag rows
emerge, from string-built queries and shell commands through fail-open error paths (A10:2025, CWE-636)
to disabled TLS verification and mutable-tag CI dependencies.

For agent and hook code, the indirect-prompt-injection paper (Greshake et al., AISec 2023, 650 Crossref
citations), Willison's "lethal trifecta" (2025), the CaMeL paper and the six-pattern design paper (both
2025) agree on one point: injection cannot be reliably filtered, only designed around. That yields six
agent rows keyed to OWASP LLM Top 10 2025 and to CWE-1427 (added in CWE 4.16, Nov 2024). Two of them —
narrow tool grants and no private-data/untrusted-input/exfiltration triple — restate for agents what this
repo already enforces for commands. Main caveats: ASVS item texts, several release dates and the Agentic
Top 10's primary page were not confirmed; see Knowledge Gaps.

## Research Methodology
**Search Strategy**: Primary sources first — standards bodies' own pages (owasp.org, cwe.mitre.org,
csrc.nist.gov, slsa.dev, openssf.org), publisher pages for bibliographic facts, arXiv and Crossref for
papers. Crossref's `is-referenced-by-count` gave citation counts where a DOI existed; no count was guessed.
**Source Selection**: Types: academic, official, technical docs, publishers; vendor blogs used only to
corroborate or to date, and marked medium. **Verification**: Each principle cross-referenced across
independent author groups (e.g. input distrust across four book author groups; prompt-injection-by-design
across Willison, Google DeepMind/ETH, and a 14-author multi-institution paper).
**Quality Standards**: Target 3 sources per major claim, 1 authoritative minimum; unconfirmed facts are
marked in place and collected in Knowledge Gaps.

---

## Findings

## 1. Secure design principles

### 1.1 Saltzer & Schroeder, "The Protection of Information in Computer Systems" (1975)

**Work**: Jerome H. Saltzer and Michael D. Schroeder. *Proceedings of the IEEE* 63(9): 1278–1308, 1975.
DOI 10.1109/PROC.1975.9939. An earlier version appeared in *CACM* 17(7), July 1974, from SOSP 1973.
Open copy: https://www.cs.virginia.edu/~evans/cs551/saltzer/ (UVA, high).
**Evidence**: The paper names eight design principles, quoted from the UVA copy:
(a) economy of mechanism, "Keep the design as simple and small as possible"; (b) fail-safe defaults, "Base
access decisions on permission rather than exclusion"; (c) complete mediation, "Every access to every
object must be checked for authority"; (d) open design, "The design should not be secret"; (e)
separation of privilege, "a protection mechanism that requires two keys to unlock it is more robust and
flexible"; (f) least privilege, "Every program and every user of the system should operate using the
least set of privileges"; (g) least common mechanism; (h) psychological acceptability. It adds two that
"apply only imperfectly to computer systems": work factor and compromise recording.
**Canonicity**: Crossref is-referenced-by-count **1,431** (queried 2026-10-20; Crossref undercounts
pre-1990 work relative to Google Scholar, which was not queried). Every later principle list restates it:
Smith 2012, NIST SP 800-160 / SP 800-53 SA-8, and the Wikipedia article, which calls it "seminal".
**Contributes**: The vocabulary of the rule's Principles half. Three principles turn into flaggable code
patterns: fail-safe defaults (an allow-list, or a `default: allow` / catch-all that grants access),
complete mediation (an endpoint or handler with no authorization check, or a cached authorization
decision reused across objects), and least privilege (a broad scope, root, `chmod 777`, wildcard IAM).
**Checkable in a diff?** Partly. Fail-safe defaults, complete mediation and least privilege leave marks in
code. Economy of mechanism, open design, separation of privilege, least common mechanism and
psychological acceptability are design judgments.
**Caveats**: The 1975 wording targets multi-user operating systems. Read "complete mediation" for a web
service as "every request, every object" — the root of CWE-862 / CWE-639 (IDOR).

### 1.2 Smith, "A Contemporary Look at Saltzer and Schroeder's 1975 Design Principles" (2012)

**Work**: Richard E. Smith. *IEEE Security & Privacy* 10(6): 20–25, Nov–Dec 2012. DOI 10.1109/MSP.2012.85.
Author's extended preprint: https://cryptosmith.com/2013/10/19/security-design-principles/ (named author
self-hosting his IEEE paper; medium-high, cross-checked against the Wikipedia citation and the Imperial
College reading-list copy).
**Evidence**: Smith sorts the principles by fate. Thrived: least privilege ("Almost every textbook
recognizes the principle of least privilege"), separation of privilege ("still widely recognized"),
fail-safe defaults (as "Deny by Default"), open design, compromise recording ("an essential feature of
every secure system"). Faded: complete mediation, "a sensible but obsolete view of security decision
making" once access control spread across platforms; psychological acceptability, "honored more in the
breach than in the observance"; economy of mechanism, "There is no real market for simplicity in modern
computing." His 2016 textbook adds a ninth principle: "Trust, but verify."
**Canonicity**: Column in *IEEE Security & Privacy* magazine; Crossref is-referenced-by-count **24**
(2026-10-20). Modest reach; useful as triage, not as a spine.
**Contributes**: The caveat the rule needs. A principles section that recites all eight equally overstates
what practice kept; Smith supplies the triage.
**Checkable in a diff?** No; it is commentary on principles.
**Caveats / conflict**: Smith's "complete mediation is obsolete" conflicts with OWASP Top 10 A01 and ASVS,
which treat a missing per-request check as the most common web flaw. Read Smith as saying a *single
central* reference monitor is obsolete, not that per-access checks are. See Conflicting Information.

### 1.3 NIST SP 800-160 Vol. 1 Rev. 1, *Engineering Trustworthy Secure Systems* (2022)

**Work**: Ron Ross (NIST), Mark Winstead and Michael McEvilley (MITRE). NIST SP 800-160 Vol. 1 Rev. 1,
November 2022 (final 2022-11-16; supersedes the 2018 edition). https://csrc.nist.gov/pubs/sp/800/160/v1/r1/final
(official, high).
**Evidence**: The abstract offers "principles, concepts, activities, and tasks" for engineering
trustworthy secure systems "regardless of its purpose, scope, size, complexity, or life-cycle stage". NIST's
2022 announcement says the revision "streamlines the design principles ... eliminating the two previous
design principle categories". A secondary site says it expands Saltzer & Schroeder into roughly 33
principles mirrored as SP 800-53 Rev. 5 control SA-8 enhancements — **count not confirmed against the PDF**.
**Canonicity**: US federal standard; the design-principle list in SA-8 is used by every FedRAMP / FISMA
assessment. It is the government's restatement of Saltzer & Schroeder.
**Contributes**: An authoritative, citable modern list of principles (least privilege, minimized trusted
elements, defense in depth, secure defaults, secure failure and recovery, trusted communication channels).
**Checkable in a diff?** No. Systems-engineering process; useful only as a principles citation.
**Caveats**: Written for systems engineers of large programmes; heavy for a code reviewer. Cite it as
corroboration, not as the spine.

## 2. Books

Bibliographic facts come from publisher pages (manning.com, nostarch.com, sre.google, schneier.com for
Wiley titles, oreilly.com for Pearson / McGraw-Hill / Microsoft Press titles) or the author's own page.
No citation counts were retrievable; every "citations" cell reads **not found** rather than a guess.

### 2.1 Summary table

| # | Work | Edition / year (verified) | Canonicity signal | Contributes to | Checkable in a diff? |
|---|---|---|---|---|---|
| B1 | Johnsson, Deogun, Sawano, *Secure by Design* (Manning) | 1st, Sept 2019, 400 pp. | Foreword by Daniel Terhorst-North; the only DDD-native security book; bridges `coding.md`'s domain modeling | Domain primitives, secure validation order, safe error handling, security as a by-product of design | **Yes, partly**: primitive obsession on security-relevant values, validation after use, exceptions leaking data |
| B2 | Kohnfelder, *Designing Secure Software* (No Starch) | 1st, Nov 2021, 312 pp. | Author co-created STRIDE with Praerit Garg ("The Threats to our Products", Microsoft *Interface*, 1999-04-01) | Threats, mitigations, patterns; Part III "Untrusted Input", "Low-Level Coding Flaws", "Web Security"; design-review method | **Mixed**: Part III is diff-checkable; Parts I–II are design |
| B3 | Shostack, *Threat Modeling: Designing for Security* (Wiley) | 1st, 2014; **2nd ed. announced** ("...in an AI World", ISBN 978-1-394-41332-4, 624 pp., listed for 2026-12-22 or 2027, unconfirmed) | Source of the Four-Question Framework; STRIDE's main expositor; Shostack led Microsoft SDL threat-modeling tools | Four questions; STRIDE per element; trust boundaries in data-flow diagrams | **No**: design/process. Supplies "trust boundary" vocabulary the flag table uses |
| B4 | Anderson, *Security Engineering* (Wiley) | 3rd, 2020 (serialized 2019-04 to 2020-09), ISBN 978-1-119-64278-7; free PDFs on the author's Cambridge page | Three editions (2001, 2008, 2020); the field's standard reference text | Economics, psychology, protocols, failure case studies; why systems fail | **No**: breadth reference, not a checklist |
| B5 | McGraw, *Software Security: Building Security In* (Addison-Wesley) | 2006 (one catalog says 2007; unconfirmed) | McGraw co-founded BSIMM; the "seven touchpoints" are a standard SDL vocabulary | Touchpoints ranked by effectiveness: code review (with a tool) and architectural risk analysis first | **No**: process; justifies the review itself |
| B6 | Howard & LeBlanc, *Writing Secure Code* (Microsoft Press) | 2nd, 2002/2003 (sources disagree) | Basis of Microsoft's Trustworthy Computing push and SDL; chapter "All Input Is Evil!" | Input distrust; least privilege; canonicalization; DoS; secure defaults | **Yes** for its coding chapters; dated (Win32/C-heavy) |
| B7 | Howard, LeBlanc, Viega, *24 Deadly Sins of Software Security* (McGraw-Hill) | 2010 (not 2009), ISBN 978-0-07-162675-0; successor to *19 Deadly Sins* (2005) | IEEE Cipher reviewed both editions | A ready-made defect list: SQL/command injection, buffer overruns, format strings, integer overflow, exception handling, too much privilege, information leakage, weak passwords, weak random numbers, crypto misuse, PKI misuse, unprotected traffic, trusting name resolution, race conditions | **Yes**: closest book to an always-flag table; each sin maps to CWE ids |
| B8 | Seacord, *Secure Coding in C and C++* (Addison-Wesley, SEI Series) | 2nd, April 2013, ISBN 978-0-321-82213-0 | Author led CERT secure coding at SEI/CMU; companion to the CERT C standard | Strings, dynamic memory, integer security, formatted output, concurrency | **Yes**, for C/C++ only; cite via CERT standard ids rather than the book |
| B9 | Ferguson, Schneier, Kohno, *Cryptography Engineering* (Wiley) | 2010 (March), ISBN 978-0-470-47424-2, 384 pp.; revises *Practical Cryptography* (2003) | Three named authorities; standard engineering text | Use vetted primitives and protocols; never design your own; secure channel construction; randomness | **Partly**: home-grown crypto, ECB, unauthenticated encryption |
| B10 | Adkins, Beyer, Blankinship, Oprea, Lewandowski, Stubblefield, *Building Secure and Reliable Systems* (O'Reilly / Google) | 1st, March 2020, 555 pp.; free online at sre.google | Google SRE series; vendor-authored but vendor-neutral in content | Least privilege, design for understandability, safe-by-construction APIs ("make the safe thing the easy thing"), code review, recovery | **Partly**: safe-API and least-privilege items show in diffs |
| B11 | Zalewski, *The Tangled Web* (No Starch) | 1st, Nov 2011, 320 pp. | Author of AFL; standard text on browser security model | Same-origin policy, content-type sniffing, framing, URL parsing quirks | **Partly**; dated (pre-CSP-3, pre-SameSite) |

### 2.2 Books not on the original list

| # | Work | Verified facts | Why consider it |
|---|---|---|---|
| B12 | Dowd, McDonald, Schuh, *The Art of Software Security Assessment* (Addison-Wesley) | Nov 2006 per O'Reilly (IEEE Cipher says 2007), ~1,200 pp. | The code-auditing reference; a reviewer's book rather than a designer's. Reception mixed (Dr. Dobb's review grew "disappointed"). |
| B13 | Aumasson, *Serious Cryptography* (No Starch) | 2nd ed., Aug 2024, 376 pp. | Current; "Each chapter includes a discussion of common implementation mistakes using real-world examples" — directly feeds crypto flags. Fresher than B9. |
| B14 | Madden, *API Security in Action* (Manning) | Nov 2020, 576 pp. | Authentication, authorization, audit logging, rate limiting, tokens and capability security for APIs; fills B1's gap on authn/authz. |
| B15 | Shostack, *Threats: What Every Engineer Should Learn from Star Wars* (Wiley, 2023) | **Not verified this session** | Shostack's developer-facing restatement of STRIDE. |
| B16 | Viega & McGraw, *Building Secure Software* (Addison-Wesley, 2001) | **Not verified this session** | First book-length statement of ten secure-design principles for developers; largely superseded. |
| B17 | Hoffman, *Web Application Security*, 2nd ed. (O'Reilly) | Jan 2024 (ebook 2024-01-17), 444 pp.; O'Reilly's search listing, corroborated by Helion (O'Reilly's Polish partner). Print and ebook ISBNs differ (978-1-098-14392-3 / 978-1-098-14389-3). Added 2026-10-20 after the main pass. | The only current web-security book found: reconnaissance, offense and defense, now with GraphQL, cloud deployments, CDNs and server-side rendering. Replaces B11 (2011) as the web book to name. Canonicity: newer and less cited than B11; contents not read. |

### 2.3 What the books agree on (interpretation, cross-referenced)

- **Distrust input at a trust boundary and validate it before use.** B2 (Ch. 10 "Untrusted Input"), B6
  ("All Input Is Evil!"), B7 (the injection sins), B1 (secure validation, domain primitives). Four
  independent author groups. Confidence: High.
- **Least privilege and deny-by-default.** Saltzer & Schroeder, Smith 2012, B7 ("executing code with too
  much privilege"), B10. Confidence: High.
- **Do not invent cryptography; use vetted, high-level constructions.** B9, B13, B7 ("using cryptography
  incorrectly"). Confidence: High.
- **Threat modeling is a design practice, not a code check.** B3, B2 Part II, B5's "architectural risk
  analysis". It belongs in the Principles half. Confidence: High.
- **Security is a design property** — B1's thesis ("good design can be the best form of security",
  reviewer quote on the Manning page) and B10's safe-by-construction APIs. This is the bridge to `coding.md`
  and `architecture.md`. Confidence: Medium (two sources; the claim is a stance, not a measurement).

## 3. Untrusted input, injection and web — standards

### 3.1 CWE (Common Weakness Enumeration) and the CWE Top 25

**Work**: MITRE / CISA. *2025 CWE Top 25 Most Dangerous Software Weaknesses*.
https://cwe.mitre.org/top25/archive/2025/2025_cwe_top25.html (official, high). Page last updated
2025-12-15; the index page (updated 2026-01-29) names 2025 as the latest list. Exact release date and
CVE data window: **not stated on the pages read**.
**Evidence**: The 2025 list, rank / id: 1 CWE-79 XSS · 2 CWE-89 SQL injection · 3 CWE-352 CSRF ·
4 CWE-862 Missing Authorization · 5 CWE-787 Out-of-bounds Write · 6 CWE-22 Path Traversal · 7 CWE-416
Use After Free · 8 CWE-125 Out-of-bounds Read · 9 CWE-78 OS Command Injection · 10 CWE-94 Code
Injection · 11 CWE-120 Classic Buffer Overflow · 12 CWE-434 Unrestricted Upload of Dangerous File Type ·
13 CWE-476 NULL Pointer Dereference · 14 CWE-121 Stack Buffer Overflow · 15 CWE-502 Deserialization of
Untrusted Data · 16 CWE-122 Heap Buffer Overflow · 17 CWE-863 Incorrect Authorization · 18 CWE-20
Improper Input Validation · 19 CWE-284 Improper Access Control · 20 CWE-200 Exposure of Sensitive
Information · 21 CWE-306 Missing Authentication for Critical Function · 22 CWE-918 SSRF · 23 CWE-77
Command Injection · 24 CWE-639 Authorization Bypass Through User-Controlled Key · 25 CWE-770 Allocation
of Resources Without Limits or Throttling.
**Canonicity**: CWE is the identifier space every other standard maps into — OWASP Top 10 categories are
defined as CWE groups, ASVS and CERT rules cross-reference CWE, and NVD tags CVEs with CWE ids. Annual
list, co-published with CISA.
**Contributes**: **The id scheme for the always-flag table.** A CWE id is stable across years; the Top 25
*ranking* is not.
**Checkable in a diff?** Mostly yes. Base-level weaknesses (CWE-89, -78, -22, -502, -918, -798, -327)
show in code. Class-level ones (CWE-20, -284, -200) are too broad to flag alone; the table should cite the
specific child.
**Caveats**: Ranking blends frequency and CVSS severity across reported CVEs; it over-weights memory
safety for memory-safe languages and under-weights logic flaws that rarely get CVEs. Cite CWE ids, not
ranks.

### 3.2 OWASP Top 10:2025

**Work**: OWASP Foundation. *OWASP Top 10:2025*. https://top10.owasp.org/2025/ (redirect target of
owasp.org/Top10; standards body, high). Page copyright 2021–2025. **Final release date not confirmed**:
a GitLab blog of 2026-01-07 still called it a release candidate with "no changes to the top 10 list
itself" expected.
**Evidence**: A01 Broken Access Control · A02 Security Misconfiguration · A03 Software Supply Chain
Failures · A04 Cryptographic Failures · A05 Injection · A06 Insecure Design · A07 Authentication
Failures · A08 Software or Data Integrity Failures · A09 Security Logging and Alerting Failures · A10
Mishandling of Exceptional Conditions. Secondary sources (GitLab, Outpost24, Qualys — industry,
medium) agree that SSRF folded into A01, A03 widens 2021's "Vulnerable and Outdated Components" to
builds and distribution, and A10 is new, covering error handling and "failing open".
**Canonicity**: Eighth edition since 2003 (editions 2003, 2004, 2007, 2010, 2013, 2017, 2021, 2025 —
from the researcher's prior knowledge, **not re-verified this session**). Widely named in compliance
regimes such as PCI DSS (not re-verified). The most widely recognised name in application security.
**Contributes**: Category names the rule can use as headings. A10:2025 gives a standard citation for
fail-open error handling — Saltzer & Schroeder's fail-safe defaults restated for code.
**Checkable in a diff?** No, not at category level — each category is a bundle of CWEs. Flag by CWE, group
by Top 10 category.
**Caveats**: OWASP calls it an awareness document, not a standard; ASVS is the verifiable standard. Ids
carry the year (A01:2025) and change every edition, so they date.

### 3.3 OWASP ASVS 5.0.0

**Work**: OWASP Foundation. *Application Security Verification Standard* 5.0.0.
https://owasp.org/www-project-application-security-verification-standard/ ; source at
https://github.com/OWASP/ASVS/tree/master/5.0/en (standards body, high). Marked "stable". Released May
2025; launch reported as 2025-05-30 at Global AppSec EU Barcelona (appknox.com, vendor glossary, medium —
date not confirmed on owasp.org).
**Evidence**: Seventeen chapters: V1 Encoding and Sanitization · V2 Validation and Business Logic ·
V3 Web Frontend Security · V4 API and Web Service · V5 File Handling · V6 Authentication · V7 Session
Management · V8 Authorization · V9 Self-contained Tokens · V10 OAuth and OIDC · V11 Cryptography ·
V12 Secure Communication · V13 Configuration · V14 Data Protection · V15 Secure Coding and Architecture ·
V16 Security Logging and Error Handling · V17 WebRTC. Identifier scheme, quoted: it is "preferable for
other documents, reports, or tools to use the following format" `v<version>-<chapter>.<section>.<requirement>`,
e.g. `v5.0.0-1.2.5` (OS command injection), and "the identifiers may change between versions of the
standard". Three levels (L1–L3) of increasing rigour.
**Canonicity**: OWASP flagship project for verifiable requirements. Prior major versions (4.0 in 2019,
4.0.3 in 2021) are from prior knowledge, **not re-verified this session**.
**Contributes**: **The second id column of the always-flag table.** ASVS items are written as testable
requirements, which is what a reviewer needs. 5.0 renumbered the chapters (V1 was Architecture in 4.0 — prior knowledge, not re-verified),
so ids must carry `v5.0.0-`.
**Checkable in a diff?** Many L1 items yes (parameterized queries, output encoding, no secrets in code,
cookie flags). Architecture and configuration items need context.
**Caveats**: Web-application oriented; agent and CLI code fit V1, V2, V5, V11, V13, V15 and V16 best.
Individual item texts were not read this session beyond 1.2.5; each id in the table should be checked
against the 5.0.0 text before the rule ships.

### 3.4 OWASP Cheat Sheet Series

**Work**: OWASP. https://cheatsheetseries.owasp.org/ (standards body, high). Living document; no
version.
**Evidence**: "a concise collection of high value information on specific application security topics".
Relevant sheets present on the index: Input Validation; Injection Prevention; Query Parameterization;
Cross Site Scripting Prevention; DOM based XSS Prevention; Password Storage; Secrets Management;
Cryptographic Storage; Deserialization; Server Side Request Forgery Prevention; Logging; LLM Prompt
Injection Prevention; NPM Security; Vulnerable Dependency Management; Software Supply Chain Security.
**Contributes**: The "preferred form" column — the fix a reviewer names (parameterize; encode for the
output context; argon2id/scrypt/bcrypt; a secrets manager).
**Checkable in a diff?** Yes; it is written at code level.
**Caveats**: Unversioned and edited continuously; cite by sheet title, as the repo cites books by title.

### 3.5 SEI CERT Coding Standards

**Work**: Software Engineering Institute, Carnegie Mellon University. SEI CERT C, C++, Oracle Java, Perl
(and Android) coding standards. https://wiki.sei.cmu.edu/confluence/ (academic/official, high).
**Evidence**: Identifiers are a three-letter category, two digits and a language suffix (`-C`, `-CPP`,
`-J`, `-PL`). For C and Java, 00–29 are recommendations and 30–99 rules; C++ uses 00–49 / 50–99
(SEI wiki "How this Coding Standard is Organized").
**Canonicity**: The C standard has print editions (2008, 2016); Seacord's book (B8) is its companion;
static analysers map to it.
**Contributes**: Language-specific rule ids for the `cpp.md` / `python.md`-style language rules, not for
the language-neutral table.
**Checkable in a diff?** Yes; rules are written to be machine-checkable.
**Caveats**: No Python, TypeScript, Go or shell standard. Out of scope for a vendor-neutral, cross-language
rule except as a pointer from `cpp.md`.

## 4. Secrets, authentication, authorization and session

### 4.1 NIST SP 800-63B-4, *Digital Identity Guidelines: Authentication and Authenticator Management*

**Work**: Temoshok, Fenton, Choong, Lefkovitz, Regenscheid, Galluzzo, Richer. NIST SP 800-63B-4, final
2025-07-31 (dated July 2025); supersedes SP 800-63B (2017, updated 2020-03-02).
https://csrc.nist.gov/pubs/sp/800/63/b/4/final ; text at https://pages.nist.gov/800-63-4/sp800-63b.html
(official, high).
**Evidence** (Sec. 3.1.1, passwords): "a minimum of 15 characters" for single-factor passwords, eight if
used only within MFA; SHOULD accept "a maximum password length of at least 64 characters"; "Other
composition requirements for passwords SHALL NOT be imposed"; "SHALL NOT require subscribers to change
passwords periodically" (forced change only on evidence of compromise); "compare the prospective secret
against a blocklist"; "SHALL NOT permit the subscriber to store a hint"; no knowledge-based questions;
"SHALL verify the entire submitted password" (no truncation); "Verifiers SHALL allow the use of password
managers and autofill functionality"; "a rate-limiting mechanism that effectively limits the number of
failed authentication attempts" (Sec. 3.2.2: at most 100 consecutive failures); store passwords salted
and hashed "using a suitable password hashing scheme", salt at least 32 bits.
**Canonicity**: US federal standard; the reference other standards (ASVS V6) align password rules to.
Revision 4 is the current one.
**Contributes**: The most diff-checkable authentication rules in any standard: a composition regex, a
forced-rotation timer, a `maxlength` under 64, truncation, a missing rate limit, a fast unsalted hash.
**Checkable in a diff?** Yes, for the items above.
**Caveats / conflict**: Rev. 4 raised single-factor minimum length from 8 to 15. Organisations' legacy
policies (composition rules, 90-day rotation) contradict it; the standard wins. See Conflicting Information.

### 4.2 OWASP ASVS 5.0.0 chapters V6 Authentication, V7 Session Management, V8 Authorization, V9 Self-contained Tokens, V10 OAuth and OIDC

See 3.3 for the citation. These chapters carry the verifiable requirements for authn, sessions,
authorization and tokens; the always-flag table cites them alongside CWE-287 / -306 / -384 / -613 /
-862 / -863 / -639 / -347. Item texts **not read this session**; confirm each id before shipping.

### 4.3 The Twelve-Factor App, "III. Config"

**Work**: Adam Wiggins et al. (Heroku), *The Twelve-Factor App*, https://12factor.net/config (listed
industry_leaders, medium-high). Undated web text, c. 2011.
**Evidence**: "The twelve-factor app stores config in environment variables." Litmus test: whether "the
codebase could be made open source at any moment, without compromising any credentials."
**Canonicity**: Widely adopted cloud-native methodology; `continuous-delivery.md` territory.
**Contributes**: The best one-sentence test for a hard-coded secret (CWE-798): would publishing this file
leak a credential?
**Checkable in a diff?** Yes — a credential literal in source or committed config.
**Caveats / conflict**: Environment variables are not a secrets store. The OWASP Secrets Management Cheat
Sheet prefers a dedicated secrets manager; environment variables leak through process listings, crash
dumps and child processes. Cite 12-Factor for *separation from code*, not for *storage*.

### 4.4 Authorization (from sources already cited)

Missing or incorrect authorization ranks 4th (CWE-862), 17th (CWE-863), 19th (CWE-284) and 24th
(CWE-639, IDOR) in the 2025 Top 25, and heads OWASP Top 10:2025 as A01. Saltzer & Schroeder's complete
mediation and fail-safe defaults are the principles behind it. Confidence: High (three independent
sources: MITRE/CISA, OWASP, Saltzer & Schroeder).

## 5. Cryptography use

The rule needs to tell a reviewer what crypto *misuse* looks like, not how ciphers work. Four source
types agree on a short list.

### 5.1 OWASP Cryptographic Storage Cheat Sheet

**Work**: OWASP. https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html
(standards body, high). Unversioned.
**Evidence**: "AES with a key that's at least 128 bits (ideally 256 bits)"; GCM and CCM "should be used
as a first preference"; "ECB should not be used outside of very specific circumstances"; CBC/CTR only
with separate authentication (Encrypt-then-MAC); non-cryptographic PRNGs "must not be used for anything
security critical" (`java.util.Random` unsafe, `SecureRandom` safe); "Do not hard-code keys into the
application source code" nor "check keys into version control"; on custom algorithms, "Don't do this";
enforce "initialization vector (IV) uniqueness", and let the library generate IVs.
**Contributes**: Nearly every crypto row of the always-flag table, with the preferred form.
**Checkable in a diff?** Yes.

### 5.2 NIST SP 800-131A (Rev. 2 in force; Rev. 3 initial public draft 2024-10-21)

**Work**: NIST. *Transitioning the Use of Cryptographic Algorithms and Key Lengths*. Rev. 3 ipd announced
https://csrc.nist.gov/news/2024/comment-on-nist-sp-800-131a-revision-3 (official, high); comments closed
2024-12-04. **Final Rev. 3 status not confirmed.**
**Evidence**: Draft moves the minimum security strength from 112 to 128 bits on 2030-12-31; SHA-1 and
other 112-bit-strength hash uses deprecated, then disallowed after 2030; AES-ECB disallowed for
encryption on publication (per the SafeLogic summary, vendor, medium — corroborates NIST's own news item
on the 128-bit move only).
**Contributes**: The authority for "weak primitive" flags (MD5, SHA-1 for signatures/integrity, DES/3DES,
RC4, RSA < 2048, ECB).
**Checkable in a diff?** Yes, for algorithm names and key sizes.
**Caveats**: Dated by design — the list moves (128-bit floor in 2030; post-quantum transition pending).
Pin the table to "NIST-disallowed or deprecated", not a frozen algorithm list.

### 5.3 Egele et al., "An Empirical Study of Cryptographic Misuse in Android Applications" (CCS 2013)

**Work**: Manuel Egele, David Brumley, Yanick Fratantonio, Christopher Kruegel. *ACM CCS '13*, pp. 73–84.
https://seclab.cs.ucsb.edu/publications/egele2015an_empirical/ (academic, high).
**Evidence**: "10,327 out of 11,748 applications that use cryptographic APIs – 88% overall – make at least
one mistake." The paper's six CryptoLint rules — no ECB; no constant IV for CBC; no constant symmetric
keys; no constant PBE salts; at least 1,000 PBE iterations; no static seed for `SecureRandom` — are from
the researcher's prior knowledge; **the rule list was not readable this session** (PDF fetch failed).
**Canonicity**: Crossref is-referenced-by-count **309** (2026-10-20). The founding empirical
crypto-misuse paper; follow-up tools (CogniCrypt, CryptoGuard — prior knowledge) build on it.
**Contributes**: Evidence that crypto misuse is *common* and *mechanically detectable* — the case for
putting crypto rows in the always-flag half.
**Checkable in a diff?** Yes; the rules are static-analysis rules.

### 5.4 Books (cited in section 2)

B9 *Cryptography Engineering* and B13 *Serious Cryptography* (2nd ed., 2024) supply the principle
behind the flags: use a vetted, high-level, authenticated construction from a maintained library; never
compose primitives yourself. B7 *24 Deadly Sins* lists "weak random numbers", "using cryptography
incorrectly", "improper use of PKI" and "failing to protect network traffic" as sins.

### 5.5 Reviewer synthesis (interpretation)

Flag: home-grown or hand-composed crypto (CWE-327); MD5/SHA-1 for passwords, signatures or integrity
(CWE-328, CWE-916); ECB (CWE-327); unauthenticated encryption where integrity matters (CWE-353); constant
or reused IV/nonce (CWE-329, CWE-323); hard-coded key (CWE-321); non-CSPRNG for tokens, keys or IDs
(CWE-338, CWE-330); TLS certificate or hostname verification disabled (CWE-295, CWE-297); non-constant-time
comparison of MACs or tokens (CWE-208). Confidence: High for the list as a whole (OWASP, NIST, CCS paper,
three books); individual CWE id fits should be confirmed against cwe.mitre.org before shipping.

## 6. Third-party packages and supply chain

### 6.1 Thompson, "Reflections on Trusting Trust" (1984)

**Work**: Ken Thompson. *Communications of the ACM* 27(8), August 1984 (pp. 761–763 per the Berkeley
copy's filename `p761`). Turing Award lecture. Copies hosted by MIT CSAIL and UC Berkeley course pages
(academic, high).
**Evidence**: Three pages. A compiler binary can be trojaned to re-insert the trojan into future builds of
itself and into `login`, so reading source cannot prove a program clean; Thompson suggests it matters more
to trust the people who wrote the software.
**Canonicity**: Crossref is-referenced-by-count **424** (2026-10-20; Crossref confirms CACM 27(8):
761–763, 1984-08-01). Turing Award lecture; set reading in MIT 6.857 and Berkeley CS161 (both host
copies); the root citation for reproducible builds.
**Contributes**: The supply-chain *principle*: you inherit the trust of everything that built your code.
**Checkable in a diff?** No. Principles half.

### 6.2 SLSA (Supply-chain Levels for Software Artifacts)

**Work**: OpenSSF / The Linux Foundation. *SLSA Specification* v1.2 (status "Approved"; v1.1 and a
working draft also listed). https://slsa.dev/spec/ (trusted per task configuration, high). **Release
date of v1.2 not shown on the page.**
**Evidence**: Organised "into a series of levels that describe increasing security guarantees" across a
Build Track and a Source Track, with cross-track threats and mitigations and provenance attestation
formats.
**Canonicity**: Originated at Google; now an OpenSSF specification; referenced by NIST SSDF mappings
(not re-verified).
**Contributes**: Vocabulary for build integrity (provenance, hermetic and isolated builds).
**Checkable in a diff?** Mostly no — a property of the build platform. A diff can show a CI change that
removes provenance generation or signing.

### 6.3 NIST SP 800-218, *Secure Software Development Framework* (SSDF)

**Work**: Souppaya, Scarfone, Dodson. NIST SP 800-218, SSDF v1.1, final 2022-02-03.
https://csrc.nist.gov/pubs/sp/800/218/final (official, high). **Rev. 1 (SSDF v1.2) initial public draft
released 2025-12-17** under Executive Order 14306 (Booth, Ogata, Kent, Souppaya, Dodson); comments closed
2026-01-30; https://csrc.nist.gov/pubs/sp/800/218/r1/ipd. **No final v1.2 found as of 2026-10-20.**
**Evidence**: "a core set of high-level secure software development practices that can be integrated
into each SDLC implementation". Practice groups PO / PS / PW / RV (Prepare the Organization, Protect the
Software, Produce Well-Secured Software, Respond to Vulnerabilities) — group names from prior knowledge,
not shown on the page read.
**Canonicity**: US federal procurement basis for software attestation; maps to BSIMM, SAMM, SLSA and
others.
**Contributes**: Process authority for "review code", "use vetted components", "archive provenance".
**Checkable in a diff?** No. Process; cite only in the Principles half.

### 6.4 OpenSSF Scorecard

**Work**: OpenSSF. https://github.com/ossf/scorecard (github.com, medium-high; OpenSSF trusted per task).
**Evidence**: "automated tool that measures security heuristics for open source projects", scoring each
check 0–10. Checks include Binary-Artifacts, Branch-Protection, Code-Review, Dangerous-Workflow,
Dependency-Update-Tool, Maintained, Pinned-Dependencies, SAST, Security-Policy, Signed-Releases,
Token-Permissions, Vulnerabilities.
**Contributes**: Several checks are diff-checkable in CI configuration: **Pinned-Dependencies** (actions
and images pinned by hash), **Dangerous-Workflow** (untrusted code checked out in a privileged trigger),
**Token-Permissions** (workflow tokens broader than read), **Binary-Artifacts** (committed binaries).
**Caveats**: A tool, not a standard; cite its check names as a source of flaggable CI patterns, and cite
CWE for the defect.

### 6.5 OpenSSF Concise Guides

**Work**: OpenSSF Best Practices Working Group. *Concise Guide for Evaluating Open Source Software*
(https://best.openssf.org/Concise-Guide-for-Evaluating-Open-Source-Software, dated 2025-03-28) and
*Concise Guide for Developing More Secure Software*; both introduced 2022-09-13
(https://openssf.org/blog/2022/09/13/...). Trusted per task configuration, high.
**Evidence**: The evaluating guide asks whether the dependency is needed at all, whether it is the
authentic project rather than a lookalike or attacker-controlled fork, and whether it is maintained
(activity in the past 12 months, recent releases, more than one maintainer). The developing guide is a
short practice list (MFA for privileged developers, a vulnerability-reporting route); its full text was
**not read this session**.
**Contributes**: The reviewer questions for **a diff that adds a dependency**: needed? authentic name?
maintained? This is the only diff-level supply-chain check that applies to every language.
**Checkable in a diff?** Partly — the addition is visible; the answers need a lookup.

### 6.6 Canonical incidents (teaching cases)

| Incident | Date | Primary source | Teaches |
|---|---|---|---|
| event-stream / flatmap-stream | Malicious `flatmap-stream@0.1.1` added to `event-stream@3.3.6`; npm removed it 2018-11-26 | npm blog "Details about the event-stream incident" (registry operator, primary); Snyk post-mortem 2018-12-06 (vendor, medium-high) | Maintainer handover to a stranger ("right9ctrl"); a transitive dependency targeting one downstream (Copay wallet) |
| Dependency confusion | Feb 2021 | Alex Birsan, "Dependency Confusion: How I Hacked Into Apple, Microsoft and Dozens of Other Companies" (Medium, named researcher; corroborated by BleepingComputer, Malwarebytes, AppleInsider) | A public package with an internal package's name wins resolution; 30+ firms hit; CVE-2021-24105 |
| xz-utils backdoor | CVE-2024-3094, published 2024-03-29, CVSS 3.1 10.0, CWE-506 | NVD: "Malicious code was discovered in the upstream tarballs of xz, starting with version 5.6.0" (official, high) | Multi-year social engineering of a lone maintainer; payload in release tarballs, not the repository — Thompson's lesson, 40 years on |
| Typosquatting | Recurrent | Taxonomy in 6.7; OpenSSF evaluating guide's "lookalike" check | A dependency name one edit from a popular one |

### 6.7 Ladisa et al., "SoK: Taxonomy of Attacks on Open-Source Software Supply Chains" (IEEE S&P 2023)

**Work**: Piergiorgio Ladisa, Henrik Plate, **Matias Martinez**, Olivier Barais. IEEE Symposium on
Security and Privacy 2023 (44th, San Francisco). Preprint https://arxiv.org/abs/2204.04008 (academic,
high). Venue confirmed only via secondary sources (neverworkintheory.org, KTH CHAINS); IEEE Xplore page
not opened.
**Evidence**: An attack tree of "107 unique vectors, linked to 94 real-world incidents, and mapped to 33
mitigating safeguards", validated with 17 experts and 134 developers; ecosystem-independent.
**Canonicity**: Top-four security venue; companion "Risk Explorer" tool (SAP). Citation count: not found.
**Contributes**: The peer-reviewed taxonomy to cite for supply-chain attack classes (typosquatting,
dependency confusion, maintainer takeover, build compromise).
**Checkable in a diff?** No; taxonomy. Supports the advisory list.

## 7. LLM and agent security

This plugin is mostly prompts, Python hooks and shell that run inside an agent. Its reviewers need the
agent-specific defects as much as the classic ones. The field is young; every source below is 2023 or
later, and versions will move.

### 7.1 Greshake et al., "Not What You've Signed Up For" (AISec 2023)

**Work**: Kai Greshake, Sahar Abdelnabi, Shailesh Mishra, Christoph Endres, Thorsten Holz, Mario Fritz.
"Not What You've Signed Up For: Compromising Real-World LLM-Integrated Applications with Indirect Prompt
Injection". *Proceedings of the 16th ACM Workshop on Artificial Intelligence and Security* (AISec '23,
co-located with CCS, Copenhagen), pp. 79–90, 2023-11-30. DOI 10.1145/3605764.3623985. Preprint
arXiv:2302.12173 (v1 2023-02-23, v2 2023-05-05). Academic, high.
**Evidence**: Introduces *indirect* prompt injection: attacks that reach an LLM-integrated application
remotely by "strategically injecting prompts into data likely to be retrieved".
**Canonicity**: Crossref is-referenced-by-count **650** (queried 2026-10-20). The paper that named the
indirect form; cited by OWASP LLM01 and NIST AI 100-2 (not re-verified).
**Contributes**: The principle that **retrieved data is code to an LLM**: any tool output, web page, file
or email an agent reads can issue instructions.
**Checkable in a diff?** The principle no; its consequence yes — untrusted text concatenated into a prompt
that also holds tools or secrets.

### 7.2 Willison, prompt injection writing and "The lethal trifecta" (2022–2025)

**Work**: Simon Willison. "The lethal trifecta for AI agents: private data, untrusted content, and
external communication", simonwillison.net, 2025-06-16
(https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/). He coined "prompt injection", named after
SQL injection; the post says "a few years ago" and the linked post's URL is from September 2022. Named
recognised expert, medium-high per task configuration; cross-referenced below.
**Evidence**: The trifecta is "Access to your private data", exposure to "any mechanism by which text (or
images) controlled by a malicious attacker could become available to your LLM", and "The ability to
externally communicate in a way that could be used to steal your data". "The only way to stay safe there
is to avoid that lethal trifecta combination entirely." On detection: "we still don't know how to 100%
reliably prevent this from happening"; a 95% guardrail detection rate is a failing grade in web security.
**Cross-reference**: The CaMeL and design-patterns papers (7.4, 7.5) reach the same conclusion — prompt
injection cannot be filtered out, only designed around — from independent author groups (Google
DeepMind/ETH; IBM/Invariant/ETH/Microsoft et al.). Confidence: High.
**Contributes**: **The single most flaggable agent-design check**: does one agent context combine private
data, untrusted content and an exfiltration channel (network, email, a write to a public place, even a
rendered image URL)? If yes, flag.
**Checkable in a diff?** Often yes, in an agent's tool grant or a hook's configuration.

### 7.3 OWASP Top 10 for LLM Applications 2025, and Top 10 for Agentic Applications 2026

**Work**: OWASP GenAI Security Project. *2025 Top 10 Risk & Mitigations for LLMs and Gen AI Apps*.
https://genai.owasp.org/llm-top-10/ (trusted per task, high). English release date not shown on the
page (translations dated 2025-03-12 and 2025-07-22; the English list is widely reported as Nov 2024 —
**not confirmed**).
**Evidence**: LLM01 Prompt Injection · LLM02 Sensitive Information Disclosure · LLM03 Supply Chain ·
LLM04 Data and Model Poisoning · LLM05 Improper Output Handling · LLM06 Excessive Agency · LLM07 System
Prompt Leakage · LLM08 Vector and Embedding Weaknesses · LLM09 Misinformation · LLM10 Unbounded
Consumption.
**Agentic list**: *OWASP Top 10 for Agentic Applications 2026* (ids ASI01–ASI10; ASI01 "Agent Goal
Hijack", ASI10 "Rogue Agents"), reported published 2025-12-09 — **confirmed only by secondary vendor
sources (Cycode, Kratikal, Indusface, medium)**; genai.owasp.org's page for it was not reached.
**Contributes**: Category ids for the agent rows: LLM01 (untrusted text in a privileged prompt), LLM05
(model output passed unescaped to a shell, SQL, HTML or `eval`), LLM06 (tools broader than the task),
LLM07 (secrets in a system prompt), LLM10 (no token, step or cost limit).
**Checkable in a diff?** LLM05, LLM06, LLM07 and LLM10 leave marks in code and config. LLM01 is checkable
as a data-flow pattern, not as a string. LLM04, LLM08, LLM09 are design or operations concerns.
**Caveats**: Ids carry the year and churn (the 2023 v1.1 list numbered them differently — prior
knowledge, not re-verified). Pin to `LLM05:2025` etc. and expect renumbering.

### 7.4 Debenedetti et al., "Defeating Prompt Injections by Design" (CaMeL, 2025)

**Work**: Edoardo Debenedetti, Ilia Shumailov, Tianqi Fan, Jamie Hayes, Nicholas Carlini, Daniel Fabian,
Christoph Kern, Chongyang Shi, Andreas Terzis, Florian Tramèr. arXiv:2503.18813, v1 2025-03-24, v2
2025-06-24 (Google DeepMind / Google / ETH Zurich). Academic preprint, high. Peer-reviewed venue **not
confirmed**.
**Evidence**: CaMeL "explicitly extracts the control and data flows from the (trusted) query", so
untrusted retrieved data "can never impact the program flow", and uses capabilities to stop private data
leaving through unauthorised flows. On AgentDojo it solves 77% of tasks "with provable security
(compared to 84% with an undefended system)".
**Contributes**: The design principle: **separate control flow (from the trusted user) from data flow
(from untrusted sources), and attach capabilities to data**. Saltzer & Schroeder's complete mediation,
applied to tokens.
**Checkable in a diff?** No; architecture. Principles half.

### 7.5 Beurer-Kellner et al., "Design Patterns for Securing LLM Agents against Prompt Injections" (2025)

**Work**: Luca Beurer-Kellner, Beat Buesser, Ana-Maria Creţu, Edoardo Debenedetti, Daniel Dobos, Daniel
Fabian, Marc Fischer, David Froelicher, Kathrin Grosse, Daniel Naeff, Ezinwanne Ozoani, Andrew Paverd,
Florian Tramèr, Václav Volhejn. arXiv:2506.08837, v1 2025-06-10, v3 2025-06-27. Academic preprint, high.
Peer-reviewed venue **not confirmed**.
**Evidence**: "a set of principled design patterns for building AI agents with provable resistance to
prompt injection". Core principle: "once an LLM agent has ingested untrusted input, it must be
constrained so that it is impossible for that input to trigger any consequential actions". The six
patterns, as summarised by Willison (2025-06-13): Action-Selector; Plan-Then-Execute; LLM Map-Reduce;
Dual LLM; Code-Then-Execute; Context-Minimization.
**Contributes**: A named vocabulary for the **preferred form** when a reviewer flags a trifecta.
**Checkable in a diff?** Partly: a reviewer can tell whether an agent's tool outputs can alter which tools
run next.

### 7.6 NIST AI 100-2 E2025, *Adversarial Machine Learning: A Taxonomy and Terminology of Attacks and Mitigations*

**Work**: Apostol Vassilev (NIST), Alina Oprea (Northeastern), Alie Fordyce and Hyrum Anderson (Cisco),
Xander Davies (UK AI Security Institute), Maia Hamin (US AI Safety Institute). NIST AI 100-2 E2025, final
2025-03-24. https://csrc.nist.gov/pubs/ai/100/2/e2025/final (official, high). Predecessor: E2023
(January 2024) — prior knowledge, not shown on the page.
**Evidence**: A hierarchy of ML method types, attack lifecycle stages, and attacker goals, capabilities and
knowledge, with mitigations and a glossary, to give "a common language for the rapidly developing AML
landscape". Keywords include data poisoning, evasion, privacy breach, abuse, large language models.
Its treatment of direct and indirect prompt injection was **not confirmed from the page read**.
**Contributes**: Authoritative terminology; the citation for "prompt injection has no complete
mitigation" if the PDF bears it out.
**Checkable in a diff?** No. Terminology and taxonomy.

### 7.7 Reviewer synthesis for agents and hooks (interpretation)

Untrusted text — tool output, file contents, web pages, issue bodies, commit messages, PR descriptions —
is data that can issue instructions. A hook or agent that concatenates it into a privileged prompt, passes
model output to a shell, SQL or `eval`, or holds private data, untrusted input and an outbound channel in
one context, is the agent form of injection. The classic CWE ids still apply to the sink: CWE-78/77 for
model output reaching a shell, CWE-94/95 for `eval`, CWE-79 for rendered output. For the
injection itself, **CWE-1427 "Improper Neutralization of Input Used for LLM Prompting"** (Base; submitted
2024-06-21, added in CWE 4.16 on 2024-11-19; https://cwe.mitre.org/data/definitions/1427.html, verified):
a product builds prompts from external data so the model "cannot separate user input from the developer's
system instructions". This gives the agent rows a CWE id like every other row.

## 8. Secure development lifecycle (only as far as it informs a code-level rule)

| Framework | Verified facts | What reaches a code-level rule |
|---|---|---|
| **Microsoft SDL** — https://www.microsoft.com/en-us/securityengineering/sdl/practices (trusted per task, high) | 10 practices, undated page (© 2026; "20 years" since SDL began): standards and governance; **proven security features, languages and frameworks**; design review and threat modeling; **cryptography standards**; **supply chain**; engineering environment; security testing; platform security; monitoring and response; training. An OWASP SAMM blog says 49 requirements sit under the 10 practices. | Practice 2 is the authority for "use the framework's escaping, the platform's crypto, a memory-safe language" — the *preferred form* column. Practices 4 and 5 back the crypto and dependency rows. |
| **OWASP SAMM v2** — https://owaspsamm.org/model/ (owasp, high) | Five business functions × three practices: Governance; Design (Threat Assessment, Security Requirements, Secure Architecture); Implementation (Secure Build, Secure Deployment, Defect Management); Verification; Operations. | Maturity model for organisations. Nothing diff-checkable; cite only to place code review inside Verification. |
| **BSIMM15** — Black Duck (vendor; descriptive study, medium-high) | Published January 2025; observes 121 organisations; themes include AI adoption and supply-chain risk. **BSIMM16 not checked.** | Descriptive (what firms do), not prescriptive. Co-founded by McGraw (B5). No code-level content. |

**Verdict (interpretation)**: SDL frameworks justify *that* code review happens and *which* standards it
applies; none supplies a flaggable item that ASVS, CWE or the cheat sheets do not already supply more
precisely. The rule should cite at most Microsoft SDL practice 2 ("proven security features") as the
principle behind preferring framework mechanisms over hand-rolled ones. Confidence: Medium (three
frameworks read at index level only).

---

## Synthesis

All of this section is **interpretation** built on the findings above. Each row names the finding it
rests on.

### Ranked shortlist (the rule's spine)

The rule should cite two kinds of work, as `ux.md` cites Nielsen beside WCAG: books and papers for the
Principles half, standards with item ids for the always-flag half.

| Rank | Work | Half | Why it earns a place |
|---|---|---|---|
| 1 | Saltzer & Schroeder, "The Protection of Information in Computer Systems" (1975) | Principles | The origin of least privilege, fail-safe defaults, complete mediation and open design; 1,431 Crossref citations; restated by NIST SP 800-160 and every textbook. Read with Smith 2012's triage (1.2). |
| 2 | **CWE**, with the 2025 CWE Top 25 (MITRE/CISA) | Always-flag | The identifier space every other standard maps into. Ids are stable for decades; every table row cites one. |
| 3 | **OWASP ASVS 5.0.0** | Always-flag | The only vendor-neutral standard written as testable requirements, with versioned ids (`v5.0.0-1.2.5`). Second id column. |
| 4 | Johnsson, Deogun, Sawano, *Secure by Design* (2019) | Principles | Security as a design property — domain primitives, validation order, safe errors — in the DDD vocabulary `coding.md` and `architecture.md` already use. The natural bridge into this repo's rules. |
| 5 | Shostack, *Threat Modeling: Designing for Security* (2014) | Principles | Four-question framework, STRIDE, trust boundaries. Design-only, but it supplies the word "trust boundary" every flag depends on. **A 2nd edition is announced for Dec 2026 / 2027**; cite by title so the edition can change. |
| 6 | OWASP Cheat Sheet Series | Always-flag (preferred form) | Code-level fixes for each flag: parameterize, encode by context, argon2id, a secrets manager, no ECB. |
| 7 | NIST SP 800-63B-4 (2025) | Always-flag (authn) | The only standard whose password rules are SHALL/SHALL NOT and diff-checkable; it also *removes* flags (composition, rotation). |
| 8 | Willison, "The lethal trifecta" (2025) + Greshake et al. (AISec 2023) + OWASP Top 10 for LLM Applications 2025 + CWE-1427 | Both | The agent half. Greshake (650 Crossref citations) establishes indirect injection; Willison gives the one flaggable design test; OWASP LLM ids and CWE-1427 give the table its ids. CaMeL and Beurer-Kellner et al. supply the preferred forms. |
| 9 | Adkins et al., *Building Secure and Reliable Systems* (Google, 2020) | Principles | Least privilege and safe-by-construction APIs from an organisation that runs them at scale; free online. Corroborates rank 1 and Microsoft SDL practice 2 ("proven security features"). |
| 10 | Kohnfelder, *Designing Secure Software* (2021) | Principles, with diff-checkable Part III | STRIDE co-author; modern, language-neutral; chapters on untrusted input and low-level flaws bridge the halves. |

**Background, not spine**: Anderson's *Security Engineering* (breadth, free online — cite for "why
systems fail", not for rules); *24 Deadly Sins* (a defect list, now subsumed by CWE ids); *Cryptography
Engineering* / *Serious Cryptography* 2nd ed. (behind the crypto rows; prefer Aumasson for currency);
Thompson 1984 (the supply-chain principle, one sentence); OWASP Top 10:2025 (category headings only);
SLSA, SSDF, Scorecard, SAMM, BSIMM, Microsoft SDL (process; not code-checkable). Seacord and the CERT
standards belong in `cpp.md`, not here.

### Candidate always-flag list

Objective, language-agnostic defects a reviewer flags on sight in a diff. "Untrusted" means data that
crossed a trust boundary: request input, files, environment from another principal, tool or model output,
issue and PR text. ASVS ids are given at **chapter level** because only `v5.0.0-1.2.5` was read this
session; resolve each to an item before the rule ships.

| # | Defect a reviewer flags | CWE | ASVS 5.0.0 | Top 10 |
|---|---|---|---|---|
| F1 | Query (SQL, NoSQL, LDAP) built by concatenating or formatting untrusted data | CWE-89 (CWE-943) | V1 | A05:2025 |
| F2 | Shell command string built from untrusted data, or a shell invoked where an argv array would do | CWE-78, CWE-77 | v5.0.0-1.2.5 | A05:2025 |
| F3 | Untrusted value placed in an argv without a `--` terminator or option check | CWE-88 | V1 | A05:2025 |
| F4 | `eval`/`exec`/dynamic import or template compilation on untrusted data | CWE-94, CWE-95, CWE-1336 | V1 | A05:2025 |
| F5 | Untrusted data rendered into HTML/JS without context encoding, or auto-escaping turned off | CWE-79 | V1, V3 | A05:2025 |
| F6 | File path from untrusted input used without canonicalising and checking containment | CWE-22 | V5 | A01:2025 |
| F7 | Native object deserialisation of untrusted bytes (pickle, unsafe YAML load, Java/.NET binary serialisers) | CWE-502 | V1 | A08:2025 |
| F8 | XML parsed from untrusted input with external entities or DTDs enabled | CWE-611 | V1 | A02:2025 |
| F9 | Server fetches a caller-supplied URL with no destination allow-list | CWE-918 | V1 | A01:2025 |
| F10 | Redirect to a caller-supplied URL with no allow-list | CWE-601 | V3 | A01:2025 |
| F11 | Handler, endpoint or command that changes or reveals data with no authorization check | CWE-862 | V8 | A01:2025 |
| F12 | Object loaded by a caller-supplied id with no ownership/tenant check (IDOR) | CWE-639 | V8 | A01:2025 |
| F13 | Critical function reachable without authentication | CWE-306 | V6 | A07:2025 |
| F14 | Error, timeout or exception path that grants access, skips a check or returns "allow" (fail-open) | CWE-636 | V16 | A10:2025 |
| F15 | Credential, API key, token or private key literal in source, committed config or a real-looking fixture | CWE-798 | V13 | A07:2025 |
| F16 | Secret, token, password or session id written to a log, error message or exception text | CWE-532, CWE-209 | V16 | A09:2025 |
| F17 | Password stored in plain text, reversibly encrypted, or with a fast hash (MD5, SHA-x) instead of a password-hashing scheme | CWE-256, CWE-916 | V6; NIST 800-63B-4 §3.1.1.2 | A04:2025 |
| F18 | Password policy that NIST forbids: composition rules, forced periodic rotation, truncation, hints, knowledge questions, or a maximum below 64 | (none; standard-only) | V6; NIST 800-63B-4 §3.1.1.2 | A07:2025 |
| F19 | Login or token check with no rate limit or lockout | CWE-307 | V6; NIST 800-63B-4 §3.2.2 | A07:2025 |
| F20 | Non-cryptographic RNG used for tokens, keys, session ids, nonces or reset codes | CWE-338, CWE-330 | V11 | A04:2025 |
| F21 | Hand-rolled cipher, MAC, KDF or protocol; or primitives composed by hand where a library offers an authenticated construction | CWE-327 | V11 | A04:2025 |
| F22 | Broken or NIST-disallowed algorithm or mode for a security purpose: MD5/SHA-1 for signatures or integrity, DES/3DES/RC4, ECB, RSA < 2048 | CWE-327, CWE-328 | V11 | A04:2025 |
| F23 | Constant, reused or predictable IV/nonce; hard-coded encryption key | CWE-329, CWE-323, CWE-321 | V11 | A04:2025 |
| F24 | TLS certificate or hostname verification disabled (`verify=False`, `rejectUnauthorized: false`, `-k`, `InsecureSkipVerify`) | CWE-295 | V12 | A04:2025 |
| F25 | MAC, token or password-hash comparison with ordinary equality instead of a constant-time compare | CWE-208 | V11 | A04:2025 |
| F26 | Signed token accepted without verifying the signature, or with the algorithm taken from the token (`alg: none`) | CWE-347 | V9 | A07:2025 |
| F27 | Session cookie without `Secure`/`HttpOnly`/`SameSite`; session id not rotated at login; cookie-authenticated state change with no CSRF defence | CWE-614, CWE-1004, CWE-384, CWE-352 | V3, V7 | A07:2025, A01:2025 |
| F28 | Unbounded work from untrusted input: no size, count, time or recursion limit; a backtracking regex on untrusted text | CWE-770, CWE-1333 | V2 | — |
| F29 | Remote code run without an integrity check: `curl … \| sh`, a CI action or image pinned by mutable tag, a script fetched at build time | CWE-494, CWE-829 | V15 | A03:2025, A08:2025 |
| F30 | Privilege broader than the task: world-writable files (`chmod 777`), running as root, wildcard IAM/scopes, CI token `write-all` | CWE-732, CWE-250 | V13 | A01:2025, A02:2025 |
| **Agent rows** | | | | **OWASP LLM 2025** |
| F31 | Untrusted text (tool output, file, web page, issue or PR body) inserted into a prompt whose context also holds tools or secrets, with no isolation | CWE-1427 | — | LLM01:2025 |
| F32 | Model output passed to a shell, SQL, `eval`, HTML or a file path without the treatment F1–F6 give untrusted input | CWE-78 / -94 / -79 / -22 | — | LLM05:2025 |
| F33 | One agent context holds private data, untrusted content and an outbound channel (Willison's lethal trifecta) | CWE-1427 | — | LLM01, LLM02, LLM06:2025 |
| F34 | Agent, hook or command granted tools beyond its task (bare shell, any-path write, network) | CWE-250 | — | LLM06:2025 |
| F35 | Secret or credential placed in a system prompt or agent instructions | CWE-798 | — | LLM07:2025 |
| F36 | Agent loop with no step, token, time or cost bound | CWE-770 | — | LLM10:2025 |

F33 and F34 restate, for agents, what this repo already enforces for commands: `mutates:` declared by the
grant, and a narrow `Bash(...)` grant beats bare `Bash` (CLAUDE.md "Commands declare mutation").

### Candidate advisory list (judgment calls)

A reviewer *raises* these; the author decides. Each needs context a diff does not carry.

- **A new trust boundary** (a new endpoint, input source, tool, or hook reading external text) without a
  stated threat model — Shostack's four questions. (B3, B2)
- **A new dependency**: is it needed, is the name authentic (one edit from a popular package?), is it
  maintained by more than one person? (OpenSSF evaluating guide; event-stream, xz, typosquatting cases)
- **Validation scattered through layers instead of at the boundary**, or a security-relevant value passed
  as a bare string where a domain primitive would enforce invariants. (B1)
- **Deny-list validation** where an allow-list is feasible. (Saltzer & Schroeder fail-safe defaults; ASVS V1/V2)
- **Security logging gaps**: an authentication or authorization decision with no audit record. (A09:2025;
  Saltzer & Schroeder compromise recording)
- **Detail in user-facing errors** beyond what the user can act on. (CWE-209; B1 safe error handling)
- **Secrets in environment variables** where a secrets manager is available. (12-Factor vs OWASP Secrets
  Management Cheat Sheet — see Conflicting Information)
- **Complexity in security code** — an authorization path too intricate to review. (economy of mechanism)
- **Agent architecture choice** among the six design patterns when F33 fires. (7.5)
- **Lockfile and pinning policy** for a library (where ranges are normal) versus an application or CI
  config (where pins are expected). (Scorecard Pinned-Dependencies)
- **Missing security headers** (CSP, frame ancestors) on new HTML surfaces. (ASVS V3)
- **Unreachable vulnerable dependency** flagged by a scanner — triage reachability before demanding an
  upgrade.

### Do-not-flag list (common false positives)

- **MD5 or SHA-1 used for a non-security purpose** — cache keys, deduplication, ETags, git object ids.
  CWE-327/328 concern security use only.
- **A non-cryptographic RNG for non-security work** — shuffling, jitter, sampling, test data.
- **Obvious placeholders and test credentials** — `.env.example`, `password123` in a login test, keys
  copied from documentation and marked as examples. Flag only values that could authenticate somewhere.
- **String-built queries or commands from constants or a fixed allow-list** — an identifier chosen from a
  closed enum is not untrusted data. F1–F3 need untrusted input reaching the sink.
- **A missing auth check on a deliberately public route** — health checks, static assets, login itself.
- **Missing validation on an internal call that crosses no trust boundary** — validate at the boundary
  (B1, B2); demanding it at every layer adds noise, not safety.
- **The absence of password composition rules, rotation, or a short maximum** — NIST 800-63B-4 forbids
  them; their absence is correct.
- **Paste and password-manager support** — NIST requires allowing autofill.
- **"Security through obscurity" objections to unpublished internals** — open design forbids *relying* on
  secrecy; it does not require publishing.
- **The absence of a prompt-injection detector or guardrail** — Willison and both design-pattern papers
  hold that filters cannot be relied on; flag the trifecta or the grant (F33, F34), not a missing filter.
- **A Top 10 category name as a finding** — "this is A05" is not a defect; name the CWE and the line.

### Versioned vs durable

| Will date (pin the version in every citation) | Durable (cite by title) |
|---|---|
| OWASP Top 10:2025 — ids carry the year; renumbered each edition | Saltzer & Schroeder 1975; Thompson 1984 |
| OWASP ASVS 5.0.0 — chapters renumbered from 4.0; OWASP warns ids "may change between versions" | CWE ids (CWE-89 has kept its number since CWE began; names occasionally change) |
| CWE Top 25 *ranking* — annual | The books' principles (Secure by Design, Shostack, Kohnfelder, Anderson) |
| OWASP Top 10 for LLM Applications 2025; Agentic Top 10 2026 | Willison's trifecta as a design test |
| NIST SP 800-63B-4 (Rev. 4, 2025); SP 800-131A (Rev. 3 draft moves the floor to 128-bit in 2030) | 12-Factor's litmus test |
| SLSA v1.2; SSDF v1.1 (v1.2 draft Dec 2025); BSIMM annual | The OWASP Cheat Sheets' advice (content is durable; pages change) |
| Specific algorithm lists (post-quantum transition pending) | "Use a vetted, authenticated construction; never compose primitives" |

**Recommendation for the rule (interpretation)**: write the always-flag rows by CWE id and plain defect
description, carry ASVS and Top 10 ids in a column stamped with their version, and add a dated line —
as `CLAUDE.md` does for Claude Code versions — naming the editions the table was checked against.

## Source Analysis

All accessed 2026-10-20. Reputation per the task's trusted-domain configuration.

| Source | Domain | Reputation | Type | Verification |
|---|---|---|---|---|
| Saltzer & Schroeder (UVA copy; Crossref) | cs.virginia.edu; api.crossref.org | High | Academic | Verified (text + Crossref) |
| Smith 2012 (author preprint; Crossref) | cryptosmith.com; api.crossref.org | Medium-high (named author) / High | Academic | Verified (Crossref + Wikipedia citation) |
| NIST SP 800-160 v1r1 | csrc.nist.gov | High | Official | Metadata verified; principle count not |
| Manning, No Starch, sre.google, schneier.com, oreilly.com publisher pages | publishers | High (bibliographic) | Publisher | Verified per title |
| Anderson *Security Engineering* author page | cl.cam.ac.uk | High | Academic | Via search snippets only |
| Shostack Four-Question repo; threatmodelingbook.com | github.com; author site | Medium-high | Industry | Verified |
| Bokus / Goodreads (Shostack 2nd ed.) | retailers | **Medium** — retailer listings | Commercial | Partially (dates disagree) |
| IEEE Cipher book reviews | ieee-security.org | High | Academic society | Search snippets |
| CWE Top 25 2025; CWE-636/208/88/1357/829/1333/1427 | cwe.mitre.org | High | Official | Verified |
| OWASP Top 10:2025 | top10.owasp.org | High | Standards body | List verified; date not |
| GitLab, Outpost24, Qualys on Top 10:2025 | vendor blogs | **Medium** | Industry | Cross-referenced against OWASP list |
| OWASP ASVS project page; GitHub ASVS 5.0 tree | owasp.org; github.com | High | Standards body | Chapters and id scheme verified; item texts not |
| appknox.com (ASVS launch date) | vendor glossary | **Medium** | Industry | Unconfirmed on owasp.org |
| OWASP Cheat Sheet Series index; Cryptographic Storage sheet | cheatsheetseries.owasp.org | High | Standards body | Verified |
| SEI CERT wiki | wiki.sei.cmu.edu | High | Academic | Via search snippets |
| NIST SP 800-63B-4 | csrc.nist.gov; pages.nist.gov | High | Official | Verified |
| 12-Factor Config | 12factor.net | Medium-high | Industry | Verified |
| NIST SP 800-131A Rev. 3 ipd | csrc.nist.gov | High | Official | Announcement verified |
| SafeLogic on 800-131A | vendor blog | **Medium** | Industry | Partial |
| Egele et al. (UCSB page; Crossref) | seclab.cs.ucsb.edu; api.crossref.org | High | Academic | Metadata + headline figure verified; rules not |
| Thompson 1984 (MIT/Berkeley copies; Crossref) | csail.mit.edu; berkeley.edu | High | Academic | Verified |
| SLSA spec | slsa.dev | High (task config) | Standards | Version verified; date not |
| NIST SP 800-218 v1.1; Rev. 1 ipd | csrc.nist.gov | High | Official | Verified |
| OpenSSF Scorecard | github.com/ossf | Medium-high / High | Open source | Verified |
| OpenSSF Concise Guides | best.openssf.org; openssf.org | High (task config) | Open source | Evaluating guide verified; developing guide not read |
| npm blog (event-stream) | blog.npmjs.org | Medium-high (registry operator) | Primary incident report | Search snippets |
| Snyk, Sophos (event-stream) | vendor blogs | **Medium** | Industry | Cross-referenced with npm |
| Birsan (Medium) + BleepingComputer, Malwarebytes, AppleInsider | medium.com; press | **Medium** — named researcher, 3-source cross-ref done | Primary + press | Cross-referenced |
| NVD CVE-2024-3094 | services.nvd.nist.gov | High | Official | Verified |
| Ladisa et al. | arxiv.org | High | Academic | Preprint verified; venue via secondary |
| Greshake et al. (arXiv; Crossref) | arxiv.org; api.crossref.org | High | Academic | Verified |
| Willison posts | simonwillison.net | Medium-high (task config) | Expert | Cross-referenced with 7.4, 7.5 |
| OWASP LLM Top 10 2025 | genai.owasp.org | High | Standards body | List verified; date not |
| Cycode, Kratikal, Indusface et al. (Agentic Top 10) | vendor blogs | **Medium** | Industry | Primary not reached |
| CaMeL; Design Patterns (arXiv) | arxiv.org | High | Academic preprint | Verified |
| NIST AI 100-2 E2025 | csrc.nist.gov | High | Official | Metadata verified |
| Microsoft SDL practices | microsoft.com/securityengineering | High (task config) | Vendor framework | Verified |
| OWASP SAMM | owaspsamm.org | High | Standards body | Verified |
| Black Duck BSIMM15 | blackduck.com | Medium-high (vendor-run study) | Industry | Search snippet |

Reputation: roughly 30 of 40 sources high (75%), 3 medium-high, 7 medium (vendor blogs and retailers,
used only for corroboration or flagged as unconfirmed). Avg ≈ 0.88. No excluded domain used.
**Bias note**: Snyk, Qualys, Cycode, GitLab, Black Duck and SafeLogic sell security products; their pages
were used only for dates or corroboration, never as sole support for a claim the rule depends on.

## Knowledge Gaps

### Gap 1: Citation counts for books
**Issue**: No citation count for any book. | **Attempted**: Crossref works only for DOI'd papers; Google
Scholar not queried. | **Recommendation**: Treat edition count, publisher series and standards adoption
as the canonicity signal for books, as this document does.

### Gap 2: ASVS 5.0.0 item texts
**Issue**: Only `v5.0.0-1.2.5` was read; the always-flag table cites ASVS at chapter level. |
**Attempted**: OWASP project page; GitHub chapter listing. | **Recommendation**: Read V1, V6–V9, V11–V13,
V15, V16 in `github.com/OWASP/ASVS/tree/master/5.0/en` and fill item ids before the rule ships.

### Gap 3: Release dates not confirmed
OWASP Top 10:2025 final release; OWASP LLM Top 10 2025 English release (reported Nov 2024); ASVS 5.0.0
(reported 2025-05-30); SLSA v1.2; Shostack 2nd edition (Goodreads 2026-12-22, Bokus 2027); McGraw (2006
or 2007); *Writing Secure Code* 2nd ed. (2002 or 2003); Dowd et al. (2006 or 2007).

### Gap 4: Status of drafts
NIST SP 800-218 Rev. 1 (SSDF v1.2, ipd 2025-12-17) and SP 800-131A Rev. 3 (ipd 2024-10-21): no final found
as of 2026-10-20. Recheck before citing either as current.

### Gap 5: Primary text not reached
OWASP Top 10 for Agentic Applications 2026 (secondary sources only); OpenSSF *Concise Guide for
Developing More Secure Software* (not opened); Egele et al.'s six rules (PDF fetch failed — listed from
prior knowledge); NIST AI 100-2's prompt-injection content; NIST SP 800-160's principle count (~33,
secondary); Ladisa et al.'s IEEE Xplore record; peer-reviewed venues (if any) for CaMeL and the
design-patterns paper.

### Gap 6: Unverified candidate books
Shostack, *Threats: What Every Engineer Should Learn from Star Wars* (2023) and Viega & McGraw, *Building
Secure Software* (2001) were not checked against publisher pages.

### Gap 7: CWE ids not individually opened
Verified on cwe.mitre.org: the whole 2025 Top 25 plus CWE-88, -208, -636, -829, -1333, -1357, -1427.
From prior knowledge and **to verify**: CWE-95, -209, -250, -256, -295, -307, -321, -323, -328, -329, -330,
-347, -353, -384, -494, -532, -601, -611, -614, -732, -916, -943, -1004, -1336.
**Resolved 2026-10-20** (during DISCUSS for `security-standards-rule`): every CWE id in the always-flag
table, plus CWE-297 and CWE-353, was looked up through MITRE's CWE REST API
(`cwe-api.mitre.org/api/v1/cwe/weakness/...`, content version 4.20, dated 2026-04-30). All resolve, and
each name matches its use in the table.

## Conflicting Information

### Conflict 1: Is complete mediation obsolete?
**Position A**: Smith calls it "a sensible but obsolete view of security decision making" (IEEE S&P 2012).
**Position B**: Missing per-request authorization heads OWASP Top 10:2025 (A01) and ranks 4th in the CWE
Top 25 (CWE-862). **Assessment**: Both hold. Smith retires the single central reference monitor; the
standards demand that every access be checked. The rule should keep the per-access check and drop the
central-monitor framing.

### Conflict 2: Are environment variables a secrets store?
**Position A**: 12-Factor: "stores config in environment variables". **Position B**: OWASP Secrets
Management Cheat Sheet and Cryptographic Storage Cheat Sheet: keys belong in a secrets manager, not in
source or version control. **Assessment**: 12-Factor's litmus test (could the code be open-sourced now?)
is the durable part; it governs *separation from code*. Storage advice favours OWASP. Flag the literal
(F15); advise on the store.

### Conflict 3: Password policy
**Position A**: NIST SP 800-63B-4 forbids composition rules and periodic rotation. **Position B**: Many
organisational and compliance policies still require both (PCI DSS's 90-day rule for single-factor
passwords — prior knowledge, **not verified this session**). **Assessment**: NIST is the newer, evidence-
based federal standard; the rule should follow it and let a project override by declaration.

### Conflict 4: Can prompt injection be filtered?
**Position A**: Guardrail and detection products claim high detection rates (vendor marketing; not cited).
**Position B**: Willison — "we still don't know how to 100% reliably prevent this"; CaMeL and the
design-patterns paper constrain capability instead of detecting attacks. **Assessment**: Three
independent expert and academic sources favour design constraints. The rule flags capability, not missing
filters.

### Conflict 5: Is the OWASP Top 10 a standard?
**Position A**: OWASP presents it as an awareness document; ASVS is the verifiable standard.
**Position B**: Compliance regimes and contracts cite it as a standard. **Assessment**: Use Top 10 ids for
grouping only; flag by CWE and ASVS.

## Full Citations

[1] Saltzer, J.H.; Schroeder, M.D. "The Protection of Information in Computer Systems". *Proc. IEEE* 63(9):1278–1308. 1975. https://www.cs.virginia.edu/~evans/cs551/saltzer/. Accessed 2026-10-20.
[2] Smith, R.E. "A Contemporary Look at Saltzer and Schroeder's 1975 Design Principles". *IEEE S&P* 10(6):20–25. 2012. https://cryptosmith.com/2013/10/19/security-design-principles/. Accessed 2026-10-20.
[3] Ross, R.; Winstead, M.; McEvilley, M. *Engineering Trustworthy Secure Systems*. NIST SP 800-160 Vol. 1 Rev. 1. 2022. https://csrc.nist.gov/pubs/sp/800/160/v1/r1/final. Accessed 2026-10-20.
[4] Johnsson, D.B.; Deogun, D.; Sawano, D. *Secure by Design*. Manning. 2019. https://www.manning.com/books/secure-by-design. Accessed 2026-10-20.
[5] Kohnfelder, L. *Designing Secure Software*. No Starch. 2021. https://nostarch.com/designing-secure-software. Accessed 2026-10-20.
[6] Kohnfelder, L.; Garg, P. "The Threats to our Products". Microsoft *Interface*. 1999-04-01. https://threatmodelingbook.com/files/microsoft/The-Threats-To-Our-Products.docx. Accessed 2026-10-20.
[7] Shostack, A. *Threat Modeling: Designing for Security*. Wiley. 2014. Four-Question Framework: https://github.com/adamshostack/4QuestionFrame. Accessed 2026-10-20.
[8] Anderson, R. *Security Engineering*, 3rd ed. Wiley. 2020. https://www.cl.cam.ac.uk/~rja14/book.html. Accessed 2026-10-20.
[9] McGraw, G. *Software Security: Building Security In*. Addison-Wesley. 2006. (catalog records via search). Accessed 2026-10-20.
[10] Howard, M.; LeBlanc, D. *Writing Secure Code*, 2nd ed. Microsoft Press. 2002/2003. https://informit.com/store/writing-secure-code-9780735687240. Accessed 2026-10-20.
[11] Howard, M.; LeBlanc, D.; Viega, J. *24 Deadly Sins of Software Security*. McGraw-Hill. 2010. https://oreilly.com/library/view/24-deadly-sins/9780071626750. Accessed 2026-10-20.
[12] Seacord, R.C. *Secure Coding in C and C++*, 2nd ed. Addison-Wesley. 2013. https://www.oreilly.com/library/view/secure-coding-in/9780132981989. Accessed 2026-10-20.
[13] Ferguson, N.; Schneier, B.; Kohno, T. *Cryptography Engineering*. Wiley. 2010. https://www.schneier.com/books/cryptography-engineering. Accessed 2026-10-20.
[14] Adkins, H. et al. *Building Secure and Reliable Systems*. O'Reilly. 2020. https://sre.google/books/building-secure-reliable-systems/. Accessed 2026-10-20.
[15] Zalewski, M. *The Tangled Web*. No Starch. 2011. https://nostarch.com/tangledweb. Accessed 2026-10-20.
[16] Dowd, M.; McDonald, J.; Schuh, J. *The Art of Software Security Assessment*. Addison-Wesley. 2006. https://www.oreilly.com/library/view/the-art-of/0321444426/. Accessed 2026-10-20.
[17] Aumasson, J.-P. *Serious Cryptography*, 2nd ed. No Starch. 2024. https://nostarch.com/serious-cryptography-2nd-edition. Accessed 2026-10-20.
[18] Madden, N. *API Security in Action*. Manning. 2020. https://www.manning.com/books/api-security-in-action. Accessed 2026-10-20.
[19] MITRE / CISA. "2025 CWE Top 25 Most Dangerous Software Weaknesses". 2025. https://cwe.mitre.org/top25/archive/2025/2025_cwe_top25.html. Accessed 2026-10-20.
[20] MITRE. "CWE-1427: Improper Neutralization of Input Used for LLM Prompting". CWE 4.16. 2024. https://cwe.mitre.org/data/definitions/1427.html. Accessed 2026-10-20.
[21] OWASP. *OWASP Top 10:2025*. https://top10.owasp.org/2025/. Accessed 2026-10-20.
[22] OWASP. *Application Security Verification Standard* 5.0.0. 2025. https://owasp.org/www-project-application-security-verification-standard/ ; https://github.com/OWASP/ASVS/tree/master/5.0/en. Accessed 2026-10-20.
[23] OWASP. *Cheat Sheet Series*. https://cheatsheetseries.owasp.org/ ; Cryptographic Storage Cheat Sheet. Accessed 2026-10-20.
[24] SEI / CMU. *SEI CERT Coding Standards*. https://wiki.sei.cmu.edu/confluence/. Accessed 2026-10-20.
[25] Temoshok, D. et al. *Digital Identity Guidelines: Authentication and Authenticator Management*. NIST SP 800-63B-4. 2025. https://pages.nist.gov/800-63-4/sp800-63b.html. Accessed 2026-10-20.
[26] Wiggins, A. et al. *The Twelve-Factor App*, "III. Config". https://12factor.net/config. Accessed 2026-10-20.
[27] NIST. "Comment on NIST SP 800-131A Revision 3". 2024. https://csrc.nist.gov/news/2024/comment-on-nist-sp-800-131a-revision-3. Accessed 2026-10-20.
[28] Egele, M.; Brumley, D.; Fratantonio, Y.; Kruegel, C. "An Empirical Study of Cryptographic Misuse in Android Applications". *ACM CCS '13*, 73–84. 2013. https://seclab.cs.ucsb.edu/publications/egele2015an_empirical/. Accessed 2026-10-20.
[29] Thompson, K. "Reflections on Trusting Trust". *CACM* 27(8):761–763. 1984. https://inst.eecs.berkeley.edu/~cs161/fa08/papers/p761-thompson.pdf. Accessed 2026-10-20.
[30] OpenSSF. *SLSA Specification* v1.2. https://slsa.dev/spec/. Accessed 2026-10-20.
[31] Souppaya, M.; Scarfone, K.; Dodson, D. *SSDF v1.1*. NIST SP 800-218. 2022. https://csrc.nist.gov/pubs/sp/800/218/final ; Rev. 1 ipd: https://csrc.nist.gov/pubs/sp/800/218/r1/ipd. Accessed 2026-10-20.
[32] OpenSSF. *Scorecard*. https://github.com/ossf/scorecard. Accessed 2026-10-20.
[33] OpenSSF Best Practices WG. *Concise Guide for Evaluating Open Source Software*. 2025-03-28. https://best.openssf.org/Concise-Guide-for-Evaluating-Open-Source-Software. Accessed 2026-10-20.
[34] npm. "Details about the event-stream incident". 2018. https://blog.npmjs.org/post/180565383195/details-about-the-event-stream-incident. Accessed 2026-10-20.
[35] Birsan, A. "Dependency Confusion: How I Hacked Into Apple, Microsoft and Dozens of Other Companies". Medium. 2021-02. Corroborated by https://www.bleepingcomputer.com/news/security/researcher-hacks-microsoft-apple-more-in-novel-supply-chain-attack/. Accessed 2026-10-20.
[36] NIST NVD. "CVE-2024-3094". 2024-03-29. https://nvd.nist.gov/vuln/detail/CVE-2024-3094. Accessed 2026-10-20.
[37] Ladisa, P.; Plate, H.; Martinez, M.; Barais, O. "SoK: Taxonomy of Attacks on Open-Source Software Supply Chains". IEEE S&P 2023. https://arxiv.org/abs/2204.04008. Accessed 2026-10-20.
[38] Greshake, K. et al. "Not What You've Signed Up For". *AISec '23*, 79–90. 2023. DOI 10.1145/3605764.3623985. https://arxiv.org/abs/2302.12173. Accessed 2026-10-20.
[39] Willison, S. "The lethal trifecta for AI agents: private data, untrusted content, and external communication". 2025-06-16. https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/. Accessed 2026-10-20.
[40] Willison, S. "Design Patterns for Securing LLM Agents against Prompt Injections" (review). 2025-06-13. https://simonwillison.net/2025/Jun/13/prompt-injection-design-patterns/. Accessed 2026-10-20.
[41] OWASP GenAI Security Project. *2025 Top 10 for LLMs and Gen AI Apps*. https://genai.owasp.org/llm-top-10/. Accessed 2026-10-20.
[42] Debenedetti, E. et al. "Defeating Prompt Injections by Design". arXiv:2503.18813. 2025. https://arxiv.org/abs/2503.18813. Accessed 2026-10-20.
[43] Beurer-Kellner, L. et al. "Design Patterns for Securing LLM Agents against Prompt Injections". arXiv:2506.08837. 2025. https://arxiv.org/abs/2506.08837. Accessed 2026-10-20.
[44] Vassilev, A. et al. *Adversarial Machine Learning: A Taxonomy and Terminology of Attacks and Mitigations*. NIST AI 100-2 E2025. 2025. https://csrc.nist.gov/pubs/ai/100/2/e2025/final. Accessed 2026-10-20.
[45] Microsoft. "Security Development Lifecycle practices". https://www.microsoft.com/en-us/securityengineering/sdl/practices. Accessed 2026-10-20.
[46] OWASP. *SAMM v2 model*. https://owaspsamm.org/model/. Accessed 2026-10-20.
[47] Black Duck. *BSIMM15*. 2025. https://www.blackduck.com/resources/analyst-reports/bsimm.html. Accessed 2026-10-20.
[48] Hoffman, A. *Web Application Security*, 2nd ed. O'Reilly. 2024. https://www.oreilly.com/library/view/-/9781098143923 (403 to automated fetch); https://helion.pl/ksiazki/e_3rz7.htm. Accessed 2026-10-20.

## Research Metadata

Examined: ~60 pages | Cited: 47 | Crossref citation counts retrieved: 5 papers | Confidence by finding:
High ≈ 60%, Medium ≈ 30%, Low ≈ 10% (the Low items are the unconfirmed dates and the Agentic Top 10) |
Tool failures: Egele PDF (TLS error); NVD HTML page (empty; API used instead); owasp.org Top 10 redirects |
Output: docs/research/security/software-security-canonical-sources.md
