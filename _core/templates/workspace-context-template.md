# {{WORKSPACE_NAME}} Workspace

{{WORKSPACE_PURPOSE}}

## Inputs

| Source | File/Location | Section/Scope | Why |
|--------|---------------|---------------|-----|
| Project map | `../../AGENTS.md` | Full file | Root routing rules |
| Project conventions | `../../_core/CONVENTIONS.md` | Full file | Canonical folder protocol |

## Process

1. Identify which stage matches the user request.
2. Read that stage's `CONTEXT.md`.
3. Load only the files and sections named by the stage.
4. Produce or edit the artifact named in the stage Outputs table.
5. Run the stage Audit before final response.

## Stage Map

| Stage | Folder | Purpose |
|-------|--------|---------|
| 01 | `stages/01-{{STAGE_SLUG}}/` | {{STAGE_PURPOSE}} |

## Outputs

| Artifact | Location | Format |
|----------|----------|--------|
| {{ARTIFACT_NAME}} | `{{ARTIFACT_PATH}}` | {{FORMAT}} |
