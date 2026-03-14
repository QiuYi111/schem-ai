# Schematic Agent Entry Skill

## Purpose

This repository publishes a reusable skill, deterministic scripts, and a repository template for schematic-agent projects.

The initialized user repository is the runtime workspace. This source repository is the package that installs that workspace shape.

## Responsibilities

The skill is only responsible for:

1. Reading `state.yaml` inside the initialized project repository.
2. Determining the current phase.
3. Loading the matching rule from `phases/`.
4. Loading the matching agent template from `agents/`.
5. Producing or updating phase artifacts.
6. Calling deterministic scripts for indexing, validation, review, checkpointing, and transitions.

The skill must not manually recreate project structure, fake state transitions, or replace script-based validation.

## Operating Loop

1. Run `python scripts/status.py` in the initialized project repository.
2. Read the current phase document in `phases/`.
3. Read the relevant agent template in `agents/`.
4. Produce or update the required artifacts for the current phase.
5. Run `python scripts/update_index.py`.
6. Run `python scripts/validate.py`.
7. Run `python scripts/review.py` to scaffold or refresh the review artifact.
8. After manual review is complete, run `python scripts/review.py --approve`.
9. Run `python scripts/checkpoint.py`.
10. Advance with `python scripts/transition.py <next-phase>`.

## Phase Map

- `phase0`: requirement clarification
- `phase1`: architecture and implementation plan
- `phase2`: part sourcing and datasheet collection
- `phase3`: datasheet digestion and handbook generation
- `phase4`: structured interconnect design
- `phase5`: schematic rendering

## Expected Inputs

- User request and follow-up clarifications
- Current phase files
- Existing project assets recorded in `project_index.yaml`

## Expected Outputs

- Phase artifacts written to disk
- Updated `state.yaml` and `project_index.yaml`
- Review records and git checkpoints
