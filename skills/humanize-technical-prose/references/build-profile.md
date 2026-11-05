# Build a Profile

The procedure for `--build-profile`, loaded from `../SKILL.md` Step B. The outcomes it reports are
defined in that file's `## Outcomes` tables, and it classifies slips in that file's Slip Vocabulary.

## B1. Gather the samples

Read only the paths the author named, now or in an earlier build of this profile. Never read a transcript, the conversation, or the author's typed
prompts as a sample: prompts show how the author gives instructions, not how they write. The script
refuses the whole run when a named path is a transcript (a `.jsonl` file, or anything under a
`.claude/projects/` directory), is missing, or is not Markdown, plain text or LaTeX. Report each under
`SAMPLE-REFUSED` with the script's `why`, report `PROFILE-NOT-BUILT`, and let the author name the
samples again.

Run `python3 ${CLAUDE_PLUGIN_ROOT}/skills/humanize-technical-prose/scripts/measure_voice.py --list`.
If the profile already exists, rebuild it from every sample, old and new: name its
listed `samples` together with the new paths. The script stores each sample by its resolved path and
measures a path named twice once, and `--build` overwrites the profile.

- A listed sample that no longer exists is left out of the rebuild and reported under
  `SAMPLE-REFUSED`, so one moved file cannot block every later build.
- A profile whose `samples` `--list` shows as `null` is broken: build it from the named paths alone,
  and say so.
- To drop a sample, build again from only the samples to keep, without carrying the old list over.

## B2. Measure

```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/humanize-technical-prose/scripts/measure_voice.py --measure {paths…}
```

The script measures only the author's own prose: it skips code, quotations, headings, tables, lists,
figures and math, and LaTeX's bookkeeping commands. It reports sentence lengths, short sentences,
questions, contractions, first person, openers, connectives and favoured phrases. A phrase is kept
only when it recurs, in two samples or three times in one, and never when it holds a name.

A sample under 500 words of own prose is left out and listed under `SAMPLE-THIN` with its count. If
every sample is thin, report `PROFILE-NOT-BUILT` and write nothing.

## B3. Tally the slips

Read each sample that was measured, whole, skipping what the script skips. Find each slip the author
made, and classify it in `../SKILL.md`'s Slip Vocabulary, the one the script accepts.

These are not slips: a spelling the author's variety of English uses, such as *travelling*; a choice
the document makes every time, such as its comma style; a term spelled the way its field spells it;
and an error inside a quotation. When unsure, it is not a slip.

Count, and never write a slipped word: not in the profile, the tally or the report. The profile needs
only the kinds and their counts, and it persists outside every repository, where a slipped word would
outlive the run.

## B4. Write the profile

Pass the tally to the script on standard input, with the same paths:

```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/humanize-technical-prose/scripts/measure_voice.py --build {name} --slips - {paths…} <<'TALLY'
{"misspelling": {"dropped letter": 0, …}, "grammar": {"revision residue": {…}, "omission": {…}, "substitution": {…}}, "on_name_or_term": 0}
TALLY
```

The script refuses a tally holding anything but whole numbers under the Slip Vocabulary, and a
profile name holding anything but lowercase letters, digits and hyphens. It prints the profile's path.
On a tally refusal, correct the tally against the Slip Vocabulary and run B4 again; never write the
profile by hand. If the script refuses it again, report `PROFILE-NOT-BUILT` with its `why`.

## B5. Report

Read `${CLAUDE_PLUGIN_ROOT}/rules/writing.md` before composing the report, as Step 7 does. Take the
measures from B2's output and the path from B4's.

```
PROFILE-BUILT {name}: {k} samples, {words} words — sentences {median}/{p90}, contractions {c} per 1,000 words, questions {q} per 100 sentences, slips {total} (grammar {g}, spelling {s}; {t} on names or terms)
  profile: {profile path}
PROFILE-NOT-BUILT {name}: {every sample was thin | the script refused a named sample | the script refused the slip tally — {why}}
SAMPLE-THIN
  {sample} — {words} words
SAMPLE-REFUSED
  {sample} — {why}
```

Name the samples by path, and quote nothing from them.
