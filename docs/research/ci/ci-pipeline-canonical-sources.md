# Research: Canonical Sources for a Vendor-Neutral CI-Pipeline Rule

**Date**: 2026-10-21 | **Researcher**: nw-researcher (Nova) | **Confidence**: High for triggering, gating, rework and flaky-retry rows; Medium for change-scoped and mutation rows and the id mapping; Low for the Goldratt and Reinertsen quotations | **Sources**: 60

> Input to a future `rules/ci-pipelines.md` with two halves: **Principles** (book- and paper-extracted
> shape, trigger, scope, speed and rework guidance) and an **always-flag reviewer table** (objective
> defects a pipeline file shows, each citing a source id).
> Each finding uses: **Work** / **Evidence** / **Canonicity** / **Contributes** / **Checkable in a pipeline file?** / **Caveats**.
> Access date for every web source: 2026-10-21 unless stated.
> Scope: complements `rules/continuous-delivery.md` (stages, build once, trunk-based, deterministic
> pipeline) and `rules/security.md` (mutable tags, `pull_request_target`, lockfile installs, CI token).

## Executive Summary

CI-pipeline guidance splits along the line `security.md` draws. **Principles** come from a few works:
Fowler's "Continuous Integration" (2024 revision) and DORA's capability pages say every push builds and
feedback arrives within about ten minutes; *Software Engineering at Google* supplies the presubmit /
post-submit split — fast, reliable, change-scoped tests before merge, everything after — and TAP's
dependency-graph test selection; trunkbaseddevelopment.com settles that "branch, open MR, merge on
green" *is* trunk-based development if the branch lives at most about two days, review wait included.
Goldratt's constraint thinking and Reinertsen's U-curve supply the speed-up procedure: shorten only the
critical path, and stop where the cost of the change exceeds the delay it saves. Humble & Farley's
"Only build packages once", already in `continuous-delivery.md`, gains a checkable form from SLSA v1.2:
verify the provenance subject digest "before use (e.g. during installation or deployment)".

**Change-scoped testing and mutation** are well supported but never alone. Memon et al. (210 Crossref
citations), Ekstazi (187) and Nx's docs show that selection is safe only relative to the dependencies
it tracks — file-level, not class-level, and with a lockfile change forcing everything (Nx's default).
Machalica et al. accept missing up to 5% of failures, so main must run the full suite. Google's
diff-based mutation at code review (Petrović & Ivanković 2018; TSE 2022) backs mutating only changed
code in the MR; every tool's incremental mode admits staleness, which justifies a scheduled full pass.
Docs-only skipping is a vendor-supported cost measure, but secret scanning must still run: Meli et al.
(NDSS 2019) found about one in five secret-bearing files were neither code nor key files, and both
GitLab's "Pipelines must succeed" and GitHub's required checks block a change that produces no status.

**For the reviewer half**, no CWE-like standard exists, but Zampetti et al. (EMSE 2020, 87 citations)
supply a peer-reviewed catalogue of 79 CI bad smells with stable ids (R, I, BP, BM, Q, D, C), and CD-Linter
(ESEC/FSE 2020) shows a subset is detectable in `.gitlab-ci.yml` at 87% precision. Twenty-one candidate
always-flag rows (P1–P21) result, keyed to Zampetti ids plus vendor docs, with `security.md`'s CWE rows
cross-referenced rather than restated. Two caveats limit the rows: Zampetti's practitioners rejected
"no parallelism", "aborting obsolete builds" and "re-running failed tests" as smells, so speed rows stay
advisory and the retry row is Medium; and several details — CI-config changes forcing a full run, a
weekly mutation cadence, cancel-on-main — are interpretation. See Knowledge Gaps.

## Research Methodology
**Search Strategy**: Primary sources first — vendor documentation for platform behaviour
(docs.gitlab.com, docs.github.com, nx.dev, bazel.build, stryker-mutator.io, pitest.org, mutants.rs,
docs.docker.com, slsa.dev), the authors' own sites for books (continuousdelivery.com, martinfowler.com,
abseil.io), DORA's capability pages, and arXiv, research.google, author and course-hosted PDFs for papers.
Crossref's `is-referenced-by-count` gave citation counts for every paper with a DOI; no count was
guessed. Compressed PDFs were read page by page.
**Source Selection**: Types: academic, official, technical docs; secondary summaries used only for book
quotations and marked unverified. Reputation: high or medium-high for every row-bearing claim.
**Verification**: Each principle cross-referenced across independent groups (e.g. the ten-minute
ceiling across Fowler, DORA and Zampetti BP27; no blanket retry across UIUC, Google and Fowler). The
Zampetti, CD-Linter and CI-Odor papers share authors and count as one group.
**Quality Standards**: Target 3 sources per major claim, 1 authoritative minimum; unconfirmed facts are
marked in place and collected in Knowledge Gaps. Avg reputation ≈ 0.88.

---

## Findings

## 1. Principles: books, articles and DORA

### 1.1 Fowler, "Continuous Integration" (2024 revision)

**Work**: Martin Fowler. "Continuous Integration". martinfowler.com, revised 2024-01-18 (first version
2000, rewritten 2006). https://martinfowler.com/articles/continuousIntegration.html (industry leader,
medium-high; the article that named the practice for most of the industry).
**Evidence**: "For most projects, however, the XP guideline of a ten minute build is perfectly within
reason." "Nothing sucks the blood of Continuous Integration more than a build that takes a long time."
The deployment pipeline is "also known as build pipeline or staged build"; "The commit build is the build
that's needed when someone pushes commits to the mainline." "Every time the mainline receives a commit,
the CI service checks out the head of the mainline" and builds; "By ensuring we have a build with every
push, should we get a failure, we know that the fault lies in that latest push." On branches: "Teams using
feature branches will usually expect everyone to pull from mainline regularly, but this is
semi-integration"; "The pre-integration code review can be problematic for Continuous Integration"; "no
code sits on a branch longer than a few hours". Broken builds: "nobody has a higher priority task than
fixing the build" (Kent Beck), and "the best way to fix the build is to revert the latest commit from the
mainline." The article does **not** discuss flaky tests.
**Canonicity**: The definition *Software Engineering at Google* (1.4) quotes as its starting point. 2024
revision is the current text.
**Contributes**: The ten-minute commit-build ceiling; "every push to mainline triggers a build" (supports
the candidate row that main runs a full pipeline); the tension between pre-merge review and CI (see
Conflicting Information 1).
**Checkable in a pipeline file?** Partly. A pipeline file shows whether a push to the default branch
triggers a build. The ten-minute ceiling is checkable only from run history, not the file.
**Caveats**: Fowler treats feature branches and CI as in tension; the candidate row "branch, open MR,
merge on green" is compatible only under the branch-lifetime limit in 1.2. `continuous-delivery.md`
already owns "Keep the build under ten minutes" and "Fix broken builds immediately"; cross-reference, do
not restate.

### 1.2 trunkbaseddevelopment.com, "Short-Lived Feature Branches"

**Work**: Paul Hammant et al. https://trunkbaseddevelopment.com/short-lived-feature-branches/ (named in
the task's trusted list as official for its own subject). Site copyright 2017–2020; page undated; source
commit d04872f shown.
**Evidence**: "Simply put, the branch should only last a couple of days." Such branches "only count as
Trunk-Based Development if integrated after a prioritized code review", and "Time spent waiting for
review counts towards the branch's short life." CI daemons verify changes "in advance of commits landing
in the trunk"; checks "(linting, static analysis, tests, coverage and the like)" run by CI against each
pull request. Developers per branch: "one (or two if pair-programming)"; the page now adds that with
agentic coding the unit is one developer and their coding agents.
**Canonicity**: The reference site for trunk-based development; DORA's capability page (1.3) links the
same model.
**Contributes**: **The answer to research question 1's last part.** "Branch, open MR/PR, merge on green"
*is* trunk-based development provided the branch lives at most about two days *including review wait*,
holds one developer (or pair), and CI runs on the PR before merge. This licenses an MR-gated pipeline
inside `continuous-delivery.md`'s trunk-based line rather than against it.
**Checkable in a pipeline file?** The PR-triggered build is (`on: pull_request`, `merge_request_event`).
Branch lifetime is not; it lives in repository history.
**Caveats**: The page now flags that PR review can become the bottleneck "especially with AI agents".

### 1.3 DORA capabilities: Continuous Integration, Trunk-Based Development

**Work**: DORA (Google Cloud). "Capabilities: Continuous integration"
(https://dora.dev/capabilities/continuous-integration/) and "Trunk-based development"
(https://dora.dev/capabilities/trunk-based-development/). dora.dev, official for DORA research; pages
undated; they cite the 2014–2018 *State of DevOps* reports.
**Evidence (CI)**: CI "leads to higher deployment frequency, more stable systems, and higher quality
software." "Each commit should trigger a build of the software." Tests "should run quickly, to give
developers feedback as soon as possible"; the page sets "an upper limit of about 10 minutes" (2018
research). Pitfalls named: not running quick tests on every change; not fixing broken builds — if a fix
takes more than a few minutes, "the change that caused the build to break should be identified and
reverted"; "The tests should not take more than a few minutes to run." Measures: percentage of commits
that trigger a build and tests without manual intervention; "The time it takes between the build breaking
and having it fixed."
**Evidence (TBD)**: Branches "typically last no more than a few hours"; "Have three or fewer active
branches"; "Don't have code freezes and don't have integration phases"; "When code review is laborious
and takes hours or days, developers avoid working in small batches." DORA describes the link to
performance as an association, not proven cause.
**Canonicity**: DORA is the largest longitudinal survey programme on delivery performance (2014–present)
and the basis of *Accelerate* (1.6).
**Contributes**: Empirical support for "every commit triggers build and fast tests" and for a ~10-minute
feedback ceiling; the metric "percentage of commits that run tests without manual intervention" is a
review question for any rule that *skips* tests on some changes (see 2 and 5).
**Checkable in a pipeline file?** The trigger coverage is (does every MR and every push to main run
something?). Duration and branch count are not.
**Caveats**: DORA's "a few hours" branch lifetime is stricter than trunkbaseddevelopment.com's "a couple
of days"; see Conflicting Information 1. DORA's measures are survey-based.

### 1.4 Winters, Manshreck, Wright (eds.), *Software Engineering at Google* (2020), Ch. 23 "Continuous Integration" and Ch. 11 "Testing Overview"

**Work**: Titus Winters, Tom Manshreck, Hyrum Wright (eds.). O'Reilly, March 2020. Free online at
https://abseil.io/resources/swe-book (Google-hosted, high). Ch. 23 by Rachel Tannenbaum (TAP section
by Adam Bender); Ch. 11 by Adam Bender.
**Evidence (Ch. 23)**: "the cost of a bug grows almost exponentially the later it is caught." Presubmit
holds "only fast, reliable ones"; slower or less deterministic tests go to post-submit. Teams typically
limit presubmit to tests for the project where the change is made. TAP's primary selection method is "an
analysis of the downstream dependency graph for every change". A change passing presubmit has "a very
high likelihood (95%+) of passing the rest of the tests", so Google integrates optimistically and runs
larger tests asynchronously after submission. Observed average submit wait under TAP "around 11
minutes"; no formal latency target is stated. "Hermetic tests have two important properties: greater
determinism (i.e., stability) and isolation." Flaky tests may be temporarily removed from presubmit while
investigated; retries are an option.
**Evidence (Ch. 11)**: Small tests "must run in a single process" and may not sleep or do I/O; medium
tests "aren't allowed to make network calls to any system other than localhost"; large tests span
machines. Flakiness: at 0.1% across 10,000 daily tests "you will be investigating 10 flakes per day";
"As you approach 1% flakiness, the tests begin to lose value"; Google's rate "hovers around 0.15%";
rerunning "is only delaying the need to address the root cause".
**Canonicity**: The only book-length account of CI at monorepo scale; free online; widely taught.
**Contributes**: (a) **Presubmit/post-submit split** — the principled basis for "MR runs the fast,
change-scoped, reliable subset; main runs the rest". (b) **Dependency-graph test selection** (TAP) as the
canonical form of "affected tests". (c) Test-size vocabulary for deciding what belongs in the MR
pipeline. (d) The 1% flakiness value threshold.
**Checkable in a pipeline file?** Partly: a job that runs network-dependent (large) tests in the MR
pipeline, or a retry wrapper around a test job, is visible. Test size is visible only where tests are
tagged by size.
**Caveats**: Google-scale numbers (thousands of daily flakes, 11-minute waits) do not transfer to a
small repo; cite the principles, not the numbers.

### 1.5 Humble & Farley, *Continuous Delivery* (2010)

**Work**: Jez Humble, David Farley. *Continuous Delivery: Reliable Software Releases through Build, Test,
and Deployment Automation*. Addison-Wesley, 2010 (ISBN 978-0-321-60191-9 and the 2011 Jolt award are
prior knowledge, **not re-verified this session**). Author's companion site
https://continuousdelivery.com/implementing/patterns/ (Humble; high as the author's own statement).
**Evidence (companion site)**: "every change in version control triggers a process" that builds packages
and runs automated checks. Commit stage: "This first step is optimized so that it takes only a few
minutes to run"; "If this initial commit stage fails, the problem must be fixed immediately." "Only build
packages once", because "the thing we're deploying is the same thing we've tested throughout the
deployment pipeline." "Deploy the same way to every environment." The book's own list "Only build your
binaries once / Binaries should not be environment specific / Deploy the same way to every environment /
Smoke-test your deployments" is reported by secondary summaries (study notes, DZone — medium); the
chapter number (believed Ch. 5, "Anatomy of the Deployment Pipeline") is **not confirmed**.
**Canonicity**: The book that named the deployment pipeline; source of `continuous-delivery.md`.
**Contributes**: Already owned by `continuous-delivery.md` ("Build once, deploy many times"; "Same
process for every environment"; the commit stage). The new rule should **cross-reference**, not restate,
and add only the *checkable* form: a deploy job that compiles, installs build dependencies, or runs
`docker build` instead of fetching the tested artifact (see 7).
**Checkable in a pipeline file?** Yes for the rebuild-in-deploy defect.
**Caveats**: Book text not read this session; quotations are from the author's site.

### 1.6 Forsgren, Humble, Kim, *Accelerate* (2018), and DORA reports

**Work**: Nicole Forsgren, Jez Humble, Gene Kim. *Accelerate: The Science of Lean Software and DevOps*.
IT Revolution, 2018. Bibliographic details from prior knowledge, **not re-verified**.
**Evidence**: DORA's capability pages (1.3), which descend from the book's research, state that
trunk-based development, CI, and prioritising broken-build fixes are "predictive of higher software
delivery performance". *Accelerate* groups 24 capabilities, including version control, deployment
automation, CI, trunk-based development and test automation (count and grouping from prior knowledge,
**not re-verified**).
**Canonicity**: Shingo Publication Award 2019 (prior knowledge, not re-verified); the empirical basis
every later DevOps text cites.
**Contributes**: The empirical warrant for the Principles half: CI and trunk-based development predict
delivery performance. It supplies nothing pipeline-file-checkable.
**Checkable in a pipeline file?** No.
**Caveats**: Survey data with self-reported outcomes; the authors argue for causal inference via
structural equation modelling, which critics dispute (not researched this session).

### 1.7 Kim, Humble, Debois, Willis, Forsgren, *The DevOps Handbook* (2nd ed., 2021)

**Work**: IT Revolution; 1st ed. 2016, 2nd ed. 2021 (prior knowledge, **not re-verified**). Already a
named source of `continuous-delivery.md` (the Three Ways).
**Contributes**: Flow (the First Way) and fast feedback (the Second Way) are already in
`continuous-delivery.md`. Nothing new and checkable was found for this rule; cross-reference only.

### 1.8 Duvall, Matyas, Glover, *Continuous Integration* (2007)

**Work**: Paul M. Duvall, Steve Matyas, Andrew Glover. *Continuous Integration: Improving Software
Quality and Reducing Risk*. Addison-Wesley Signature Series (Fowler), 2007; Jolt award 2008 (prior
knowledge, **not re-verified this session**).
**Evidence**: Not read this session. Its widely reported themes (private builds before commit, the
"integration build", staged builds, fast feedback, reports) overlap Fowler (1.1) and Humble & Farley.
**Contributes**: Historical canonicity only; Fowler's 2024 text supersedes it for currency.
**Checkable in a pipeline file?** Not assessed.
**Caveats**: Listed under Knowledge Gaps; Duvall's "CI anti-patterns" (IBM developerWorks, 2008) were
not located.

### 1.9 Goldratt, *The Goal* (1984) and Reinertsen, *The Principles of Product Development Flow* (2009)

See 6.5 and 6.6.

## 2. Change-scoped testing

Two families exist. **Safe** regression test selection (RTS) runs every test whose dependencies changed
and claims to miss nothing; **predictive** selection drops tests a model judges unlikely to fail and
accepts a known miss rate. Both need a full run somewhere as the safety net.

### 2.1 Memon et al., "Taming Google-Scale Continuous Testing" (ICSE-SEIP 2017)

**Work**: Atif Memon, Zebao Gao, Bao Nguyen, Sanjeev Dhanda, Eric Nickell, Rob Siemborski, John Micco.
ICSE-SEIP 2017, pp. 233–242. DOI 10.1109/ICSE-SEIP.2017.16. https://research.google/pubs/taming-google-scale-continuous-testing/
(Google Research, high).
**Evidence**: "Even with enormous resources dedicated to testing, we are unable to regression test each
code change individually." Findings: "very few of our tests ever fail, but those that do are generally
'closer' to the code they test"; "code recently modified by multiple developers (more than 3) breaks
more often."
**Canonicity**: Crossref is-referenced-by-count **210** (queried 2026-10-21). The standard citation for
test selection at Google; complements TAP's dependency-graph selection (1.4).
**Contributes**: Empirical warrant for change-scoped testing: failures cluster near the changed code, so
running tests "close" to the change finds most breakages.
**Checkable in a pipeline file?** No; it justifies a selection step, which is.
**Caveats**: Google monorepo with Blaze; the distance finding is a correlation.

### 2.2 Machalica et al., "Predictive Test Selection" (ICSE-SEIP 2019)

**Work**: Mateusz Machalica, Alex Samylkin, Meredith Porth, Satish Chandra (Facebook). ICSE-SEIP 2019,
pp. 91–100. DOI 10.1109/ICSE-SEIP.2019.00018. Preprint arXiv:1810.05286 (academic, high).
**Evidence**: Running "all potentially-impacted tests on each change" is infeasible at Facebook's scale;
the learned selector "reduces the total infrastructure cost of testing code changes by a factor of two"
while "guaranteeing that over 95% of individual test failures and over 99.9% of faulty changes" are
still reported.
**Canonicity**: Crossref is-referenced-by-count **110** (2026-10-21). The reference for ML-based
selection in industry.
**Contributes**: The caveat that **predictive selection is unsafe by design** (up to 5% of individual
failures unreported pre-merge). A rule that permits it must keep a full post-merge run. Supports the
candidate row "main runs everything".
**Checkable in a pipeline file?** No.
**Caveats**: Requires training data the size of Facebook's; out of reach for most projects. The rule
should prefer build-graph selection (2.4) and name predictive selection as an option only with a full
run behind it.

### 2.3 Gligoric, Eloussi, Marinov, "Practical Regression Test Selection with Dynamic File Dependencies" (Ekstazi, ISSTA 2015)

**Work**: Milos Gligoric, Lamyaa Eloussi, Darko Marinov. *ISSTA 2015*, pp. 211–222, 2015-07-13. DOI
10.1145/2771783.2771784.
**Evidence**: Ekstazi records, per test, the files it depends on — "either executable code or external
resources" — and skips a test when none changed; it "requires no integration with version-control
systems". Across 615 revisions of 32 open-source projects, end-to-end testing time fell 32% on average
against running all tests, and 54% for longer-running suites. Quoted from the authors' abstract via
search snippets; the abstract file on utexas.edu failed TLS and the paper text was **not read**.
A community summary (AcaWiki, medium) reports the paper's point that "collecting only the classes is not
safe, and hence Ekstazi uses files as dependencies".
**Canonicity**: Crossref is-referenced-by-count **187** (2026-10-21). Adopted by Apache projects (prior
knowledge, not re-verified); the reference safe-RTS tool for Java.
**Contributes**: **What makes selection safe.** Dependencies must include non-code files (config,
resources, fixtures); class-level or source-file-level tracking alone misses tests. This is the basis for
the rule's "force a full run" list.
**Checkable in a pipeline file?** No; it supports the forced-full-run row (P3 in the Synthesis).
**Caveats**: Savings are modest (32%) at file granularity; JVM-specific tool.

### 2.4 Build-graph "affected" selection: Bazel, Nx

**Work**: Bazel query guide, https://bazel.build/query/guide (official for Bazel; no version shown).
Nx "Run Only Tasks Affected by a PR", https://nx.dev/docs/features/ci-features/affected (official for Nx;
no version or date shown).
**Evidence (Bazel)**: "You can use `rdeps(u, x)` to find the reverse dependencies of the targets in `x`
within the transitive closure of `u`"; a file maps to its target with `bazel query path/to/file`; tests
filter with `kind(".*_test rule", ...)`. The guide gives no ready "affected tests" recipe.
**Evidence (Nx)**: Default base is `main`; for CI, "The recommended approach is to set the base SHA to
the latest successful commit" on main. "By default, Nx will mark all projects as affected whenever your
package manager's lock file changes" — "a failsafe in case Nx misses a project that should be affected by
a dependency update"; `projectsAffectedByDependencyUpdates: "all"` is "the safest option but may result in
unnecessary CI work". Tasks with a custom hasher are always selected.
**Canonicity**: Official tool docs; TAP (1.4) is the same idea at Google.
**Contributes**: (a) A tool-native, checkable form of change-scoped testing (`bazel query rdeps`,
`nx affected`). (b) **The lockfile-forces-everything default**, from a vendor that sells affected
selection. (c) Base = last successful main commit, not merge-base alone, so a red main is not masked.
**Checkable in a pipeline file?** Yes: whether the MR job uses an affected command, whether the base is
set, and whether `projectsAffectedByDependencyUpdates` was weakened.
**Caveats**: Gradle's equivalent (build cache and up-to-date checks, not test selection) was not
researched; see Knowledge Gaps.

### 2.5 What must force a full run (synthesis, interpretation)

From 2.3 (non-code files are dependencies), 2.4 (lockfile change marks all affected) and 1.4
(dependency graph): a change-scoped MR pipeline is safe only if any change to the following runs the
full suite:
1. **The dependency manifest or lockfile** — Nx's default; Ekstazi's external-file dependencies.
2. **The CI configuration itself** (`.gitlab-ci.yml`, `.github/workflows/**`, included templates) — a
   change to the selector can hide its own breakage. No source states this directly (**interpretation**;
   see Knowledge Gaps).
3. **Shared test infrastructure** — fixtures, test helpers, conftest, test-runner config — which every
   test depends on (Ekstazi's file dependencies; Bazel rdeps of a shared target is "everything").
4. **Build tool config and toolchain pins** (`nx.json`, `WORKSPACE`/`MODULE.bazel`, `pyproject.toml`
   tool sections, `.tool-versions`).
Confidence: Medium (items 1 and 3 have two sources each; items 2 and 4 are interpretation).

## 3. Mutation testing in CI

### 3.1 Jia & Harman, "An Analysis and Survey of the Development of Mutation Testing" (TSE 2011)

**Work**: Yue Jia, Mark Harman. *IEEE Transactions on Software Engineering* 37(5): 649–678, Sept 2011.
DOI 10.1109/TSE.2010.62.
**Canonicity**: Crossref is-referenced-by-count **1,378** (2026-10-21). The standard survey; every
later mutation paper cites it.
**Contributes**: Canonicity for mutation analysis as a test-adequacy measure, and for its central cost
problem (many mutants, each needing a test run), which motivates every CI-scoping technique below.
Survey text **not read** this session; cite for canonicity only.
**Checkable in a pipeline file?** No.

### 3.2 Petrović & Ivanković, "State of Mutation Testing at Google" (ICSE-SEIP 2018)

**Work**: Goran Petrović, Marko Ivanković (Google). *ICSE-SEIP '18*, pp. 163–171, 2018-05-27. DOI
10.1145/3183519.3183521. https://research.google/pubs/state-of-mutation-testing-at-google/ (high).
**Evidence**: "we present a diff-based probabilistic approach to mutation analysis that drastically
reduces the number of mutants"; "We focus on a code-review based approach and consider the effects of
surfacing mutation results on developer attention"; it skips *arid* lines — lines "without statement
coverage" or judged "uninteresting" — by a heuristic.
**Canonicity**: Crossref is-referenced-by-count **83** (2026-10-21).
**Contributes**: The primary source for **mutate only changed code, at review time**. This is the
candidate row "MR pipeline runs mutation only for changed code".
**Checkable in a pipeline file?** Yes: a mutation job in the MR pipeline either passes a diff scope
(`--since`, `--incremental`, `--in-diff`, a changed-file list) or runs the whole codebase.
**Caveats**: Google shows mutants to reviewers as advisory findings; it does not gate merge on a
mutation score (from the abstract's "developer attention" framing; the paper's gating stance was **not
read**). A rule that *fails* the MR on surviving mutants goes beyond this source.

### 3.3 Petrović, Ivanković, Fraser, Just, "Practical Mutation Testing at Scale: A View from Google" (TSE 2022)

**Work**: Goran Petrović, Marko Ivanković, Gordon Fraser, René Just. *IEEE TSE* 48(10): 3900–3912,
2022-10-01 (online 2021). DOI 10.1109/TSE.2021.3107634.
https://research.google/pubs/practical-mutation-testing-at-scale-a-view-from-google/ (high).
**Evidence**: The approach is "mutating only changed code during code review, rather than the entire
code base", "limiting the number of mutants per line and per code review process"; Google has "two
billion lines of code and more than 150,000,000 tests are executed on a daily basis"; the system is
"used by more than 24,000 developers on more than 1,000 projects".
**Canonicity**: Crossref is-referenced-by-count **66** (2026-10-21); TSE journal version of the 2018
work, with Fraser and Just (academic mutation-testing authorities).
**Contributes**: Second, independent-venue confirmation of changed-code mutation at review, plus the
**per-line and per-review mutant caps** that keep it fast.
**Checkable in a pipeline file?** The scope flag is; the caps are tool settings.
**Caveats**: Same research group as 3.2, so the two count as one source for independence. Neither paper
(abstract level) prescribes a scheduled full run; that row rests on tool docs and interpretation.

### 3.4 Tool support: StrykerJS incremental, Stryker.NET `since`/baseline, PIT history, cargo-mutants shards

**Work**: StrykerJS "Incremental" (https://stryker-mutator.io/docs/stryker-js/incremental/, "Available
since Stryker 6.2"); Stryker.NET "Configuration" (https://stryker-mutator.io/docs/stryker-net/configuration/,
no version shown); PIT "Incremental analysis" (https://pitest.org/quickstart/incremental_analysis/);
cargo-mutants "Sharding" (https://mutants.rs/shards.html). All official for their tool.
**Evidence (StrykerJS)**: `--incremental` runs mutation "only on the changed parts" and will "still
provide you with the full mutation report at the end!"; results stored in `reports/stryker-incremental.json`.
Limitation: Stryker "will not detect any changes you've made in files other than mutated files and test
files" — environment variables, updated (dev) dependencies, `.snap` files are not detected; test-change
detection depends on the runner (full for Jest/Vitest, names only for Jasmine/Karma, nothing for the
command runner). `--force` reruns everything in scope.
**Evidence (Stryker.NET)**: `since`: "Use git information to test only code changes since the given
target"; "All other mutants will not have a result." `with-baseline` reuses the stored report for
unchanged mutants; "When Stryker is still unable to find a baseline we will do a complete instead of
partial testrun." Experimental features "can contain false positives and false negatives."
**Evidence (PIT)**: Incremental analysis is experimental; every optimisation except reuse of killed
mutants "introduce[s] a degree of potential error"; PIT considers only superclasses and outer classes as
dependencies; the core assumption is "currently **unproven**." `scmMutationCoverage` is **not on this
page** (it is a Maven goal; not verified).
**Evidence (cargo-mutants)**: `--shard k/n` — shards "each independently discover the available mutants
and then select a subset"; "All shards must be run with the same arguments, and the same sharding
denominator `n`"; use a CI matrix with `fail-fast: false`, upload each shard's output, start with
about 8–32 shards; sharding "can also combine with `--in-diff`".
**Canonicity**: Vendor docs, authoritative for their own tool behaviour only.
**Contributes**: (a) Every incremental mode **admits it can go stale** — StrykerJS misses dependency
and environment changes; PIT calls its assumption unproven; Stryker.NET warns of false negatives. That is
the evidence for the candidate row **"a scheduled full mutation pass"**: it is the reset that incremental
modes need. (b) Native sharding exists (cargo-mutants); for Stryker, mutmut and PIT no built-in shard
option was found, so "parallelise the full run" means CI-matrix splitting by file or package, or the
tool's in-process concurrency.
**Checkable in a pipeline file?** Yes: the MR mutation job's scope flag; the existence of a scheduled
full mutation job; a matrix/`parallel:` on it.
**Caveats**: No source found that says "full mutation weekly"; cadence is the plugin author's choice.
mutmut docs were not read (see Knowledge Gaps).

### 3.5 Synthesis for the candidate rows (interpretation)

- **MR: mutate changed code only** — supported by Google (3.2, 3.3; one group) and by all four tools'
  diff/incremental modes. Confidence: High for the practice; Medium for *gating* on it.
- **Main: no mutation; weekly scheduled full pass** — the "no mutation on main" half is the author's
  economics, not a sourced practice. A squash or merge-commit on main may contain code the MR's diff
  mutation never saw (rebases, merge resolution); the scheduled full run catches that. The scheduled
  full pass is supported indirectly by the tools' stale-result warnings (3.4). Confidence: Medium.
- **Shard the full run** — cargo-mutants documents matrix sharding; general test-runner sharding is
  standard (4.3 `parallel:`/matrix). Confidence: Medium.

## 4. Pipeline triggering and duplication (GitLab, GitHub Actions)

Vendor docs are the authoritative reference for their own product. GitLab pages show no doc version;
the YAML reference carries history notes up to GitLab 19.2 (`rules:changes:regexp`), so the text read
is GitLab 19.x, accessed 2026-10-21. GitHub pages are the github.com (cloud) docs, unversioned, accessed
2026-10-21.

### 4.1 GitLab: duplicate pipelines and `workflow:rules`

**Work**: GitLab Docs, "Specify when jobs run with `rules`" (https://docs.gitlab.com/ci/jobs/job_rules/)
and "`workflow`" (https://docs.gitlab.com/ci/yaml/workflow/). Official, high.
**Evidence**: "If a job uses `rules`, a single action, like pushing a commit to a branch, can trigger
multiple pipelines"; "You should not include both push and merge request pipelines in the same job
without" workflow rules that prevent duplicates; "If you use both pipeline types at the same time,
duplicate pipelines might run at the same time." The documented pattern, "Switch between branch
pipelines and merge request pipelines":
```yaml
workflow:
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - if: $CI_COMMIT_BRANCH && $CI_OPEN_MERGE_REQUESTS
      when: never
    - if: $CI_COMMIT_BRANCH
```
`CI_PIPELINE_SOURCE` values listed: `api`, `chat`, `external`, `external_pull_request_event`,
`merge_request_event`, `ondemand_dast_scan`, `ondemand_dast_validation`, `parent_pipeline`, `pipeline`,
`push`, `schedule`, `security_orchestration_policy`, `trigger`, `web`, `webide`.
**Contributes**: The candidate row **"no duplicate branch + MR pipelines"** is the vendor's own
guidance. Note the documented pattern still runs **branch pipelines for branches without an MR**; the
plugin author's stricter "pipelines only for branches with an open MR" replaces the last rule with
`if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH` (plus `schedule`, `tag` as needed). That stricter form is
the author's choice, not GitLab's default.
**Checkable in a pipeline file?** **Yes** — the strongest checkable row in this research. A
`.gitlab-ci.yml` whose jobs admit both `push` and `merge_request_event` with no `workflow:rules`
guard is a defect.
**Caveats**: Removing branch pipelines for MR-less branches removes feedback for a developer who pushes
before opening an MR; trunkbaseddevelopment.com's model (1.2) expects the PR early, so this fits it.

### 4.2 GitLab: the `rules:changes` pitfall

**Work**: GitLab CI/CD YAML reference, `rules:changes` and `rules:changes:compare_to`
(https://docs.gitlab.com/ci/yaml/). Official, high.
**Evidence**: "Pipelines like tag pipelines, scheduled pipelines, and manual pipelines, all do not have a
Git `push` event"; "For new branch pipelines or when there is no Git `push` event, `rules: changes`
always evaluates to true"; "`rules: changes` still evaluates to true when creating a new branch."
`compare_to` lets a job "specify which ref to compare against"; CI/CD variable support since GitLab 17.2.
**Contributes**: **A checkable trap for path-scoped pipelines.** A docs-only skip built on
`rules:changes` silently runs everything on a scheduled pipeline (harmless) and on the *first push of a
new branch* (wasteful), and — the dangerous inverse — a rule written as `changes: [src/**] → when:
never` behaves differently across pipeline sources. In MR pipelines `changes` compares against the
target branch, which is the reliable case.
**Checkable in a pipeline file?** Yes: `rules:changes` in a job that can run in a branch, tag, schedule
or web pipeline without `compare_to` or a `CI_PIPELINE_SOURCE` guard.
**Caveats**: The always-true behaviour is fail-safe (runs more, not less) everywhere except where a rule
uses `changes` to *exclude*.

### 4.3 GitLab: merge gating, merged results, interruptible, `needs`, `parallel`, cache vs artifacts

**Work**: GitLab Docs: "Auto-merge" / Pipelines must succeed
(https://docs.gitlab.com/user/project/merge_requests/auto_merge/; Free tier); "Merged results
pipelines" (https://docs.gitlab.com/ci/pipelines/merged_results_pipelines/; **Premium, Ultimate**);
YAML reference (`interruptible`, `needs`, `parallel`); "Caching in GitLab CI/CD"
(https://docs.gitlab.com/ci/caching/). Official, high.
**Evidence**:
- *Pipelines must succeed*: "This setting also prevents merge requests from merging if there is no
  pipeline"; it "requires the existence of a successful pipeline, not the absence of failed pipelines";
  skipped pipelines block merging unless "Skipped pipelines are considered successful" is enabled;
  "merge request pipelines take precedence over other pipeline types".
- *Merged results*: "test a temporary merged commit that combines code from the source and target
  branches"; `.gitlab-ci.yml` "must be configured for merge request pipelines" or MRs may stick.
- *interruptible*: "cancels a job before it completes if a pipeline starts on the same ref for a new
  commit"; controlled with `workflow:auto_cancel:on_new_commit`; "Only set `interruptible: true` if the
  job can be safely canceled after it has started, like a build job."
- *needs*: "Use `needs` to execute jobs out-of-order"; relationships form "a directed acyclic graph";
  `needs: []` starts a job "as soon as the pipeline is created"; with `needs`, a job downloads artifacts
  only from the jobs it needs.
- *parallel*: "run a job multiple times in parallel in a single pipeline", 1 to 200; `parallel:matrix`
  permutations "cannot exceed 200".
- *Cache vs artifacts*: "Use cache for dependencies, like packages you download from the internet";
  "Use artifacts to pass intermediate build results between stages"; "Caching is an optimization, but
  it isn't guaranteed to always work"; "If you use cache and artifacts to store the same path in your
  jobs, the cache might be overwritten"; "Pin your dependency versions so that the contents of a pipeline
  do not change when the cache is cleared." `cache:key:files` keys a cache on file content (examples key
  on `Gemfile.lock`, `yarn.lock`).
**Contributes**: (a) **Pipelines must succeed + a docs-only skip interact**: if a docs-only MR produces
*no* pipeline, it cannot merge. The candidate row "docs-only runs secret scanning" keeps a pipeline in
existence and so keeps the gate meaningful — a sourced reason, not just a security preference.
(b) Merged-results pipelines are the GitLab form of "test what will land", but Premium-only.
(c) `needs`, `parallel`, `interruptible` and `cache` are the four speed levers a reviewer can see.
(d) **Cache is for inputs, artifacts are for outputs** — the checkable half of "no rework" (7).
**Checkable in a pipeline file?** Yes for every item except the project settings (Pipelines must
succeed, auto-cancel), which live in the API, not the file.
**Caveats**: Merge gating is a project setting; a file-only reviewer cannot see it and must raise it as
an advisory question.

### 4.4 GitHub Actions: triggers, concurrency, caching, scheduling, required checks, merge queue

**Work**: GitHub Docs: "Events that trigger workflows"
(https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows);
"Control the concurrency of workflows and jobs"
(https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/control-the-concurrency-of-workflows-and-jobs);
"Dependency caching" (https://docs.github.com/en/actions/reference/workflows-and-actions/dependency-caching);
"Troubleshooting required status checks"
(https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/collaborating-on-repositories-with-code-quality-features/troubleshooting-required-status-checks);
"Managing a merge queue"
(https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-a-merge-queue).
Official for GitHub (github.com, listed industry_leaders; vendor docs count as official for the
product per task).
**Evidence**:
- *pull_request*: runs by default on `opened`, `synchronize`, `reopened`; "`GITHUB_SHA` for this event
  is the last merge commit of the pull request merge branch" (`refs/pull/N/merge`) — GitHub tests the
  merged result by default, on every plan.
- *schedule*: "Scheduled workflows run on the latest commit on the default branch"; may be "delayed
  during periods of high loads"; "High load times include the start of every hour"; "In a public
  repository, scheduled workflows are automatically disabled when no repository activity has occurred in
  60 days"; minimum interval 5 minutes.
- *concurrency*: one running job or workflow per group; `cancel-in-progress: true` cancels running
  ones; the group `github.head_ref || github.run_id` "cancels in-progress jobs or runs on
  `pull_request` events only", falling back to the unique run id elsewhere; "ordering is not guaranteed".
- *caching*: key on `hashFiles('package-lock.json')`; `restore-keys` for misses; entries unused for 7
  days are evicted; 10 GB per repository by default; "don't store any sensitive information"; PR runs can
  restore caches from the base branch.
- *required checks*: when a workflow is skipped by path filtering, branch filtering or commit message,
  "Associated checks stay in a "Pending" state and block merging"; recommendation "Avoid requiring
  workflows that can be skipped"; a job skipped by an `if:` conditional reports "Success"; "Use
  `always()` with `needs` for required checks that depend on other jobs."
- *merge queue*: "ensuring the branch is never broken by incompatible changes"; "You must use the
  merge_group event to trigger your GitHub Actions workflow"; "Otherwise, status checks will not be
  triggered when you add a pull request to a merge queue."
**Contributes**: (a) **The required-check path-filter pitfall** (GitHub's own words) is the GitHub twin
of 4.3(a): a docs-only skip done with workflow-level `paths-ignore` on a required workflow blocks every
docs-only PR forever. The safe form is a job-level `if:` driven by a changed-files step, so the
required job reports Success. (b) `concurrency` with `head_ref || run_id` is the documented
"cancel superseded PR runs, never main" idiom. (c) A merge queue silently never reports unless the
workflow lists `merge_group`. (d) Scheduled runs: avoid minute 0; public repos stop scheduling after 60
idle days — a weekly mutation run on a quiet public repo will stop.
**Checkable in a pipeline file?** Yes for (a) only when the reviewer knows which checks are required
(a ruleset/branch-protection setting outside the file); (b), (c) and (d) yes.
**Caveats**: GitHub's docs do not name duplicate `push` + `pull_request` runs as a defect; the common
remedy (`push: branches: [main]` plus `pull_request`) is **interpretation** from the trigger docs plus the
GitLab guidance in 4.1.

## 5. Docs-only and path-scoped pipelines; secret scanning

No source found prescribes "docs-only change runs only secret scanning" as a named practice. The row is
assembled below from three sourced parts: skipping is supported by vendor path-filter docs (4.2, 4.4);
secrets leak outside source code (5.2); and a gate needs a pipeline to exist (4.3, 4.4).

### 5.1 gitleaks

**Work**: gitleaks project README, https://github.com/gitleaks/gitleaks (github.com; official for the
tool). No release number on the page; the pre-commit example pins `rev: v8.24.2`; README says
"v8.19.0 introduced a change that deprecated `detect` and `protect`". Latest release **not confirmed**.
**Evidence**: "Gitleaks is a tool for detecting secrets like passwords, API keys, and tokens in git
repos, files" and stdin. Modes `git`, `dir`, `stdin`; `git` runs `git log -p`, scoped with
`--log-opts`, e.g. `gitleaks git -v --log-opts="--all commitA..commitB" path_to_repo`. "Gitleaks can be
implemented as a pre-commit hook directly in your repo or as a GitHub action". Findings are suppressed
with `.gitleaksignore`; rules carry allowlists "to reduce false positives". The README names no file-type
restriction.
**Contributes**: The checkable form: a secret-scan job that runs on **every** pipeline source the rule
admits (MR and default branch), scanning the MR's commit range (`--log-opts` with the MR base..head),
not only the working tree. Scanning commits catches a secret added and then deleted within the MR,
which a tree scan misses (**interpretation** from `git log -p`).
**Checkable in a pipeline file?** Yes: presence of the job, its rules (does any `changes:` / `paths`
filter exclude it?), and its scan range.
**Caveats**: gitleaks-action requires a licence key for organisation accounts (prior knowledge, **not
verified**). Vendor neutrality: name the practice ("a secret scanner on every change"), cite gitleaks
as one implementation.

### 5.2 Meli, McNiece, Reaves, "How Bad Can It Git? Characterizing Secret Leakage in Public GitHub Repositories" (NDSS 2019)

**Work**: Michael Meli, Matthew R. McNiece, Bradley Reaves (NC State). *NDSS 2019*, San Diego.
DOI 10.14722/ndss.2019.23418. https://ndss-symposium.org/wp-content/uploads/2019/02/ndss2019_04B-3_Meli_paper.pdf
(academic, high; PDF read).
**Evidence**: Abstract: secret leakage is "pervasive — affecting over 100,000 repositories — but that
*thousands* of new, unique secrets are leaked every day." Search-API median time to discovery of a newly
pushed string: "20 seconds". Fig. 3: most secrets still present after 24 hours ("the majority remain").
Fig. 5 (file categories of files holding secrets, read from the bar chart, **approximate**): crypto key
files ≈50%, source code ≈30%, data ≈8%, no extension ≈6%, other ≈3%, config ≈2%. The paper concludes
"most secret leakage is likely caused by committed cryptographic key files and API keys embedded in code."
**Canonicity**: Crossref is-referenced-by-count **109** (2026-10-21); the founding measurement study
of secret leakage on GitHub.
**Contributes**: (a) Roughly one in five secret-bearing files was neither code nor a key file (data,
extensionless, other, config) — so a path filter that equates "not code" with "cannot hold a secret" is
wrong. (b) Discovery within seconds of push: scanning **before** merge to the default branch matters,
and only a pre-merge MR job or a pre-commit hook achieves it.
**Checkable in a pipeline file?** No; it justifies a row that is.
**Caveats**: 2017–2018 data; markdown is not broken out (it falls in "other", detail in the paper's
Appendix A, **not read**). GitHub secret scanning (5.3) and a 2026 Radware report on credentials in AI
agent instruction files (CLAUDE.md-style markdown; page blocked by a bot check, **not read**, vendor,
medium) suggest markdown leakage has grown; unconfirmed.

### 5.3 GitHub secret scanning; OWASP Secrets Management Cheat Sheet

**Work**: GitHub Docs, "About secret scanning"
(https://docs.github.com/en/code-security/secret-scanning/introduction/about-secret-scanning; official
for GitHub). OWASP *Secrets Management Cheat Sheet*
(https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html; standards body,
high; unversioned).
**Evidence**: GitHub: "Secret scanning scans your entire Git history on all branches of your repository
for hardcoded credentials", and beyond code also issue descriptions and comments, PR titles,
descriptions and comments, Discussions, wikis and secret gists — i.e. **prose surfaces**. OWASP §8.1:
"Consider enabling secrets detection at the developer level to avoid checking secrets into code before
commit/PR", e.g. "via pre-commit hook"; "Consider having more than one detection utility"; §8.2 lists
"Application configuration files" and "Connection strings" among secret types; §3.1 "Make sure that
pipeline output does not leak secrets."
**Contributes**: GitHub's scanner treating prose (issues, PRs, wikis) as a leak surface is direct vendor
evidence that **text, not only code, carries secrets** — the warrant for scanning docs-only changes.
OWASP supports scanning before commit/PR and layered detectors (pre-commit hook + CI job).
**Checkable in a pipeline file?** The CI job is; a pre-commit hook is checkable in
`.pre-commit-config.yaml`.
**Caveats**: OWASP does **not** explicitly say "scan in CI on every change"; neither source names
markdown files. `security.md` already owns CWE-798 (a credential literal in a diff); the CI rule owns
only the *pipeline* property "a scanner runs on every change". Cross-reference CWE-798.

### 5.4 Synthesis: the docs-only row (interpretation)

- **Skip build/test on docs-only changes**: supported as a cost measure by every vendor's path filters
  (4.2, 4.4). Not a named practice in any principles source; DORA's "percentage of commits that run tests"
  measure (1.3) cuts mildly against it.
- **Still run secret scanning**: supported by 5.2 (secrets outside code), 5.3 (prose surfaces scanned
  by GitHub), and the merge-gate mechanics (4.3: a GitLab MR with no pipeline cannot merge under
  Pipelines must succeed; 4.4: a skipped required GitHub workflow stays Pending forever). Confidence:
  Medium-High.
- **Define "docs-only" by an allow-list of paths** (`*.md`, `docs/**`), never a deny-list of code
  paths: a new code directory then runs everything by default (fail-safe; Saltzer & Schroeder's
  fail-safe defaults, already cited in `security.md`). **Caveat for this plugin**: its product *is*
  markdown — skills, rules, commands. In a prose-product repo, "docs" is code; the rule must let a
  project declare which markdown is product.

## 6. Speed and ROI

### 6.1 Hilton et al., "Usage, Costs, and Benefits of Continuous Integration in Open-Source Projects" (ASE 2016)

**Work**: Michael Hilton, Timothy Tunnell, Kai Huang, Darko Marinov, Danny Dig. *ASE 2016*, pp. 426–437,
2016-08-25. DOI 10.1145/2970276.2970358. PDF via University of Waterloo course copy
(https://cs.uwaterloo.ca/~m2nagapp/courses/CS846/1171/papers/hilton_ase16.pdf; academic, high; pages
1–2 read).
**Evidence**: 34,544 GitHub projects, 1,529,291 Travis CI builds, 442 developers surveyed. "We found
that projects that use CI release twice as often as those that do not use CI. We also found that
projects with CI accept pull requests faster than projects without CI." The most common reason for not
using CI is "lack of familiarity"; "the average project makes only 12 changes to their CI configuration
file". RQ9 asks "How long do CI builds take on average?" (answer not read).
**Canonicity**: Crossref is-referenced-by-count **272** (2026-10-21); the founding large-scale CI usage
study.
**Contributes**: Empirical benefit of CI (release frequency, PR latency); and that CI configs change
rarely — so a defect in one persists.
**Checkable in a pipeline file?** No.
**Caveats**: Travis-era, open-source only; correlational.

### 6.2 Ghaleb, da Costa, Zou, "An Empirical Study of the Long Duration of Continuous Integration Builds" (EMSE 2019) and "The Promise and Reality of CI Caching" (EASE 2026)

**Work**: Taher Ahmed Ghaleb, Daniel Alencar da Costa, Ying Zou. *Empirical Software Engineering*
24(4): 2102–2139, online 2019-03-01. DOI 10.1007/s10664-019-09695-9. Follow-up: "The Promise and Reality
of Continuous Integration Caching: An Empirical Study of Travis CI Builds", arXiv:2601.19146 (v1
2026-01-27, v2 2026-03-19), "Accepted at ... EASE '26" (academic, high).
**Evidence (2019)**: Abstract **not retrieved**; the ICSE 2020 Journal-First listing and Ghaleb's
Queen's University dissertation say it studies characteristics associated with long build durations and
that "a misconfiguration of CI can make builds run for too long" (dissertation summary via search,
**paraphrase**). Specific factors **not confirmed**.
**Evidence (2026)**: 513,384 builds from 1,279 projects; "only 30% of projects adopt CI caching"; PRs
enabling caching: "nearly half are accepted or merged"; "While one-third of projects see substantial
build-time reductions", cache uploads happen in "97% of builds"; "27% of projects contain stale cached
artifacts" (the abstract's figure; a search snippet said 33%, the arXiv abstract read says 27%).
**Canonicity**: 2019 paper: Crossref is-referenced-by-count **77** (2026-10-21). 2026 paper: too new
for a count.
**Contributes**: **Caching is not free and not always a win**: two-thirds of adopting projects saw no
substantial gain, nearly every build pays an upload, and over a quarter hold stale artifacts. This is
the evidence for "speed-up work stops at the ROI inflection point" and for keying caches on lockfile
content (4.3, 4.4).
**Checkable in a pipeline file?** Partly: a cache with a constant key (never invalidated) or no key
tied to a lockfile is visible; whether it pays is not.
**Caveats**: Travis CI only; 2026 paper is a conference paper, newly published.

### 6.3 Gallaba, Ewart, Junqueira, McIntosh, "Accelerating Continuous Integration by Caching Environments and Inferring Dependencies" (TSE 2022)

**Work**: Keheliya Gallaba, John Ewart, Yves Junqueira, Shane McIntosh. *IEEE TSE* 48(6): 2040–2052,
2022-06-01 (online Dec 2020). DOI 10.1109/TSE.2020.3048335. Author page
https://rebels.cs.uwaterloo.ca/journalpaper/2020/12/27/accelerating-continuous-integration-by-caching-environments-and-inferring-dependencies.html
(academic, high).
**Evidence** (abstract via search): build dependency graphs written by hand are "either incomplete or
overly strict"; Kotinos "accelerates CI builds by caching the build environment and skipping unaffected
build steps"; across 14,364 build records from three proprietary and seven open-source projects, at
least 87.9% of builds triggered an acceleration and 74% of accelerated builds ran about twice as fast.
**Canonicity**: Crossref is-referenced-by-count **29** (2026-10-21).
**Contributes**: Two levers ranked by measured payoff — cache the environment (images, toolchains,
dependencies) and skip unaffected steps — corroborating 2.4 and the GitLab efficiency guide (6.4).
**Checkable in a pipeline file?** Partly (an environment rebuilt from scratch each job: `apt-get
install` / toolchain download in every job rather than a prebuilt image).
**Caveats**: Research tool; figures from the abstract only.

### 6.4 Gallaba, Lamothe, McIntosh, "Lessons from Eight Years of Operational Data from a Continuous Integration Service" (ICSE 2022), and GitLab "Pipeline efficiency"

**Work**: Keheliya Gallaba, Maxime Lamothe, Shane McIntosh. *ICSE '22*, pp. 1330–1342, 2022-05-21.
DOI 10.1145/3510003.3510211; author page https://rebels.cs.uwaterloo.ca/confpaper/2022/05/21/lessons-from-eight-years-of-operational-data-from-a-continuous-integration-service.html.
GitLab Docs, "Pipeline efficiency", https://docs.gitlab.com/ci/pipelines/pipeline_efficiency/ (official).
**Evidence (ICSE 2022, abstract via search)**: 22.2 million CircleCI builds from 7,795 projects,
2012–2020; compilation and testing "consistently consume a large proportion of build time across
consumer groups (median 33%)"; premature terminations stem from "availability issues, configuration
errors, user cancellation, and exceeding time limits"; heavy consumers benefit most from skipping build
steps and from queue optimisation.
**Evidence (GitLab)**: "The easiest indicators to check for inefficient pipelines are the runtimes of
the jobs, stages"; the critical path "represents the minimum and maximum pipeline duration"; the `needs`
graph view "can help analyze the critical path in the pipeline and understand possible blockers";
"Design pipelines so that jobs that can fail fast run earlier"; stage-only ordering is "the slowest in
most cases", though DAGs "can also make pipelines harder to understand and analyze"; parallel jobs need
"more runners running simultaneously"; "If your dependencies change rarely, caching can make pipeline
execution much faster"; "It's usually much faster to download a larger pre-configured image" than
install on each run; "Make small changes, monitor the effect, then iterate again."
**Canonicity**: ICSE 2022: Crossref is-referenced-by-count **31** (2026-10-21); the largest CI
operational dataset in the literature. GitLab: vendor guidance for its product.
**Contributes**: **The critical-path principle in vendor words**, plus the measured fact that
non-compile/test actions (dependency retrieval, setup) take a large share of build time — so caching
setup often beats optimising tests. The ordered lever list: measure job durations → find the critical
path → `needs` DAG → fail-fast ordering → cache dependencies / prebuilt image → parallelise → stop and
measure.
**Checkable in a pipeline file?** Partly: stage-only ordering with no `needs` where jobs are
independent; slow jobs ahead of fast lint jobs; software installed in every job. Critical path
itself needs run history.
**Caveats**: Neither source states a stopping rule; the ROI cut-off is economic (6.5, 6.6).

### 6.5 Goldratt, *The Goal* (1984): optimise the constraint

**Work**: Eliyahu M. Goldratt, Jeff Cox. *The Goal: A Process of Ongoing Improvement*. North River
Press, 1984 (later editions 1992, 2004, 2014 — prior knowledge, **not re-verified**).
**Evidence**: Only secondary sources were reached (personal blogs, flashcards, an exam-prep guide —
**medium to low**): "An hour lost at a bottleneck is an hour lost for the entire system"; "An hour saved
at a non-bottleneck is a mirage"; the five focusing steps: identify the constraint, exploit it,
subordinate everything else, elevate it, and repeat because the constraint moves. Exact book location
**not confirmed**.
**Canonicity**: The founding text of the Theory of Constraints; *The DevOps Handbook* and *The Phoenix
Project* build on it (prior knowledge).
**Contributes**: **The principle behind "speed-up work targets the critical-path job"**: in a pipeline
DAG, only shortening the critical path shortens wall-clock feedback; making an off-path job faster is
"a mirage". And "repeat" — once the critical job is fixed, another job becomes critical.
**Checkable in a pipeline file?** No; a principle for the skill's speed-up procedure.
**Caveats**: Quotations unverified against the book; label as Goldratt's principle, cite by title.

### 6.6 Reinertsen, *The Principles of Product Development Flow* (2009): economic framing

**Work**: Donald G. Reinertsen. Celeritas Publishing, 2009 (prior knowledge; **not re-verified**).
**Evidence**: Secondary sources only (book reviews, reading notes — medium): "If you quantify only one
thing, quantify the cost of delay"; the batch-size **U-curve** — optimal batch size balances holding
cost (delayed feedback) against transaction cost; reducing transaction cost (e.g. test automation)
makes smaller batches economical.
**Canonicity**: Standard reference for flow economics in software (SAFe and Kanban literature cite it).
**Contributes**: **The stopping rule**: optimise pipeline duration while the cost of developer delay
saved exceeds the cost of the change (runner minutes, complexity, maintenance). A U-curve means there
*is* an optimum, so "stop at the inflection point" is principled, not lazy. Combined with 6.2 (caching
often does not pay) and GitLab's DAG-complexity caveat (6.4).
**Checkable in a pipeline file?** No.
**Caveats**: Quotation unverified against the book. No source gives a numeric ROI threshold for CI
work; the rule should state the procedure, not a number.

### 6.7 Speed targets (cross-reference)

Ten-minute commit build: Fowler (1.1), DORA "upper limit of about 10 minutes" (1.3), already
`continuous-delivery.md` "Keep the build under ten minutes". Google: presubmit holds "only fast,
reliable" tests; observed ~11-minute submit wait; no formal target (1.4). **No source found** for a
mutation-run or full-suite target; the scheduled full run is off the feedback path, so only its
completion within the schedule window matters (interpretation).

## 7. Rework and waste

### 7.1 Build once, promote the tested artifact (cross-reference to `continuous-delivery.md`)

**Work**: Humble & Farley (1.5): "Only build packages once", because "the thing we're deploying is the
same thing we've tested throughout the deployment pipeline"; "Deploy the same way to every environment".
GitLab caching docs (4.3): "Use artifacts to pass intermediate build results between stages."
**Contributes**: `continuous-delivery.md` owns the principle ("Build once, deploy many times"). The new
rule adds the **pipeline-file signatures of rework**, which no CD source lists but each follows from the
principle (interpretation):
- a deploy or release job that runs the build command (`npm run build`, `mvn package`, `go build`,
  `docker build`) instead of fetching the artifact or image digest the test stage produced;
- an image re-tagged by *rebuilding* rather than by re-pointing a tag at the tested digest;
- a later stage that reinstalls and recompiles what an earlier stage could have passed as an artifact;
- build output passed through `cache:` rather than `artifacts:` (GitLab says caching "isn't guaranteed
  to always work").
**Checkable in a pipeline file?** Yes, all four.
**Caveats**: Environment-specific *configuration* injected at deploy is fine and is
`continuous-delivery.md`'s "Separate configuration from code"; the defect is environment-specific
*compilation*.

### 7.2 SLSA v1.2 Build track and "Verifying artifacts"

**Work**: OpenSSF. *SLSA Specification* v1.2, status "Approved" (https://slsa.dev/spec/v1.2/verifying-artifacts);
v1.0 "Security levels" page now marked "Retired" with "Version 1.2 is the current version"
(https://slsa.dev/spec/v1.0/levels). Trusted per task, high. v1.2 release date **not shown** (also an
open gap in the security research).
**Evidence**: Provenance "describes what entity built the artifact, what process they used, and what
the inputs were." Build L1 "Package has provenance showing how it was built. Can be used to prevent
mistakes but is trivial to bypass or forge"; L2 hosted platform with signed provenance — prevents
tampering after the build; L3 hardened builds — prevents tampering during the build. Verification:
"Verify that statement's `subject` matches the digest of the artifact in question"; check builder
identity against trusted builders; check the canonical source repository to stop "an adversary from
building from an unofficial fork"; verify "before use (e.g. during installation or deployment)".
**Canonicity**: OpenSSF specification; the security research (`software-security-canonical-sources.md`
6.2) already cites it.
**Contributes**: **The checkable form of "the artifact deployed is the one tested"**: the build job
emits provenance whose subject is the artifact digest; the deploy job verifies that digest before
deploying. SLSA L1 is explicitly about "mistakes" — exactly the rework/rebuild error — not only attacks.
**Checkable in a pipeline file?** Yes: a provenance or attestation step in the build job (e.g.
`actions/attest-build-provenance`, `slsa-github-generator`, GitLab's artifact attestation — tool names
from prior knowledge, **not verified this session**) and a verify step before deploy.
**Caveats**: `security.md`'s Principles half cites SLSA for build integrity; keep the security framing
there and the "no rework" framing here, cross-referenced. SLSA adoption above L1 needs platform support.

### 7.3 Caching dependencies vs rebuilding them; Docker layer cache

**Work**: Docker Docs, "Docker build cache" (https://docs.docker.com/build/cache/) and "Optimize cache
usage in builds" (https://docs.docker.com/build/cache/optimize/). Official for Docker (docker.com/docs
listed high). No version or date shown. GitLab and GitHub cache docs (4.3, 4.4); Gallaba et al. (6.3);
Ghaleb et al. 2026 (6.2).
**Evidence**: "If a layer changes, all other layers that come after it are also affected"; "Once a layer
changes, then all downstream layers need to be rebuilt as well." Order: "First, copy over the package
management files", install dependencies, then copy source. ".dockerignore ... lets you exclude files and
directories from the build context." "Cache mounts are a way to specify a persistent cache location to be
used during builds." For CI, "`--cache-to` exports the build cache" and "`--cache-from` specifies remote
caches for the build to use" (registry backend example).
**Contributes**: Checkable rework rows for container builds: `COPY . .` before the dependency install
(every source change reinstalls all dependencies); no `.dockerignore`; ephemeral CI runners with no
`--cache-from`/`--cache-to` (every build starts cold). With 6.2's caveat: a cache must key on the lockfile
and be measured, since a third of projects see the gain and over a quarter carry stale caches.
**Checkable in a pipeline file?** Yes (Dockerfile ordering, `.dockerignore` presence, cache flags in
the CI build step).
**Caveats**: Docker pages are vendor docs for BuildKit; Podman/Buildah behaviour not researched.

## 8. Flaky tests and pipeline reliability

`continuous-delivery.md` already owns "Fix flaky tests immediately—they destroy determinism". The new
rule needs only the pipeline-file side: **how retry and quarantine show up in CI config, and which form
is acceptable**.

### 8.1 Luo, Hariri, Eloussi, Marinov, "An Empirical Analysis of Flaky Tests" (FSE 2014)

**Work**: Qingzhou Luo, Farah Hariri, Lamyaa Eloussi, Darko Marinov (UIUC). *FSE 2014*, pp. 643–653,
2014-11-11. DOI 10.1145/2635868.2635920. PDF via Vanderbilt course copy
(https://huang.isis.vanderbilt.edu/cs8395/paper/flakytest.pdf; academic, high; pages 1–2 read).
**Evidence**: 201 commits that likely fix flaky tests in 51 Apache projects. Table 1: "The top three
categories of flaky tests are Async Wait, Concurrency, and Test Order Dependency"; "Most flaky tests
(78%) are flaky the first time they are written"; "Most Test Order Dependency flaky tests (74%) are
fixed by cleaning the shared state between test runs"; "Some fixes to flaky tests (24%) modify the CUT,
and most of these cases (94%) fix a bug in the CUT"; implication: "Flaky tests should not simply be
removed or disabled because they can help uncover bugs in the CUT." On reruns: at Google "a failing test
is rerun 10 times against the same code version on which it previously failed, and if it passes in any
of those 10 reruns, it is labeled as a flaky test"; TAP "had 1.6M test failures on average each day in
the past 15 months, and 73K out of 1.6M (4.56%) test failures were caused by flaky tests" (personal
communication with John Micco); current approaches (rerun, `@Ignore`) "are more 'workarounds' rather
than solutions" and "can potentially waste a lot of machine resources".
**Canonicity**: Crossref is-referenced-by-count **411** (2026-10-21); ESEC/FSE 2024 Test-of-Time
honourable mention (per the FSE 2024 site via search).
**Contributes**: (a) Blanket retry is a workaround that hides real bugs (24% of fixes touched the code
under test, 94% of those fixing a bug). (b) 78% of flaky tests are flaky from birth — so **new tests are
the place to catch flakiness**, e.g. by running changed tests repeatedly in the MR pipeline (a
change-scoped practice that joins section 2).
**Checkable in a pipeline file?** Yes: a job-level `retry:` (GitLab) or a rerun wrapper
(`pytest --reruns`, `nick-fields/retry`, `jest.retryTimes`) applied to a whole test job rather than to
named, tracked tests.
**Caveats**: Apache/Java-heavy 2014 sample. Root-cause percentages for the three categories are not
in the table read; not cited.

### 8.2 Parry, Kapfhammer, Hilton, McMinn, "A Survey of Flaky Tests" (TOSEM 2021)

**Work**: Owain Parry, Gregory M. Kapfhammer, Michael Hilton, Phil McMinn. *ACM TOSEM* 31(1), online
2021-10-26. DOI 10.1145/3476105.
**Canonicity**: Crossref is-referenced-by-count **154** (2026-10-21). The standard survey.
**Contributes**: Canonicity for flaky-test terminology. Body **not read** this session; its treatment of
quarantine vs rerun is listed under Knowledge Gaps.

### 8.3 Google: SWE book, Testing Blog (2016)

**Work**: *Software Engineering at Google* Ch. 11 and Ch. 23 (1.4). John Micco, "Flaky Tests at Google
and How We Mitigate Them", Google Testing Blog, 2016-05-27
(https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html; Google-owned, medium-high).
**Evidence**: Micco: "about 84% of the transitions we observe from pass to fail involve a flaky test!"
(quoted via search snippet of the primary post; the fetch returned only comments). About 16% of tests
show some flakiness — **secondary only** (BENEVOL 2019, citing Leong et al. ICSE-SEIP 2019). A Google
reply in the comments: "Our rerun mechanism is only used for tests that are marked as flaky or when users
specifically request it." SWE book: flaky tests may be removed from presubmit temporarily while
investigated; "As you approach 1% flakiness, the tests begin to lose value"; rerunning "is only delaying
the need to address the root cause".
**Contributes**: **Retry is scoped to tests marked flaky**, not applied wholesale — the acceptable form.
**Checkable in a pipeline file?** Yes (blanket retry vs a marked-test retry).

### 8.4 Fowler, "Eradicating Non-Determinism in Tests" (2011)

**Work**: Martin Fowler, martinfowler.com, 2011-04-14
(https://martinfowler.com/articles/nonDeterminism.html; medium-high).
**Evidence**: Non-deterministic tests are "useless" and "a virulent infection that can completely ruin
your entire test suite". "Place any non-deterministic test in a quarantined area", fixed quickly; cap
the quarantine — "only allow 8 tests in quarantine" or "no longer than a week"; keep quarantined tests out
of the main deployment pipeline. Automatic retry is not endorsed.
**Contributes**: **Quarantine with a cap**, as the alternative to retry. Corroborated by Google's
temporary removal from presubmit (8.3) and Luo's warning that removal loses bug-finding power (8.1) —
hence the cap.
**Checkable in a pipeline file?** Partly: a quarantine job marked `allow_failure: true` /
`continue-on-error: true` is visible; its size and age are not.

### 8.5 Synthesis (interpretation)

Three independent groups (UIUC, Google, Fowler) agree: blanket retry hides bugs; retry, if any, is for
tests individually marked flaky and tracked; quarantine is allowed if bounded and out of the gate.
Confidence: High. Pipeline-file signatures: job-wide `retry:` on test jobs (GitLab `retry:` is meant for
`runner_system_failure`-style infrastructure failures — the `retry:when` values were **not verified this
session**); `allow_failure: true` on the main test job; a rerun plugin with no marker filter.

## 9. Defect id spaces for the reviewer half

The security rule keys rows to CWE. No equivalent standard exists for non-security pipeline defects. Two
academic catalogues and two security catalogues were evaluated.

### 9.1 Zampetti et al., "An Empirical Characterization of Bad Practices in Continuous Integration" (EMSE 2020) — the recommended id space

**Work**: Fiorella Zampetti, Carmine Vassallo, Sebastiano Panichella, Gerardo Canfora, Harald Gall,
Massimiliano Di Penta. *Empirical Software Engineering* 25(2): 1095–1135, online 2020-01-08. DOI
10.1007/s10664-019-09785-8. Accepted manuscript hosted by co-author Vassallo at UZH:
https://www.ifi.uzh.ch/seal/people/vassallo/ZampettiEMSE2019.pdf (academic, high; Tables 4–12 read,
pages 15–24). Publisher copy paywalled.
**Evidence (method)**: Interviews with 13 experts plus 2,322 Stack Overflow posts (533 relevant) →
182 symptoms → card-sorted into "a total of 79 bad smells grouped into 7 categories"; validated on 330
unseen posts (only one new smell found); perceived relevance surveyed with 26 practitioners. Column "D"
marks the smells that map to Duvall's antipatterns (Duvall 2011, the DZone Refcard catalogue — see 9.5).
**Evidence (the catalogue, ids verbatim)**: Repository R1–R10; Infrastructure Choices I1–I7; Build
Process Organization BP1–BP29; Build Maintainability BM1–BM8; Quality Assurance Q1–Q14; Delivery Process
D1–D5; Culture C1–C6 (10+7+29+8+14+5+6 = 79). The ids relevant to this rule:

| Id | Bad smell (verbatim) | Survey: agree / disagree (n) | Majority view |
|---|---|---|---|
| R8 | Generated artifacts are versioned, while they should not | 18% / 50% (25) | — |
| R9 | Blobs are unnecessarily checked-in at every build instead of being cached | 23% / 41% (25) | — |
| R10 | Pipeline related resources are not versioned | 64% / 12% (25) | **Relevant** |
| BP2 | Missing Package Management | 58% / 25% (24) | **Relevant** |
| BP3 | Wide and incohesive build jobs are used | 40% / 44% (25) | — |
| BP4 | Monolithic builds are used in the pipeline | 56% / 28% (25) | **Relevant** |
| BP5 | Independent build jobs are not executed in parallel | 36% / 48% (25) | **Not relevant** |
| BP6 | Only the last commit is built, aborting obsolete and queued builds | 24% / 44% (25) | **Not relevant** |
| BP7 | Build steps are not properly ordered | 48% / 40% (25) | **Relevant** (Table 11) |
| BP8 | Pipeline steps/stages are skipped arbitrarily | 46% / 46% (24) | — |
| BP10 | Incremental builds are used while never building the whole project from scratch | 36% / 36% (25) | — |
| BP11 | Poor build triggering strategy | 50% / 33% (24) | — |
| BP13 | Some pipeline's tasks are started manually | 44% / 44% (25) | — |
| BP14 | Use of nightly builds | 48% / 36% (25) | — |
| BP16 | A build is succeeded when a task is failed or an error is thrown | 64% / 28% (25) | **Relevant** |
| BP17 | A build fails because of some flakiness in the execution, whereas it should not | 67% / 12% (24) | **Relevant** |
| BP18 | Dependency management is not used | 44% / 40% (25) | — |
| BP25 | Time-out is not properly configured | 52% / 36% (25) | **Relevant** |
| BP26 | Unneeded tasks are scheduled in the build process | 44% / 28% (25) | — |
| BP27 | Build time for the "commit stage" overcomes the 10-minutes rule | 52% / 22% (23) | **Relevant** |
| BP28 | Unnecessary re-build steps are performed | 40% / 28% (25) | — |
| BP29 | Authentication data is hardcoded (in clear) under VCS | 52% / 32% (25) | **Relevant** |
| BM1 | Absolute/machine-dependent paths are used | 65% / 31% (26) | **Relevant** |
| BM4 | Build configurations are cloned in different environments | 29% / 50% (24) | — |
| BM5 | Build jobs are not parametrized | 38% / 38% (25) | — |
| Q5 | Missing tests on feature branches | 50% / 31% (26) | — |
| Q8 | Testing is not fully automated leading to a non-reproducible build | 65% / 27% (26) | **Relevant** |
| Q9 | Test suite contains flaky tests | 69% / 19% (26) | **Relevant** |
| Q10 | Bad choice on the subset of test cases to run on the CI server | 40% / 28% (25) | — |
| Q11 | Failed tests are re-executed in the same build | 20% / 52% (25) | **Not relevant** |
| D1 | Artifacts locally generated are deployed | 58% / 35% (26) | **Relevant** |
| D2 | Missing Artifacts' repository | 46% / 35% (26) | — |
| C5 | Build failures are not fixed immediately giving priority to other changes | 58% / 12% (26) | **Relevant** |

Percentages are the agree and disagree end-figures of each stacked bar, read from the table images;
"Relevant" / "Not relevant" are the paper's own Tables 11 and 12 (majority over 50%).
**Canonicity**: Crossref is-referenced-by-count **87** (2026-10-21); the only peer-reviewed,
technology-neutral catalogue of CI bad practices with stable ids found. The abstract says it confirms
some literature (branch misuse), surfaces new smells (static-analysis misuse, "abuse of shell
scripts"), and contradicts prior advice "about avoiding nightly builds".
**Contributes**: **The id column for the non-security rows** — the CWE-equivalent this rule needs.
Ids carry the paper's version implicitly (one edition, 2020); cite as `Zampetti BP16` etc.
**Checkable in a pipeline file?** About a third of the 79 are: R8, R9, R10, BP4–BP8, BP10, BP11, BP13,
BP14, BP16, BP25–BP29, BM1, BM5, Q5, Q10, Q11, D1, D2. The rest (culture, infrastructure, notification)
are process.
**Caveats**: (a) The survey has n ≈ 25; its relevance figures are weak evidence and **two cut against
the candidate rows**: practitioners rejected BP5 (no parallelism) and BP6 (aborting obsolete builds)
as bad smells, and rejected Q11 (re-executing failed tests) — see Conflicting Information 3 and 4.
(b) The catalogue's "smell" is a symptom, not always a defect; BP14 (nightly builds) is contested by the
authors themselves. (c) The online appendix with full definitions was **not read**.

### 9.2 Vassallo et al., CD-Linter, "Configuration Smells in Continuous Delivery Pipelines" (ESEC/FSE 2020)

**Work**: Carmine Vassallo, Sebastian Proksch, Anna Jancso, Harald C. Gall, Massimiliano Di Penta.
*ESEC/FSE 2020*, pp. 327–337, 2020-11-08. DOI 10.1145/3368089.3409709. Abstract via TU Delft portal
(https://research.tudelft.nl/en/publications/configuration-smells-in-continuous-delivery-pipelines-a-linter-an;
academic, high). Tool: https://bitbucket.org/sealuzh/cd-linter/ (linked from a CD-Linter-filed issue;
not opened).
**Evidence**: Existing linters find syntax errors, vulnerabilities or feature misuse but "do not support
developers that want to prevent common misconfigurations of a CD pipeline that potentially violate CD
principles ('CD smells')"; CD-Linter "can automatically identify four different smells in pipeline
configuration files"; over 145 issues in six months, "CD smells are accepted and fixed by most of the
developers"; precision 87%, recall 94%; "31% of projects with long configurations are affected by at
least one smell" (5,312 GitLab projects). The four smells — **Fake Success, Retry Failure, Manual
Execution, Fuzzy Version** — are named in the author's slide deck (via search; deck too large to fetch)
and **not confirmed against the paper**. One CD-Linter issue read in full (gitlab.com/gnutls/libtasn1
issue 23): "The build process has to be deterministic"; retries "might not only hide the underlying
problem"; fix: "Remove `retry: 1` from the job definition or consider adding the option `when` to
specify failures cases"; it cites Humble & Farley. A maintainer replied (via search snippet) that
`retry: 1` "reduces the number of times that deserve manual attention".
**Canonicity**: Crossref is-referenced-by-count **41** (2026-10-21). Same group as 9.1 — the linter
operationalises a subset of the catalogue for `.gitlab-ci.yml`.
**Contributes**: Proof that some catalogue smells are **mechanically detectable in `.gitlab-ci.yml`
with high precision**, and that maintainers accept the reports — exactly the always-flag property.
Mapping (interpretation): Fake Success ≈ BP16 (`allow_failure: true` on a test job); Retry Failure ≈
Q11/BP17 (`retry:` without `when:` limited to infrastructure failures); Manual Execution ≈ BP13
(`when: manual`); Fuzzy Version ≈ BP18/`security.md` mutable tags (`image: x:latest`, unpinned
dependency) — **owned by `security.md` CWE-829 row; cross-reference**.
**Checkable in a pipeline file?** Yes, by design.
**Caveats**: Smell definitions unconfirmed at paper level; GitLab-only.

### 9.3 Vassallo et al., CI-Odor, "Automated Reporting of Anti-Patterns and Decay in Continuous Integration" (ICSE 2019)

**Work**: Carmine Vassallo, Sebastian Proksch, Harald C. Gall, Massimiliano Di Penta. *ICSE 2019*,
pp. 105–115. DOI 10.1109/ICSE.2019.00028. Anti-pattern definitions as reproduced in Biazotto et al.,
arXiv:2604.10631 (2026-04-12; academic, secondary for this purpose).
**Evidence** (Vassallo's definitions, as quoted by Biazotto et al.): Late Merging; Skip Failed Tests
("Skipping a previously failing test 'fixes' the build symptom without addressing the cause"); Absent
Feedback; Email Notif.; Broken Release ("A broken build not fixed promptly prevents CI from assessing new
changes"); Slow Build ("Report increasing build times and outliers in build duration"); Aged Branches;
Bloated Repo ("Build artifacts/binaries should not be committed"); **Scheduled Builds ("Scheduled builds
either rebuild changes unnecessarily or indicate changes are not automatically built")**.
**Canonicity**: Crossref is-referenced-by-count **56** (2026-10-21).
**Contributes**: Log-based (run-history) anti-patterns — Slow Build, Broken Release — that a
pipeline-file reviewer **cannot** see; they belong to a skill that reads run history, not to the file
rule. Scheduled Builds is a caution for the weekly-mutation row: a schedule is legitimate only for work
that *is not* the per-change build (see Conflicting Information 5).
**Checkable in a pipeline file?** Mostly no (log-based); Bloated Repo is checkable in the repository.
**Caveats**: Definitions via a secondary 2026 paper; ICSE paper text not read.

### 9.4 Security id spaces: OWASP Top 10 CI/CD Security Risks, OpenSSF Scorecard, SLSA

**Work**: OWASP, *Top 10 CI/CD Security Risks* (https://owasp.org/www-project-top-10-ci-cd-security-risks/;
standards body, high; release date and version **not shown** — commonly dated 2022, unconfirmed).
OpenSSF Scorecard checks (https://github.com/ossf/scorecard/blob/main/docs/checks.md; trusted per
task). SLSA v1.2 (7.2).
**Evidence (OWASP)**: CICD-SEC-1 Insufficient Flow Control Mechanisms · CICD-SEC-2 Inadequate Identity
and Access Management · CICD-SEC-3 Dependency Chain Abuse · CICD-SEC-4 Poisoned Pipeline Execution (PPE)
· CICD-SEC-5 Insufficient PBAC (Pipeline-Based Access Controls) · CICD-SEC-6 Insufficient Credential
Hygiene · CICD-SEC-7 Insecure System Configuration · CICD-SEC-8 Ungoverned Usage of 3rd Party Services ·
CICD-SEC-9 Improper Artifact Integrity Validation · CICD-SEC-10 Insufficient Logging and Visibility.
**Evidence (Scorecard)**: **CI-Tests** (Low): "This check tries to determine if the project runs tests
before pull requests are merged." **Branch-Protection** (High), tiered: tier 3 (8/10) "Require branch
to pass at least 1 status check before merging". **Dangerous-Workflow** (Critical): untrusted checkout
under `pull_request_target` / `workflow_run`, script injection. **Token-Permissions** (High): read-only
top-level, write per job. **Pinned-Dependencies** (Medium). **SAST** (Medium).
**Contributes**: Security ids for the rows that overlap `security.md` — and **two non-security
bridges**: CICD-SEC-1 (flow control: a change reaching main without the gate) and CICD-SEC-9 (artifact
integrity: the deployed artifact is not the verified one) give security ids to the "merge on green"
and "no rebuild in deploy" rows; Scorecard CI-Tests and Branch-Protection tier 3 give a measurable
form of "a passing PR pipeline is required to merge".
**Checkable in a pipeline file?** Dangerous-Workflow, Token-Permissions, Pinned-Dependencies yes
(already `security.md`). CI-Tests and Branch-Protection need forge settings or run history.
**Caveats**: CICD-SEC definitions not read (only names); ids are security-scoped and would
misclassify speed and scope defects. Use them only where the defect is also a security defect.

### 9.5 Duvall's CI anti-patterns

Zampetti's column "D" maps 30-odd smells to "Duvall's antipatterns (Duvall, 2011)" — the
reference is to Paul Duvall's *Continuous Delivery Patterns and Anti-Patterns* catalogue (DZone Refcard,
2011 — identification from the paper's reference key; the Refcard itself **not read**). Zampetti
subsumes it with ids; cite Zampetti.

### 9.6 Verdict (interpretation)

Key the non-security rows to **Zampetti ids** (79-item, peer-reviewed, technology-neutral, stable since
2020), and add CD-Linter's smell names where it detects the same thing. Key overlap rows to
`security.md`'s CWE ids and, where the defect is a pipeline-integrity one, to CICD-SEC-1 / -9. Do not
use Scorecard names as ids — Scorecard is a tool whose checks change; cite them as corroboration.
Confidence: Medium-High (one catalogue, one research group across 9.1–9.3; no competing catalogue found).

## Synthesis

### The rule's spine (ranked shortlist)

| Rank | Work(s) | Half | Why it ranks here |
|---|---|---|---|
| 1 | Zampetti et al., EMSE 2020 (79 CI bad smells, ids R/I/BP/BM/Q/D/C) + Vassallo et al. CD-Linter, ESEC/FSE 2020 | Reviewer | The only peer-reviewed, technology-neutral defect catalogue with stable ids (87 Crossref citations); CD-Linter shows a subset is detectable in `.gitlab-ci.yml` at 87% precision / 94% recall and that maintainers accept the reports. The CWE-equivalent for this rule. |
| 2 | Winters, Manshreck, Wright (eds.), *Software Engineering at Google*, Ch. 23 and Ch. 11 | Principles | Presubmit holds "only fast, reliable" tests; post-submit runs the rest; TAP selects by "downstream dependency graph"; test sizes; the 1% flakiness value threshold. The principled basis for MR-scoped vs main-full. Free online. |
| 3 | GitLab CI/CD docs (`workflow:rules`, `rules:changes`, Pipelines must succeed, merged results, `needs`, `parallel`, `interruptible`, cache vs artifacts, pipeline efficiency) and GitHub Actions docs (required checks and path filters, `concurrency`, `merge_group`, `schedule`, caching) | Reviewer | The checkable half of triggering, duplication, gating and speed, in the vendors' own words, including the two traps (`changes:` always true without a push event; a skipped required workflow stays Pending). |
| 4 | Fowler, "Continuous Integration" (2024) + trunkbaseddevelopment.com + DORA CI and TBD capabilities | Principles | Every push to mainline builds; ten-minute commit build; DORA's ~10-minute ceiling and "percentage of commits that run tests"; and the condition under which PR-gated work is still trunk-based (≈2-day branch including review wait, one developer). |
| 5 | Memon et al. ICSE-SEIP 2017 + Gligoric et al. (Ekstazi) ISSTA 2015 + Machalica et al. ICSE-SEIP 2019 + Nx/Bazel docs | Both | Change-scoped testing is safe only with file-level (not class-level) dependencies and a lockfile failsafe (Nx's default); predictive selection drops up to 5% of failures and needs a full post-merge run. Supplies the forced-full-run list. |
| 6 | Petrović & Ivanković ICSE-SEIP 2018 + Petrović et al. TSE 2022 + Stryker/PIT/cargo-mutants docs; Jia & Harman TSE 2011 for canonicity | Both | Diff-based mutation at code review at Google scale (24,000 developers); every tool's incremental mode admits staleness, which justifies a scheduled full pass; cargo-mutants documents matrix sharding. |
| 7 | Humble & Farley, *Continuous Delivery* (via continuousdelivery.com) + SLSA v1.2 "Verifying artifacts" | Both | "Only build packages once" (already `continuous-delivery.md`); SLSA gives its checkable form: provenance subject digest = deployed artifact digest, verified "before use (e.g. during installation or deployment)". |
| 8 | Luo et al. FSE 2014 + Fowler "Eradicating Non-Determinism in Tests" (2011) + Google (SWE book, Micco 2016) | Both | Three independent groups: blanket retry is a workaround that hides bugs (24% of flaky fixes changed the code under test); retry only marked tests; quarantine bounded ("only allow 8 tests", "no longer than a week"). |
| 9 | Gallaba et al. ICSE 2022 and TSE 2022 + Ghaleb et al. EMSE 2019 / EASE 2026 + GitLab "Pipeline efficiency" + Goldratt *The Goal* + Reinertsen *Flow* | Principles | Measure, find the critical path, then cache/skip/parallelise; caching pays for only a third of projects and goes stale in 27%; Goldratt's "an hour saved at a non-bottleneck is a mirage"; Reinertsen's U-curve gives a principled stopping point. |
| 10 | Meli et al. NDSS 2019 + GitHub secret scanning docs + gitleaks + OWASP Secrets Management Cheat Sheet | Reviewer | Thousands of secrets leak daily and are found within ~20 seconds; ≈20% of secret-bearing files were neither code nor key files; GitHub scans prose surfaces. Warrant for "secret scanning runs on every change, docs included". |

**Background, not spine**: *Accelerate* and *The DevOps Handbook* (empirical warrant and the Three Ways —
already `continuous-delivery.md`); Duvall et al. 2007 (historical; superseded by Fowler 2024 and subsumed
by Zampetti's column D); Hilton et al. ASE 2016 (CI projects "release twice as often" — motivation, not
rules); Parry et al. TOSEM 2021 (survey canonicity); OWASP CICD-SEC and Scorecard (ids only where the
defect is also a security defect — `security.md` territory); CI-Odor (run-history anti-patterns, for a
skill that reads build logs).

### Candidate rows tested against sources

| Candidate row (plugin author) | Support | Contrary or limiting evidence | Verdict and caveat |
|---|---|---|---|
| Run pipelines only for branches with an open MR/PR; no duplicate branch+MR pipelines; a passing MR pipeline is required to merge | GitLab: duplicates are a documented failure; `workflow:rules` pattern; Pipelines must succeed. GitHub: `pull_request` tests the merge commit. trunkbaseddevelopment.com: PR-gated short-lived branches are TBD. Scorecard Branch-Protection tier 3; CI-Tests. Zampetti BP11, Q5. | GitLab's own pattern keeps branch pipelines for MR-less branches; Fowler: pre-integration review "can be problematic for CI"; DORA: branches of "a few hours" and synchronous review. | **Encode.** The no-duplicate half is always-flag (P1). "MR-only" is a declared project policy, not a universal defect. The merge-gate half is a forge setting — advisory for a file-only reviewer. Cross-reference `continuous-delivery.md`'s trunk-based line with the ≈2-day limit. |
| MR runs tests and mutation only for changed or affected code; docs-only runs only secret scanning (MR and main) | Google TAP; Memon; Ekstazi; Nx/Bazel affected; Petrović 2018/2022; Stryker `since`/incremental; Meli; GitHub secret scanning; merge-gate mechanics. | Machalica: selection misses failures; Ekstazi: class-level selection unsafe; Stryker misses dependency/env changes; DORA measures "percentage of commits that run tests"; Zampetti Q10 ("Bad choice on the subset of test cases"). | **Encode with a forced-full-run list** (lockfile/manifest, CI config, shared test infra, build-tool config) and docs defined by an **allow-list**. In a repo whose product is prose, "docs" must be declared. |
| Main runs everything except mutation; weekly scheduled full mutation pass, off-hours, parallelised | Post-submit full run (Google); main as the safety net for selection (Machalica); Zampetti BP10; tools' stale-result warnings; cargo-mutants sharding; GitHub schedule docs (avoid minute 0). Zampetti contradicts "avoid nightly builds"; BP14 48% vs 36%. | CI-Odor lists "Scheduled Builds" as an anti-pattern; no source gives a weekly cadence; GitHub disables schedules after 60 idle days on public repos; main's merge result may contain code no MR diff mutated. | **Encode**, framing the schedule as *the reset for incremental mutation*, not as the build. Cadence is the project's choice. |
| Speed-up work targets the bottleneck (critical-path) job and stops at the ROI inflection point: parallelise, cache, and similar high/medium payoff changes | GitLab pipeline efficiency (critical path, fail fast, iterate); Gallaba ICSE 2022 (non-compile/test actions take a large share) and TSE 2022 (~2× on accelerated builds); Goldratt; Reinertsen U-curve. | Ghaleb 2026: caching gave substantial gains to only one-third of adopters, 27% stale; GitLab: DAGs "harder to understand"; parallel needs more runners; Zampetti BP5 judged *not relevant* by practitioners. | **Encode as procedure in the skill, not as always-flag rows.** Only fail-fast ordering (BP7) and rework rows are file-checkable defects. |
| No rework: the artifact built and tested is the one deployed; never rebuild in deploy | Humble & Farley; SLSA v1.2 verify digest before deployment; GitLab artifacts vs cache; Zampetti D1, BP28; CICD-SEC-9. | None found. | **Encode** as always-flag (P11, P12); cross-reference `continuous-delivery.md` "Build once, deploy many times" rather than restate. |

### Candidate always-flag list

Objective defects a reviewer can see in a pipeline file (`.gitlab-ci.yml`, `.github/workflows/*`,
`Dockerfile`), each citing an id. `security.md` keeps mutable tags, `pull_request_target`, lockfile
installs and token scope; rows that touch them cross-reference instead.

| # | Defect a reviewer flags | Zampetti id | Other id / source | Confidence |
|---|---|---|---|---|
| P1 | Jobs admit both a push and an MR/PR event for the same branch with no guard — GitLab jobs reachable by `push` and `merge_request_event` with no `workflow:rules`; GitHub `on: [push, pull_request]` with `push` unrestricted to the default branch | BP11 | GitLab `workflow` docs ("duplicate pipelines might run"); CD-Linter n/a | High (GitLab), Medium (GitHub — interpretation) |
| P2 | A push to the default branch triggers no pipeline, or only a subset that skips the full test suite | BP11, BP10 | Fowler 2024 ("Every time the mainline receives a commit"); DORA CI; SWE at Google post-submit | High |
| P3 | Change-scoped test selection in the MR pipeline with no full run forced by a change to the lockfile or manifest, the CI configuration, shared test infrastructure, or build-tool configuration | Q10 | Nx (lockfile marks "all projects as affected"); Ekstazi (file-level deps); interpretation for CI config | Medium |
| P4 | Change-scoped selection in the MR pipeline and no full-suite run on the default branch or schedule | BP10 | Machalica 2019; SWE at Google (post-submit) | High |
| P5 | `rules:changes` used to *exclude* or *skip* a job that can run in a pipeline without a push event (schedule, tag, web, API) or on a new branch, with no `compare_to` and no `CI_PIPELINE_SOURCE` guard | BP8 | GitLab YAML reference ("always evaluates to true") | High |
| P6 | A required check that a workflow-level `paths`/`paths-ignore`/branch filter can skip (GitHub), or a workflow that produces no pipeline for some MRs where "Pipelines must succeed" is on (GitLab) | BP11 | GitHub "Troubleshooting required status checks" ("stay in a 'Pending' state and block merging"); GitLab auto-merge docs ("prevents merge requests from merging if there is no pipeline") | High |
| P7 | No secret-scanning job in the MR pipeline or the default-branch pipeline, or a path filter that excludes it from docs-only changes | BP29 | Meli et al. NDSS 2019; GitHub secret scanning; OWASP SM Cheat Sheet §8.1; CICD-SEC-6; `security.md` CWE-798 | Medium-High |
| P8 | MR mutation job mutates the whole codebase where the tool offers a diff or incremental scope | BP26 | Petrović & Ivanković 2018; Petrović et al. 2022; Stryker `since`/`--incremental`; cargo-mutants `--in-diff` | Medium (fires only when the full run breaks the MR time budget — see Do-not-flag) |
| P9 | Diff-scoped or incremental mutation with no scheduled full mutation run | BP10 | StrykerJS ("will not detect any changes ... in files other than mutated files and test files"); PIT ("currently unproven"); Stryker.NET (false negatives) | Medium |
| P10 | A test or gating job marked to tolerate failure — GitLab `allow_failure: true`, GitHub `continue-on-error: true` — so the pipeline passes when it fails | BP16 | CD-Linter "Fake Success" (name unconfirmed at paper level); Zampetti "Relevant" (64%) | High |
| P11 | A deploy or release job that rebuilds — compiles, installs build dependencies, or runs `docker build` — instead of promoting the artifact or image digest the tested job produced | BP28, D1 | Humble & Farley "Only build packages once"; SLSA v1.2 verify subject digest; CICD-SEC-9; cross-ref `continuous-delivery.md` | High |
| P12 | Build output passed between jobs through `cache:` instead of `artifacts:` (or `actions/cache` instead of upload/download-artifact) | BP28 | GitLab caching docs ("Use artifacts to pass intermediate build results between stages"; caching "isn't guaranteed") | High |
| P13 | A dependency cache whose key is constant or not derived from the lockfile | BP2 | GitLab `cache:key:files`; GitHub `hashFiles('package-lock.json')`; Ghaleb et al. 2026 (27% stale) | Medium |
| P14 | Job-wide retry on a test job — GitLab `retry:` with no `when:` limited to infrastructure failures, a rerun wrapper with no flaky-marker filter | Q11, BP17 | CD-Linter "Retry Failure"; Luo et al. 2014; Fowler 2011; Google ("only used for tests that are marked as flaky") | Medium (practitioners disagree — Conflict 4) |
| P15 | `cancel-in-progress` or auto-cancel that applies to default-branch runs, so a superseded main commit is never verified | BP6 (inverse) | GitHub concurrency docs (`github.head_ref \|\| github.run_id` cancels "on `pull_request` events only"); Fowler ("the fault lies in that latest push") | Medium (interpretation) |
| P16 | A merge queue in use while the required workflow does not trigger on `merge_group` | BP11 | GitHub merge-queue docs ("status checks will not be triggered") | High |
| P17 | A fail-fast check (lint, format, type check, secret scan) that waits for, or runs after, the long test job | BP7 | GitLab pipeline efficiency ("jobs that can fail fast run earlier"); Zampetti "Relevant" | Medium-High |
| P18 | A manual step (`when: manual`, a required human trigger) between MR and merge or between merge and the test stages — not a production-release approval | BP13 | CD-Linter "Manual Execution" (unconfirmed); DORA CI ("Manual steps create opportunities for mistakes") | Medium |
| P19 | Absolute or machine-dependent paths in pipeline scripts | BM1 | Zampetti "Relevant" (65%) | Medium |
| P20 | Dockerfile that copies the whole source tree before installing dependencies, so any source change reinstalls them | BP28 | Docker "Optimize cache usage" ("First, copy over the package management files") | High |
| P21 | Test or gate job with no timeout, where the platform default is far above the pipeline's budget | BP25 | Zampetti "Relevant" (52%); platform defaults **not verified** | Low-Medium |

### Candidate advisory list (judgment calls)

- **Pipelines for branches with no open MR** — flag only where the project declares MR-only pipelines.
- **Merge without a passing pipeline** — a forge setting (GitLab Pipelines must succeed; GitHub branch
  protection or ruleset required checks; Scorecard Branch-Protection tier 3). Ask; the file cannot show it.
- **A superseded MR pipeline left running** — no `interruptible` + auto-cancel, no `concurrency` group
  on the PR ref. Waste, not a defect (Zampetti BP6 judged not relevant).
- **Independent jobs serialised by stages** on the critical path where `needs` would shorten it, or
  independent work in one job that `parallel`/matrix would split — raise only with durations in hand
  (Goldratt; GitLab efficiency; BP5 judged not relevant).
- **Software installed in every job** where a prebuilt image or cached environment would serve
  (Gallaba TSE 2022; GitLab efficiency) — ROI depends on frequency.
- **"Docs-only" defined by a deny-list of code paths** rather than an allow-list of doc paths — a new
  code directory then skips tests (fail-safe defaults; `security.md` principle).
- **A scheduled job at minute 0, or on a public repo that may go 60 days idle** (GitHub schedule docs).
- **Quarantined tests with no cap on count or age** (Fowler 2011).
- **New or changed tests not rerun to expose flakiness** — 78% of flaky tests are flaky from birth (Luo).
- **No provenance or attestation on a released artifact** — SLSA L1; the security rule owns the
  integrity framing.
- **Cache that has never been measured** — one-third of adopters gain substantially (Ghaleb 2026).

### Do-not-flag list (common false positives)

- **Aborting a superseded MR pipeline** (`interruptible`, `cancel-in-progress` on the PR ref) — it is
  the documented idiom; Zampetti's practitioners rejected BP6 as a smell.
- **A scheduled full run for expensive work** (full mutation, long suites) — Zampetti's findings
  contradict "avoid nightly builds"; flag a schedule only when it *replaces* per-change builds (CI-Odor
  "Scheduled Builds").
- **Retry limited to infrastructure failures** (`retry: when: runner_system_failure`, stuck-runner
  timeouts) or to individually marked flaky tests.
- **A manual approval before production deploy** — continuous delivery, not deployment; `continuous-delivery.md`
  owns release strategy.
- **No parallelism or caching in a pipeline already inside its time budget** — Reinertsen's U-curve;
  BP5 judged not relevant.
- **Full mutation or full tests in the MR pipeline of a small codebase** that stays inside the
  ten-minute budget — scoping is a cost measure, not a correctness rule.
- **Skipping build and test on an allow-listed docs-only change** while the secret scan still runs and
  the gate still receives a status.
- **Branch pipelines in a project that has not declared MR-only pipelines** — GitLab's own default pattern.

### Where the sources support an existing rule line (cross-reference, do not restate)

| Existing line | Rule | Sources here that support it |
|---|---|---|
| "Build once, deploy many times"; "Same process for every environment" | `continuous-delivery.md` | Humble & Farley (1.5); SLSA (7.2); Zampetti D1, BP28 |
| "Keep the build under ten minutes"; "Fix broken builds immediately" | `continuous-delivery.md` | Fowler 2024; DORA; Zampetti BP27, C5 |
| "Trunk-based development enables continuous integration"; "Long-lived branches" anti-pattern | `continuous-delivery.md` | DORA TBD; trunkbaseddevelopment.com (≈2-day PR branch); Fowler |
| "Fix flaky tests immediately" | `continuous-delivery.md` | Luo 2014; SWE at Google Ch. 11; Fowler 2011; Zampetti Q9, BP17 |
| "Version control everything ... pipeline definitions" | `continuous-delivery.md` | Zampetti R10 (64% relevant) |
| Mutable-tag actions and images (CWE-829/494) | `security.md` | Scorecard Pinned-Dependencies; CD-Linter "Fuzzy Version" (unconfirmed); CICD-SEC-3 |
| `pull_request_target` running PR head | `security.md` | Scorecard Dangerous-Workflow; CICD-SEC-4 |
| CI token `write-all` (CWE-732/250) | `security.md` | Scorecard Token-Permissions; CICD-SEC-5 |
| Lockfile installs (CWE-1357) | `security.md` | Zampetti BP2, BP18; GitLab "Pin your dependency versions" |
| Credential literal (CWE-798) | `security.md` | Zampetti BP29; Meli et al. 2019 |

## Source Analysis

All accessed 2026-10-21. Reputation per the task's trusted-domain configuration; vendor docs count as
official for their own product.

| Source | Domain | Reputation | Type | Verification |
|---|---|---|---|---|
| Fowler, "Continuous Integration" (2024); "Eradicating Non-Determinism in Tests" (2011) | martinfowler.com | Medium-high | Industry leader | Read; cross-referenced with DORA, SWE at Google |
| trunkbaseddevelopment.com | trunkbaseddevelopment.com | High (task config) | Official for subject | Read; cross-referenced with DORA |
| DORA CI and TBD capabilities | dora.dev | High | Research | Read |
| *Software Engineering at Google* Ch. 11, 23 | abseil.io | High | Book (publisher-sanctioned free copy) | Read |
| continuousdelivery.com patterns | continuousdelivery.com | High (author's site) | Author | Read; book text not read |
| Study notes, DZone on "only build your binaries once" | cliffsnotes, dzone.com | **Medium/low** | Secondary | Used only to name the book's list; flagged |
| Crossref API (19 DOIs) | api.crossref.org | High | Bibliographic | Counts retrieved 2026-10-21 |
| Memon 2017; Petrović 2018, 2022 abstracts | research.google | High | Academic | Abstracts read |
| Machalica 2019; Ghaleb 2026; Biazotto 2026 | arxiv.org | High | Academic | Abstracts / table read |
| Ekstazi abstract (via search); AcaWiki summary | utexas.edu (TLS failed); acawiki.org | High / **Medium** | Academic / community | Figures from search snippets of the authors' abstract |
| Bazel query guide | bazel.build | High (vendor) | Technical docs | Read |
| Nx affected | nx.dev | High (vendor) | Technical docs | Read |
| StrykerJS, Stryker.NET, PIT, cargo-mutants docs | stryker-mutator.io, pitest.org, mutants.rs | High (vendor) | Technical docs | Read |
| GitLab docs (8 pages) | docs.gitlab.com | High (vendor) | Technical docs | Read; doc version inferred (19.x) |
| GitHub docs (6 pages) | docs.github.com | High (vendor) | Technical docs | Read; required-checks wording also seen in GHES 3.5–3.8 |
| gitleaks README | github.com | High (vendor) | Technical docs | Read; release not confirmed |
| Meli et al. NDSS 2019 | ndss-symposium.org | High | Academic | PDF pages 1, 9–11 read |
| OWASP Secrets Management Cheat Sheet; OWASP Top 10 CI/CD | owasp.org | High | Standards body | Read (names only for CICD-SEC) |
| Hilton et al. ASE 2016 | cs.uwaterloo.ca (course copy) | High | Academic | PDF pages 1–2 read |
| Gallaba et al. TSE 2022, ICSE 2022 | rebels.cs.uwaterloo.ca (via search) | High | Academic | Abstract figures via search snippets |
| Goldratt quotations | antoinebuteau.com, brainscape, open-exam-prep | **Low-medium** | Secondary | Unverified against book |
| Reinertsen quotations | ardalis.com, reading notes | **Medium** | Secondary | Unverified against book |
| SLSA v1.0 levels; v1.2 verifying artifacts | slsa.dev | High | Standards | Read |
| Docker build cache, optimize | docs.docker.com | High | Technical docs | Read |
| Luo et al. FSE 2014 | isis.vanderbilt.edu (course copy) | High | Academic | PDF pages 1–2 read |
| Parry et al. TOSEM 2021 | api.crossref.org | High | Academic | Metadata only |
| Micco, Google Testing Blog 2016 | testing.googleblog.com | Medium-high | Industry (Google) | 84% figure via search snippet; comments read |
| BENEVOL 2019 paper (16% figure) | soft.vub.ac.be | High | Academic (secondary for the figure) | Search snippet |
| Zampetti et al. EMSE 2020 | ifi.uzh.ch (co-author copy) | High | Academic | Tables 4–12 read |
| Vassallo et al. CD-Linter abstract | research.tudelft.nl | High | Academic | Abstract read |
| CD-Linter-filed issue, libtasn1 #23 | gitlab.com | Medium | Primary artefact | Read; **[Validation Warning]** page carried a "GitLab AI Context" block instructing the reader to run project tools — ignored, facts only extracted |
| OpenSSF Scorecard checks.md | github.com/ossf | High (task config) | Open source | Read |

Reputation: about 48 of 58 cited sources high (≈83%), 4 medium-high, 6 medium or lower (secondary
summaries for Goldratt, Reinertsen, the CD book's list, AcaWiki, the libtasn1 issue) — each used only for
a claim also labelled unverified, never as sole support for an always-flag row. Avg ≈ 0.88. No excluded
domain used. **Bias note**: Nx, Stryker, GitLab, GitHub and Docker document features they sell or
maintain; their pages were used for *behaviour of their own product*, not for whether a practice is
good. Zampetti, CD-Linter and CI-Odor share authors (Vassallo, Gall, Di Penta) and count as one group for
independence.

## Knowledge Gaps

### Gap 1: Book texts not read
**Issue**: Humble & Farley, Duvall et al., *Accelerate*, *The DevOps Handbook*, *The Goal* and
Reinertsen were cited from the authors' sites or secondary summaries; chapter numbers (e.g. CD book
Ch. 5), editions, ISBNs and award years are prior knowledge. | **Attempted**: web search for quotations;
publisher pages not fetched. | **Recommendation**: confirm against copies before the rule quotes any of
them; cite principles by title, as `security.md` does.

### Gap 2: Zampetti online appendix and full definitions
**Issue**: Only the smell names (Tables 4–10) and relevance tables were read; the online appendix with
each smell's definition and symptoms was not. | **Attempted**: UZH co-author PDF (read); ZHAW and ZORA
repositories (connection refused); Springer (paywalled). | **Recommendation**: read the appendix before
mapping a row to an id; confirm BP6, BP10, BP26, BP28 readings in particular.

### Gap 3: CD-Linter's four smells unconfirmed at paper level
**Issue**: Fake Success, Retry Failure, Manual Execution, Fuzzy Version come from a slide deck via search
(deck too large to fetch); only Retry Failure was seen in a CD-Linter-filed issue. | **Attempted**: TU
Delft portal (abstract only), Bitbucket repo not opened, ResearchGate not fetched. |
**Recommendation**: read the FSE paper's Section 3.

### Gap 4: Paper abstracts read only via search snippets
Ekstazi (utexas.edu TLS failure), Ghaleb et al. 2019 (factors of long builds not retrieved), Gallaba et
al. TSE 2022 and ICSE 2022 (figures from snippets of the abstracts), Micco 2016 (84% figure), Parry et
al. 2021 (body not read — its quarantine-vs-rerun treatment is unknown).

### Gap 5: Unconfirmed versions and dates
gitleaks latest release; SLSA v1.2 release date; OWASP Top 10 CI/CD release date (commonly 2022);
GitLab docs version (inferred 19.x from history notes); GitHub docs (unversioned cloud); Nx, Bazel,
Docker docs (no version shown); StrykerJS incremental "since 6.2" is the only tool version confirmed.

### Gap 6: No source for several row details
- **CI configuration changes force a full run** (P3) — interpretation; no vendor or paper states it.
- **"Docs-only runs secret scanning"** as a named practice — assembled from three parts (5.4).
- **A weekly cadence for full mutation** — no source; author's choice.
- **Cancel-in-progress on main is a defect** (P15) — interpretation from Fowler and GitHub docs.
- **Mutation sharding for Stryker, mutmut, PIT** — no built-in shard option found; mutmut docs not read.
- **Gradle** test selection / build-avoidance docs — not researched.
- **Platform default timeouts** (P21) — not verified.
- **GitLab `retry:when` values** — not verified on docs.gitlab.com.
- **Provenance tool names** (`actions/attest-build-provenance`, `slsa-github-generator`, GitLab
  attestation) — prior knowledge.

### Gap 7: Secrets in markdown specifically
**Issue**: Meli et al. do not break out markdown; a 2026 Radware report on credentials in AI-agent
instruction files (CLAUDE.md-style) was blocked by a bot check. | **Recommendation**: find a peer-reviewed
per-extension breakdown (SecretBench, MSR 2023, covers 311 file types) before claiming markdown rates.

### Gap 8: Numeric ROI threshold
No source gives a numeric stopping rule for pipeline optimisation; the rule should state the procedure
(measure, critical path, stop when cost exceeds delay saved), not a number.

## Conflicting Information

### Conflict 1: How short must a PR branch be to count as trunk-based?
**Position A**: trunkbaseddevelopment.com — "the branch should only last a couple of days", review wait
included. **Position B**: DORA — branches "typically last no more than a few hours"; Fowler — "no code
sits on a branch longer than a few hours"; both warn about asynchronous review. **Assessment**: Both are
authoritative; DORA's is the performance-correlated target, the TBD site's the outer limit. The rule
should name "hours, at most about two days, review wait included" and cross-reference
`continuous-delivery.md`'s "Integrate code at least daily".

### Conflict 2: Is change-scoped testing safe?
**Position A**: Safe RTS (Ekstazi) and build-graph selection (TAP, Bazel, Nx) aim to miss nothing.
**Position B**: Machalica — predictive selection reports "over 95%" of failures, so up to 5% are missed;
StrykerJS and PIT admit incremental modes miss non-tracked changes. **Assessment**: Selection is safe only
relative to the dependencies it tracks. Hence P3 (forced full runs) and P4 (full run on main).

### Conflict 3: Is a non-parallel or non-cancelling pipeline a smell?
**Position A**: GitLab efficiency guide and `interruptible` docs recommend parallel jobs and cancelling
superseded pipelines; Zampetti lists BP5 and BP6 as smells. **Position B**: Zampetti's own survey —
practitioners judged both "not relevant" (BP5 36% agree / 48% disagree; BP6 24% / 44%). **Assessment**:
Practitioners treat both as optimisations, not defects. Advisory or Do-not-flag, never always-flag.

### Conflict 4: Should failed tests be retried?
**Position A**: Luo 2014 (reruns are "workarounds"), Fowler 2011, Google (retry "only ... for tests that
are marked as flaky"), CD-Linter Retry Failure (accepted by most maintainers). **Position B**: Zampetti Q11
— "Failed tests are re-executed in the same build" judged not relevant (20% / 52%); a libtasn1 maintainer
defended `retry: 1` for timing-sensitive tests. **Assessment**: Three independent expert groups plus a
linter study outweigh a 25-person survey; but the conflict caps P14 at Medium and leaves infrastructure
retries and marked-test retries in Do-not-flag.

### Conflict 5: Are scheduled builds an anti-pattern?
**Position A**: CI-Odor — "Scheduled builds either rebuild changes unnecessarily or indicate changes are
not automatically built." **Position B**: Zampetti's findings "contradict knowledge from existing
literature, e.g., about avoiding nightly builds"; nightly builds are "useful in certain circumstances,
e.g., to run computationally-expensive tasks". **Assessment**: Both hold: a schedule that *replaces*
per-change builds is the anti-pattern; a schedule that *adds* expensive analysis (full mutation) is
legitimate. The weekly-mutation row stands.

### Conflict 6: Does caching pay?
**Position A**: GitLab — "caching can make pipeline execution much faster"; Gallaba — environment
caching roughly halves accelerated builds. **Position B**: Ghaleb 2026 — substantial gains for one-third
of adopters; uploads in 97% of builds; 27% stale. **Assessment**: Caching is a hypothesis to measure, not
a rule. Flag only a cache that cannot invalidate (P13); advise measurement.

## Full Citations

[1] Fowler, M. "Continuous Integration". martinfowler.com. Revised 2024-01-18. https://martinfowler.com/articles/continuousIntegration.html. Accessed 2026-10-21.
[2] Hammant, P. et al. "Short-Lived Feature Branches". trunkbaseddevelopment.com. Undated (site © 2017–2020). https://trunkbaseddevelopment.com/short-lived-feature-branches/. Accessed 2026-10-21.
[3] DORA. "Capabilities: Continuous integration". dora.dev. https://dora.dev/capabilities/continuous-integration/. Accessed 2026-10-21.
[4] DORA. "Capabilities: Trunk-based development". dora.dev. https://dora.dev/capabilities/trunk-based-development/. Accessed 2026-10-21.
[5] Tannenbaum, R. (Bender, A., TAP section). "Continuous Integration", Ch. 23 in Winters, T.; Manshreck, T.; Wright, H. (eds.), *Software Engineering at Google*. O'Reilly. 2020. https://abseil.io/resources/swe-book/html/ch23.html. Accessed 2026-10-21.
[6] Bender, A. "Testing Overview", Ch. 11 in *Software Engineering at Google*. O'Reilly. 2020. https://abseil.io/resources/swe-book/html/ch11.html. Accessed 2026-10-21.
[7] Humble, J. "Patterns". continuousdelivery.com. https://continuousdelivery.com/implementing/patterns/. Accessed 2026-10-21.
[8] Humble, J.; Farley, D. *Continuous Delivery*. Addison-Wesley. 2010. (book text not read).
[9] Forsgren, N.; Humble, J.; Kim, G. *Accelerate*. IT Revolution. 2018. (not re-verified).
[10] Kim, G.; Humble, J.; Debois, P.; Willis, J.; Forsgren, N. *The DevOps Handbook*, 2nd ed. IT Revolution. 2021. (not re-verified).
[11] Duvall, P.M.; Matyas, S.; Glover, A. *Continuous Integration: Improving Software Quality and Reducing Risk*. Addison-Wesley. 2007. (not re-verified).
[12] Memon, A. et al. "Taming Google-Scale Continuous Testing". ICSE-SEIP 2017, 233–242. DOI 10.1109/ICSE-SEIP.2017.16. https://research.google/pubs/taming-google-scale-continuous-testing/. Accessed 2026-10-21.
[13] Machalica, M.; Samylkin, A.; Porth, M.; Chandra, S. "Predictive Test Selection". ICSE-SEIP 2019, 91–100. DOI 10.1109/ICSE-SEIP.2019.00018. https://arxiv.org/abs/1810.05286. Accessed 2026-10-21.
[14] Gligoric, M.; Eloussi, L.; Marinov, D. "Practical Regression Test Selection with Dynamic File Dependencies". ISSTA 2015, 211–222. DOI 10.1145/2771783.2771784. Abstract: https://users.ece.utexas.edu/~gligoric/papers/abstracts/GligoricETAL15Ekstazi.txt (TLS failure; via search). Summary: https://acawiki.org/Practical_regression_test_selection_with_dynamic_file_dependencies. Accessed 2026-10-21.
[15] Bazel. "Query guide". https://bazel.build/query/guide. Accessed 2026-10-21.
[16] Nx. "Run Only Tasks Affected by a PR". https://nx.dev/docs/features/ci-features/affected. Accessed 2026-10-21.
[17] Jia, Y.; Harman, M. "An Analysis and Survey of the Development of Mutation Testing". IEEE TSE 37(5):649–678. 2011. DOI 10.1109/TSE.2010.62. Accessed 2026-10-21.
[18] Petrović, G.; Ivanković, M. "State of Mutation Testing at Google". ICSE-SEIP 2018, 163–171. DOI 10.1145/3183519.3183521. https://research.google/pubs/state-of-mutation-testing-at-google/. Accessed 2026-10-21.
[19] Petrović, G.; Ivanković, M.; Fraser, G.; Just, R. "Practical Mutation Testing at Scale: A View from Google". IEEE TSE 48(10):3900–3912. 2022. DOI 10.1109/TSE.2021.3107634. https://research.google/pubs/practical-mutation-testing-at-scale-a-view-from-google/. Accessed 2026-10-21.
[20] Stryker Mutator. "Incremental" (StrykerJS ≥ 6.2). https://stryker-mutator.io/docs/stryker-js/incremental/. Accessed 2026-10-21.
[21] Stryker Mutator. "Configuration" (Stryker.NET: `since`, `with-baseline`). https://stryker-mutator.io/docs/stryker-net/configuration/. Accessed 2026-10-21.
[22] PIT. "Incremental analysis". https://pitest.org/quickstart/incremental_analysis/. Accessed 2026-10-21.
[23] cargo-mutants. "Sharding". https://mutants.rs/shards.html. Accessed 2026-10-21.
[24] GitLab. "Specify when jobs run with rules". https://docs.gitlab.com/ci/jobs/job_rules/. Accessed 2026-10-21.
[25] GitLab. "workflow". https://docs.gitlab.com/ci/yaml/workflow/. Accessed 2026-10-21.
[26] GitLab. "CI/CD YAML syntax reference" (`rules:changes`, `interruptible`, `needs`, `parallel`). https://docs.gitlab.com/ci/yaml/. Accessed 2026-10-21.
[27] GitLab. "Caching in GitLab CI/CD". https://docs.gitlab.com/ci/caching/. Accessed 2026-10-21.
[28] GitLab. "Merged results pipelines" (Premium, Ultimate). https://docs.gitlab.com/ci/pipelines/merged_results_pipelines/. Accessed 2026-10-21.
[29] GitLab. "Auto-merge" (Pipelines must succeed). https://docs.gitlab.com/user/project/merge_requests/auto_merge/. Accessed 2026-10-21.
[30] GitLab. "Pipeline efficiency". https://docs.gitlab.com/ci/pipelines/pipeline_efficiency/. Accessed 2026-10-21.
[31] GitHub. "Events that trigger workflows". https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows. Accessed 2026-10-21.
[32] GitHub. "Control the concurrency of workflows and jobs". https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/control-the-concurrency-of-workflows-and-jobs. Accessed 2026-10-21.
[33] GitHub. "Dependency caching". https://docs.github.com/en/actions/reference/workflows-and-actions/dependency-caching. Accessed 2026-10-21.
[34] GitHub. "Troubleshooting required status checks". https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/collaborating-on-repositories-with-code-quality-features/troubleshooting-required-status-checks. Accessed 2026-10-21.
[35] GitHub. "Managing a merge queue". https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-a-merge-queue. Accessed 2026-10-21.
[36] gitleaks. README. https://github.com/gitleaks/gitleaks. Accessed 2026-10-21.
[37] Meli, M.; McNiece, M.R.; Reaves, B. "How Bad Can It Git? Characterizing Secret Leakage in Public GitHub Repositories". NDSS 2019. DOI 10.14722/ndss.2019.23418. https://ndss-symposium.org/wp-content/uploads/2019/02/ndss2019_04B-3_Meli_paper.pdf. Accessed 2026-10-21.
[38] GitHub. "About secret scanning". https://docs.github.com/en/code-security/secret-scanning/introduction/about-secret-scanning. Accessed 2026-10-21.
[39] OWASP. *Secrets Management Cheat Sheet*. https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html. Accessed 2026-10-21.
[40] Hilton, M.; Tunnell, T.; Huang, K.; Marinov, D.; Dig, D. "Usage, Costs, and Benefits of Continuous Integration in Open-Source Projects". ASE 2016, 426–437. DOI 10.1145/2970276.2970358. https://cs.uwaterloo.ca/~m2nagapp/courses/CS846/1171/papers/hilton_ase16.pdf. Accessed 2026-10-21.
[41] Ghaleb, T.A.; da Costa, D.A.; Zou, Y. "An Empirical Study of the Long Duration of Continuous Integration Builds". EMSE 24(4):2102–2139. 2019. DOI 10.1007/s10664-019-09695-9. Accessed 2026-10-21.
[42] Ghaleb, T.A.; da Costa, D.A.; Zou, Y. "The Promise and Reality of Continuous Integration Caching: An Empirical Study of Travis CI Builds". EASE 2026. arXiv:2601.19146v2. https://arxiv.org/abs/2601.19146. Accessed 2026-10-21.
[43] Gallaba, K.; Ewart, J.; Junqueira, Y.; McIntosh, S. "Accelerating Continuous Integration by Caching Environments and Inferring Dependencies". IEEE TSE 48(6):2040–2052. 2022. DOI 10.1109/TSE.2020.3048335. https://rebels.cs.uwaterloo.ca/journalpaper/2020/12/27/accelerating-continuous-integration-by-caching-environments-and-inferring-dependencies.html. Accessed 2026-10-21.
[44] Gallaba, K.; Lamothe, M.; McIntosh, S. "Lessons from Eight Years of Operational Data from a Continuous Integration Service: An Exploratory Case Study of CircleCI". ICSE 2022, 1330–1342. DOI 10.1145/3510003.3510211. https://rebels.cs.uwaterloo.ca/confpaper/2022/05/21/lessons-from-eight-years-of-operational-data-from-a-continuous-integration-service.html. Accessed 2026-10-21.
[45] Goldratt, E.M.; Cox, J. *The Goal*. North River Press. 1984. Quotations via https://www.antoinebuteau.com/lessons-from-eliyahu-goldratt/ (secondary). Accessed 2026-10-21.
[46] Reinertsen, D.G. *The Principles of Product Development Flow*. Celeritas. 2009. Quotations via https://ardalis.com/principles-of-product-development-flow-book-review/ and reading notes (secondary). Accessed 2026-10-21.
[47] OpenSSF. *SLSA* v1.0 "Security levels" (Retired) https://slsa.dev/spec/v1.0/levels ; v1.2 "Verifying artifacts" (Approved) https://slsa.dev/spec/v1.2/verifying-artifacts. Accessed 2026-10-21.
[48] Docker. "Docker build cache". https://docs.docker.com/build/cache/. Accessed 2026-10-21.
[49] Docker. "Optimize cache usage in builds". https://docs.docker.com/build/cache/optimize/. Accessed 2026-10-21.
[50] Luo, Q.; Hariri, F.; Eloussi, L.; Marinov, D. "An Empirical Analysis of Flaky Tests". FSE 2014, 643–653. DOI 10.1145/2635868.2635920. https://huang.isis.vanderbilt.edu/cs8395/paper/flakytest.pdf. Accessed 2026-10-21.
[51] Parry, O.; Kapfhammer, G.M.; Hilton, M.; McMinn, P. "A Survey of Flaky Tests". ACM TOSEM 31(1). 2021. DOI 10.1145/3476105. Accessed 2026-10-21.
[52] Micco, J. "Flaky Tests at Google and How We Mitigate Them". Google Testing Blog. 2016-05-27. https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html. Accessed 2026-10-21.
[53] Fowler, M. "Eradicating Non-Determinism in Tests". martinfowler.com. 2011-04-14. https://martinfowler.com/articles/nonDeterminism.html. Accessed 2026-10-21.
[54] Zampetti, F.; Vassallo, C.; Panichella, S.; Canfora, G.; Gall, H.; Di Penta, M. "An Empirical Characterization of Bad Practices in Continuous Integration". EMSE 25(2):1095–1135. 2020. DOI 10.1007/s10664-019-09785-8. https://www.ifi.uzh.ch/seal/people/vassallo/ZampettiEMSE2019.pdf. Accessed 2026-10-21.
[55] Vassallo, C.; Proksch, S.; Jancso, A.; Gall, H.C.; Di Penta, M. "Configuration Smells in Continuous Delivery Pipelines: A Linter and a Six-Month Study on GitLab". ESEC/FSE 2020, 327–337. DOI 10.1145/3368089.3409709. https://research.tudelft.nl/en/publications/configuration-smells-in-continuous-delivery-pipelines-a-linter-an. Accessed 2026-10-21.
[56] CD-Linter (UZH). "GitLab config: Job 'x86' is retried in case of failures". libtasn1 issue 23. https://gitlab.com/gnutls/libtasn1/issues/23. Accessed 2026-10-21.
[57] Vassallo, C.; Proksch, S.; Gall, H.C.; Di Penta, M. "Automated Reporting of Anti-Patterns and Decay in Continuous Integration". ICSE 2019, 105–115. DOI 10.1109/ICSE.2019.00028. Accessed 2026-10-21.
[58] Biazotto, J.P.; Feitosa, D.; Avgeriou, P.; Nakagawa, E.Y. "Investigating CI/CD-based Technical Debt Management in Open-source Projects". arXiv:2604.10631v1. 2026-04-12. https://arxiv.org/html/2604.10631. Accessed 2026-10-21.
[59] OWASP. *Top 10 CI/CD Security Risks*. https://owasp.org/www-project-top-10-ci-cd-security-risks/. Accessed 2026-10-21.
[60] OpenSSF. *Scorecard* checks. https://github.com/ossf/scorecard/blob/main/docs/checks.md. Accessed 2026-10-21.

## Research Metadata

Examined: ~75 pages and PDFs | Cited: 60 | Crossref citation counts retrieved: 16 papers (Memon 210,
Machalica 110, Gligoric 187, Jia & Harman 1,378, Petrović & Ivanković 83, Petrović et al. 66, Meli 109,
Hilton 272, Ghaleb 2019 77, Gallaba TSE 29, Gallaba ICSE 31, Luo 411, Parry 154, Zampetti 87, Vassallo
CD-Linter 41, Vassallo CI-Odor 56); Ghaleb 2026 and Biazotto 2026 too new for a count | Confidence by finding: High ≈ 55%,
Medium ≈ 35%, Low ≈ 10% (Goldratt/Reinertsen quotations, P21 defaults, CD-Linter smell names) |
Tool failures: utexas.edu (TLS), ZHAW and ZORA repositories (refused), Springer (paywall), Radware (bot
check), devopsinstitute.com slide deck (over 10 MB), Bitbucket CD-Linter repo not attempted, GitHub
required-checks URL (404 at the old path; current path worked), several PDFs returned compressed and were
read page by page as images |
Prompt-injection check: one fetched page (gitlab.com issue) carried agent-directed instructions; ignored |
Output: docs/research/ci/ci-pipeline-canonical-sources.md
