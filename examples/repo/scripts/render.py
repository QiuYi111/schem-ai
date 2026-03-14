from __future__ import annotations

import argparse
import json
import sys

from common import resolve_project_root, utc_now


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", default=".")
    args = parser.parse_args()

    project_root = resolve_project_root(args.project_root)
    design_path = project_root / "design" / "interconnect.json"
    if not design_path.exists():
        print(f"Missing design input: {design_path}")
        return 1

    out_dir = project_root / "render" / "schematic_output"
    out_dir.mkdir(parents=True, exist_ok=True)
    placeholder = out_dir / "placeholder_schematic.txt"
    payload = json.loads(design_path.read_text(encoding="utf-8-sig"))
    placeholder.write_text(
        "Render placeholder\n"
        f"Generated from: {design_path.name}\n"
        f"Top-level keys: {', '.join(sorted(payload.keys())) if isinstance(payload, dict) else 'n/a'}\n",
        encoding="utf-8",
    )
    log_path = project_root / "render" / "render_log.md"
    log_path.write_text(
        "\n".join(
            [
                "# Render Log",
                "",
                f"- Timestamp: {utc_now()}",
                "- Renderer: placeholder",
                f"- Input: {design_path.relative_to(project_root).as_posix()}",
                f"- Output: {placeholder.relative_to(project_root).as_posix()}",
                "",
            ]
        ),
        encoding="utf-8",
    )
    print(f"Rendered placeholder output at {placeholder}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
