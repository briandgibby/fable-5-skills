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

1. Keep `SKILL.md` concise: operating loop, observable reference triggers, and operating rules only.
2. Move detail into one-level references or templates. Each rule gets one canonical home; consolidate rather than duplicate.
3. Keep evaluation-arm and roadmap content out of the shipped package.
4. Give every operational reference one worked wrong-versus-right example.
5. Add references only when they change agent behavior.
6. Bump `version` in the frontmatter and record the change in `CHANGELOG.md`.
7. Run `python scripts/check-skill-package.py` and fix any errors.

## Outputs

| Artifact | Location | Format |
|----------|----------|--------|
| Skill package | `../../../../fable-task-harness/` | Versioned skill package (Codex and Claude Code compatible) |

## Audit

| Check | Pass condition |
|-------|----------------|
| Package check | `scripts/check-skill-package.py` exits clean: valid frontmatter YAML, required fields, resolving links |
| Entrypoint size | `SKILL.md` stays short enough to load quickly |
| Trigger quality | Description says what it does and when to use it; reference triggers are observable, not judgment calls |
| Progressive disclosure | Rare details live in references or templates |
| Factory/product separation | No evaluation-arm or roadmap content ships in the package |
| Versioning | `version` bumped and `CHANGELOG.md` updated for behavior changes |
