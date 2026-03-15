---
name: schematic
description: Orchestrate the end-to-end schematic-agent workflow for initialized project repositories. Use when Codex needs to run or continue the phase-based process defined by this repository: read workflow state, load the active phase rule, pick the right agent role, create or update phase artifacts, invoke deterministic scripts, run review and checkpoint gates, and advance the project through phase0 to phase5 without replacing script-owned validation or state transitions.
---
# Schematic

Drive the initialized project repository through a phase-based schematic design workflow.

Treat this skill as the top-level orchestrator. Make decisions, write artifacts, and route work. Leave deterministic operations to the repository scripts.

## Operating Model

Work in five layers and do not blur them:

1. `Makefile` is the human-friendly entrypoint.
2. `scripts/` performs deterministic operations such as bootstrap, init, status, indexing, validation, review state updates, checkpointing, transitions, and rendering.
3. `state.yaml` and `project_index.yaml` are the workflow source of truth.
4. `phases/*.md` defines what the current phase must accomplish.
5. `agents/*.md` defines the role to use for the current task.

Do not manually simulate what a script already owns.

## Main-Agent Principle

In every phase, the main agent acts as an orchestrator first and a specialist second.

The main agent should:

1. Read workflow state
2. Load the active phase rule
3. Decide which specialized agent role should perform the core phase work
4. Invoke that role with tight task-local context
5. Keep the conversation, repository artifacts, and workflow state aligned
6. Run the script-owned gates such as index, validate, review, checkpoint, and transition

Do not let the main agent drift into doing every task itself when a phase-specific agent exists.

The intended pattern is:

1. `SKILL.md` teaches the overall workflow and orchestration rules
2. `phases/<phase>.md` teaches what the active phase must accomplish
3. `agents/<role>.md` teaches the specialized role how to perform the core task
4. The main agent coordinates these layers and remains responsible for final synthesis and workflow control

## Hard Boundaries

Do:

1. Read the current state before acting.
2. Read only the current phase file and the agent file needed for the task.
3. Produce or update the phase artifacts on disk.
4. Call scripts at the required gates.
5. Use review loops before advancing phases.
6. Keep the repository auditable through index updates and checkpoints.

Do not:

1. Recreate project structure by hand if init scripts should do it.
2. Pretend validation passed without running `scripts/validate.py`.
3. Pretend review is complete without running `scripts/review.py`.
4. Edit `state.yaml` or `project_index.yaml` manually unless a script explicitly requires manual repair and the user has asked for that repair.
5. Jump phases or fake a transition instead of using `scripts/transition.py`.
6. Keep important reasoning only in chat when PRD requires it to be written to files.

## Startup Routine

At the start of work in an initialized project repository:

1. Run `python scripts/status.py --project-root <repo>` or `make status`.
2. Read `state.yaml` to confirm `phase`, `status`, `blocked`, `allow_transition`, `review_status`, and `pending_reviews`.
3. Read the active phase file from `phases/`.
4. Read the matching agent role from `agents/`.
5. Read only the input artifacts relevant to the active phase.
6. Decide whether the next action is:
   - artifact production,
   - artifact revision,
   - review,
   - approval after review,
   - checkpoint,
   - transition,
   - or render.

If the repository is not initialized, do not improvise the layout. Run `python scripts/init_project.py --target <path>` or `make init TARGET=<path>`.

## Preferred Commands

Prefer `make` when the target exists and the repository is being driven like a user project. Use direct Python script calls when you need explicit `--project-root` control.

Available entrypoints:

- `make bootstrap`
- `make init TARGET=<path>`
- `make status`
- `make index`
- `make validate`
- `make review`
- `make approve-review`
- `make checkpoint`
- `make phase0` through `make phase5`
- `make render`

Python equivalents exist in `scripts/`.

## Script Contract

Use scripts at these moments:

1. `scripts/bootstrap.py`
   Use to verify the environment and install project-local dependencies. In this repository it installs `lightpanda` and `pdf-to-markdown` into `.tools/`.
2. `scripts/init_project.py`
   Use to create a new runtime repository. Do not hand-build the project tree instead.
3. `scripts/status.py`
   Use at the beginning of every meaningful work session and after major gates if state may have changed.
4. `scripts/update_index.py`
   Use immediately after creating, deleting, or materially changing tracked artifacts.
5. `scripts/validate.py`
   Use after artifact updates and before any review approval or phase transition.
6. `scripts/review.py`
   Use when a phase deliverable is ready for review. This scaffolds or refreshes the phase review file and updates review state.
7. `scripts/review.py --approve`
   Use only after reviewer findings are resolved, the review artifact is semantically clean, and the project is genuinely ready to move forward.
8. `scripts/checkpoint.py`
   Use after a validated, reviewed milestone when there are actual git changes to preserve.
9. `scripts/transition.py <phase>`
   Use to move exactly one phase forward. Use `--allow-rollback` only when a recorded change request justifies rollback.
10. `scripts/render.py`
    Use only in `phase5` after `design/interconnect.json` is ready.

## Tool References

When browser execution is needed in this source repository:

1. Read `tools/lightpanda/README.md` before first use.
2. Prefer `./.tools/bin/lightpanda fetch --dump <url>` for fast one-shot page execution and DOM capture.
3. Use `./.tools/bin/lightpanda serve --host 127.0.0.1 --port 9222` only when a CDP endpoint is needed.
4. Set `LIGHTPANDA_DISABLE_TELEMETRY=true` for local agent workflows.

Treat `.tools/` as a local dependency directory, not as a project artifact to commit.

## Core Loop

Follow this loop every time:

1. Inspect state.
2. Load the active phase rule.
3. Decide which specialized agent should perform the core phase work.
4. Load the role definition needed for the current work.
5. Read the minimum required input artifacts.
6. Produce or revise the required output artifacts.
7. Run `scripts/update_index.py`.
8. Run `scripts/validate.py`.
9. Run `scripts/review.py`.
10. Invoke the reviewer role or reviewer-style clean-context subagent when the phase requires approval review.
11. Address review findings by updating artifacts, then rerun index and validate as needed.
12. Run `scripts/review.py --approve` only when reviewer findings are resolved and review is clean.
13. Run `scripts/checkpoint.py`.
14. Run `scripts/transition.py <next-phase>` when the current phase is complete and approved.

Do not transition in the same breath as draft artifact creation. Treat review approval as a real gate.

## Phase Routing

Route work by `state.yaml.phase`:

- `phase0`
  Main agent stays in orchestration mode.
  Load `phases/phase0.md` and invoke `agents/clarifier.md` as the primary worker.
  Convert user intent into explicit requirements, constraints, assumptions, and open questions.
  Detect X-Y problems and restate the real goal before locking requirements.
  Use `agents/reviewer.md` when an independent requirement-quality check is needed before approval.

- `phase1`
  Main agent stays in orchestration mode.
  Load `phases/phase1.md` and invoke `agents/architect.md` as the primary worker.
  Turn phase0 outputs into a system design, interface matrix, and risk register.
  `agents/reviewer.md` is a required approval-gate role in this phase, not an optional helper.

- `phase2`
  Main agent stays in orchestration mode.
  Load `phases/phase2.md` and invoke `agents/sourcer.md` as the primary worker.
  Research candidate parts, compare tradeoffs, choose approved parts, and curate datasheets.
  Use `agents/reviewer.md` to challenge sourcing rationale before approval.

- `phase3`
  Main agent stays in orchestration mode.
  Load `phases/phase3.md` and invoke the best available sourcing or handbook-focused role.
  Turn approved parts and datasheets into handbook guidance that is implementation-ready.
  Use `agents/reviewer.md` when handbook quality or omission risk is material.

- `phase4`
  Main agent stays in orchestration mode.
  Load `phases/phase4.md` and invoke `agents/architect.md` as the primary design worker.
  Convert requirements, architecture, and handbook constraints into `design/interconnect.json` and supporting notes.
  `agents/reviewer.md` is a required approval-gate role in this phase and must independently attack the final design before approval.

- `phase5`
  Main agent stays in orchestration mode.
  Load `phases/phase5.md` and invoke the appropriate design-preparation role before calling `scripts/render.py`.
  Verify render inputs and log outputs.
  Use `agents/reviewer.md` to judge render readiness and output traceability before approval when needed.

Use `agents/reviewer.md` as the system's approval-gate reviewer whenever a phase deliverable needs semantic signoff.

## Task Allocation

Assign work by role, not by convenience:

1. `clarifier`
   Own requirement extraction, contradiction detection, X-Y problem handling, assumptions, and open questions.
2. `architect`
   Own solution decomposition, interface definition, interconnect logic, and design-level risk analysis.
3. `sourcer`
   Own candidate research, selection criteria, approved part decisions, datasheet curation, and datasheet-derived constraints.
4. `reviewer`
   Own semantic review, missing-risk detection, inconsistency detection, and go or no-go approval-gate judgment for delivery readiness.

## Reviewer Principle

Treat the reviewer as an approval-gate role, not as a cosmetic assistant.

The reviewer should:

1. Challenge the active phase output independently
2. Look for hidden assumptions, inconsistencies, and downstream failure points
3. Write findings into the phase review artifact
4. Block approval when semantic quality is not strong enough

Do not use the reviewer merely to confirm that the files exist or to produce lightweight reassurance.

In phase1 and phase4, reviewer involvement is mandatory before approval.

## Subagent Protocol

Use subagents deliberately. They are not a default replacement for thinking; they are a tool for isolation, adversarial review, and parallel comparison.

Start a subagent when one of these conditions is true:

1. A phase requires independent review before delivery.
2. Two or more candidate solutions or parts must be compared in parallel.
3. You need a clean-context pass to detect hidden assumptions or reasoning contamination.
4. The active task is large enough that decomposition improves quality without weakening traceability.

Do not start a subagent when:

1. The task is a simple deterministic script invocation.
2. The needed work is a small edit in the current artifact and no independent judgment is required.
3. You cannot provide the subagent with a tight task-local context package.

When launching a subagent, provide only:

1. The current phase.
2. The exact task to perform.
3. The required input files for that task.
4. The expected output artifact or review format.
5. Any hard constraints that must not be violated.

Do not provide:

1. The full project conversation history.
2. Irrelevant artifacts from other phases.
3. Your preferred answer when asking for review.
4. Hidden conclusions that would bias an independent check.

Require every subagent to return:

1. A concise decision or recommendation.
2. The evidence path, citing the files it used.
3. Any risks, gaps, or contradictions found.
4. The exact artifact changes or review findings it proposes.

The parent agent remains responsible for:

1. Deciding whether a subagent is needed.
2. Framing the task and context package.
3. Evaluating the returned result.
4. Merging useful findings into project artifacts.
5. Running index, validate, review, checkpoint, and transition scripts.

When using multiple agents or subagents:

1. Share only the current task, required input artifacts, and expected output artifacts.
2. Do not share the full project conversation history.
3. Do not leak your preferred answer into review prompts.
4. Ask independent reviewers to judge artifacts, not to agree with your plan.
5. Merge findings back into the repository artifacts explicitly.

## Subagent Routing By Phase

Use subagents in these patterns:

1. `phase0`
   Optional.
   Use a reviewer-style subagent only when requirements are ambiguous, contradictory, or likely affected by X-Y problem framing.

2. `phase1`
   Required before delivery.
   Start at least one clean-context review subagent to challenge the architecture, interface boundaries, and risk register.

3. `phase2`
   Strongly recommended.
   Use parallel sourcer subagents to evaluate different candidate parts or sourcing directions independently, then reconcile results in the main thread.

4. `phase3`
   Optional.
   Use a review subagent when handbook extraction from datasheets is complex or safety-critical and needs a second pass for omissions.

5. `phase4`
   Required before approval.
   Use `agents/reviewer.md` or a reviewer-style clean-context subagent to look for missing nets, interface mismatches, and contradictions between architecture, handbook constraints, and final interconnect output.

6. `phase5`
   Optional before render, useful after render failure.
   Use a subagent to inspect render readiness or diagnose mismatch between `design/interconnect.json`, design notes, and render outputs.

## Review Discipline

Treat review as a first-class phase gate.

For every phase:

1. Finish draft artifacts.
2. Update the index.
3. Validate structure and required files.
4. Generate or refresh the review artifact with `scripts/review.py`.
5. Use the reviewer role to inspect semantic quality:
   - missing requirements,
   - weak assumptions,
   - design contradictions,
   - sourcing gaps,
   - handbook omissions,
   - JSON inconsistency,
   - render readiness.
6. In phase1 and phase4, reviewer involvement is mandatory before approval.
7. Before approval, run one or more clean-context review subagents when the phase calls for independent review.
8. Write findings into `review/<phase>_review.md`.
9. Revise artifacts until blocking findings are cleared.
10. Approve review with `scripts/review.py --approve`.

Do not approve review while `pending_reviews` is non-empty or while the review document still contains unresolved blockers.

## Transition Rules

Advance a phase only when all of the following are true:

1. Required phase artifacts exist and are non-empty.
2. `scripts/update_index.py` has been run after the latest artifact changes.
3. `scripts/validate.py` passes.
4. Review has been scaffolded, completed, and approved.
5. `state.yaml.allow_transition` is true.

If a phase needs to be revisited after completion, create or update a change request record under `review/change_requests/` before using rollback.

## Artifact Policy

Persist important outputs to disk immediately. At minimum, maintain:

- `spec/` for clarified requirements
- `architecture/` for solution design
- `sourcing/` for candidate parts, approved parts, notes, and datasheets
- `handbook/` for datasheet-derived design guidance
- `design/` for interconnect JSON and notes
- `render/` for rendered outputs and logs
- `review/` for review records and change requests

If a result matters to later phases, it must exist as a file and be indexed.

## Failure Handling

Stop and surface the issue instead of improvising when:

1. `state.yaml` contains an unknown phase.
2. Validation fails and the cause is unclear.
3. Review reveals a blocker that changes upstream assumptions.
4. A rollback is needed but no change request exists.
5. Required inputs for the active phase are missing.
6. Render input is incomplete or inconsistent with design notes.

When blocked:

1. Record the blocker in the appropriate artifact or review file.
2. Do not force a transition.
3. Ask for the missing user decision only if it cannot be resolved from repository context.

## Writing Style For This Skill

When acting under this skill:

1. Be concise in chat and detailed in files.
2. Separate confirmed facts, assumptions, open questions, and decisions.
3. Prefer structured artifacts over freeform notes.
4. Preserve traceability from each phase output to its inputs.
5. Keep the context window small by loading only the active phase and relevant artifacts.
