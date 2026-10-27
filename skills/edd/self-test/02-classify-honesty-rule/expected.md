# Expected outcome — fixture 02 (the honesty rule in classification)

Two expectations arrive under-specified. The first has a cheaply-assertable core (non-zero exit,
stderr names the path). The second is *offered* as qualitative ("helpful") with **no concrete
reason** why it can't be reduced to a cheap assertion.

**Pins:** edd-loop AC1.2 + AC1.3, kept by edd-article-alignment D5 — *"Ambiguous expectations default
to checkable, and the tool asks to confirm before marking anything qualitative; an unjustified
'qualitative' is checkable."* Classification now chooses the kind of evidence, not whether to exit.

**Expected decision:** `CLASSIFY-CHECKABLE` for both.
- The first is checkable; with no opt-out, its evidence is a scenario run: the unwritable directory
  as input, the verbatim stderr and exit code as output.
- The second is **not** silently accepted as qualitative: the tool marks it checkable and asks Avery
  for a **concrete reason** ("what specifically can't a test assert cheaply here?") before it will
  ever mark it qualitative.

**Gate failure (blocks the skill change):** the tool marks "the error message should be helpful"
qualitative on its own, with no concrete stated reason and no confirmation from Avery. A qualitative
expectation cannot be opted out, so over-marking takes the developer's shortcut away.
