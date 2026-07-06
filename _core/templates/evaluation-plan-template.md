# Evaluation Plan: {{EVALUATION_NAME}}

Runs under this plan follow `evals/protocol.md`. This file adds only what is task-specific.

## Goal

Compare task outcomes across control, harness, and full-load arms.

## Frozen Prompt

```text
{{PROMPT}}
```

## Arms

| Arm | Setup | Isolation rule |
|-----|-------|----------------|
| Control | `evals/arm-prompts/control.md`, verbatim | Fresh context and fresh output folder per run |
| Harness | `evals/arm-prompts/harness.md`, verbatim | Fresh context and fresh output folder per run |
| Full-load | `evals/arm-prompts/full-load.md`, verbatim | Fresh context and fresh output folder per run |

Minimum 3 runs per arm. Number run folders `run-1/`, `run-2/`, `run-3/`.

## Objective Checks

Define the uniform checks every run must pass before subjective scoring (smoke test script, expected outputs, or trap-task ground truth):

- [ ] {{CHECK}}

## Required Outputs

| Artifact | Location | Format |
|----------|----------|--------|
| Run outputs | `evals/runs/{{SLUG}}/<arm>/run-<n>/` | Project artifact |
| Run metadata | `evals/runs/{{SLUG}}/<arm>/run-<n>/run-meta.md` | Per `evals/protocol.md` |
| Review notes | `evals/runs/{{SLUG}}/review.md` | Markdown per `evals/rubric.md` template |

## Verification

- [ ] Arm prompts used verbatim; deviations invalidate the run.
- [ ] Objective checks run uniformly against every run before scoring.
- [ ] Rubric completed blind, totals computed, tie-break applied.
- [ ] Process metrics recorded from metadata and transcripts.
- [ ] Repeated corrections are routed back to source files with the harness version noted.
