# Phase0: Requirement Clarification

## Goal

Turn the user's natural-language request into explicit, reviewable, file-backed requirement artifacts.

This phase is not for solution design. It is for understanding the real problem well enough that phase1 can begin without guessing.

## Main-Agent Role

In phase0, the main agent acts as an orchestrator.

Its job is to:

1. Read workflow state and confirm phase0 is active
2. Read this phase rule
3. Invoke the clarifier role for direct requirement clarification work
4. Keep the conversation and repository aligned
5. Ensure outputs are written to `spec/`
6. Run index, validate, review, and later transition gates

The main agent should not try to do ad hoc requirement clarification without loading the clarifier role.

## Primary Worker

Use `agents/clarifier.md` as the primary specialized agent for this phase.

The clarifier is responsible for:

1. Running a structured scan of the problem space
2. Detecting X-Y problem risk
3. Clarifying electrical parameters, I/O, system behavior, and constraints
4. Separating facts, assumptions, and open questions
5. Producing a structured restatement for confirmation

## Working Method

Phase0 should follow this pattern:

1. Main agent reads state and phase rule
2. Main agent invokes the clarifier role
3. Clarifier interacts with the user using a scan-based clarification process
4. Clarifier writes or updates the required `spec/` artifacts
5. Main agent reviews whether the artifacts actually reflect the latest understanding
6. Main agent runs:
   - `python scripts/update_index.py --project-root <repo>`
   - `python scripts/validate.py --project-root <repo>`
   - `python scripts/review.py --project-root <repo>`
7. If needed, the main agent or clarifier performs another clarification loop
8. Phase0 is only complete after the requirement baseline is clear enough for phase1

## Required Outputs

- `spec/requirements.md`
- `spec/constraints.md`
- `spec/open_questions.md`
- `spec/assumptions.md`

## Required Content

At minimum, the artifacts must cover:

1. The user's real goal
2. The user's proposed solution idea, if any
3. Electrical parameters
4. Inputs and outputs
5. Required system functions
6. Design constraints
7. Known assumptions
8. Open questions
9. X-Y problem risk, if present

## Scan Requirement

The clarifier must use a structured scan approach rather than only reacting to the last user message.

The scan must cover:

1. Real objective
2. Proposed implementation path
3. Electrical environment
4. I/O and external interfaces
5. System behavior and operating modes
6. Constraints and fixed boundaries
7. Missing data and requirement red flags

If a dimension is unknown, it must be recorded as unknown or assumed, not silently invented.

## Restatement Requirement

Before phase0 is considered complete, the clarifier must restate the interpreted problem in structured form.

That restatement must include:

1. The inferred real goal
2. The user-proposed path, if any
3. Confirmed requirements
4. Confirmed constraints
5. Assumptions
6. Open questions
7. Any X-Y problem or contradiction signals

If the restatement has not been confirmed by the user, or repository context still contains serious ambiguity, phase0 should remain open.

## Subagent Guidance

The clarifier may use a clean-context reviewer-style subagent when:

1. The request is contradictory
2. X-Y problem risk is high
3. The requirement set is dense enough that an independent read may catch hidden assumptions

Subagents in phase0 should receive only:

1. The user request
2. Current draft `spec/` files
3. The specific review question

The main agent remains responsible for synthesis, user-facing alignment, and artifact updates.

## Entry Conditions

Phase0 may start when:

1. `state.yaml.phase` is `phase0`
2. The repository is initialized
3. The main agent has loaded `SKILL.md`, this phase rule, and `agents/clarifier.md`

## Exit Criteria

Phase0 is ready for review only when:

1. All four `spec/` files exist and are non-empty
2. The user's real goal has been distinguished from any proposed implementation
3. Electrical parameters, I/O, functions, and constraints have been scanned
4. Assumptions and open questions are clearly separated from confirmed facts
5. A structured restatement has been produced

Phase0 is ready to transition only when:

1. `scripts/update_index.py` has been run after the latest artifact changes
2. `scripts/validate.py` passes
3. `scripts/review.py` has been run
4. Review findings have been resolved
5. `scripts/review.py --approve` has been run
6. The project state allows transition

## Failure Modes

Do not close phase0 if any of the following is true:

1. The user goal is still ambiguous
2. The artifacts contain hidden assumptions presented as facts
3. Electrical or interface requirements are still materially undefined
4. The user proposal has not been separated from the true requirement
5. Open questions that block phase1 are buried or unstated

If phase0 fails validation or semantic review, keep the phase open and continue clarification rather than forcing progress.
