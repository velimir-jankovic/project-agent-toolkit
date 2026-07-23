# Governance configuration

`.agent-governance.json` is project data consumed by the toolkit. Schema
version `3` is current.

## Top level

- `version`: schema version.
- `project.name`: display name used by generated adapters.
- `entrypoints`: concise files automatically or conventionally read by agents.
- `adapters.outputs`: generated platform-facing files.
- `authorities`: canonical project documents.
- `routes`: task/path routing to authorities and validation profiles.
- `route_tests`: deterministic routing contracts.
- `rules`: registered durable rules and their guards.
- `development_interfaces`: optional development-only control surfaces,
  including MCP activation and production policy.
- `limits`: context and duplication budgets.
- `tooling`: configuration roots and files allowed inside them.
- `validation`: named, composable validation profiles.
- `evidence.directory`: ignored directory for revision-bound receipts.

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

Terms are case-insensitive substrings of the task. Paths are
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

`verify` writes `project-agent-toolkit.evidence.v1` receipts. They include the
governance-file digest, UTC timestamp, version-control revision and dirty-state
digest when Git is available, routing result, selected profiles, claims,
commands, proof statements, exit codes, durations, and stdout/stderr hashes.
Command output itself is not persisted.

## Development interface

```json
{
  "id": "editor-mcp",
  "protocol": "mcp",
  "activation_flag": "--enable-editor-mcp",
  "default_enabled": false,
  "production_allowed": false,
  "guard_profiles": ["focused", "release"]
}
```

The activation flag is the single switch that starts the surface.
`default_enabled` must be false. `guard_profiles` name project-owned checks
that prove enabled behavior, disabled behavior, and—when
`production_allowed` is false—release exclusion. The toolkit validates the
declaration; those project checks validate the executable.

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
