<!-- decision-request-emission:v1 -->

<!-- context -->

Verified detail behind the three that remain:

- `agents/` — all five (`adversarial-reviewer`, `adversarial-verifier`, `edd-evidence-producer`, `refactor-critic-correctness`, `refactor-proposer`) carry `color=0 examples=0`
- No `LICENSE` file anywhere in the tree, and no `license` field in `.claude-plugin/plugin.json`
- `CLAUDE.md` is copied verbatim into every cached install — confirmed present in the 0.12.0, 0.19.0 and 0.36.0 snapshots

<!-- /context -->

<!-- marker -->

---

<!-- /marker -->

<!-- interrupted -->

Everything the reviewers recommended is now done except three things I should not decide for you.

Two of them the tool cannot settle.

<!-- /interrupted -->

<!-- decision -->

This project has no license text and no license named anywhere, while being published through a marketplace for other people to install

<!-- /decision -->

<!-- consequence -->

— that is a legal question about your intent, not a formatting gap.

<!-- /consequence -->

<!-- decision -->

Separately, the file holding this project's own development rules gets copied into every install, so strangers receive nineteen kilobytes of instructions meant only for working here, and the editor prints a warning about it on load.

<!-- /decision -->

<!-- consequence -->

Leaving it is defensible; leaving it silently while something warns is the part worth choosing.

<!-- /consequence -->

<!-- decision -->

The third is work rather than a decision: the five background helpers each lack the worked examples their own authoring guide asks for, which measurably improves how accurately they get picked.

<!-- /decision -->

<!-- consequence -->

That is real writing across five unrelated files.

<!-- /consequence -->

<!-- call -->
