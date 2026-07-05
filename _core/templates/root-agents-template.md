# {{PROJECT_NAME}}

{{ONE_SENTENCE_PURPOSE}}

## Folder Map

```text
AGENTS.md                 Layer 0: root map and routing hints
CONTEXT.md                Layer 1: task routing table
_core/                    Canonical conventions and templates
docs/                     Source design notes
knowledge/                Source ledgers and synthesized project knowledge
workspaces/               Stage contracts for repeatable workflows
```

## Routing

| User wants | Read first |
|------------|------------|
| Understand project structure | `CONTEXT.md`, `_core/CONVENTIONS.md` |
| Work on {{WORKFLOW_NAME}} | `workspaces/{{WORKSPACE_SLUG}}/CONTEXT.md` |

## Operating Rules

- Treat routing files as control surfaces, not content dumps.
- Load the smallest context that can responsibly handle the task.
- Keep canonical rules in one place and point to them elsewhere.
- Use stage contracts with Inputs, Process, and Outputs.
- Prefer plain markdown and local scripts before orchestration frameworks for sequential human-reviewed work.
- Keep humans in the verification loop for judgment-heavy stages.
