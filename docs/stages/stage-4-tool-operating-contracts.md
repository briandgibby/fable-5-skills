# Stage 4: Tool Operating Contracts

## Status

Accepted as the tool-contract layer of the Fable pseudo harness.

Stage 4 should not copy Fable's exact tool catalog. Most of those tools are environment-specific. The reusable value is the way each tool is documented and sequenced: a tool is not a magic button, but a contract with triggers, preconditions, parameters, side effects, and expected follow-through.

## Core Idea

Stage 4 teaches the harness to treat tools as specialized instruments. Use the tool closest to the task whenever possible. A generic tool can sometimes work, but only as a fallback when the right tool is unavailable.

The useful abstraction is:

```text
Identify tool domain -> verify fit -> satisfy preconditions -> call with exact parameters -> handle result -> complete follow-through.
```

## Main Rules

### Tool Cards

Every important tool should have a compact tool card that defines:

- What the tool does.
- When to use it.
- When not to use it.
- Required preconditions.
- Required sequencing before and after use.
- Parameter hygiene.
- Result handling.
- Side effects and turn-ending behavior.
- Failure recovery.

This should become a reusable `tool-card-template.md` reference.

### Specialized Tool Priority

Use the most specialized reliable tool available for the task before falling back to a generic tool.

Examples:

- Use a sports data tool for live scores before generic web search.
- Use a document parser for PDFs or Office files before ad hoc text extraction.
- Use a browser automation tool for interactive web validation before static HTTP fetching.
- Use a structural code rewrite tool before regex replacement when syntax matters.
- Use a connector or domain API when the requested data lives in that domain.

### Ask Only When Needed

Before asking the user for clarification, check whether the answer is already present or inferable from the conversation, current workspace, file names, query syntax, docs, or prior instructions.

If the user already gave meaningful constraints, proceed with those constraints and state any assumption. Do not ask questions merely to postpone judgment.

If the missing context cannot be safely recovered, ask a concise question before using tools or building.

### Workflow Sequencing

A tool card should identify required ordering. Common examples:

- Search before display when a display tool requires IDs from a search result.
- Inspect before edit when modifying an existing file.
- Create before present when producing a deliverable.
- Discover schema before calling a deferred tool.
- Read-only validation before mutation when a tool can change external state.
- Authentication or connector selection before accessing user-owned external data.

The harness should know not only which tool to use, but what must happen before and after that tool.

### Parameter Hygiene

Never guess identifiers, schemas, paths, coordinates, line ranges, old strings, or API fields.

Inspect or discover exact values before using them. Preserve case-sensitive IDs exactly. Treat displayed line numbers, UI labels, and rendered snippets as potentially different from raw source values.

For edits, prefer structured or syntax-aware mechanisms when available. If exact text replacement is used, verify uniqueness before replacing and re-read after successful edits.

### Side-Effect Boundaries

Classify each tool before use:

- Read-only.
- File-writing.
- User-facing presentation.
- External mutation.
- User elicitation.
- Turn-ending.
- Credential or connector flow.
- Code execution.

Tools that mutate state, send messages, change external systems, or end the turn need stronger preconditions than read-only inspection tools.

### Presenting Completed Work

Creating a deliverable is not enough. The agent must make the result accessible and inspectable.

For Codex, that usually means providing a concrete path, URL, test result, screenshot, branch/commit/PR directive, or clear verification summary. The user should not have to guess where the work landed.

### Strategic Variants

The message-composition tool encodes a useful general pattern: when a task is high-stakes or goal-ambiguous, offer variants that optimize for different outcomes, not merely different tones.

This pattern can apply to plans, product decisions, architecture choices, communication drafts, and research recommendations.

## Candidate GitHub Tools To Borrow Or Wrap

Do not replicate every Fable tool. Prefer established tools for capabilities that are hard to implement correctly.

Useful candidates to evaluate:

- [microsoft/playwright-mcp](https://github.com/microsoft/playwright-mcp) or [microsoft/playwright](https://github.com/microsoft/playwright) for browser automation, interaction, screenshots, and UI validation.
- [github/github-mcp-server](https://github.com/github/github-mcp-server) for GitHub issues, PRs, code context, and workflow automation through MCP.
- [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers) as reference implementations for writing MCP servers, not as drop-in production components.
- [microsoft/markitdown](https://github.com/microsoft/markitdown) for converting Office, PDF, HTML, and other files into Markdown-like LLM-readable text.
- [docling-project/docling](https://github.com/docling-project/docling) and [docling-project/docling-mcp](https://github.com/docling-project/docling-mcp) for more serious document conversion, layout extraction, and MCP-style document processing.
- [ocrmypdf/OCRmyPDF](https://github.com/ocrmypdf/OCRmyPDF) for scanned PDF OCR and searchable PDF generation.
- [ast-grep/ast-grep](https://github.com/ast-grep/ast-grep) for syntax-aware code search and rewriting when regex replacement is too brittle.
- [firecrawl/firecrawl](https://github.com/firecrawl/firecrawl) or [firecrawl/firecrawl-mcp-server](https://github.com/firecrawl/firecrawl-mcp-server) for web search, scraping, crawling, and clean content extraction in research-heavy workflows.

These should be considered candidate tools for future implementation, not dependencies to install automatically. Any MCP or external tool added for commercial use needs a trust-boundary and permission review first.

## Proposed Harness Placement

Stage 4 should support Stage 2 rather than sit in the always-on spine.

The core harness should say:

```text
If tools are needed, prefer specialized tools and follow their operating contracts.
```

The details should live in references:

- `references/tool-card-template.md`
- `references/tool-sequencing.md`
- `references/parameter-hygiene.md`
- `references/side-effect-boundaries.md`

## Open Design Questions

1. Which tool cards should be authored first for the A/B/C harness test?
2. Should candidate GitHub tools be wrapped as scripts, MCP servers, or just referenced as preferred external utilities?
3. Should mutation-capable tools require explicit confirmation by default in commercial contexts?
4. Should the harness include a standard "tool result follow-through" checklist?

