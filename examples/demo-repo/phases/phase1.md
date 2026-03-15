# Phase1: Solution Design

## Goal

Convert the clarified requirement baseline into a reviewable system architecture that downstream phases can actually use.

This phase is not for part selection or detailed implementation. It is for deciding the system structure, module boundaries, interfaces, architectural tradeoffs, and major risks early enough that the rest of the workflow is built on a coherent design.

## Main-Agent Role

In phase1, the main agent acts as an orchestrator.

Its job is to:

1. Read workflow state and confirm phase1 is active
2. Read this phase rule
3. Invoke the architect role as the primary specialized worker
4. Keep the architecture artifacts aligned with the requirement baseline
5. Ensure unresolved tensions are made explicit rather than silently absorbed
6. Run index, validate, review, checkpoint, and transition gates

The main agent should not perform freeform architecture work without loading the architect role.

## Primary Worker

Use `agents/architect.md` as the primary specialized agent for this phase.

The architect is responsible for:

1. System decomposition
2. Functional boundary definition
3. Interface definition
4. Architectural tradeoff reasoning
5. Requirement-to-solution mismatch detection
6. Risk identification and exposure
7. Preparing the design for adversarial review

## Working Method

Phase1 should follow this pattern:

1. Main agent reads state and phase rule
2. Main agent invokes the architect role
3. Architect reads the `spec/` requirement baseline in depth
4. Architect defines the major system structure and boundaries
5. Architect writes or updates the required `architecture/` artifacts
6. Main agent checks whether the architecture is traceable to the requirement baseline
7. Main agent runs:
   - `python scripts/update_index.py --project-root <repo>`
   - `python scripts/validate.py --project-root <repo>`
   - `python scripts/review.py --project-root <repo>`
8. Before approval, the architect or main agent launches clean-context review subagents to attack the design
9. Architecture is revised until review findings are resolved
10. Phase1 is only complete when the architecture is stable enough to support sourcing and later design work

## Required Outputs

- `architecture/system_overview.md`
- `architecture/interface_matrix.md`
- `architecture/risk_register.md`

## Required Content

At minimum, the architecture artifacts must cover:

1. The overall system objective in architectural terms
2. Major modules or subsystems
3. The responsibility and boundary of each module
4. Interfaces between modules
5. Interfaces to external systems
6. Architectural rationale for major decisions
7. Key tradeoffs
8. Architectural risks
9. Requirement gaps or assumptions that materially affect the design

## Design Requirement

The architect must produce a real system design, not a paraphrase of the requirements.

The design must answer:

1. How the system is partitioned
2. Why it is partitioned that way
3. Where each major function belongs
4. How modules interact
5. Which requirements or constraints drove the architecture
6. What is still risky or underconstrained

If the requirement baseline is too weak to support a trustworthy design, phase1 must surface that weakness instead of hiding it.

## Interface Requirement

The interface definition must be concrete enough for downstream phases to use as a design contract.

At minimum, the interface model must make visible:

1. Source and destination or ownership where meaningful
2. Data, control, power, or clock relationships where relevant
3. External integration points
4. Major assumptions on electrical level, timing, protocol, or isolation
5. Boundaries that must remain stable later

If interfaces are still too fuzzy for sourcing or interconnect design to proceed, phase1 is not done.

## Risk Requirement

Risk work is mandatory in phase1.

The architecture must explicitly expose:

1. Structural risks
2. Requirement-to-solution mismatch risks
3. Integration risks
4. Timing or performance risks
5. Risks caused by assumptions or unresolved questions
6. Places where later sourcing or design work may fail because the architecture is weakly supported

Do not treat risk capture as a formality.

## Review Requirement

Phase1 must be reviewed aggressively before approval.

At least one clean-context review subagent is required before phase1 can be approved.

That review should challenge:

1. Module partitioning
2. Interface completeness
3. Hidden coupling
4. Missing rationale
5. Understated risks
6. Design choices that rely on weak assumptions

When helpful, use an alternative-architecture subagent to test whether a different decomposition better fits the same requirement baseline.

## Entry Conditions

Phase1 may start when:

1. `state.yaml.phase` is `phase1`
2. Phase0 artifacts exist and are usable
3. The main agent has loaded `SKILL.md`, this phase rule, and `agents/architect.md`
4. The requirement baseline is strong enough to support architectural reasoning

If phase0 outputs are too weak, contradictory, or underconfirmed, do not force phase1. Push the issue back explicitly.

## Exit Criteria

Phase1 is ready for review only when:

1. All three `architecture/` files exist and are non-empty
2. The architecture is traceable to the requirement baseline
3. Module boundaries are clear enough to guide downstream work
4. Interfaces are explicit enough to support later sourcing and interconnect work
5. Major tradeoffs and design tensions are written down
6. Architectural risks have been captured honestly

Phase1 is ready to transition only when:

1. `scripts/update_index.py` has been run after the latest architecture changes
2. `scripts/validate.py` passes
3. `scripts/review.py` has been run
4. Clean-context review subagent findings have been incorporated
5. Review findings have been resolved
6. `scripts/review.py --approve` has been run
7. The project state allows transition

## Failure Modes

Do not close phase1 if any of the following is true:

1. The architecture is only a reformatted summary of requirements
2. Module boundaries are hand-wavy or overlapping
3. Interfaces are too vague for downstream use
4. Risks are understated or missing
5. Major architectural choices are not justified
6. Requirement gaps that affect design have been buried
7. The design has not survived independent clean-context review

If phase1 fails semantic review, keep the phase open and continue design refinement rather than forcing progress.
