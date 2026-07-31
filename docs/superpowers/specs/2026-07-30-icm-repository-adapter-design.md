# ICM Repository Adapter Design

**Date:** 2026-07-30
**Status:** Approved in conversation

## Goal

Evolve `fable-5-skills` in place so nontrivial repository changes can use the central ICM planning and build lifecycle. Keep the current harness, evaluation assets, context routers, stage contracts, and knowledge files intact.

The repository will consume the separately maintained central ICM kernel. It will not copy the kernel's contracts, policies, skills, templates, or validators.

## Decisions

- Add a thin repository-specific `icm/` adapter.
- Keep `fable-task-harness/` as the existing installable product.
- Preserve the root `CONTEXT.md`, `workspaces/`, `knowledge/`, `docs/`, and `evals/` structures as canonical factory and product sources.
- Make ICM mandatory for nontrivial changes to the skill package, project architecture, scripts, evaluation protocols, tracked cases, or graders.
- Keep the existing minimal workflow for small documentation and routing corrections that do not alter behavior or contracts.
- Require explicit `$plan-task`, separate approval, and explicit `$build-task` entrypoints for ICM work.
- Commit coherent, verified design, implementation, and repair milestones separately.

## Rejected Approaches

### Migrate the existing structure into `icm/`

Moving the current routers, workspace stages, and knowledge base would create unnecessary churn, break established paths, and obscure the distinction between repository knowledge and ICM lifecycle control.

### Vendor the central kernel

Copying central contracts, policies, skills, templates, or validators would create a second implementation that could drift from `ICM-agentic-system`.

### Create a parallel harness package

A second `fable-task-harness-icm/` package would imply a product fork. The requested change concerns how this repository plans and builds nontrivial work, not a new end-user harness behavior.

## Architecture

`AGENTS.md` remains the root entrypoint. It classifies work before routing:

- Nontrivial skill, architecture, script, evaluation-protocol, case, or grader changes route to `icm/CONTEXT.md` and require the central ICM lifecycle.
- Small non-behavioral documentation or routing corrections continue through the existing lightweight workflow.

The repository adapter contains only repository facts and routes:

```text
icm/
  CONTEXT.md
  profile.json
  checks/
    CONTEXT.md
  knowledge/
    CONTEXT.md
  tasks/
    CONTEXT.md
```

The existing five-layer context model remains the content-routing architecture. The ICM adapter is a control plane over nontrivial change execution; it does not replace those layers.

## Component Responsibilities

### `icm/CONTEXT.md`

Route ICM planning and building to the repository profile, existing canonical knowledge, reusable checks, and task packages. State that central orchestration policy remains authoritative.

### `icm/profile.json`

Record the repository name, verified commands, source and test paths, high-risk triggers, and any repository review rubrics. Store only commands and paths verified in this checkout.

Use the central repository-profile shape with these exact top-level fields:

- `profile_version`: `1`.
- `repository_name`: `fable-5-skills`.
- `commands`: `test`, `lint`, `typecheck`, and `build` arrays. The `test` array contains the four commands in the Verification section; the other arrays are empty because the repository has no separately verified commands for those categories.
- `paths.source`: `AGENTS.md`, `CONTEXT.md`, `README.md`, `_core/`, `docs/`, `evals/`, `fable-task-harness/`, `knowledge/`, `scripts/`, and `workspaces/`.
- `paths.tests`: `scripts/tests/` and `evals/cases/`.
- `task_profile_triggers.high_risk`: the central template's security, authentication, authorization, migration, destructive, financial, irreversible, and external-side-effect triggers.
- `domain_review_rubrics`: an empty array because the current evaluation rubric is not a repository implementation-review rubric.

### `icm/knowledge/CONTEXT.md`

Map architecture, domain, conventions, and safety needs to existing canonical files and exact sections. Do not restate their durable content.

### `icm/checks/CONTEXT.md`

Map change types to the repository's deterministic checks. Keep command definitions aligned with `icm/profile.json`.

### `icm/tasks/CONTEXT.md`

Define `icm/tasks/<task-id>/` as task-package and execution-evidence storage. State that task observations remain local candidates until a human promotes them and that historical task evidence is not current repository policy.

### Root documentation

- `AGENTS.md` declares the ICM gate and preserves the small-correction exception.
- `CONTEXT.md` routes ICM lifecycle work to `icm/CONTEXT.md`.
- `_core/CONVENTIONS.md` distinguishes ICM lifecycle control from the five-layer content model.
- `README.md` explains the operator flow and central-kernel prerequisite.

### Repository adapter checker

`scripts/check-icm-repository.py` validates the local adapter boundary only. It does not reproduce central plan, approval, run, review, or evidence validation.

The checker verifies:

- Required adapter files exist.
- `profile.json` has the expected repository-profile fields and value types.
- Profile paths are relative and exist in the repository.
- Profile commands are nonempty strings.
- Adapter files contain no unresolved template placeholders.
- Central-only `icm/contracts`, `icm/policies`, and `icm/validators` directories are absent.

`scripts/tests/test_check_icm_repository.py` covers the valid adapter and credible failures for each enforced boundary.

## Lifecycle

For a nontrivial change:

1. `AGENTS.md` identifies the ICM gate.
2. The user explicitly invokes `$plan-task` for one change request.
3. The central planner loads central contracts plus the repository adapter and the exact existing sources it routes to.
4. Planning writes only `icm/tasks/<task-id>/` and stops after independent review.
5. A later explicit approval hash-locks the task package.
6. The user explicitly invokes `$build-task` with the approved task path.
7. The central builder validates approval, creates an isolated worktree, changes only approved paths, runs repository checks, records evidence, and obtains independent review.
8. The successful local run stops before integration. Push, merge, pull request creation, publication, or deployment remains a separate user decision.

Small non-behavioral documentation and routing corrections continue to use the repository's minimal-change workflow and normal verification.

## Failure Behavior

- If the central kernel is unavailable, stop and report the prerequisite. Do not create a local fallback.
- If approval hashes or the recorded base are stale, stop and require replanning or reapproval.
- If profile commands or paths cannot be verified, omit them or stop; do not guess.
- If authoritative sources conflict, report both sources and stop rather than choosing by model preference.
- If a proposed change needs central-only code in this repository, stop because it violates the adapter boundary.
- Preserve unrelated working-tree changes and stage explicit paths only.

## Verification

Implementation is accepted when these commands exit zero with fresh output:

```powershell
python scripts/check-icm-repository.py
python scripts/check-skill-package.py
python scripts/check-eval-cases.py
python -m unittest discover -s scripts/tests -v
```

Review the final diff to confirm that:

- Only approved adapter, routing, convention, operator-documentation, checker, and checker-test files changed.
- No central contracts, policies, skills, templates, or validators were copied.
- Existing harness behavior and version are unchanged.
- Existing evaluation content and stage documents are unchanged.

## Non-Goals

- Changing `fable-task-harness` behavior or version.
- Migrating or deleting existing context routers, workspace stages, knowledge files, or evaluation assets.
- Copying or modifying the central ICM kernel.
- Creating a synthetic historical ICM task package for the bootstrap change.
- Pushing, merging, opening a pull request, publishing, or deploying.
