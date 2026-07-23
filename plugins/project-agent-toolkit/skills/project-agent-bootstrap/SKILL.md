---
name: project-agent-bootstrap
description: Set up or migrate concise, project-neutral repository agent governance. Use when a user asks to add AGENTS.md or Copilot/Codex instructions, standardize AI contributor workflow, introduce task-scoped policy routing, add generic architect/verifier/worker roles, or make an existing project reusable across coding agents without embedding product-specific behavior in a plugin.
---

# Project Agent Bootstrap

Create a small governance surface that points to project-owned policy instead
of copying that policy into every agent entrypoint.

## Workflow

1. Inspect version-control state and preserve unrelated work.
2. Inventory existing agent entrypoints, role files, prompts, hooks, workflow
   docs, architecture docs, progress files, and validation scripts.
3. Run the plugin CLI in additive mode:

   ```console
   python <plugin-root>/scripts/governance.py init --root <project-root>
   ```

   Use `--profile full` only when generic roles and prompt adapters are wanted.
   Do not use `--force` until the user has accepted overwriting existing files.

4. Read
   [migration-playbook.md](references/migration-playbook.md) when adopting a
   mature repository.
5. Edit `.agent-governance.json` so every authority and route reflects the
   project. The plugin must remain project-neutral; project-specific rules stay
   in the target repository.
6. Add representative `route_tests` before managing adapters. Every non-default
   route needs at least one test.
7. Preview and then write generated adapters:

   ```console
   python <plugin-root>/scripts/governance.py generate --root <project-root>
   python <plugin-root>/scripts/governance.py generate --root <project-root> --write
   ```

   `--force` is required to adopt existing unmanaged entrypoints. Review that
   diff carefully; generation must not erase unique project policy.
8. Keep generated `AGENTS.md` and `.github/copilot-instructions.md` as concise
   indexes. Move durable rules to one canonical project-owned document.
9. Configure validation profiles with `{ "run": ..., "proves": ... }` command
   objects and route each task class to the appropriate profile. Bootstrap
   profiles are intentionally empty and verification cannot pass until real
   project-owned commands are configured.
10. Run:

   ```console
   python <plugin-root>/scripts/governance.py audit --root <project-root>
   python <plugin-root>/scripts/governance.py route-test --root <project-root>
   python <plugin-root>/scripts/governance.py coverage --root <project-root> --strict
   python <plugin-root>/scripts/governance.py route --root <project-root> --task "<representative task>"
   ```

11. Test at least one architecture task, one implementation task, and one
   unrelated/default task. Confirm each route returns only useful authorities.
12. Report files created, existing policy preserved, unresolved migration risks,
   and exact validation.

## Upgrade

For an existing toolkit configuration:

```console
python <plugin-root>/scripts/governance.py upgrade --root <project-root>
python <plugin-root>/scripts/governance.py upgrade --root <project-root> --write
```

The first command is a preview. After writing, review the configuration, run
adapter generation explicitly, and rerun audit, route contracts, and coverage.

## Non-negotiables

- Never replace project architecture or rules with generic boilerplate.
- Never bake a language, framework, product, model name, or vendor workflow
  into the plugin.
- Never make every domain document always-loaded merely because it may become
  relevant later.
- Never overwrite a mature instruction surface without preserving its unique
  project policy in a canonical home.
- Role templates define responsibilities; model choice remains environment
  configuration.
