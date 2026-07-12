# Evaluation Case: {{EVALUATION_NAME}}

This tracked case follows `evals/protocol.md`. Keep its prompt, fixture, objective
ground truth, grader, tests, and curated receipts together under
`evals/cases/{{SLUG}}/`.

## Goal

{{GOAL}}

## Case Files

| File | Purpose |
|------|---------|
| `case.json` | Versioned machine-readable contract, normalized hashes, grader arguments, and golden outcome |
| `README.md` | Human-readable case intent, setup, grading, and interpretation limits |
| `prompt.md` | Frozen task prompt with declared placeholders only |
| `fixture/` | Pristine inputs copied into every isolated run |
| `grader.py` | Single-run structured objective grader; exit 0 pass, 1 candidate failure, 2 invalid invocation |
| `test_grader.py` | Known-good, known-bad, and alternative-valid grader tests |
| `receipts/` | Curated summaries of batteries that informed durable changes |

## Arms

| Arm | Setup | Isolation rule |
|-----|-------|----------------|
| Control | `evals/arm-prompts/control.md`, verbatim | Fresh context and fresh output folder per run |
| Harness | `evals/arm-prompts/harness.md`, verbatim | Fresh context and fresh output folder per run |
| Full-load | `evals/arm-prompts/full-load.md`, verbatim | Fresh context and fresh output folder per run |

Minimum 3 runs per arm. Generated artifacts belong under
`evals/runs/{{SLUG}}/<arm>/run-<n>/` and remain ignored.

## Objective Contract

- User-visible capability: {{CAPABILITY}}
- Allowed fixture changes: {{ALLOWED_CHANGES}}
- Decoy or protected paths: {{PROTECTED_PATHS}}
- Required run files: `verification.md`, `run-meta.md`
- Ignored verification transients: {{IGNORED_TRANSIENTS}}

The exact values belong in `case.json`; this section explains their intent without
duplicating hashes or long expected outputs.

## Verification

- [ ] `python scripts/check-eval-cases.py` passes.
- [ ] Grader known-good tests pass.
- [ ] Each required failure mode has a known-bad test that returns exit 1.
- [ ] The grader does not mutate the run it grades.
- [ ] Arm and case prompts are assembled verbatim except declared placeholders.
- [ ] Objective results are produced before blind subjective scoring.
- [ ] Durable source-learning results are promoted into `receipts/` with harness and case versions.
