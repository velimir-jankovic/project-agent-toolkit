---
name: mcp-driven-development
description: Design, implement, or verify an optional MCP development surface over a project's public APIs, with semantic tool control, deterministic inspection, and a single explicit activation flag that is disabled by default and guardable in production. Use for editor automation, agent-driven QA, MCP servers, tool-driven authoring, or development-only control planes.
---

# MCP-Driven Development

Treat MCP as a development adapter over a real application API, not as an
alternate source of truth.

## Workflow

1. Read the routed architecture, rules, workflow, and validation authorities.
2. Identify the public API that owns the capability. Add or improve that API
   before exposing private UI or runtime internals through MCP.
3. Register the surface in `.agent-governance.json` under
   `development_interfaces`. Map each required proof category to one or more
   non-empty project validation profiles; profile names without executable
   checks are rejected.
4. Use exactly one explicit activation flag. The disabled path is the default
   and must start no server, listener, worker, polling loop, or tool registry.
5. Keep transport local by default: stdio or loopback. Remote exposure requires
   a separate security design and explicit project authority.
6. Prefer semantic IDs, typed commands, capability discovery, deterministic
   state snapshots, transactions, and structured errors over screen
   coordinates or mouse automation.
7. Exercise the same public API from tests and MCP. Do not implement behavior
   only inside the MCP adapter.
8. Verify both modes:

   - without the flag, the MCP surface is absent and ordinary behavior is
     unchanged;
   - with the flag, tools are discoverable and representative read/write
     workflows succeed;
   - when production use is forbidden, the release guard proves the surface
     cannot become active.

9. Use [mcp-development-contract.md](references/mcp-development-contract.md)
   for design and acceptance checks.

## Project configuration

Declare the exact switch rather than relying on convention:

```json
{
  "development_interfaces": [
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
  ]
}
```

The toolkit requires executable guards for every category. `release` is
required when production activation is forbidden. Project-owned guards prove
the runtime actually honors the declaration.
