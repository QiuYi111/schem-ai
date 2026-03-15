from __future__ import annotations

import copy
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

PACKAGE_ROOT = Path(__file__).resolve().parent.parent
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
]
REQUIRED_FILES = ["state.yaml", "project_index.yaml", "Makefile", "SKILL.md", ".gitignore"]
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
DEFAULT_STATE = {
    "phase": "phase0",
    "status": "not_started",
    "blocked": False,
    "allow_transition": False,
    "review_status": "not_started",
    "pending_reviews": [],
    "last_completed_phase": None,
}
DEFAULT_INDEX = {
    "documents": [],
    "design_files": [],
    "approved_parts": [],
    "datasheets": [],
    "current_artifacts": {
        "state": "state.yaml",
        "index": "project_index.yaml",
        "skill": "SKILL.md",
    },
}
PHASE_DOCS = [f"phases/{phase}.md" for phase in PHASES]
AGENT_DOCS = [
    "agents/clarifier.md",
    "agents/architect.md",
    "agents/sourcer.md",
    "agents/reviewer.md",
]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_data(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    text = path.read_text(encoding="utf-8-sig").strip()
    if not text:
        return {}
    return json.loads(text)


def write_data(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def resolve_project_root(raw: str | None) -> Path:
    return (Path(raw) if raw else Path.cwd()).resolve()


def state_path(project_root: Path) -> Path:
    return project_root / "state.yaml"


def index_path(project_root: Path) -> Path:
    return project_root / "project_index.yaml"


def hooks_path(project_root: Path) -> Path:
    return project_root / "hooks"


def default_state() -> dict[str, Any]:
    payload = copy.deepcopy(DEFAULT_STATE)
    payload["last_updated"] = utc_now()
    return payload


def default_index() -> dict[str, Any]:
    payload = copy.deepcopy(DEFAULT_INDEX)
    payload["last_updated"] = utc_now()
    return payload


def run_hook_group(project_root: Path, hook_group: str, extra_env: dict[str, str] | None = None) -> int:
    hook_root = hooks_path(project_root)
    if not hook_root.exists():
        return 0

    hook_files = sorted(path for path in hook_root.iterdir() if path.is_file() and path.name.startswith(hook_group))
    if not hook_files:
        return 0

    env = os.environ.copy()
    env["PROJECT_ROOT"] = str(project_root)
    env["HOOK_GROUP"] = hook_group
    if extra_env:
        env.update(extra_env)

    for hook in hook_files:
        if hook.suffix == ".py":
            cmd = [sys.executable, str(hook), "--project-root", str(project_root)]
        elif hook.suffix in {".sh", ".bash"}:
            cmd = [str(hook), "--project-root", str(project_root)]
        else:
            continue

        print(f"Running hook {hook.name}")
        result = subprocess.run(cmd, cwd=project_root, env=env, capture_output=True, text=True, check=False)
        if result.stdout.strip():
            print(result.stdout.strip())
        if result.stderr.strip():
            print(result.stderr.strip())
        if result.returncode != 0:
            print(f"Hook failed: {hook.name}")
            return result.returncode

    return 0
