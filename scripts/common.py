from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATE_PATH = ROOT / "state.yaml"
INDEX_PATH = ROOT / "project_index.yaml"
PHASES = ["phase0", "phase1", "phase2", "phase3", "phase4", "phase5"]
REQUIRED_DIRS = [
    "spec",
    "architecture",
    "sourcing",
    "sourcing/datasheets",
    "handbook",
    "design",
    "render",
    "render/schematic_output",
    "review",
    "review/change_requests",
    "scripts",
    "hooks",
    "phases",
    "agents",
    "examples",
]
PHASE_REQUIRED_FILES = {
    "phase0": [
        "spec/requirements.md",
        "spec/constraints.md",
        "spec/open_questions.md",
        "spec/assumptions.md",
    ],
    "phase1": [
        "architecture/system_overview.md",
        "architecture/interface_matrix.md",
        "architecture/risk_register.md",
    ],
    "phase2": [
        "sourcing/candidate_parts.csv",
        "sourcing/approved_parts.yaml",
        "sourcing/selection_notes.md",
    ],
    "phase3": ["handbook/README.md"],
    "phase4": ["design/interconnect.json", "design/design_notes.md"],
    "phase5": ["render/render_log.md"],
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_data(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_data(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
