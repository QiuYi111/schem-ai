# Phase5: Rendering

## Goal

Render the structured interconnect into a schematic artifact and a traceable render log.

This phase is where the project turns the final design representation into renderer output, while preserving enough traceability to diagnose render or upstream design failures.

## Main-Agent Role

In phase5, the main agent acts as an orchestrator.

Its job is to:

1. Read workflow state and confirm phase5 is active
2. Read this phase rule
3. Ensure the design package is ready for rendering
4. Invoke the renderer through the script-owned path
5. Invoke reviewer judgment when render readiness or output validity is in question
6. Run index, validate, review, checkpoint, and final transition or completion gates

## Primary Worker

Use the architect role as the default design-readiness worker before rendering.

In phase5, that worker is responsible for:

1. Checking that the final design artifacts are coherent enough to render
2. Ensuring render input does not rely on hidden interpretation
3. Helping explain render issues if output and design disagree

Rendering itself is owned by `scripts/render.py`.

## Working Method

Phase5 should follow this pattern:

1. Main agent reads state and phase rule
2. Main agent checks render readiness against the phase4 outputs
3. Main agent runs `python scripts/render.py --project-root <repo>`
4. Main agent runs:
   - `python scripts/update_index.py --project-root <repo>`
   - `python scripts/validate.py --project-root <repo>`
   - `python scripts/review.py --project-root <repo>`
5. Use reviewer involvement when render output, render log, and design intent may not align
6. Revise upstream artifacts or rerender as needed until findings are resolved

## Required Outputs

- `render/schematic_output/`
- `render/render_log.md`

## Required Inputs

At minimum, phase5 must use:

- `design/interconnect.json`
- `design/design_notes.md`

## Required Content

At minimum, phase5 must preserve:

1. Render outputs in `render/schematic_output/`
2. Render traceability in `render/render_log.md`
3. Enough information to tell whether a render issue is caused by the renderer or by weak upstream design

## Render Requirement

The renderer should not be asked to guess what the design means.

If phase4 output is too weak, contradictory, or underexplained, the main agent should surface that and push the issue back instead of pretending render success means design success.

## Review Requirement

Reviewer involvement should challenge:

1. Whether the render output matches the design intent
2. Whether render failures reveal upstream design ambiguity
3. Whether render logs are sufficient for traceability and debugging
4. Whether the project is actually ready to treat the render result as a valid deliverable

## Entry Conditions

Phase5 may start when:

1. `state.yaml.phase` is `phase5`
2. Phase4 design artifacts exist and are usable
3. The main agent has loaded `SKILL.md`, this phase rule, and any relevant design-readiness role
4. The render input is concrete enough to avoid hidden interpretation

## Exit Criteria

Phase5 is ready for review only when:

1. Renderer output exists in `render/schematic_output/`
2. `render/render_log.md` exists and is non-empty
3. Render output is traceable to the current design input
4. Any render failure or mismatch has been investigated honestly

Phase5 is complete only when:

1. `scripts/update_index.py` has been run after the latest render outputs
2. `scripts/validate.py` passes
3. `scripts/review.py` has been run
4. Reviewer findings have been resolved
5. `scripts/review.py --approve` has been run
6. The project state allows closure or final transition behavior

## Failure Modes

Do not close phase5 if any of the following is true:

1. Render output exists but does not match the intended design
2. Render success is being used to hide weak upstream design
3. Render logs are too thin to explain what happened
4. The project cannot distinguish renderer limitations from design problems

If phase5 fails semantic review, keep the phase open and continue investigation or upstream correction rather than forcing completion.
