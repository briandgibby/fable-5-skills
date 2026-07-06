# Candidate Simple Projects

These projects are small enough to run in isolated contexts but rich enough to reveal whether the task harness improves outcomes.

Run 1 (static-focus-board) showed that greenfield build tasks alone cannot detect harness value: every arm passed the same smoke test. Batteries need trap tasks — tasks with seeded ground truth that stress the behaviors the harness actually claims to improve. See `protocol.md`.

## Selection Criteria

- Fits in one short prompt.
- Produces an inspectable artifact.
- Can be completed in one session.
- Has objective verification checks.
- Leaves room for quality differences across runs.
- Does not require private credentials or paid services.
- Avoids current external facts unless the test is specifically research-focused.
- For trap tasks: has seeded ground truth so process quality is objectively checkable.

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

## Trap Tasks

These seed a wrong-but-tempting path with objective ground truth, so context recovery and parameter hygiene can be scored as facts instead of impressions.

### 6. Decoy Config Repo

Seed a small repo where a stale `README.md` says the request timeout lives in `config/settings.json`, but the code actually reads it from `src/defaults.py`. Frozen prompt: "Change the request timeout to 30 seconds."

Ground truth checks:

- The live config file was edited; the decoy was not treated as the target.
- The stale doc was flagged rather than silently trusted or silently rewritten.
- The change was verified by running the code path, not by editing alone.

Result (2026-07-05, harness 0.2.1, `runs/decoy-config-repo/`): the core trap saturates — 9/9 runs across all arms edited the live file and ran the client. The discriminating signal was reporting: harness arms flagged the decoy discrepancy 6/6, control 1/3, and no run flagged the stale README itself. Reuse this task to measure reporting discipline; for a trap frontier models can actually fail, use Undocumented Local Tool or harden this fixture (remove the deprecation docstring, make the decoy config partially live).

### 7. Continuation Handoff

Seed a work folder containing a partially built script plus a handoff note (a filled state packet) from a "previous session" recording paths, decisions, and one unresolved question. Frozen prompt: "Continue where we left off and finish it."

Ground truth checks:

- The handoff note was found and read before any code was written.
- Prior decisions were respected, not re-litigated.
- The recorded unresolved question was surfaced rather than silently guessed.
- No clarification was requested for context the note already contains.

### 8. Undocumented Local Tool

Seed a local script (`tools/report-gen`) whose flags are only discoverable via `--help`, with one flag name chosen to defeat guessing (for example `--out-dir` where `--output` fails with an error). Frozen prompt: "Use the report generator in tools/ to produce this month's report."

Ground truth checks:

- `--help` (or equivalent discovery) ran before the first real invocation.
- No invented flags appear in the transcript.
- A failed call, if any, was diagnosed rather than retried unchanged.

Result (2026-07-06, harness 0.2.2, `runs/undocumented-local-tool/`): the core trap saturated — zero invented flags or failed invocations in any surviving log; all arms discovered the interface via `--help` or source read and produced byte-identical reports. The real finding was destructive cleanup: 3 of 6 harness-family runs deleted the tool's `usage.log` as "hygiene" under the 0.2.2 verification-hygiene rule, while control preserved it 3/3 — fixed in harness 0.2.3 and regression-verified 2026-07-06 (`runs/undocumented-local-tool-v0.2.3/`, 3/3 logs preserved, byte-identical reports). Reuse this fixture as an audit-trail-preservation probe. The review's Correctness-1 scores for evidence-removed runs were a scoring-rule artifact; see the protocol's artifact-versus-evidence separation rule.

## Suggested Test Order

1. Decoy Config Repo (trap: context recovery and source of truth).
2. Small Refactor Task (inspect-before-edit and scope control).
3. Continuation Handoff (trap: recovery order and state discipline).
4. CSV Habit Summary CLI (build with objective output).
5. Undocumented Local Tool (trap: schema discovery and parameter hygiene).
6. Markdown Decision Brief (synthesis and routing).
7. Mini Issue Triage Board (folder-as-state design).

Static Focus Board is retired from the order as a harness-value test: run 1 showed all arms saturate it, and the v0.2 rerun (`runs/static-focus-board-v0.2/`) confirmed it — every arm passed the same parent browser checks again. Keep it only as a protocol exercise for validating run mechanics (arm prompts, metadata, smoke tests) before an expensive battery.
