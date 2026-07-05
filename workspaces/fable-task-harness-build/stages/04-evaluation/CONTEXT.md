# Stage 04: Evaluation

Use this stage when designing or running control, always-on, and situational harness tests.

## Inputs

| Source | File/Location | Section/Scope | Why |
|--------|---------------|---------------|-----|
| Master plan | `../../../../docs/fable-pseudo-harness-master.md` | A/B/C Test Protocol | Accepted test design |
| Harness skill | `../../../../fable-task-harness/SKILL.md` | Modes | What is being tested |
| Project tenets | `../../../../knowledge/wiki/project-structure-tenets.md` | Build Partial Autonomy First | Evaluation posture |
| Templates | `../../../../fable-task-harness/templates/harness-checklist.md` | Full file | Checklist basis |
| Candidate projects | `../../../../evals/candidate-simple-projects.md` | Full file | Test selection |
| Rubric | `../../../../evals/rubric.md` | Full file | Scoring |
| Initial plan | `../../../../evals/initial-ab-test-plan.md` | Full file | First run protocol |

## Process

1. Choose one frozen task prompt.
2. Define isolated contexts for control, always-on, and situational runs.
3. Score artifact and process with a blind rubric where practical.
4. Track repeated corrections as source-improvement signals.
5. Save evaluation artifacts under `evals/`.

## Outputs

| Artifact | Location | Format |
|----------|----------|--------|
| Evaluation plan | `../../../../evals/` | Markdown |
| Run artifacts | `../../../../evals/runs/` | Markdown or project files |
| Review rubric | `../../../../evals/` | Markdown |

## Audit

| Check | Pass condition |
|-------|----------------|
| Isolation | Runs do not share generated context |
| Rubric | Correctness, completeness, simplicity, maintainability, UX, tool use, context recovery, verification, speed, and intervention are scored |
| Source learning | Recurring corrections are routed back to source files |
