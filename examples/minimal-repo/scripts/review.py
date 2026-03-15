from __future__ import annotations

import argparse
import sys
from pathlib import Path

from common import read_state, resolve_project_root, run_hook_group, state_path, utc_now, write_data


PLACEHOLDER_FINDINGS = "- Add reviewer findings here."
PLACEHOLDER_DECISION = "- Approve or request changes after manual review."
VALID_DECISIONS = {"ready to approve", "needs revision", "blocked by unresolved issue"}


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
                PLACEHOLDER_FINDINGS,
                "",
                "## Decision",
                "",
                PLACEHOLDER_DECISION,
                "",
            ]
        ),
        encoding="utf-8",
    )


def parse_decision(review_path: Path) -> str | None:
    text = review_path.read_text(encoding="utf-8-sig")
    lowered = text.lower()
    if PLACEHOLDER_FINDINGS in text or PLACEHOLDER_DECISION in text:
        return None
    for decision in VALID_DECISIONS:
        if decision in lowered:
            return decision
    return None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--approve", action="store_true")
    args = parser.parse_args()

    project_root = resolve_project_root(args.project_root)
    state_file = state_path(project_root)
    if not state_file.exists():
        print(f"Missing workflow state: {state_file}")
        return 1

    state = read_state(project_root)
    phase = state.get("phase", "phase0")
    review_dir = project_root / "review"
    review_dir.mkdir(parents=True, exist_ok=True)
    review_path = review_dir / f"{phase}_review.md"
    ensure_review_file(review_path, phase)

    pending = state.get("pending_reviews", [])
    if args.approve:
        hook_result = run_hook_group(
            project_root,
            "pre-review-approve",
            {"HOOK_REVIEW_PHASE": phase, "HOOK_REVIEW_FILE": review_path.name},
        )
        if hook_result != 0:
            return hook_result

        pending = [item for item in pending if item != review_path.name]
        state["pending_reviews"] = pending
        state["review_status"] = "approved"
        state["allow_transition"] = not pending
        state["status"] = "ready_to_transition"
        state["last_updated"] = utc_now()
        write_data(state_file, state)

        hook_result = run_hook_group(
            project_root,
            "post-review-approve",
            {"HOOK_REVIEW_PHASE": phase, "HOOK_REVIEW_FILE": review_path.name},
        )
        if hook_result != 0:
            return hook_result

        print(f"Approved review for {phase}: {review_path}")
        return 0

    decision = parse_decision(review_path)
    if decision == "ready to approve":
        state["review_status"] = "ready_for_approval"
        state["status"] = "review_ready"
    else:
        if review_path.name not in pending:
            pending.append(review_path.name)
        state["review_status"] = "pending"
        state["status"] = "review_pending"
    state["pending_reviews"] = pending
    state["allow_transition"] = False
    state["last_updated"] = utc_now()

    hook_result = run_hook_group(
        project_root,
        "pre-review",
        {"HOOK_REVIEW_PHASE": phase, "HOOK_REVIEW_FILE": review_path.name},
    )
    if hook_result != 0:
        return hook_result

    write_data(state_file, state)

    hook_result = run_hook_group(
        project_root,
        "post-review",
        {"HOOK_REVIEW_PHASE": phase, "HOOK_REVIEW_FILE": review_path.name},
    )
    if hook_result != 0:
        return hook_result

    print(f"Review scaffold ready at {review_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
