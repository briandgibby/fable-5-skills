# Runtime And State Contracts

Use this reference when work crosses tool, API, file, runtime, state, rendering, or structured-output boundaries.

## Runtime Loop

```text
Discover runtime contract -> preserve state -> use exact schemas -> parse structured outputs -> respect environment limits -> validate result.
```

## State Preservation

Carry forward:

- User goal and constraints.
- Current files and paths.
- Current app, workflow, or tool state.
- Prior tool outputs.
- Authentication or connector choices.
- Generated IDs, handles, URLs, run IDs, branch names, and paths.
- Current assumptions and unresolved questions.

Do not assume a tool, API, subagent, or model call remembers context that was not explicitly provided.

## Validation

Validate before relying on outputs:

- Structured model output parses as required.
- Tool responses contain expected fields or block types.
- Files exist and have expected type/size/content.
- UI, visual, or media output renders where the user will inspect it.
- Runtime commands completed successfully.
- Follow-up actions use the verified state, not stale assumptions.

## Related References

- [tool-schema-discovery.md](tool-schema-discovery.md)
- [structured-output-and-parsing.md](structured-output-and-parsing.md)
- [environment-contract.md](environment-contract.md)
