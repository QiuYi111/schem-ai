from __future__ import annotations

import argparse
import sys

from common import default_state, resolve_project_root, state_path, read_data


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", default=".")
    args = parser.parse_args()

    project_root = resolve_project_root(args.project_root)
    state = read_data(state_path(project_root)) or default_state()
    print(f"Project root: {project_root}")
    print("Current workflow state:")
    for key in [
        "phase",
        "status",
        "blocked",
        "allow_transition",
        "review_status",
        "pending_reviews",
        "last_completed_phase",
        "last_updated",
    ]:
        print(f"- {key}: {state.get(key)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
