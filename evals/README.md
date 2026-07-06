# Evaluations

This folder holds harness test protocols, plans, run artifacts, and review rubrics.

Start here:

- `protocol.md` defines how every evaluation runs: arms, repeat counts, frozen arm prompts, per-run metadata, blind scoring, and computed totals.
- `arm-prompts/` holds the frozen verbatim setup text for each arm.
- `candidate-simple-projects.md` lists build tasks and trap tasks suitable for testing.
- `rubric.md` defines scoring and process metrics.
- `initial-ab-test-plan.md` is the record of run 1 (static-focus-board); its arm design is superseded by `protocol.md`.
- `runs/` holds isolated run artifacts.

Run artifacts under `runs/` are local evidence by default and are ignored by git. Promote only curated summaries, screenshots, scripts, or examples that should become reusable project material.
