# Candidate Simple Projects

These projects are small enough to run in isolated contexts but rich enough to reveal whether the task harness improves outcomes.

## Selection Criteria

- Fits in one short prompt.
- Produces an inspectable artifact.
- Can be completed in one session.
- Has objective verification checks.
- Leaves room for quality differences across runs.
- Does not require private credentials or paid services.
- Avoids current external facts unless the test is specifically research-focused.

## Recommended First Project

### 1. Static Focus Board

Build a single-page static web app for daily focus planning.

Why it is useful:

- Tests output-surface routing because the result should be an actual file, not prose.
- Tests frontend polish without needing a framework.
- Tests state handling through `localStorage`.
- Tests verification because the app can be opened directly in a browser.
- Tests scope discipline because it should stay small.

Frozen prompt candidate:

```text
Build a single-file static HTML app called Focus Board. It should let me add, edit, complete, and delete today's tasks; mark one task as the current focus; persist state in localStorage; and include a compact daily summary. Keep it usable on mobile and desktop. Put the finished artifact in the requested output folder and include brief verification notes.
```

Expected artifact:

- `index.html`
- Optional `README.md` only if needed.

Objective checks:

- Opens without a build step.
- Add, edit, complete, delete all work.
- Current focus is visually distinct.
- State survives reload.
- Mobile width remains usable.

## Other Strong Candidates

### 2. CSV Habit Summary CLI

Build a tiny CLI or script that reads a CSV of habit logs and writes a markdown summary.

Why it is useful:

- Tests structured parsing and file output.
- Tests use of standard library before dependencies.
- Easy to verify with sample input and expected output.

Expected artifacts:

- Script file.
- Sample CSV.
- Generated markdown report.
- Brief verification command.

### 3. Markdown Decision Brief

Given three short source notes, produce a decision brief with options, tradeoffs, recommendation, and open questions.

Why it is useful:

- Tests context routing and synthesis.
- Tests source attribution without requiring live web search.
- Easy to blind review for clarity and completeness.

Expected artifacts:

- `decision-brief.md`
- Source note references.

### 4. Mini Issue Triage Board

Build a local markdown-based issue board with status folders and a status report.

Why it is useful:

- Tests folder-as-state design.
- Tests stage handoffs and file organization.
- Directly mirrors the project philosophy.

Expected artifacts:

- `issues/backlog/`, `issues/ready/`, `issues/done/`
- Example issue files.
- `status.md`

### 5. Small Refactor Task

Provide a deliberately messy single-file script and ask the agent to simplify it without changing behavior.

Why it is useful:

- Tests inspect-before-edit discipline.
- Tests verification and scope control.
- Good for comparing maintainability outcomes.

Expected artifacts:

- Updated script.
- Before/after notes.
- Test or command output.

## Suggested Test Order

1. Static Focus Board.
2. CSV Habit Summary CLI.
3. Markdown Decision Brief.
4. Small Refactor Task.
5. Mini Issue Triage Board.
