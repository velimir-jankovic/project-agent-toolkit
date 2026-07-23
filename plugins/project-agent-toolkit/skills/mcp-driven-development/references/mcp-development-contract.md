# MCP development contract

## Architecture

- The application or engine public API owns behavior.
- MCP translates protocol requests into that API.
- UI, tests, scripts, and MCP may share the API; none should bypass its
  validation or authority boundaries.
- Simulation, document, and persistence authority remain in their normal
  owners. The MCP server is never authoritative state.

## Activation and production safety

- One documented flag is the only activation path.
- The default is disabled in every environment.
- Disabled means no bind, listener, advertised tool, background worker,
  polling, or measurable per-frame work.
- Prefer compiling the adapter out of production artifacts when practical.
- If it remains compiled in, a release guard must prove the flag is rejected
  or ignored when `production_allowed` is false.
- Stdio and loopback transports are development-safe defaults. Non-local
  transports require authentication, authorization, rate limits, auditability,
  and an explicit threat model.

## Tool design

- Expose capabilities and schema versions through introspection.
- Address objects with stable semantic IDs, not labels or screen positions.
- Separate reads, previews, mutations, and irreversible operations.
- Return typed results and actionable error codes.
- Make mutation batches atomic when partial application would corrupt state.
- Support undo or compensating commands for authoring workflows.
- Prefer idempotent commands and client-provided request IDs.
- Expose bounded pagination, filtering, and search for large object graphs.
- Publish state revisions so clients can detect stale reads and edits.

## Human and agent usability

- A human should be able to discover the same nouns and operations in the
  product UI or documentation.
- Tool names use domain language rather than implementation details.
- Avoid giant catch-all JSON mutation tools.
- Provide representative recipes for inspect, create, modify, save, validate,
  and recover.
- When an MCP task reveals a missing public capability, add that capability
  instead of automating mouse coordinates or editing authoritative artifacts
  behind the application's back.

## Required evidence

1. Disabled-mode test: start normally and prove no MCP surface exists.
2. Enabled-mode test: start with the declared flag, discover tools, and perform
   representative reads and writes.
3. Parity test: call the underlying public API and MCP path with equivalent
   input and compare observable results.
4. Lifecycle test: repeated start/stop and application shutdown leak no
   listener, worker, or process.
5. Release test: when production is forbidden, prove a release artifact cannot
   activate the surface.
6. Performance test: disabled mode has no material steady-state cost.

Declare those proofs explicitly:

```json
{
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

`release` is required when `production_allowed` is false. Every referenced
profile must expand to at least one executable project-owned command, and at
least one command's `proves` statement must explicitly name its proof category.
