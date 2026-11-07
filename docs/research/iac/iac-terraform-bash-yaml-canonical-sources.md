# Research: Canonical Sources for Bash, YAML, Infrastructure-as-Code and Terraform Review Rules

**Date**: 2026-11-06 | **Researcher**: nw-researcher (Nova) | **Confidence**: High for Terraform (vendor docs agree across HashiCorp, Google, AWS and Brikman) and for the YAML typing table; Medium-High for Bash (primary docs agree; the `set -e` question is contested); Medium for tool-agnostic IaC (vendor guidance strong, academic catalogues read only in part); Low for Morris quotations and parser-version claims marked unverified | **Sources**: 47

> Input to four rules — `rules/bash.md`, `rules/yaml.md`, `rules/iac.md`, `rules/terraform.md` — each
> split into Principles, Always-flag, Advisory and Do not flag (feature D3).
> Each finding uses: **Work** / **Evidence** / **Canonicity** / **Contributes** / **Checkable in a file?** / **Caveats**.
> Access date for every web source: 2026-11-06.
> Scope: complements `rules/security.md` (shell injection CWE-78, credential literals CWE-798, secrets at
> rest CWE-312, unsafe YAML load CWE-502), `rules/ci-pipelines.md` (what a pipeline does),
> `rules/ci-runners.md` and `rules/lambda-web-app-speed.md` (their own Terraform reads), and
> `rules/continuous-delivery.md` § *Infrastructure as Code* (four bullets). Rows that touch those rules
> point to them rather than restate them (D12).

**Read the Addendum (2026-11-06) at the end first.** An independent review and a live re-check of every
row-bearing quote corrected this document; where the two disagree, the Addendum wins.

## Executive Summary

**Bash.** The GNU manual and POSIX.1-2024 define `errexit` and `pipefail`; the Google Shell Style Guide
supplies most idiom rows and **verifies D10's threshold: "more than 100 lines long, or that uses
non-straightforward control flow logic"**. ShellCheck covers quoting (SC2086), masked statuses (SC2155),
unchecked `cd` (SC2164), missing shebang (SC2148) and bashisms in `sh` (SC3010, SC3043). **No ShellCheck
check, default or optional, flags a missing `set -e` or `pipefail`**, which confirms the feature's gap.
Wooledge's BashFAQ/105 argues against `set -e` itself, and ShellCheck's SC2310 page agrees, so the rule
should flag an *unchecked failure* and a *lost pipe status* and accept explicit checks as the fix. Two
findings refine locked decisions: **`pipefail` is now POSIX** (D8 survives on portability, not on the
standard), and **a sourced `.sh` library legitimately has no shebang** (D8's no-shebang finding needs
that carve-out). D9's rationale is wrong: ShellCheck neither treats `.sh` as a dialect signal nor
discovers files. Eleven candidate Always-flag rows result, seven marked hazard.

**YAML.** The 1.1 type repository and the 1.2.2 Core schema give an exact typing diff: `yes/no/on/off/y/n`
are booleans only in 1.1; `0755` is 493 in 1.1 but 755 in 1.2; `22:22` is base 60 in 1.1; `3.10` is the
float 3.1 in *both*. Real parsers lag the spec: PyYAML is "a complete YAML 1.1 parser", Go's `yaml.v3`
is a 1.1/1.2 hybrid (and archived), and Docker's Compose reference warns about base 60 and `yes`/`no`.
So every typing row's Preferred form is **quote the string**. yamllint names the rules (`truthy`,
`key-duplicates`, `octal-values`, `anchors`) but its default preset disables `octal-values` and flags
GitHub's `on:`; **no yamllint rule catches `3.10` or `22:22`**. No study measures incidence; vendor docs
and issues show the defect recurs across projects. Seven Always-flag rows, six hazard.

**IaC and Terraform.** HashiCorp, Google Cloud, AWS and Brikman agree on remote locked state, one state
per environment, environments as thin roots over shared modules, pins in the root, and a committed lock
file. Gang of Eight (ICSE 2020, replicated 2025) supplies a category per IAC row. For Terraform, **both
measured questions resolve as "not a defect"**: HashiCorp asks for only a *minimum* `required_version`
(TFLint's own example is `>= 1.0`; AWS writes `>= 1.11`), and the lock file belongs to the root, so its
presence or absence in a child module means nothing. **D11 holds**, sharpened to `count` over a collection
indexed by `count.index`; Brikman supplies both halves, and no TFLint rule covers it. Nine IAC and
fifteen TF Always-flag rows result. Morris's book and the configuration-smell names were not read; see
Knowledge Gaps.

## Research Methodology

**Search Strategy**: Primary sources first — each tool's own documentation (gnu.org, pubs.opengroup.org,
ShellCheck wiki and manual, yaml.org, yamllint, PyYAML, go-yaml, developer.hashicorp.com, TFLint),
then hyperscaler prescriptive guidance (Google Cloud, AWS), then the canonical authors through their own
sites (Google style guide, Wooledge, Brikman's Gruntwork posts, Morris's site), then papers via Crossref,
ACM, arXiv and university repositories. Issue trackers were used only as primary evidence of a tool's
behaviour or a maintainer's position.
**Source Selection**: Types: official, technical documentation, academic; industry sources only for the
canonical author's own text or a maintainer's statement. Reputation: high or medium-high for every
row-bearing claim except Wooledge (medium, cross-checked against GNU, POSIX and ShellCheck) and StrictYAML
(medium, cross-checked against yaml.org and PyYAML).
**Verification**: Each row's claim cross-referenced across independent parties where they exist (e.g. the
`count` hazard across HashiCorp, Google and Brikman; remote locked state across AWS, Google and Brikman).
Crossref is-referenced-by-count was queried for every paper with a DOI; none was guessed. Every linter
rule id was confirmed on its own documentation page, or is marked unverified in place.
**Quality Standards**: Target 3 sources per major claim, 1 authoritative minimum. Avg reputation ≈ 0.90.
Interpretation is labelled; each Synthesis subsection is interpretation except where a source is cited.

---

## Findings

## 1. Bash

Source ids in this section run B1–B12; Full Citations gives each in full. Every ShellCheck code below
was confirmed on its own wiki page this session unless marked otherwise.

### 1.1 GNU Bash Reference Manual: `set -e`, `set -u`, `pipefail`

**Work**: Free Software Foundation. *Bash Reference Manual*, § 4.3.1 "The Set Builtin".
https://www.gnu.org/software/bash/manual/html_node/The-Set-Builtin.html [B1] (gnu.org; official for its
own tool, high).
**Evidence**: `-e`: "Exit immediately if a pipeline (see Pipelines), which may consist of a single simple
command (see Simple Commands), a list (see Lists of Commands), or a compound command (see Compound
Commands) returns a non-zero status." It does not exit when the failing command is "part of the command
list immediately following a `while` or `until` reserved word, part of the test in an `if` statement,
part of any command executed in a `&&` or `||` list except the command following the final `&&` or `||`,
any command in a pipeline but the last (subject to the state of the `pipefail` shell option), or if the
command's return status is being inverted with `!`." `-u`: "Treat unset variables and parameters other
than the special parameters '@' or '*', or array variables subscripted with '@' or '*', as an error when
performing parameter expansion." `pipefail`: "If set, the return value of a pipeline is the value of the
last (rightmost) command to exit with a non-zero status, or zero if all commands in the pipeline exit
successfully. This option is disabled by default."
**Canonicity**: The shell's own manual; it defines the behaviour every other source argues about.
**Contributes**: The mechanism behind two hazard rows. Without `pipefail`, `curl … | jq …` reports
`jq`'s status and a failed download passes (SH-2). `errexit` is suspended inside conditions and `&&`/`||`
lists, which is why a function called from an `if` runs without it (SH-11 Advisory).
**Checkable in a file?** Yes. The `set` line, the shebang and each pipeline are visible.
**Caveats**: `inherit_errexit` (Bash 4.4+) was not read on the manual's `shopt` page: gnu.org returned
HTTP 429. Its behaviour is taken from B4 and ShellCheck SC2311 (1.6), two independent sources.

### 1.2 POSIX Shell Command Language, IEEE Std 1003.1-2024 (Issue 8)

**Work**: The Open Group / IEEE. *The Open Group Base Specifications Issue 8, IEEE Std 1003.1-2024*,
Shell Command Language. https://pubs.opengroup.org/onlinepubs/9799919799/utilities/V3_chap02.html [B2]
(standards body, high).
**Evidence**: `set -e`: "when any command fails … the shell immediately shall exit", with exceptions:
"The failure of any individual command in a multi-command pipeline, or of any subshell environments in
which command substitution was performed during word expansion, shall not cause the shell to exit. Only
the failure of the pipeline itself shall be considered." `-o pipefail`: "Derive the exit status of a
pipeline from the exit statuses of all of the commands in the pipeline, not just the last (rightmost)
command." `[[` sits among words that "may be recognized as reserved words, in which case the results are
unspecified"; `local` sits in the table of command names whose "results are unspecified".
**Canonicity**: The standard `#!/bin/sh` promises. Issue 8 is the current edition.
**Contributes**: **A correction to D8's premise.** `pipefail` *is* POSIX as of the 2024 edition. `[[ ]]`
and `local` remain unspecified. D8's verdict survives on portability, not on the standard: the shells
behind `/bin/sh` adopted `pipefail` late (1.8).
**Checkable in a file?** Yes: a `#!/bin/sh` script that uses `[[`, `local` or arrays shows it.
**Caveats**: Read through WebFetch in two windows of a 262,782-character page; the quotations come from
the `set` special built-in and § 2.4.

### 1.3 Google Shell Style Guide

**Work**: Google. "Shell Style Guide". https://google.github.io/styleguide/shellguide.html [B3]
(google.github.io, Google-hosted; treated as developers.google.com-equivalent technical documentation,
high). Undated page, revision 2.02 per prior knowledge (**not re-verified**).
**Evidence**: When to use shell: "Shell should only be used for small utilities or simple wrapper
scripts." "If you are writing a script that is more than 100 lines long, or that uses non-straightforward
control flow logic, you should rewrite it in a more structured language *now*. Bear in mind that scripts
grow." "If performance matters, use something other than shell." "When assessing the complexity of your
code (e.g. to decide whether to switch languages) consider whether the code is easily maintainable by
people other than its author." Files: "Executables must start with `#!/bin/bash` and minimal flags."
"Executables should have a `.sh` extension or no extension." "Libraries must have a `.sh` extension and
should not be executable." Quoting: "Always quote strings containing variables, command substitutions,
spaces or shell meta characters"; "Use `"$@"` unless you have a specific reason to use `$*`";
"Using braces in `${var}` is *not* a form of quoting." Tests: "`[[ … ]]` is preferred over `[ … ]`,
`test` and `/usr/bin/[`", because "no pathname expansion or word splitting takes place between `[[` and
`]]`." Locals: "Declare function-specific variables with `local`." "Declaration and assignment must be
separate statements when the assignment value is provided by a command substitution; as the `local`
builtin does not propagate the exit code from the command substitution." Pipes: "Bash also has the
`PIPESTATUS` variable that allows checking of the return code from all parts of a pipe." "`eval` should
be avoided." "Always check return values and give informative return values." ShellCheck "is recommended
for all scripts, large or small."
**Canonicity**: The most widely cited published shell style guide; written for a Bash-only codebase.
**Contributes**: **D10's threshold, verified: "more than 100 lines long, or … non-straightforward control
flow logic".** It also backs `[[ ]]` (SH-6), `local` (SH-7), declare-then-assign (SH-3), quoting (SH-4),
check-every-return (SH-1) and the library-without-shebang exception (Do not flag).
**Checkable in a file?** Mostly. Line count, `[[`, `local`, quoting and `eval` are visible. "Easily
maintainable by people other than its author" is not.
**Caveats**: The guide **says nothing on `set -e` or `pipefail`** beyond a warning to "be wary" of a
standalone `(( … ))` "particularly with `set -e` enabled". "Strict mode" has no Google backing; it comes
from practitioner writing (Conflict B-1). The guide mandates Bash, so its `[[ ]]` and `local` rows say
nothing about a `#!/bin/sh` script.

### 1.4 Wooledge, BashFAQ/105: "Why doesn't set -e … do what I expected?"

**Work**: Greg Wooledge et al. (GreyCat's wiki). https://mywiki.wooledge.org/BashFAQ/105 [B4] (community
wiki; not in the trusted list; the de facto reference of the #bash IRC community; medium, cross-referenced
against B1, B2 and ShellCheck).
**Evidence**: "GreyCat's personal recommendation is simple: don't use set -e. Add your own error checking
instead." "As soon as a function is used as a conditional … set -e stops being applied within the
function." "In function f, the exit status of somecommand is discarded" (the `local var=$(…)` case).
"Using a pipe makes no difference, as only the rightmost process is considered." "set -o pipefail is a
workaround by returning the exit code of the first failed process", with the warning that "with pipefail
in effect, code like this will sometimes cause an error" (a reader closing a pipe early, e.g. `head`).
"Subshells from command substitution unset set -e, however (unless inherit_errexit is set with Bash
4.4)."
**Canonicity**: The longest-standing public catalogue of `set -e` edge cases; ShellCheck's own SC2310
page ends with the same advice (1.6).
**Contributes**: **The case against an "always use `set -e`" row.** It agrees with Google on the goal
(check every failure) and differs on the mechanism. A rule can always-flag an *unchecked* failure; it
cannot always-flag a *missing* `set -e` when the script checks explicitly.
**Checkable in a file?** Partly: whether a command's failure is tested is visible; whether it matters is
judgement.
**Caveats**: A personal recommendation, worded as one. See Conflict B-1.

### 1.5 Wooledge, BashPitfalls

**Work**: https://mywiki.wooledge.org/BashPitfalls [B5] (community wiki, medium).
**Evidence**: Pitfall 1 (`for f in $(ls *.mp3)`): "This entire approach is fatally flawed, and there is
no trick that can make it work." Pitfall 4 (`[ $foo = "bar" ]`): "you should quote your variables if you
aren't sure whether they could contain white space or wildcards." Pitfall 19 (`cd /foo; bar`): "You must
always check for errors from a cd command." Pitfall 22: "you cannot rely on x && y || z if y has any
chance of failure!" Pitfall 27 (`local var=$(cmd)`): "it's best to use separate commands for this".
Pitfall 60 (`set -euo pipefail`): "There are many pitfalls to enabling these options at the start of a
script."
**Canonicity**: Numbered, stable anchors; widely linked from ShellCheck's wiki.
**Contributes**: A second, independent source for SH-3, SH-4, SH-5, SH-8 and the `a && b || c` Advisory,
with stable pitfall numbers usable as citations.
**Checkable in a file?** Yes for every pitfall quoted.
**Caveats**: Pitfall numbers have shifted over the wiki's life; cite the heading as well as the number.

### 1.6 ShellCheck wiki: default checks

**Work**: Vidar Holen et al. ShellCheck wiki, https://github.com/koalaman/shellcheck/wiki [B6] (github.com,
the tool's own docs; medium-high per the trusted list, high as primary for its own tool).
**Evidence (titles verbatim)**:
- SC2086 "Double quote to prevent globbing and word splitting." Exceptions: "Sometimes you want to split
  on spaces, like when building a command line" — use arrays, or `set -f`.
- SC2155 "Declare and assign separately to avoid masking return values." "`export` will instead always
  return true … This may prevent conditionals, `set -e` and traps from working correctly."
- SC2164 "Use `cd ... || exit` in case `cd` fails."
- SC2148 "Tips depend on target shell and yours is unknown. Add a shebang." Fix: a shebang, `-s`, a
  `# shellcheck shell=` directive, "or use a `.bash`, `.ksh`, or `.dash` file extension".
- SC2064 "Use single quotes, otherwise this expands now rather than when signalled."
- SC3043 "In POSIX sh, `local` is undefined." "`local` is supported in many shells, including bash, ksh,
  dash, and BusyBox ash. However, it is not specified by POSIX."
- SC3010: the page's first sentence is "POSIX sh uses `[ ]` and `test` instead." (Its title did not
  render through WebFetch; that it covers `[[ ]]` in `sh` is from the sentence.)
- SC3040: `set -o` with an option POSIX does not define (via B9; title not read directly).
**Canonicity**: ShellCheck is the de facto shell linter; Dong et al. (1.9) used it as their analyser.
**Contributes**: The linter column for SH-3, SH-4, SH-5, SH-12, SH-13 and SH-14.
**Checkable in a file?** Yes, by definition.
**Caveats**: SC2045 (iterating `ls` output), SC2046, SC2068 and SC2034 appear in the wiki's page index;
their titles were **not read this session**. SC2034 as "unused variable" rests on the feature's own
ShellCheck 0.11.0 run.

### 1.7 ShellCheck: optional checks and dialect detection

**Work**: ShellCheck wiki "Optional" (https://github.com/koalaman/shellcheck/wiki/Optional) [B7], SC2310,
SC2311, SC2312 wiki pages, and the manual page `shellcheck.1.md`
(https://raw.githubusercontent.com/koalaman/shellcheck/master/shellcheck.1.md) [B8].
**Evidence**: The Optional page lists eleven checks, off by default: `add-default-case`,
`avoid-negated-conditions`, `avoid-nullary-conditions`, `check-extra-masked-returns` ("Check for
additional cases where exit codes are masked"), `check-set-e-suppressed` ("Notify when set -e is
suppressed during function invocation"), `check-unassigned-uppercase`, `deprecate-which`,
`quote-safe-variables`, `require-double-brackets` ("Require [[ and warn about [ in Bash/Ksh"),
`require-variable-braces` (SC2250), `useless-use-of-cat`. Codes confirmed on their own pages:
`check-extra-masked-returns` → SC2312 ("Consider invoking this command separately to avoid masking its
return value (or use '|| true' to ignore)"); `check-set-e-suppressed` → SC2310 ("This function is
invoked in an 'if' condition so set -e will be disabled") and SC2311 ("Bash implicitly disabled set -e
for this function invocation because it's inside a command substitution"). SC2310's page ends: "You may
also want to consider replacing `set -e` with explicit `|| exit` after every relevant command to avoid
such surprises." Dialect: "The default is to deduce the shell from the file's `shell` directive,
shebang, or `.bash/.bats/.dash/.ksh` extension, in that order." The directive is "useful for files meant
to be included (and thus lacking a shebang)." Default severity: "The default is *style*."
**Canonicity**: Primary for the tool.
**Contributes**: (a) **No ShellCheck check, default or optional, flags a missing `set -e` or `pipefail`.**
The eleven optional names and the default checks read this session include none; a search of the issue
tracker found no such request accepted (closest: issue 2237, "add check for set e and operator", status
unread). The feature delta's claim stands, with that caveat. (b) **`require-double-brackets` has no SC
code on the Optional page**; cite it by name. (c) **ShellCheck does not treat `.sh` as a dialect
signal**: `.sh` is absent from the extension list, so a `.sh` file with no shebang gets SC2148. (d)
**ShellCheck does not discover files.** It checks the files it is given; finding extensionless scripts by
shebang is the caller's job (`find`, pre-commit's `types: [shell]`, an editor).
**Checkable in a file?** Yes.
**Caveats**: The SC code for `require-double-brackets` may exist (likely SC2292, **unverified**); do not
cite a number until read.

### 1.8 ShellCheck issue 2555: `pipefail` in POSIX `sh`

**Work**: "`set -o pipefail` is part of POSIX now, consider disabling the warning for `sh`".
https://github.com/koalaman/shellcheck/issues/2555 [B9] (github.com, medium-high).
**Evidence**: Opened 2022-08-11 citing the POSIX draft; closed as completed by the maintainer through
PR 3305 on 2025-09-25, with a later commit referencing POSIX.1-2024 for SC3040. Commenters report that
Debian's dash rejected `set -o pipefail` in 2023 ("Illegal option -o pipefail"), that upstream dash
merged support by November 2024, that the then-current Ubuntu LTS lacked it in September 2025, and that
macOS's `sh` lacked it in 2026.
**Canonicity**: Primary for ShellCheck's behaviour; secondary (user reports) for each shell's support.
**Contributes**: **D8 holds for a practical reason.** A `#!/bin/sh` script that sets `pipefail` fails
outright on any `/bin/sh` without it, so a rule must not demand it there. The same thread shows newer
ShellCheck accepts `pipefail` in `sh`, so ShellCheck's silence there is no longer evidence either way.
**Checkable in a file?** Yes.
**Caveats**: Shell-support dates are user comments, **unverified** against dash's changelog.

### 1.9 Dong et al., "Bash in the Wild: Language Usage, Code Smells, and Bugs" (TOSEM 2023)

**Work**: Yiwen Dong, Zheyang Li, Yongqiang Tian, Chengnian Sun, Michael W. Godfrey, Meiyappan Nagappan.
*ACM TOSEM* 32(1), 2023. DOI 10.1145/3517193 [B10] (acm.org, academic, high). Companion: Zheyang Li,
"An Empirical Study on Bash Language Usage in Github", MMath thesis, University of Waterloo, 2021
(uwspace.uwaterloo.ca, academic, high) [B11].
**Evidence (thesis abstract, read in full)**: "based on an analysis over one million open-source Bash
scripts found in Github repositories … Using static analysis, we find that Bash scripts are often error
prone, and the error-proneness has a moderately positive correlation with the size of the script. We
also find that the most common problem areas concern quoting, resource management, command options,
permissions, and error handling."
**Canonicity**: Crossref is-referenced-by-count **14** (queried 2026-11-06). The largest empirical study
of Bash in the wild found.
**Contributes**: Empirical warrant for the row families: quoting (SH-4), resource management (SH-8 trap
cleanup), error handling (SH-1 to SH-3, SH-5). The size correlation backs D10's Advisory with data,
not only Google's opinion.
**Checkable in a file?** n/a (it justifies rows).
**Caveats**: The TOSEM full text was not reachable (404 at the author's site); per-code frequencies and
the correlation coefficient are **not quoted**. "Moderately positive" is the authors' wording.

### 1.10 Mazurak & Zdancewic, "ABASH: Finding Bugs in Bash Scripts" (PLAS 2007)

**Work**: Karl Mazurak, Steve Zdancewic. *PLAS '07*. DOI 10.1145/1255329.1255347 [B12] (acm.org,
academic, high). Crossref is-referenced-by-count **18** (queried 2026-11-06).
**Evidence**: Bibliographic record only; text not read this session.
**Contributes**: Historical canonicity: static analysis of Bash for argument-splitting defects predates
ShellCheck. Nothing citable for a row.
**Caveats**: Greenberg et al.'s POSIX shell semantics (Smoosh, POPL 2020) and related work were **not
located** this session; see Knowledge Gaps.

### 1.11 Synthesis: Bash (interpretation unless a source is cited)

**What a rule adds over ShellCheck.** Two hazard rows have no linter at all: an unchecked failure with
no `errexit` (SH-1) and a pipeline that loses its left-hand failure (SH-2). Two more have none: `trap`
cleanup (SH-8) and function-scoped `local` (SH-7), and the length Advisory (SH-A1) has none. SH-13 is
only partly linted, since newer ShellCheck accepts `pipefail` in `sh` (1.8). Everything else restates a
ShellCheck code; under D13 the rule cites it and stands down where CI runs ShellCheck with that check
enabled.

**Candidate Always-flag rows**

| Id | Defect | Preferred form | Linter | Sources | Hazard |
|---|---|---|---|---|---|
| SH-1 | A Bash script with no `set -e` in which a command whose failure the next step depends on goes unchecked | `set -euo pipefail` after the shebang, or an explicit `\|\| exit` / `if !` on that command | none (no ShellCheck check flags a missing `set -e`, 1.7) | B1, B3 ("Always check return values"), B4 | **hazard** |
| SH-2 | A pipeline in a Bash script with no `pipefail` and no `PIPESTATUS` check, whose left-hand command can fail (`curl … \| jq …`) | `set -o pipefail`, or test `"${PIPESTATUS[@]}"` immediately after | none | B1, B2, B3, B4 | **hazard** |
| SH-3 | `local`, `export`, `declare` or `readonly` combined with `$(…)` | Declare, then assign on its own line | SC2155 | B3, B5 #27, B6 | **hazard** |
| SH-4 | An unquoted parameter expansion or command substitution in a command argument, `[ ]` test, or `for` list | Double-quote it; use `"$@"`; build argv in an array where splitting is wanted | SC2086 (SC2068 for `$@`, title unread) | B3, B5 #4, B6 | **hazard** |
| SH-5 | `cd` unchecked in a script without `errexit` | `cd dir \|\| exit` | SC2164 | B5 #19, B6 | **hazard** |
| SH-6 | `[ … ]` or `test` in a Bash script | `[[ … ]]` | `require-double-brackets` (optional; SC code unverified) | B3 | no |
| SH-7 | A variable assigned inside a Bash function without `local` and read only there | `local name` | none | B3 | no (leaks state; interpretation) |
| SH-8 | A script that creates a temp file, directory, lock or background process and registers no `trap … EXIT` to remove it | `tmp=$(mktemp)` then `trap 'rm -f "$tmp"' EXIT` | none | B10/B11 ("resource management"); interpretation for the form | no |
| SH-12 | A `.sh` file, or an executable file, with no shebang and no `# shellcheck shell=` directive | A shebang naming the shell, or the directive in a sourced library | SC2148 | B3, B6, B8 | no |
| SH-13 | A `#!/bin/sh` script that uses a Bash feature: `[[ ]]`, `local`, arrays, `set -o pipefail` (portability), `function` keyword | Rewrite in POSIX, or change the shebang to `bash` | SC3010, SC3043, SC3040 | B2, B6, B9 | **hazard** (fails under dash) |
| SH-14 | Iterating over `ls` output or an unquoted `$(find …)` | A glob (`for f in ./*.mp3`) or `find … -print0 \| while IFS= read -r -d ''` | SC2045 (title unread) | B5 #1 | **hazard** |

SH-9 to SH-11 label Advisory items below. These ids are proposals; renumber them freely before the
rule ships, since D3 forbids reuse only once an id is published.

**Candidate Advisory**
- **SH-A1 — rewrite in another language.** More than 100 lines, or "non-straightforward control flow"
  (B3); signals: arrays of records, parsing JSON or CSV in shell, nested functions with return codes.
  Dong et al. tie error-proneness to size (B10). Never Always-flag (D10).
- **SH-9 — `trap` with double-quoted expansions** (SC2064): intended at times; ask.
- **SH-10 — command substitution as an argument whose failure matters** (`cmd "$(failing)"`):
  SC2312 under `check-extra-masked-returns` (B7).
- **SH-11 — a function called inside `if`, `!`, `&&`/`||` or `$(…)` that relies on `set -e` internally**
  (SC2310, SC2311; B1, B4).
- **`a && b || c` used as if-then-else** (B5 #22).
- **`eval`** (B3: "should be avoided"); an injection path belongs to `security.md` CWE-78.
- **No ShellCheck in CI** — one Advisory per project (D13).

**Candidate Do not flag**
- A `#!/bin/sh` script's omission of `pipefail`, `[[ ]]` and `local` (D8; B2, B9). `set -eu` there is
  complete.
- A missing `set -e` where every command whose failure matters is checked explicitly (B4, SC2310's own
  advice).
- A sourced library (`.sh`, not executable) with no shebang that carries a `# shellcheck shell=`
  directive (B3, B8).
- SC2034 (unused) on a variable a sourcing script or `envsubst` reads.
- Unquoted expansion where splitting is the documented intent and globbing is off or impossible, e.g.
  `$#`, `$?`, an arithmetic context, the left side of `[[ ]]` (B3: no splitting inside `[[ ]]`).
- Any row whose SC code the project's CI already enforces with ShellCheck (D13).

**Conflict B-1** (set -e) is recorded under Conflicting Information.

## 2. YAML

Source ids run Y1–Y16. The question for every row: what does the parser that reads this file make of
this scalar? The answer depends on the YAML version the parser implements, so 2.4 records which parser
implements which.

### 2.1 YAML 1.1 type repository: `bool`, `int`, `float`, `merge`

**Work**: Oren Ben-Kiki, Clark Evans, Brian Ingerson. "Boolean Language-Independent Type for YAML
Version 1.1" (Working Draft 2005-01-18), https://yaml.org/type/bool.html [Y1]; "Integer …" (2005-02-11),
https://yaml.org/type/int.html [Y2]; "Merge Key …" (2005-01-18), https://yaml.org/type/merge.html [Y3]
(yaml.org; the specification's own site, official for YAML, high).
**Evidence**: Booleans: `y|Y|yes|Yes|YES|n|N|no|No|NO|true|True|TRUE|false|False|FALSE|on|On|ON|off|Off|OFF`.
Integers: `[-+]?0[0-7_]+ # (base 8)` and `[-+]?[1-9][0-9_]*(:[0-5]?[0-9])+ # (base 60)`, with examples
`octal: 02472256` and `sexagesimal: 190:20:30`. Merge: "The '<<' merge key is used to indicate that all
the keys of one or more specified maps" be inserted; each pair "is inserted into the current mapping,
unless the key already exists in it"; for a sequence, "Keys in mapping nodes earlier in the sequence
override keys specified in later mapping nodes."
**Canonicity**: The 1.1 type repository is what PyYAML, libyaml-based parsers and Go's `yaml.v2` resolve
against (2.4).
**Contributes**: The exact lexicon for YAML-1 (22 boolean spellings, `y` and `n` included), YAML-3
(leading-zero octal) and YAML-4 (`xx:yy` base 60). The merge semantics for YAML-6: a key written in the
mapping silently beats the merged one, and the first merged map beats later ones.
**Checkable in a file?** Yes; each is a lexical pattern on a plain (unquoted) scalar.
**Caveats**: The float page (base-60 floats such as `20:30.15`) was not fetched; Docker's docs link it
(2.5).

### 2.2 YAML 1.2.2 (2021-10-01): the Core and JSON schemas

**Work**: YAML Language Development Team. *YAML Ain't Markup Language Version 1.2*, Revision 1.2.2
(2021-10-01). https://yaml.org/spec/1.2.2/ [Y4] (official, high).
**Evidence**: Version 1.2's "primary focus was making YAML a strict superset of JSON. It also removed many
of the problematic implicit typing recommendations." Core Schema (§ 10.3.2): bool is
`true | True | TRUE | false | False | FALSE`; int base 8 is `0o [0-7]+`; base 10 `[-+]? [0-9]+`; base 16
`0x [0-9a-fA-F]+`; float `[-+]? ( \. [0-9]+ | [0-9]+ ( \. [0-9]* )? ) ( [eE] [-+]? [0-9]+ )?`. JSON
Schema bool: `true | false`. Mappings: "The content of a mapping node is an unordered set of key/value
node pairs, with the restriction that each of the keys is unique."
**Canonicity**: The current spec.
**Contributes**: **The 1.1→1.2 typing diff, settled:**

| Plain scalar | YAML 1.1 (Y1, Y2) | YAML 1.2 Core (Y4) |
|---|---|---|
| `yes`, `no`, `on`, `off`, `y`, `n` (any case listed) | bool | string |
| `0755` | int 493 (octal) | int 755 (decimal) |
| `0o755` | string | int 493 |
| `22:22`, `190:20:30` | int (base 60): 1342, 685230 | string |
| `<<` as a key | merge | an ordinary key (no merge type in the Core schema) |
| `3.10`, `9.3` | float 3.1, 9.3 | float 3.1, 9.3 |
| `true`, `false`, `null`, `~` | bool, null | bool, null |

Two rows matter most. **`0755` changes value between versions**, so its meaning depends on the parser.
**`3.10` is a float under both**, so the version-string defect is not a 1.1 artefact.
**Checkable in a file?** Yes.
**Caveats**: The 1.2.2 text read this session contains no "changes from 1.1" list and no statement on the
merge key; that 1.2 dropped `<<` rests on its absence from the Core schema table, and on ruamel.yaml's
changelog treating merge keys as a supported extension (2.4). Duplicate-key *uniqueness* is quoted; the
spec's statement of what a parser must *do* on a duplicate was not found.

### 2.3 yamllint: rules and defaults

**Work**: Adrien Vergé et al. yamllint documentation, "Rules" and "Configuration".
https://yamllint.readthedocs.io/en/stable/rules.html [Y5], …/configuration.html [Y6] (readthedocs.org,
technical documentation, high); issue 666, https://github.com/adrienverge/yamllint/issues/666 [Y7].
**Evidence**: `truthy`: "forbid non-explicitly typed truthy values other than allowed ones (by default:
`true` and `false`), for example `YES` or `off`"; `allowed-values: ['true', 'false']`,
`check-keys: true`. `key-duplicates`: "prevent multiple entries with the same key in mappings";
`forbid-duplicated-merge-keys: false`. `octal-values`: "prevent values with octal numbers";
`forbid-implicit-octal: true`, `forbid-explicit-octal: true` when enabled. `float-values`: options
`forbid-inf`, `forbid-nan`, `forbid-scientific-notation`, `require-numeral-before-decimal`, all false.
`anchors`: "report duplicated anchors and aliases referencing undeclared anchors";
`forbid-undeclared-aliases: true`, `forbid-duplicated-anchors: false`, `forbid-unused-anchors: false`.
`quoted-strings`: forbid "any string values that are not quoted"; `required: true`. **Default preset**:
`anchors: enable`, `key-duplicates: enable`, `truthy: level: warning`, **`octal-values: disable`**,
**`float-values: disable`**, `quoted-strings: disable`. The `relaxed` preset sets `truthy: disable`.
Issue 666, "False positive with github actions yaml" (2024-04-03): the warning on `on:` is "intended
default behavior"; fixes are quoting the key, `check-keys: false`, or, "Since #650 and yamllint 1.34.0",
a `%YAML 1.2` directive.
**Canonicity**: The de facto YAML linter; its rule names are the citation column D3 asks for.
**Contributes**: The linter column for YAML-1 (`truthy`), YAML-3 (`octal-values`), YAML-5
(`key-duplicates`), YAML-6 (`key-duplicates` with `forbid-duplicated-merge-keys`) and YAML-7
(`anchors`). **No yamllint rule catches `3.10` or `22:22`**: `float-values` has no option for it, and only
`quoted-strings` (off by default, and noisy) would. Those rows are where a review adds most.
**Checkable in a file?** Yes.
**Caveats**: The rules page shows no version number. **Default yamllint flags GitHub Actions' `on:`**,
which is D7's case; D13's "CI runs the linter" exemption therefore needs the project's config, not the
mere presence of yamllint.

### 2.4 Which parser implements which YAML

| Parser (consumer) | Version it resolves | Evidence | Status |
|---|---|---|---|
| PyYAML | 1.1 | "a complete YAML 1.1 parser" — pyyaml.org/wiki/PyYAML [Y8] | Verified |
| ruamel.yaml | 1.2 | "a YAML 1.2 loader/dumper package for Python" — pypi.org/project/ruamel.yaml [Y9] | Verified (default version not stated on the page) |
| Go `gopkg.in/yaml.v3` | "most of YAML 1.2, but preserves some behavior from 1.1" | README: 1.1 bools "supported as long as they are being decoded into a typed bool value. Otherwise they behave as a string"; "Octals encode and decode as *0777* per YAML 1.1, rather than *0o777*"; no base-60 floats. "THIS PROJECT IS UNMAINTAINED"; archived 2025-04-01 — github.com/go-yaml/yaml [Y10] | Verified |
| Go `gopkg.in/yaml.v2` | 1.1 | Prior knowledge | **Unverified** |
| `sigs.k8s.io/yaml` (Kubernetes, Helm) | Converts YAML to JSON "using go-yaml" then `json.Unmarshal` — github.com/kubernetes-sigs/yaml [Y11] | README names neither v2 nor v3 for the main package (both forks sit in the repo) | **Version unverified** |
| GitHub Actions | Reads `on:` as a key | yamllint issue 666 (maintainer); third-party yamllint configs say "GitHub likely parses as 1.2" | **Unverified**: no GitHub doc found naming its parser or YAML version |
| GitLab CI (Ruby Psych) | libyaml-based; 1.1 by prior knowledge | docs.ruby-lang.org/en/master/Psych.html: "leverages libyaml" [Y12] | **Version unverified** |
| Docker Compose | Documents 1.1 hazards | Docker's Compose reference warns about base 60 and `yes`/`no` (2.5) | Parser library **unverified** |

**Contributes**: A reviewer cannot assume 1.2. Go's v3 is a hybrid: `0755` is octal 493 there, as in 1.1,
not 755 as the 1.2 spec says. So the safe Preferred form for every typing row is **quote the string**,
which every version reads alike. "Which parser" settles only the Do-not-flag cases (D7).
**Caveats**: Interpretation, from the table: no consumer was verified as a pure YAML 1.2 Core reader.

### 2.5 Vendor docs that warn about the defect

**Work**: Docker. "Compose file reference: services", https://docs.docker.com/reference/compose-file/services/
[Y13] (docker.com/docs, official, high). actions/setup-python issue 160, "Python 3.10 not recognized"
(2020-11-04), https://github.com/actions/setup-python/issues/160 [Y14] (github.com, medium-high).
**Evidence**: Docker, `ports`: "`HOST:CONTAINER` should always be specified as a (quoted) string, to avoid
conflicts with YAML base-60 float." Docker, `environment`: boolean values "should be enclosed in quotes
to ensure they are not converted to True or False by the YAML parser" (applies to `true`, `false`, `yes`,
`no`). setup-python 160: the error was "Version 3.1 with arch x64 not found"; the maintainer replied,
"You should specify input with quotes to treat it as string."
**Canonicity**: Two primary vendors documenting the defect in their own product.
**Contributes**: Primary evidence that YAML-1, YAML-2 and YAML-4 bite in practice in exactly the files D5
names (compose, CI). Further instances from the same search, not read in full: Apache Arrow PR 11608
(2021) and LaunchDarkly openfeature-python-server PR 43 both quote `"3.10"` for this reason.
**Checkable in a file?** Yes.
**Caveats**: setup-python's own advanced-usage doc quotes every version (`'3.13'`) but never says why.

### 2.6 Duplicate keys: spec says unique, PyYAML keeps the last

**Work**: yaml/pyyaml issue 165, "Duplicate keys are not handled properly", opened 2018-05-10, still open,
labelled `task:bug`. https://github.com/yaml/pyyaml/issues/165 [Y15] (github.com, primary for the
parser's behaviour).
**Evidence**: PyYAML "naively overwrites results with the last key"; the sample loads as
`{'a': {'q': 'b'}}`. A project member: "I think forbidding duplicate keys should be the default" and
"merge key behaviour should stay the same." Search snippets (not read in full) report the same defect
costing dbt-core users a whole `models:` block (dbt-core issue 5114) and ruamel.yaml raising
`DuplicateKeyError`.
**Canonicity**: Primary.
**Contributes**: YAML-5 is a **hazard**: under the most-used Python parser the first value vanishes
without an error. The merge-key carve-out explains why yamllint's `forbid-duplicated-merge-keys` is off by
default.
**Checkable in a file?** Yes.
**Caveats**: Other parsers' duplicate-key behaviour (Go v3, Psych, GitHub Actions) **not verified**.

### 2.7 The Norway problem and implicit typing in general

**Work**: Colm O'Connor, StrictYAML, "The Norway Problem — why StrictYAML refuses to do implicit typing
and so should you". https://hitchdev.com/strictyaml/why/implicit-typing-removed/ [Y16] (author's project
site; not in the trusted list; medium — it names the problem, and its examples are reproducible against
Y1 and Y8).
**Evidence**: A list of country codes ending `- NO` loads under PyYAML as
`{'countries': ['GB', 'IE', 'FR', 'DE', False]}`. `postgres: 9.3` loads under ruamel.yaml as a float, so
"downstream code receives a type it didn't expect"; `surname: Null` loads as `None`.
**Canonicity**: The origin of the name "Norway problem"; widely repeated (bram.us 2022; a January 2026
write-up; both medium, not relied on).
**Contributes**: The `null` case for an Advisory (YAML-A2), and a second independent source for YAML-1
and YAML-2.
**Caveats**: StrictYAML argues for its own library; the bias is declared, the examples are checkable.

### 2.8 How common is the defect? (interpretation)

No source found measures incidence: no empirical study of YAML typing defects in CI or config files
turned up (Knowledge Gaps). What the sources show is *recurrence*: two vendors document it in their
reference pages (Y13), a setup-python maintainer answered it in 2020 (Y14), unrelated projects shipped
the same fix (Arrow, LaunchDarkly), and PyYAML's duplicate-key bug has stayed open since 2018 (Y15). The
feature's scan found no instance in the sibling repos. Read together, the defect is **rare per file but
recurring across projects, and severe when it lands**, which fits a hazard row that seldom fires. US-02's
dogfood clause ("or records that none exists") is the right acceptance test.

### 2.9 Synthesis: YAML (interpretation unless a source is cited)

**Candidate Always-flag rows**

| Id | Defect | Preferred form | Linter | Sources | Hazard |
|---|---|---|---|---|---|
| YAML-1 | A plain value spelled as a YAML 1.1 boolean other than `true`/`false` (`yes`, `no`, `on`, `off`, `y`, `n`, any case), where the author meant a string or the consumer's schema wants a string | Quote it (`"no"`); write `true`/`false` where a boolean is meant | yamllint `truthy` (default: warning) | Y1, Y4, Y5, Y13, Y16 | **hazard** |
| YAML-2 | A plain value that reads as a number but is meant as a string: a version (`3.10`, `1.20`), an id or code with significant zeros or dots | Quote it (`"3.10"`) | none (`quoted-strings`, off by default, is the nearest) | Y4 (float in 1.1 and 1.2), Y14, Y16 | **hazard** |
| YAML-3 | A plain integer with a leading zero (`0755`, `01234`) | Quote it if a string; if a number, write it without the zero or, for a mode, as the consumer documents (`"0755"`, or `0o755` only for a 1.2 parser) | yamllint `octal-values` (off by default) | Y2, Y4, Y10 | **hazard** (value differs by parser) |
| YAML-4 | A plain `digits:digits` value (`22:22`, `10:30`) | Quote it (`"22:22"`) | none | Y2, Y13 | **hazard** |
| YAML-5 | The same key twice in one mapping | One key; merge the values by hand | yamllint `key-duplicates` (default: on) | Y4, Y5, Y15 | **hazard** |
| YAML-6 | Two `<<` merge keys in one mapping, or a mapping whose own key silently overrides a merged key the author meant to keep | One `<<: [*a, *b]` in precedence order; delete or rename the overriding key | yamllint `key-duplicates` with `forbid-duplicated-merge-keys: true` (off by default) | Y3, Y5 | **hazard** |
| YAML-7 | An anchor name defined twice in one document | Unique anchor names | yamllint `anchors` with `forbid-duplicated-anchors: true` (off by default) | Y5 | no |

**Candidate Advisory**
- **YAML-A1 — merge keys in a file whose consumer does not document them.** `<<` is a 1.1 type, absent
  from the 1.2 Core schema; under a pure 1.2 reader it is an ordinary key (Y3, Y4).
- **YAML-A2 — `null`, `Null`, `~` or an empty value where a string was meant** (Y4, Y16).
- **YAML-A3 — no `yamllint` in CI, or a config that disables `truthy` and `key-duplicates`** (D13).
- **YAML-A4 — a schema exists for the file (JSON Schema store, Kubernetes OpenAPI) and nothing validates
  against it** (interpretation).

**Candidate Do not flag**
- **A key the consuming tool defines**: GitHub Actions' `on:` (Y7; D7). yamllint's maintainer calls the
  warning intended and offers `check-keys: false` or `%YAML 1.2`; the review should apply that exemption
  without asking for either.
- **A value the consumer's typed schema coerces safely and documents** — e.g. a Go struct field typed
  `bool` under `yaml.v3`, where `yes` decodes as `true` by design (Y10). Flag only where the author's
  intent was a string.
- `true`, `false`, quoted scalars, `0o` octals in a file read by a parser known to implement 1.2.
- Helm `templates/*.yaml` (D6).
- A duplicate key produced by a YAML merge (`<<`), which is the merge mechanism, not a duplicate (Y15's
  member comment).
- A row whose yamllint rule the project's CI enforces with that rule enabled (D13). The rule must read the
  config: `octal-values` and `float-values` are off in yamllint's default preset.

## 3. Infrastructure as Code (tool-agnostic)

Source ids run I1–I9. `rules/continuous-delivery.md` § *Infrastructure as Code* (line 145) holds four
bullets: treat infrastructure like application code; provision environments automatically; never make
manual changes to production; environments are disposable and reproducible. This section supplies the
checkable form of each, stated so no single tool owns it. Terraform is the evidence for most rows because
the vendors write their prescriptive guidance for it; section 4 gives the Terraform form.

### 3.1 Kief Morris, *Infrastructure as Code*, 3rd edition (O'Reilly, 2025)

**Work**: Kief Morris. *Infrastructure as Code: Designing and Delivering Dynamic Systems for the Cloud
Age*, 3rd ed. O'Reilly, March 2025 per the publisher's listing (ISBN 9781098150358 per retailer listings;
retailers give dates from 2025-03-25 to 2025-04-29). The author's site, https://infrastructure-as-code.com/
[I1] (author's own statement, medium-high): "The third edition is out now, in print and ebook, and on the
O'Reilly Learning Platform." 1st ed. 2016, 2nd ed. 2020 (prior knowledge, **not re-verified**).
**Evidence**: Site subtitle: "Using software engineering practices to design and deliver dynamic
infrastructure." The publisher's catalogue record lists chapters including "Design principles for
infrastructure as code", "Infrastructure components" and "Designing deployable infrastructure stacks"
(via search snippet). **No principle text was read this session.** The site does not state the
principles the task names (reproducible, disposable, drift, snowflake, environments differing by
parameters).
**Canonicity**: The book that named the practice for most practitioners; Morris is a Thoughtworks
distinguished engineer (catalogue record).
**Contributes**: Canonicity for the rule's Principles section and its vocabulary ("stack", "deployable
stack"). The *checkable* rows below rest on the vendor and academic sources, not on Morris.
**Checkable in a file?** n/a.
**Caveats**: Paywalled; see Knowledge Gaps. Any Morris quotation in `iac.md` must be checked against the
book first.

### 3.2 Rahman, Mahdavi-Hezaveh, Williams, "A systematic mapping study of infrastructure as code research" (IST 2019)

**Work**: Akond Rahman, Rezvan Mahdavi-Hezaveh, Laurie Williams. *Information and Software Technology*,
2019. DOI 10.1016/j.infsof.2018.12.004 [I2] (sciencedirect.com, academic, high). Crossref
is-referenced-by-count **148** (queried 2026-11-06).
**Evidence**: Bibliographic record only this session.
**Canonicity**: The standard survey of IaC research; the most-cited paper in this section.
**Contributes**: Canonicity only: the field's map. Nothing row-bearing was read.
**Caveats**: Abstract not read; listed in Knowledge Gaps.

### 3.3 Rahman, Farhana, Parnin, Williams, "Gang of Eight: A Defect Taxonomy for Infrastructure as Code Scripts" (ICSE 2020), and its 2025 replication

**Work**: ICSE 2020. DOI 10.1145/3377811.3380409 [I3] (acm.org, academic, high). Crossref
is-referenced-by-count **64** (queried 2026-11-06). Replication: Wendell Oliveira, Filipe Paiva, Thiago
Emmanuel Pereira, João Brunet, "A Defect Taxonomy for Infrastructure as Code: A Replication Study",
arXiv:2505.01568v3, 2025-06-18 [I4] (arxiv.org, academic, high).
**Evidence (I4, quoting and mapping the original's categories)**: Conditional — "flawed logic or branching
conditions"; Configuration data — "incorrect settings or values"; Dependency — "missing or improperly
specified external requirements like packages or files"; Documentation — "inaccurate information in
comments or READMEs"; Idempotency — "code causes unintended changes when run multiple times instead of
ensuring a consistent state"; Security — "vulnerabilities such as exposing secrets"; Service — "problems
provisioning or managing services like databases or web servers"; Syntax — "basic grammatical errors in
the code". "Configuration data is the most frequent category in all datasets". "defect proportions were
remarkably similar between the original study (15.3%) and this replication (16.8%)", across 3,364
defect-related commits from 285 PL-IaC repositories (Pulumi, CDK). The original analysed 1,448
defect-related commits and surveyed 66 practitioners (search snippet; NSF PAR record, not read in full).
**Canonicity**: The only defect taxonomy specific to IaC found; replicated on a second tool family.
**Contributes**: A category column for `iac.md`, the way Zampetti ids served `ci-pipelines.md`: each IAC
row maps to a Gang of Eight category (Dependency for pinning and lock files; Idempotency for
imperative scripts; Configuration data for environment copies and hard-coded values). Security belongs
to `security.md` (D12).
**Checkable in a file?** Categories, not rows. Syntax defects are a parser's job.
**Caveats**: The original's category definitions are quoted through the replication's paraphrase. The
categories classify *fix commits*; they say what goes wrong, not how a reviewer sees it.

### 3.4 Sharma, Fragkoulis, Spinellis, "Does Your Configuration Code Smell?" (MSR 2016)

**Work**: MSR 2016, pp. 189–200. DOI 10.1145/2901739.2901761 [I5] (acm.org, academic, high). Crossref
is-referenced-by-count **109** (queried 2026-11-06). Author draft:
https://www.spinellis.gr/pubs/conf/2016-MSR-conf-smells/html/SFS16.html.
**Evidence**: "We propose a catalog of 13 implementation and 11 design configuration smells"; "We
analyzed 4,621 Puppet repositories containing 8.9 million lines of code"; "the design configuration
smells show 9% higher average co-occurrence among themselves"; "design configuration smell density shows
negative correlation" with size.
**Canonicity**: The founding configuration-smell catalogue; the second-most-cited work here.
**Contributes**: Precedent for splitting IaC defects into *implementation* (line-level, linter-shaped) and
*design* (module-level, reviewer-shaped) smells, which matches the rule's Always-flag / Advisory split.
**Checkable in a file?** Implementation smells, yes (they extended Puppet-Lint); design smells needed a
separate tool.
**Caveats**: **The 24 smell names were not retrieved**; do not cite a smell by name until read. Puppet,
not Terraform. No Terraform- or HCL-specific smell study was found (Knowledge Gaps).

### 3.5 Google Cloud, "Best practices for using Terraform"

**Work**: Google Cloud. "Best practices for general style and structure", "… for root modules", "… for
reusable modules". https://docs.cloud.google.com/docs/terraform/best-practices/ (moved from
cloud.google.com/docs, 301) [I6] (cloud.google.com/docs, technical documentation, high).
**Evidence (root modules)**: "Don't include more than 100 resources (and ideally only a few dozen) in a
single state." Split a service into `modules` and `environments` directories; "Each environment directory
must contain the following files:" `backend.tf` and `main.tf`; use only the default workspace. "Other
Terraform environments and applications can reference root module-level outputs only." Providers:
"declare each provider and pin to a minor version" (example `~> 4.0.0`). Lock file: "should be checked
into source control. This allows for tracking and reviewing changes in provider selections."
**Evidence (reusable modules)**: "When referencing a module, use a version constraint to pin to the major
version." Shared modules declare minimum provider versions (`>= 4.0.0`); "Unless proven otherwise, assume
that new provider versions will work." Modules "must not configure providers or backends". "For every
resource defined in a shared module, include at least one output that references the resource."
**Evidence (style)**: "Give variables defined types." "Variables must have descriptions." For
environment-specific values (such as `project_id`), "don't provide default values." "To instantiate a
resource conditionally, use the `count` meta-argument." "Avoid custom scripts, if possible. Use them only
when Terraform resources don't support the desired behavior." "All Terraform files must conform to the
standards of `terraform fmt`."
**Canonicity**: A hyperscaler's prescriptive guidance, independent of HashiCorp.
**Contributes**: The tool-agnostic shapes for IAC-2 (one state per environment), IAC-3 (environments call
shared modules and differ by input), IAC-4/IAC-5 (pin in the deployable unit, lock committed), IAC-6 (a
reusable unit configures no backend) and the size Advisory.
**Checkable in a file?** Yes for all but the resource-count ceiling, which needs a count across files.
**Caveats**: Google's examples are GCP; the principles quoted are not.

### 3.6 AWS Prescriptive Guidance, "Backend best practices" (Terraform AWS Provider)

**Work**: AWS. https://docs.aws.amazon.com/prescriptive-guidance/latest/terraform-aws-provider-best-practices/backend.html
[I7] (docs.aws.amazon.com, official, high).
**Evidence**: "Storing Terraform state remotely in Amazon S3, with S3 native state locking, provides key
benefits over local file storage." "State locking prevents concurrent write operations and reduces errors
from simultaneous changes by multiple users. Use S3 native state locking by setting `use_lockfile = true`.
It's generally available in Terraform 1.11 and later, so set `required_version = ">= 1.11"`. Locking
through Amazon DynamoDB (the `dynamodb_table` argument) is deprecated." "Use distinct Terraform backends
for each application environment." "Although you can use Terraform workspaces to separate state between
environments, distinct backends provide stronger isolation." "Restrict permissions for the production
state backend to read-only access for most users. Limit who can modify the production infrastructure to
the CI/CD pipeline and break glass roles."
**Canonicity**: The second hyperscaler, independent of Google and HashiCorp.
**Contributes**: IAC-1 (remote state with locking), IAC-2 (separate backend per environment), and the
pipeline-only production apply that operationalises `continuous-delivery.md`'s "never make manual
changes". Also **a vendor writing a lower-bound-only `required_version`** (4.4).
**Checkable in a file?** Yes: the backend block, its locking argument and the per-environment layout.
**Caveats**: S3-specific mechanics; the principle (remote, locked, isolated) is generic.

### 3.7 Brikman, "How to manage Terraform state" (Gruntwork; *Terraform: Up & Running* ch. 3)

**Work**: Yevgeniy Brikman. https://www.gruntwork.io/blog/how-to-manage-terraform-state [I8] (vendor
blog by the book's author; not in the trusted list; medium-high as the author's own text). First
published 2016-09-29; updated 2022-09-28 for Terraform 1.2 and the book's 3rd edition.
**Evidence**: Storing state in version control is "a *bad idea*" (manual error, no locking, plaintext
secrets). "Most of the remote backends natively support locking." Workspaces "are not a suitable
mechanism for isolating one environment from another"; file layout is "useful for production use cases
for which you need strong separation between environments"; use "separate Terraform folders (and
therefore separate state files) for each environment".
**Canonicity**: The book chapter excerpt; the standard practitioner reference.
**Contributes**: Third independent source for IAC-1 and IAC-2.
**Checkable in a file?** Yes.
**Caveats**: Gruntwork sells Terraform tooling (Terragrunt); the advice matches AWS and Google.

### 3.8 HashiCorp, `terraform plan`: saved plans and drift

**Work**: HashiCorp. "terraform plan command". https://developer.hashicorp.com/terraform/cli/commands/plan
[I9] (vendor docs, primary for the tool, high).
**Evidence**: `-out=FILENAME` "Writes the generated plan to the given filename in an opaque file format
that you can later pass to `terraform apply` to execute the planned changes." `-detailed-exitcode`: "0 =
Succeeded with empty diff (no changes)", "1 = Error", "2 = Succeeded with non-empty diff (changes
present)". `-refresh-only` "creates a plan whose goal is only to update the Terraform state and any root
module output values to match changes made to remote objects outside of Terraform."
**Contributes**: The mechanism for IAC-7 (apply the plan that was reviewed) and IAC-A1 (detect drift on a
schedule: exit code 2 on an unchanged commit means the world moved).
**Checkable in a file?** In the pipeline file that runs the tool.
**Caveats**: The page does not use the word "drift"; that framing is interpretation. Ownership: a
pipeline row about *how* a job runs is `ci-pipelines.md`'s; this rule owns only that infrastructure
changes go through a reviewed plan.

### 3.9 Synthesis: IaC (interpretation unless a source is cited)

Each row names its Gang of Eight category (I3) beside its sources.

**Candidate Always-flag rows**

| Id | Defect | Preferred form | Linter | Sources (category) | Hazard |
|---|---|---|---|---|---|
| IAC-1 | State kept locally, committed to version control, or in a shared backend with locking off | A remote backend with locking on; state files ignored by version control | none | I7, I8, T1 (.gitignore) (Dependency) | **hazard** (concurrent apply corrupts or loses state; lost state recreates resources) |
| IAC-2 | Two environments share one state, or are separated only by a workspace switch | One backend (and, where the platform allows, one account) per environment | none | I6, I7, I8 (Configuration data) | no |
| IAC-3 | An environment added by copying another's directory and editing values inline: two environment roots whose resource definitions differ in more than input values | One shared module; each environment a thin root that passes its inputs | none | I6 (Configuration data) | no |
| IAC-4 | A deployable root that does not bound its tool or provider versions from above (no `~>` or equivalent) | A lower and upper bound per provider in the root | `terraform_required_providers` checks presence only | T2, I6 (Dependency) | no |
| IAC-5 | A deployable root with no committed dependency lock | Commit the tool's lock file | none | T1, T3, I6 (Dependency) | no |
| IAC-6 | A reusable module that configures its own backend or provider credentials | Configure backends and providers in the root only | none | I6 (Dependency) | no |
| IAC-7 | A pipeline or script that applies changes without applying the plan a person or gate reviewed (plan and apply in one unreviewed step, `-auto-approve` on an unsaved plan to production) | Save the plan, review it, apply that file | none | I9, I7 (pipeline-only production apply) | no |
| IAC-8 | Environment-specific identifiers (account, project, region, CIDR) hard-coded in a reusable module, or given a default there | A variable with no default, set by each environment's root | none | I6 (Configuration data) | no |
| IAC-9 | An imperative script (`local-exec`, a wrapper shell step) doing what a declared resource can do | The declared resource | none | I6 ("Avoid custom scripts") (Idempotency) | no |

**Candidate Advisory**
- **IAC-A1 — no drift detection**: no scheduled plan whose non-empty result (`-detailed-exitcode` 2)
  alerts someone (I9). Operationalises "never make manual changes to production".
- **IAC-A2 — one state holds more than about 100 resources** (Google: "ideally only a few dozen") (I6).
- **IAC-A3 — production state writable by people rather than only by the pipeline and break-glass
  roles** (I7). Usually invisible in the file; ask.
- **IAC-A4 — a reusable module with no output for a resource it creates** (I6).
- **IAC-A5 — no IaC linter or format check in CI** (D13).

**Candidate Do not flag**
- A lower-bound-only constraint on the tool or providers **in a reusable module** (T2, I6).
- A lower-bound-only tool constraint (`required_version = ">= 1.11"`) in a root (T2 sets upper bounds for
  providers only; I7 writes exactly this).
- A missing lock file in a module that is never a root (T3).
- Secrets in code or state: `security.md` owns them (CWE-798, CWE-312); flag there, once.
- Hand-run applies in a project that has declared no pipeline for infrastructure: flag the missing
  pipeline once as Advisory, not every file.

## 4. Terraform

Source ids run T1–T10. Each row that is the Terraform form of an IAC row points to it.

### 4.1 HashiCorp Terraform style guide

**Work**: HashiCorp. "Style Guide". https://developer.hashicorp.com/terraform/language/style [T1]
(vendor docs, primary, high).
**Evidence**: "Run `terraform fmt` and `terraform validate` before committing your code to version
control." Files: `backend.tf`, `main.tf`, "A `outputs.tf` file that contains all output blocks in
alphabetical order", `providers.tf`, "A `variables.tf` file that contains all variable blocks in
alphabetical order." "Define a `type` and a `description` for every variable." "For sensitive variables,
such as passwords and private keys, set the `sensitive` parameter to `true`." "Only use variable
validation when your variable values have uniquely restrictive requirements." "Include a description for
every output." "Use `count` and `for_each` sparingly." "A common practice to conditionally create
resources is to use the `count` meta-argument with a conditional expression." "If some of the arguments
need distinct values that you cannot derive from an integer, use `for_each`." Versions: "We also recommend
that you set a minimum required version of the Terraform binary"; "Pin modules to a specific major and
minor version". "Use a linter such as TFLint to enforce your organization's own coding best practices."
Commit "Your `.terraform.lock.hcl` dependency lock file"; never commit "Your `terraform.tfstate` state
file", "Your `.terraform` directory", or "Any `.tfvars` files that contain sensitive information."
**Canonicity**: The tool vendor's own style guide.
**Contributes**: TF-3 (type), TF-4 (description), TF-5 (`sensitive`), TF-12 (`fmt`), the conditional
`count` exemption (D11), and **"a minimum required version of the Terraform binary"** — the measured
lower-bound-only `required_version` is the documented practice.
**Checkable in a file?** Yes.
**Caveats**: "Alphabetical order" of variables and outputs is style; leave it to the linter or nowhere.

### 4.2 HashiCorp, "Version Constraints": best practices

**Work**: https://developer.hashicorp.com/terraform/language/expressions/version-constraints [T2]
(vendor docs, high).
**Evidence**: "Reusable modules should constrain only their minimum allowed versions of Terraform and
providers, such as `>= 0.12.0`." "Root modules should use a `~>` constraint to set both a lower and upper
bound on versions for each provider they depend on." Modules: "Require specific versions to ensure that
updates only happen when convenient to you"; "Specify version ranges when your organization consistently
uses semantic versioning for modules it maintains."
**Contributes**: **Settles the `required_version` question.** HashiCorp asks for an upper bound only on
*providers* in *root* modules; for the Terraform CLI it asks only for a minimum in reusable modules, and
the style guide (T1) asks for a minimum everywhere. **All 45 lower-bound-only `required_version`
constraints are the documented practice, not a defect.** The sampled roots' `~>` provider pins are also
correct. TF-6 flags a root *provider* without an upper bound.
**Checkable in a file?** Yes, once the file is known to be a root (a `backend` block, or no caller).
**Caveats**: Root vs reusable is a judgement where a directory is both; see TF-6's Do-not-flag.

### 4.3 HashiCorp, "Dependency Lock File"

**Work**: https://developer.hashicorp.com/terraform/language/files/dependency-lock [T3] (vendor docs,
high).
**Evidence**: "At present, the dependency lock file tracks only provider dependencies." "Terraform does
not remember version selections for remote modules". The lock file "belongs to the configuration as a
whole, rather than to each separate module in the configuration"; Terraform "expects to find it in your
current working directory", the directory holding "the `.tf` files for the root module". "You should
include this file in your version control repository".
**Contributes**: **Settles the lock-file question.** A lock file is required in each root (TF-10); one in
a child module directory is never read when that module is called, so it is neither required nor a
defect (it appears when someone runs `terraform init` there, e.g. to test). The 56 of 63 directories
holding one are consistent with this; the seven without need sorting only to find any *root* among them.
**Checkable in a file?** Yes, with the root/child judgement.
**Caveats**: "Never read when called as a child" is interpretation from "belongs to the configuration as
a whole" and "current working directory".

### 4.4 HashiCorp, `count`, `for_each` and `moved`

**Work**: "The count Meta-Argument", https://developer.hashicorp.com/terraform/language/meta-arguments/count
[T5]; "The for_each Meta-Argument", …/meta-arguments/for_each [T6]; "Refactoring",
https://developer.hashicorp.com/terraform/language/modules/develop/refactoring [T7] (vendor docs, high).
**Evidence**: count: "Use the `count` argument when you want to create nearly identical instances." "Use
`for_each` when some instance arguments must have distinct values that can't be directly derived from an
integer index." "You can use the `count` argument as a conditional for creating resources" (example
`count = var.creator ? 3 : 0`). Instances are addressed by index, "starting at `0`". for_each: "accepts a
map or a set of strings"; "The keys of the map or all values in a set of strings must be known values."
moved: "You can use a `moved` block to update a resource address without destroying it." Without one,
"Terraform interprets a change as an instruction to destroy the existing resource." Example under "The old
configuration used "count" and the new configuration uses "for_each"": `moved { from =
aws_instance.c[0]  to = aws_instance.c["small"] }`. "We strongly recommend that you retain all historical
`moved` blocks"; "Removing a `moved` block is a breaking change." "Terraform v1.1 and later is required".
**Contributes**: TF-1's boundary and TF-2. **HashiCorp's docs do not themselves state that removing a
middle element recreates later instances**; that consequence is Brikman's (4.6) and follows from index
addressing.
**Checkable in a file?** Yes: `count = length(x)` with `x[count.index]` in the body is visible; so is an
address change with no `moved` block in the same diff.
**Caveats**: The heading "When to use for_each instead of count", which the task names, no longer exists;
the current heading is "How to choose between count and for_each".

### 4.5 HashiCorp, "Standard Module Structure"

**Work**: https://developer.hashicorp.com/terraform/language/modules/develop/structure [T8] (vendor docs,
high; page labelled Terraform v1.17.x).
**Evidence**: "everything is optional except for the root module." "These are the recommended filenames
for a minimal module, even if they're empty" (`main.tf`, `variables.tf`, `outputs.tf`). "All variables
and outputs should have one or two sentence descriptions that explain their purpose." "Nested modules
should exist under the `modules/` subdirectory." "Examples of using the module should exist under the
`examples/` subdirectory".
**Contributes**: TF-4 (descriptions); module layout as Advisory, since the page itself calls every file
but the root module optional.
**Checkable in a file?** Yes.

### 4.6 Brikman, *Terraform: Up & Running*, 3rd ed. (2022), via "Terraform tips & tricks: loops, if-statements, and gotchas"

**Work**: Yevgeniy Brikman. O'Reilly, 3rd ed. released 2022-09-28 (per the post). Excerpt:
https://www.gruntwork.io/blog/terraform-tips-tricks-loops-if-statements-and-gotchas [T9] (author's text,
medium-high). First published 2016-10-03; updated for Terraform 1.2 and the 3rd edition.
**Evidence**: Removing an item from the middle of a `count` list: "Terraform will delete every resource
after that item and then re-create those resources again from scratch." The plan proposes to "rename the
'trinity' IAM user to 'morpheus'" and destroy the last one. "you should almost always prefer to use
`for_each` instead of `count` to create multiple copies of a resource." For conditionals: `count =
var.enable_autoscaling ? 1 : 0`; he "typically recommend[s] using `count` to conditionally create
resources and modules."
**Canonicity**: The standard Terraform book; the post is the author's own excerpt.
**Contributes**: **Both halves of D11 from one authoritative author**: `count` over a list is the defect
(TF-1, hazard); the 0/1 toggle is the recommended idiom (Do not flag).
**Checkable in a file?** Yes.
**Caveats**: Book text itself not read; the post is the author's excerpt and is dated to the 3rd
edition.

### 4.7 TFLint terraform ruleset

**Work**: terraform-linters, tflint-ruleset-terraform. Rules index
https://github.com/terraform-linters/tflint-ruleset-terraform/blob/main/docs/rules/README.md and
configuration https://github.com/terraform-linters/tflint-ruleset-terraform/blob/main/docs/configuration.md
[T10] (github.com, primary for the tool, medium-high).
**Evidence**: Twenty rules. Recommended preset (✔ on the index): `terraform_deprecated_index` ("Disallow
legacy dot index syntax"), `terraform_deprecated_interpolation`, `terraform_deprecated_lookup`,
`terraform_empty_list_equality`, `terraform_json_syntax`, `terraform_map_duplicate_keys` ("Disallow
duplicate keys in a map object"), `terraform_module_pinned_source` ("Disallow specifying a git or
mercurial repository as a module source without pinning to a version"), `terraform_module_version`
("Checks that Terraform modules sourced from a registry specify a version"),
`terraform_required_providers` ("Require that all providers have version constraints through
required_providers"), `terraform_required_version` ("Disallow `terraform` declarations without
require_version"), `terraform_typed_variables` ("Disallow `variable` declarations without type"),
`terraform_unused_declarations`, `terraform_workspace_remote`. `all` preset only:
`terraform_comment_syntax`, `terraform_documented_outputs`, `terraform_documented_variables`,
`terraform_module_shallow_clone`, `terraform_naming_convention`, `terraform_standard_module_structure`,
`terraform_unused_required_providers`. Defaults: "When using the bundled plugin built into TFLint, you
can use this plugin without declaring a "plugin" block. In this case the default is `recommended`";
otherwise "Default: `all`". `terraform_required_version` checks presence only; its compliant example is
`required_version = ">= 1.0"` [T4].
**Contributes**: The linter column for TF-3, TF-4, TF-7, TF-8, TF-11, TF-13, TF-14. **No TFLint rule
flags `count = length(…)`**, a missing `moved` block, a provider in a child module, or a missing lock
file — those are where a review adds most. **TFLint's own example of a compliant `required_version` is
lower-bound only.**
**Checkable in a file?** Yes.
**Caveats**: The documented-variables/outputs and module-structure rules are off under the bundled
default; D13's "CI runs the linter" exemption must check which preset is configured.

### 4.8 Synthesis: Terraform (interpretation unless a source is cited)

**Candidate Always-flag rows**

| Id | Defect | Preferred form | Linter | Sources | Hazard |
|---|---|---|---|---|---|
| TF-1 | `count = length(<collection>)` (or `count` over any list) whose body reads `<collection>[count.index]` or `element(…, count.index)` | `for_each` over a map or set keyed by a stable id; migrate with `moved` blocks | none | T5, T6, T9 | **hazard** (removing a middle element recreates every later instance) |
| TF-2 | A resource or module address changed (rename, `count`→`for_each`, moved into a module) with no `moved` block in the same change | A `moved { from = … to = … }` block per changed address; keep it | none | T7 | **hazard** (destroy and recreate) |
| TF-3 | A `variable` with no `type` | `type = string` (or the narrowest type) | `terraform_typed_variables` (recommended) | T1, I6, T10 | no |
| TF-4 | A `variable` or `output` with no `description` | A one- or two-sentence `description` | `terraform_documented_variables`, `terraform_documented_outputs` (`all` only) | T1, T8, I6, T10 | no |
| TF-5 | A variable or output carrying a password, key or token with no `sensitive = true` | `sensitive = true` (it hides the value in output, not in state — CWE-312 stays `security.md`'s) | none | T1 | no |
| TF-6 | A root module's provider with no upper bound (no `~>`), or no `required_providers` entry — IAC-4's Terraform form | `version = "~> X.Y"` in `required_providers` | `terraform_required_providers` (presence only) | T2, I6, T10 | no |
| TF-7 | A `terraform` block with no `required_version` | `required_version = ">= X.Y"` | `terraform_required_version` | T1, T10 | no |
| TF-8 | A git module source with no `?ref=`, or a registry module with no `version` | Pin a tag or commit; `version = "~> X.Y"` | `terraform_module_pinned_source`, `terraform_module_version` | T2, T10 | no (supply-chain angle: `security.md`) |
| TF-9 | A `provider` configuration or `backend` block inside a reusable (child) module — IAC-6's Terraform form | Configure both in the root; pass providers in | none | I6 | no |
| TF-10 | A root module with no committed `.terraform.lock.hcl` — IAC-5's Terraform form | Commit the lock file | none | T1, T3, I6 | no |
| TF-11 | Deprecated syntax: legacy dot index (`list.0`), a lone `"${var.x}"`, two-argument `lookup()` | `list[0]`, `var.x`, `lookup(m, k, default)` or `m[k]` | `terraform_deprecated_index`, `_interpolation`, `_lookup` | T10 | no |
| TF-12 | A file not in `terraform fmt` form | Run `terraform fmt` | `terraform fmt -check` | T1, I6 | no |
| TF-13 | A map literal with a duplicate key | One key | `terraform_map_duplicate_keys` | T10 | **hazard** (Terraform's behaviour on the duplicate **unverified**) |
| TF-14 | A variable, local or data source declared and never used | Delete it | `terraform_unused_declarations` | T10 | no |
| TF-15 | State committed or a `.tfstate`, `.terraform/` or secret `.tfvars` not ignored — IAC-1's Terraform form | `.gitignore` them; a remote backend with locking | none | T1, I7, I8 | **hazard** (see IAC-1) |

**Candidate Advisory**
- **TF-A1 — module layout** off the Standard Module Structure (no `variables.tf`/`outputs.tf`, nested
  modules outside `modules/`) (T8: "everything is optional except for the root module").
- **TF-A2 — S3 backend locking through `dynamodb_table` only**: deprecated; `use_lockfile = true` with
  `required_version >= 1.11` (I7). Provider-specific, so Advisory (slice 04 puts provider rows out of
  scope).
- **TF-A3 — `count` or `for_each` where a plain block would do** ("Use `count` and `for_each` sparingly",
  T1).
- **TF-A4 — variable `validation` missing where a value has "uniquely restrictive requirements"** (T1).
- **TF-A5 — no `tflint` or `terraform validate` in CI** (D13).

**Candidate Do not flag**
- **`count = <condition> ? 1 : 0`** (and `? N : 0` for identical instances): the documented toggle (T1,
  T5, T9, I6). D11 confirmed.
- **`count = N` for nearly identical instances** that read nothing by index (T5).
- **Lower-bound-only `required_version`** anywhere (T1, T2, T10's own example, I7). The 45 measured sites
  are correct.
- **`>=` provider constraints in a reusable module** (T2, I6).
- **A missing `.terraform.lock.hcl` in a child module**, and a present one (T3).
- **A variable with no `validation`** unless its values are uniquely restricted (T1).
- **Rows whose TFLint rule the project's CI runs with that rule enabled** (D13); the bundled default is
  `recommended`, which excludes TF-4 (T10).

## Decisions tested against sources

| Decision | Support | Contrary or limiting evidence | Verdict and caveat |
|---|---|---|---|
| **D7** — a key the consuming tool defines (GitHub Actions `on:`) is Do not flag | GitHub runs workflows whose trigger key is `on:` (the feature's `ci.yml:8`); yamllint's maintainer calls the `truthy` warning on it "intended default behavior" and offers `check-keys: false` or `%YAML 1.2` (Y7) | Default yamllint flags it (Y5, Y6). No GitHub document found names its YAML parser or version (2.4). | **Holds.** Scope the exemption to keys and values the consumer *documents*; the only one evidenced is GitHub Actions' `on:`. "Any key the tool documents as a string" needs a source per tool before it is cited. |
| **D8** — `#!/bin/sh` is POSIX: no demand for `pipefail`, `[[ ]]`, `local`; a `.sh` with no shebang is a finding | `[[` and `local` are unspecified in POSIX (B2; SC3010, SC3043). dash lacked `pipefail` until about 2024 and macOS `sh` still lacks it per user reports (B9). | **`pipefail` is in POSIX.1-2024** (B2), so "POSIX has no pipefail" is no longer true. Google: "Libraries must have a `.sh` extension and should not be executable" (B3), so a sourced library legitimately has no shebang; ShellCheck's `shell=` directive exists for exactly that file (B8). | **Holds, two refinements.** (1) Rest the `pipefail` half on portability, not on the standard. (2) The no-shebang finding (SH-12) fires only on an executable file, or a `.sh` file with neither shebang nor `# shellcheck shell=` directive. **Most likely change to a locked decision in the Bash rule.** |
| **D9** — match `.sh`, `.bash`, and extensionless files whose shebang names sh/bash ("ShellCheck's own detection") | Google: "Executables should have a `.sh` extension or no extension" (B3). | ShellCheck deduces dialect from "the file's `shell` directive, shebang, or `.bash/.bats/.dash/.ksh` extension, in that order" (B8): **`.sh` is not a dialect signal, and ShellCheck does not find files**; the caller passes them. | **The match holds; the rationale is wrong.** Cite Google for the extensions and ShellCheck only for "judge the dialect by the shebang first". Also match a `.sh`-less file with a `# shellcheck shell=` directive. |
| **D10** — "rewrite in Python" is Advisory; threshold and signals per Google | Google: "more than 100 lines long, or that uses non-straightforward control flow logic … rewrite it in a more structured language *now*" (B3), plus "easily maintainable by people other than its author". Dong et al.: error-proneness correlates "moderately positive[ly]" with size (B10). | Google uses "must"-strength language ("now"); the feature's 934–1,958-line scripts work. | **Holds; 100 lines verified.** The signals "arrays of records, parsing JSON" are interpretation; Google names only length and "non-straightforward control flow". Keep Advisory: Google's own word is advice to the author, and length is not a line defect. |
| **D11** — `count` over a collection is Always-flag; `count = cond ? 1 : 0` is Do not flag | Brikman: removing a middle item makes Terraform "delete every resource after that item and then re-create"; "almost always prefer to use `for_each`"; he "typically recommend[s] using `count` to conditionally create" (T9). HashiCorp: `for_each` when values "can't be directly derived from an integer index"; `count` "as a conditional" (T5); style guide endorses the conditional (T1). Google: `count` to "instantiate a resource conditionally" (I6). | HashiCorp's own conditional example is `? 3 : 0` (T5), and `count = N` for "nearly identical instances" is documented. | **Holds, with a sharper trigger.** Flag `count` over a collection **whose body indexes it by `count.index`**; do not flag `cond ? N : 0` or `count = N` over identical instances. No TFLint rule covers it (T10), so this row is pure review value. Pair it with TF-2 (`moved`). |
| **D13** — rows cite linters; the rule never runs one; CI-run linter → Do not flag | ShellCheck, yamllint, TFLint each catch a subset (1.6–1.7, 2.3, 4.7). | Defaults differ from what a row cites: ShellCheck's `check-extra-masked-returns`, `check-set-e-suppressed` and `require-double-brackets` are off (B7); yamllint's default preset **disables** `octal-values` and `float-values` and **flags** `on:` (Y6); TFLint's bundled default is `recommended`, which excludes `terraform_documented_*` and `terraform_standard_module_structure` (T10). | **Holds, with a condition**: the Do-not-flag clause applies to a row only when the project's linter config enables *that rule*. "CI runs yamllint" is not enough. |
| **Measured: lock file in 56 of 63 `*.tf` directories** | The lock file "belongs to the configuration as a whole"; Terraform looks for it in the root's working directory; commit it (T3, T1, I6). | None found. | **A lock file in a child module is harmless and unread; its absence there is not a defect.** Flag only a *root* without one (TF-10). |
| **Measured: all 45 `required_version` lower-bound only** | Style guide: "set a minimum required version of the Terraform binary" (T1); reusable modules "constrain only their minimum" (T2); TFLint's compliant example is `>= 1.0` (T4); AWS writes `required_version = ">= 1.11"` (I7). | HashiCorp asks root modules for `~>` on **providers** (T2), not on the CLI. | **Documented practice, not a defect.** Do not flag. |

## Source Analysis

| Id | Source | Domain | Reputation | Type | Access date | Cross-verified |
|---|---|---|---|---|---|---|
| B1 | GNU Bash Reference Manual, The Set Builtin | gnu.org | High (primary) | official | 2026-11-06 | Y (B2, B4) |
| B2 | POSIX.1-2024 Shell Command Language | pubs.opengroup.org | High | standard | 2026-11-06 | Y (B1, B9) |
| B3 | Google Shell Style Guide | google.github.io | High | technical docs | 2026-11-06 | Y (B5, B6) |
| B4 | Wooledge BashFAQ/105 | mywiki.wooledge.org | Medium | community wiki | 2026-11-06 | Y (B1, SC2310) |
| B5 | Wooledge BashPitfalls | mywiki.wooledge.org | Medium | community wiki | 2026-11-06 | Y (B3, B6) |
| B6 | ShellCheck wiki: SC2086, SC2155, SC2164, SC2148, SC2064, SC3043, SC3010 | github.com | Medium-High (primary for tool) | technical docs | 2026-11-06 | Y (B3, B5) |
| B7 | ShellCheck wiki: Optional; SC2310, SC2311, SC2312 | github.com | Medium-High (primary) | technical docs | 2026-11-06 | Y (B4) |
| B8 | ShellCheck manual page `shellcheck.1.md` | github.com | Medium-High (primary) | technical docs | 2026-11-06 | Partial |
| B9 | ShellCheck issue 2555 | github.com | Medium-High (primary for tool; user reports for shells) | industry | 2026-11-06 | Partial (B2) |
| B10 | Dong et al., TOSEM 2023 | acm.org | High | academic | 2026-11-06 | Y (B11) |
| B11 | Li, MMath thesis, Waterloo 2021 | uwaterloo.ca | High | academic | 2026-11-06 | Y (B10) |
| B12 | Mazurak & Zdancewic, PLAS 2007 | acm.org | High | academic | 2026-11-06 | N (record only) |
| Y1–Y3 | YAML 1.1 type repository: bool, int, merge | yaml.org | High (spec) | official | 2026-11-06 | Y (Y4, Y13) |
| Y4 | YAML 1.2.2 specification | yaml.org | High (spec) | official | 2026-11-06 | Y (Y1, Y10) |
| Y5 | yamllint Rules | readthedocs.io | High | technical docs | 2026-11-06 | Y (Y7) |
| Y6 | yamllint Configuration | readthedocs.io | High | technical docs | 2026-11-06 | Y (Y7) |
| Y7 | yamllint issue 666 | github.com | Medium-High (maintainer) | industry | 2026-11-06 | Y (Y5) |
| Y8 | PyYAML wiki page | pyyaml.org | High (primary) | technical docs | 2026-11-06 | Y (Y16, Y15) |
| Y9 | ruamel.yaml on PyPI | pypi.org | Medium-High (primary) | technical docs | 2026-11-06 | Partial |
| Y10 | go-yaml v3 README | github.com | Medium-High (primary) | technical docs | 2026-11-06 | N |
| Y11 | sigs.k8s.io/yaml README | github.com | Medium-High (primary) | technical docs | 2026-11-06 | N |
| Y12 | Ruby Psych documentation | ruby-lang.org | High (primary) | official | 2026-11-06 | N (version not stated) |
| Y13 | Docker Compose reference: services | docs.docker.com | High | official | 2026-11-06 | Y (Y2, Y1) |
| Y14 | actions/setup-python issue 160 | github.com | Medium-High (maintainer) | industry | 2026-11-06 | Y (Arrow, LaunchDarkly PRs via snippet) |
| Y15 | yaml/pyyaml issue 165 | github.com | Medium-High (primary) | industry | 2026-11-06 | Partial (dbt-core via snippet) |
| Y16 | StrictYAML, "The Norway Problem" | hitchdev.com | Medium (author bias declared) | industry | 2026-11-06 | Y (Y1, Y8) |
| I1 | infrastructure-as-code.com (Morris) | infrastructure-as-code.com | Medium-High (author) | industry | 2026-11-06 | N |
| I2 | Rahman et al., IST 2019 | sciencedirect.com | High | academic | 2026-11-06 | N (record only) |
| I3 | Rahman et al., ICSE 2020 (Gang of Eight) | acm.org | High | academic | 2026-11-06 | Y (I4) |
| I4 | Oliveira et al., arXiv 2025 replication | arxiv.org | High | academic | 2026-11-06 | Y (I3) |
| I5 | Sharma et al., MSR 2016 | acm.org / spinellis.gr | High | academic | 2026-11-06 | N (abstract only) |
| I6 | Google Cloud, Terraform best practices (3 pages) | cloud.google.com/docs | High | technical docs | 2026-11-06 | Y (T1, T2, I7) |
| I7 | AWS Prescriptive Guidance, Backend best practices | docs.aws.amazon.com | High | official | 2026-11-06 | Y (I6, I8) |
| I8 | Brikman, "How to manage Terraform state" | gruntwork.io | Medium-High (author; vendor) | industry | 2026-11-06 | Y (I6, I7) |
| I9 | HashiCorp, `terraform plan` | developer.hashicorp.com | High (primary) | technical docs | 2026-11-06 | N |
| T1 | HashiCorp, Style Guide | developer.hashicorp.com | High (primary) | technical docs | 2026-11-06 | Y (I6, T10) |
| T2 | HashiCorp, Version Constraints | developer.hashicorp.com | High (primary) | technical docs | 2026-11-06 | Y (I6, I7) |
| T3 | HashiCorp, Dependency Lock File | developer.hashicorp.com | High (primary) | technical docs | 2026-11-06 | Y (T1, I6) |
| T4 | TFLint rule `terraform_required_version` | github.com | Medium-High (primary) | technical docs | 2026-11-06 | Y (T1, T2) |
| T5 | HashiCorp, `count` | developer.hashicorp.com | High (primary) | technical docs | 2026-11-06 | Y (T9, I6) |
| T6 | HashiCorp, `for_each` | developer.hashicorp.com | High (primary) | technical docs | 2026-11-06 | Y (T5) |
| T7 | HashiCorp, Refactoring (`moved`) | developer.hashicorp.com | High (primary) | technical docs | 2026-11-06 | N |
| T8 | HashiCorp, Standard Module Structure | developer.hashicorp.com | High (primary) | technical docs | 2026-11-06 | Y (T1) |
| T9 | Brikman, "Terraform tips & tricks" | gruntwork.io | Medium-High (author) | industry | 2026-11-06 | Y (T5, T1) |
| T10 | TFLint terraform ruleset: rules index, configuration | github.com | Medium-High (primary) | technical docs | 2026-11-06 | Y (T1) |

Reputation: High 31 (66%) · Medium-High 13 (28%) · Medium 3 (6%) · Avg ≈ 0.90. Crossref counts were
queried for every paper with a DOI; none was guessed. Sources seen only through search snippets (Apache
Arrow PR 11608, LaunchDarkly PR 43, dbt-core issue 5114, NSF PAR record for Gang of Eight, O'Reilly and
retailer listings for Morris) are named in place and not counted.

**Bias notes**: Gruntwork (I8, T9) sells Terraform tooling; StrictYAML (Y16) argues for its own library;
HashiCorp, Google and AWS each write for their own platform. Each row-bearing claim from them is
cross-checked against an independent party where one was found.

## Knowledge Gaps

### Gap 1: Morris, *Infrastructure as Code* (3rd ed.), not read
**Issue**: No principle text quoted; the author's site states none. | **Attempted**: infrastructure-as-code.com;
publisher and retailer listings via search. | **Recommendation**: Read the book's "Design principles"
chapter before `iac.md` quotes Morris; until then cite it for canonicity only.

### Gap 2: Configuration-smell names and a Terraform-specific smell study
**Issue**: Sharma et al.'s 24 smell names were not retrieved (the author draft page holds only the
abstract); Rahman et al. IST 2019's abstract was not read; no dedicated search for HCL or Terraform smell
studies was run within budget. | **Attempted**: spinellis.gr (404 on one path, abstract-only on another);
Crossref. | **Recommendation**: Read the MSR 2016 PDF and search ACM/IEEE for "Terraform smells" before
any IAC row cites a smell by name.

### Gap 3: Bash empirical frequencies
**Issue**: Dong et al.'s per-ShellCheck-code frequencies and correlation coefficient are not quoted; the
TOSEM PDF was a 404 and the thesis was read only to its abstract. Greenberg et al.'s POSIX shell work
(Smoosh) was not located. | **Recommendation**: Read the thesis's results chapter for the top codes;
it would rank SH rows by observed frequency.

### Gap 4: ShellCheck details not confirmed
**Issue**: Titles of SC2034, SC2045, SC2046, SC2068 and SC3040, and SC3010's title, were not read on
their pages; `require-double-brackets` has no SC code on the Optional page (likely SC2292,
**unverified**). `inherit_errexit` was not read in the GNU manual (HTTP 429). | **Recommendation**: Open
each page before the rule cites the code.

### Gap 5: Absence claims
**Issue**: "No linter flags a missing `set -e` or `pipefail`" rests on ShellCheck's default and optional
lists and an issue search; bashate, shfmt and shellharden were not checked. "No TFLint rule flags `count =
length(…)`" rests on the terraform ruleset's 20 rules; provider rulesets (AWS, Google, Azure) were not
checked. | **Recommendation**: Treat both as "not found", not "proven absent".

### Gap 6: Which YAML version each consumer implements
**Issue**: GitHub Actions, GitLab CI (Psych/libyaml), Docker Compose and `sigs.k8s.io/yaml` were not
confirmed against their own docs; Go `yaml.v2` as 1.1 is prior knowledge. Duplicate-key behaviour is
verified for PyYAML only. | **Recommendation**: The rule's Preferred form ("quote it") works under every
version, so this gap limits only the Do-not-flag list. Confirm per consumer before adding an exemption.

### Gap 7: YAML defect incidence
**Issue**: No study measures how often implicit-typing or duplicate-key defects occur in real CI or
config files. | **Recommendation**: The US-02 dogfood run is itself the measurement; record the count.

### Gap 8: Terraform duplicate map keys
**Issue**: TFLint forbids them (T10), but what Terraform does with a duplicate key in a map literal was
not verified; TF-13's hazard mark is provisional.

### Gap 9: Azure Well-Architected IaC guidance
**Issue**: Not read within budget. Google, AWS and HashiCorp already agree on every IAC row they share.

## Conflicting Information

### Conflict B-1: Should a Bash script use `set -e` ("strict mode")?
**Position A**: Enable `errexit` (and `pipefail`) so failures stop the script. — ShellCheck's SC2155 and
SC2312 pages explain masked statuses in terms of breaking "`set -e` and traps" (B6, B7); the GNU manual
and POSIX define the behaviour (B1, B2). Reputation: medium-high to high. Note: Google's guide does **not**
take this position (B3).
**Position B**: "don't use set -e. Add your own error checking instead." — BashFAQ/105 (B4), BashPitfalls
#60: "There are many pitfalls to enabling these options" (B5). ShellCheck's own SC2310 page: "consider
replacing `set -e` with explicit `|| exit` after every relevant command" (B7). Reputation: medium, plus
the linter's maintainer.
**Assessment**: Both positions want every failure that matters checked; Google says so outright ("Always
check return values", B3). They differ on mechanism. A rule can safely always-flag **an unchecked failure
the next step depends on** (SH-1) and **a pipeline that loses its left-hand status** (SH-2), accepting
either `set -euo pipefail` or explicit checks as the fix. It must **not** always-flag a script merely for
lacking `set -e`. `pipefail` has its own edge case: a reader that closes early (`… | head -1`) makes the
writer fail with SIGPIPE (B4); the review should not demand `pipefail` where the pipeline ends in `head`
without a check of its own.

### Conflict Y-1: Which YAML does a file speak?
**Position A**: YAML 1.2 removed `yes`/`no`/`on`/`off` booleans, leading-zero octal and base 60 (Y4).
**Position B**: PyYAML is "a complete YAML 1.1 parser" (Y8); Go's v3 keeps 1.1 octals and 1.1 bools into
typed fields (Y10); Docker documents 1.1 hazards in Compose (Y13).
**Assessment**: The spec has moved; the parsers have not. Quote the string, which both read alike. Do not
reason from the spec version alone.

### Conflict Y-2: Is `on:` a defect?
**Position A**: yamllint's default `truthy` flags it; its maintainer calls that intended (Y5, Y7).
**Position B**: GitHub Actions reads it as the trigger key, and every GitHub workflow uses it.
**Assessment**: The consumer decides (D7). Do not flag; yamllint itself offers `check-keys: false` or
`%YAML 1.2` for this case.

### Conflict T-1: How tightly to pin a module
**Position A**: "Pin modules to a specific major and minor version" (T1).
**Position B**: "use a version constraint to pin to the major version" (I6); "Require specific versions"
for third-party modules (T2).
**Assessment**: All three require a pin; they differ on granularity. TF-8 flags only an unpinned source;
granularity is the project's choice.

### Conflict T-2: `count` as a conditional versus "use sparingly"
**Position A**: "Use `count` and `for_each` sparingly" (T1).
**Position B**: The conditional `count` is "a common practice" (T1), recommended by Brikman (T9) and Google
(I6).
**Assessment**: No real conflict: "sparingly" warns against needless meta-arguments (TF-A3). The 0/1
toggle stays Do not flag (D11).

## Full Citations

[B1] Free Software Foundation. "The Set Builtin". *Bash Reference Manual*. https://www.gnu.org/software/bash/manual/html_node/The-Set-Builtin.html. Accessed 2026-11-06.
[B2] The Open Group / IEEE. "Shell Command Language". *The Open Group Base Specifications Issue 8, IEEE Std 1003.1-2024*. https://pubs.opengroup.org/onlinepubs/9799919799/utilities/V3_chap02.html. Accessed 2026-11-06.
[B3] Google. "Shell Style Guide". https://google.github.io/styleguide/shellguide.html. Accessed 2026-11-06.
[B4] Wooledge, G. et al. "BashFAQ/105: Why doesn't set -e (or set -o errexit, or trap ERR) do what I expected?". https://mywiki.wooledge.org/BashFAQ/105. Accessed 2026-11-06.
[B5] Wooledge, G. et al. "BashPitfalls". https://mywiki.wooledge.org/BashPitfalls. Accessed 2026-11-06.
[B6] Holen, V. et al. ShellCheck wiki: SC2086, SC2155, SC2164, SC2148, SC2064, SC3043, SC3010. https://github.com/koalaman/shellcheck/wiki/SC2086 (and sibling pages). Accessed 2026-11-06.
[B7] Holen, V. et al. ShellCheck wiki: "Optional", SC2310, SC2311, SC2312. https://github.com/koalaman/shellcheck/wiki/Optional. Accessed 2026-11-06.
[B8] Holen, V. "shellcheck(1)". https://raw.githubusercontent.com/koalaman/shellcheck/master/shellcheck.1.md. Accessed 2026-11-06.
[B9] tgross35 et al. "`set -o pipefail` is part of POSIX now, consider disabling the warning for `sh`". koalaman/shellcheck issue 2555, 2022-08-11, closed 2025-09-25. https://github.com/koalaman/shellcheck/issues/2555. Accessed 2026-11-06.
[B10] Dong, Y., Li, Z., Tian, Y., Sun, C., Godfrey, M. W., Nagappan, M. "Bash in the Wild: Language Usage, Code Smells, and Bugs". *ACM TOSEM* 32(1), 2023. DOI 10.1145/3517193. Crossref is-referenced-by-count 14. Accessed 2026-11-06.
[B11] Li, Z. "An Empirical Study on Bash Language Usage in Github". MMath thesis, University of Waterloo, 2021. https://uwspace.uwaterloo.ca/bitstream/handle/10012/17036/Li_Zheyang.pdf. Accessed 2026-11-06.
[B12] Mazurak, K., Zdancewic, S. "ABASH: Finding Bugs in Bash Scripts". *PLAS '07*. DOI 10.1145/1255329.1255347. Crossref is-referenced-by-count 18. Accessed 2026-11-06.
[Y1] Ben-Kiki, O., Evans, C., Ingerson, B. "Boolean Language-Independent Type for YAML Version 1.1". Working Draft 2005-01-18. https://yaml.org/type/bool.html. Accessed 2026-11-06.
[Y2] Ben-Kiki, O., Evans, C., Ingerson, B. "Integer Language-Independent Type for YAML Version 1.1". Working Draft 2005-02-11. https://yaml.org/type/int.html. Accessed 2026-11-06.
[Y3] Ben-Kiki, O., Evans, C., Ingerson, B. "Merge Key Language-Independent Type for YAML Version 1.1". Working Draft 2005-01-18. https://yaml.org/type/merge.html. Accessed 2026-11-06.
[Y4] YAML Language Development Team. *YAML Ain't Markup Language Version 1.2*, Revision 1.2.2, 2021-10-01. https://yaml.org/spec/1.2.2/. Accessed 2026-11-06.
[Y5] Vergé, A. et al. "Rules". yamllint documentation. https://yamllint.readthedocs.io/en/stable/rules.html. Accessed 2026-11-06.
[Y6] Vergé, A. et al. "Configuration". yamllint documentation. https://yamllint.readthedocs.io/en/stable/configuration.html. Accessed 2026-11-06.
[Y7] "False positive with github actions yaml". adrienverge/yamllint issue 666, 2024-04-03. https://github.com/adrienverge/yamllint/issues/666. Accessed 2026-11-06.
[Y8] PyYAML. "PyYAML". https://pyyaml.org/wiki/PyYAML. Accessed 2026-11-06.
[Y9] ruamel.yaml on PyPI, version 0.19.1 (2026-01-02 per release history). https://pypi.org/project/ruamel.yaml/. Accessed 2026-11-06.
[Y10] Niemeyer, G. et al. go-yaml v3 README. https://github.com/go-yaml/yaml/tree/v3 (archived 2025-04-01). Accessed 2026-11-06.
[Y11] Kubernetes SIGs. sigs.k8s.io/yaml README. https://github.com/kubernetes-sigs/yaml. Accessed 2026-11-06.
[Y12] Ruby. "Psych". https://docs.ruby-lang.org/en/master/Psych.html. Accessed 2026-11-06.
[Y13] Docker. "Services top-level elements". Compose file reference. https://docs.docker.com/reference/compose-file/services/. Accessed 2026-11-06.
[Y14] "Python 3.10 not recognized". actions/setup-python issue 160, 2020-11-04. https://github.com/actions/setup-python/issues/160. Accessed 2026-11-06.
[Y15] horenmar et al. "Duplicate keys are not handled properly". yaml/pyyaml issue 165, 2018-05-10. https://github.com/yaml/pyyaml/issues/165. Accessed 2026-11-06.
[Y16] O'Connor, C. "The Norway Problem — why StrictYAML refuses to do implicit typing and so should you". https://hitchdev.com/strictyaml/why/implicit-typing-removed/. Accessed 2026-11-06.
[I1] Morris, K. *Infrastructure as Code*, 3rd ed. O'Reilly, 2025; author's site https://infrastructure-as-code.com/. Accessed 2026-11-06.
[I2] Rahman, A., Mahdavi-Hezaveh, R., Williams, L. "A systematic mapping study of infrastructure as code research". *Information and Software Technology*, 2019. DOI 10.1016/j.infsof.2018.12.004. Crossref is-referenced-by-count 148. Accessed 2026-11-06.
[I3] Rahman, A., Farhana, E., Parnin, C., Williams, L. "Gang of Eight: A Defect Taxonomy for Infrastructure as Code Scripts". *ICSE 2020*. DOI 10.1145/3377811.3380409. Crossref is-referenced-by-count 64. Accessed 2026-11-06.
[I4] Oliveira, W., Paiva, F., Pereira, T. E., Brunet, J. "A Defect Taxonomy for Infrastructure as Code: A Replication Study". arXiv:2505.01568v3, 2025-06-18. https://arxiv.org/html/2505.01568v3. Accessed 2026-11-06.
[I5] Sharma, T., Fragkoulis, M., Spinellis, D. "Does Your Configuration Code Smell?". *MSR 2016*, pp. 189–200. DOI 10.1145/2901739.2901761. Crossref is-referenced-by-count 109. https://www.spinellis.gr/pubs/conf/2016-MSR-conf-smells/html/SFS16.html. Accessed 2026-11-06.
[I6] Google Cloud. "Best practices for general style and structure"; "… for root modules"; "… for reusable modules". https://docs.cloud.google.com/docs/terraform/best-practices/general-style-structure (and sibling pages). Accessed 2026-11-06.
[I7] AWS. "Backend best practices". *Best practices for using the Terraform AWS Provider*, AWS Prescriptive Guidance. https://docs.aws.amazon.com/prescriptive-guidance/latest/terraform-aws-provider-best-practices/backend.html. Accessed 2026-11-06.
[I8] Brikman, Y. "How to manage Terraform state". Gruntwork, 2016-09-29, updated 2022-09-28. https://www.gruntwork.io/blog/how-to-manage-terraform-state. Accessed 2026-11-06.
[I9] HashiCorp. "terraform plan command". https://developer.hashicorp.com/terraform/cli/commands/plan. Accessed 2026-11-06.
[T1] HashiCorp. "Style Guide". https://developer.hashicorp.com/terraform/language/style. Accessed 2026-11-06.
[T2] HashiCorp. "Version Constraints". https://developer.hashicorp.com/terraform/language/expressions/version-constraints. Accessed 2026-11-06.
[T3] HashiCorp. "Dependency Lock File". https://developer.hashicorp.com/terraform/language/files/dependency-lock. Accessed 2026-11-06.
[T4] terraform-linters. "terraform_required_version". https://github.com/terraform-linters/tflint-ruleset-terraform/blob/main/docs/rules/terraform_required_version.md. Accessed 2026-11-06.
[T5] HashiCorp. "The count Meta-Argument". https://developer.hashicorp.com/terraform/language/meta-arguments/count. Accessed 2026-11-06.
[T6] HashiCorp. "The for_each Meta-Argument". https://developer.hashicorp.com/terraform/language/meta-arguments/for_each. Accessed 2026-11-06.
[T7] HashiCorp. "Refactoring". https://developer.hashicorp.com/terraform/language/modules/develop/refactoring. Accessed 2026-11-06.
[T8] HashiCorp. "Standard Module Structure" (v1.17.x). https://developer.hashicorp.com/terraform/language/modules/develop/structure. Accessed 2026-11-06.
[T9] Brikman, Y. "Terraform tips & tricks: loops, if-statements, and gotchas". Gruntwork, 2016-10-03, updated 2022-09-28. https://www.gruntwork.io/blog/terraform-tips-tricks-loops-if-statements-and-gotchas. Accessed 2026-11-06.
[T10] terraform-linters. tflint-ruleset-terraform: rules index and configuration. https://github.com/terraform-linters/tflint-ruleset-terraform/blob/main/docs/rules/README.md; …/docs/configuration.md. Accessed 2026-11-06.

## Research Metadata

Duration: one session, 2026-11-06 | Examined: ~60 pages and records | Cited: 47 | Crossref counts: 6
papers (B10, B12, I2, I3, I5; I4 is arXiv-only) | Candidate rows: SH 11 Always-flag, YAML 7, IAC 9, TF 15 |
Confidence: High ≈ 60% of row-bearing claims, Medium ≈ 30%, Low ≈ 10% (book texts, parser versions,
smell names) | Tool failures: gnu.org `shopt` page HTTP 429; Dong et al. TOSEM PDF 404; thesis PDF
read to its abstract only; spinellis.gr Puppet-smells path 404; WebFetch could not render SC3010's title |
Output: `docs/research/iac/iac-terraform-bash-yaml-canonical-sources.md`

## Addendum 2026-11-06: independent check

The developer asked for this check after `rules/bash.md` shipped on the body above. Where the Addendum
and the body disagree, the Addendum wins. The research's row ids (SH-1 to SH-14) differ from the
shipped rule's: research SH-12, SH-13 and SH-14 are `bash.md`'s SH-8, SH-9 and SH-10 after this
Addendum's revision.

### How it was checked

- **Reasoning.** A research-reviewer agent, which cannot fetch pages, judged each candidate row against
  the Evidence it cites. Verdict: 17 of the 42 Always-flag rows over-reach their sources. The Hazard
  marks follow no stated test, and several absence claims outrun the searches behind them.
- **Quotes.** Two agents fetched the live sources and marked each row-bearing quote and linter id:

  | Section | Claims | Verified | Paraphrased | Not found | Contradicted |
  |---|---|---|---|---|---|
  | Bash | 70 | 63 | 3 | 3 | 1 |
  | YAML | 42 | 40 | 2 | 0 | 0 |
  | IaC | 62 | 58 | 1 | 0 | 2 |
  | Terraform | 60 | 58 | 1 | 0 | 0 (1 left unchecked, already marked unverified) |
  | Decisions table | 15 | 14 | 1 | 0 | 0 |

- **Parsers.** A fourth agent read each YAML consumer's parser in its source and parsed the disputed
  scalars on this machine (PyYAML 6.0.3, ruamel.yaml 0.18.10, Psych 5.1.2).

The full tables stay outside the repository; this Addendum carries every correction they make.

### The tests a row now meets

- **Hazard**: a miss changes what a run, an apply or a parse produces.
- **Always-flag**: a cited source states the defect, or, for an idiom row filed at Priority 7, names the
  preferred form. A row whose only support is this document's interpretation is Advisory.

### Bash

- Google has no section "Pipes"; its `PIPESTATUS` text sits under "Checking Return Values".
- POSIX.1-2024 treats `[[` in § 2.4 and `local` in § 2.9.1.4.
- SC3040 no longer flags `set -o pipefail` in `sh` on ShellCheck's main branch: the change merged
  2025-09-25, after release 0.11.0 (2025-08-04). Released ShellCheck still flags it.
- `require-double-brackets` is SC2292. A loop over `$(find …)` is SC2044; SC2045 covers `ls` alone.
  SC2206 covers an unquoted expansion in an array assignment.
- The guide's "revision 2.02" appears nowhere on its page.
- `local` works in dash, BusyBox ash and ksh (SC3043). Research SH-13's "fails under dash" holds for
  `[[ ]]`, arrays, `function`, and `set -o pipefail` before dash adopted it, not for `local`.
- Research SH-2 omitted Conflict B-1's carve-out for a pipeline that ends in `head`.
- Research SH-8 (a temp file with no `trap … EXIT`): no source names the defect or the form. Advisory.
- Research SH-12 (no shebang): Google requires a shebang of an executable and gives a library none, so
  the clause flagging a `.sh` library without a directive contradicts the source. Advisory.
- Research SH-6 and SH-7: Google states preferences. They are idiom rows, not defects.
- Research SH-14's `$(find …)` half rests on ShellCheck SC2044 and BashPitfalls alone.
- "No ShellCheck check flags a missing `set -e` or `pipefail`" means none among the checks read: the
  eleven optional checks, about eight default codes, and an issue search with no recorded terms.
- D10: Google says "should", not "must".

### YAML

- yamllint's `truthy` cannot flag `y` or `n`, and PyYAML reads both as strings.
- YAML 1.1 base 60 needs a first digit of 1 to 9 and later parts matching `[0-5]?[0-9]`, so `08:30`
  stays a string. Research YAML-4's `digits:digits` is broader than the hazard.
- YAML 1.2.2 § 3.2.1.3 says a processor should "flag the duplicate key as an error".
- The "intended default behavior" comment in yamllint issue 666 came from a contributor, not the
  maintainer.
- yamllint's default config disables both `octal-values` and `float-values`.
- Research YAML-6 turns on what the author meant and on a merge key only YAML 1.1 defines; research
  YAML-7 rests on an option that is off by default. Both are Advisory candidates.
- "Rare per file", and recurrence claimed from search snippets, are unmeasured.

**Which YAML each consumer reads** (source code, vendor docs and local parses; GitHub's server-side
parser is not public, so its row rests on the runner):

| Consumer | Library | YAML | `no` → false | `0755` → 493 | `1:20` base 60 | `3.10` → 3.1 |
|---|---|---|---|---|---|---|
| GitHub Actions | YamlDotNet 5.3.0, typed by the runner's `YamlObjectReader` | 1.2 core | No | No (755) | No | Yes |
| GitLab CI | Psych (`YAML.safe_load`) | 1.1 | Yes | Yes | Yes, as 4800 not 80 | Yes |
| Compose v2 | compose-go v2.16.2 on go.yaml.in/yaml/v4 | 1.2 core | Only in a bool field, with a warning | Yes | No | Yes |
| Kubernetes, Helm values | sigs.k8s.io/yaml v1.6.0 on yaml.v2 | 1.1 | Yes | Yes | No | Yes |
| PyYAML (Ansible) | PyYAML | 1.1 | Yes (not `y`/`n`) | Yes | Yes | Yes |
| ruamel.yaml | default mode | 1.2 | No | No (755) | No | Yes |
| Go yaml.v3, v4 | — | 1.2 with 1.1 bools | Only into a typed `bool` | Yes | No | Yes |

So `3.10` becomes 3.1 for every consumer, and a version-number row holds everywhere. An unquoted `no`
is false for GitLab CI, Kubernetes, Helm values, PyYAML and yaml.v2, and a string for GitHub Actions.
Feature D5 ("every YAML file") must scope its boolean and octal rows by the consumer that reads the
file. Evidence: `actions/runner` `YamlObjectReader.cs`; `actions/setup-python` issue 249; GitLab
`lib/gitlab/config/loader/yaml.rb` and its CI variables docs; `compose-spec/compose-go` v2.16.2
`loader/`; `kubernetes-sigs/yaml` `yaml.go`; `helm/helm` `pkg/chart/common/values.go`; the PyYAML
documentation; `go-yaml/yaml` v2 and v3 `resolve.go` and the v3 README.

### Infrastructure as Code

- Research IAC-4 asks for an upper bound on "tool or provider" versions. The sources bound providers
  only, as research TF-6 and the Do-not-flag list already say. Drop "tool or".
- The `terraform plan` page does use "drift", once, in its `-target` warning.
- Research IAC-3, IAC-6, IAC-8 and IAC-9 rest on Google's page alone. IAC-1's remote-state half cites a
  benefit, not a defect. IAC-7 cites pages that say nothing of reviewing a plan.
- The Gang of Eight replication (I4) studied Pulumi and CDK repositories, not declarative tools.
- **Sharma et al.'s smell names**, from the authors' InfoQ article (2016) and their tool's README, not
  the paper:
  - implementation smells: Missing Default Case, Inconsistent Naming Convention, Complex Expression,
    Duplicate Entity, Misplaced Attribute, Improper Alignment, Invalid Property Value, Incomplete
    Tasks, Deprecated Statement Usage, Improper Quote Usage, Long Statement, Incomplete Conditional,
    Unguarded Variable;
  - design smells: Multifaceted Abstraction, Unnecessary Abstraction, Imperative Abstraction, Missing
    Abstraction, Insufficient Modularization, Duplicate Block, Broken Hierarchy, Unstructured Module,
    Dense Structure, Deficient Encapsulation, Weakened Modularity.
- Morris's third edition: O'Reilly's page refused the fetch (HTTP 403). A library catalogue and
  retailers list it. The book remains unread.

### Terraform

- All twenty TFLint rules exist. The `recommended` preset holds thirteen, matching the index and
  `preset.go`. No rule examines `count`.
- The `terraform_required_version` page never calls `>= 1.0` compliant, and the output printed beneath
  that example warns. The style guide, the Version Constraints page and AWS carry the point without it.
- Research TF-1's hazard rests on Brikman alone; HashiCorp's pages state no removal hazard.
- Research TF-13's hazard is provisional: Terraform's behaviour on a duplicate map key is unverified.
- Research TF-7 rests on "we also recommend", and TF-12 is formatting. Both are Advisory candidates.
- Research TF-15's secret `.tfvars` clause belongs to `security.md`.

### Counts and metadata

- The feature delta's measured counts (45, 56 of 63) came from a scratchpad script this document does
  not record. Rerun them before a rule cites them.
- Research Metadata lists five Crossref papers, not six, and the reputation tally recounts to 29 High,
  15 Medium-High and 3 Medium.

### What changed downstream

- `rules/bash.md`: citations corrected; research SH-8 and SH-12's library clause moved to Advisory;
  `local` in `sh` moved to Advisory; the Linter cells completed; the hazard test stated.
- Slice 02 scopes its boolean and octal rows by consumer (D5). Slices 03 and 04 start from this
  Addendum's IaC and Terraform corrections.

### Slice 02 additions (2026-11-06)

Local parses under PyYAML 6.0.3, ruamel.yaml 0.18.10 and Psych 5.1.2, a fetch of the Kubernetes API
reference, and a scan of every local repository, made while writing `rules/yaml.md`:

- **Psych reads `08:30` as 30600.** Its regex, `^[-+]?[0-9][0-9_]*(:[0-5]?[0-9]){1,2}$`, admits a
  leading zero, so the YAML bullet above that `08:30` "stays a string" holds for PyYAML alone.
- **A duplicate key**: PyYAML and Psych keep the last value without an error; ruamel.yaml refuses the
  file with `DuplicateKeyError`.
- **Two `<<` keys in one mapping**: PyYAML and Psych merge both and let the later win, the reverse of
  `<<: [*a, *b]`, where the earlier wins; ruamel.yaml refuses the file. A second `<<` is therefore a
  duplicate key under research YAML-5, and research YAML-6 keeps only the own-key override, as
  Advisory.
- **Kubernetes documents octal mode bits in YAML.** `defaultMode`: "Must be an octal value between
  0000 and 0777 or a decimal value between 0 and 511. YAML accepts both octal and decimal values, JSON
  requires decimal values for mode bits." (API reference, ConfigMapVolumeSource.) Research YAML-3 does
  not reach it.
- **Incidence, measured (Gap 7).** The scan composed each file with PyYAML, matched every plain scalar
  and key against the YAML 1.1 boolean, leading-zero, base-60 and trailing-zero patterns, and compared
  each mapping's keys. Of 400 files — this repository's 50, the sibling repositories' 339 and the
  developer's other repositories' 11 — 391 parsed; the other nine are nWave documents and cloud-init
  templates. It found no instance of research YAML-1 to YAML-5. Its hits were 16 `on:` keys in GitHub
  workflows, which D7 clears, and 333 trailing-zero numbers, each meant as a number (`min`, `max`,
  `cpus: 2.0`, a weight of `1.0`) or, once, an AWS Image Builder `schemaVersion: 1.0`. Every Python
  version in a CI file was already quoted. The rule's tier rests on its sources, and the null result
  is recorded in the feature delta.
- **`rules/yaml.md`** takes research YAML-1 to YAML-5 as YAML-1 to YAML-5, scoped by the consumer
  table; research YAML-6 and YAML-7 and the merge-key and schema candidates are Advisory.

### Slices 03 and 04 evidence check (2026-11-06)

The Handoff's check, rerun over § 3 and § 4 before `iac.md` and `terraform.md`: a research reviewer
for each section, two agents that fetched every row-bearing source again, and Terraform 1.15.3 run
locally.

| Section | Claims | Verified | Paraphrased | Not found | Contradicted |
|---|---|---|---|---|---|
| IaC | 60 | 51 | 4 | 2 | 3 |
| Terraform | 88 | 84 | 1 | 0 | 3 |

**Infrastructure as Code**

- **Morris, in his own words** (the book is still unread; O'Reilly refused the fetch again):
  - drift: "The little differences and inconsistencies that accumulate between servers over time are
    Configuration Drift" (infrastructure-as-code.com, "Models for server updates", 2016);
  - copied environments: "Maintaining separate, inconsistent copies of infrastructure code for
    different environment that should be essentially consistent is an antipattern, Snowflakes as
    Code"; the remedy is to "reuse a single instance of infrastructure code for multiple instances of
    the infrastructure, and manage necessary variation between environments with parameters"
    ("Snowflakes as Code", updated 2025-01-08). In 2017 he still called per-environment definitions
    workable "for simple setups";
  - manual change: "The only changes made to an environment you care about are the ones that have
    been fed into the pipeline" ("Environment pipeline", 2017);
  - nothing on pinning versions or on applying the reviewed plan.
- Gap 1's "the site does not state the principles" holds for its home page only; the posts above do.
- Research IAC-3 now has a source that states the defect (Morris), beside Google's form.
- Research IAC-1: no page says lost state recreates resources. Brikman says committed state leads "to
  conflicts, data loss, and state file corruption"; that is the hazard. Its locking half cites a
  benefit only: Advisory.
- Research IAC-2: AWS calls workspaces acceptable with weaker isolation, so a workspace-only split is
  Advisory; two environments in one state is the hazard.
- Research IAC-7: the Addendum's "say nothing of reviewing a plan" is wrong. The plan page: "check
  whether the proposed changes match what you expected before you apply the changes or share your
  changes with your team for broader review"; the apply page recommends "first perform a plan operation
  and review the proposed changes". The row still judges a pipeline file, so it is Advisory.
- Research IAC-9: Sharma's Imperative Abstraction ("imperative statements (such as 'exec') defies the
  purpose of the language") joins Google's "Avoid custom scripts, if possible"; both are preferences,
  so Advisory.
- **Sharma et al., read in full**: the 24 names above are exact; the catalogue is Puppet only. It has no
  hard-coded-value smell; Duplicate Block means a block over 150 tokens repeated within a module, and
  Unguarded Variable an interpolation without braces. None maps to a row.
- The Gang of Eight's "Configuration data is the most frequent" comes from the replication's automated
  run; its manual classification put Syntax first (933 against 895).

**Terraform**

- **Gap 8 closed: TF-13 is a hazard.** `{ a = 1, a = 2 }` passes `terraform validate` and plans as
  `{ a = 2 }` with no warning, on Terraform 1.15.3. HashiCorp's bulletin HCSEC-2023-26: "When
  processing maps with duplicate keys, Terraform silently replaces all but the last entry", and `plan`
  "does not warn about duplicate keys". A duplicate argument in a block is a hard error ("Each argument
  may be set only once").
- **TF-1's wording.** Removing a middle element does not recreate every later instance: each later
  instance takes its neighbour's values, updated in place where it can be and replaced where an
  argument forces it, and the last is destroyed (Brikman's own plan; a local apply). The hazard stands;
  "shifts every later instance" replaces "recreates". HashiCorp's `count` page uses the pattern as an
  example, so the defect rests on Brikman alone.
- **TF-9** gains HashiCorp's own text: "A module intended to be called by one or more other modules
  must not contain any provider blocks" (providers-within-modules page).
- **TF-11**: TFLint says a lone `"${var.x}"` is "not deprecated in the latest Terraform version". The
  recommended preset covers the row and it is no hazard: dropped.
- **TF-12**: HashiCorp's `fmt` page says "you may choose not to use this command"; a formatting check
  is a CI job, not a review row: Advisory. **TF-7** rests on "We also recommend": Advisory. **TF-14**
  needs a search across files and the preset covers it: dropped. **TF-5** names a form but no defect:
  Advisory.
- **TF-8** and **TF-10** meet the hazard test: an unpinned module source or an uncommitted lock changes
  what the next `init` installs.
- **TFLint**: the recommended preset's thirteen rules are confirmed; none of the twenty reads `count`,
  `for_each` or `moved`. `terraform_map_duplicate_keys` skips keys it cannot evaluate, and sixteen
  rules lint only the directory TFLint runs in, so a child module is checked only under `--recursive`.
- The rows that restate an IaC row (TF-6, TF-9, TF-10, TF-15) stay in `iac.md`; `terraform.md` gives
  their Terraform spelling and files them under the IAC id (D12).
