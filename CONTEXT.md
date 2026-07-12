# Project Context

This project turns the useful parts of the Fable 5 methodology into practical agent skills and workspace patterns.

## Task Routing

| Task type | Workspace or file | Section to load | Why |
|-----------|-------------------|-----------------|-----|
| Project conventions | `_core/CONVENTIONS.md` | Full file | Canonical folder and authoring rules |
| Prior stage decisions | `docs/fable-pseudo-harness-master.md` | Stage Decisions and Immediate Next Steps | Accepted design source |
| Folder-agent research | `knowledge/wiki/project-structure-tenets.md` | Full file | Current synthesis of Van Clief and Karpathy tenets |
| Source verification | `knowledge/sources/2026-07-05-folder-agents-source-ledger.md` | Full file | External source ledger |
| Harness innovation research | `knowledge/wiki/agent-harness-innovation-gaps.md`, `knowledge/sources/2026-07-12-agent-harness-innovation-source-ledger.md` | Full files | Current official and academic evidence, adopted tenets, and gap map |
| Harness innovation implementation | `docs/superpowers/specs/2026-07-12-harness-innovation-evaluation-design.md`, `docs/superpowers/plans/2026-07-12-harness-innovation-sprint.md` | Full files | Approved architecture and sequenced sprint backlog |
| Harness skill build | `workspaces/fable-task-harness-build/CONTEXT.md` | Full file | Stage map for the main artifact |
| Folder templates | `_core/templates/` | Relevant template | Scaffold root, workspace, stage, source, or evaluation files |
| Evaluation candidates | `evals/candidate-simple-projects.md` | Full file | Choose build and trap tasks for harness tests |
| Tracked evaluation cases | `evals/cases/README.md`, selected case `README.md` and `case.json` | Full files | Author, reuse, or grade a reproducible case |
| Evaluation methodology | `evals/protocol.md`, `evals/rubric.md` | Full file | Run and score any A/B/C test |
| Evaluation case validation | `scripts/check-eval-cases.py` | Run it | Validate tracked manifests, hashes, paths, graders, and receipts |
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
| Approved designs and implementation plans | `docs/superpowers/specs/`, `docs/superpowers/plans/` | Markdown |
| Build workflow contracts | `workspaces/fable-task-harness-build/` | Markdown stage contracts |
| Tracked evaluation cases | `evals/cases/` | Versioned manifests, prompts, fixtures, graders, and receipts |
| Generated evaluation runs | `evals/runs/` | Ignored local artifacts and metadata |
