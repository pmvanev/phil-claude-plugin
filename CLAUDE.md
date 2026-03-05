# Global Development Standards

Development and writing standards live in `~/.claude/rules/`. Rules load automatically based on the files you touch — no manual reading required.

## Key Principles (always apply)

- **Test first.** Write a failing test before production code.
- **Separate structure from behavior.** Refactoring commits and behavior-change commits are separate.
- **Dependencies point inward.** Business rules never import infrastructure.
- **Make every word tell.** Active voice, no needless words, clear on first read.
- **Empirical design over speculation.** Solve for what is really there, not imagined futures.
