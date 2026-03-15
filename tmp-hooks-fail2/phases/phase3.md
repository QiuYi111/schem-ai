# Phase3: Datasheet Deep Read

## Goal

Turn the approved parts and their datasheets into implementation-ready handbook guidance.

This phase is where part selection becomes design knowledge.

## Main-Agent Role

In phase3, the main agent acts as an orchestrator.

Its job is to:

1. Read workflow state and confirm phase3 is active
2. Read this phase rule
3. Invoke the best available handbook-producing role, typically the sourcer role unless a dedicated handbook role exists later
4. Keep handbook artifacts aligned with approved parts and datasheet evidence
5. Ensure critical constraints are preserved for downstream design
6. Run index, validate, review, checkpoint, and transition gates

## Primary Worker

Use `agents/sourcer.md` as the default primary specialized agent for this phase until a more specialized handbook-focused role exists.

In phase3, that worker is responsible for:

1. Reading approved part selections
2. Reading the preserved datasheets
3. Extracting implementation-relevant design guidance
4. Turning raw datasheet evidence into handbook notes that later phases can use

## Working Method

Phase3 should follow this pattern:

1. Main agent reads state and phase rule
2. Main agent invokes the handbook-producing worker
3. The worker reads approved parts and datasheets
4. The worker writes or updates handbook artifacts, at minimum `handbook/README.md`
5. Main agent checks whether the handbook is grounded in the selected parts and datasheet evidence
6. Main agent runs:
   - `python scripts/update_index.py --project-root <repo>`
   - `python scripts/validate.py --project-root <repo>`
   - `python scripts/review.py --project-root <repo>`
7. Use reviewer involvement when omission risk or handbook quality risk is material
8. Revise until handbook findings are resolved

## Required Outputs

- `handbook/README.md`

Additional handbook files may be added if that improves clarity, but the handbook must remain coherent and navigable.

## Required Inputs

At minimum, phase3 must use:

- `sourcing/approved_parts.yaml`
- relevant files in `sourcing/datasheets/`
- relevant architecture artifacts

## Required Content

At minimum, the handbook must cover:

1. Supply and power constraints
2. Clock and timing constraints where relevant
3. Reset requirements where relevant
4. Interface requirements and caveats
5. Protection, reliability, or layout-sensitive caveats where relevant
6. Important operating limits and design warnings
7. Cross-links to the approved parts and datasheet evidence

## Handbook Requirement

The handbook must be written for downstream design use, not as a datasheet summary for its own sake.

A good handbook helps later phases answer:

1. What must be respected in the design
2. What is dangerous to assume
3. What implementation caveats are easy to miss
4. Which constraints materially shape the final interconnect design

## Review Requirement

Reviewer involvement should challenge:

1. Whether important constraints were omitted
2. Whether implementation-relevant caveats were buried
3. Whether the handbook is actually grounded in the approved part set and datasheets
4. Whether the output is useful for phase4 rather than merely descriptive

## Entry Conditions

Phase3 may start when:

1. `state.yaml.phase` is `phase3`
2. Phase2 sourcing artifacts exist and are usable
3. The main agent has loaded `SKILL.md`, this phase rule, and the selected worker role
4. Relevant datasheets are present

## Exit Criteria

Phase3 is ready for review only when:

1. `handbook/README.md` exists and is non-empty
2. The handbook is traceable to the approved parts and datasheets
3. Critical constraints and caveats are visible
4. The handbook is usable by phase4 without requiring datasheet rediscovery

Phase3 is ready to transition only when:

1. `scripts/update_index.py` has been run after the latest handbook changes
2. `scripts/validate.py` passes
3. `scripts/review.py` has been run
4. Reviewer findings have been resolved
5. `scripts/review.py --approve` has been run
6. The project state allows transition

## Failure Modes

Do not close phase3 if any of the following is true:

1. The handbook is just a loose summary with no downstream design value
2. Critical constraints are missing
3. The handbook is not clearly grounded in the approved parts and datasheets
4. The output leaves phase4 to rediscover essential part behavior

If phase3 fails semantic review, keep the phase open and continue handbook refinement rather than forcing progress.
