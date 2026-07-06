# Verification Playbook

Use this reference before declaring any work verified or finished.

Every artifact type has a depth ladder from strongest to weakest verification. Start at the top. If a rung is blocked, step down, keep going, and report which rung you reached. Never present a lower rung as if it were a higher one.

## Depth Ladders

### Static Web App Or Page

1. Real browser: load the page, exercise every requested behavior, watch the console, and test the smallest requested viewport.
2. If `file://` navigation is blocked: serve the folder locally (for example `python -m http.server`) and run the same checks against localhost.
3. If no browser is available: DOM-level simulation in a runtime (Node, jsdom) covering the same behaviors.
4. Last resort: static checks — files exist, constraints hold, scripts parse, required handlers and persistence code are present.

### CLI Or Script

1. Run it against real sample input and compare actual output to expected output.
2. If execution is blocked: dry-run or help invocation to confirm the interface exists as described.
3. Last resort: syntax or parse check plus a manual trace of the main path.

### Code Change In A Repo

1. Run the project's tests, or the affected subset.
2. If no tests exist: run the affected command, endpoint, or entry path directly.
3. Type-check, lint, or build.
4. Last resort: read the final diff line by line against the requested behavior.

### Documents And Markdown

1. Render or preview the document where the user will read it.
2. Check that every relative link and referenced file resolves.
3. Check structure against the requested sections or governing template.

### Data Outputs

1. Validate against the schema or expected columns.
2. Spot-check real rows against the source.
3. Sanity-check counts, ranges, and duplicates.

## Verification Hygiene

Verification must not contaminate the deliverable. Do not leave build caches, bytecode, or temp files that your own checks created — for Python smoke checks, set `PYTHONDONTWRITEBYTECODE=1`.

Cleanup applies only to artifacts your verification created. Logs, audit trails, state files, receipts, and history that a tool or system produced during its normal operation are records, not litter — never delete them as cleanup. When unsure whether a generated file is disposable, leave it in place and mention it in your notes.

## Reporting Rule

Verification notes must state:

- Which checks ran and what they found.
- The highest rung reached, and which rungs were blocked and why.
- What remains unverified.
- Any stale doc, config, or reference encountered that contradicts the live source of truth — name the stale file and the live one, so the reader learns what you learned.
- Any files the work generated beyond the requested artifact — logs, records, caches deliberately left in place — named, with one line on why they were left.

Weak verification written confidently is worse than a plainly reported blocked check.

## Example

An in-app browser refuses `file://` URLs while verifying a static HTML app.

Wrong: fall back to scanning the HTML for handler names and report the app as verified.

Right: serve the output folder with `python -m http.server 8765`, run the interactive checks against `http://127.0.0.1:8765/index.html`, and report: "Verified at rung 2 — localhost browser session; direct `file://` loading was blocked by browser URL policy."
