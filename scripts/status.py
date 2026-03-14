from __future__ import annotations

import sys

from common import STATE_PATH, read_data


def main() -> int:
    state = read_data(STATE_PATH)
    if not state:
        print("State file not found or empty.")
        return 1
    print("Current workflow state:")
    for key in ["phase", "status", "blocked", "allow_transition", "pending_reviews", "last_updated"]:
        print(f"- {key}: {state.get(key)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
