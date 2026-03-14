from __future__ import annotations

import sys
from pathlib import Path

from common import INDEX_PATH, PHASE_REQUIRED_FILES, REQUIRED_DIRS, ROOT, STATE_PATH, read_data


def missing_paths() -> list[str]:
    missing = []
    for item in REQUIRED_DIRS:
        if not (ROOT / item).exists():
            missing.append(item + "/")
    for item in ["state.yaml", "project_index.yaml", "Makefile", "SKILL.md"]:
        if not (ROOT / item).exists():
            missing.append(item)
    return missing


def phase_missing_files(phase: str) -> list[str]:
    required = PHASE_REQUIRED_FILES.get(phase, [])
    return [item for item in required if not (ROOT / item).exists()]


def is_nonempty(path: Path) -> bool:
    return path.exists() and path.stat().st_size > 0


def main() -> int:
    failures = []

    for path in missing_paths():
        failures.append(f"Missing required path: {path}")

    state = read_data(STATE_PATH)
    index = read_data(INDEX_PATH)
    if not state:
        failures.append("State file is unreadable or empty.")
    if not index:
        failures.append("Project index file is unreadable or empty.")

    current_phase = state.get("phase", "phase0") if state else "phase0"
    for path in phase_missing_files(current_phase):
        failures.append(f"Missing artifact for {current_phase}: {path}")

    for path in ["spec/requirements.md", "architecture/system_overview.md", "design/interconnect.json", "render/render_log.md"]:
        if (ROOT / path).exists() and not is_nonempty(ROOT / path):
            failures.append(f"Artifact exists but is empty: {path}")

    if failures:
        print("Validation failed:")
        for item in failures:
            print(f"- {item}")
        return 1

    print("Validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
