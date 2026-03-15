from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", default=".")
    args = parser.parse_args()

    project_root = Path(args.project_root).resolve()
    design_input = Path(os.environ.get("HOOK_RENDER_INPUT", project_root / "design" / "interconnect.json"))
    design_notes = project_root / "design" / "design_notes.md"
    print(f"Pre-render guard: {design_input}")

    if not design_input.exists():
        print(f"Missing render input: {design_input}")
        return 1
    if not design_notes.exists() or design_notes.stat().st_size == 0:
        print(f"Missing or empty design notes: {design_notes}")
        return 1

    try:
        payload = json.loads(design_input.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError as exc:
        print(f"Render input is not valid JSON: {exc}")
        return 1

    if not isinstance(payload, dict) or not payload:
        print("Render input JSON must be a non-empty object.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
