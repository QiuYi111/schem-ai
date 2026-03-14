from __future__ import annotations

import sys

from common import PHASES, STATE_PATH, read_data, utc_now, write_data


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python scripts/transition.py <phase>")
        return 1

    target = sys.argv[1]
    if target not in PHASES:
        print(f"Unknown phase: {target}")
        return 1

    state = read_data(STATE_PATH)
    current = state.get("phase", "phase0")
    if state.get("blocked"):
        print("Transition blocked: current state is blocked.")
        return 1
    if not state.get("allow_transition", True):
        print("Transition blocked: allow_transition is false.")
        return 1

    current_index = PHASES.index(current)
    target_index = PHASES.index(target)
    if target_index > current_index + 1:
        print(f"Illegal transition: cannot jump from {current} to {target}")
        return 1

    state["phase"] = target
    state["status"] = "in_progress"
    state["last_updated"] = utc_now()
    write_data(STATE_PATH, state)
    print(f"Transitioned from {current} to {target}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
