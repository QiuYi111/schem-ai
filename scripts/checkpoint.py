from __future__ import annotations

import subprocess
import sys

from common import ROOT, STATE_PATH, read_data


def run_git(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=ROOT, capture_output=True, text=True, check=False)


def has_git_identity() -> bool:
    name = run_git(["git", "config", "user.name"])
    email = run_git(["git", "config", "user.email"])
    return bool(name.stdout.strip()) and bool(email.stdout.strip())


def main() -> int:
    if not (ROOT / ".git").exists():
        print("Git repository not initialized. Run init first.")
        return 1

    if not has_git_identity():
        print("Git checkpoint blocked: configure git config user.name and git config user.email for this repository or globally.")
        return 1

    status = run_git(["git", "status", "--short"])
    if not status.stdout.strip():
        print("No changes to checkpoint.")
        return 0

    state = read_data(STATE_PATH)
    phase = state.get("phase", "phase0")
    add = run_git(["git", "add", "."])
    if add.returncode != 0:
        print(add.stderr.strip() or add.stdout.strip())
        return add.returncode

    commit = run_git(["git", "commit", "-m", f"checkpoint: {phase}"])
    if commit.returncode != 0:
        print(commit.stderr.strip() or commit.stdout.strip())
        return commit.returncode

    print(commit.stdout.strip())
    return 0


if __name__ == "__main__":
    sys.exit(main())
