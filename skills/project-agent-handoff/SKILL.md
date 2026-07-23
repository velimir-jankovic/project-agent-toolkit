---
name: project-agent-handoff
description: Create, refresh, or consume a compact project checkpoint for context resets, session handoffs, interrupted work, or resuming a repository task. Use when progress must survive another agent or session without copying chat history or overstating validation.
---

# Project Agent Handoff

Preserve enough verified state to resume in minutes, not a transcript of how the
session felt.

## Create or refresh

1. Read the task-routed authorities and current progress document.
2. Inspect version-control status, recent relevant commits, and current
   validation evidence.
3. Use [checkpoint-format.md](references/checkpoint-format.md).
4. Replace the current checkpoint rather than creating a chain of dated
   handover files, unless the project explicitly requires an immutable log.
5. Keep exact commands only when they are the reproducible next action or
   evidence. Do not preserve speculative debugging history.
6. Link or name the latest relevant evidence receipt. Do not copy its command
   output into the checkpoint.

## Resume

1. Read the concise entrypoint, governance configuration, checkpoint, and
   authorities routed for the next action.
2. Inspect version-control state and run the narrowest check that detects drift
   from the checkpoint.
3. State the objective, verified drift, blocker if any, and next action briefly.
4. Continue the work. Do not ask the user to reconstruct prior chat.

## Honesty rules

- A command not run is not green.
- A file not inspected is not verified.
- "Implemented" and "accepted" are different states.
- Dirty user work is named and preserved.
- One concrete next action is better than a long backlog.
