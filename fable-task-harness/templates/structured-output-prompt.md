# Structured Output Prompt

Use this template when another model call must produce machine-readable output.

```text
Return only valid JSON.

Schema:
{
  "items": [
    {
      "id": "string",
      "label": "string",
      "status": "pending|complete|blocked",
      "notes": "string"
    }
  ]
}

Rules:
- Include all required fields.
- Use only the allowed status values.
- Do not include extra top-level fields.
- Do not include markdown or commentary outside the JSON.
```

Validation before use:

- [ ] JSON parses.
- [ ] Required fields exist.
- [ ] Field types match.
- [ ] Enum values are allowed.
- [ ] Downstream consumer accepts the shape.
