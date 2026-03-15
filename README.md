# Schem-AI Template Package

This repository is the publishable source for:

1. The entry `SKILL.md`.
2. Deterministic workflow scripts in `scripts/`.
3. Phase and agent templates in `phases/` and `agents/`.
4. JSON Schema contracts in `schemas/`.
5. A ready-to-copy initialized project template in `examples/minimal-repo/`.
6. A richer showcase repository in `examples/demo-repo/`.

## Package Model

This repository is not the user project itself.

Users initialize their own repository by copying the template into a target directory:

```powershell
python scripts/init_project.py --target C:\path\to\user-repo
```

After initialization, the user repository contains its own `Makefile`, `scripts/`, `schemas/`, `state.yaml`, `project_index.yaml`, and phase artifacts.

The root `Makefile` intentionally targets `examples/minimal-repo` by default so package commands do not pretend the source repository is a live project.

## Platform Scope

`bootstrap.py` is currently macOS-only. Version 0.1 officially supports bootstrap on macOS hosts only.

## Examples

- `examples/minimal-repo/` is the clean initialized template used by `init_project.py`.
- `examples/demo-repo/` is a more filled-in demonstration repository for inspection and smoke tests.

## Common Commands

Run against the minimal initialized repository:

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
