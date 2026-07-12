# Stage 02: Architecture

Use this stage when changing folder layout, routing files, workspace contracts, or canonical project rules.

## Inputs

| Source | File/Location | Section/Scope | Why |
|--------|---------------|---------------|-----|
| Project conventions | `../../../../_core/CONVENTIONS.md` | Full file | Canonical rules |
| Project routing | `../../../../AGENTS.md`, `../../../../CONTEXT.md` | Full file | Current control surface |
| Research synthesis | `../../../../knowledge/wiki/project-structure-tenets.md` | Recommended Repo Shape and Deferred | Grounding |
| Harness innovation synthesis | `../../../../knowledge/wiki/agent-harness-innovation-gaps.md` | Architecture Deepening Decisions | Current Module, Interface, Seam, and Adapter decisions |
| Current tree | Workspace file listing | Full listing | Avoid duplicate homes |

## Process

1. Identify the canonical home for any new rule or artifact.
2. Preserve one-way dependencies.
3. Add or update routing before adding deeper content.
4. Keep stage contracts short and specific.
5. Create `.gitkeep` files for empty persistent output folders.

## Outputs

| Artifact | Location | Format |
|----------|----------|--------|
| Root routing | `../../../../AGENTS.md`, `../../../../CONTEXT.md` | Markdown |
| Conventions | `../../../../_core/CONVENTIONS.md` | Markdown |
| Workspace contracts | `../../../../workspaces/` | Markdown |

## Audit

| Check | Pass condition |
|-------|----------------|
| Canonical source | New durable rules have one home |
| Routing only | `CONTEXT.md` files point instead of becoming large references |
| One-way dependencies | No circular project references introduced |
| Inspectability | A future agent can find the next file to read |
