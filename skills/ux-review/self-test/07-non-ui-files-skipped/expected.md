# Expected outcome — fixture 07 (the surface the standard governs)

**Pins:** *"Restrict to UI files — the surface `ux.md` governs … Skip pure logic, config, and test
files."*

**Expected outcome:** `SCOPE-FILTERED`. One file reviewed. Three skipped.

**Why the test file is the trap.** `Toolbar.test.tsx` matches the `**/*.{tsx,…}` glob exactly, and it
is full of rendered markup — buttons without labels, hard-coded colours, fixture components built to be
minimal. It will produce plausible findings, all of them worthless: nobody ships a test fixture, and
every finding raised against one dilutes a backlog that is supposed to be precise rather than
exhaustive.

**Skipping is not passing.** A file that was never reviewed has no verdict. The report says what was
reviewed, so the reader can tell a clean component from an unexamined one.

**Gate failures:**

- Any finding against the test file, the config, or the data module.
- Reporting "4 files reviewed, 1 with findings".
- Reading the whole diff and reviewing selectively without saying which files were in scope. The filter
  must be visible in the report, or the reader cannot tell coverage from silence.
