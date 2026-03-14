from __future__ import annotations

import shutil
import sys


def main() -> int:
    checks = {
        "python": shutil.which("python"),
        "git": shutil.which("git"),
        "make": shutil.which("make"),
    }
    print("Environment check:")
    for name, value in checks.items():
        status = value if value else "missing"
        print(f"- {name}: {status}")
    if not checks["python"] or not checks["git"]:
        print("Missing required tools: python and git are mandatory.")
        return 1
    if not checks["make"]:
        print("Notice: make is not installed. The Makefile is present, but direct python scripts/*.py usage is required on this machine.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
