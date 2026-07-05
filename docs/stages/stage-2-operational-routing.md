# Stage 2: Operational Routing

## Status

Accepted as the main structural foundation for the Fable pseudo harness.

Stage 1 will not receive a dedicated markdown file for now. Its risk-handling material should be revisited later as a separate prompt-injection or trust-boundary skill, likely for commercial agentic systems such as Signsense rather than this harness project.

## Core Idea

Stage 2 is about deciding where a task belongs before doing the task. The harness should make an early routing pass across available context, tools, skills, files, and output surfaces instead of jumping straight into prose or implementation.

The useful abstraction is:

```text
Understand the request -> check context sufficiency -> recover needed context -> choose the source of truth -> choose the output surface -> load relevant skills -> act.
```

## Main Rules

### Capability Routing

Before acting, identify the best source of truth for the task:

- Current conversation when the user provided enough context.
- Current working directory when repo, code, file, or project state matters.
- Existing documentation when the task depends on prior decisions or project language.
- Memory or thread context when the user implies prior shared context.
- Installed skills or references when the task touches a specialized workflow, file format, framework, or domain.
- Connected tools or apps when the task concerns data that lives outside the repo.
- Web search only when freshness, external verification, or public source material is needed.
- User clarification when the above surfaces cannot resolve the ambiguity safely.

The model's default move should include an earnest check that it has enough context to build or change something responsibly. If the missing context can be recovered from the workspace, documentation, memory, or tools, recover it. If it cannot, ask before building.

### Context Recovery

Treat continuation language as a retrieval cue. Examples include "my project," "that workflow," "the thing we decided," "continue where we left off," "same as before," or any definite reference that assumes shared context.

For Codex, context recovery should check the current workspace, relevant docs, memory, and available thread history before answering. The model should not pretend the missing context is obvious.

If the continuation language is too vague to resolve after checking available context, ask a concise clarifying question before continuing. Do not invent the referent.

### Preference Discipline

Preference handling should live in the initial instruction layer of the pseudo harness, not as a standalone skill.

Apply user or project preferences only when they materially improve the current task, are relevant to the domain, and would not surprise the user. The latest explicit instruction wins over stored preference.

### Skill Preflight

Skill preflight is first-class priority for this project.

Before touching a specialized format, framework, workflow, domain, or tool-heavy task, check whether an existing skill or reference applies. Load the relevant instructions before writing code, creating files, editing deliverables, or using specialized tools.

This rule should become part of the harness spine, not optional advice buried in a reference.

### Output Surface Routing

Choose the form of the answer intentionally:

- Inline prose for explanations, strategy, reviews, summaries, and lightweight decisions.
- Files for reusable deliverables, docs, scripts, reports, specs, or anything the user asks to save, download, compare, submit, or reuse.
- Edits to the actual file when the user asks to modify an existing artifact.
- Visuals, diagrams, screenshots, or generated assets only when they materially improve understanding or are explicitly requested.
- A project/app implementation when the user asks for a usable tool, site, app, game, workflow, or code change.

The harness should prevent "fake deliverables" where the assistant says it created a file but only pasted content in chat.

### Environment Contract

Before producing files or running tool-heavy work, establish the environment contract:

- Which directories are writable.
- Which paths are source inputs versus final outputs.
- Which files are generated versus user-owned.
- Which persistence mechanisms are available.
- Which presentation mechanism the user expects.
- Which tools require schema discovery or setup before use.

Claude-specific artifact paths and UI rules should not be copied directly into this project unless we intentionally build a Claude-specific variant.

## Proposed Harness Placement

Stage 2 should provide the top-level operating loop for both harness modes:

- Always-on mode should keep these rules short and early.
- Situational mode should trigger these rules when a task involves files, tools, prior context, specialized formats, or nontrivial deliverables.
- Control mode should run without these rules so the A/B/C test has a true baseline.

## Open Design Questions

1. Should context recovery inspect memory before local project docs, or should local workspace state win by default?
2. Should skill preflight be mandatory for every code/file task, or only when the task touches a known specialized area?
3. Should the final harness expose its routing decision to the user, or keep routing silent unless the decision affects scope, cost, or risk?
4. Should output routing become a separate reference file, or stay in the main harness spine?

## Likely Implementation Pieces

- `SKILL.md`: concise operating loop and trigger description.
- `references/intake-and-routing.md`: detailed routing rules.
- `references/context-recovery.md`: continuation-language cues and clarification fallback.
- `references/output-surface-routing.md`: inline versus file versus visual versus implementation rules.
- `references/environment-contract.md`: workspace and tool-readiness checks.
