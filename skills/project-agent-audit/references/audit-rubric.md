# Agent setup audit rubric

## Authority

- Can an agent tell which document wins?
- Does current state ever override a stable contract accidentally?
- Does each durable rule have one owner?

## Context

- Are entrypoints indexes or warehouses?
- Are unrelated domains always loaded?
- Are historical receipts mixed with live instructions?
- Can a task obtain all required policy from deterministic routes?

## Enforcement

- Which repeated failures are still prose-only?
- Are guards focused, fast, and named after the invariant?
- Do hooks fail safely and does CI run the authoritative gate?
- Are exceptions structured, justified, and bounded?
- Does every non-default route have a representative contract test?
- Does every registered rule name a validation profile?
- Are validation profiles invoked by a route, default, or rule?
- Are generated adapters current with their canonical configuration?

## Roles

- Are analysis, implementation, verification, and visual review separated when
  useful?
- Does the root retain integration and completion ownership?
- Are role semantics independent of a specific model?

## State

- Can work resume without chat?
- Does the checkpoint distinguish delivered, verified, blocked, and next?
- Is transient output kept out of canonical policy?
- Is validation evidence tied to the tested revision and dirty state?

## Tooling hygiene

- Is configuration mixed with runtime data?
- Are secrets, certificates, caches, environments, or binaries living under an
  agent configuration directory?
- Can a clean clone reconstruct the setup?

## Severity

- Error: authority cannot be followed or a configured contract is broken.
- Warning: reliability or context cost is materially degraded.
- Note: improvement with no current correctness impact.
