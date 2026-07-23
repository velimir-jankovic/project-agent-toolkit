# Architecture

The repository has four independent layers:

1. A Git-backed Codex marketplace catalog under `.agents/plugins/`.
2. The distributable plugin under `plugins/project-agent-toolkit/`, including
   metadata, skills, project-neutral templates, and the dependency-free
   governance CLI.
3. Repository development guards under `scripts/` and regression tests under
   `tests/`.
4. This repository's own governed policy and generated agent adapters.

Skills define agent behavior. The CLI owns deterministic enforcement. Templates
are data copied additively into a project. A target project's
`.agent-governance.json` owns its authority graph, routes, budgets, tooling
allowlist, and optional validation commands.

No target project imports this repository as runtime application code.
Marketplace installation supplies skills and their packaged CLI; contributors
can also invoke that CLI directly from the source tree.

Optional development interfaces, including MCP control surfaces, are declared
as project governance data. The toolkit validates their activation and guard
contracts; the target project owns the public API, adapter implementation, and
runtime proofs.
