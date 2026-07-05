# Tool Sequencing

Use this reference when a task requires tools, connectors, browser automation, APIs, or code execution.

## Core Sequence

```text
Identify tool domain -> verify fit -> satisfy preconditions -> call with exact parameters -> handle result -> complete follow-through.
```

## Common Ordering Rules

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

## Follow-Through

After tool use, make the result inspectable with a path, URL, screenshot, test result, branch, commit, PR, or concise verification summary.
