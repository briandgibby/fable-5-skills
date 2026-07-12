# Tracked Evaluation Case Module Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:test-driven-development` for behavior changes and request an independent review before completion.

**Goal:** Create a tracked, self-contained evaluation-case module and migrate `decoy-config-repo` into it while keeping generated runs ignored.

**Architecture:** A case is a folder under `evals/cases/<case-id>/` whose small `case.json` manifest is the machine-readable interface. The folder owns its frozen prompt, pristine fixture, case-specific grader, grader tests, and curated result receipts. `scripts/check-eval-cases.py` validates the tracked contract and hashes; raw execution artifacts remain under ignored `evals/runs/`.

**Tech Stack:** Python standard library, JSON, Markdown, `unittest`, Git.

## Global Constraints

- Keep one canonical home for case-specific ground truth.
- Use only Python's standard library; add no package dependency.
- Grade one run at a time and emit structured JSON to stdout.
- Exit zero only when every required objective check passes.
- Keep `evals/runs/` ignored; track reusable case inputs and graders under `evals/cases/`.
- Do not commit or push unless the user explicitly requests it.

---

### Task 1: Case-contract validator

**Files:**
- Create: `scripts/tests/test_check_eval_cases.py`
- Create: `scripts/check-eval-cases.py`

**Interfaces:**
- Consumes: `evals/cases/*/case.json`
- Produces: process exit `0` only when every discovered case is valid; concise errors on stderr otherwise

- [x] **Step 1: Write failing validator tests**

  Cover a valid temporary case, a prompt hash mismatch, a fixture hash mismatch, a missing referenced file, and a manifest whose `id` differs from its directory name.

- [x] **Step 2: Verify RED**

  Run: `python -m unittest scripts.tests.test_check_eval_cases -v`

  Expected: import or file-not-found failure because `scripts/check-eval-cases.py` does not exist.

- [x] **Step 3: Implement the smallest validator**

  Validate `schema_version`, `id`, `version`, `kind`, referenced prompt/fixture/grader paths, prompt SHA-256, the exact fixture file inventory and hashes, and a grader command containing `{run_dir}`.

- [x] **Step 4: Verify GREEN**

  Run: `python -m unittest scripts.tests.test_check_eval_cases -v`

  Expected: all validator tests pass.

### Task 2: Decoy Config tracked case and grader

**Files:**
- Create: `evals/cases/README.md`
- Create: `evals/cases/decoy-config-repo/case.json`
- Create: `evals/cases/decoy-config-repo/prompt.md`
- Create: `evals/cases/decoy-config-repo/grader.py`
- Create: `evals/cases/decoy-config-repo/test_grader.py`
- Create: `evals/cases/decoy-config-repo/receipts/harness-v0.2.1.md`
- Create: `evals/cases/decoy-config-repo/fixture/app/README.md`
- Create: `evals/cases/decoy-config-repo/fixture/app/config/settings.json`
- Create: `evals/cases/decoy-config-repo/fixture/app/src/__init__.py`
- Create: `evals/cases/decoy-config-repo/fixture/app/src/client.py`
- Create: `evals/cases/decoy-config-repo/fixture/app/src/defaults.py`
- Create: `evals/cases/decoy-config-repo/fixture/app/src/legacy_config.py`

**Interfaces:**
- Consumes: `python grader.py --run-dir <run-folder>`
- Produces: JSON object with `schema_version`, `case_id`, `passed`, and named `checks`; exit `0` on pass and `1` on objective failure

- [x] **Step 1: Write failing grader tests**

  Cover a known-good run, extra runtime output, an additional decoy edit, missing metadata, misplaced verification notes, and CLI nonzero exit for a failed run.

- [x] **Step 2: Verify RED**

  Run: `python -m unittest discover -s evals/cases/decoy-config-repo -p "test_*.py" -v`

  Expected: import or file-not-found failure because `grader.py` does not exist.

- [x] **Step 3: Implement the minimal grader and tracked fixture**

  Load ground truth from `case.json`; run `python -m src.client` with bytecode disabled, require exact stdout, compare the final app tree with the pristine fixture allowing only `app/src/defaults.py` to change, require root-level nonblank verification notes, and validate every protocol metadata field is present and nonblank. Report Python bytecode as an ignored transient.

- [x] **Step 4: Verify GREEN**

  Run: `python -m unittest discover -s evals/cases/decoy-config-repo -p "test_*.py" -v`

  Expected: all grader tests pass.

- [x] **Step 5: Validate the real tracked module**

  Run: `python scripts/check-eval-cases.py`

  Expected: `decoy-config-repo: valid` and exit `0`.

### Task 3: Routing and durable-evidence documentation

**Files:**
- Modify: `.gitignore`
- Modify: `AGENTS.md`
- Modify: `CONTEXT.md`
- Modify: `_core/CONVENTIONS.md`
- Create: `_core/templates/evaluation-case-template.md`
- Delete: `_core/templates/evaluation-plan-template.md`
- Modify: `README.md`
- Modify: `evals/README.md`
- Modify: `evals/protocol.md`
- Modify: `evals/candidate-simple-projects.md`
- Delete: `evals/decoy-config-repo-test-plan.md`
- Modify: `workspaces/fable-task-harness-build/stages/04-evaluation/CONTEXT.md`
- Modify: `fable-task-harness/CHANGELOG.md`

**Interfaces:**
- Consumes: requests to design, validate, or run an evaluation case
- Produces: direct routing to the tracked case module while preserving ignored raw runs

- [x] **Step 1: Update canonical routing**

  Route case design and objective grading to `evals/cases/`; keep protocol-level rules in `evals/protocol.md` and run outputs in `evals/runs/`.

- [x] **Step 2: Move the old test plan into the tracked case module**

  Delete the standalone plan after promoting its intent into the case README; keep exact prompt, hashes, and ground truth canonical in `case.json` and `prompt.md`.

- [x] **Step 3: Clarify ignore behavior**

  Document that only raw runs are ignored; tracked cases, graders, and curated evidence live outside `evals/runs/`.

- [x] **Step 4: Run all verification**

  Run:

  - `python -m unittest discover -s scripts/tests -p "test_*.py" -v`
  - `python -m unittest discover -s evals/cases/decoy-config-repo -p "test_*.py" -v`
  - `python scripts/check-eval-cases.py`
  - `python scripts/check-skill-package.py`
  - `git diff --check`

  Expected: all commands exit `0`; no warnings or whitespace errors.
