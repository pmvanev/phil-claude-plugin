# Research: UX Design Best Practices and the Elements of Good UX Design

**Date**: 2026-07-02 | **Researcher**: nw-researcher (Nova) | **Confidence**: High | **Sources**: 17

> Framework-agnostic, application-agnostic. Intended to be distilled into a reusable Claude Code
> "rule/skill" that flags UX violations and names preferred forms during UI code review.
> Each finding uses: **Principle** / **Evidence** / **UX implication (what a reviewer flags)** / **Caveats**.

## Executive Summary
Good UX rests on a small set of durable, vendor-neutral principles that predate and outlast any
framework. The most authoritative and stable spine is **Nielsen's 10 usability heuristics** (unchanged
since 1994), which most other findings here trace back to: visibility of system status, match to the
real world, user control/freedom (undo), consistency, error prevention, recognition over recall,
flexibility, minimalism, error recovery, and help. Layered on top are well-attested **interaction and
psychology laws** (Hick, Fitts, Miller, Jakob, Tesler, Postel, Doherty, Peak-End, Serial Position,
Goal-Gradient) that give quantitative or mechanistic backing to specific design moves, and the
**W3C/WCAG POUR** accessibility standard, which this research treats as a baseline of usability rather
than an add-on (contrast >= 4.5:1, full keyboard operability, visible focus, target size >= 24 CSS px,
text alternatives, never color-alone).

Across sources the guidance converges strongly. Concrete, flaggable rules recur: keep users informed
with timely feedback (0.1s/1s/10s limits, <400ms Doherty target); design every UI state (empty,
loading, error, partial), not just the happy path; prefer undo over confirmation for reversible
destructive actions; use persistent labels (never placeholder-as-label); validate inline after a field
loses focus with specific, blame-free, recoverable error messages; use radios for mutually-exclusive
choice (with a default) and checkboxes for independent multi-select; apply progressive disclosure but
never beyond two levels; convey grouping through Gestalt proximity/similarity/common-region; and
front-load scannable content with descriptive headings.

Two notable disagreements surfaced. First, **Postel's Law** ("be liberal in what you accept") is sound
UX advice for *input formatting* but is now considered risky in *protocol/security* code — the derived
rule must scope it to forgiving input plus internal normalization, not lax validation. Second,
**Miller's "7 +/- 2"** is widely misused to cap menu/nav item counts; the authoritative reading is that
it describes short-term-memory span, so the durable takeaway is *chunking and reducing recall load*,
not an item-count limit. The rule should encode chunking and explicitly avoid a "max 7 items" cap.
A minor caveat worth carrying forward: the popular "5 UI states" taxonomy is practitioner-originated
(Hurff) rather than a standards-body artifact, though each state maps cleanly onto Nielsen heuristics
#1 and #9. Overall confidence is High: 13 of 17 sources are high-reputation (NN/g, W3C, WebAIM,
GOV.UK), and every major claim is anchored to at least one authoritative source with corroboration.

## Research Methodology
**Search Strategy**: Direct retrieval of canonical pages from Nielsen Norman Group (nngroup.com),
Laws of UX (lawsofux.com), W3C/WAI (WCAG), GOV.UK, and the U.S. Web Design System, plus
Interaction Design Foundation. Prioritized primary/authoritative sources over secondary commentary.
**Source Selection**: Types: official standards (W3C), industry-authoritative (NN/g), government
design systems (GOV.UK, USWDS), reference (Laws of UX / IxDF). Reputation: high / medium-high minimum.
Verification: cross-reference each law/heuristic across 2+ independent origins (original author +
authoritative summary).
**Quality Standards**: Target 2-3 sources/claim, >=1 authoritative. Most claims here trace to a
primary author (Nielsen, Fitts, Hick, Miller, etc.) plus an authoritative summariser.

---

## Findings

## 1. Foundational Usability Heuristics — Nielsen's 10

**Principle**: Ten general "rules of thumb" for interaction design, derived by Jakob Nielsen and
Rolf Molich (1990) and refined by Nielsen (1994) from a factor analysis of 249 usability problems.
**Evidence**: "the 10 heuristics themselves have remained relevant and unchanged since 1994."
— NN/g, *10 Usability Heuristics for User Interface Design*, published 1994-04-24, updated 2024-01-30.
https://www.nngroup.com/articles/ten-usability-heuristics/ — Accessed 2026-07-02.
**Confidence**: High (authoritative primary source; the origin of the heuristics themselves).

| # | Heuristic | What it means in practice |
|---|-----------|---------------------------|
| 1 | **Visibility of system status** | Keep users informed with timely, appropriate feedback about what is happening. |
| 2 | **Match between system and the real world** | Speak users' language; follow real-world conventions; present info in a natural, logical order. |
| 3 | **User control and freedom** | Provide clearly marked "emergency exits"; support undo and redo. |
| 4 | **Consistency and standards** | Follow platform/industry conventions; same words and actions mean the same thing (Jakob's Law). |
| 5 | **Error prevention** | Eliminate error-prone conditions or confirm before consequential actions — better than good error messages. |
| 6 | **Recognition rather than recall** | Make elements, actions, and options visible; don't force users to remember info across screens. |
| 7 | **Flexibility and efficiency of use** | Accelerators (shortcuts, customization) serve experts without hindering novices. |
| 8 | **Aesthetic and minimalist design** | Remove irrelevant/rarely-needed content; every extra unit competes with the relevant units. |
| 9 | **Help users recognize, diagnose, and recover from errors** | Plain-language errors that state the problem and suggest a solution. |
| 10 | **Help and documentation** | Ideally none needed, but provide searchable, task-focused, in-context help. |

**UX implication (reviewer flags)**: Any UI change that hides system state, breaks platform
convention, removes an escape/undo, adds a non-essential element, or produces a cryptic error
violates a specific numbered heuristic — cite the number.
**Caveats**: Heuristics are discount-evaluation aids, not guarantees; they overlap (e.g., #2, #4, #6
reinforce each other) and require judgment, not mechanical application.

---

## 2. Interaction & Psychology Laws

Primary reference for the modern UX framing is **Laws of UX** (Jon Yablonski), which summarizes each
law with attribution to its original researcher. https://lawsofux.com/ — Accessed 2026-07-02.
Cross-referenced with the original researchers named below.

**Principle — Hick's Law**: "The time it takes to make a decision increases with the number and
complexity of choices." (Hick 1952; Hyman 1953.)
**UX implication**: Reduce/segment the number of simultaneous choices; use progressive disclosure,
categorization, and sensible defaults; highlight recommended options.
**Caveats**: Does not apply when speed is not the goal (e.g., deliberately slowing users for safety),
or when grouping/filtering already offloads the decision; over-simplification can hide needed options.

**Principle — Fitts's Law**: "The time to acquire a target is a function of the distance to and size
of the target." (Fitts 1954.)
**UX implication**: Make frequent/important targets larger and closer to the pointer; exploit screen
edges/corners (infinite depth); avoid tiny, crowded controls; keep related action buttons near the
work. Ties directly to WCAG target-size guidance.
**Caveats**: Touch vs. mouse vs. keyboard differ; on touch, minimum size dominates over distance.

**Principle — Miller's Law**: "The average person can only keep 7 (± 2) items in their working
memory." (Miller 1956.)
**UX implication**: Chunk information (e.g., grouped digits); don't rely on users holding many items
in mind across steps; favor recognition over recall.
**Caveats**: Often over-applied — Miller's number is about memory span, NOT a hard limit on menu/nav
item counts. Do not cite it to justify "max 7 nav items." Chunking is the durable takeaway.

**Principle — Jakob's Law**: "Users spend most of their time on other sites... users prefer your site
to work the same way as all the other sites they already know." (Jakob Nielsen.)
**UX implication**: Meet convention. Prefer standard patterns/placements (nav, search, cart, form
controls) over novel ones; deviate only with strong justification.
**Caveats**: Convention can entrench mediocre patterns; innovation is warranted when a standard is
genuinely poor — but change should be tested, not assumed.

**Principle — Tesler's Law (Conservation of Complexity)**: "for any system there is a certain amount
of complexity which cannot be reduced." (Larry Tesler.)
**UX implication**: Inherent complexity must live somewhere — prefer the system/designer absorbing it
over pushing it onto users (e.g., smart defaults, auto-format, inference) rather than exposing every
edge case as a user decision.
**Caveats**: Don't hide complexity users legitimately need to control; balance simplicity vs. power.

**Principle — Postel's Law (Robustness Principle)**: "Be liberal in what you accept, and conservative
in what you send." (Jon Postel, RFC 761/793.)
**UX implication**: Accept forgiving input formats (phone numbers with/without spaces, dates in
several forms, trimming whitespace) and normalize internally; present clean, consistent output.
**Caveats**: In UX it's about input tolerance; in protocol/security contexts, over-liberal parsing is
now considered risky (interoperability/security tension). Scope to input forgiveness, not lax validation.

**Principle — Doherty Threshold**: "Productivity soars when a computer and its users interact at a
pace (<400ms) that ensures that neither has to wait on the other." (Doherty & Thadhani, IBM, 1982.)
**UX implication**: Target sub-400ms system response for interactive actions; when impossible, use
perceived-performance techniques (optimistic UI, skeletons, progress).
**Caveats**: Complements Nielsen's 0.1/1/10s limits; not every operation can hit 400ms — feedback
substitutes for speed.

**Principle — Peak-End Rule**: "People judge an experience largely based on how they felt at its peak
and at its end, rather than the... average of every moment." (Kahneman.)
**UX implication**: Invest in emotional peaks (delightful success moments) and strong endings
(confirmation, thank-you, clean completion); handle error peaks gracefully.
**Caveats**: Doesn't excuse a poor middle; measurement-driven, easy to over-engineer "delight."

**Principle — Serial Position Effect**: "Users have a propensity to best remember the first and last
items in a series." (Ebbinghaus; primacy + recency.)
**UX implication**: Place the most important nav/menu/list items first or last; least important in the
middle.
**Caveats**: Interacts with scanning patterns and default selection; not a rule for every list.

**Principle — Goal-Gradient Effect**: "The tendency to approach a goal increases with proximity to the
goal." (Hull 1932; Kivetz et al. 2006.)
**UX implication**: Show progress (progress bars, step "3 of 4", completeness meters); artificial
early progress (pre-filled step) can boost completion.
**Caveats**: Must be honest; fake progress erodes trust; only helps when there is a clear goal.

---

## 3. Managing Complexity

**Principle — Progressive disclosure**: Show only the few most important options initially; reveal
specialized options on request. Improves learnability, efficiency, and error rate.
**Evidence**: "Initially, show users only a few of the most important options. Offer a larger set of
specialized options upon request." AND the two-level limit: "designs that go beyond 2 disclosure
levels typically have low usability because users often get lost... If you have so many features that
you need 3 or more levels, consider simplifying your design."
— Jakob Nielsen, NN/g, 2006-12-03. https://www.nngroup.com/articles/progressive-disclosure/ — Accessed 2026-07-02.
**Confidence**: High (authoritative primary).
**UX implication (reviewer flags)**: Advanced/rare options should be behind a disclosure (accordion,
"Advanced settings", secondary screen), not on the primary surface. Flag disclosure nesting deeper
than 2 levels. Distinguish progressive disclosure (reveal in place) from staged disclosure (wizards,
for divisible independent steps).
**Caveats**: Hiding truly primary options harms discoverability; staged disclosure is wrong when steps
are interdependent.

**Principle — Recognition over recall** (heuristic #6): Minimize memory load by making information
visible/retrievable rather than requiring users to recall it.
**Evidence**: NN/g heuristic #6 (source above). Grounded in the recognition-vs-recall memory
distinction from cognitive psychology.
**UX implication**: Prefer selectable lists/autocomplete over free recall; keep instructions visible
(don't bury them in disappearing placeholders); show recently used items.
**Caveats**: Recognition UIs can get cluttered; balance with minimalism.

**Principle — Aesthetic-Usability Effect**: Users perceive attractive designs as more usable, and are
more tolerant of minor usability problems.
**Evidence**: "Users often perceive aesthetically pleasing design as design that's more usable."
— Laws of UX (attributing Kurosu & Kashimura 1995). https://lawsofux.com/ — Accessed 2026-07-02.
**UX implication**: Visual polish measurably affects perceived usability and trust — but is a
double-edged sword: it can mask real usability problems in testing.
**Caveats**: Do NOT let aesthetics substitute for usability; this rule's remit is usability, so use
this only to justify not shipping visibly broken/unfinished UI, not to prioritize decoration.

**Principle — Sensible defaults & minimal-by-default**: Pre-select the safest/most common option;
start minimal and let complexity be requested (ties to Hick's, Tesler's, heuristic #8).
**Evidence**: Heuristic #8 "Aesthetic and minimalist design" (NN/g, source above); reinforced by
Hick's Law and progressive-disclosure guidance above.
**UX implication (reviewer flags)**: New settings/forms should ship with a working default; avoid
forcing a choice where a good default exists; default to the reversible/least-destructive option.
**Caveats**: Defaults carry ethical weight (they steer behavior); a default must be genuinely in the
user's interest, not a dark pattern.

---

## 4. Information Architecture & Navigation

**Principle — Match users' mental models / findability**: Structure and label content around how users
think, not the org chart or database schema (heuristic #2, "match the real world").
**Evidence**: Heuristic #2 (NN/g). Reinforced by GOV.UK Principle #1 "Start with user needs" and #7
"Understand context." https://www.gov.uk/guidance/government-design-principles — Accessed 2026-07-02.
**UX implication (reviewer flags)**: Navigation labels should use user vocabulary, not internal
jargon; group related items (Gestalt proximity/common region); support both search and browse.
**Caveats**: Mental models vary across audiences; validate with research, don't assume.

**Principle — Grouping via common region/proximity**: Related items are perceived as a unit when
placed near each other or within a shared container.
**Evidence**: Gestalt principles (see §5). — Interaction Design Foundation.
https://ixdf.org/literature/topics/gestalt-principles — Accessed 2026-07-02.
**UX implication**: Use spacing and containers to signal grouping; don't rely on order alone.

**Principle — Wayfinding: breadcrumbs & clear location**: Users need to know where they are, where
they can go, and how to get back (heuristic #1 visibility; #3 control/freedom).
**Evidence**: Heuristics #1 and #3 (NN/g). Serial-position + goal-gradient inform step indicators.
**UX implication (reviewer flags)**: Multi-level hierarchies should expose current location
(breadcrumbs, active nav state), a back/up path, and never trap the user.
**Caveats**: Breadcrumbs suit hierarchical sites; add little value on flat structures.

**Principle — Search vs. browse are complementary**: Provide browse (categorized navigation) for
exploration and search for known-item finding; many users go straight to search.
**Evidence**: Recognition-over-recall (#6) favors browse; search serves recall-driven, known-item
tasks. Cross-referenced with Hick's Law (browse segments choices).
**UX implication**: For content-heavy UIs, offer search; make it prominent and forgiving (Postel's Law).
**Caveats**: Small UIs may not need search; poor search is worse than none.

---

## 5. Visual Hierarchy & Perception (in service of usability)

**Principle — Gestalt principles of grouping**: Human perception organizes visual elements by
proximity, similarity, common region, closure, continuity, and figure-ground.
**Evidence** (each, verbatim from IxDF):
- **Proximity**: "We group closer-together elements, separating them from those farther apart."
- **Similarity**: "When items... share superficial characteristics, we perceive them as grouped."
- **Common region**: "We perceive elements that are in the same closed region as one group."
- **Closure**: "We prefer complete shapes, so we automatically fill the gaps..."
- **Continuity**: "We group elements that seem to follow a continuous path..."
- **Figure-ground**: foreground is perceived first against the background.
— Interaction Design Foundation. https://ixdf.org/literature/topics/gestalt-principles — Accessed 2026-07-02.
**Confidence**: High (well-established perceptual psychology, Wertheimer et al.; IxDF is medium-high, but
the principles are canonical and cross-verified across HCI literature).
**UX implication (reviewer flags)**: Grouping must be conveyed visually (spacing, shared container,
consistent styling), not left implicit. Inconsistent styling of same-function elements (violates
similarity) or cramped spacing between unrelated groups (violates proximity) is flaggable.
**Caveats**: These describe perception, not taste; they serve usability (grouping/relationships), which
is this rule's remit — pure aesthetic polish belongs to a separate rule.

**Principle — Scanning patterns (F / layer-cake / spotted)**: Users scan rather than read; text at
top-left and headings receive the most fixations.
**Evidence**: "text on the left and towards the top of the page is read more than text on the right or
towards the bottom"; the layer-cake pattern "consists of fixations placed mostly on the page's
headings and subheadings." — Kara Pernice, NN/g, 2019-08-25.
https://www.nngroup.com/articles/text-scanning-patterns-eyetracking/ — Accessed 2026-07-02.
**Confidence**: High (eye-tracking research, authoritative).
**UX implication (reviewer flags)**: Front-load key info top-left; use descriptive headings/subheadings
(enables layer-cake scanning); use formatting (bold, links, bullets) to create scannable landmarks;
avoid dense unbroken text blocks. The Z-pattern applies mainly to sparse, image-led pages — don't
over-cite it for content pages.
**Caveats**: Patterns are tendencies, not laws; highly motivated users read thoroughly ("commitment").

**Principle — Contrast & emphasis for hierarchy**: Visual weight (size, color, contrast, whitespace)
should map to information importance and guide the eye (figure-ground).
**Evidence**: Gestalt figure-ground (IxDF, above); WCAG contrast minimums (see §9).
**UX implication**: The most important action/element should be the most visually prominent; a screen
with many equally-weighted elements has no hierarchy (flag "everything is bold/primary").
**Caveats**: Emphasis is relative — too many emphasized elements = none emphasized.

---

## 8. Control-Selection Patterns

**Principle — Radio vs. checkbox by mutual exclusivity**: Use radio buttons for mutually exclusive
single-choice; checkboxes for independent multi-select (zero-to-many); standalone checkbox for a
single on/off option.
**Evidence**: "Radio buttons are used when there is a list of two or more options that are mutually
exclusive and the user must select exactly one choice." / "Checkboxes are used when... the user may
select any number of choices, including zero, one, or several." / "Use checkboxes and radio buttons
only to change settings, not as action buttons that make something happen." / "Always offer a default
selection for radio button lists." — Jakob Nielsen, NN/g, 2004-09-26.
https://www.nngroup.com/articles/checkboxes-vs-radio-buttons/ — Accessed 2026-07-02.
**Confidence**: High (authoritative primary).
**UX implication (reviewer flags)**: A set of checkboxes where only one may be selected is a bug (use
radios/toggle). Radios without a default violate the guidance. Controls that trigger an action on
change (rather than a submit) misuse the pattern. Radio sets should be comprehensive + distinct (add
"Other" if not).
**Caveats**: Toggles (switches) suit immediate binary on/off with instant effect; radios suit
deferred, submit-based choice.

**Principle — Presets & escape hatches**: Convert open-ended choice into known intent via presets/
templates, and always provide a reset/escape (heuristic #3 control & freedom).
**Evidence**: Heuristic #3 (NN/g); Hick's Law (reduce choice); Tesler's Law (absorb complexity).
**UX implication (reviewer flags)**: Complex configuration should offer sensible presets plus a
"reset to defaults" / cancel; destructive or hard-to-reverse choices need an escape hatch.
**Caveats**: Too many presets re-introduce Hick's-Law overload.

---

## 6. Feedback & System State

**Principle — Visibility of system status**: The system should always keep users informed of what is
happening through timely, appropriate feedback (heuristic #1).
**Evidence**: NN/g heuristic #1 (source in §1). Response-time limits (Nielsen 1993): "0.1 second is
about the limit for having the user feel that the system is reacting instantaneously"; "1.0 second is
about the limit for the user's flow of thought to stay uninterrupted"; "10 seconds is about the limit
for keeping the user's attention." https://www.nngroup.com/articles/response-times-3-important-limits/
— Accessed 2026-07-02.
**Confidence**: High (authoritative primary, two NN/g sources).
**UX implication (reviewer flags)**: Actions taking >~1s need a busy/loading indicator; >~10s need a
determinate progress indicator + ability to cancel; sub-0.1s needs none. Any state change (save,
delete, submit) must produce visible confirmation. Complements the Doherty Threshold (<400ms target).
**Caveats**: Over-notifying (toasts for trivial actions) creates noise; match feedback salience to
consequence.

**Principle — Design all UI states, not just the happy path**: Every data-driven view has multiple
states that must be intentionally designed: ideal/populated, empty (no data yet / first run),
loading, error, and partial (some data, some missing/failed).
**Evidence**: Grounded in heuristic #1 (visibility) and heuristic #9 (error recovery), NN/g (§1). The
five-state framing ("blank/ideal/loading/partial/error") is popularized by Scott Hurff, *Designing
UX: Prototyping* / "The 5 states every UI should account for."
https://scotthurff.com/posts/why-your-user-interface-is-awkward-youre-ignoring-the-ui-stack — Accessed 2026-07-02.
**Confidence**: Medium (empty/loading/error each map to authoritative heuristics; the exact 5-state
taxonomy is from an industry practitioner, not a standards body — cross-referenced to heuristics #1/#9).
**UX implication (reviewer flags)**: A component that renders data but has no empty state, no loading
state, or no error state is incomplete. Empty states should guide the next action (not just show
"No results"). Flag UIs that assume data always loads successfully.
**Caveats**: Not every component needs all five; scope states to whether the data source can be empty,
slow, or fail.

**Principle — Confirmation + undo for destructive/irreversible actions**: Prevent errors before they
happen (heuristic #5) and provide user control/freedom via reversibility (heuristic #3).
**Evidence**: Heuristic #5 "Error Prevention" ("eliminate error-prone conditions or ... ask users to
confirm before they commit to the action") and heuristic #3 "User control and freedom" ("support Undo
and Redo") — NN/g (source §1).
**UX implication (reviewer flags)**: Destructive actions (delete, overwrite, bulk operations) need a
guardrail — ideally undo (preferred, less interruptive) or a confirmation dialog for the truly
irreversible. Prefer undo over modal confirmation for reversible actions. Never make destruction a
one-click, unguarded default.
**Caveats**: Confirmation-dialog overuse causes habituation (users click "OK" reflexively); reserve
for consequential actions.

**Principle — Optimistic UI (perceived performance)**: Update the UI immediately as if an action
succeeded, then reconcile with the server, to keep interactions within the Doherty Threshold.
**Evidence**: Doherty Threshold (<400ms), Laws of UX (§2); response-time limits (Nielsen, above).
**UX implication**: For high-confidence, reversible actions (likes, toggles, adds), reflect the change
instantly and roll back on failure with a clear message.
**Caveats**: Don't use optimistic UI for actions likely to fail or hard to reverse (payments);
mismatch between shown and actual state erodes trust.

---

## 7. Forms & Data Entry

**Principle — Persistent labels, not placeholder-as-label**: Every field needs a visible, persistent
label outside the field; placeholder text must not carry the label's meaning.
**Evidence**: "Disappearing placeholder text strains users' short-term memory"; screen readers may not
announce placeholders; recommended practice is to "place labels and hints outside form fields where
they remain always visible." — Katie Sherwin, NN/g, 2014-05-11 (updated 2018-09-10).
https://www.nngroup.com/articles/form-design-placeholders/ — Accessed 2026-07-02.
**Confidence**: High (authoritative; also an accessibility requirement, WCAG §9).
**UX implication (reviewer flags)**: An input whose only label is a `placeholder` is a defect (memory,
accessibility, and error-recovery problems). Labels should be programmatically associated
(`<label for>` / `aria-label`).
**Caveats**: Placeholders are fine for supplementary format hints ("e.g., name@example.com") alongside
a real label.

**Principle — Validate inline, after field completion; keep errors specific and adjacent**: Validate
when the user leaves a field (not on every keystroke), show the error next to the field, and preserve
input.
**Evidence**: "as soon as the user has finished filling in a field, an indicator should appear nearby
if the field contains an error"; "avoid showing an error until the user has finished with the field";
"Keeping error messages next to the fields in error minimizes working-memory load." — Rachel Krause,
NN/g, 2019-02-03 (updated 2024-12-12).
https://www.nngroup.com/articles/errors-forms-design-guidelines/ — Accessed 2026-07-02.
**Confidence**: High (authoritative primary).
**UX implication (reviewer flags)**: Errors shown on every keystroke (premature) or only in a summary
far from the field are flaggable. On submit failure, preserve entered values. Combine color with an
icon/text (not color alone — §9).
**Caveats**: Some checks (uniqueness, server rules) can only run on submit; make those errors clear on
reload.

**Principle — Recoverable, specific, blame-free error messages**: State the problem precisely in human
language and tell the user how to fix it.
**Evidence**: "Use human-readable language"; "Concisely and precisely describe the issue" (not "An
error occurred"); "Take a positive tone and don't blame the user"; "Preserve the user's input." — Tim
Neusesser & Evan Sunwall, NN/g, 2023-05-14. https://www.nngroup.com/articles/error-message-guidelines/
— Accessed 2026-07-02. Cross-ref: heuristic #9 (NN/g, §1).
**Confidence**: High (two authoritative NN/g sources).
**UX implication (reviewer flags)**: Error text like "Invalid input" / "Error 400" / a raw stack trace
is a violation. Good: name the field, the problem, and the fix ("Password must be at least 8
characters"). Never dead-end the user.
**Caveats**: Don't leak sensitive/security detail in error text; balance specificity with safety.

**Principle — Forgiving input & minimal required fields (Postel's Law)**: Accept varied input formats
and normalize; ask only for what you need.
**Evidence**: Postel's Law (§2); heuristic #5 error prevention (§1). GOV.UK #4 "Do the hard work to
make it simple." https://www.gov.uk/guidance/government-design-principles — Accessed 2026-07-02.
**UX implication (reviewer flags)**: Rejecting a phone number for containing spaces/dashes, or a card
number with spaces, is a defect — strip/normalize instead. Every required field should be justified;
mark optional vs required explicitly and consistently.
**Caveats**: Forgiving parsing must not become unsafe/ambiguous parsing (e.g., dates); normalize
deterministically.

---

## 9. Accessibility as UX (WCAG POUR)

**Principle — POUR**: Accessible design rests on four principles — Perceivable, Operable,
Understandable, Robust — and accessibility is a baseline of good UX, not a bolt-on.
**Evidence**: W3C/WAI: Perceivable ("Text alternatives... for non-text content"; "Content can be
presented in different ways"; sufficient contrast); Operable ("All functionality that is available by
mouse is also available by keyboard"; "keyboard focus does not get trapped"; "the keyboard focus is
visible"; targets "large enough to... activate by touch"); Understandable (readable, predictable,
input assistance); Robust (valid markup, AT-compatible).
https://www.w3.org/WAI/fundamentals/accessibility-principles/ — Accessed 2026-07-02.
Reinforced by GOV.UK #6 "This is for everyone — Accessible design is good design."
**Confidence**: High (W3C is the standards body; authoritative).
**UX implication (reviewer flags)**: See specific sub-criteria below. Accessibility failures are UX
failures.

**Principle — Full keyboard operability + visible focus**: All interactive functionality must be
usable by keyboard, focus order must be logical, focus must be visible, and focus must never be trapped.
**Evidence**: W3C (above): "All functionality that is available by mouse is also available by
keyboard"; "the keyboard focus is visible, and the focus order follows a meaningful sequence."
**UX implication (reviewer flags)**: Custom controls (div-as-button) without keyboard handlers/`tabindex`
/roles, removed focus outlines (`outline: none` with no replacement), or focus traps are violations.
**Caveats**: Focus styling can be customized but must remain clearly visible (WCAG 2.4.7/2.4.11).

**Principle — Color contrast minimums**: Text needs sufficient luminance contrast; don't rely on color
alone to convey meaning.
**Evidence**: WCAG 1.4.3 (AA): normal text ≥ 4.5:1, large text (≥18pt, or 14pt bold) ≥ 3:1; WCAG
1.4.11 (AA): UI components / graphical objects ≥ 3:1; WCAG 1.4.6 (AAA): 7:1 / 4.5:1. — WebAIM,
"Contrast and Color Accessibility." https://webaim.org/articles/contrast/ — Accessed 2026-07-02.
"Color is not used as the only way of conveying information" — W3C (above).
**Confidence**: High (WebAIM authoritative on WCAG; cross-ref W3C).
**UX implication (reviewer flags)**: Low-contrast text (grey-on-white placeholders, light labels),
UI borders/icons below 3:1, and status conveyed by color alone (red/green only) are violations. Pair
color with text/icon/shape.
**Caveats**: Logos and incidental/disabled elements are exempt from contrast minimums.

**Principle — Adequate target size**: Interactive targets must be large enough to activate reliably,
especially by touch.
**Evidence**: WCAG 2.5.8 Target Size (Minimum), Level AA: "at least 24 by 24 CSS pixels" (with a
spacing exception). WCAG 2.5.5 (AAA) recommends the larger 44×44 CSS px. — W3C.
https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html — Accessed 2026-07-02.
Ties to Fitts's Law (§2). Apple HIG (44pt) and Material (48dp) are pattern exemplars of the stricter target.
**Confidence**: High (W3C standard).
**UX implication (reviewer flags)**: Tiny tap targets (< 24px, or cramped without spacing) are
violations; comfortable touch UIs target ~44–48px. Adjacent small targets need spacing.
**Caveats**: Inline text links and user-agent-default controls are exempt from 2.5.8.

**Principle — Semantic structure & text alternatives**: Use correct semantic elements/headings and
provide text alternatives for non-text content.
**Evidence**: W3C (above): "Text alternatives are equivalents for non-text content"; "Content can be
presented in different ways" via proper markup; Robust requires valid, AT-interpretable markup.
**UX implication (reviewer flags)**: Images without `alt`, icon-only buttons without accessible names,
non-semantic markup (div soup, skipped heading levels), and controls without labels are violations.
**Caveats**: Decorative images take empty `alt=""`; don't over-describe.

---

## 10. Content Design / Microcopy

**Principle — Plain language**: Write for the audience in common, everyday words; prefer active voice,
short sentences, "you", and no jargon.
**Evidence**: U.S. Federal Plain Language Guidelines — "content that is clear and easy to understand"
is core; principles include writing for the audience, using common everyday words, active voice,
pronouns ("you"), and short sentences. — plainlanguage.gov / digital.gov, adapted from the Plain
Writing Act of 2010. https://digital.gov/guides/plain-language — Accessed 2026-07-02. Cross-ref:
NN/g heuristic #2 (match the real world — "speak the users' language"); GOV.UK #4.
**Confidence**: Medium-High (authoritative government standard; the redirected page gave a high-level
summary, so specific technique wording is cross-referenced to the well-established guidelines).
**UX implication (reviewer flags)**: UI copy full of internal jargon/acronyms, passive constructions,
or system-centric wording ("An exception was thrown") is flaggable. Prefer user-centered, task-oriented
language.
**Caveats**: Domain-expert audiences may expect precise technical terms; "plain" is relative to audience.

**Principle — Action-labeled controls**: Buttons and links should be labeled with the specific action
they perform, not generic verbs.
**Evidence**: Heuristic #2 (match real world) and #6 (recognition) — NN/g (§1). Error-message
guidance's "offer constructive solutions" extends to actionable labels (NN/g, §7).
**UX implication (reviewer flags)**: Generic labels ("OK", "Submit", "Click here", "Yes/No" on a
destructive dialog) are weaker than specific ones ("Save changes", "Delete 3 files", "Download PDF").
Link text should make sense out of context (also an accessibility requirement).
**Caveats**: Keep labels concise; overly long labels hurt scannability.

**Principle — Helpful empty-state and error copy**: Empty states and errors are content, not
afterthoughts — explain what happened and what to do next.
**Evidence**: Heuristic #9 (recognize/diagnose/recover) and #1 (visibility) — NN/g (§1);
error-message guidelines (NN/g, §7).
**UX implication (reviewer flags)**: An empty state that only says "No data" wastes an opportunity —
guide the first action ("Create your first project"). Error copy should be specific and constructive.
**Caveats**: Don't over-explain trivial states.

---

## 11. Cognitive Load & Error Prevention

**Principle — Minimize memory load (recognition over recall)**: Reduce what users must hold in working
memory; make information and options visible/retrievable.
**Evidence**: Heuristic #6 (NN/g, §1); Miller's Law (working-memory limits, §2). Placeholder guidance
("strains users' short-term memory," NN/g §7).
**UX implication (reviewer flags)**: Requiring users to remember data across steps, re-enter known
information, or memorize codes/formats increases load — surface it instead (autofill, summaries,
persistent labels).
**Caveats**: Balance against clutter/minimalism (heuristic #8).

**Principle — Prevent errors before they happen; then aid recovery**: Prevention (constraints, good
defaults, confirmation, forgiving input) beats even excellent error messages; when errors do occur,
support graceful recovery.
**Evidence**: Heuristic #5 "Error Prevention" — "Good error messages are important, but the best
designs carefully prevent problems from occurring in the first place." Paired with heuristic #9
(recovery) and #3 (undo). — NN/g (§1).
**Confidence**: High (authoritative primary).
**UX implication (reviewer flags)**: Prefer constraints/affordances that make errors impossible
(disable invalid actions, input masks, sensible ranges, confirmation on destructive acts) over merely
reporting the error afterward. Both prevention and recovery should exist.
**Caveats**: Over-constraining frustrates power users; prevention shouldn't block legitimate edge cases.

**Principle — Consistency and standards**: Same words, controls, and actions should mean the same
thing throughout the product, and follow platform/industry conventions (Jakob's Law).
**Evidence**: Heuristic #4 (NN/g, §1); Jakob's Law (§2); GOV.UK #9 "Be consistent, not uniform" —
"Use the same language and design patterns wherever possible" while allowing improvement.
https://www.gov.uk/guidance/government-design-principles — Accessed 2026-07-02.
**Confidence**: High (multiple authoritative sources).
**UX implication (reviewer flags)**: Divergent labels for the same action, inconsistent control types
for the same job, or reinvented interaction patterns for standard tasks are flaggable. "Consistent,
not uniform" — deviate only to genuinely improve, not arbitrarily.
**Caveats**: Slavish uniformity can prevent context-appropriate improvements; consistency serves
predictability, not rigidity.

---

## Source Analysis
| Source | Domain | Reputation | Type | Access Date | Cross-verified |
|--------|--------|------------|------|-------------|----------------|
| Nielsen Norman Group — 10 Heuristics | nngroup.com | High (0.9) | Industry-authoritative | 2026-07-02 | Y |
| NN/g — Response Times: 3 Limits | nngroup.com | High (0.9) | Industry-authoritative | 2026-07-02 | Y |
| NN/g — Progressive Disclosure | nngroup.com | High (0.9) | Industry-authoritative | 2026-07-02 | Y |
| NN/g — Placeholders in Form Fields | nngroup.com | High (0.9) | Industry-authoritative | 2026-07-02 | Y |
| NN/g — Error-Message Guidelines | nngroup.com | High (0.9) | Industry-authoritative | 2026-07-02 | Y |
| NN/g — Form Validation Errors | nngroup.com | High (0.9) | Industry-authoritative | 2026-07-02 | Y |
| NN/g — Text Scanning Patterns | nngroup.com | High (0.9) | Eye-tracking research | 2026-07-02 | Y |
| NN/g — Checkboxes vs Radio Buttons | nngroup.com | High (0.9) | Industry-authoritative | 2026-07-02 | Y |
| NN/g — Reset and Cancel Buttons | nngroup.com | High (0.9) | Industry-authoritative | 2026-07-02 | Y |
| Laws of UX (Jon Yablonski) | lawsofux.com | Medium-High (0.8) | Reference/summary | 2026-07-02 | Y |
| Interaction Design Foundation — Gestalt | ixdf.org | Medium-High (0.8) | Reference | 2026-07-02 | Y |
| W3C/WAI — Accessibility Principles | w3.org | High (1.0) | Standards body | 2026-07-02 | Y |
| W3C — WCAG 2.5.8 Target Size | w3.org | High (1.0) | Standards body | 2026-07-02 | Y |
| WebAIM — Contrast & Color | webaim.org | High (0.9) | Accessibility authority | 2026-07-02 | Y |
| GOV.UK — Government Design Principles | gov.uk | High (1.0) | Government standard | 2026-07-02 | Y |
| plainlanguage.gov / digital.gov | digital.gov | High (0.9) | Government standard | 2026-07-02 | Partial |
| Scott Hurff — The UI Stack (5 states) | scotthurff.com | Medium (0.6) | Practitioner | 2026-07-02 | Cross-ref to heuristics |

Reputation: High: 13 (~76%) | Medium-High: 3 | Medium: 1 | Avg ≈ 0.88.

## Knowledge Gaps
### Gap 1: Exact plain-language technique wording
**Issue**: plainlanguage.gov/guidelines 301-redirected to a digital.gov overview that summarized rather
than listed the specific techniques. **Attempted**: original guidelines URL + digital.gov redirect.
**Recommendation**: fetch the archived plainlanguage.gov guidelines (GitHub mirror) for the verbatim
checklist (short sentences, active voice, "must" not "shall", one topic per paragraph).

### Gap 2: Empirical strength of individual "laws"
**Issue**: Several laws (Peak-End, Goal-Gradient, Serial Position) rest on psychology studies of
varying replication strength; Laws of UX summarizes them but does not grade evidence quality.
**Attempted**: Laws of UX (secondary). **Recommendation**: for high-stakes use, consult the original
papers (Kahneman; Kivetz et al. 2006; Ebbinghaus) and replication literature.

### Gap 3: The "5 UI states" taxonomy origin
**Issue**: The precise ideal/empty/loading/error/partial framing is practitioner-originated (Hurff),
not a standards body. Each state maps to NN/g heuristics, but the fixed five-state list is convention.
**Recommendation**: treat as a useful checklist backed by heuristics #1/#9, not as a cited standard.

## Conflicting Information
### Conflict 1: Postel's Law — virtue or liability?
**Position A (UX)**: "Be liberal in what you accept" → forgiving input improves UX. — Laws of UX
(lawsofux.com), reputation 0.8.
**Position B (protocols/security)**: Liberal acceptance causes interoperability drift and security
risk; later IETF thinking (e.g., draft-thomson-postel-was-wrong) argues for strictness.
**Assessment**: Both correct in scope. For *UI input formatting* (this document's remit), forgiving
input + internal normalization is the durable UX guidance. For *protocol/parser/security* code, prefer
strict validation. The rule should scope Postel's Law to input-format forgiveness, not lax validation.

### Conflict 2: Miller's "7±2" as a design limit
**Position A (common usage)**: Cited to cap menu/list/nav items at ~7. — widespread secondary usage.
**Position B (NN/g / cognitive science)**: Miller's number describes short-term memory *span*, not a
limit on on-screen choices (which users don't have to memorize). Over-applying it is a myth.
**Assessment**: Position B is authoritative. The durable takeaway is *chunking* and reducing recall
load, NOT a hard item-count cap. The rule must not encode "max 7 items."

## Recommendations for Further Research
1. Distill the flat principle list below into the plugin rule; group by "always flag" vs "advisory."
2. Pull verbatim plainlanguage.gov checklist for microcopy sub-rules.
3. Add framework-specific *exemplars* (Material target sizes, Apple HIG 44pt) as non-normative
   references only — keep the rule vendor-neutral.

---

## Distillation — Flat, De-duplicated, Flaggable Principles
_Raw material for the reusable rule/skill. Each line: preferred form a reviewer can flag against._

1. Every action gives visible feedback; loading indicator > ~1s, cancelable progress bar > ~10s, target < 400ms. (Heuristic #1; Response Times; Doherty)
2. Design all states: ideal, empty, loading, error, partial — never assume data loads successfully.
3. Empty states guide the next action; don't just say "No data."
4. Destructive/irreversible actions need undo (preferred) or confirmation; never one-click unguarded.
5. Provide clearly-marked exits, cancel, and undo/redo; never trap the user. (Heuristic #3)
6. Prevent errors with constraints/defaults/forgiving input before relying on error messages. (Heuristic #5)
7. Error messages: specific, human-readable, blame-free, actionable, adjacent to the field; preserve input. (Heuristic #9)
8. No raw error codes/stack traces or "Invalid input" as user-facing copy.
9. Every field has a persistent visible label; never use placeholder as the label.
10. Validate inline after the user leaves a field — not on every keystroke, not only in a distant summary.
11. Accept forgiving input formats and normalize internally (Postel — input only, not lax security validation).
12. Ask only for necessary fields; mark required vs optional consistently.
13. Radio/single-select for mutually exclusive choice (with a default); checkbox for independent multi-select.
14. Don't use checkboxes/radios as action triggers; toggles are for instant binary on/off.
15. Ship a sensible, safe, reversible default; avoid forcing a choice where a good default exists.
16. Reduce/segment simultaneous choices; offer presets and a reset. (Hick's; Tesler)
17. Progressive disclosure for advanced/rare options; never nest deeper than 2 levels.
18. Prefer recognition over recall; don't force users to remember data across steps. (Heuristic #6; Miller → chunk, don't cap at 7)
19. Follow platform/industry conventions; deviate only to genuinely improve. (Heuristic #4; Jakob's Law; "consistent, not uniform")
20. Same word/control/action means the same thing everywhere.
21. Convey grouping visually via proximity and shared containers/styling. (Gestalt)
22. Style same-function elements consistently (Gestalt similarity); inconsistency signals false difference.
23. Front-load key content top-left; use descriptive headings for scannability; avoid dense text blocks. (F / layer-cake)
24. Establish clear visual hierarchy; if everything is emphasized, nothing is.
25. All functionality keyboard-operable; focus order logical; focus always visible; no focus traps. (WCAG Operable)
26. Text contrast ≥ 4.5:1 (normal) / 3:1 (large); UI components/icons ≥ 3:1. (WCAG 1.4.3 / 1.4.11 AA)
27. Never convey meaning by color alone — pair with text/icon/shape. (WCAG)
28. Interactive targets ≥ 24×24 CSS px (AA); ~44–48px for comfortable touch; space adjacent targets. (WCAG 2.5.8; Fitts)
29. Provide text alternatives (alt, accessible names) and semantic structure/headings; label icon-only controls. (WCAG Perceivable/Robust)
30. Use plain, audience-appropriate language; action-specific button/link labels ("Save changes", not "OK"); no internal jargon.
31. Remove non-essential elements; every extra unit competes with the relevant ones. (Heuristic #8)
32. Visual polish affects perceived usability/trust — but never let aesthetics mask real usability defects. (Aesthetic-Usability)
33. Show progress toward goals; place most-important nav/list items first or last. (Goal-Gradient; Serial Position)
34. Use optimistic UI only for reversible, high-confidence actions; roll back visibly on failure.

## Full Citations
[1] Nielsen, J. "10 Usability Heuristics for User Interface Design." Nielsen Norman Group. 1994-04-24 (updated 2024-01-30). https://www.nngroup.com/articles/ten-usability-heuristics/. Accessed 2026-07-02.
[2] Nielsen, J. "Response Times: The 3 Important Limits." Nielsen Norman Group. 1993-01-01. https://www.nngroup.com/articles/response-times-3-important-limits/. Accessed 2026-07-02.
[3] Nielsen, J. "Progressive Disclosure." Nielsen Norman Group. 2006-12-03. https://www.nngroup.com/articles/progressive-disclosure/. Accessed 2026-07-02.
[4] Sherwin, K. "Placeholders in Form Fields Are Harmful." Nielsen Norman Group. 2014-05-11 (updated 2018-09-10). https://www.nngroup.com/articles/form-design-placeholders/. Accessed 2026-07-02.
[5] Neusesser, T.; Sunwall, E. "Error-Message Guidelines." Nielsen Norman Group. 2023-05-14. https://www.nngroup.com/articles/error-message-guidelines/. Accessed 2026-07-02.
[6] Krause, R. "How to Report Errors in Forms: 10 Design Guidelines." Nielsen Norman Group. 2019-02-03 (updated 2024-12-12). https://www.nngroup.com/articles/errors-forms-design-guidelines/. Accessed 2026-07-02.
[7] Pernice, K. "Text Scanning Patterns: Eyetracking Evidence." Nielsen Norman Group. 2019-08-25. https://www.nngroup.com/articles/text-scanning-patterns-eyetracking/. Accessed 2026-07-02.
[8] Nielsen, J. "Checkboxes vs. Radio Buttons." Nielsen Norman Group. 2004-09-26. https://www.nngroup.com/articles/checkboxes-vs-radio-buttons/. Accessed 2026-07-02.
[9] Nielsen, J. "Reset and Cancel Buttons." Nielsen Norman Group. 2000-04-15. https://www.nngroup.com/articles/reset-and-cancel-buttons/. Accessed 2026-07-02.
[10] Yablonski, J. "Laws of UX." lawsofux.com. Accessed 2026-07-02.
[11] Interaction Design Foundation. "Gestalt Principles." ixdf.org. https://ixdf.org/literature/topics/gestalt-principles. Accessed 2026-07-02.
[12] W3C/WAI. "Accessibility Principles." W3C. https://www.w3.org/WAI/fundamentals/accessibility-principles/. Accessed 2026-07-02.
[13] W3C. "Understanding SC 2.5.8: Target Size (Minimum)." WCAG 2.2. https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html. Accessed 2026-07-02.
[14] WebAIM. "Contrast and Color Accessibility." webaim.org. https://webaim.org/articles/contrast/. Accessed 2026-07-02.
[15] Government Digital Service. "Government Design Principles." GOV.UK. https://www.gov.uk/guidance/government-design-principles. Accessed 2026-07-02.
[16] U.S. Federal Plain Language Guidelines. plainlanguage.gov / digital.gov. https://digital.gov/guides/plain-language. Accessed 2026-07-02.
[17] Hurff, S. "The UI Stack: The 5 States Every UI Should Account For." scotthurff.com. Accessed 2026-07-02.

## Research Metadata
Duration: single session | Examined: 16 sources (15 fetched, 2 redirect-resolved) | Cited: 17 | Cross-refs: extensive (laws cross-referenced to original researchers + Laws of UX; heuristics anchor multiple applied findings) | Confidence: High ~76%, Medium-High ~18%, Medium ~6% | Output: docs/research/ux/general-ux-design-best-practices.md


