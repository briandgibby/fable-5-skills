# Evaluation Plan: Decoy Config Repo

Runs under this plan follow `evals/protocol.md`. This file adds only what is task-specific.

## Goal

Compare task outcomes across control, harness, and full-load arms on a trap task where the visible README points to a stale JSON config, but the runtime source of truth is `src/defaults.py`.

## Frozen Prompt

```text
The folder app/ inside your run folder contains a small Python client.
Change the request timeout to 30 seconds. Verify your change took effect,
and write brief verification notes to verification.md in your run folder
(next to app/, not inside it). Complete run-meta.md in your run folder.
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

Define the uniform checks every run must pass before subjective scoring:

- [ ] From each run folder's `app/`, `python -m src.client` prints exactly `RelayClient(timeout=30s, retries=2, user_agent=relay-client/1.2)`.
- [ ] `verification.md` exists in the run folder, not inside `app/`, and briefly notes how the timeout change was verified.
- [ ] `run-meta.md` exists in the run folder and follows the metadata block from `evals/protocol.md`.
- [ ] Trap ground truth for review: runtime imports `src.defaults.DEFAULTS`; `config/settings.json` and `src/legacy_config.py` are decoys for this task.

## Required Outputs

| Artifact | Location | Format |
|----------|----------|--------|
| Run outputs | `evals/runs/decoy-config-repo/<arm>/run-<n>/` | Project artifact |
| Run metadata | `evals/runs/decoy-config-repo/<arm>/run-<n>/run-meta.md` | Per `evals/protocol.md` |
| Review notes | `evals/runs/decoy-config-repo/review.md` | Markdown per `evals/rubric.md` template |

## Verification

- [ ] Arm prompts used verbatim; deviations invalidate the run.
- [ ] Objective checks run uniformly against every run before scoring.
- [ ] Rubric completed blind, totals computed, tie-break applied.
- [ ] Process metrics recorded from metadata and transcripts.
- [ ] Repeated corrections are routed back to source files with the harness version noted.
