from __future__ import annotations

import argparse
import subprocess
import sys

from common import read_data, resolve_project_root, state_path


def run_git(project_root, args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=project_root, capture_output=True, text=True, check=False)


def has_git_identity(project_root) -> bool:
    name = run_git(project_root, ["git", "config", "user.name"])
    email = run_git(project_root, ["git", "config", "user.email"])
    return bool(name.stdout.strip()) and bool(email.stdout.strip())


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--message")
    args = parser.parse_args()

    project_root = resolve_project_root(args.project_root)
    if not (project_root / ".git").exists():
        print("Git repository not initialized. Run init first.")
        return 1
    if not has_git_identity(project_root):
        print("Git checkpoint blocked: configure git config user.name and git config user.email for this repository or globally.")
        return 1

    status = run_git(project_root, ["git", "status", "--short"])
    if not status.stdout.strip():
        print("No changes to checkpoint.")
        return 0

    state = read_data(state_path(project_root))
    phase = state.get("phase", "phase0")
    add = run_git(project_root, ["git", "add", "."])
    if add.returncode != 0:
        print(add.stderr.strip() or add.stdout.strip())
        return add.returncode

    message = args.message or f"checkpoint: {phase}"
    commit = run_git(project_root, ["git", "commit", "-m", message])
    if commit.returncode != 0:
        print(commit.stderr.strip() or commit.stdout.strip())
        return commit.returncode

    print(commit.stdout.strip())
    return 0


if __name__ == "__main__":
    sys.exit(main())
