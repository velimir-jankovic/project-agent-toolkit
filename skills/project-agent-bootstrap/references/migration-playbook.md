# Migration playbook

## Mature repository

Treat existing policy as user data.

1. Inventory all instruction, role, prompt, plan, handoff, hook, and guard
   surfaces.
2. Identify the canonical owner of every durable rule.
3. Mark exact duplicates, paraphrased duplicates, contradictions, historical
   receipts, and temporary state.
4. Create task routes before shrinking entrypoints.
5. Move unique policy to its owner; do not delete it merely because it is
   verbose.
6. Replace copied text with links.
7. Convert repeat failures into focused checks.
8. Test representative routing before removing the old always-loaded path.

## Authority pattern

Use this default precedence unless the project defines a stronger one:

1. current user request;
2. non-negotiable project rules;
3. architecture and public contracts;
4. workflow;
5. active state and plans;
6. historical notes.

State and history explain; they do not silently override architecture.

## Safe adoption

- Additive bootstrap first.
- Audit next.
- Refactor one authority boundary at a time.
- Keep a version-control diff that makes lost policy visible.
- Run both generic governance checks and existing project gates.
