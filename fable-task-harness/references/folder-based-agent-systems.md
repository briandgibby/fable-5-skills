# Folder-Based Agent Systems

Use this reference when structuring agent workflows, workspaces, stage contracts, or reusable project folders.

## Core Pattern

For sequential, human-reviewed workflows, folders can replace much of the orchestration code:

```text
folder map -> workspace routing -> stage contract -> references -> working artifacts
```

The agent reads the right files at the right moment. Humans can inspect and edit every intermediate artifact.

## Adopted Tenets

- One stage, one job.
- Plain markdown is the interface.
- Stage folders are numbered in execution order.
- Each stage has an Inputs, Process, and Outputs contract.
- Stages hand off through files, usually in `output/` folders.
- Context is loaded by layer and section, not all at once.
- Canonical information has one home.
- Dependencies point one way.
- Local scripts handle deterministic mechanics that do not need model judgment.
- Old outputs are artifacts, not quality standards.

## Suggested Workspace Shape

```text
AGENTS.md
CONTEXT.md
_core/
knowledge/
workspaces/
  example-workspace/
    CONTEXT.md
    stages/
      01-first-stage/
        CONTEXT.md
        output/
      02-second-stage/
        CONTEXT.md
        output/
```

## Stage Contract Shape

```md
## Inputs

| Source | File/Location | Section/Scope | Why |
|--------|---------------|---------------|-----|

## Process

1. Step one.
2. Step two.

## Outputs

| Artifact | Location | Format |
|----------|----------|--------|
```

Add checkpoints or audits when creative judgment, architecture, or cross-stage alignment matters.

## Source Integrity

Editing an output fixes one run. Editing the source improves future runs. When recurring edits appear, trace them back to:

- Stage contract.
- Reference material.
- Skill instruction.
- Template.
- Source or synthesis note.

Then update the source that caused the repeated issue.
