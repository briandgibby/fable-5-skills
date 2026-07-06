# Initial A/B/C Test Plan: Static Focus Board

> Historical record of run 1 (2026-07-05, harness 0.1.0). The arm design here — always-on versus situational modes — no longer matches the shipped skill, and the methodology was superseded by `protocol.md` after this run exposed its weaknesses (n=1, unfrozen arm prompts, unblinded self-scoring, unmeasured cost). Do not use this plan for new runs.

## Goal

Compare whether the Fable task harness improves a small but complete implementation task.

## Frozen Prompt

```text
Build a single-file static HTML app called Focus Board. It should let me add, edit, complete, and delete today's tasks; mark one task as the current focus; persist state in localStorage; and include a compact daily summary. Keep it usable on mobile and desktop. Put the finished artifact in the requested output folder and include brief verification notes.
```

## Modes

| Mode | Instruction setup | Output folder |
|------|-------------------|---------------|
| Control | No harness instructions | `evals/runs/static-focus-board/control/` |
| Always-on | Load compact `fable-task-harness/SKILL.md` from the start | `evals/runs/static-focus-board/always-on/` |
| Situational | Start with routing only, then load only explicitly allowed references as task shape warrants | `evals/runs/static-focus-board/situational/` |

## Isolation Rules

- Use separate contexts for each mode.
- Do not show one run's output to another run.
- Use the same frozen prompt for all modes.
- Use the same available tools and time expectations.
- Do not manually improve outputs before scoring.
- For situational runs, do not load `fable-task-harness/SKILL.md` after the run starts unless the test explicitly allows it.
- Parent review may inspect all outputs only after all three isolated runs are complete.

## Required Artifacts

| Artifact | Location | Format |
|----------|----------|--------|
| Control app | `evals/runs/static-focus-board/control/index.html` | HTML |
| Always-on app | `evals/runs/static-focus-board/always-on/index.html` | HTML |
| Situational app | `evals/runs/static-focus-board/situational/index.html` | HTML |
| Review | `evals/runs/static-focus-board/review.md` | Markdown |

## Verification Checklist

- [ ] Each `index.html` opens without a build step.
- [ ] Task add, edit, complete, delete work.
- [ ] Current focus can be set and cleared or changed.
- [ ] `localStorage` persists tasks after reload.
- [ ] Daily summary reflects current state.
- [ ] Mobile viewport remains usable.
- [ ] No console errors during basic workflow.
- [ ] Parent reviewer runs the same browser smoke test against all three outputs before scoring.

## Scoring

Use `evals/rubric.md`.

Record any repeated failures as source-improvement candidates. Examples:

- If outputs miss verification, update harness verification rules.
- If outputs overbuild, update simplicity guidance.
- If outputs do not create actual files, update output-surface routing.
- If UI is rough but functional, decide whether frontend guidance belongs in this harness or in a separate skill.
