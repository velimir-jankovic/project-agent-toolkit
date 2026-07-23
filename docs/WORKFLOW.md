# Project workflow

## Change

1. Route the task through this repository's governance configuration.
2. Keep skills concise; move detailed contracts into their `references/`.
3. Change templates only when the behavior should apply to newly bootstrapped
   projects.
4. Change `governance.py` when enforcement or routing semantics change.
5. Add a focused unit test for CLI behavior and a structural guard for invariant
   changes.

## Verify

Run `python scripts/quality.py`. For plugin ingestion changes, also run the
current Codex plugin and skill validators when available.

## Release

Update semantic version, rerun quality and ingestion validation, then reinstall
the local plugin so Codex invalidates its cached version.
