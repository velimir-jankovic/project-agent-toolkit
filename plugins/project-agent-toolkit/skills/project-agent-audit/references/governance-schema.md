# Governance configuration

`.agent-governance.json` is project data consumed by the toolkit. Schema
version `4` is current.

## Top level

- `version`: schema version.
- `project.name`: display name used by generated adapters.
- `entrypoints`: concise files automatically or conventionally read by agents.
- `adapters.outputs`: generated platform-facing files.
- `authorities`: canonical project documents.
- `routes`: task/path routing to authorities and validation profiles.
- `route_tests`: deterministic routing contracts.
- `capabilities`: optional task/path routing to concise implementation owners.
- `capability_tests`: deterministic capability ownership contracts.
- `capability_coverage`: optional changed-path scope that rejects uncategorized
  implementation changes.
- `rules`: registered durable rules and their guards.
- `development_interfaces`: optional development-only control surfaces,
  including MCP activation and production policy.
- `visual_validation`: routes that require rendered artifact and review
  evidence.
- `limits`: context and duplication budgets.
- `tooling`: configuration roots and files allowed inside them.
- `validation`: named, composable validation profiles.
- `evidence.directory`: Git-ignored directory for revision-bound receipts.
  Audit and receipt creation reject a non-ignored directory inside a Git
  worktree because writing the receipt would mutate the validated state.

## Authority

```json
{
  "id": "architecture",
  "path": "docs/ARCHITECTURE.md",
  "purpose": "Stable system ownership",
  "always": false
}
```

`id` is referenced by routes. `always` should be rare. A document may be
important without being needed for every task.

## Route

```json
{
  "id": "data-model",
  "terms": ["schema", "migration"],
  "paths": ["src/data/**", "migrations/**"],
  "read": ["architecture", "rules", "data-policy", "state"],
  "validation": ["focused"]
}
```

Terms are case-insensitive whole words or phrases in the task. Paths are
repository-relative globs. All matching non-default routes are combined. When
none match, the route named `default` is used.

## Route test

```json
{
  "id": "schema-change",
  "task": "change the persisted schema",
  "paths": ["src/data/model.py"],
  "expect_routes": ["data-model"],
  "expect_documents": ["RULES.md", "docs/ARCHITECTURE.md"],
  "expect_validation_profiles": ["focused"]
}
```

Order is contractual because it is the reading order presented to agents.

## Capability map

Policy routes answer which rules apply. Capability entries separately answer
which small set of implementation files owns the requested behavior:

```json
{
  "id": "drafting",
  "purpose": "Author legal draft transitions.",
  "terms": ["draft", "reroll"],
  "paths": ["src/draft/**"],
  "owners": ["src/draft/system.py", "src/draft/types.py"],
  "depends_on": ["build-resolution"]
}
```

`governance.py context` returns routed authorities, validation profiles, direct
capability matches, their transitive dependencies, and de-duplicated owner
paths. Owner paths must exist and remain within the project. The configured
`limits.capability_owner_max_count` warns when one capability stops being a
useful low-context starting point. Agents begin with direct owners and inspect
dependency owners only when the task crosses that declared boundary.

Capability tests keep project-specific ownership maps from silently drifting:

```json
{
  "id": "draft-context",
  "task": "add a draft choice",
  "paths": ["src/draft/system.py"],
  "expect_capabilities": ["drafting", "build-resolution"],
  "expect_owners": [
    "src/draft/system.py",
    "src/draft/types.py",
    "src/build/resolver.py"
  ]
}
```

When several capability path globs match, the longest literal prefix wins.
This lets a broad subsystem capability cover new files while a more specific
feature capability remains the direct starting point.

The optional changed-path guard makes declared ownership mechanically
maintainable:

```json
{
  "capability_coverage": {
    "include": ["src/**", "scripts/**"],
    "exclude": ["src/generated/**"]
  }
}
```

Run it against local work, explicit paths, or a branch diff:

```console
governance.py capability-check --root . --changed
governance.py capability-check --root . --base origin/main --changed
governance.py capability-check --root . --path src/new_feature.py
```

Every changed path inside `include` and outside `exclude` must match at least
one capability path or exact owner. The command reports the most-specific
direct owner and fails on gaps. CI should pass its merge-base revision through
`--base`; local hooks and agents use `--changed`. This guarantees that scoped
changes remain categorized, while owner existence and capability tests guard
the declared map. It cannot infer that a file's semantic responsibility
changed without its path changing, so review still owns that judgment.

The map is not an exhaustive call graph and does not replace code inspection.
It is a bounded starting surface that prevents every task from rediscovering
subsystem ownership through broad repository reads.

## Generated adapter

```json
{
  "adapters": {
    "outputs": [
      {"kind": "agents", "path": "AGENTS.md"},
      {"kind": "copilot", "path": ".github/copilot-instructions.md"}
    ]
  }
}
```

Generated files carry a marker. The toolkit refuses to overwrite an unmanaged
file unless `generate --write --force` is explicitly used.

## Validation

```json
{
  "validation": {
    "default_profiles": ["fast"],
    "profiles": {
      "fast": {
        "commands": [
          {
            "run": "python scripts/check.py",
            "proves": "Static project invariants hold"
          }
        ]
      },
      "focused": {
        "extends": ["fast"],
        "commands": [
          {
            "run": "python -m unittest",
            "proves": "Focused behavioral contracts pass"
          }
        ]
      }
    }
  }
}
```

Profiles form an acyclic graph. Commands are de-duplicated in expansion order.
Every command should state what it proves.

## Rule registry

```json
{
  "id": "public-contract-compatibility",
  "authority": "rules",
  "source": "RULES.md#compatibility",
  "guard": "focused"
}
```

The guard is a validation profile. Coverage reports registered rules without a
guard; it cannot infer unregistered prose rules semantically.

## Evidence

`verify` writes `project-agent-toolkit.evidence.v2` receipts. They include the
governance-file digest, UTC timestamp, version-control revision, tracked diff
and untracked-content digest when Git is available, routing result, selected
profiles, claims, commands, proof statements, exit codes, durations, and
stdout/stderr hashes. Pre/post state is compared and a guard that mutates the
tested source or visual artifacts cannot pass. Command output itself is not
persisted.

## Development interface

```json
{
  "id": "editor-mcp",
  "protocol": "mcp",
  "activation_flag": "--enable-editor-mcp",
  "default_enabled": false,
  "production_allowed": false,
  "guard_profiles": {
    "disabled": ["mcp-disabled"],
    "enabled": ["mcp-enabled"],
    "parity": ["mcp-parity"],
    "lifecycle": ["mcp-lifecycle"],
    "performance": ["mcp-performance"],
    "release": ["mcp-release"]
  }
}
```

The activation flag is the single switch that starts the surface.
`default_enabled` must be false. Every required `guard_profiles` category must
name profiles that expand to executable commands. `release` is mandatory when
`production_allowed` is false, and each category needs a matching command
`proves` statement. The toolkit validates the declaration; those project checks
validate the executable.

## Visual validation

```json
{
  "visual_validation": {
    "routes": ["visual"],
    "artifact_min_count": 1,
    "min_review_checks": 1,
    "artifact_max_age_seconds": 3600,
    "require_review": true,
    "require_surface": true
  }
}
```

When any configured route matches, `verify` refuses to run without the minimum
number of project-relative, structurally valid, recent image/video artifacts,
a named actual acceptance surface, a `pass` verdict, and the configured number
of concrete `--visual-check` values. Artifact paths, formats, dimensions when
available, timestamps, sizes, and hashes are stored in the content-bound
evidence receipt.

## Limits and tooling

- `entrypoint_max_lines`: per-entrypoint warning threshold.
- `always_loaded_max_chars`: combined byte budget for entrypoints and
  authorities with `always: true`.
- `duplicate_paragraph_min_chars`: normalized paragraph size used by duplicate
  policy detection.
- `tooling.roots`: directories to inspect for configuration pollution.
- `tooling.allowed`: project-relative configuration-file globs.

Tool configuration directories should not contain virtual environments,
certificates, caches, databases, downloads, or logs.

The audit also inspects project-scoped `.codex/config.toml` and
`.codex/agents/*.toml` when present. Role files must be valid TOML with
non-empty `name`, `description`, and `developer_instructions` fields. Audit
metrics report role names plus explicit model and reasoning override counts;
zero overrides means those roles inherit environment policy.
