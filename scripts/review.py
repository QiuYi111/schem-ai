from __future__ import annotations

import sys
from pathlib import Path

from common import STATE_PATH, read_data, utc_now, write_data


def main() -> int:
    state = read_data(STATE_PATH)
    phase = state.get("phase", "phase0")
    review_path = Path(__file__).resolve().parent.parent / "review" / f"{phase}_review.md"
    if not review_path.exists():
        review_path.write_text(
            "\n".join(
                [
                    f"# Review for {phase}",
                    "",
                    "## Findings",
                    "",
                    "- No automated semantic findings. Manual agent review still required.",
                    "",
                    "## Follow-ups",
                    "",
                    "- Confirm phase outputs are complete and self-consistent.",
                    "",
                ]
            ),
            encoding="utf-8",
        )
    pending = state.get("pending_reviews", [])
    if str(review_path.name) not in pending:
        pending.append(review_path.name)
    state["pending_reviews"] = pending
    state["last_updated"] = utc_now()
    write_data(STATE_PATH, state)
    print(f"Review scaffold ready at {review_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
