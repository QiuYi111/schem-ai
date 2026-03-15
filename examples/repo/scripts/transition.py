from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from common import PHASES, read_data, resolve_project_root, run_hook_group, state_path, utc_now, write_data


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("phase")
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--allow-rollback", action="store_true")
    args = parser.parse_args()

    project_root = resolve_project_root(args.project_root)
    target = args.phase
    if target not in PHASES:
        print(f"Unknown phase: {target}")
        return 1

    state_file = state_path(project_root)
    state = read_data(state_file)
    current = state.get("phase", "phase0")
    if state.get("blocked"):
        print("Transition blocked: current state is blocked.")
        return 1
    if current not in PHASES:
        print(f"Unknown current phase in state: {current}")
        return 1
    if target == current:
        print(f"Already at {target}")
        return 0

    current_index = PHASES.index(current)
    target_index = PHASES.index(target)
    if target_index < current_index and not args.allow_rollback:
        print("Rollback requires --allow-rollback and a recorded change request.")
        return 1
    if target_index > current_index + 1:
        print(f"Illegal transition: cannot jump from {current} to {target}")
        return 1

    hook_result = run_hook_group(
        project_root,
        "pre-transition",
        {
            "HOOK_CURRENT_PHASE": current,
            "HOOK_TARGET_PHASE": target,
            "HOOK_ALLOW_ROLLBACK": "1" if args.allow_rollback else "0",
        },
    )
    if hook_result != 0:
        return hook_result

    if target_index > current_index:
        validate_script = Path(__file__).with_name("validate.py")
        result = subprocess.run(
            [sys.executable, str(validate_script), "--project-root", str(project_root)],
            check=False,
        )
        if result.returncode != 0:
            print("Transition blocked: validation did not pass.")
            return result.returncode
        if state.get("review_status") != "approved" or state.get("pending_reviews"):
            print("Transition blocked: review has not been approved.")
            return 1
        if not state.get("allow_transition", False):
            print("Transition blocked: allow_transition is false.")
            return 1
        state["last_completed_phase"] = current

    state["phase"] = target
    state["status"] = "in_progress"
    state["review_status"] = "not_started"
    state["allow_transition"] = False
    state["pending_reviews"] = []
    state["last_updated"] = utc_now()
    write_data(state_file, state)

    hook_result = run_hook_group(
        project_root,
        "post-transition",
        {
            "HOOK_CURRENT_PHASE": current,
            "HOOK_TARGET_PHASE": target,
            "HOOK_ALLOW_ROLLBACK": "1" if args.allow_rollback else "0",
        },
    )
    if hook_result != 0:
        return hook_result

    print(f"Transitioned from {current} to {target}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
