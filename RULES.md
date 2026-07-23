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
