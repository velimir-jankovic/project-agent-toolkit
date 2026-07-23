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
as project governance data. MCP declarations map each required proof category
to non-empty project validation profiles. The target project owns the public
API, adapter implementation, and runtime proofs.

The toolkit's deterministic guard runner is Python standard-library code.
Individual projects own the commands it invokes, so a guard may be JavaScript,
Python, a native executable, an engine test, or another repository-native
tool. Visual routes add a separate evidence gate requiring rendered artifacts
and recorded inspection in addition to those commands. Evidence v2 snapshots
the revision, tracked diff, untracked contents, governance configuration, and
visual hashes before validation, then rejects source or artifact mutation
during the guard run.
