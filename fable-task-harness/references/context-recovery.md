# Context Recovery

Use this reference when the user uses continuation language or the task assumes shared context.

## Continuation Cues

Treat these as retrieval cues:

- "My project"
- "That workflow"
- "The thing we decided"
- "Continue where we left off"
- "Same as before"
- "The current version"
- Any definite reference without a local noun

## Recovery Order

Use the cheapest reliable surface first:

1. Current conversation.
2. Current workspace files and docs.
3. Project-specific memory or thread history.
4. Connected tools or apps that own the live state.
5. Web or external sources when the missing context is public, current, or external.
6. User clarification.

Local workspace state normally outranks memory because it is fresher and inspectable. Memory is useful for prior decisions, preferences, and paths, but may be stale.

## Clarification Threshold

Ask a concise question when:

- Multiple plausible referents remain after recovery.
- The wrong choice would cause destructive edits, external mutations, or wasted work.
- The user asked for a specific artifact but the target path or format cannot be inferred.
- The workspace and memory disagree in a material way.

Do not ask merely to postpone judgment when the context is recoverable.

## State To Carry Forward

When continuing after recovery, keep these visible to yourself:

- User goal.
- Source of truth used.
- Relevant files, paths, IDs, URLs, or tool handles.
- Assumptions.
- Unresolved questions.
- Verification needed before final response.

## Example

Task: "Pick up where we left off on the importer."

Wrong: immediately ask "Which importer?", or guess and start rebuilding from scratch.

Right: check the conversation, then the workspace — recent commits, importer-named files, TODO or handoff notes — and resume from the recovered state, stating what was found. Ask only if two or more plausible importers remain after that.
