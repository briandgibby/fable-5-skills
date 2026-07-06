# Intake And Routing

Use this reference when a task needs project context, file changes, tools, skills, or a reusable artifact.

## Routing Loop

```text
Understand the request -> check context sufficiency -> recover needed context -> choose the source of truth -> choose the output surface -> load relevant skills -> act.
```

## Source Of Truth

Prefer the highest-fidelity surface for the task:

- Current conversation when the user supplied enough detail.
- Current workspace when repo, code, files, or project state matters.
- Existing docs when the task depends on prior decisions or project language.
- Memory or thread history when the user implies prior shared context.
- Installed skills or references for specialized workflows, formats, tools, frameworks, or domains.
- Connected tools or apps when the requested data lives outside the repo.
- Web search when freshness, external verification, or public source material is needed.
- User clarification when the above cannot resolve the ambiguity safely.

## Context Sufficiency Check

Before building or changing anything, ask:

- What outcome did the user request?
- What constraints are explicit?
- What source of truth should govern the answer?
- Is the needed context locally recoverable?
- Would acting now risk producing the wrong artifact, editing the wrong file, or using the wrong external system?

Recover context before asking. Ask only when missing context cannot be recovered safely.

## Skill Preflight

Before specialized work, check whether a relevant skill or reference applies. Load it before writing code, editing files, calling specialized tools, or producing domain-specific deliverables.

Use skill preflight for:

- Specialized file formats.
- Frameworks, SDKs, APIs, or cloud services.
- Tool-heavy work.
- Domain workflows.
- Research or source-backed writing.
- Visual, UI, frontend, or media output.

## Routing Visibility

Keep routine routing silent. State routing decisions only when they affect:

- Scope.
- Cost.
- Risk.
- Required approval.
- Output surface.
- Assumptions the user should see.

## Example

Task: "Add an export button to the dashboard."

Wrong: scaffold a new dashboard in a new folder because no file was named.

Right: the workspace is the source of truth. Locate the existing dashboard code, confirm the framework and conventions, load any frontend skill that applies, then edit in place following the repo's existing button patterns.
