# Environment Contract

Use this reference before file-writing, code execution, tool-heavy work, app output, or runtime-dependent deliverables.

## Establish The Contract

Check:

- Current working directory.
- Writable and read-only paths.
- Source inputs and generated outputs.
- Runtime versions and package managers.
- Network availability.
- Persistence rules.
- Available specialized tools.
- UI, rendering, or media constraints.
- Whether actions mutate files, external services, or user-facing state.

## File Boundaries

- Inspect before editing.
- Do not overwrite user-owned inputs unless asked.
- Create sibling or generated outputs when preserving the current iteration matters.
- Do not read binary files as text.
- Use appropriate parsers for PDFs, Office files, spreadsheets, images, archives, and structured data.

## Runtime Boundaries

- Discover dependency/runtime paths before using bundled tooling.
- Start a dev server only when the app needs one.
- If a static file is enough, provide the local path instead of running unnecessary infrastructure.
- Validate generated visuals, UI, and media in the surface where the user will inspect them.
