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
4. Name the plausible failure before adding a test. Prefer an existing check or
   extend one focused test; add nothing when cheaper evidence already proves
   the contract.

## Integrate

Before independent review or project-wide validation, the root integrates all
accepted slices, resolves overlaps and TODOs, and self-reviews the current diff
against ownership and acceptance criteria. Treat that state as the candidate
freeze. Delegated workers run only explicitly assigned focused local checks.
If a verifier finds blockers, fix them under root ownership and request
targeted closure; repeat the full review only when the acceptance surface
changes.

## Verify

Run the least expensive checks capable of disproving the claim: focused static
checks, focused tests, integration checks, then broader gates only when risk
warrants them. For a bug fix, prove the regression against pre-fix behavior
when practical. Test count and coverage percentage are not outcomes. A check
that was not run is not evidence. Configure at least one project-owned command
in a routed validation profile before using `verify`; bootstrap profiles are
empty by design.

Validation profiles are cumulative. Do not run a narrower profile immediately
before a broader profile that extends it on the same source; run the broader
profile once after candidate freeze unless the narrower result is needed to
guide ongoing implementation.

## Handoff

Update `PROGRESS.md` with the current objective, delivered behavior, unresolved
risks, exact evidence, dirty-worktree state, and one next action. Do not copy a
chat transcript.

## Communicate

Lead with the outcome. Report only material decisions, results, blockers,
risks, and evidence. Do not narrate routine steps or paste logs unless asked.
