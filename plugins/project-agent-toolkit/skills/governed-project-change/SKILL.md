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

6. Make the smallest coherent change. Prefer existing mechanisms, remove
   duplication, and treat maintenance cost as part of correctness. Preserve
   unrelated edits.
7. Before independent review or project-wide validation, the root integrates
   every accepted slice, resolves overlaps and TODOs, and self-reviews the
   current diff against ownership and acceptance criteria. Treat that state as
   the candidate freeze. Delegated workers run only explicitly assigned
   focused checks; the root owns shared routed validation.
8. When independent verification is warranted or requested, give the verifier
   the frozen candidate and its acceptance criteria. Resolve findings under
   root ownership, then request targeted closure of those findings. Repeat the
   complete review only when a fix changes the architecture, public boundary,
   or acceptance surface.
9. Validate through routed profiles:

   ```console
   python <plugin-root>/scripts/governance.py verify \
     --root <project-root> \
     --task "<user request>" \
     --path <changed path> \
     --claim "<claim being proved>"
   ```

   First name the plausible failure or observable contract. Add or change a
   test only when it can falsify that failure and no cheaper existing check
   already proves the claim. Prefer extending a focused or table-driven test;
   do not mirror implementation, assert trivial details, duplicate coverage,
   or optimize for test count. For a bug fix, show the regression against
   pre-fix behavior when practical. Never substitute a mock for the requested
   real workflow.
   When a configured visual route matches, use
   `$visual-change-verification`; the verification command requires rendered
   artifacts and an explicit review.
   Do not run a narrower profile immediately before a broader profile that
   extends it on the same source. Run the broader profile once after the
   candidate freeze unless the narrower result is needed to guide ongoing
   implementation.
10. Update canonical state only when the durable objective, decision, or next
   action changed.
11. Before claiming completion, use
   [execution-contract.md](references/execution-contract.md) and cite the
   current evidence receipt.

## Delegation

Delegate only a concrete, bounded subtask that can run independently. The root
agent owns architecture, integration, final verification, and the completion
claim. Inputs from architects and explorers that can change the plan must be
resolved before candidate freeze. A worker self-reviews its own diff and runs
only assigned focused checks before returning integration notes; it does not
spend the repository-wide validation budget. A role name describes
responsibility; it does not justify a particular model or reasoning setting.

## Communication

Lead with the outcome. Send intermediate updates only for a material decision,
result, blocker, or risk. Keep the completion report to the change, evidence,
and unresolved work; omit routine narration, repeated summaries, raw logs, and
exhaustive file lists unless requested.
