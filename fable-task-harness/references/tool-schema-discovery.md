# Tool Schema Discovery

Use this reference before calling dynamic, deferred, MCP, plugin, connector, or unfamiliar tools.

## Discovery Rules

- Discover the current tool name, parameters, types, required fields, enum values, and response shape.
- Prefer official tool metadata or schema over examples.
- Do not infer schema from memory when discovery is cheap.
- If the tool returns empty or unexpected results, re-check schema and input format before retrying.
- Preserve generated handles, IDs, cursors, and resource URIs exactly.

## Calling Rules

- Use only documented parameter names.
- Omit optional empty values unless the schema requires them.
- Do not invent IDs, cursors, page numbers, selectors, or connector names.
- Respect tool-specific sequencing and turn-ending behavior.

## Result Rules

- Parse by explicit fields, block types, status codes, MIME types, and stable IDs.
- Do not assume the first item in an array is the target.
- Store the state needed for follow-up calls.
