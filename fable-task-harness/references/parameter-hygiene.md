# Parameter Hygiene

Use this reference before calling tools, editing files, invoking APIs, or passing structured data downstream.

## Do Not Guess

Do not guess:

- Paths.
- IDs.
- Schemas.
- Coordinates.
- Line ranges.
- Old strings for replacement.
- API fields.
- Enum values.
- MIME types.
- Branch names, issue numbers, or run IDs.

Inspect or discover exact values before using them.

## Edit Hygiene

- Read the target before editing.
- Verify exact text uniqueness before replacement.
- Prefer structured or syntax-aware edits when available.
- Re-read after edits.
- Preserve unrelated user changes.
- Do not normalize formatting or metadata outside the requested scope.

## Structured Inputs

- Validate JSON or machine-readable output before use.
- Preserve case-sensitive identifiers.
- Process responses by stable fields, not display order.
- Treat empty or unexpected tool results as a schema/input problem before retrying.
