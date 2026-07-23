# Project workflow

## Start

1. Read the concise agent entrypoint.
2. Route the task with `.agent-governance.json`.
3. Inspect repository state and relevant implementation.
4. State assumptions that materially affect the result.

## Change

1. Diagnose before selecting a fix.
2. Decide ownership before placing code or policy.
3. Make one coherent bounded change.
4. Add or update the narrowest regression proof.

## Verify

Run checks in increasing cost order: focused static checks, focused tests,
integration checks, then broader gates when risk warrants them. A check that
was not run is not evidence.

## Handoff

Update `PROGRESS.md` with the current objective, delivered behavior, unresolved
risks, exact evidence, dirty-worktree state, and one next action. Do not copy a
chat transcript.
