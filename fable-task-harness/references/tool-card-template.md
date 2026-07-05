# Tool Card Template Guide

Use this reference when documenting an important tool for the harness.

Every important tool should have a compact tool card. A tool card defines the contract around the tool so agents do not treat it as a magic button.

## Required Sections

- What it does.
- When to use it.
- When not to use it.
- Preconditions.
- Required sequencing.
- Parameter hygiene.
- Result handling.
- Side effects.
- Failure recovery.

## Writing Rules

- Keep the card operational and short.
- Use exact parameter names only when they are stable.
- Mention schema discovery for dynamic tools.
- Classify side effects clearly.
- Include what to verify after use.
- Prefer examples that show sequencing, not just syntax.

See [../templates/tool-card.md](../templates/tool-card.md) for a fillable card.
