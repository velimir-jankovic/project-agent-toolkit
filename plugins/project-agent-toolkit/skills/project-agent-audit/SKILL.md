---
name: project-agent-audit
description: Review and improve a repository's complete AI-agent setup, including AGENTS.md, Copilot/Codex configuration, skills, roles, prompts, policy docs, plans, handoffs, hooks, and validation guards. Use when instructions are bloated, contradictory, expensive to load, project-specific process should be extracted, agents repeatedly miss rules, or a reusable governance plugin is being evaluated.
---

# Project Agent Audit

Find structural causes of unreliable agent work rather than adding more prose.

## Iteration mode

When the user is iterating on agent policy, inspect only the affected
instruction surface, make the coherent policy change, self-review it, and run
at most one cheapest relevant sanity check. Do not run the full audit, adapter,
route, coverage, or focused-test sequence unless the user requests a
checkpoint or audit gate. An explicit request for no validation skips the
sanity check.

## Required audit

Use the full sequence below outside iteration mode.

1. Inspect the working tree before reading policy.
2. Inventory every agent-facing file and every script or hook that enforces an
   agent claim.
3. Read [governance-schema.md](references/governance-schema.md) and
   [audit-rubric.md](references/audit-rubric.md).
4. If `.agent-governance.json` exists, run:

   ```console
   python <plugin-root>/scripts/governance.py audit --root <project-root> --json
   ```

   If it does not exist, do not treat that alone as the audit. Continue with
   manual discovery and recommend bootstrap only when it improves the project.
5. Run adapter, route, and coverage checks:

   ```console
   python <plugin-root>/scripts/governance.py generate --root <project-root>
   python <plugin-root>/scripts/governance.py route-test --root <project-root>
   python <plugin-root>/scripts/governance.py coverage --root <project-root> --strict
   python <plugin-root>/scripts/governance.py context --root <project-root> --task "<representative task>"
   python <plugin-root>/scripts/governance.py capability-check --root <project-root> --changed
   ```

6. Classify each issue by root cause:

   - authority ambiguity;
   - excess always-loaded context;
   - duplicated or contradictory policy;
   - missing task routing;
   - missing or stale capability ownership;
   - prose-only rule that should be mechanical;
   - stale state or handoff;
   - role ambiguity or unsafe delegation;
   - tooling/runtime data mixed with policy;
   - unsupported completion claims.

7. Separate generic process from project-specific policy. Extract only the
   generic process; keep domain rules with their project.
8. Rank fixes by reliability and context saved, not by cosmetic neatness.
9. After edits, rerun the audit, representative task routes, existing project
   guards, and focused tests. Do not apply this step in iteration mode.

## Output

Lead with the outcome. Report:

- critical findings and evidence;
- always-loaded context before and after;
- canonical authority order;
- task routes introduced or corrected;
- bounded capability ownership maps introduced or corrected;
- changed-path ownership scopes and remaining semantic-review limits;
- rules converted to guards;
- routing contracts and coverage gaps;
- stale generated adapters;
- validation profiles and evidence-receipt readiness;
- policy intentionally left project-specific;
- validation actually run.

Do not describe a rearrangement as an optimization unless it reduces ambiguity,
context cost, or unverified behavior.
