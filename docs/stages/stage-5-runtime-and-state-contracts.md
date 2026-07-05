# Stage 5: Runtime And State Contracts

## Status

Accepted as part of the main task harness.

Stage 5 is a guidance layer, not a separate skill. It should live inside the main harness references because it improves execution quality whenever work crosses tool, API, runtime, state, file, or rendering boundaries.

## Core Idea

Stage 5 prevents quiet runtime failure. It asks what the current execution environment requires so that schemas, state, files, structured responses, and tool outputs do not break between steps.

The useful abstraction is:

```text
Discover runtime contract -> preserve state -> use exact schemas -> parse structured outputs -> respect environment limits -> validate result.
```

## Main Rules

### Schema Discovery

Before using a dynamic, deferred, MCP, plugin, connector, or unfamiliar tool, discover its current schema and call it with exact parameter names and types.

Do not guess tool names, fields, enum values, path formats, or response structures. If a tool returns unexpected or empty results, re-check the schema and input format before retrying.

This rule extends Stage 4 parameter hygiene into runtime behavior.

### State Preservation

When a workflow spans multiple calls, explicitly carry forward the relevant state.

Relevant state can include:

- User goal and constraints.
- Current files and paths.
- Current app/workflow state.
- Prior tool outputs.
- Conversation turns needed for continuity.
- Authentication or connector choices.
- Generated IDs, handles, branch names, URLs, and run IDs.
- Current assumptions and unresolved questions.

Do not assume a tool, API, subagent, or model call remembers context that was not explicitly provided.

### Structured Output Discipline

When downstream code or tooling depends on model output, constrain the output format and validate it before use.

Use strict format instructions for JSON or other machine-readable outputs. Parse defensively. Treat malformed output as a recoverable runtime error, not as trustworthy data.

If a parser accepts only one shape, the model prompt and validation logic should both enforce that shape.

### Response Parsing By Structure

Process tool and API responses by explicit structure, not by assumed position, UI appearance, or brittle regex.

Prefer:

- Block type.
- JSON fields.
- Stable IDs.
- MIME types.
- Status codes.
- Structured metadata.

Avoid assuming that the first item in an array, first text block, first match, or rendered display string is the value that matters.

### Environment Contract

Before producing runtime-dependent output, establish the environment contract:

- Which paths are writable.
- Which paths are read-only.
- Which directory or URL the user can access.
- Which network access is available.
- Which runtime versions and libraries are available.
- Which persistence mechanisms are supported.
- Which UI/rendering limitations apply.
- Which files are source inputs versus generated outputs.

This overlaps with Stage 2's environment contract, but Stage 5 makes it operational during execution.

### Rendering And Visual Setup

Before producing specialized visual, UI, artifact, or frontend output, load or inspect the runtime/design constraints for that surface.

For Codex, this can mean reading the relevant skill, checking available libraries, starting the correct dev server, verifying with screenshots, or confirming generated assets render correctly.

Visual output should be validated in the environment where the user will actually inspect it.

### File And Media Handling

Handle files according to their actual type and runtime needs.

Do not blindly read binary files as text. Use appropriate parsers for PDFs, images, Office files, spreadsheets, archives, and structured data. Preserve media type and encoding when passing files to APIs or tools.

When modifying read-only or user-owned inputs, copy or create a new output rather than overwriting the source unless explicitly requested.

### Error Handling

Wrap fragile runtime calls in explicit error handling. Surface useful failure context without drowning the user in raw logs.

For recoverable errors, try the likely fix: re-check schemas, inspect paths, validate environment assumptions, retry with corrected input, or fall back to a safer tool.

For non-recoverable errors, report what was attempted, what failed, and what remains blocked.

### Source Attribution

When source-backed claims are produced from retrieved material, preserve attribution while writing in original words.

This belongs primarily to Stage 3, but Stage 5 should ensure the runtime path from retrieval to final answer does not lose citation/source metadata.

## Proposed Harness Placement

Stage 5 should live in the main `fable-task-harness` references:

- `references/runtime-and-state-contracts.md`
- `references/tool-schema-discovery.md`
- `references/structured-output-and-parsing.md`
- `references/environment-contract.md`

Likely templates:

- `templates/state-packet.md`
- `templates/structured-output-prompt.md`
- `templates/runtime-preflight-checklist.md`

The core harness should include a compact rule:

```text
When work crosses tool, API, file, state, or rendering boundaries, discover schemas, preserve state, parse structurally, respect the environment, and validate before using outputs.
```

## Relationship To Other Stages

- Stage 2 decides whether runtime-aware execution is needed.
- Stage 3 governs external research and source use.
- Stage 4 governs tool choice and tool contracts.
- Stage 5 governs execution correctness once tools, APIs, files, visuals, or stateful systems are involved.

## Open Design Questions

1. How much of Stage 5 should appear in the always-on harness spine versus references?
2. What should the minimum state packet include for A/B/C test projects?
3. Should runtime preflight be mandatory before every dev-server or browser-validation task?
4. How should the harness score runtime discipline during evaluations?

