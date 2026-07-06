# Project Context

This project turns the useful parts of the Fable 5 methodology into practical agent skills and workspace patterns.

## Task Routing

| Task type | Workspace or file | Section to load | Why |
|-----------|-------------------|-----------------|-----|
| Project conventions | `_core/CONVENTIONS.md` | Full file | Canonical folder and authoring rules |
| Prior stage decisions | `docs/fable-pseudo-harness-master.md` | Stage Decisions and Immediate Next Steps | Accepted design source |
| Folder-agent research | `knowledge/wiki/project-structure-tenets.md` | Full file | Current synthesis of Van Clief and Karpathy tenets |
| Source verification | `knowledge/sources/2026-07-05-folder-agents-source-ledger.md` | Full file | External source ledger |
| Harness skill build | `workspaces/fable-task-harness-build/CONTEXT.md` | Full file | Stage map for the main artifact |
| Folder templates | `_core/templates/` | Relevant template | Scaffold root, workspace, stage, source, or evaluation files |
| Evaluation candidates | `evals/candidate-simple-projects.md` | Full file | Choose build and trap tasks for harness tests |
| Evaluation methodology | `evals/protocol.md`, `evals/rubric.md` | Full file | Run and score any A/B/C test |
| Installable harness skill | `fable-task-harness/SKILL.md` | Full file | Skill entrypoint |
| Skill package validation | `scripts/check-skill-package.py` | Run it | Frontmatter, links, and size checks before shipping |

## Process

1. Read the row that matches the user request.
2. Load only the referenced sections or files.
3. Follow the relevant stage contract if the task changes files.
4. Verify changed artifacts before final response.

## Outputs

| Artifact | Location | Format |
|----------|----------|--------|
| Installable skill | `fable-task-harness/` | Codex skill package |
| Research synthesis | `knowledge/wiki/` | Markdown |
| Source ledgers | `knowledge/sources/` | Markdown |
| Build workflow contracts | `workspaces/fable-task-harness-build/` | Markdown stage contracts |
| Evaluation plans and runs | `evals/` | Markdown and generated artifacts |
