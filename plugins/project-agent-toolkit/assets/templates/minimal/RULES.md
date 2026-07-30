# Project rules

Keep only non-negotiable, mechanically meaningful project constraints here.
Prefer one existing mechanical check for a rule when it can be enforced
reliably; do not multiply guards for the same invariant.

## Change discipline

- Preserve unrelated work.
- Do not bypass validation or hooks to make a change appear complete.
- Do not hide missing shared capability in a consumer-local workaround.
- Prefer the simplest maintainable change that uses existing mechanisms.
- Add or change a test only when it can falsify a plausible failure or protect
  an observable contract not already proved by a cheaper check. Do not mirror
  implementation, test trivial details, duplicate coverage, or optimize for
  test count.
- When work is expected to iterate, self-review the coherent slice and run at
  most one cheapest relevant sanity check. Do not add tests for volatile
  details, stack validation commands, invoke an independent verifier, or run a
  full gate. A new test is justified only for a stable contract or regression
  expected to survive the iteration. An explicit user request for no
  validation skips even the sanity check.
- Do not claim evidence that was not produced from the current source contents.
- Visual work requires fresh rendered evidence from the actual acceptance
  surface and concrete inspection checks.
- Keep status and completion reports concise and outcome-first. Omit
  play-by-play narration and raw logs unless requested.

## Repository-specific rules

Add the project's actual constraints here. Give each rule one canonical home
and link to it elsewhere instead of copying it.
