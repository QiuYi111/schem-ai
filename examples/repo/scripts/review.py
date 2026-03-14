from __future__ import annotations

import argparse
import sys
from pathlib import Path

from common import read_data, resolve_project_root, state_path, utc_now, write_data


def ensure_review_file(review_path: Path, phase: str) -> None:
    if review_path.exists():
        return
    review_path.write_text(
        "\n".join(
            [
                f"# Review for {phase}",
                "",
                "Status: pending",
                "",
                "## Findings",
                "",
                "- Add reviewer findings here.",
                "",
                "## Decision",
                "",
                "- Approve or request changes after manual review.",
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--approve", action="store_true")
    args = parser.parse_args()

    project_root = resolve_project_root(args.project_root)
    state_file = state_path(project_root)
    state = read_data(state_file)
    phase = state.get("phase", "phase0")
    review_dir = project_root / "review"
    review_dir.mkdir(parents=True, exist_ok=True)
    review_path = review_dir / f"{phase}_review.md"
    ensure_review_file(review_path, phase)

    pending = state.get("pending_reviews", [])
    if args.approve:
        pending = [item for item in pending if item != review_path.name]
        state["pending_reviews"] = pending
        state["review_status"] = "approved"
        state["allow_transition"] = not pending
        state["status"] = "ready_to_transition"
        state["last_updated"] = utc_now()
        write_data(state_file, state)
        print(f"Approved review for {phase}: {review_path}")
        return 0

    if review_path.name not in pending:
        pending.append(review_path.name)
    state["pending_reviews"] = pending
    state["review_status"] = "pending"
    state["allow_transition"] = False
    state["status"] = "review_pending"
    state["last_updated"] = utc_now()
    write_data(state_file, state)
    print(f"Review scaffold ready at {review_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
