# Project Agent Toolkit

A project-neutral Codex plugin for keeping repository agent instructions
small, task-scoped, testable, and easy to resume.

## Install in Codex

Add this GitHub repository as a marketplace, then install the plugin:

```console
codex plugin marketplace add velimir-jankovic/project-agent-toolkit
codex plugin add project-agent-toolkit@project-agent-toolkit
```

Start a new Codex task after installation so all six skills are loaded.

It separates two things that often become tangled:

- reusable process: authority, task routing, planning, implementation,
  verification, review, and handoff;
- project policy: the architecture, constraints, domains, commands, and
  acceptance gates that belong to one repository.

The plugin never assumes a language, framework, product, model, or directory
layout. Projects describe their own policy in `.agent-governance.json`.

## Included skills

- `project-agent-bootstrap` creates or adopts the governance surface.
- `project-agent-audit` finds bloated context, broken authority, stale links,
  duplicated policy, and tooling-directory pollution.
- `governed-project-change` routes a task to only the relevant policy and
  requires proportionate evidence.
- `mcp-driven-development` defines an optional semantic MCP control surface
  over project-owned public APIs, enabled by one explicit flag and disabled by
  default.
- `visual-change-verification` requires fresh rendered artifacts and an
  explicit review for UI, drawing, modeling, animation, VFX, scene, map, and
  other appearance-dependent work.
- `project-agent-handoff` creates compact, honest resume checkpoints.

## CLI

```console
python plugins/project-agent-toolkit/scripts/governance.py init --root C:\path\to\project
python plugins/project-agent-toolkit/scripts/governance.py audit --root C:\path\to\project
python plugins/project-agent-toolkit/scripts/governance.py route --root C:\path\to\project --task "change API" --path src/api/client.py
python plugins/project-agent-toolkit/scripts/governance.py check --root C:\path\to\project
python plugins/project-agent-toolkit/scripts/governance.py generate --root C:\path\to\project
python plugins/project-agent-toolkit/scripts/governance.py route-test --root C:\path\to\project
python plugins/project-agent-toolkit/scripts/governance.py coverage --root C:\path\to\project --strict
python plugins/project-agent-toolkit/scripts/governance.py verify --root C:\path\to\project --task "change API" --claim "API contract is valid"
python plugins/project-agent-toolkit/scripts/governance.py upgrade --root C:\path\to\project
```

`init` is additive by default and never overwrites an existing file. Use
`--profile full` to include generic role and prompt templates. Use `--force`
only after reviewing the diff. Bootstrap also adds `.agent-evidence/` to
`.gitignore` without removing existing ignore rules. Before `verify` can pass,
configure at least one real project-owned command in a routed validation
profile; `audit` reports empty routed profiles explicitly.
Receipt creation is rejected in a Git worktree when the configured evidence
directory is not ignored, so recording evidence cannot invalidate the source
state it claims to verify.

`generate` keeps platform-facing agent adapters synchronized with one canonical
configuration. It checks by default; `--write` updates only managed files, and
`--force` is required to adopt an unmanaged existing file.

`verify` selects validation profiles through the same task routes used for
policy, runs project-owned commands, and writes a receipt containing the
configuration digest, version-control revision and dirty state, commands,
results, durations, proof statements, and output hashes.

For configured visual routes, it additionally requires one or more rendered
artifacts plus an explicit review:

```console
python plugins/project-agent-toolkit/scripts/governance.py verify --root C:\path\to\project --task "fix UI layout" --visual-artifact artifacts/ui.png --visual-surface "Actual application window at 1280x720" --visual-check "No clipping at the target viewport" --visual-verdict pass
```

Visual artifacts must be structurally valid, recent image/video containers.
Receipts record format, dimensions when available, timestamps, hashes,
acceptance-surface metadata, references, and concrete checks. The reviewer
still owns aesthetic judgment; the guard prevents missing, malformed, stale,
or anonymous evidence from being presented as verified.

Validation commands are trusted repository configuration and run through the
host platform shell. Review changes to `.agent-governance.json` with the same
care as changes to CI or hook configuration.

`upgrade` prints a non-destructive migration preview by default. `--write`
atomically upgrades only `.agent-governance.json`.

## Guards

The repository has one authoritative, dependency-free quality gate:

```console
python scripts/quality.py
```

It compiles the Python tooling, validates plugin and skill structure, runs the
strict governance audit, and runs the test suite. GitHub Actions runs the same
command. Local hooks are opt-in:

```console
python scripts/install_hooks.py
```

The generated project governance is also guard-driven: `governance.py check`
fails on broken authority paths, invalid routes, missing links, duplicate
long-form policy, excess always-loaded context, and unexpected runtime files in
agent tooling directories. It also fails on stale generated adapters, broken
route contracts, invalid validation graphs, unknown rule guards, and malformed
evidence configuration. `coverage --strict` additionally rejects unrouted
authorities, untested routes, unused validation profiles, and unguarded
registered rules.

All executable toolkit logic uses Python 3 and only the standard library. There
are no Node.js, PowerShell, Bash, pip, or third-party runtime dependencies.
GitHub Actions YAML and plugin manifests remain declarative configuration.

## Design rules

- Entrypoints are short indexes, not policy warehouses.
- One document owns each durable rule.
- Task routes use progressive disclosure.
- Model selection is environment policy, not repository architecture.
- Validation commands are project data.
- Validation starts from a plausible failure and uses the least expensive check
  that can falsify it; test count and coverage percentage are not goals.
- Simplicity and maintenance cost are part of correctness.
- Generated adapters have one source of truth.
- Route behavior is contract-tested with representative tasks.
- Validation claims are revision-bound evidence, not remembered terminal output.
- Dirty-tree receipts hash tracked diffs and untracked file contents, and fail
  when validation mutates the tested source state.
- MCP development surfaces are optional adapters, not runtime authority, and
  remain off unless their one declared activation flag is present. MCP
  declarations require executable disabled, enabled, parity, lifecycle,
  performance, and—when production activation is forbidden—release proofs.
- Visual changes require current render evidence and a concrete visual verdict;
  compilation and unit tests alone are insufficient.
- "Done" means the requested outcome exists and current evidence supports it.
- Agent communication is concise and outcome-first, not a transcript of routine
  work or a dump of validation logs.
- Handoffs preserve decisions and next actions, not chat transcripts.

See [governance-schema.md](plugins/project-agent-toolkit/skills/project-agent-audit/references/governance-schema.md)
for the configuration contract.
