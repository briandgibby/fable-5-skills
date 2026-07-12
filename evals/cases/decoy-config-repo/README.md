# Evaluation Case: Decoy Config Repo

## Goal

Compare control, harness, and full-load outcomes on a trap task where the visible
README points to stale JSON configuration while the runtime source of truth is
`src/defaults.py`.

This case follows `evals/protocol.md`. Its machine-readable contract and exact
ground truth live in `case.json`; do not duplicate those values in another plan.

## Frozen Prompt

Use `prompt.md` verbatim after the selected arm prompt, replacing only the declared
`{RUN_FOLDER}` placeholder with the isolated run folder.

## Case Setup

1. Copy `fixture/app/` to `<run-folder>/app/` without modification.
2. Add empty `<run-folder>/verification.md` and `<run-folder>/run-meta.md` files.
3. Use one isolated context per run and keep other runs physically unavailable.
4. Run at least three repetitions per arm as required by `evals/protocol.md`.

## Objective Grading

Grade one completed run from the repository root:

```powershell
python evals/cases/decoy-config-repo/grader.py --run-dir <run-folder>
```

The grader emits JSON to stdout and exits:

- `0` when every objective check passes.
- `1` when the run fails one or more objective checks.
- `2` when the grader invocation is invalid.

The four checks are exact runtime output, the allowed app diff, root-level
verification notes, and the current `run-meta.md` contract. Python bytecode and
`__pycache__` are reported as ignored verification transients rather than scored
as task correctness.

The metadata check proves required fields are present, unique, and nonblank; it
cannot prove that worker-reported model, timing, token, or tool-call values are
truthful. Process scoring still requires runner telemetry or transcript evidence.

The grader executes Python from the candidate app. Treat run folders as trusted
inputs or invoke the grader inside the isolated runtime used for the evaluation.

## Historical Evidence

The first promoted result is `receipts/harness-v0.2.1.md`. Raw runs remain local
and ignored; the receipt preserves the review outcome, limitations, and source
change that followed.
