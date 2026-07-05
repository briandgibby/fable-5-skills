# Pragmatic AI Build Principles

Use this reference when deciding how much autonomy, structure, tooling, or verification an agentic workflow should have.

## Software 3.0 Posture

Prompts, context windows, examples, tool definitions, memory, and templates are part of the program. Treat them like source code:

- Keep them small enough to review.
- Put durable rules in canonical files.
- Prefer explicit schemas and examples over vague prose.
- Verify behavior after changing instructions.

## Human And Agent Roles

Humans should curate sources, set direction, review judgment calls, and decide when an output is good enough.

Agents should handle bookkeeping, drafting, cross-linking, formatting, structured transformations, and repetitive checks.

## Build Style

- Work in small concrete chunks.
- Keep the generation-verification loop fast.
- Make intermediate artifacts inspectable.
- Prefer partial autonomy before full autonomy.
- Add checkpoints where judgment matters.
- Use deterministic scripts when the job is mechanical.
- Meet agents halfway with clear files, commands, paths, schemas, and expected outputs.

## Reliability Stance

Do not design as if agents are fully reliable. Design so mistakes are easy to catch:

- Stage audits before handoff.
- Source-backed claims with links.
- Structured outputs with validation.
- Tool calls with exact schemas.
- Human review gates for high-impact choices.

## Practical Test

Before adding machinery, ask:

- Is this workflow repeatable?
- Does each stage produce a distinct artifact?
- Can a human review or edit the handoff?
- Would a local script be more reliable than a model call?
- Is the context contract clearer than orchestration code?
