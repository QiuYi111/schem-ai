# Phase4: Interconnect Design

## Goal

Convert the requirement baseline, architecture, and handbook constraints into the final structured schematic design representation.

This phase is where the project turns system intent into a concrete, reviewable interconnect model that the renderer can consume.

## Main-Agent Role

In phase4, the main agent acts as an orchestrator.

Its job is to:

1. Read workflow state and confirm phase4 is active
2. Read this phase rule
3. Invoke the architect role as the primary design worker
4. Invoke the reviewer role as the primary review worker before approval
5. Keep the design artifacts aligned with requirements, architecture, and handbook constraints
6. Run index, validate, review, checkpoint, and transition gates

The main agent should not improvise the final schematic design without loading the architect role.

## Primary Design Worker

Use `agents/architect.md` as the primary specialized agent for this phase.

In phase4, the architect is responsible for:

1. Reading the requirement baseline
2. Reading the architecture baseline
3. Reading handbook constraints from selected parts
4. Turning those inputs into the final structured interconnect design
5. Recording rationale for non-obvious connections or boundary choices

## Primary Review Worker

Use `agents/reviewer.md` as the primary specialized reviewer for this phase.

The reviewer is responsible for:

1. Checking consistency between requirements, architecture, handbook guidance, and interconnect output
2. Looking for missing nets, interface mismatches, hidden assumptions, and underdefined boundaries
3. Deciding whether the design is concrete enough for rendering

## Working Method

Phase4 should follow this pattern:

1. Main agent reads state and phase rule
2. Main agent invokes the architect role
3. Architect reads `spec/`, `architecture/`, and `handbook/` artifacts
4. Architect writes or updates:
   - `design/interconnect.json`
   - `design/design_notes.md`
5. Main agent checks whether the design is traceable to the requirement and architecture baseline
6. Main agent runs:
   - `python scripts/update_index.py --project-root <repo>`
   - `python scripts/validate.py --project-root <repo>`
   - `python scripts/review.py --project-root <repo>`
7. Main agent invokes the reviewer role in clean context to attack the design
8. Design is revised until reviewer findings are resolved
9. Phase4 is only complete when the interconnect model is stable enough for rendering without hidden interpretation

## Required Outputs

- `design/interconnect.json`
- `design/design_notes.md`

## Required Inputs

At minimum, phase4 must use:

- `spec/requirements.md`
- `spec/constraints.md`
- `spec/open_questions.md`
- `spec/assumptions.md`
- `architecture/system_overview.md`
- `architecture/interface_matrix.md`
- `architecture/risk_register.md`
- relevant `handbook/*.md`

Phase4 should not be driven by chat memory alone.

## Required Content

At minimum, the design output must capture:

1. The major interconnect structure implied by the architecture
2. The required interfaces and boundaries
3. Key nets, buses, control relationships, power relationships, reset relationships, clock relationships, and protection relationships where relevant
4. Design assumptions that materially affect connectivity
5. Rationale for non-obvious or high-risk design choices

## Design Requirement

The architect must produce a real final design representation, not a vague bridge document.

The design must answer:

1. How the modules from the architecture are concretely connected
2. How handbook constraints shape those connections
3. Which boundaries are fixed versus assumed
4. What later rendering should not have to infer on its own

If the architect cannot produce a trustworthy interconnect design because upstream artifacts are weak or contradictory, phase4 must surface that instead of hiding it.

## Review Requirement

Reviewer involvement is mandatory in phase4.

Before approval, the reviewer must attack the design for:

1. Missing or inconsistent interfaces
2. Missing critical relationships such as power, reset, clock, or protection where relevant
3. Contradictions between architecture and interconnect output
4. Contradictions between handbook constraints and interconnect output
5. Underexplained design choices in `design/design_notes.md`
6. Design ambiguity that would force the renderer to guess

Phase4 should not be approved until reviewer findings are resolved or explicitly documented as accepted risk.

## Entry Conditions

Phase4 may start when:

1. `state.yaml.phase` is `phase4`
2. Phase0, phase1, and phase3 artifacts exist and are usable
3. The main agent has loaded `SKILL.md`, this phase rule, `agents/architect.md`, and `agents/reviewer.md`
4. The architecture and handbook baseline is strong enough to support final interconnect design

If the architecture or handbook artifacts are too weak, do not force phase4. Push the issue back explicitly.

## Exit Criteria

Phase4 is ready for review only when:

1. `design/interconnect.json` exists and is non-empty
2. `design/design_notes.md` exists and is non-empty
3. The design is traceable to requirements, architecture, and handbook constraints
4. The design is concrete enough that rendering does not require hidden interpretation
5. Design assumptions and non-obvious choices are made explicit

Phase4 is ready to transition only when:

1. `scripts/update_index.py` has been run after the latest design changes
2. `scripts/validate.py` passes
3. `scripts/review.py` has been run
4. Reviewer findings have been incorporated or resolved
5. `scripts/review.py --approve` has been run
6. The project state allows transition

## Failure Modes

Do not close phase4 if any of the following is true:

1. The interconnect design is only a vague translation of architecture prose
2. Important nets or interface relationships are missing
3. The design notes are insufficient to explain non-obvious choices
4. Rendering would still require hidden assumptions
5. The design conflicts with handbook constraints or architectural boundaries
6. Independent review has not challenged the output

If phase4 fails semantic review, keep the phase open and continue design refinement rather than forcing progress.
