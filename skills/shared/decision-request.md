# Pose a Decision Request

Shared standard for the moment a command stops and needs a call only the human can make — a blocker, an
architectural choice, which option to take on an issue, whether an irreversible action is sanctioned.

Referenced by name from the skills that hold `AskUserQuestion`. The reference is what puts this in force;
see *Reach* at the bottom for where it does not reach.

The failure this exists to stop is not a wording preference. Three modes were measured across this repo,
and all three ship a question the reader cannot act on:

| Mode | What arrives | Why it fails |
|---|---|---|
| **Bare** | A numbered option list, no framing | The options are legible; the decision is not |
| **Jargon wall** | Paragraphs of internal vocabulary | The reader must reconstruct the question before answering it |
| **Buried** | Correct wording, embedded in output | Correct content, zero signal — a *placement* defect, not a wording one |

## The shape of an ask

Emit the framing as prose **before** calling `AskUserQuestion`. The tool renders options and has no slot
that forces framing, so a call made without it reproduces mode 1 by default. Ordering is not stylistic:

1. **State what is being decided.** One sentence.
2. **State what turns on it** — what actually changes depending on the answer. Not optional, and not last.
3. **Then the options.**

Write the framing so it can be read cold, by someone who was doing something else a second ago and does
not share the loaded context.

## The ceiling

**200 words, hard.** Count the framing. Over is a failure, not a warning.

The ceiling exists to force the ordering above. If it starts evicting *what turns on it*, it is being
applied backwards — cut options, or cut to a smaller decision, and move detail below. Never cut the
framing to fit.

A decision genuinely too large to frame in 200 words is a decision to **split**. The split is the answer;
a longer ask is not.

## The detail block

Supporting detail is **permitted, unbounded, and separated** from the ask. It sits below, and it is
outside the count.

This is what makes the ceiling affordable rather than lossy. Without it, the ceiling squeezes a hard
decision and becomes the defect it was meant to prevent.

Every token the ask may not contain belongs here: file paths, issue numbers, label names, internal
identifiers, evidence, command output. Two constraints on it:

- The ask must be **answerable without reading the detail**. A consequence stated only in the detail block
  is a consequence the reader will miss.
- The detail block is not a place to restate progress. Restating the surrounding output inside the ask is
  how mode 3 gets rebuilt from the inside.

## Forbidden in the ask

No internal vocabulary in the framing or the option labels. In this plugin that means no wave labels, no
issue numbers, no slice ids, no decision numbers, no skill names, no command names used as nouns, no file
or artifact paths.

**The rule is absence, not explanation.** An explained label is still a label the reader has to hold. If
the ask needs the token to make sense, the ask is written at the wrong altitude — describe the thing, not
its identifier.

Naming a command the reader is about to run is not a violation. Naming a command as a shorthand for a
concept is.

## Placement

**Placement is part of the asking.** A conforming ask that is buried still fails.

Set the ask apart from the output that preceded it, so its existence is visible without hunting. Name what
the question is interrupting — one line, and the cheapest artifact here, so it is the one most often
dropped, because the asker never lost the thread.

## Options

Each option names its own **cost or risk**, not only its benefit. An option list where every entry reads
as an upside makes the trade invisible and pushes the reader onto the ordering.

Marking one option recommended is useful and permitted. Presenting a recommendation **without naming what
it costs** converts the ask into a rubber stamp — mode 1 in a politer register.

Collapse options that differ in wording and not in outcome. Three restatements of one option is a bare
list with extra steps.

## Do not ask at all when there is no consequence

If the answer changes nothing that can be named, do not ask. An ask with no stated consequence is a
request for reassurance wearing a decision's clothes, and it trains the reader to stop reading asks.
Decide it, state the assumption, and carry on.

This is the one clause that governs *whether* to ask rather than *how*. It is here because the ceiling
surfaces it: a framing that cannot state what turns on the answer is usually a question that should not
have been asked.

## Handling the answer

- **Silence is not consent.** An ambiguous reply — "ok", "sure", "sounds right" — is unanswered. Ask once
  more, naming what is still needed. With a recommendation on the table an ambiguous reply plausibly reads
  as acceptance, and adopting it records a decision the human never made while every visible rule looks
  satisfied.
- **A deferral is recorded as a deferral**, and whatever depended on it is reported as blocked. Never
  silently promote a deferral to the recommended option.
- **Declining and deferring are first-class** and need no decoding either. Do not make them harder to
  express than answering.

## Reach

Inside a command that references this file, the standard is in force deterministically — the reference is
loaded with the skill.

**Outside a command, it is not.** A decision request in ordinary conversation loads nothing, and the
mechanisms that would reach it are probabilistic or repo-local. That gap is real, is not closed by this
file, and must not be described as covered. It is stated here rather than left to be discovered by a
reader whose question arrived as a bare list anyway.

`rules/` cannot carry this standard, and the reason is worth recording so it is not re-proposed: a rule
with a `paths:` glob fires on the file being touched, and a decision request happens regardless of which
file is open — `rules/ux.md` already carries a *no internal jargon* line and its globs are web-UI file
types, so it is structurally dark here. A rule with **no** `paths:` is a manual-reference rule that never
auto-loads; `rules/llm-inference.md` states that semantics explicitly.
