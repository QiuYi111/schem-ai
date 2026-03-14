# Schem-AI Template Package

This repository is the publishable source for:

1. The entry `SKILL.md`.
2. Deterministic workflow scripts in `scripts/`.
3. Phase and agent templates in `phases/` and `agents/`.
4. A ready-to-copy initialized project template in `examples/repo/`.

## Package Model

This repository is not the user project itself.

Users initialize their own repository by copying the template into a target directory:

```powershell
python scripts/init_project.py --target C:\path\to\user-repo
```

After initialization, the user repository contains its own `Makefile`, `scripts/`, `state.yaml`, `project_index.yaml`, and phase artifacts.

## Common Commands

Run against the example initialized repository:

```powershell
make status
make validate
make review
make approve-review
```

Initialize another repository:

```powershell
make init TARGET=C:\path\to\user-repo
```
