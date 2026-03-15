from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", default=".")
    args = parser.parse_args()

    project_root = Path(args.project_root).resolve()
    current = os.environ.get("HOOK_CURRENT_PHASE", "")
    target = os.environ.get("HOOK_TARGET_PHASE", "")
    print(f"Pre-transition guard: {current} -> {target}")

    validate_script = project_root / "scripts" / "validate.py"
    result = subprocess.run([sys.executable, str(validate_script), "--project-root", str(project_root)], check=False)
    if result.returncode != 0:
        print("Pre-transition hook blocked transition because validation failed.")
        return result.returncode
    return 0


if __name__ == "__main__":
    sys.exit(main())
