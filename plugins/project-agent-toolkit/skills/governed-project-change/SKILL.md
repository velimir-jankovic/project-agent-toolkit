---
name: governed-project-change
description: Execute a repository change using task-scoped policy, explicit capability ownership, proportionate validation, and honest completion evidence. Use when a project has `.agent-governance.json`, when the user asks to follow the repository AI workflow, or when an implementation must avoid loading unrelated policy and avoid consumer-local workarounds.
---

# Governed Project Change

Use repository governance as a router and constraint system, not as a substitute
for understanding the code.

## Workflow

1. Read the concise agent entrypoint and inspect version-control state.
2. Route the request:

   ```console
   python <plugin-root>/scripts/governance.py route \
     --root <project-root> \
     --task "<user request>" \
     --path <likely changed path>
   ```

3. Read every returned authority completely. Read additional implementation
   files only as the task requires.
4. Classify the request: answer, diagnose, design, implement, review, or
   monitor. Do not infer authorization for a materially different action.
5. For a change, decide capability ownership before editing:

   - shared capability belongs to the shared owner;
   - product or policy behavior belongs to the consumer;
   - compatibility shims need an explicit boundary and removal condition.

6. Make the smallest coherent change. Preserve unrelated edits.
7. Validate through routed profiles:

   ```console
   python <plugin-root>/scripts/governance.py verify \
     --root <project-root> \
     --task "<user request>" \
     --path <changed path> \
     --claim "<claim being proved>"
   ```

   Prefer a focused regression proof before a broad gate. Never substitute a
   mock for the requested real workflow.
   When a configured visual route matches, use
   `$visual-change-verification`; the verification command requires rendered
   artifacts and an explicit review.
8. Update canonical state only when the durable objective, decision, or next
   action changed.
9. Before claiming completion, use
   [execution-contract.md](references/execution-contract.md) and cite the
   current evidence receipt.

## Delegation

Delegate only a concrete, bounded subtask that can run independently. The root
agent owns architecture, integration, final verification, and the completion
claim. A role name describes responsibility; it does not justify a particular
model or reasoning setting.
