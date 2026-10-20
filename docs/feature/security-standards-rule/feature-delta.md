<!-- markdownlint-disable MD024 -->
# Feature Delta — security-standards-rule

Wave: DISCUSS ✓ (2026-10-20) · Density: lean
Build path: DISCUSS here, then the rule is written directly — the deliverable is prose, so DESIGN,
DISTILL and DELIVER stay out (edd-loop DDD8). Rules are not a plugin component, so no plugin-dev schema
applies to `rules/security.md` itself; `plugin-dev:skill-reviewer` reviews the `review-code` change.

This feature adds the plugin's first security standard, `rules/security.md`, and makes
`/phil:review-code` apply it. It is grounded in
`docs/research/security/software-security-canonical-sources.md`, as `ux.md` is grounded in
`docs/research/ux/`.

---

## Wave: DISCUSS / [REF] The gap, measured

Measured 2026-10-20 against `main` at `f59a0d8`:

- **No rule owns security.** Of 23 files in `rules/`, none does. Four lines touch it, each owned by a
  rule about something else: `react.md:52` (`dangerouslySetInnerHTML`), `architecture.md:67` (secrets
  injected at runtime), `continuous-delivery.md:66,74` (pinned versions, for reproducibility).
- **The reviewer has one bullet and no standard.** `skills/review-code/SKILL.md:75` lists "Security
  vulnerabilities (injection, unsanitized input)" under Priority 1. Nothing tells it what counts, what
  to cite, or what not to flag, so it reviews from general knowledge — the condition every other
  Priority exists to end.
- **Third-party packages, secrets, authorization, cryptography and agent security** have no mention
  anywhere in `rules/`. `llm-inference.md` covers serving models and says nothing about prompt
  injection.
- **This repo's own code is the dogfood surface.** 17 non-test Python, shell and JS files; six shell
  out or call a forge (`hooks/decision-request/check-ask.py`, `scripts/probe-board.py`,
  `scripts/check-invariants.py`, `scripts/check-plugin-skew.py`, `scripts/check-tests.py`,
  `scripts/plain_language.py`). `check-ask.py` is a hook that reads model-composed text — the agent
  half's own case.

## Wave: DISCUSS / [REF] Pre-requisites

- **Research precursor (D1), done:** `docs/research/security/software-security-canonical-sources.md`,
  48 sources, 2026-10-20. `@infrastructure` — it lands as a precursor commit, not a slice.
- **Verification precursor (D5), not done:** 24 CWE ids in the research table come from the
  researcher's prior knowledge (its Gap 7). Each is opened on cwe.mitre.org before slice 01 ships.
- **Existing artifacts touched:** `rules/security.md` (new), `skills/review-code/SKILL.md`,
  `skills/review-code/self-test/`, `README.md`, `.claude-plugin/plugin.json`, `docs/product/jobs.yaml`,
  `docs/product/personas/quinn-codebase-steward.yaml`.

## Wave: DISCUSS / [REF] Persona ID

**`quinn-codebase-steward`, extended with a facet — no new persona.** Quinn already owns the health of
a codebase and already runs `/phil:review-code`; a security defect is a health defect the reviewer
cannot yet name. Same person, same command, one more thing it must catch.

**Rejected: a new "security reviewer" persona.** This repo earns a new persona only for a position
orthogonal to every domain, as `ari-interrupted-decider` is. A developer reviewing a diff is Quinn's
position exactly. **Rejected: `devon-ui-developer`** — XSS reaches UI files, but most rows (shell,
deserialisation, secrets, supply chain, agents) never touch one.

## Wave: DISCUSS / [REF] JTBD one-liner

**New job: `catch-security-defects-in-review`.**

> When I review a change, I want the objective security defects in it flagged by the weakness they are
> and the fix that closes them — and the false alarms left alone — so I can stop shipping
> vulnerabilities without carrying CWE, ASVS and NIST in my head or drowning in scanner noise.

Not a facet of `catch-ux-violations-while-building-ui`: different readers, different standards, and a
different failure — a missed UX defect annoys a user, a missed security defect hands an attacker the
system. Recorded in `docs/product/jobs.yaml` with dimensions and forces.

## Wave: DISCUSS / [REF] Locked decisions

| ID | Decision | Rationale |
|----|----------|-----------|
| D1 | **Research is a precursor**, done. | The `ux-standards-rule` and `mobile-web-standards` bar; "empirical design over speculation". |
| D2 | **One new rule, `rules/security.md`.** No separate supply-chain rule; no CERT language rules. | One reviewer reads one standard. Supply chain is six rows and one advisory question, too few to own a file. CERT ids are language-specific and belong in `cpp.md` if anywhere. |
| D3 | **Two halves, split on checkability**, labeled as `clean-craftsmanship.md` labels its standards and its oath: **Principles** extracted from books and papers, and a reviewer half shaped like `ux.md` — **Always-flag**, **Advisory**, **Do not flag**. | Nearly nothing in the principles works can be checked in a diff; the standards can. Mixing them lends design advice the authority of a CWE id. |
| D4 | **Every always-flag row is keyed by CWE id.** ASVS is cited at **chapter** level, stamped `v5.0.0`. OWASP Top 10 ids group rows and are never a finding. A dated line names the editions the table was checked against. | CWE ids are stable for decades; ASVS says its own item ids "may change between versions", so a chapter outlives an item; the Top 10 calls itself an awareness document. Closes research Gap 2 by decision rather than by lookup. |
| D5 | **Every CWE id is opened on cwe.mitre.org before it ships.** | Research Gap 7. A wrong id is a citation a reader trusts and cannot check. |
| D6 | **`review-code` Priority 1 reads `security.md`**, names each security finding by its CWE id, takes the fix from the row, honours Do not flag, and routes `report only`. | The bullet at `SKILL.md:75` is where the standard was always missing. Priority 1 items already route `report only`. Satisfies `check-rule-reachability.py`. |
| D7 | **Agent and hook rows live in `security.md`**, keyed to CWE-1427 and OWASP LLM 2025 ids — not in `llm-inference.md`. | `llm-inference.md` is serving reference and unreached by design. Prompt injection is injection; its sink rows reuse CWE-78/94/79/22. |
| D8 | **Complement, do not restate.** `react.md` keeps `dangerouslySetInnerHTML`; `architecture.md` keeps runtime secret injection; `continuous-delivery.md` keeps pinning for reproducibility. `security.md` states the general form once and points. | The ownership-paragraph pattern every newer rule follows. |
| D9 | **NIST SP 800-63B-4 governs password rows.** Composition rules and forced rotation are flagged; their absence is never flagged. A project overrides by declaration. | The newer, evidence-based federal standard; research Conflict 3. |
| D10 | **Flag the capability, never a missing filter.** For prompt injection, flag the lethal trifecta and the over-broad grant; never demand a detector. | Willison, CaMeL and the design-patterns paper agree from independent author groups; research Conflict 4. |
| D11 | **The rule states what is its own.** A Sources section names which rows, wordings and the split are this rule's synthesis, and that the rule was written from the research document, not from the books in hand. | `test-patterns.md` "Sources and Synthesis" and `agent-instructions.md` "Evidence" set the pattern. |
| D12 | **`paths:` mirrors `coding.md`'s code globs plus CI and container config.** | Rows F29 and F30 live in workflows and Dockerfiles. The globs take effect only for a consumer who copies the rule. |

## Wave: DISCUSS / [REF] Driving ports

- **`/phil:review-code`** — Priority 1 applies the always-flag table to the files it reads and writes
  CWE-named items to `.refactoring-backlog.md`.
- **The rule file itself** — read by any skill that names it, and by a consumer who copies it into
  `.claude/rules/`.

## Wave: DISCUSS / [REF] WS strategy

**A — none.** Additive, brownfield, one new file and one edited skill. Slice 01 is the thinnest
end-to-end value: a review that names a security defect by CWE.

## Wave: DISCUSS / [REF] Scope Assessment: PASS

Three slices, two precursors, one context (the rules and review system), no integration point beyond
`review-code`. No oversized signal fires. Each slice runs against this repo's own hooks and scripts as
production data, beside a seeded fixture.

## Wave: DISCUSS / [REF] User stories

All stories trace to `job_id: catch-security-defects-in-review`.

### US-01 — `review-code` flags classic security defects by CWE *(walking-skeleton slice)*

**Problem.** Quinn runs `/phil:review-code` on a change that builds a shell command from an issue
title. The reviewer may catch it, may call it "unsanitized input", and may also flag an MD5 cache key
beside it. Nothing decides which.

**Solution.** `rules/security.md` with its Always-flag table (rows F1–F30 of the research, each keyed
by CWE id, ASVS chapter and preferred form) and its Do not flag list; `review-code` Priority 1 reads it.

#### Elevator Pitch
Before: a review names security defects by impression, with no id, no fix and no false-alarm discipline.
After: run `/phil:review-code scripts/` → sees backlog items such as `Priority 1 — CWE-78: shell
command built from untrusted data — pass an argv list` and no item for an MD5 used as a cache key.
Decision enabled: which security defects to fix before the change merges.

#### Acceptance Criteria
- [ ] `rules/security.md` exists with an Always-flag table of at least the 30 classic rows; each row
      names the defect, the CWE id, the ASVS 5.0.0 chapter and the preferred form.
- [ ] Every CWE id in the table was opened on cwe.mitre.org (D5), and the file carries a dated line
      naming the CWE, ASVS and NIST editions checked.
- [ ] A Do not flag list covers at least: non-security hashes and RNGs, test and example credentials,
      constant-built queries, deliberately public routes, internal calls crossing no boundary, and
      the absence of NIST-forbidden password rules.
- [ ] `review-code` Priority 1 names `rules/security.md`, requires the CWE id in the item's Smell
      field, and honours Do not flag.
- [ ] A new self-test fixture seeds at least six always-flag defects and four Do-not-flag decoys;
      the expected backlog holds every defect with its CWE id and none of the decoys.
- [ ] `python3 -m pytest -q` and `scripts/check-invariants.py` stay green.

### US-02 — Principles and Advisory: the half no diff can check

**Problem.** A change adds a hook that reads issue bodies, or a new dependency one letter from a
popular one. Neither is a defect on a line; both are where the next defect comes from.

**Solution.** A Principles half — Saltzer and Schroeder's surviving principles with Smith's triage,
security as a design property (*Secure by Design*), trust boundaries and the four questions (Shostack,
Kohnfelder), safe-by-construction APIs (Google), and the supply-chain principle (Thompson) — plus an
Advisory list the reviewer raises and the author decides, including the three new-dependency questions.

#### Elevator Pitch
Before: a review has nothing to say about a new trust boundary or a new dependency.
After: run `/phil:review-code --changes` on a change adding a package → sees an Advisory item asking
whether the package is needed, authentically named and maintained by more than one person.
Decision enabled: whether to adopt the dependency, or threat-model the new boundary, before merging.

#### Acceptance Criteria
- [ ] The Principles half cites each work by title and states what it contributes, with no item
      phrased as a checkable flag.
- [ ] The Advisory list carries at least the new-trust-boundary and new-dependency questions, and is
      labelled as raised, not blocking.
- [ ] `review-code` raises Advisory items as findings the author decides, distinguishable from
      Always-flag items in the backlog.

### US-03 — Agent and hook rows

**Problem.** This plugin is prompts, hooks and scripts that run inside an agent. A hook that pastes a
PR body into a prompt holding a shell is injection with no CWE row to cite.

**Solution.** Agent rows (research F31–F36) keyed to CWE-1427 and OWASP LLM 2025 ids, with the six
design patterns as the preferred form, and the D10 do-not-flag: never demand a detector.

#### Elevator Pitch
Before: a review of a hook that feeds model output to a shell finds nothing to name.
After: run `/phil:review-code hooks/` → sees `Priority 1 — CWE-1427 / LLM01:2025: untrusted issue text
in a prompt that holds a shell — separate the planner from the reader (Dual LLM)`.
Decision enabled: whether the hook's design must change before it ships.

#### Acceptance Criteria
- [ ] Agent rows cover at least: untrusted text in a privileged prompt, model output reaching a sink,
      the lethal trifecta, over-broad tool grants, secrets in a prompt, and an unbounded agent loop.
- [ ] Do not flag holds "a missing prompt-injection filter".
- [ ] The fixture from US-01 gains at least two agent defects and one agent decoy.

## Wave: DISCUSS / [REF] Out-of-scope

- Language-specific secure-coding rules (CERT C/C++/Java); a pointer from `cpp.md` is a later card.
- A security command of its own (`/phil:security-review`). `review-code` applies the rule.
- Running scanners (SAST, dependency audit) or adding them to CI.
- Applying agent rows to Markdown frontmatter grants. `check-readonly-commands.py` already enforces
  command grants; extending `harden-instructions` to agents and skills is a card.
- Item-level ASVS ids (D4).
- Threat-modelling this repo.

## Wave: DISCUSS / [REF] Definition of Done

1. The research precursor is committed and the rule cites it.
2. Every CWE id was opened on cwe.mitre.org; the dated editions line is present.
3. `rules/security.md` holds both halves, labelled by checkability, with an ownership paragraph.
4. `review-code` Priority 1 names the rule and the CWE-id requirement.
5. The self-test fixture passes its own suite green, and its expected backlog pins every seeded
   defect and excludes every decoy.
6. A dogfood run of `/phil:review-code` over `hooks/` and `scripts/` is recorded, naming the
   version or saying the skill's prose was driven by hand.
7. README's Rules list names `security`; the plugin version is bumped.
8. `python3 -m pytest -q`, `scripts/check-invariants.py` and `scripts/check-rule-reachability.py` pass.
9. The commit message names that `nw-discuss` ran and which `plugin-dev` reviewers ran.

## Wave: DISCUSS / [REF] Outcome KPIs

- **Who:** a developer running `/phil:review-code` on a change.
- **Does what:** gets each objective security defect named by CWE id with its fix.
- **By how much:** every seeded always-flag defect surfaced with the right CWE (10 of 10 across
  US-01 and US-03, as delivered); zero items on the decoys (0 of 6).
- **Measured by:** the self-test fixture, plus the dogfood run over this repo's hooks and scripts.
- **Baseline:** no rule; the reviewer's one bullet names no id and no exemption.

## Wave: DISCUSS / [REF] DoR validation

All nine items pass: job traceable (new job in `jobs.yaml`); persona exists (Quinn, extended); ACs
testable against a fixture; KPIs numeric; scope assessed; evidence base decided (D1) with its one open
verification named (D5); structure decided (D2, D3, D4); boundaries with existing rules named (D8);
out-of-scope listed.

## Wave: DISCUSS / [REF] Slice briefs

- `docs/feature/security-standards-rule/slices/slice-01-always-flag-by-cwe.md`
- `docs/feature/security-standards-rule/slices/slice-02-principles-and-advisory.md`
- `docs/feature/security-standards-rule/slices/slice-03-agent-and-hook-rows.md`

## Wave: DISCUSS / [REF] Handoff

Order: research precursor → CWE verification (D5) → slice 01 → slice 02 → slice 03. Slice 01 carries
the highest uncertainty — whether 30 rows stay readable and whether the decoys hold — so it goes first.

## Wave: DISCUSS / [REF] Delivered and dogfooded (2026-10-20)

All three slices landed together in `57f7d8b` (1.2.0); the rule was drafted whole, so the slices did
not ship separately. Fixture 02 grew from eight seeded defects to ten when its first drive filed two
correct items the fixture had not listed (CWE-297, CWE-250).

**Fixture drive.** A fresh agent followed this working tree's `SKILL.md` over fixture 02, reading only
the code: 8 of the 8 then-listed defects, 0 of 6 decoys, both guard-elsewhere cases sent to Advisory.

**Dogfood run.** A fresh agent followed this working tree's `SKILL.md`, Priority 1 security only,
over `hooks/` and `scripts/` — the released copy was not run. Seven items, two confirmed by executing
the code:

| Item | File | Finding |
|---|---|---|
| CWE-636 | `hooks/refactor-loop/block-test-file-write.py` | Guard G2 fails open: an undecodable ledger, or a non-object `tool_input`, lets a test-file write through. Confirmed by running the hook. |
| CWE-1333 | `scripts/plain_language.py` | Path regexes backtrack quadratically; `check-ask.py` scans the whole question even after it fails the word ceiling. 1.0 s on 20,000 characters, measured. |
| CWE-88 | `scripts/probe-board.py` | `--repo` reaches `gh repo view` positionally with no leading-dash guard; the only check is `"/" in args.repo`. |
| CWE-943 | `scripts/probe-board.py` | GraphQL queries `%`-format owner and name into string literals; seven sites, one fix (GraphQL variables). |
| CWE-1427 | `scripts/render-block.py` | Forge-supplied project, view, option and workflow names are written verbatim into `CLAUDE.md`, which every later session loads. |
| CWE-1427 | `scripts/render-block.py` | Label names from the board are written verbatim into the declared region. |
| Advisory | `hooks/refactor-loop/reinject-pinned-constraints.py` | Ledger lines re-injected as context; a cloned repo can commit a ledger. Unregistered today. |

**Where the rule made the reviewer hesitate** — candidate refinements, not yet applied:

1. *(Applied, 1.2.1.)* Model output is untrusted only where the code grants more than the model's own
   grant; a script that writes a path the model could write directly grants nothing.
2. *(Applied, 1.2.3.)* A sink an earlier, unrelated call happens to protect has no stated tier.
3. *(Applied, 1.2.3.)* CWE-636 needs a scope: a deny that is not a security control (a wording standard) is outside it.
4. *(Applied, 1.2.3.)* CWE-1333's threshold: whether "overlapping quantifiers" covers a class beside a literal it matches.
5. *(Applied, 1.2.3.)* One defect matching two ids of one row: file the most specific, not both.
6. *(Applied: forge metadata 1.2.1, the instruction-file row 1.2.2.)* CWE-1427's Preferred form assumes a live session; a write into an instruction file needs its own
   fix (render as inert data, or keep it out), and forge metadata belongs in the untrusted list.
7. *(Applied, 1.2.1.)* An untrusted status the code cannot show belongs with the trust-boundary
   Advisory, unstated today.
8. *(Applied, 1.2.4: CWE-180, CWE-807, and an Advisory bullet for CWE-312.)* No row for an uncanonicalised path in a guard, a guard its subject can disable, or verbatim
   transcripts written at default permissions.
9. Do not flag held cleanly: a SHA-1 compare-and-swap fingerprint and list-form `subprocess.run`.

Each refinement changes what the rule asserts, so per `CLAUDE.md` it folds into `rules/security.md`
with a fixture that would have caught it and a version bump. The seven findings are defects in this
repo and belong on the board.

**Fixture drives after the refinements (2026-10-20).** Fresh agents drove the working tree's `SKILL.md`
over fixtures 02 to 05, reading only each fixture's code. At 1.2.4, fixtures 04 and 05 passed. Fixtures
02 and 03 made every judgement right but paraphrased three Preferred forms each, which a strict match
refuses and a reader cannot trace to its row. At 1.2.5 the skill requires the form verbatim, and a
mechanical grade (id, verbatim prefix, lines ±2, decoys) passed both: 10 of 10 and 4 of 4, no
security item on a decoy, no extra security item.

**Skill review of the 1.2.3 and 1.2.5 changes (2026-10-20).** `plugin-dev:skill-reviewer` had reviewed
`review-code` only at 1.2.0. Run over the later two changes, it rated them "needs improvement": "most
specific" settled only parent-child pairs, the fixtures' own verdicts disagreed under any single test,
the instance the skill required appeared in no expected item and was forbidden by the test, and
deferring or menu-shaped forms copied verbatim named no one fix. 1.2.6 answers each. Re-driven:
fixture 04 passed, and fixture 02 passed after one more sharpening — the first 1.2.6 drive folded
CWE-250 into CWE-1427, which the independent-restoration test now separates.
