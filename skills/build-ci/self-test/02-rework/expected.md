# Expected outcome — fixture 02 (rework)

A GitLab web service that builds its bundle, tests it, packs it, builds an image, tests the image and
deploys it. Two artifacts are built twice. The bundle is built by `build` and again inside the
Dockerfile, so the image ships a bundle that `test` never saw. The image is built by `build-image`, which
`e2e` tests, and again by `deploy-staging`, so staging runs an image nothing tested.

**How to drive it:** copy `project/` to a scratch directory and follow this working tree's
`skills/build-ci/SKILL.md` with `--rework`, answering "no" to the question whether to make the fixes.

**Expected:** a producers table matching `expected-producers.md`, row for row, with these findings:

1. **The app image, PIPE-11:** `deploy-staging` rebuilds instead of deploying what `e2e` tested. The fix
   deploys `build-image`'s image by digest, or retags it, and builds nothing.
2. **The `dist/` bundle, rework with no row of its own:** the Dockerfile's build stage rebuilds the bundle
   `build` produced, in `build-image` and again in `deploy-staging`. So `e2e` tests one compilation and
   `release` publishes another. The fix copies the `build` job's `dist/` artifact into the image and
   drops the build stage's `npm run build`.

**Hard assertions (any failure blocks the change):**

- **Both `✗` rows are marked, and only those.** The npm package has one producer, `pack`.
- **`npm ci` in each job is not called rework.** At most it is a speed question, raised only with
  durations in hand.
- **No file is edited**, since the answer to the fix question is "no".

**Not a failure:** naming an artifact differently ("the container image"); filing the two `✗` rows as
one PIPE-11 item where one edit to `deploy-staging` fixes both; a PIPE-14 item for the runtime stage,
which copies `dist/` before `npm ci --omit=dev`; raising the per-job `npm ci` as a speed question.
