# Stage 04: Evaluation

Use this stage when designing or running control, harness, and full-load evaluation arms.

## Inputs

| Source | File/Location | Section/Scope | Why |
|--------|---------------|---------------|-----|
| Protocol | `../../../../evals/protocol.md` | Full file | Governing methodology for every run |
| Arm prompts | `../../../../evals/arm-prompts/` | Relevant arm files | Frozen verbatim setup text |
| Harness skill | `../../../../fable-task-harness/SKILL.md` | Frontmatter and Reference Triggers | What is being tested, and its version |
| Master plan | `../../../../docs/fable-pseudo-harness-master.md` | Revision: Post-Eval Restructure | Accepted test design decisions |
| Project tenets | `../../../../knowledge/wiki/project-structure-tenets.md` | Build Partial Autonomy First | Evaluation posture |
| Candidate projects | `../../../../evals/candidate-simple-projects.md` | Full file | Build and trap task selection |
| Rubric | `../../../../evals/rubric.md` | Full file | Scoring and process metrics |

## Process

1. Choose frozen task prompts: at least one build task and one trap task.
2. Run control, harness, and full-load arms per `protocol.md`: at least 3 isolated runs per arm, verbatim arm prompts, per-run metadata recorded.
3. Run the uniform objective checks against every run before subjective scoring.
4. Score blind, unblind, compute totals, and break artifact ties toward lower measured cost.
5. Track repeated corrections as source-improvement signals with the harness version they apply to.
6. Save evaluation artifacts under `evals/`.

## Outputs

| Artifact | Location | Format |
|----------|----------|--------|
| Evaluation plan | `../../../../evals/` | Markdown |
| Run artifacts and metadata | `../../../../evals/runs/` | Markdown or project files, plus `run-meta.md` per run |
| Review | `../../../../evals/runs/<task>/review.md` | Markdown per rubric template |

## Audit

| Check | Pass condition |
|-------|----------------|
| Isolation | Runs do not share generated context; arm prompts used verbatim |
| Repetition | At least 3 runs per arm per task |
| Metadata | Every run folder has `run-meta.md` with model ID and harness version |
| Scoring integrity | Blind scoring used, totals computed, tie-break rule applied |
| Rubric | All dimensions and process metrics recorded |
| Source learning | Recurring corrections are routed back to source files |
