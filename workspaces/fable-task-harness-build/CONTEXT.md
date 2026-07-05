# Fable Task Harness Build Workspace

This workspace builds and evaluates the installable `fable-task-harness` skill.

## Inputs

| Source | File/Location | Section/Scope | Why |
|--------|---------------|---------------|-----|
| Project map | `../../AGENTS.md` | Full file | Root routing rules |
| Project conventions | `../../_core/CONVENTIONS.md` | Full file | Canonical folder protocol |
| Original plan | `../../docs/fable-pseudo-harness-master.md` | Current Position through Immediate Next Steps | Accepted harness decisions |
| Research synthesis | `../../knowledge/wiki/project-structure-tenets.md` | Full file | Folder-agent and Karpathy grounding |

## Process

1. Identify which stage matches the user request.
2. Read that stage's `CONTEXT.md`.
3. Load only the files and sections named by the stage.
4. Produce or edit the artifact named in the stage Outputs table.
5. Run the stage Audit before final response.

## Stage Map

| Stage | Folder | Purpose |
|-------|--------|---------|
| 01 | `stages/01-research-and-tenets/` | Maintain source-backed project tenets |
| 02 | `stages/02-architecture/` | Maintain folder architecture and routing |
| 03 | `stages/03-skill-package/` | Maintain the installable harness skill |
| 04 | `stages/04-evaluation/` | Design and run A/B/C harness tests |

## Outputs

| Artifact | Location | Format |
|----------|----------|--------|
| Skill package | `../../fable-task-harness/` | Codex skill package |
| Project routing | `../../AGENTS.md`, `../../CONTEXT.md` | Markdown |
| Conventions | `../../_core/CONVENTIONS.md` | Markdown |
| Research knowledge | `../../knowledge/` | Markdown |
| Evaluation materials | `../../evals/` | Markdown and artifacts |
