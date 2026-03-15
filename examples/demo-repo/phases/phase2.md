# Phase2: Part Sourcing

## Goal

Compare candidate parts, choose approved parts, and capture the datasheet evidence needed for later design work.

This phase is where the project converts architecture into concrete implementation options and part-level commitments.

## Main-Agent Role

In phase2, the main agent acts as an orchestrator.

Its job is to:

1. Read workflow state and confirm phase2 is active
2. Read this phase rule
3. Invoke the sourcer role as the primary specialized worker
4. Keep sourcing artifacts aligned with requirements and architecture
5. Ensure selection rationale and sourcing risk are explicit
6. Run index, validate, review, checkpoint, and transition gates

## Primary Worker

Use `agents/sourcer.md` as the primary specialized agent for this phase.

The sourcer is responsible for:

1. Candidate discovery
2. Candidate comparison
3. Approved part recommendation
4. Datasheet curation
5. Recording sourcing logic and risk

## Working Method

Phase2 should follow this pattern:

1. Main agent reads state and phase rule
2. Main agent invokes the sourcer role
3. Sourcer reads `spec/` and `architecture/` artifacts
4. Sourcer creates or updates:
   - `sourcing/candidate_parts.csv`
   - `sourcing/approved_parts.yaml`
   - `sourcing/selection_notes.md`
   - relevant files in `sourcing/datasheets/`
5. Main agent checks whether selection logic is traceable to requirements and architecture
6. Main agent runs:
   - `python scripts/update_index.py --project-root <repo>`
   - `python scripts/validate.py --project-root <repo>`
   - `python scripts/review.py --project-root <repo>`
7. Use reviewer or reviewer-style clean-context review to challenge the sourcing rationale
8. Revise until sourcing findings are resolved

## Required Outputs

- `sourcing/candidate_parts.csv`
- `sourcing/approved_parts.yaml`
- `sourcing/selection_notes.md`
- `sourcing/datasheets/`

## Required Inputs

At minimum, phase2 must use:

- `spec/requirements.md`
- `spec/constraints.md`
- `spec/open_questions.md`
- `spec/assumptions.md`
- `architecture/system_overview.md`
- `architecture/interface_matrix.md`
- `architecture/risk_register.md`

## Required Content

At minimum, the sourcing package must make visible:

1. The architectural role each selected part serves
2. The criteria used to compare candidates
3. The reason approved parts won
4. The reason serious alternatives were rejected
5. Residual sourcing or supply-chain risk
6. The datasheet evidence preserved for later phases

## Evidence Contract

Every approved part entry must carry these fields explicitly:

1. `source`
2. `rationale`
3. `confidence`
4. `unresolved_items`

Candidate rows should carry the same evidence trail where possible so the final decision can be audited without replaying chat.

## Parallel Comparison Requirement

Parallel or independent comparison is strongly encouraged in this phase when multiple part families or sourcing directions exist.

Use isolated comparisons when that helps reduce bias or improve coverage.

## Datasheet Requirement

Keep the datasheets that later phases actually need.

Phase2 should not leave behind a noisy pile of irrelevant PDFs. Preserve evidence with intent.

## Review Requirement

Before approval, reviewer involvement should challenge:

1. Whether the comparison criteria are real and sufficient
2. Whether the chosen parts actually fit the architecture
3. Whether hidden assumptions or risks are being ignored
4. Whether the preserved datasheets support the claimed decision logic

## Entry Conditions

Phase2 may start when:

1. `state.yaml.phase` is `phase2`
2. Phase0 and phase1 artifacts exist and are usable
3. The main agent has loaded `SKILL.md`, this phase rule, and `agents/sourcer.md`
4. The architecture is concrete enough to support part selection

## Exit Criteria

Phase2 is ready for review only when:

1. All required sourcing artifacts exist and are non-empty where applicable
2. The approved part set is traceable to the requirement and architecture baseline
3. Selection criteria and rejection reasons are explicit
4. Relevant datasheets are available for later phases
5. Sourcing risks are written down honestly
6. `sourcing/approved_parts.yaml` satisfies the schema contract in `schemas/approved_parts.schema.json`

Phase2 is ready to transition only when:

1. `scripts/update_index.py` has been run after the latest sourcing changes
2. `scripts/validate.py` passes
3. `scripts/review.py` has been run
4. Reviewer findings have been resolved
5. `scripts/review.py --approve` has been run
6. The project state allows transition

## Failure Modes

Do not close phase2 if any of the following is true:

1. Approved parts were chosen without visible comparison criteria
2. The architecture is too vague to justify the selection
3. Rejection reasons for meaningful alternatives are missing
4. Datasheets are missing, irrelevant, or badly curated
5. Sourcing risk has been softened or ignored
6. Evidence fields are missing or hand-wavy enough that later phases cannot trace the decision

If phase2 fails semantic review, keep the phase open and continue sourcing refinement rather than forcing progress.
