from __future__ import annotations

import argparse
import sys

from common import resolve_project_root, state_path, read_state


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", default=".")
    args = parser.parse_args()

    project_root = resolve_project_root(args.project_root)
    state_file = state_path(project_root)
    if not state_file.exists():
        print(f"Missing workflow state: {state_file}")
        print("This path is not an initialized project repository.")
        return 1

    state = read_state(project_root)
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
