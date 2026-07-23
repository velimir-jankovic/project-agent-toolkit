#!/usr/bin/env python3
"""Opt in to repository-tracked Git hooks."""

from __future__ import annotations

import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    result = subprocess.run(
        ["git", "config", "core.hooksPath", ".githooks"],
        cwd=ROOT,
        check=False,
    )
    if result.returncode:
        return result.returncode
    print("Installed opt-in hooks: core.hooksPath -> .githooks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
