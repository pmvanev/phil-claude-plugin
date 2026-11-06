# RECORD — the comments autopilot leaves on the card

Part of the `autopilot` skill; `../SKILL.md` governs this file as much as this file does. Read it whole
before the first comment. Every word the run composes follows the writing standard `../SKILL.md` names;
every quoted line of the card, `CLAUDE.md` or `AGENTS.md` keeps its own words.

## Three comments, one shape rule

| Comment | First line, exactly | Posted |
|---|---|---|
| The path | `**Autopilot · build path**` | before the first step, unless the card holds it already |
| A step | `**Autopilot · step <k> of <m>**`, then on the same line `— <the step> — done`, or `— work done, landing left` | after each step the run finishes |
| A blocker | `**Autopilot · blocked at step <k> of <m>**` | when a blocker stops the run |

Start every line with the header, a step number, `-`, `Next:` or `Starting the run`, never with `/`:
GitLab runs a note line that starts with a quick action such as `/close`, with the poster's rights.
Keep each quote on the same line as its step.

**The path comment** holds the steps, one line each with its quote, then the next step and the
authorized writes. The AUTHORIZED line lists the writes that leave the machine; commits in the card's
worktree belong to the work. This repo's path reads:

```
**Autopilot · build path**

1. nw-discuss (done) — CLAUDE.md, Build path for this plugin: "Run `nw-discuss` before authoring a new feature, skill or command."
2. author after plugin-dev — CLAUDE.md, Build path for this plugin: "Read `plugin-dev:skill-development`, `command-development`, `agent-development` or `plugin-structure` before writing the file."
3. …
6. push and open a pull request — CLAUDE.md, CI workflow: "Land every change on `main` through a pull request: push a feature branch, open a pull request, and merge once its pipeline passes."
7. merge once its pipeline passes — CLAUDE.md, CI workflow: (the same line)

Next: step 2.
Starting the run authorizes: push (step 6), pull request (step 6), merge once its pipeline passes (step 7).
```

**A step comment** quotes the step's source line on its second line, so a later run can tell the step
is the same one. Then it lists the step's decisions, one line each — the question, the option taken,
and its source — and any work found beyond the card. A step that raised no question says so. A
landing step's comment also names the pull or merge request and its pipeline's result, fixes included.

```
**Autopilot · step 2 of 7** — author after plugin-dev — done
- Source: CLAUDE.md, Build path for this plugin: "Read `plugin-dev:skill-development`, … before writing the file."
- Split the skill's detail into references? — took "yes", recommended: the body passed 3,000 words.
- File a card for the two GitHub-only commands? — no, by your saved preference "ask before filing a new card".
- Found: `/phil:resume` reads the board through `gh` only — yours to place.
```

**A blocker comment** names what stopped the run, its kind, and the line or fact behind it, then what
the developer does next.

```
**Autopilot · blocked at step 3 of 7**
- Which of your unpublished essays should the profile learn from? — an input only you hold.
- Next: answer on this card, then run /phil:autopilot 88 to resume at step 3.
```

## Read, compare, post, read back

Read the card's comments, every page:

```bash
gh api graphql --paginate -f query='
query($o:String!,$r:String!,$n:Int!,$endCursor:String){ viewer{ login }
  repository(owner:$o,name:$r){ issue(number:$n){
    comments(first:100, after:$endCursor){ pageInfo{ hasNextPage endCursor }
      nodes{ body author{ login } } } } } }' \
  -f o=<owner> -f r=<repo> -F n=<n>
```

A read that fails posts nothing: `RECORD-FAILED`, quoting the error. For the path comment, take the
latest comment by `viewer.login` whose first line is `**Autopilot · build path**`. Where it holds the
same quoted lines, in the same order, with the same step numbers on its authorized writes, post
nothing: `ALREADY-RECORDED`. The `done` marks and the words the run composed may differ; they are not
compared, because progress lives in the step comments. Step and blocker comments are never compared:
post each once. Then post:

```bash
gh issue comment <n> -R <owner/repo> --body-file - <<'EOF'
<the comment>
EOF
```

Use `gh issue comment` only with `-R` and `--body-file -`; never `--edit-last` or `--delete-last`.
Read the comments back once. A comment is `RECORDED` where the developer's latest comment with its
first line now holds the quoted lines posted — for a step or blocker comment, its first line and its
source line. A post that fails, or does not read back, is `RECORD-FAILED`, quoting the error. Post once
only, and repair nothing: a timed-out post may have landed. A failed step comment does not stop the
run; the report names it.

## On GitLab

A comment is a note, read and posted with `<p>` and `<repo>` as
`${CLAUDE_PLUGIN_ROOT}/skills/start/references/gitlab.md` writes them. Read the card's notes, newest
first, skipping the system notes GitLab writes itself:

```bash
glab api --hostname <host> --paginate \
  "projects/<p>/issues/<n>/notes?sort=desc&order_by=created_at&per_page=100" |
  jq -c '.[] | select(.system | not) | {body, author: .author.username}'
```

The developer is `user`'s `username`, and the first matching note is the latest. The pipe's exit code
is `jq`'s, so judge the read by `glab`'s own output: any `glab` error, on any page, fails the read,
whatever `jq` printed. Post the note with the whole comment in `--message`, writing each `'` in it as
`'\''`:

```bash
glab issue note <n> -R <repo> --message '<the comment>'
```

Use `glab issue note` only with `-R` and `--message`: without `--message` it opens an editor. The rules
above — compare, post once, read back — stand. These two calls follow `glab` 1.112.0's
`issue note --help` and GitLab's notes API; no run has exercised them yet.
