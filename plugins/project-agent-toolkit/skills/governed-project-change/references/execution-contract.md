# Completion contract

Before claiming a change complete, answer:

1. Does the requested behavior exist on the current revision?
2. Is the capability owned by the correct component?
3. Were unrelated user changes preserved?
4. Is there a focused regression proof for the failure or contract changed?
5. Which commands ran, and what did each prove?
6. Which current evidence receipt records the revision, dirty state, and
   results?
7. Which relevant validation did not run?
8. Did documentation or current state change durably?
9. Is any required work still pending?

If required work remains, report progress rather than completion.

## Evidence ladder

Use the lowest sufficient rung, then move upward with risk:

1. static or schema validation;
2. focused unit or contract test;
3. component integration test;
4. real workflow or runtime test;
5. broad project gate;
6. human visual or experiential acceptance.

Higher rungs do not excuse missing focused regression coverage.
