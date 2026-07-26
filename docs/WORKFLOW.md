# Project workflow

## Change

1. Route the task through this repository's governance configuration.
2. Keep skills concise; move detailed contracts into their `references/`.
3. Change templates only when the behavior should apply to newly bootstrapped
   projects.
4. Change `plugins/project-agent-toolkit/scripts/governance.py` when
   enforcement or routing semantics change.
5. Before adding a test, name the plausible failure and observable contract it
   would protect. Prefer an existing check or extend one focused, table-driven
   test. Add no test when a compiler, static check, guard, or existing test
   already proves the claim.

## Integrate

Before independent review or `quality.py`, integrate every accepted slice,
resolve overlaps and TODOs, and self-review the current diff against ownership
and acceptance criteria. Treat that state as the candidate freeze. Delegated
workers run only assigned focused local checks. If review finds blockers,
resolve them under root ownership and request targeted closure; repeat the full
review only when the acceptance surface changes.

## Verify

Use the least expensive evidence capable of disproving the claim. For a bug
fix, demonstrate the regression against pre-fix behavior when practical; if
that is impractical, record why. Run `python scripts/quality.py` as this
repository's release gate. For plugin ingestion changes, also run the current
Codex plugin and skill validators when available. Test count and coverage
percentage are not completion criteria.

Do not run a narrower validation profile immediately before a broader profile
that extends it on the same source. Run the broader profile once after
candidate freeze unless the narrower result is needed to guide ongoing work.

## Communicate

Lead with the outcome. During work, report only a changed decision, meaningful
result, blocker, or risk. In the final response, summarize the change, evidence,
and anything still unresolved without dumping logs or narrating every step.

## Release

Update semantic version, use the plugin-creator cachebuster helper, rerun
quality and ingestion validation, push the marketplace, then reinstall the
plugin so Codex invalidates its cached version. Exercise the installed cache
against a clean scratch project before calling the release complete.
