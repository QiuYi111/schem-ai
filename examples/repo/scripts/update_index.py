from __future__ import annotations

import argparse
import sys
from pathlib import Path

from common import index_path, read_data, resolve_project_root, utc_now, write_data


def collect_files(project_root: Path, prefix: str, suffixes: tuple[str, ...]) -> list[str]:
    base = project_root / prefix
    if not base.exists():
        return []
    return sorted(
        str(path.relative_to(project_root)).replace("\\", "/")
        for path in base.rglob("*")
        if path.is_file() and path.suffix.lower() in suffixes
    )


def read_approved_parts(project_root: Path) -> list[str]:
    approved_path = project_root / "sourcing" / "approved_parts.yaml"
    if not approved_path.exists():
        return []
    parts: list[str] = []
    for line in approved_path.read_text(encoding="utf-8-sig").splitlines():
        stripped = line.strip()
        if stripped.startswith("- "):
            parts.append(stripped[2:].strip())
    return parts


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", default=".")
    args = parser.parse_args()

    project_root = resolve_project_root(args.project_root)
    index = {
        "documents": sorted(
            set(
                collect_files(project_root, "spec", (".md",))
                + collect_files(project_root, "architecture", (".md",))
                + collect_files(project_root, "handbook", (".md",))
                + collect_files(project_root, "review", (".md",))
            )
        ),
        "design_files": sorted(
            set(
                collect_files(project_root, "design", (".json", ".md"))
                + collect_files(project_root, "render", (".md", ".json", ".svg", ".png", ".kicad_sch", ".txt"))
            )
        ),
        "approved_parts": read_approved_parts(project_root),
        "datasheets": collect_files(project_root, "sourcing/datasheets", (".pdf",)),
        "current_artifacts": {
            "state": "state.yaml",
            "index": "project_index.yaml",
            "skill": "SKILL.md",
        },
        "last_updated": utc_now(),
    }
    write_data(index_path(project_root), index)
    print(f"Updated project index for {project_root}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
