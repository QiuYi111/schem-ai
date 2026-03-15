from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", default=".")
    args = parser.parse_args()

    project_root = Path(args.project_root).resolve()
    output_dir = Path(os.environ.get("HOOK_RENDER_OUTPUT_DIR", project_root / "render" / "schematic_output"))
    render_log = Path(os.environ.get("HOOK_RENDER_LOG", project_root / "render" / "render_log.md"))
    print(f"Post-render guard: {output_dir}")

    if not output_dir.exists() or not any(output_dir.iterdir()):
        print(f"Render output directory is missing or empty: {output_dir}")
        return 1
    if not render_log.exists() or render_log.stat().st_size == 0:
        print(f"Render log is missing or empty: {render_log}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
