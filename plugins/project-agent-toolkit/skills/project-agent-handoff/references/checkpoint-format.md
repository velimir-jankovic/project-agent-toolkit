# Checkpoint format

Keep the checkpoint compact and overwrite the previous current checkpoint.

```markdown
## Current objective

One outcome sentence.

## Delivered

- Behavior that exists on the current revision.

## Evidence

- Evidence receipt path or identifier - result and what it proves.

## Open risks

- Required unresolved issue, or "none".

## Working tree

- Branch, relevant dirty files, and user-owned changes to preserve.

## Decisions

- Only decisions that constrain the next agent.

## Next action

One concrete action.
```

Exclude chat summaries, abandoned speculation, exhaustive file lists, and
commands that are neither evidence nor the next action.
