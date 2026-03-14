from __future__ import annotations

import subprocess
import sys

from common import INDEX_PATH, REQUIRED_DIRS, ROOT, STATE_PATH, read_data, utc_now, write_data


def ensure_git_repo() -> None:
    if (ROOT / ".git").exists():
        return
    subprocess.run(["git", "init"], cwd=ROOT, check=True)


def ensure_dirs() -> None:
    for item in REQUIRED_DIRS:
        (ROOT / item).mkdir(parents=True, exist_ok=True)


def main() -> int:
    ensure_dirs()
    state = read_data(STATE_PATH) or {
        "phase": "phase0",
        "status": "not_started",
        "blocked": False,
        "allow_transition": True,
        "pending_reviews": [],
    }
    state["last_updated"] = utc_now()
    write_data(STATE_PATH, state)

    index = read_data(INDEX_PATH) or {
        "documents": [],
        "design_files": [],
        "approved_parts": [],
        "datasheets": [],
        "current_artifacts": {},
    }
    index["last_updated"] = utc_now()
    write_data(INDEX_PATH, index)

    ensure_git_repo()
    print(f"Project initialized at {ROOT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
