# Project Agent Toolkit rules

- The plugin is project-neutral: no language, framework, product, repository,
  model, or vendor workflow is required by generated policy.
- Templates never select a model. Roles describe responsibility and inherit the
  user's environment policy.
- Bootstrap is additive by default. Existing project files are not overwritten
  without explicit `--force`.
- One canonical document owns each durable rule; entrypoints and prompts link.
- Always-loaded context stays within `.agent-governance.json` limits.
- Every configuration path and route is validated mechanically.
- Changes pass `python scripts/quality.py` before completion is claimed.
- Simplicity, cognitive load, and maintenance cost are acceptance criteria.
  Prefer existing mechanisms and remove duplication over adding speculative
  abstractions.
- Add or change a test only when it can falsify a named plausible failure or
  protect an observable contract not already proved by a cheaper check. Do not
  mirror implementation, assert trivial details, duplicate coverage, or treat
  test count and coverage percentage as outcomes.
- When work is expected to iterate, self-review the coherent slice and run at
  most one cheapest relevant sanity check. Do not add tests for volatile
  details, stack validation commands, invoke an independent verifier, or run a
  full gate. A new test is justified only for a stable contract or regression
  expected to survive the iteration. An explicit user request for no
  validation skips even the sanity check.
- A check that did not run is not reported as evidence.
- Evidence receipts identify dirty source contents, not only dirty filenames,
  and validation that mutates the tested source state cannot pass.
- MCP development surfaces are thin adapters over public project APIs, use one
  explicit activation flag, default to disabled, and require executable
  disabled, enabled, parity, lifecycle, performance, and applicable release
  guards.
- Visual work is complete only after the actual acceptance surface is rendered,
  captured recently in structurally valid artifacts, inspected against
  specific checks, and recorded as content-bound evidence.
- Communication is outcome-first and concise. Report material decisions,
  blockers, risks, and evidence; omit play-by-play narration, repeated
  summaries, raw logs, and exhaustive file lists unless requested.
