# Stage 03: Skill Package

Use this stage when changing the installable `fable-task-harness` skill.

## Inputs

| Source | File/Location | Section/Scope | Why |
|--------|---------------|---------------|-----|
| Skill entrypoint | `../../../../fable-task-harness/SKILL.md` | Full file | Main behavior |
| Skill references | `../../../../fable-task-harness/references/` | Relevant files only | Detailed rules |
| Skill templates | `../../../../fable-task-harness/templates/` | Relevant files only | Reusable forms |
| Original plan | `../../../../docs/fable-pseudo-harness-master.md` | Proposed Skill Architecture and Core Harness Spine | Scope control |
| Structure tenets | `../../../../knowledge/wiki/project-structure-tenets.md` | What The Research Adds | Folder and Software 3.0 grounding |

## Process

1. Keep `SKILL.md` concise and trigger-focused.
2. Move detail into one-level references or templates.
3. Avoid duplicating canonical project conventions.
4. Add references only when they change agent behavior.
5. Verify links and file names after edits.

## Outputs

| Artifact | Location | Format |
|----------|----------|--------|
| Skill package | `../../../../fable-task-harness/` | Codex skill package |

## Audit

| Check | Pass condition |
|-------|----------------|
| Entrypoint size | `SKILL.md` stays short enough to load quickly |
| Trigger quality | Description says what it does and when to use it |
| Progressive disclosure | Rare details live in references or templates |
| Link integrity | Referenced files exist |
