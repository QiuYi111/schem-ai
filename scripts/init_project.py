from __future__ import annotations

import argparse
import csv
import json
import shutil
import subprocess
import sys
from pathlib import Path

from common import PACKAGE_ROOT, default_index, default_state, write_data

TEMPLATE_ROOT = PACKAGE_ROOT / "examples" / "minimal-repo"
COPY_ROOT_FILES = [".gitignore", "Makefile", "SKILL.md"]
COPY_DIRS = ["hooks", "phases", "schemas"]
SKIP_NAMES = {"__pycache__", ".git"}
SKIP_SUFFIXES = {".pyc", ".pyo", ".pyd"}


def copy_tree(src: Path, dst: Path) -> None:
    dst.mkdir(parents=True, exist_ok=True)
    for item in src.iterdir():
        if item.name in SKIP_NAMES or item.suffix.lower() in SKIP_SUFFIXES:
            continue
        target = dst / item.name
        if item.is_dir():
            copy_tree(item, target)
        else:
            shutil.copy2(item, target)


def ensure_clean_target(target_root: Path, force: bool) -> None:
    conflicts: list[str] = []
    for name in COPY_ROOT_FILES + COPY_DIRS:
        if (target_root / name).exists():
            conflicts.append(name)
    for item in TEMPLATE_ROOT.iterdir():
        if (target_root / item.name).exists():
            conflicts.append(item.name)
    if conflicts and not force:
        joined = ", ".join(sorted(set(conflicts)))
        raise FileExistsError(f"Target already contains managed paths: {joined}")


def ensure_git_repo(target_root: Path) -> None:
    if (target_root / ".git").exists():
        return
    subprocess.run(["git", "init"], cwd=target_root, check=True)


def seed_schema_examples(target_root: Path) -> None:
    approved_parts_path = target_root / "sourcing" / "approved_parts.yaml"
    if approved_parts_path.exists():
        write_data(
            approved_parts_path,
            {
                "approved_parts": [],
                "unresolved_items": ["No parts selected yet."],
            },
        )

    interconnect_path = target_root / "design" / "interconnect.json"
    if interconnect_path.exists():
        interconnect_path.write_text(
            json.dumps(
                {
                    "project": None,
                    "modules": [],
                    "nets": [],
                    "components": [],
                    "constraints": [],
                    "assumptions": [],
                    "evidence": [],
                    "unresolved_items": ["Interconnect design has not started."],
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )

    candidate_parts = target_root / "sourcing" / "candidate_parts.csv"
    if candidate_parts.exists():
        with candidate_parts.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.writer(handle)
            writer.writerow([
                "candidate_id",
                "part_number",
                "manufacturer",
                "role",
                "status",
                "source",
                "rationale",
                "confidence",
                "unresolved_items",
            ])


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", required=True)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    target_root = Path(args.target).resolve()
    if target_root == PACKAGE_ROOT and not args.force:
        print("Refusing to initialize the package repository itself. Pass --target to a user repository.")
        return 1

    target_root.mkdir(parents=True, exist_ok=True)
    try:
        ensure_clean_target(target_root, args.force)
    except FileExistsError as exc:
        print(str(exc))
        return 1

    for name in COPY_ROOT_FILES:
        shutil.copy2(PACKAGE_ROOT / name, target_root / name)
    for name in COPY_DIRS:
        copy_tree(PACKAGE_ROOT / name, target_root / name)
    copy_tree(TEMPLATE_ROOT, target_root)

    write_data(target_root / "state.yaml", default_state())
    write_data(target_root / "project_index.yaml", default_index())
    seed_schema_examples(target_root)
    ensure_git_repo(target_root)

    update_script = PACKAGE_ROOT / "scripts" / "update_index.py"
    subprocess.run([sys.executable, str(update_script), "--project-root", str(target_root)], check=True)

    print(f"Initialized schematic-agent repository at {target_root}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
