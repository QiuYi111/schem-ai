# Hooks

Hooks are lightweight guardrails around workflow actions.

In this project, hooks exist to protect quality and enforce workflow discipline at key boundaries. They do not own the workflow state machine.

## Core Principle

Hooks are guards, not governors.

Use hooks to:

1. Run pre-checks before important actions
2. Run post-checks after important actions
3. Block illegal or unsafe transitions
4. Trigger deterministic validation or checkpoint helpers at the right boundaries
5. Enforce repository hygiene around workflow actions

Do not use hooks to:

1. Store workflow state
2. Decide the current phase
3. Replace `state.yaml`
4. Replace `scripts/transition.py`
5. Replace the main-agent orchestration logic in `SKILL.md`
6. Perform high-token reasoning or semantic design work

State belongs in `state.yaml`. Transition logic belongs in scripts. Semantic judgment belongs in agents. Hooks only guard the edge.

## What Hooks Should Guard

Hooks are most useful at these boundaries:

1. Before transition
   Check whether required artifacts exist, review is complete, and the state allows movement

2. After transition
   Confirm the repository is in the expected post-transition state and remind the workflow to regenerate any needed scaffolding

3. Before review approval
   Ensure validation has passed and review artifacts are present

4. After review approval
   Trigger follow-up deterministic actions such as checkpoint or index refresh when appropriate

5. Before render
   Ensure final design inputs exist and are not obviously stale or missing

## Recommended Hook Categories

Use the directory as a place for small guard scripts or wrappers grouped by intent.

Recommended naming scheme:

- `pre-transition-*`
- `post-transition-*`
- `pre-review-*`
- `post-review-*`
- `pre-render-*`
- `post-render-*`

If the project later adds executable hook scripts, keep them small and deterministic.

## Design Rules

A good hook should be:

1. Fast
2. Deterministic
3. Local in scope
4. Easy to understand
5. Safe to run repeatedly

A good hook should not:

1. Mutate unrelated project files
2. Encode hidden workflow rules that are absent from scripts or docs
3. Depend on long conversational context
4. Produce major project artifacts
5. Hide failures behind silent fallback behavior

If a rule matters enough to define the workflow, put it in the phase docs or scripts first. Hooks should enforce that rule, not invent it.

## Relationship To Scripts

Hooks should generally call or wrap existing deterministic scripts rather than reimplementing them.

Examples:

1. Use a pre-transition hook to call `scripts/validate.py`
2. Use a pre-approve hook to verify review artifacts exist
3. Use a post-approve hook to call `scripts/checkpoint.py` if that behavior is desired

Prefer reusing script entrypoints over embedding duplicate logic in hooks.

## Relationship To Agents

Agents should know hooks exist, but should not rely on hooks as hidden intelligence.

The main agent should still:

1. Read `state.yaml`
2. Read the active phase document
3. Invoke the correct specialized agent
4. Run the required scripts explicitly

Hooks are there to catch violations or automate small guard actions around those steps.

## Failure Behavior

When a hook fails, it should fail loudly and block the guarded action.

A hook failure should communicate:

1. What check failed
2. Why the guarded action is unsafe or illegal
3. Which script or artifact needs attention

Do not allow hooks to fail silently.

## Minimal Roadmap

If we later implement executable hooks, the first useful ones are:

1. Pre-transition validation hook
2. Pre-approve review-integrity hook
3. Pre-render design-readiness hook

These provide guard value without turning hooks into a second workflow engine.
