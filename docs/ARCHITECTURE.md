# Architecture

The repository has three independent layers:

1. Codex plugin metadata and skills under `.codex-plugin/` and `skills/`.
2. Project-neutral templates under `assets/templates/`.
3. A dependency-free CLI under `scripts/` that initializes, routes, audits, and
   checks a target repository.

Skills define agent behavior. The CLI owns deterministic enforcement. Templates
are data copied additively into a project. A target project's
`.agent-governance.json` owns its authority graph, routes, budgets, tooling
allowlist, and optional validation commands.

No target project imports this repository as runtime application code. Plugin
installation supplies skills; the CLI can also be used directly.
