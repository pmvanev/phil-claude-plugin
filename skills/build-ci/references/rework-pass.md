# The Rework Pass (`/phil:build-ci --rework`)

Work done twice is time spent, and a build nobody tested. Read the Rework rows of
`${CLAUDE_PLUGIN_ROOT}/rules/ci-pipelines.md` and its counting paragraph first. Gather the pipeline and
the recorded decisions as `SKILL.md` Step 1's bullets do, including every `Dockerfile*` a job builds, the
build tool's configuration, and the manifest's lifecycle scripts.

## 1. List each artifact's producing jobs

Every compiled output, bundle, package, archive and image the pipeline makes. Name it by what it is, not
by its path in one job. Two outputs are **the same artifact** when they come from the same inputs, the
same build command and the same target: a test-target image and a production-target image are two
artifacts, and so are a debug and a release build. A matrix or `parallel:` job is one producer.

Look for producers a job does not name:

- a `Dockerfile` stage that builds — every job that builds the image produces what that stage produces,
  whatever the tool: `docker build`, `buildx`, Kaniko, Buildah;
- npm's `prepare`, `prepack` and `prepublishOnly` scripts, which `npm ci`, `npm pack` and a bare
  `npm publish` run;
- `pip install .`, which builds the project's own wheel.

## 2. List its consumers

The jobs that take it through `artifacts:` and `needs:`, a download step, or an image tag or digest.

## 3. Write the table

Artifact, producing jobs, consuming jobs. Mark each row with more than one producer `✗`.

## 4. File each `✗`

**An artifact with two producers is rework.** Where a later producer is a deploy or release job, it is
also PIPE-11, deploy what was tested; file the PIPE-11 item at that job, and one edit that fixes several
rows is one item, as the rule counts. A second producer that deploys nothing is filed as rework, with no
row id: name the artifact, its producers and what each consumer received.

Then check the Rework rows a table does not show: build output passed through a cache (PIPE-12), and a
`Dockerfile` that copies the source, or files built from it, before it installs (PIPE-14).

A dependency install in a deploy or release job is PIPE-11's "installs build dependencies". In any
other job it is not rework: it is a speed question, raised only with durations in hand.

## 5. Ask, fix, report

Ask once, one question per fix, whether to make it: produce the artifact once and pass it on, by artifact
or by digest. Make the fixes taken as `SKILL.md` Step 5 writes any job, then lint as Step 6.3 does.
**Report** the table, each item filed with its row and fix, what was not read, and which fixes were made.
