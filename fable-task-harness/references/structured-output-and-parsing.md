# Structured Output And Parsing

Use this reference when model output will be consumed by code, tools, workflows, or another model call.

## Prompting Contract

Constrain the output format:

- Name the exact format.
- Define required fields.
- Define allowed enum values.
- State whether extra fields are allowed.
- Provide one compact example when useful.
- Require no prose outside the structured object when a parser expects only data.

## Parsing Contract

Validate before use:

- The output parses.
- Required fields exist.
- Field types are correct.
- Enum values are allowed.
- Lists are within expected bounds.
- Strings are safe for their destination.

Treat malformed output as a recoverable runtime error.

## Defensive Use

- Process by fields, not display order.
- Keep original source attribution with extracted claims.
- Preserve raw output when useful for debugging.
- Handle missing or partial data explicitly.
