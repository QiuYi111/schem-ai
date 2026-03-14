from __future__ import annotations

import sys

from common import INDEX_PATH, ROOT, utc_now, write_data


def collect_files(prefix: str, suffixes: tuple[str, ...]) -> list[str]:
    base = ROOT / prefix
    if not base.exists():
        return []
    return sorted(
        str(path.relative_to(ROOT)).replace("\\", "/")
        for path in base.rglob("*")
        if path.is_file() and path.suffix.lower() in suffixes
    )


def main() -> int:
    index = {
        "documents": sorted(
            set(
                collect_files("spec", (".md",))
                + collect_files("architecture", (".md",))
                + collect_files("handbook", (".md",))
                + collect_files("review", (".md",))
            )
        ),
        "design_files": sorted(
            set(collect_files("design", (".json", ".md")) + collect_files("render", (".md", ".json", ".svg", ".png", ".kicad_sch")))
        ),
        "approved_parts": [],
        "datasheets": collect_files("sourcing/datasheets", (".pdf",)),
        "current_artifacts": {
            "state": "state.yaml",
            "index": "project_index.yaml",
            "skill": "SKILL.md",
        },
        "last_updated": utc_now(),
    }
    write_data(INDEX_PATH, index)
    print(f"Updated {INDEX_PATH.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
