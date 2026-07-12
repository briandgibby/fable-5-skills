# Stage 04: Evaluation

Use this stage when designing or running control, harness, and full-load evaluation arms.

## Inputs

| Source | File/Location | Section/Scope | Why |
|--------|---------------|---------------|-----|
| Protocol | `../../../../evals/protocol.md` | Full file | Governing methodology for every run |
| Tracked cases | `../../../../evals/cases/README.md`, selected case folder | Full README and `case.json` | Frozen prompt, fixture, grader, and case ground truth |
| Arm prompts | `../../../../evals/arm-prompts/` | Relevant arm files | Frozen verbatim setup text |
| Harness skill | `../../../../fable-task-harness/SKILL.md` | Frontmatter and Reference Triggers | What is being tested, and its version |
| Master plan | `../../../../docs/fable-pseudo-harness-master.md` | Revision: Post-Eval Restructure | Accepted test design decisions |
| Project tenets | `../../../../knowledge/wiki/project-structure-tenets.md` | Build Partial Autonomy First | Evaluation posture |
| Candidate projects | `../../../../evals/candidate-simple-projects.md` | Full file | Build and trap task selection |
| Rubric | `../../../../evals/rubric.md` | Full file | Scoring and process metrics |

## Process

1. Choose tracked cases: at least one build task and one trap task; create a case module first when none exists.
2. Run `python scripts/check-eval-cases.py`, then copy the selected fixture into every isolated run.
3. Run control, harness, and full-load arms per `protocol.md`: at least 3 isolated runs per arm, verbatim arm and case prompts, per-run metadata recorded.
4. Run the tracked case grader uniformly against every run before subjective scoring.
5. Score blind, unblind, compute totals, and break artifact ties toward lower measured cost.
6. Track repeated corrections as source-improvement signals with the harness and case versions they apply to.
7. Keep raw artifacts under `evals/runs/`; promote durable findings to the case's tracked `receipts/` folder.

## Outputs

| Artifact | Location | Format |
|----------|----------|--------|
| Evaluation case | `../../../../evals/cases/<task>/` | Manifest, prompt, fixture, grader, tests, and receipts |
| Run artifacts and metadata | `../../../../evals/runs/` | Markdown or project files, plus `run-meta.md` per run |
| Raw review | `../../../../evals/runs/<task>/review.md` | Ignored Markdown per rubric template |
| Curated receipt | `../../../../evals/cases/<task>/receipts/` | Tracked result summary and limitations |

## Audit

| Check | Pass condition |
|-------|----------------|
| Isolation | Runs do not share generated context; arm prompts used verbatim |
| Case integrity | `scripts/check-eval-cases.py` passes; fixture and prompt hashes match |
| Repetition | At least 3 runs per arm per task |
| Metadata | Every run folder has `run-meta.md` with case, model, and harness versions |
| Grader | Known-good and known-bad tests pass; failed objective checks return nonzero |
| Scoring integrity | Blind scoring used, totals computed, tie-break rule applied |
| Rubric | All dimensions and process metrics recorded |
| Source learning | Recurring corrections are routed back to source files and durable results are receipted |
