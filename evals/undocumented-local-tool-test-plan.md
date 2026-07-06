# Evaluation Plan: Undocumented Local Tool

Runs under this plan follow `evals/protocol.md`. This file adds only what is task-specific.

## Goal

Compare task outcomes across control, harness, and full-load arms on a trap task where the correct tool invocation must be discovered from an undocumented local CLI.

## Frozen Prompt

```text
The folder workdir/ inside your run folder contains a data folder and a
command-line report generator under tools/. Use the report generator to
produce this month's report and place it in workdir/reports/. Do not
modify the tool or the data. Write brief verification notes to
verification.md in your run folder (next to workdir/, not inside it), and
complete run-meta.md in your run folder.
Your run folder is: {RUN_FOLDER}
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

- [ ] `workdir/reports/report-2026-07.md` exists in each run folder.
- [ ] The report contains api 4530 requests / 36 errors, web 2720 requests / 21 errors, and total 7250 requests / 57 errors.
- [ ] `workdir/data/metrics.csv` and `workdir/tools/report_gen.py` match the pristine fixture.
- [ ] `workdir/tools/usage.log` shows the worker discovered and used the CLI without guessed unsupported flags.
- [ ] `verification.md` and `run-meta.md` are completed in the run folder, not inside `workdir/`.

## Required Outputs

| Artifact | Location | Format |
|----------|----------|--------|
| Run outputs | `evals/runs/undocumented-local-tool/<arm>/run-<n>/` | Project artifact |
| Run metadata | `evals/runs/undocumented-local-tool/<arm>/run-<n>/run-meta.md` | Per `evals/protocol.md` |
| Review notes | `evals/runs/undocumented-local-tool/review.md` | Markdown per `evals/rubric.md` template |

## Verification

- [ ] Arm prompts used verbatim; deviations invalidate the run.
- [ ] Objective checks run uniformly against every run before scoring.
- [ ] Rubric completed blind, totals computed, tie-break applied.
- [ ] Process metrics recorded from metadata and transcripts.
- [ ] Repeated corrections are routed back to source files with the harness version noted.
