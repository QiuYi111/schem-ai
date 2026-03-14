from __future__ import annotations

import argparse
import sys
from pathlib import Path

from common import (
    AGENT_DOCS,
    PHASE_DOCS,
    PHASE_REQUIRED_FILES,
    PHASES,
    REQUIRED_DIRS,
    REQUIRED_FILES,
    default_index,
    default_state,
    index_path,
    read_data,
    resolve_project_root,
    state_path,
)


def missing_paths(project_root: Path) -> list[str]:
    missing = []
    for item in REQUIRED_DIRS:
        if not (project_root / item).exists():
            missing.append(item + "/")
    for item in REQUIRED_FILES + PHASE_DOCS + AGENT_DOCS:
        if not (project_root / item).exists():
            missing.append(item)
    return missing


def is_nonempty(path: Path) -> bool:
    return path.exists() and path.stat().st_size > 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", default=".")
    args = parser.parse_args()

    project_root = resolve_project_root(args.project_root)
    failures: list[str] = []

    for path in missing_paths(project_root):
        failures.append(f"Missing required path: {path}")

    state = read_data(state_path(project_root)) or default_state()
    index = read_data(index_path(project_root)) or default_index()

    phase = state.get("phase", "phase0")
    if phase not in PHASES:
        failures.append(f"Unknown phase in state.yaml: {phase}")
    else:
        for rel in PHASE_REQUIRED_FILES[phase]:
            artifact = project_root / rel
            if not artifact.exists():
                failures.append(f"Missing artifact for {phase}: {rel}")
            elif not is_nonempty(artifact):
                failures.append(f"Artifact exists but is empty: {rel}")

    if state.get("review_status") == "approved" and state.get("pending_reviews"):
        failures.append("State is inconsistent: review_status is approved but pending_reviews is not empty.")

    for category in ["documents", "design_files", "datasheets"]:
        for rel in index.get(category, []):
            if not (project_root / rel).exists():
                failures.append(f"Project index references a missing file: {rel}")

    for key in ["state", "index", "skill"]:
        rel = index.get("current_artifacts", {}).get(key)
        if rel and not (project_root / rel).exists():
            failures.append(f"Current artifact path is missing: {rel}")

    if failures:
        print(f"Validation failed for {project_root}:")
        for item in failures:
            print(f"- {item}")
        return 1

    print(f"Validation passed for {project_root}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
