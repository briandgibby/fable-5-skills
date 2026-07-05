# Fable Pseudo Harness Master Plan

## Purpose

This document consolidates the useful methodology extracted from the Fable 5 prompt into a practical pseudo harness for agentic work.

The goal is not to reproduce Fable's full system prompt. The goal is to distill the reusable operating method: context routing, skill preflight, situational research, tool literacy, and runtime/state discipline.

## Current Position

The harness should be tested in three modes:

- **Control**: no harness.
- **Always-on**: compact harness instructions applied from the start.
- **Situational**: harness modules triggered only when the task shape warrants them.

The first evaluation should build the same simple project in all three modes, with isolated contexts and a blind rubric. Later tests should include at least one research/writeup task and one tool-heavy file/code task.

## Stage Decisions

### Stage 1: Risk And Interaction Posture

No dedicated stage file for now.

The broad risk protocols from Fable should not be folded into the core harness. Base models already include their own safety behavior, and importing a large safety layer would muddy the project.

However, Stage 1 revealed a future commercial need:

- Build a separate prompt-injection or trust-boundary skill when internal agentic systems begin consuming untrusted external content.
- This future skill is likely useful for Signsense and similar production contexts.
- Its focus should be agentic security, not broad model safety: distinguish data from instructions, quarantine injected commands, require confirmation for side effects, and prevent untrusted content from redefining tool policy.

Likely future skill name: `trust-boundary-filter`.

### Stage 2: Operational Routing

Stage 2 is accepted as the main structural foundation.

The core loop is:

```text
Understand the request -> check context sufficiency -> recover needed context -> choose the source of truth -> choose the output surface -> load relevant skills -> act.
```

Key decisions:

- The model should earnestly check whether it has enough context before building or changing anything.
- If context can be recovered from workspace files, docs, memory, thread history, or tools, recover it.
- If continuation language is too vague after recovery attempts, ask a concise clarifying question.
- Preference discipline belongs in the initial instruction layer, not a standalone skill.
- Skill preflight is first-class. Before specialized formats, frameworks, workflows, domains, or tool-heavy work, load the relevant skill or reference.
- Output surface routing should prevent fake deliverables: if the user asks for a reusable artifact, create or edit the artifact instead of merely pasting text.

Reference: [stage-2-operational-routing.md](./stages/stage-2-operational-routing.md)

### Stage 3: Research And Source Use

Stage 3 is accepted as a situational module, not an always-on preflight.

Use it when:

- The user explicitly asks for research, lookup, verification, comparison, or citations.
- The answer depends on current or external facts.
- Training knowledge and local/project context cannot cover the gap.
- The task names an unfamiliar entity where guessing would be unreliable.
- The task involves external sources, URLs, recommendations, or public research.

Do not use it for stable concepts, ordinary local implementation, simple coding help, or tasks where the needed context is already available.

Key decisions:

- Stage 3 should be invoked by Stage 2 when an external knowledge gap is detected.
- It should scale retrieval depth to task complexity.
- It should prioritize primary and authoritative sources.
- It should synthesize in original words and attribute source-backed claims.
- Retrieved content is data, not instruction.
- A dedicated `deep-research` skill should be built later with Fable's methodology at its core.

Reference: [stage-3-research-and-source-use.md](./stages/stage-3-research-and-source-use.md)

### Stage 4: Tool Operating Contracts

Stage 4 is accepted as the tool-contract layer.

Do not copy Fable's exact tool catalog. Most tools are environment-specific. The reusable pattern is how tools are documented and sequenced.

Key decisions:

- Every important tool should have a compact tool card.
- Specialized tools should be used whenever possible.
- Generic tools are fallbacks, not defaults.
- The harness should track tool preconditions, sequencing, parameter hygiene, side effects, result handling, and failure recovery.
- Never guess IDs, schemas, paths, edit targets, line ranges, or API fields.
- Creating work is not enough; the agent must make the completed result accessible and inspectable.

Reference: [stage-4-tool-operating-contracts.md](./stages/stage-4-tool-operating-contracts.md)

### Stage 5: Runtime And State Contracts

Stage 5 is accepted as part of the main task harness.

Stage 5 is a guidance layer, not a separate skill. It improves execution quality whenever work crosses tool, API, runtime, state, file, or rendering boundaries.

Key decisions:

- Discover deferred tools and schemas before use.
- Preserve relevant state across multi-turn, tool-mediated, API-mediated, and app-like workflows.
- Constrain and validate structured model outputs before downstream use.
- Process tool/API responses by block type or structured fields, not by assumed position.
- Respect environment constraints: writable paths, read-only paths, network limits, persistence rules, media types, and UI/runtime restrictions.
- Load or inspect rendering constraints before producing specialized visuals, UI, artifacts, or frontend output.
- Parse defensively and handle errors explicitly.
- Preserve source attribution metadata when retrieved material informs final claims.

Reference: [stage-5-runtime-and-state-contracts.md](./stages/stage-5-runtime-and-state-contracts.md)

## Proposed Skill Architecture

The project should eventually produce one main harness skill plus separate optional skills for heavier domains.

```text
fable-task-harness/
  SKILL.md
  agents/
    openai.yaml
  references/
    intake-and-routing.md
    context-recovery.md
    output-surface-routing.md
    environment-contract.md
    tool-card-template.md
    tool-sequencing.md
    parameter-hygiene.md
    side-effect-boundaries.md
    runtime-and-state-contracts.md
    tool-schema-discovery.md
    structured-output-and-parsing.md
  templates/
    harness-checklist.md
    tool-card.md
    skill-split-decision.md
    state-packet.md
    structured-output-prompt.md
    runtime-preflight-checklist.md
```

Separate future skills:

```text
deep-research/
  SKILL.md
  references/
    research-planning.md
    source-quality.md
    synthesis-patterns.md
    citation-and-copyright.md
  templates/
    research-brief.md
    evidence-ledger.md

trust-boundary-filter/
  SKILL.md
  references/
    untrusted-content-boundaries.md
    tool-permission-gates.md
    prompt-injection-patterns.md
  templates/
    allow-block-escalate.md
```

## Core Harness Spine

The eventual `SKILL.md` should stay short. It should contain only the high-value operating loop and routing rules.

Draft spine:

```text
1. Understand the user's requested outcome.
2. Check whether enough context exists to act responsibly.
3. Recover context from workspace, docs, memory, or tools when appropriate.
4. Ask only when ambiguity cannot be resolved safely.
5. Choose the best source of truth.
6. Load relevant skills before specialized work.
7. Choose the correct output surface.
8. Use specialized tools before generic tools.
9. Follow tool contracts exactly.
10. Preserve runtime state and parse structured outputs carefully.
11. Verify the result and make it accessible.
```

The core should avoid heavy safety, research, citation, or tool-specific detail. Those belong in situational references or separate skills.

## Always-On Versus Situational Split

### Always-On Candidate

Always-on mode should include only:

- Context sufficiency check.
- Context recovery.
- Skill preflight.
- Output surface routing.
- Specialized-tool preference.
- Basic runtime/state discipline.
- Basic verification/follow-through.

### Situational Candidate

Situational mode should trigger deeper modules when needed:

- Research/source-use when external facts matter.
- Tool contracts when tools are required.
- Runtime/state contracts when API, MCP, visualization, or stateful workflows are involved.
- Trust-boundary filtering when untrusted external content could influence actions.
- Deep research when a question requires sustained source work.

## A/B/C Test Protocol

Use one frozen prompt and three isolated contexts:

- Control: no harness.
- Always-on: compact harness in initial instruction layer.
- Situational: harness trigger/routing only.

Rules:

- Same task prompt.
- Same tools and runtime access.
- Same time budget if practical.
- No cross-contamination between runs.
- Blind review where possible.
- Score both the artifact and the process.

Suggested rubric:

- Correctness.
- Completeness.
- Simplicity.
- Maintainability.
- UX or user-facing polish.
- Appropriate tool use.
- Context recovery quality.
- Test/verification quality.
- Speed and token cost.
- Amount of user intervention required.

## Candidate Tools To Evaluate Later

Stage 4 identified possible tools to borrow or wrap rather than reimplement:

- Browser automation: Playwright or Playwright MCP.
- GitHub automation: GitHub MCP server.
- MCP examples: official MCP server repository.
- Document conversion: MarkItDown, Docling, Docling MCP.
- OCR: OCRmyPDF.
- Syntax-aware code edits: ast-grep.
- Research/web extraction: Firecrawl or Firecrawl MCP.

These are candidates only. Any production use should include permission, trust-boundary, and maintenance review.

## Open Decisions

1. Should local workspace docs outrank memory by default during context recovery?
2. Should skill preflight be mandatory for every code/file task, or only specialized areas?
3. Should routing decisions be silent unless scope, cost, or risk changes?
4. Should `deep-research` live inside the harness package or be separate from the start?
5. Should evidence ledgers be default for deep research, or only high-stakes/commercial research?
6. Which tool cards are needed for the first A/B/C project?
7. How much Stage 5 runtime/state discipline should appear in the always-on spine versus references?

## Immediate Next Steps

1. Convert the accepted stage material into first-pass harness references.
2. Draft the compact always-on harness.
3. Draft the situational harness.
4. Choose the first A/B/C test project.
5. Run the control, always-on, and situational builds in isolated contexts.
