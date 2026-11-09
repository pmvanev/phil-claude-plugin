# Research: Canonical Sources for User-Story and Issue-Card Quality (INVEST, SMART, 3 Cs)

**Date**: 2026-11-09 | **Researcher**: nw-researcher (Nova) | **Confidence**: High for INVEST, SMART and
the 3 Cs as their authors defined them (primaries read: Wake, Doran's scanned pages, Jeffries); Medium for
the template critique and splitting (Patton, Klement and Adzic read only through their own shorter texts or
secondaries); Medium-Low for Definition of Ready (one primary critic) and #NoEstimates (critics not read) |
**Sources**: 33

> Evidence base for a future `rules/stories.md` in the `phil` plugin: INVEST, SMART and related story-quality
> heuristics, recorded so the skills that compose or groom cards stay mindful of them — held lightly, not as
> a formula. Each finding uses **Work** / **Evidence** / **Canonicity** / **Contributes** / **Caveats**.
> Access date for every web source: 2026-11-09. Interpretation is labelled; the section *Applying it to
> the current card format* is interpretation throughout.

## Executive Summary

**The acronyms' authors hold them lightly themselves.** Bill Wake built INVEST (2003) by clustering
intuitions into "roughly ten fuzzy clusters" and rearranging initials into a word [1]. He pairs it with
SMART **for tasks, not stories**: "These are good characteristics for tasks as well", and his Measurable
reduces to "can we mark it as done?" [1]. George Doran's original SMART (1981) was for management
objectives, used *Assignable* and *Realistic*, and says outright that "the suggested acronym doesn't mean
that every objective written will have all five criteria", calling it "a guideline" [2]. The peer-reviewed
Quality User Story framework calls INVEST "highly qualitative" heuristics [13]. A 2023 review finds SMART
"is not based on scientific theory" [29]. The developer's stance — record them, be mindful, no formula —
matches the canonical position.

**The template is optional everywhere it is canonical.** Jeffries' 3 Cs (2001) make the card "a token
representing the requirement" and confirmation "the acceptance test" [4]. By 2019 he writes "We would
definitely not need cards with a consistent format", recalling that C3 tried one around 1998 and "realized
it was a bad idea" [7]. Cohn, the template's chief popularizer, says "There is no magic formula" [8]; Wake
says "you don't need a template to start" [28]. Klement's job stories swap the role for the *situation* [11],
[12]. The `phil` card's opening paragraph — what is wrong and why it matters — is a situation-and-motivation
statement in prose, and its `## Done when` is Jeffries' Confirmation and North's in-card acceptance
criteria [15].

**Where the sources push back.** Sticky-note brevity worked because a room held the conversation;
asynchronous, distributed boards are the named weak case [30], so the `phil` card rightly carries more —
nearer Beck's "a paragraph or two" [32] than a sticky note. The `groom-issues` rule that judges "oversized"
by demonstrability, never size, has precedent in North's "demonstrable chunks" [15] and Cockburn's "visibly
different from last slice" [18], and Lawrence and Wake show a size-only split can break Valuable and
Independent [1], [20]. But no source endorses a *large* demonstrable card, and every size the sources name
has shrunk since 2003 [1], [9], [17]. Recommendation (interpretation): keep demonstrability as the defect
test and treat the length of `## Done when` as an advisory size prompt [15], [17]. Of the 14 letters
mapped (six INVEST, five SMART, three Cs), six reduce to the three presence checks the skill already makes
— purpose, done-condition, chain. Estimable and Time-bound have no consumer on this board; the conversation
is not a body property. Everything else should stay advisory.

## Research Methodology

**Search Strategy**: Primary sources first — each author's own site (xp123.com, ronjeffries.com,
dannorth.net, mountaingoatsoftware.com, jpattonassociates.com, alistaircockburn.com, humanizingwork.com,
scrumguides.org, c2.com), then a scan of Doran's original pages, then peer-reviewed papers through the
Utrecht RE-Lab preprints and a university research portal, then glossaries and Wikipedia for lineage and
letter drift. Local: `skills/groom-issues/SKILL.md` lines 55–125 and 260–280, and this repo's existing
research documents for shape.
**Source Selection**: Types: primary practitioner texts by the originators; peer-reviewed (REFSQ, *RE
Journal*, *Health Psychology Review*); official (Scrum Guide); industry (InfoQ, martinfowler.com,
Agile Alliance); community (Scrum.org forum, Wikipedia) for sentiment and lineage only. Every source
cited was opened; where a book or original post could not be opened, the finding says so and Knowledge
Gaps lists it.
**Verification**: Each definitional claim rests on the originator's text, cross-checked against at least
one independent restatement (e.g. INVEST: Wake [1], Fowler [9], Agile Alliance [27], Lucassen [13]; 3 Cs:
Jeffries [4], Agile Alliance [5], Wake [1], c2 [32]). Bias noted: Mountain Goat Software and Humanizing
Work sell training in the practices they describe.
**Quality Standards**: Target 3 sources per major claim, 1 authoritative minimum. Average reputation ≈
0.85 (primary authors' own sites rated medium-high as the canonical record of their positions).

## Findings

### A. INVEST and SMART at their source

#### Finding A1: Wake defines INVEST for stories, as a mnemonic he built by clustering, not a derived standard

**Work**: Bill Wake, "INVEST in Good Stories, and SMART Tasks", XP123, posted 2003-08-17 (written April and
August 2003; postscript 2011-02-16) [1].

**Evidence** (verbatim from [1]):
- Independent: "Stories are easiest to work with if they are independent." / "we'd like them to not
  overlap in concept, and we'd like to be able to schedule and implement them in any order."
- Negotiable: "It is not an explicit contract for features; rather, details will be co-created…" / "A good
  story captures the essence, not the details."
- Valuable: "it needs to be valuable to the customer." / "Think of a whole story as a multi-layer cake…
  the best way is to slice vertically through the layers."
- Estimable: "We don't need an exact estimate, but just enough to help the customer rank and schedule."
- Small: "Stories typically represent at most a few person-weeks worth of work." He adds "Smaller stories
  tend to get more accurate estimates."
- Testable: "I understand what I want well enough that I could write a test for it."
- The 2011 postscript: Wake listed every attribute of good stories he could think of, grouped them into
  about ten fuzzy clusters, picked a word per cluster and rearranged the initials into a pronounceable word,
  having tried VESTIGE and VESTING. He no longer has the original list.

**Canonicity**: Primary. Wake coined INVEST; every later source cites this article. The Agile Alliance
glossary [27] confirms the 2003 origin and Cohn's 2004 adoption ("Chapter 2" of *User Stories Applied*),
and glosses V as "aluable (or vertical)", S as "mall (so as to fit within an iteration)" and T as
"estable (in principle, even if there isn't a test for it yet)".

**Contributes**: The definitions a rule should quote. Two points matter for the plugin: Negotiable says a
card "captures the essence, not the details", and the postscript shows INVEST is a memory aid over
clustered intuitions, not an empirically derived checklist. Both support holding it lightly.

**Caveats**: Wake's "Small" is a size in person-weeks, and "Estimable" exists to let a customer "rank and
schedule". Both assume a planning game the `phil` board does not run (see Finding E3 and the applying
section). Wake's Independent concerns *concept overlap and order*, not technical dependency alone.

#### Finding A2: Wake applies SMART to tasks, not to stories

**Work**: Same article [1], second half.

**Evidence** (verbatim from [1]): "There is an acronym for creating effective goals: "SMART" –" … "(There are
a lot of variations in what the letters stand for.)" … "These are good characteristics for tasks as well."
His letters are Specific ("A task needs to be specific enough that everyone can understand what's involved
in it"), Measurable ("The key measure is, "can we mark it as done?""), Achievable ("The task owner should
expect to be able to achieve a task"), Relevant ("Every task should be relevant, contributing to the story
at hand"), Time-boxed ("A task should be time-boxed: limited to a specific duration"). Wake does not
attribute SMART to anyone.

**Canonicity**: Primary.

**Contributes**: The split the developer half-remembers is exact: **INVEST for stories, SMART for the
tasks a story is broken into.** Wake's "Measurable" collapses to "can we mark it as done?", which is what
the card's `## Done when` already asks. His "Relevant" means "contributing to the story at hand" — a
task-to-story link, not a goal-to-strategy link.

**Caveats**: Wake's letters differ from Doran's (Finding A3). A rule that cites "SMART" must say whose.

#### Finding A3: Doran's SMART (1981) was for management objectives, and he said not every objective needs all five

**Work**: George T. Doran, "There's a S.M.A.R.T. way to write management's goals and objectives",
*Management Review* (AMA Forum) 70(11), November 1981, pp. 35–36. Read as a scan of the original pages [2].

**Evidence** (verbatim from the scan [2]): "Ideally speaking, each corporate, department, and section
objective should be: Specific—target a specific area for improvement. Measurable—quantify or at least
suggest an indicator of progress. Assignable—specify who will do it. Realistic—state what results can
realistically be achieved, given available resources. Time-related—specify when the result(s) can be
achieved." Then: "Notice that these criteria don't say that all objectives must be quantified on all levels
of management." / "Practicing managers and corporations can lose the benefit of a more abstract objective
in order to gain quantification." / "It is the combination of the objective and its action plan that is
really important." / "the suggested acronym doesn't mean that every objective written will have all five
criteria. However, the closer we get to the SMART criteria as a guideline, the smarter our objectives will
be."

**Canonicity**: Primary; the founding text.

**Contributes**: Doran himself framed SMART as "a guideline", warned that forced quantification destroys
abstract value, and expected objectives to miss criteria. That is the developer's "held lightly" stance,
stated by the acronym's author. His A is *Assignable* (an owner), which maps onto a card's assignee, not
onto its prose.

**Caveats**: Doran wrote about corporate objectives, not software work items. The letters drifted: A became
Achievable/Attainable/Agreed, R became Relevant, T became Time-bound; Wikipedia lists the variants [3].
The strongest published criticism is Swann et al., *Health Psychology Review* 17(2), 2023 [29] (abstract
read; full text not opened): SMART "is not based on scientific theory", "is not consistent with empirical
evidence", "does not consider what type of goal is set", "is not applied consistently" and "has a risk of
potentially harmful effects". Their field is physical-activity goals, not software; the transfer to work
items is interpretation.

### B. The 3 Cs and the card as token

#### Finding B1: Jeffries' 3 Cs (2001) make the card a token, and the confirmation an acceptance test

**Work**: Ron Jeffries, "Essential XP: Card, Conversation, Confirmation", ronjeffries.com, 2001-08-30 [4].

**Evidence** (from [4]): the card is "a token representing the requirement"; conversation is "an
*exchange* of thoughts, opinions, and feelings"; confirmation: "This component is the acceptance test."
The customer "defines the acceptance tests that will be used to show that the story has been implemented
correctly." The card carries enough to identify the need and jog memory; priority and cost notes are added
in planning.

**Canonicity**: Primary. Wake [1] cites this as the source of "Cards, Conversation, and Confirmation",
and credits Alistair Cockburn with cards as "tokens promising a future conversation".

**Contributes**: The 3 Cs give a card two jobs — *point at* the requirement and *say how it will be
confirmed*. The `phil` card's opening paragraph is the first; `## Done when` is the third.

**Caveats**: "Promise for a conversation" is Cockburn's phrase as quoted by Wake [1] and the Agile Alliance
glossary [5]; this research did not open a Cockburn primary text for it.

#### Finding B2: Jeffries later argues against writing stories down at all, and against a standard card format

**Work**: Ron Jeffries, "How should user stories be written?", 2008-08-01 [6]; "Three-C's Revisited",
2019-03-26 [7].

**Evidence**: 2008 [6]: asked whether stories should be written, "No, not really." / "A User Story is just
'a thing to do.'" / the card is "just a token for the story, used to mark its progression through the
process" / "Anything at all that reminds everyone of what the story means." The "As a … I want … so that
…" form "reminds us that we need to consider all the users of our product" — a thinking aid, not a
requirement. 2019 [7]: "if you didn't have enough room on the Card for the story, you needed a smaller
card." / "We would definitely not need cards with a consistent format." / C3 "tried a standard format card
in something like 1998 and realized it was a bad idea then." / "the Card was not a requirements document."
/ "There might not even be a Card at all!" Detail goes into "Examples of what the system should do",
ideally "concrete executable Customer Tests".

**Canonicity**: Primary; the originator of the 3 Cs revising his emphasis.

**Contributes**: The strongest support for the developer's stance: the person who named the Card says a
consistent format was tried and rejected in 1998. It also *tests* the stance. Jeffries' answer to
"too much on the card" is to move detail into confirmation examples, not into more card sections. The
`phil` board is asynchronous and written — the conversation happens in the card and its comments — so
the card must carry more than Jeffries' wall card did (interpretation; see Conflicts).

**Caveats**: Jeffries writes for a co-located team with an on-site customer. A board read by strangers and
by a future self has no conversation to fall back on — the reason `groom-issues` rule 1 demands "a purpose
readable without context".

#### Finding B3: Cohn, who popularised the template, calls it optional

**Work**: Mike Cohn, *User Stories Applied* (Addison-Wesley, 2004) — not opened; see Knowledge Gaps.
Cohn, "Advantages of the 'As a user, I want' user story template", Mountain Goat Software (last updated
2026-04-22) [8].

**Evidence** (from [8]): the template "originated with agile coach Rachel Davies at a UK company,
Connextra, in the early 2000s." / "There is no magic formula that must be used to create user stories." /
on the so-that clause, "I don't consider it mandatory because sometimes it just doesn't add any value." /
"When expressing something in the standard user story template doesn't make sense, don't use that
template."

**Canonicity**: Primary for Cohn's own position; the book itself is secondary here because it was not
opened.

**Contributes**: Even the template's chief advocate makes it optional. The `phil` card's omission of
"As a… I want… so that…" departs from a habit, not from a canon.

**Caveats**: Cohn's blog post is periodically re-dated; the claims quoted are his current position, not
necessarily his 2004 text.

#### Finding B4: The Agile Alliance glossary and Fowler restate the token reading — and drift on "Small"

**Work**: Agile Alliance, glossary entry "Three C's" [5]; Martin Fowler, "User Story", bliki, 2013-04-22 [9].

**Evidence**: [5]: the card is "a physical token giving tangible and durable form to what would otherwise
only be an abstraction"; confirmation is "the more formal the better, that the objectives the
conversation revolved around have been reached"; "2001: the Card, Conversation, Confirmation model is
proposed by Ron Jeffries", to distinguish "social" user stories from "documentary" requirements. [9]:
"The essence of a story can be written on a single note card." / "Stories are deliberately not fleshed
out in detail until they are ready to be developed." Fowler glosses Wake's Small as "usually a matter of
person-days".

**Canonicity**: Secondary but independent of each other and of Wake; both cite the primaries.

**Contributes**: Independent confirmation of the token reading and of INVEST's letters. Fowler's
"person-days" against Wake's "at most a few person-weeks" shows "Small" tightening over a decade with no
new evidence (see Conflicts).

**Caveats**: Neither page opens "promise for a conversation"; that phrase stays attributed to Cockburn via
Wake only.

#### Finding B5: The XP lineage — a name and "a paragraph or two", a coupon to talk, and Wake's own later "you don't need a template"

**Work**: Ward Cunningham's wiki, "User Story" page (c2.com, last edited 2006-02-14) [32]; J. B.
Rainsberger, "User Stories: A Ticket for a Conversation", 2012-12-14 (updated 2018-09-11) [31]; Bill Wake,
"What Is a User Story?", XP123, 2021-10-06 [28]; Wikipedia, "User story" [30]; Abel Avram's InfoQ
summary of Rachel Davies' QCon London 2007 talk, 2008-05-21 [33].

**Evidence**: [32]: Kent Beck, "Write down the name of the story and a paragraph or two"; Jeffries, "The
UserStory promises as much subsequent conversation as necessary to fill in the details of what is
wanted", and "we ask the users to split a story if we estimate it at more than about 3 weeks". [31]: the
card as a "reminder to talk about the story, and nothing more", with the title credited to Jeffries. [28]:
the card is "An index card with a summary headline and a sentence or two of explanation"; "a template
helps with the Card, but the Conversation is key"; "you don't need a template to start." [30]: "The XP
team at Connextra in London devised the user story format"; Davies "credits the team as a whole"
(tagged citation needed); listed limitations include poor scaling, difficulty for "geographically
distributed teams", vagueness, and missing non-functional requirements. [33]: in Confirmation "the team
tries to figure out which are the necessary acceptance tests to be written."

**Canonicity**: c2 is the historical primary record of XP practice (Beck and Jeffries signed their
entries). Wake 2021 is primary. Rainsberger is an independent practitioner voice. Wikipedia and the InfoQ
summary are secondary; Davies' own words were not read.

**Contributes**: Beck's original card was "a paragraph or two" — closer to the `phil` card's opening
paragraph than to a one-line template. The inventor of INVEST says no template is needed. Wikipedia's
limitation list names the `phil` board's exact condition — distributed and asynchronous — as the one
where a bare card fails, which explains why the `phil` card carries more than a sticky note did.

**Caveats**: The Connextra attribution rests on Cohn [8] and a Wikipedia line tagged "citation needed";
no Davies primary was opened.

### C. Against the template: what a story must actually carry

#### Finding C1: Patton — the story's context lives in the conversation and the map, not in a flat card

**Work**: Jeff Patton, "The New User Story Backlog is a Map", jpattonassociates.com, 2008-10-08 (updated
2023-04-12) [10]. *User Story Mapping* (O'Reilly, 2014) — **not opened**; O'Reilly returned 403.

**Evidence** (from [10]): a flat ordered backlog is "A bag of context-free mulch." / "Arranging user
stories in the order you'll build them doesn't help me explain to others what the system does." / "I need
that context in order for me to really tell a story about the system." / "Talking through the map with
users and others helps me find things I've missed." The first release is "the smallest possible system you
could build that would give you end to end functionality."

**Canonicity**: Primary for Patton's 2008 argument. The phrase the brief attributes to the book — "stories
are for telling, not writing" — **could not be verified** in any text this research opened. A Goodreads
reader note on the book records "primarily spoken, not written" [secondary, not cited as evidence]. See
Knowledge Gaps.

**Contributes**: Patton's complaint is context loss: a card read in isolation lacks the why. The `phil`
card answers it inside the card — the opening paragraph states "why it matters" — which a map would
otherwise supply. That is a design choice the evidence supports for an asynchronous board.

**Caveats**: Patton's remedy is a spatial map and a live conversation; the `phil` board has neither. His
argument does not show that a written why substitutes for talking (interpretation).

#### Finding C2: Klement's job story replaces the role with the situation; Cohn and academics accept it as an alternative

**Work**: Alan Klement, "Replacing The User Story With The Job Story" (2013) — **original not opened**
(jtbd.info fetch failed). Read through Lucassen et al., "Jobs-to-be-Done Oriented Requirements
Engineering: A Method for Defining Job Stories", REFSQ 2018 [11], and Cohn, "Job Stories Offer a Viable
Alternative to User Stories" (last updated 2024-07-11) [12].

**Evidence**: [11] gives the template as "When <situation>, I want (to) <motivation>, so that (I can)
<expected outcome>" and reports that "Klement argues that user stories' emphasis on roles and their
actions inhibit the discovery of the 'why' due to the many assumptions a personified role implies." It
quotes Klement: "You can write a job story to define a problem and then write user stories as potential
solutions to that job story." It also reports the variety: "The original template for job stories has
been customized by practitioners in different ways" across 131 collected job stories. [12]: "Job stories
originated at Intercom and were best explained by Alan Klement." / "If your product's users do not differ
in significant ways, job stories are likely the better approach."

**Canonicity**: Klement's text is the primary and was not read; the REFSQ paper is peer-reviewed and
quotes him; Cohn's post is an independent practitioner endorsement. Two independent secondaries agree.

**Contributes**: What a story must carry, per Klement: **situation, motivation, expected outcome** — no
role. The `phil` card's opening paragraph ("what is wrong or missing, and why it matters") is a
situation-plus-motivation statement in prose, closer to a job story than to a user story
(interpretation). On a single-developer plugin board where every user is "a developer using the plugin",
Cohn's own test favours dropping the role.

**Caveats**: Job stories are themselves a template; adopting the wording would trade one formula for
another, which the developer's stance rejects.

#### Finding C3: The academic quality framework calls INVEST "highly qualitative" and finds many template defects that a format avoids by not using the template

**Work**: Lucassen, Dalpiaz, van der Werf, Brinkkemper, "Improving agile requirements: the Quality User
Story framework and tool", *Requirements Engineering* 21(3):383–403, 2016, DOI 10.1007/s00766-016-0250-x;
author preprint [13].

**Evidence** (from [13]): "Existing approaches either employ highly qualitative metrics, such as the six
mnemonic heuristics of the INVEST … framework, or generic guidelines for quality in agile RE." The paper
defines 13 criteria in three classes. Syntactic: Well-formed ("includes at least a role and a means"),
Atomic ("expresses a requirement for exactly one feature"), Minimal ("contains nothing more than role,
means and ends"). Semantic: Conceptually sound, Problem-oriented ("only specifies the problem, not the
solution to it"), Unambiguous, Conflict-free. Pragmatic: Full sentence, Estimatable ("does not denote a
coarse-grained requirement that is difficult to plan and prioritize"), Unique, Uniform ("All user stories
in a specification employ the same template"), Independent, Complete. It also notes "There are over 80
syntactic variants of user stories". AQUSA was evaluated on 1,023 stories from 18 organisations.

**Canonicity**: Peer-reviewed, journal version; the most-cited academic treatment of story quality.

**Contributes**: Two things. (1) Academic confirmation that INVEST is a set of *qualitative heuristics*,
not a checkable standard — the property that makes it right to hold advisory. (2) A split between
**checkable-by-tool** criteria (well-formed, minimal, uniform, unique) and **judgement** criteria
(conceptually sound, problem-oriented, complete). The `groom-issues` presence checks are the same kind of
thing as QUS's syntactic class, applied to a different template.

**Caveats**: QUS assumes the Connextra template; "Minimal" would flag every `phil` card, because the card
deliberately carries more than role, means and ends. Its expansion of INVEST's S as "Scalable" is an error
against Wake [1]. Only pages 1–5 of the preprint were read.

### D. Acceptance criteria and done-ness

#### Finding D1: North makes acceptance criteria "an intrinsic part of the story" and the definition of done

**Work**: Dan North, "Introducing BDD", *Better Software*, March 2006, republished 2006-09-20 [14]; "What's
in a Story?", 2007-02-11 [15].

**Evidence**: [14]: "Given some initial context (the givens), When an event occurs, Then ensure some
outcomes." The fragments are "fine-grained enough to be represented directly in code." A story's
behaviour "is simply its acceptance criteria." [15]: acceptance criteria are "a set of criteria by which
we all agree that it is "done"" and "The acceptance criteria are an intrinsic part of the story." / "The
story title should always describe actual behaviour by a user of the system." On size: "There are no hard
and fast rules about how you do this, as long as you break it down into demonstrable chunks"; more than
five or six scenarios suggests a split.

**Canonicity**: Primary; North coined BDD and Given-When-Then.

**Contributes**: Two direct confirmations of the `phil` format. (1) The done-condition belongs *in* the
card, which is what `## Done when` is and what `groom-issues` rule 2 checks for. (2) North's sizing test
is **"demonstrable chunks"** — the same criterion `groom-issues` uses for "oversized" (line 267: "cannot
be demonstrated on its own"). The plugin's departure from INVEST's Small has a named precedent in the
author of Given-When-Then.

**Caveats**: North also says "your story should contain all of the elements described in the template",
including the "As a / I want / So that" narrative — the `phil` card rejects that half of his advice. The
Given-When-Then *form* is not required for a criterion to be checkable; North's own claim is about
behaviour, not syntax.

#### Finding D2: Adzic — examples over abstract criteria, specifications that describe *what*, not test scripts

**Work**: Gojko Adzic, *Specification by Example* (Manning, 2011) — **book not opened**. Read through
Adzic's own words in an InfoQ article on the book [16].

**Evidence** (Adzic, quoted in [16]): "Specification by Example is a set of process patterns that
facilitate change in software products"; the patterns run from deriving scope from goals through
illustrating using examples, refining the specification, automating validation without changing
specifications, validating frequently, to evolving a documentation system. He warns against "using
technical language and scripts to describe how something is tested" and against "the combinatorial
explosion of cases" that makes examples "useless as communication tools."

**Canonicity**: Adzic's own words, through an editorial outlet; the book is the primary and was not read.

**Contributes**: The test for a checkable `## Done when` item: **it names an observable outcome a
stranger can verify, in the domain's language, not a procedure.** "Deriving scope from goals" also
matches the card's opening paragraph — the why precedes the what.

**Caveats**: Adzic's patterns assume automated executable specifications; most `phil` cards change prose,
where "automate validation" means a self-test fixture or a check script, when it means anything.

#### Finding D3: Jeffries and Killick — slice until a story needs a single acceptance test

**Work**: Ron Jeffries, "Story Points Revisited", 2019-05-23 [17].

**Evidence**: "I may have invented story points, and if I did, I'm sorry now." He slices stories until
"each of as high value as possible, but requiring very little time to get done", crediting Neil Killick
with "slice stories down until they just need a single acceptance test." He concludes that "estimation,
be it in points or time, is to be avoided."

**Canonicity**: Primary for Jeffries; Killick's heuristic is reported second-hand (Killick not opened).

**Contributes**: Links Testable to Small without Estimable: the number of acceptance checks is a size
proxy that needs no estimate. A long `## Done when` list is the signal, not a point count
(interpretation; it parallels North's "five or six scenarios" [15]).

**Caveats**: A heuristic, offered by its authors as a trick, not a rule.

### E. Sizing and splitting

#### Finding E1: Elephant Carpaccio — a valid slice is visible, end to end and more valuable than the last

**Work**: Henrik Kniberg and Alistair Cockburn, "Elephant Carpaccio exercise" facilitation guide,
2013-07-11 [18]; Cockburn, "Elephant Carpaccio", alistaircockburn.com (©2022) [19].

**Evidence**: [18]: the exercise practises breaking "stories into really thin vertical slices"; "A slice
is only valid if it has a UI, input & output, and is visibly different from last slice"; no slice may be
just a mockup, a data structure or a test case; teams aim for 15–20 slices where most would build it in
2–3. The debrief warns tiny slices can push rushed work. [19]: "all of the slicing decisions are based on
the business situation, not the technology aspects."

**Canonicity**: Primary (Cockburn invented the exercise; the guide is co-signed).

**Contributes**: Cockburn's validity test is **demonstrability**, not size — "visibly different from last
slice". This is the same test `groom-issues` applies. It also shows the cost side: thin slicing is a skill
to practise, and over-slicing has a quality cost the guide names.

**Caveats**: The exercise targets 2–6-minute slices of a toy app; it trains a habit, and does not set a
card size.

#### Finding E2: Splitting patterns — Lawrence's nine (Humanizing Work) and Cohn's SPIDR are different sources

**Work**: Humanizing Work, "The Humanizing Work Guide to Splitting User Stories" (Richard Lawrence's
flowchart; no byline or date on the page) [20]; Mike Cohn, "Five Simple but Powerful Ways to Split User
Stories" (last updated 2026-08-06) [21].

**Evidence**: [20] lists nine patterns: Workflow Steps, Operations, Business Rule Variations, Variations
in Data, Data Entry Methods, Major Effort, Simple/Complex, Defer Performance, Break Out a Spike. The
flowchart first checks a story against INVEST *except Small*; Small then drives splitting. Valuable is
the usual problem with "unsplittable" stories, which are often tasks or components. Splitting by layer
may satisfy "small" but fails "independent" and "valuable". Size: a top-of-backlog story should fit in a
sprint with roughly 6–10 others. [21]: "The five I ended up with form the acronym SPIDR" — Spike, Path,
Interfaces, Data, Rules; "almost every story can be split with one of five techniques."

**Canonicity**: Primary for each author's own scheme.

**Contributes**: Correct attribution: **the nine patterns are Lawrence's; SPIDR is Cohn's.** Both make
the same point the plugin relies on — a horizontal split satisfies Small while breaking Valuable and
Independent, so size alone is the wrong test.

**Caveats**: Lawrence's "6–10 per sprint" is a ratio against a sprint; the `phil` board has no sprints.
The Humanizing Work page carries no byline; attribution rests on the page crediting "Richard's story
splitting flowchart".

#### Finding E3: #NoEstimates attacks the purpose of Estimable — but its originators do not reject estimates outright

**Work**: Ben Linders, "Q&A with Vasco Duarte on the #NoEstimates Book", InfoQ, 2015-12-07 [22]; Ron
Jeffries, "The #NoEstimates Movement", 2013-04-29 [23]; Jeffries [17].

**Evidence**: Duarte [22]: "Estimates are a poor predictor of project success"; "focus on value, make
decisions based on value, not estimates"; he tracks progress by counting items — "I count the number of
items delivered, and compare that to the number of items in the backlog"; "The earliest recorded tweet
with the #NoEstimates was by Woody Zuill." Jeffries [23]: "Estimation is difficult, perhaps impossible,
and we would be well off if we could avoid it." / "Estimates are often used as a bludgeon to try to get
programmers to work faster." / "estimation, in certain forms, is not always impossible."

**Canonicity**: Duarte is primary for his position via interview; Jeffries is primary. Zuill's own 2012
post was **not opened**.

**Contributes**: Wake's Estimable exists so a customer can "rank and schedule" [1]. Where nobody ranks by
estimate — the `phil` board ranks by position and `phil:rank-issues` records a basis, not points —
Estimable has no consumer. What survives is its *proxy* use: a story you cannot estimate is one you do
not yet understand (Wake [1] ties Estimable to understanding and to Small). That survivor is already
covered by Testable and by `## Open questions` (interpretation).

**Caveats**: #NoEstimates is contested; critics such as Steve McConnell argue estimates serve business
commitments (not opened; see Knowledge Gaps). Even its proponents say "not always impossible".

### F. Definition of Ready

#### Finding F1: The Scrum Guide has no Definition of Ready; its only readiness test is "can be Done within one Sprint"

**Work**: Ken Schwaber and Jeff Sutherland, *The Scrum Guide*, November 2020 [24]; Scrum.org forum
thread "What is the purpose of 'Definition of Ready'?", January 2018 [25].

**Evidence**: [24]: "Product Backlog items that can be Done by the Scrum Team within one Sprint are deemed
ready for selection"; refinement "is the act of breaking down and further defining Product Backlog
items". The phrase "Definition of Ready" does not occur; "Definition of Done" does: "Work cannot be
considered part of an Increment unless it meets the Definition of Done." [25]: "Definition of Ready (DoR)
is not a part of the Scrum Guide" (Timothy Baffa); "teams should beware of making exhaustive checklists as
DoRs because that may lead to a waterfall-esque situation" (Julian Bayer).

**Canonicity**: The Guide is the primary definition of Scrum. The forum is community opinion (medium
weight), cited only for practitioner sentiment.

**Contributes**: The canonical framework defines Done formally and Ready only as "doable in one go". The
`phil` standard does the same: `## Done when` is required; no readiness checklist exists.

**Caveats**: The Guide's silence is not a prohibition.

#### Finding F2: Cohn warns that a Definition of Ready becomes a stage gate, and asks for guidelines, not rules

**Work**: Mike Cohn, "Definition of Ready: What It Is and Why It's Dangerous", Mountain Goat Software
(last updated 2023-06-28) [26].

**Evidence**: "the definition of ready becomes a huge step towards a sequential, stage-gate approach";
this "will prevent the team from being agile"; stage-gate is "another way of describing a waterfall
process." Dangerous rule: "Each story must be accompanied by a detailed mock up of all new screens before
we start work." His remedy: "Favor guidelines rather than rules on your Definition of Ready."

**Canonicity**: Primary for Cohn; independent of the Scrum Guide and of the forum.

**Contributes**: The clearest statement of the developer's stance from a mainstream author: **readiness
heuristics as guidelines, never as a gate.** A `rules/stories.md` that turned INVEST into a pass/fail
precondition would be exactly the Definition of Ready Cohn warns against.

**Caveats**: Cohn still endorses a DoR as guidelines; he objects to its rigid form, not its existence. The
brief named Jeffries as a DoR critic; this research found no Jeffries text on DoR (see Knowledge Gaps).

## Applying it to the current card format

Everything in this section is **interpretation** of the findings above, measured against the four-part
card (opening paragraph · `## What it does` / `## What it holds` · `## Done when` · `## Open questions`) and
against `skills/groom-issues/SKILL.md` lines 56–125 and 260–280.

**Columns.** *Carried*: **explicit** (a section exists for it), **implicit** (it falls out of a section
written for something else), or **no**. *Skill can check*: **presence** (a section or field exists — the
kind of check `groom-issues` already makes, rules 1, 2 and 5), **advisory** (judgement a skill may raise
as a question, never as a defect), or **n/a**.

### INVEST (Wake [1])

| Letter | Wake's meaning | Where the card carries it | Carried | Skill can check |
|---|---|---|---|---|
| **I**ndependent | No concept overlap; build in any order | `## Chain` when blocked (rule 5); the duplicates scan covers overlap | implicit | **presence** of a chain line when an edge exists — already checked. Whether the card *should* be independent: advisory. QUS notes "no dependency at all … is practically impossible" [13] |
| **N**egotiable | "captures the essence, not the details" | `## Open questions` names what is undecided | explicit | **advisory**. An empty `## Open questions` may mean "settled", so absence is not a defect. Raise only when `## What it does` fixes implementation detail the opening paragraph does not need |
| **V**aluable | Valuable to the customer; slice vertically | Opening paragraph — "why it matters", often a measured wound | explicit | **presence** of a purpose (rule 1). Whether the why is real value: advisory |
| **E**stimable | Enough to "rank and schedule" | Nothing; the board ranks by position, not estimate | no | **n/a**. Its purpose has no consumer here (Finding E3). Its proxy — "do we understand it?" — is carried by `## Open questions` and Testable |
| **S**mall | "at most a few person-weeks" | Replaced by *demonstrable on its own* (lines 267–274) | no (replaced) | **advisory** only. See the assessment below |
| **T**estable | "I could write a test for it" | `## Done when` | explicit | **presence** of a done-condition (rule 2). Whether each item is an observable outcome: advisory |

### SMART — Wake's task letters [1], with Doran's [2] where they differ

| Letter | Meaning | Where the card carries it | Carried | Skill can check |
|---|---|---|---|---|
| **S**pecific | Wake: "everyone can understand what's involved"; Doran: "target a specific area" | Opening paragraph plus `## What it does` | implicit | **advisory** — "readable without context" is rule 1's presence test; clarity itself is judgement, and judging a human's prose is excluded by lines 117–126 |
| **M**easurable | Wake: "can we mark it as done?"; Doran: "quantify or at least suggest an indicator of progress" | `## Done when` | explicit | **presence** (rule 2). Doran warns forced quantification can "lose the benefit of a more abstract objective" — so never demand a number |
| **A**chievable / **A**ssignable | Wake: owner "should expect to be able to achieve"; Doran: "specify who will do it" | Doran's A is the forge's assignee, set by `/phil:start`, not the body. Wake's A is partly `## Open questions` | implicit | Assignee: a forge field, out of a body standard's scope. Achievable: **advisory** |
| **R**elevant | Wake: "contributing to the story at hand" | For a card, its link upward — a parent, a `## Chain`, a wave label; for a checklist item, its tie to the opening paragraph | implicit | **advisory** |
| **T**ime-boxed / Time-related | Wake: "limited to a specific duration"; Doran: "specify when" | Nothing; the board carries no dates | no | **n/a**. Wake applies SMART to *tasks*, not stories; leaving T off a story card follows Wake |

### The 3 Cs (Jeffries [4], [6], [7])

| C | Meaning | Where the card carries it | Carried | Skill can check |
|---|---|---|---|---|
| **Card** | "a token representing the requirement" | The issue itself; its opening paragraph is the reminder | explicit | **presence** (rule 1) |
| **Conversation** | "an *exchange* of thoughts, opinions, and feelings" | Issue comments, `## Open questions`, `/phil:groom-ask` elicitation | implicit | **n/a** — a conversation is not a body property |
| **Confirmation** | "This component is the acceptance test" | `## Done when` | explicit | **presence** (rule 2) |

### Assessment of the "oversized means not demonstrable, never large" departure

- **Supported.** Cockburn's validity test is "visibly different from last slice" [18]; North sizes by
  "demonstrable chunks" [15]; Lawrence and Wake both treat a horizontal split as *failing* Valuable and
  Independent even though it passes Small [1], [20]. All three put demonstrability before size, so a
  size-only check would propose splits that break V and I. The plugin's reason — a size test would flag
  every correct one-feature card on every run (lines 269–272) — follows from the same logic.
- **Not fully supported.** No source says a large demonstrable card is fine. Every source that names a
  size wants it smaller over time: person-weeks (Wake 2003 [1]) → person-days (Fowler 2013 [9]) → "a day or
  less" (Jeffries 2019 [17]). The canonical reason for Small is feedback and risk, which demonstrability
  alone does not deliver. The sources would accept the departure *as the defect test* and still expect an
  advisory nudge toward thinner slices.
- **A size proxy that needs no estimate exists**: the count of `## Done when` items. North suggests a
  split past "five or six" scenarios [15]; Killick, via Jeffries, slices "until they just need a single
  acceptance test" [17]. A skill could raise a long done-list as a *question*, never as a defect —
  consistent with the "held lightly" stance and with lines 269–272's refusal to re-propose declined
  splits.

### Testing the developer's stance

- **Confirmed by the sources.** INVEST's author built it by clustering intuitions [1]. SMART's author
  wrote that "every objective written" need not meet "all five criteria" and called it "a guideline" [2].
  The academic quality framework calls INVEST "highly qualitative" [13]. Jeffries rejected a standard
  card format in 1998 [7]; Cohn says "no magic formula" [8] and asks for DoR "guidelines rather than
  rules" [26]; Wake says "you don't need a template" [28]. "Held lightly, recorded" is the canonical
  position, not a departure from it.
- **Challenged by the sources.** "Originally sticky notes" is true of the card, but the sticky note
  worked because the conversation and confirmation lived elsewhere — in a room and in acceptance tests
  [4], [7]. Wikipedia's limitation list names distributed teams as the weak case [30]. A forge board read
  asynchronously by a stranger has no room, so the `phil` card *must* carry the why and the confirmation
  in writing. It does — the format is closer to Beck's "a paragraph or two" [32] plus North's in-card
  acceptance criteria [15] than to a sticky note. "Simple" holds; "sticky-note simple" would not.
- **One tension the format carries.** `## What it does` lists the change. Negotiable [1] and QUS's
  Problem-oriented criterion [13] both warn against a card that specifies the solution. The opening
  paragraph states the problem first, which answers most of it; a skill could note, advisorily, a card
  whose `## What it does` fixes detail the problem does not require.
- **Unfalsifiable from the literature.** "Just the right level of formal" is not tested by any source
  found: no study compares card formats by outcome (see Knowledge Gaps). The claim rests on the board's
  own experience, which is admissible evidence but not this document's to grade.

### What a `rules/stories.md` could take from this (interpretation)

1. Record INVEST (for stories) and SMART (for tasks) with their authors' own words and their authors'
   own disclaimers [1], [2].
2. Keep presence checks to the three the skill already makes — purpose, done-condition, chain — because
   only those correspond to letters a tool can check without judging prose.
3. Everything else is advisory, phrased as a question to the author, and never re-raised once declined.
4. Do not adopt Estimable or Time-bound for cards; say why, citing Wake's purpose for each.
5. Keep "demonstrable on its own" as the oversized defect test; add the done-list length as an advisory
   size prompt.

## Conflicts between sources

### Conflict 1: How small is Small?
**Position A**: "at most a few person-weeks" — Wake 2003 [1]; split past "about 3 weeks" — Jeffries on c2
[32]. **Position B**: "usually a matter of person-days" — Fowler 2013 [9]; "a day or less" — Jeffries
2019 [17]; "fit within an iteration" — Agile Alliance [27]; 6–10 per sprint — Lawrence [20].
**Position C**: no size, "demonstrable chunks" — North [15]; "visibly different from last slice" —
Cockburn/Kniberg [18].
**Assessment**: Wake is authoritative for what INVEST *meant*; the trend since is smaller, with no new
evidence offered for any number. Position C is the only one that does not depend on a sprint, which the
`phil` board lacks.

### Conflict 2: Should cards share a template?
**Position A**: "your story should contain all of the elements described in the template" — North [15];
"All user stories in a specification employ the same template" (Uniform) — Lucassen et al. [13].
**Position B**: "We would definitely not need cards with a consistent format" — Jeffries [7]; "no magic
formula" — Cohn [8]; "you don't need a template to start" — Wake [28].
**Assessment**: Position B comes from the originators of INVEST, the 3 Cs and the template's chief
popularizer. Position A is right that a *board* benefits from uniformity for tooling — which the `phil`
format supplies through fixed section headings, not a sentence template.

### Conflict 3: How much belongs on the card?
**A**: "nothing more than role, means and ends" — QUS [13]; "reminder to talk … and nothing more" —
Rainsberger [31]; "There might not even be a Card at all!" — Jeffries [7]. **B**: "a paragraph or two" —
Beck [32]; acceptance criteria "an intrinsic part of the story" — North [15]. **Assessment**: A assumes a
live conversation; an asynchronous board needs B, and the `phil` card follows it.

### Conflict 4: What SMART stands for, and what it applies to
**A**: Doran — objectives; *Assignable*, *Realistic*, *Time-related* [2]. **B**: Wake — tasks;
*Achievable*, *Relevant*, *Time-boxed* [1]. **C**: popular usage — goals and acceptance criteria, many
variants [3]. **Assessment**: Doran is the origin; Wake is the origin in agile and confines SMART to tasks.
No primary source found applies it to stories or acceptance criteria.

### Conflict 5: Is Estimable a quality?
**A**: Wake [1], the Agile Alliance [27] and Mitchell [25] keep an estimate as a readiness signal. **B**:
"estimation, be it in points or time, is to be avoided" — Jeffries [17]; "Estimates are a poor predictor
of project success" — Duarte [22]. **Assessment**: Unresolved in the field; on a board that never ranks by
estimate, B costs nothing.

## Knowledge Gaps

Anything not opened is a gap; each is stated plainly.

1. **Cohn, *User Stories Applied* (2004)** — not opened. Cohn's 2004 treatment of INVEST is known only
   through the Agile Alliance glossary [27] and his current blog posts [8], [12], [21], [26].
2. **Patton, *User Story Mapping* (2014)** — not opened (O'Reilly returned 403). The phrase "stories are
   for telling, not writing" was **not verified** in any opened text. Patton's position is cited from his
   2008 article [10] only.
3. **Klement, "Replacing The User Story With The Job Story" (2013)** — not opened (jtbd.info fetch
   failed). His argument is cited through Lucassen et al. [11] and Cohn [12].
4. **Adzic, *Specification by Example* (2011)** — not opened; cited through Adzic's words in InfoQ [16].
5. **Swann et al. (2023)** — abstract only [29]; full text not opened.
6. **Zuill's December 2012 #NoEstimates post** and **critics of #NoEstimates** (e.g. Steve McConnell,
   Glen Alleman) — not opened. The #NoEstimates finding is therefore one-sided.
7. **Jeffries on Definition of Ready** — searched for and not found. The DoR critique rests on Cohn [26],
   the Scrum Guide's silence [24] and a forum thread [25]. No Scrum.org *blog* article on DoR as a stage
   gate was opened.
8. **Cockburn's "promise for a conversation"** — known only through Wake [1]; no Cockburn primary found.
9. **Rachel Davies' own account of the Connextra template** — not found; attribution rests on Cohn [8] and
   a Wikipedia line tagged "citation needed" [30].
10. **Neil Killick's "single acceptance test" heuristic** — known only through Jeffries [17].
11. **SMART applied to acceptance criteria** — the brief asks how SMART is applied to acceptance criteria.
    No primary or peer-reviewed source applying it there was found; only Wake's task usage [1] and Doran's
    objective usage [2] were verified.
12. **Outcome evidence for card formats** — no study found that compares story or card formats by delivery
    outcome. QUS [13] measures conformance to a template, not results. Lucassen et al., "The Use and
    Effectiveness of User Stories in Practice" (REFSQ 2016), was not opened and may bear on this.
13. **Beck, *Extreme Programming Explained* (1999)** — not opened; Beck is cited only through his signed
    c2 entry [32].

## References

All web sources accessed 2026-11-09.

1. Wake, B. "INVEST in Good Stories, and SMART Tasks". XP123. 2003-08-17 (postscript 2011-02-16). https://xp123.com/articles/invest-in-good-stories-and-smart-tasks/
2. Doran, G. T. "There's a S.M.A.R.T. way to write management's goals and objectives". *Management Review* 70(11):35–36. November 1981. Scan read at https://www.decisionskills.com/uploads/5/1/6/0/5160560/doran_1981_s.m.a.r.t-way-management-review.pdf
3. Wikipedia. "SMART criteria". https://en.wikipedia.org/wiki/SMART_criteria
4. Jeffries, R. "Essential XP: Card, Conversation, Confirmation". ronjeffries.com. 2001-08-30. https://ronjeffries.com/xprog/articles/expcardconversationconfirmation/
5. Agile Alliance. "Three C's" (glossary). https://agilealliance.org/glossary/three-cs
6. Jeffries, R. "How should user stories be written?". ronjeffries.com. 2008-08-01. https://ronjeffries.com/xprog/blog/how-should-user-stories-be-written/
7. Jeffries, R. "Three-C's Revisited". ronjeffries.com. 2019-03-26. https://ronjeffries.com/articles/019-01ff/3cs-revisited/
8. Cohn, M. "Advantages of the 'As a user, I want' user story template". Mountain Goat Software. Last updated 2026-04-22. https://www.mountaingoatsoftware.com/blog/advantages-of-the-as-a-user-i-want-user-story-template
9. Fowler, M. "User Story". martinfowler.com bliki. 2013-04-22. https://martinfowler.com/bliki/UserStory.html
10. Patton, J. "The New User Story Backlog is a Map". Jeff Patton & Associates. 2008-10-08 (updated 2023-04-12). https://jpattonassociates.com/the-new-backlog/
11. Lucassen, G., van de Keuken, M., Dalpiaz, F., Brinkkemper, S., Sloof, G. W., Schlingmann, J. "Jobs-to-be-Done Oriented Requirements Engineering: A Method for Defining Job Stories". REFSQ 2018. Preprint: https://webspace.science.uu.nl/~dalpi001/papers/luca-keuk-dalp-brin-18-refsq.pdf
12. Cohn, M. "Job Stories Offer a Viable Alternative to User Stories". Mountain Goat Software. Last updated 2024-07-11. https://www.mountaingoatsoftware.com/blog/job-stories-offer-a-viable-alternative-to-user-stories
13. Lucassen, G., Dalpiaz, F., van der Werf, J. M. E. M., Brinkkemper, S. "Improving agile requirements: the Quality User Story framework and tool". *Requirements Engineering* 21(3):383–403. 2016. DOI 10.1007/s00766-016-0250-x. Preprint (pp. 1–5 read): https://webspace.science.uu.nl/~dalpi001/papers/luca-dalp-werf-brin-16-rej.pdf
14. North, D. "Introducing BDD". *Better Software*, March 2006; dannorth.net 2006-09-20. https://dannorth.net/blog/introducing-bdd/
15. North, D. "What's in a Story?". dannorth.net. 2007-02-11. https://dannorth.net/blog/whats-in-a-story/
16. InfoQ. "Specification by Example" (article on Adzic's book, quoting Adzic). https://www.infoq.com/articles/specification-by-example-book
17. Jeffries, R. "Story Points Revisited". ronjeffries.com. 2019-05-23. https://ronjeffries.com/articles/019-01ff/story-points/Index.html
18. Kniberg, H., Cockburn, A. "Elephant Carpaccio exercise" (facilitation guide). 2013-07-11. https://docs.google.com/document/d/1TCuuu-8Mm14oxsOnlk8DqfZAA1cvtYu9WGv67Yj_sSk/pub
19. Cockburn, A. "Elephant Carpaccio". alistaircockburn.com. ©2022. https://alistaircockburn.com/Elephant-Carpaccio
20. Humanizing Work (Lawrence, R.). "The Humanizing Work Guide to Splitting User Stories". Undated. https://www.humanizingwork.com/the-humanizing-work-guide-to-splitting-user-stories/
21. Cohn, M. "Five Simple but Powerful Ways to Split User Stories" (SPIDR). Mountain Goat Software. Last updated 2026-08-06. https://www.mountaingoatsoftware.com/blog/five-simple-but-powerful-ways-to-split-user-stories
22. Linders, B. "Q&A with Vasco Duarte on the #NoEstimates Book". InfoQ. 2015-12-07. https://www.infoq.com/articles/book-review-noestimates
23. Jeffries, R. "The #NoEstimates Movement". ronjeffries.com. 2013-04-29. https://ronjeffries.com/xprog/articles/the-noestimates-movement/
24. Schwaber, K., Sutherland, J. *The Scrum Guide*. November 2020. https://scrumguides.org/scrum-guide.html
25. Scrum.org Forum. "What is the purpose of 'Definition of Ready'?". January 2018. https://www.scrum.org/node/14779
26. Cohn, M. "Definition of Ready: What It Is and Why It's Dangerous". Mountain Goat Software. Last updated 2023-06-28. https://www.mountaingoatsoftware.com/blog/the-dangers-of-a-definition-of-ready
27. Agile Alliance. "INVEST" (glossary). https://agilealliance.org/glossary/invest/
28. Wake, B. "What Is a User Story?". XP123. 2021-10-06. https://xp123.com/?p=5453
29. Swann, C., Jackman, P. C., Lawrence, A., et al. "The (over)use of SMART goals for physical activity promotion: A narrative review and critique". *Health Psychology Review* 17(2):211–226. 2023. DOI 10.1080/17437199.2021.2023608. Abstract read at https://researchportal.scu.edu.au/esploro/outputs/journalArticle/The-overuse-of-SMART-goals-for/991012994285102368
30. Wikipedia. "User story". https://en.wikipedia.org/wiki/User_story
31. Rainsberger, J. B. "User Stories: A Ticket for a Conversation". 2012-12-14 (updated 2018-09-11). https://legacy-blog.jbrains.ca/permalink/user-stories-a-ticket-for-a-conversation
32. Cunningham & Cunningham wiki. "User Story" (entries signed by Kent Beck and Ron Jeffries). Last edited 2006-02-14. https://c2.com/xp/UserStory.html
33. Avram, A. "Agile Project Lifecycle" (summary of Rachel Davies, QCon London 2007). InfoQ. 2008-05-21. https://www.infoq.com/news/2008/05/Agile-Project-Lifecycle
