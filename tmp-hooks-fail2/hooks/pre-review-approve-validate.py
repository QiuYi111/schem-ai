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
    phase = os.environ.get("HOOK_REVIEW_PHASE", "")
    review_file = os.environ.get("HOOK_REVIEW_FILE", "")
    review_path = project_root / "review" / review_file
    print(f"Pre-review-approve guard: {phase}")

    validate_script = project_root / "scripts" / "validate.py"
    result = subprocess.run([sys.executable, str(validate_script), "--project-root", str(project_root)], check=False)
    if result.returncode != 0:
        print("Pre-review-approve hook blocked approval because validation failed.")
        return result.returncode

    if not review_path.exists():
        print(f"Review file missing: {review_path}")
        return 1

    text = review_path.read_text(encoding="utf-8-sig")
    if "Add reviewer findings here." in text:
        print("Review approval blocked: review file still contains placeholder findings.")
        return 1
    if "Approve or request changes after manual review." in text:
        print("Review approval blocked: review file still contains placeholder decision text.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
