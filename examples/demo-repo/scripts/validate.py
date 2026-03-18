from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import jsonschema

from common import (
    AGENT_DOCS,
    PHASE_DOCS,
    PHASE_REQUIRED_FILES,
    PHASES,
    REQUIRED_DIRS,
    REQUIRED_FILES,
    SCHEMA_FILES,
    read_data,
    read_index,
    read_state,
    resolve_project_root,
    schemas_path,
)


PHASE_DIR_REQUIREMENTS = {
    "phase0": [],
    "phase1": [],
    "phase2": ["sourcing/datasheets"],
    "phase3": ["sourcing/datasheets"],
    "phase4": ["sourcing/datasheets"],
    "phase5": ["sourcing/datasheets"],
}


def missing_paths(project_root: Path, phase: str) -> list[str]:
    missing = []
    for item in REQUIRED_DIRS:
        if not (project_root / item).exists():
            missing.append(item + "/")
    for item in PHASE_DIR_REQUIREMENTS.get(phase, []):
        if not (project_root / item).exists():
            missing.append(item + "/")
    for item in REQUIRED_FILES + PHASE_DOCS + AGENT_DOCS + SCHEMA_FILES:
        if not (project_root / item).exists():
            missing.append(item)
    return missing


def is_nonempty(path: Path) -> bool:
    return path.exists() and path.stat().st_size > 0


def has_render_output(project_root: Path) -> bool:
    output_dir = project_root / "render" / "schematic_output"
    return output_dir.exists() and any(path.is_file() for path in output_dir.rglob("*"))


def load_schema(project_root: Path, name: str) -> dict:
    path = schemas_path(project_root) / name
    return json.loads(path.read_text(encoding="utf-8-sig"))


def validate_schema(failures: list[str], payload: dict, schema: dict, label: str) -> None:
    try:
        jsonschema.validate(payload, schema)
    except jsonschema.ValidationError as exc:
        location = ".".join(str(part) for part in exc.absolute_path) or "<root>"
        failures.append(f"Schema validation failed for {label} at {location}: {exc.message}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", default=".")
    args = parser.parse_args()

    project_root = resolve_project_root(args.project_root)
    failures: list[str] = []

    state = read_state(project_root)
    index = read_index(project_root)
    phase = state.get("phase", "phase0")

    for path in missing_paths(project_root, phase):
        failures.append(f"Missing required path: {path}")

    if not failures:
        validate_schema(failures, state, load_schema(project_root, "state.schema.json"), "state.yaml")
        validate_schema(failures, index, load_schema(project_root, "project_index.schema.json"), "project_index.yaml")

        approved_parts_path = project_root / "sourcing" / "approved_parts.yaml"
        if approved_parts_path.exists():
            validate_schema(
                failures,
                read_data(approved_parts_path),
                load_schema(project_root, "approved_parts.schema.json"),
                "sourcing/approved_parts.yaml",
            )

        interconnect_path = project_root / "design" / "interconnect.json"
        if interconnect_path.exists():
            validate_schema(
                failures,
                json.loads(interconnect_path.read_text(encoding="utf-8-sig")),
                load_schema(project_root, "interconnect.schema.json"),
                "design/interconnect.json",
            )

    if phase not in PHASES:
        failures.append(f"Unknown phase in state.yaml: {phase}")
    else:
        for rel in PHASE_REQUIRED_FILES[phase]:
            artifact = project_root / rel
            if not artifact.exists():
                failures.append(f"Missing artifact for {phase}: {rel}")
            elif not is_nonempty(artifact):
                failures.append(f"Artifact exists but is empty: {rel}")

    if phase == "phase5" and not has_render_output(project_root):
        failures.append("Missing render output for phase5: render/schematic_output/ must contain at least one file.")

    if state.get("review_status") == "approved" and state.get("pending_reviews"):
        failures.append("State is inconsistent: review_status is approved but pending_reviews is not empty.")

    # Datasheet Gating
    phase_idx = PHASES.index(phase) if phase in PHASES else -1
    phase2_idx = PHASES.index("phase2")
    
    approved_parts_file = project_root / "sourcing" / "approved_parts.yaml"

    if phase_idx >= phase2_idx:
        has_approved_parts = False
        if approved_parts_file.exists():
            parts_data = read_data(approved_parts_file)
            approved_parts = parts_data.get("approved_parts", []) if isinstance(parts_data, dict) else []
            has_approved_parts = isinstance(approved_parts, list) and len(approved_parts) > 0

        if has_approved_parts:
            datasheet_dir = project_root / "sourcing" / "datasheets"
            datasheets = index.get("datasheets", [])

            if not datasheets and not (datasheet_dir.exists() and any(datasheet_dir.iterdir())):
                failures.append("Datasheet gating failure: Approved parts exist but no datasheets found in sourcing/datasheets/ or project index.")

            # Check for empty datasheets
            if datasheet_dir.exists():
                for ds in datasheet_dir.glob("*.pdf"):
                    if ds.stat().st_size == 0:
                        failures.append(f"Datasheet is empty: {ds.name}")

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
