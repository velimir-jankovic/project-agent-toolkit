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

## Iterate

Treat work the user identifies as exploratory, prototypical, or expected to
change repeatedly as iteration mode. Make the coherent implementation change,
self-review the affected code, then run at most one cheapest relevant sanity
check such as a parser, static check, or affected-target compile. Do not stack
checks or run a routed profile that expands beyond this budget.

Do not add tests for values, layout, presentation, tuning, or other volatile
details. Add a test without prompting only when it protects a stable contract
or regression expected to survive the current iteration and cheaper evidence
cannot cover it. Do not invoke an independent verifier, broad suite, runtime
capture, or checkpoint autonomously.

An explicit user request for no validation skips the sanity check. Leave
iteration mode when the user requests a particular check, checkpoint, review,
or release gate.

## Checkpoint

At an explicit checkpoint, run focused tests for stable contracts, use one
independent review when it can expose meaningful integration risk, and exercise
the real workflow when acceptance depends on it. Do not create broad tests for
volatile behavior merely to increase checkpoint evidence.

## Integrate

Before independent review or project-wide validation, the root integrates all
accepted slices, resolves overlaps and TODOs, and self-reviews the current diff
against ownership and acceptance criteria. Treat that state as the candidate
freeze. Delegated workers run only explicitly assigned focused local checks.
If a verifier finds blockers, fix them under root ownership and request
targeted closure; repeat the full review only when the acceptance surface
changes.

## Verify

Outside iteration mode, run the least expensive checks capable of disproving
the claim: focused static checks, focused tests, integration checks, then
broader gates only when risk warrants them. For a bug fix, prove the regression
against pre-fix behavior when practical. Test count and coverage percentage are
not outcomes. A check that was not run is not evidence. Configure at least one
project-owned command in a routed validation profile before using `verify`;
bootstrap profiles are empty by design.

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
