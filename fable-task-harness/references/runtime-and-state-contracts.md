# Runtime And State Contracts

Use this reference when work crosses tool, API, file, runtime, state, rendering, or structured-output boundaries.

## Runtime Loop

```text
Discover environment contract -> preserve state -> use exact schemas -> parse structured outputs -> respect environment limits -> validate result.
```

## Environment Contract

Before file-writing, code execution, or runtime-dependent deliverables, check:

- Current working directory, writable paths, and read-only paths.
- Source inputs versus generated outputs.
- Runtime versions, package managers, and network availability.
- Persistence rules and available specialized tools.
- UI, rendering, or media constraints.
- Whether actions mutate files, external services, or user-facing state.

File boundaries:

- Inspect before editing. Do not overwrite user-owned inputs unless asked.
- Create sibling or generated outputs when preserving the current iteration matters.
- Do not read binary files as text. Use appropriate parsers for PDFs, Office files, spreadsheets, images, archives, and structured data.
- Start a dev server only when the app needs one. If a static file is enough, provide the local path instead of running unnecessary infrastructure.

## State Preservation

Carry forward:

- User goal and constraints.
- Current files, paths, and app, workflow, or tool state.
- Prior tool outputs and authentication or connector choices.
- Generated IDs, handles, URLs, run IDs, branch names, and paths.
- Current assumptions and unresolved questions.

Do not assume a tool, API, subagent, or model call remembers context that was not explicitly provided. Use the [state packet](../templates/state-packet.md) for long multi-step work.

## Structured Output Contract

When model output will be consumed by code, tools, or another model call, constrain the format:

- Name the exact format, required fields, and allowed enum values.
- State whether extra fields are allowed.
- Provide one compact example when useful.
- Require no prose outside the structured object when a parser expects only data.

The [structured output prompt template](../templates/structured-output-prompt.md) is a fillable version.

## Parsing And Validation

Validate before relying on outputs:

- Structured output parses; required fields exist; types and enum values are correct; lists are within expected bounds; strings are safe for their destination.
- Tool responses contain expected fields or block types.
- Files exist with expected type, size, and content.
- UI, visual, or media output renders where the user will inspect it.
- Runtime commands completed successfully.

Treat malformed output as a recoverable runtime error. Process by fields, not display order. Preserve raw output when useful for debugging, and handle missing or partial data explicitly.

## Example

A workflow step asks a model to extract tasks as JSON for a script to consume.

Wrong: pass the reply straight to `JSON.parse` and take `result[0]` as "the first task".

Right:

1. Prompt with the exact schema and "return only valid JSON".
2. Parse the reply; on failure, treat it as a recoverable error and re-prompt once with the parse error included.
3. Validate required fields and enum values before use.
4. Select items by their `id` field, not array position.
