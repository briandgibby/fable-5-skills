# Evaluations

This folder holds the shared harness evaluation protocol, tracked case modules,
generated run artifacts, and the review rubric.

Start here:

- `protocol.md` defines how every evaluation runs: arms, repeat counts, frozen arm prompts, per-run metadata, blind scoring, and computed totals.
- `arm-prompts/` holds the frozen verbatim setup text for each arm.
- `cases/` holds tracked, reusable prompts, fixtures, graders, grader tests, and curated receipts.
- `candidate-simple-projects.md` lists build tasks and trap tasks suitable for testing.
- `rubric.md` defines scoring and process metrics.
- `initial-ab-test-plan.md` is the record of run 1 (static-focus-board); its arm design is superseded by `protocol.md`.
- `runs/` holds generated isolated run artifacts and is ignored by Git.

Start case-specific work at `cases/README.md`, then load the selected case's
`README.md` and `case.json`. A case module is the canonical source for its frozen
prompt, fixture, ground truth, and grader.

Run artifacts under `runs/` are local evidence by default. Promote durable findings
into the case's `receipts/` folder rather than making ignored run folders a dependency
of tracked docs or changelog claims.
