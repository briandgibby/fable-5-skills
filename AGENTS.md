# Fable 5 Skills

This repo builds Fable-derived agent skills and tests them as folder-based, human-reviewed workflows.

## Folder Map

```text
AGENTS.md                         Layer 0: root map and routing hints
CONTEXT.md                        Layer 1: task routing table
_core/                            Canonical project conventions and templates
docs/                             Source design notes from the stage analysis
knowledge/sources/                Source ledgers for external research
knowledge/wiki/                   LLM-maintained synthesis and project tenets
workspaces/fable-task-harness-build/
                                  Stage contracts for building the harness
evals/cases/                      Tracked prompts, fixtures, graders, and result receipts
evals/runs/                       Generated local evaluation artifacts
evals/                            Shared protocol, arm prompts, rubric, and case catalog
fable-task-harness/               Installable skill package artifact
scripts/                          Deterministic repo checks
```

## Routing

| User wants | Read first |
|------------|------------|
| Understand project structure | `CONTEXT.md`, `_core/CONVENTIONS.md` |
| Research agent/workflow methods | `workspaces/fable-task-harness-build/stages/01-research-and-tenets/CONTEXT.md` |
| Change project architecture | `workspaces/fable-task-harness-build/stages/02-architecture/CONTEXT.md` |
| Update the skill package | `workspaces/fable-task-harness-build/stages/03-skill-package/CONTEXT.md` |
| Design tracked cases or run A/B/C tests | `workspaces/fable-task-harness-build/stages/04-evaluation/CONTEXT.md` |
| Create a new workspace/stage | `_core/templates/`, `_core/CONVENTIONS.md` |

## Operating Rules

- Treat routing files as control surfaces, not content dumps.
- Load the smallest context that can responsibly handle the task.
- Keep canonical rules in one place and point to them elsewhere.
- Use stage contracts with Inputs, Process, and Outputs.
- Prefer plain markdown and local scripts before orchestration frameworks for sequential human-reviewed work.
- Keep humans in the verification loop for judgment-heavy stages.
- When recurring output edits reveal a pattern, update the source contract or reference.
