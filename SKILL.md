# Schematic Agent Entry Skill

## Purpose

This skill is the single entry point for the schematic-agent workflow defined in prd.md.

## Responsibilities

The skill is only responsible for:

1. Reading state.yaml.
2. Determining the current phase.
3. Loading the matching phase rule from phases/.
4. Loading the matching agent template from gents/.
5. Calling deterministic scripts for validate, review, indexing, transitions, and checkpointing.

The skill must not manually recreate project structure, fake state transitions, or replace script-based validation.

## Operating Loop

1. Run python scripts/status.py to inspect state.
2. Read the current phase document in phases/.
3. Produce or update the required artifacts for that phase.
4. Run python scripts/update_index.py.
5. Run python scripts/validate.py.
6. Run python scripts/review.py.
7. If validation passes and review is resolved, run python scripts/checkpoint.py.
8. Advance with python scripts/transition.py <phase>.

## Phase Map

- phase0: requirement clarification
- phase1: architecture and implementation plan
- phase2: part sourcing and datasheet collection
- phase3: datasheet digestion and handbook generation
- phase4: structured interconnect design
- phase5: schematic rendering

## Expected Inputs

- User request and follow-up clarifications
- Current phase files
- Existing project assets recorded in project_index.yaml

## Expected Outputs

- Phase artifacts written to disk
- Updated state and project index
- Review record and git checkpoint
