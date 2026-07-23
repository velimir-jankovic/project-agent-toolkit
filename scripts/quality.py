#!/usr/bin/env python3
"""Authoritative local/CI quality gate for Project Agent Toolkit."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def run(label: str, command: list[str]) -> bool:
    print(f"\n== {label} ==", flush=True)
    result = subprocess.run(command, cwd=ROOT, check=False)
    if result.returncode:
        print(f"{label}: FAILED ({result.returncode})", file=sys.stderr)
        return False
    return True


def main() -> int:
    python = sys.executable
    checks = [
        (
            "Python compile",
            [
                python,
                "-m",
                "compileall",
                "-q",
                "scripts",
                "plugins/project-agent-toolkit/scripts",
                "tests",
            ],
        ),
        ("Plugin structure", [python, "scripts/check_plugin.py"]),
        (
            "Governance",
            [
                python,
                "plugins/project-agent-toolkit/scripts/governance.py",
                "check",
                "--root",
                ".",
            ],
        ),
        (
            "Generated adapters",
            [
                python,
                "plugins/project-agent-toolkit/scripts/governance.py",
                "generate",
                "--root",
                ".",
            ],
        ),
        (
            "Route contracts",
            [
                python,
                "plugins/project-agent-toolkit/scripts/governance.py",
                "route-test",
                "--root",
                ".",
            ],
        ),
        (
            "Governance coverage",
            [
                python,
                "plugins/project-agent-toolkit/scripts/governance.py",
                "coverage",
                "--root",
                ".",
                "--strict",
            ],
        ),
        ("Tests", [python, "-m", "unittest", "discover", "-s", "tests", "-v"]),
    ]
    failures = sum(not run(label, command) for label, command in checks)
    if failures:
        print(f"\nquality: FAIL ({failures} check group(s))", file=sys.stderr)
        return 1
    print("\nquality: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
