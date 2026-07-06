# Tool Contracts

Use this reference when a task requires tools, connectors, browser automation, APIs, or code execution — especially unfamiliar, dynamic, deferred, MCP, or plugin tools.

## Core Sequence

```text
Identify tool domain -> verify fit -> discover schema if unfamiliar -> satisfy preconditions -> call with exact parameters -> handle result -> follow through.
```

## Ordering Rules

- Search before display when display requires IDs from search results.
- Inspect before edit when modifying an existing file.
- Read-only validation before mutation when a tool can change external state.
- Discover schema before using a deferred, dynamic, MCP, plugin, connector, or unfamiliar tool.
- Authenticate or select the connector before accessing user-owned external data.
- Create the deliverable before presenting it.
- Verify after mutation.

## Specialized Tool Priority

Use the most specialized reliable tool available before falling back to generic tools:

- Domain data tools before generic web search.
- Document parsers before ad hoc text extraction.
- Browser automation before static fetching for interactive UI validation.
- Syntax-aware code tools before regex replacement when syntax matters.
- Connectors or domain APIs when the requested data lives in that domain.

## Exact Inputs

Do not guess paths, IDs, schemas, coordinates, line ranges, old strings for replacement, API fields, enum values, MIME types, branch names, issue numbers, or run IDs. Inspect or discover exact values before using them.

Edit hygiene:

- Read the target before editing.
- Verify exact text uniqueness before replacement.
- Prefer structured or syntax-aware edits when available.
- Re-read after edits and preserve unrelated user changes.
- Do not normalize formatting or metadata outside the requested scope.

## Schema Discovery

For dynamic or unfamiliar tools:

- Discover the current tool name, parameters, types, required fields, enum values, and response shape from official tool metadata, not memory or old examples.
- Use only documented parameter names. Omit optional empty values unless the schema requires them.
- Do not invent IDs, cursors, page numbers, selectors, or connector names.
- Respect tool-specific sequencing and turn-ending behavior.

## Result Handling

- Parse by explicit fields, block types, status codes, MIME types, and stable IDs — never by display order or assumed position.
- Treat empty or unexpected results as a schema or input problem before retrying.
- Do not retry an identical failing call; change something diagnosable first.
- Preserve generated handles, IDs, cursors, and resource URIs exactly for follow-up calls.

## Follow-Through

After tool use, make the result inspectable with a path, URL, screenshot, test result, branch, commit, PR, or concise verification summary.

When the tool's interface was undocumented, state how you discovered it — help output, source read, or both — and record the exact working command in your notes.

Document important recurring tools with a [tool card](../templates/tool-card.md).

## Example

Task: "Close the stale issue about the login bug."

Wrong: call `close_issue(id=123)` because 123 is remembered from a similar repo.

Right:

1. `search_issues(query="login bug", state="open")` returns issue `#87`.
2. Confirm `#87` matches the described issue by title and body.
3. `close_issue(id=87)`.
4. Re-fetch `#87`, confirm state is `closed`, and report the issue URL.
