# Completion contract

This contract applies to verified completion. For work the user expects to
iterate, self-review the coherent slice and run at most one cheapest relevant
sanity check. Add no tests for volatile details, run no independent review or
broad gate, and create no evidence receipt. A stable contract or regression
that will survive the iteration may justify one focused test. An explicit user
request for no validation skips the sanity check.

Before claiming a change complete, answer:

1. Does the requested behavior exist on the current revision?
2. Is the capability owned by the correct component?
3. Were unrelated user changes preserved?
4. Was the integrated candidate self-reviewed and frozen before independent
   verification or project-wide validation?
5. If a verifier found blockers, were fixes checked through targeted closure
   rather than restarting an unchanged full review?
6. What plausible failure or observable contract needed proof? Did an existing
   check already cover it, or can the new proof fail independently of the
   implementation being tested?
7. Which commands ran, and what did each prove? Was an inherited narrower
   profile needlessly run immediately before its broader profile?
8. Which current evidence receipt records the revision, dirty state, and
   results?
9. Which relevant validation did not run?
10. Did documentation or current state change durably?
11. Is any required work still pending?

If required work remains, report progress rather than completion.

## Evidence ladder

Iteration mode uses at most the first applicable rung. A user-requested
checkpoint, review, or release may move higher.

Use the lowest sufficient rung, then move upward with risk:

1. static or schema validation;
2. focused unit or contract test;
3. component integration test;
4. real workflow or runtime test;
5. broad project gate;
6. human visual or experiential acceptance.

Use only the rungs the risk requires. A new test needs a failure hypothesis and
an independent observable outcome; code that merely repeats the implementation
assumption is confirmation, not evidence. Prefer extending an existing focused
or table-driven test and remove superseded coverage. Test count and coverage
percentage are not outcomes.

Evidence v2 hashes the tracked diff and untracked file contents. Validation
must leave the tested project and supplied visual artifacts unchanged; a
mutating guard produces a failed receipt.

For configured visual routes, compile and test commands are incomplete
evidence. The verification receipt must also contain current rendered
artifacts, their hashes, concrete inspection checks, and a passing visual
verdict.
