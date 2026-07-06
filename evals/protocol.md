# Evaluation Protocol

This is the durable methodology for harness evaluations. Individual test plans define the task; this file defines how every test runs. It supersedes the arm design in `initial-ab-test-plan.md`, which is kept as the record of run 1.

## Why This Exists

Run 1 (static-focus-board) had four methodology failures that this protocol prevents:

1. One run per arm, so normal output variance could explain every observed difference.
2. Arm definitions lived in prose, and the situational arm drifted into loading the full skill.
3. The orchestrating agent scored its own unblinded runs, and totals were never computed — a 51-51 tie was reported as a win.
4. "Speed and cost" was scored by feel with no measured tokens, time, or tool calls.

## Arms

| Arm | Setup | What it measures |
|-----|-------|------------------|
| A: Control | No harness content of any kind | Baseline model capability |
| B: Harness | `fable-task-harness/SKILL.md` loaded at start; references loaded only per its trigger table | The product as shipped |
| C: Full-load | `SKILL.md` plus every file in `references/` loaded at start | Ceiling versus token cost of full context |

Arm setup text is frozen verbatim in `arm-prompts/`. Use it exactly; any deviation invalidates the run.

## Run Requirements

- At least 3 runs per arm per task. Report every run; compare medians.
- Separate, isolated contexts. No run sees another run's output or transcript.
- Same frozen task prompt, tools, and time expectations for all arms.
- No manual improvement of outputs before scoring.
- Record per-run metadata (below) before scoring anything.

## Per-Run Metadata

Each run folder must contain a `run-meta.md` with:

```md
# Run Metadata

- Task:
- Arm: control | harness | full-load
- Run number:
- Date:
- Model ID:
- Harness version: (from fable-task-harness/SKILL.md frontmatter; n/a for control)
- Arm prompt file used:
- Wall time start (ISO 8601):
- Wall time end (ISO 8601):
- Token usage (input/output):
- Tool calls (top-level assistant invocations):
- Tool operations (underlying operations, if separately countable):
- Files read (count):
- Clarification questions asked (count):
```

Metadata rules, added after the decoy-config-repo battery where three runs lacked start times and tool-call counts mixed definitions:

- Capture the start timestamp as the first action of the run, not retroactively.
- Tool calls means top-level assistant tool invocations (a parallel batch counts as one); underlying operations go on their own line.
- When the runtime does not expose a value, write the exact literal `not reported` — never leave a line blank or paraphrase.

## Task Batteries

A battery must include at least one task from each group:

- Build tasks (greenfield artifacts) — measure output routing, simplicity, and verification.
- Trap tasks (seeded ground truth) — measure context recovery, source-of-truth choice, and parameter hygiene. See the trap candidates in `candidate-simple-projects.md`.

Greenfield build tasks alone cannot detect harness value: a frontier model completes them unaided, and run 1 demonstrated exactly that.

## Objective Checks

Objective checks must target user-visible capabilities, not implementation details. A smoke test that requires a specific DOM shape — `data-action` attributes, particular element IDs, task text outside inputs — will fail valid implementations. Allow variants: text may render inside inputs, buttons may be identified by label, destructive actions may confirm first. When a check fails, decide whether the run failed the capability or the checker assumed an implementation; a checker bug is fixed and re-run, not scored against the arm.

## Scoring

1. After all runs finish, copy artifacts into neutrally named folders (`run-01/`, `run-02/`, ...) with a private mapping kept aside.
2. Run the uniform parent smoke test (or task-specific objective checks) against every run before subjective scoring.
3. Score with `rubric.md` blind, then unblind and attach the mapping.
4. Compute totals. Artifact-quality ties break toward the arm with lower measured cost (tokens, then wall time, then tool calls).
5. Score process metrics from transcripts, not from the artifact: guessed parameters, wrong-file reads or edits, verification depth reached, unrequested features shipped.
6. Keep artifact facts and evidence facts separate in ground-truth rules. Missing process evidence (a deleted log, an absent transcript) caps process-dimension scores and gets flagged, but does not fail artifact dimensions unless bypass is affirmatively indicated — non-matching output, a modified tool, or notes contradicted by the artifacts. The undocumented-local-tool battery scored byte-correct reports as Correctness 1 because its rules conflated the two; do not repeat that.

## Source Learning

Every review must end with source-improvement candidates: recurring issue, upstream file, suggested change. Route fixes to the harness, templates, or this protocol — not to run outputs. Record which harness version the findings apply to.
