# Evaluation Plan: {{EVALUATION_NAME}}

## Goal

Compare task outcomes across control, always-on harness, and situational harness runs.

## Frozen Prompt

```text
{{PROMPT}}
```

## Modes

| Mode | Harness instructions | Isolation rule |
|------|----------------------|----------------|
| Control | No harness | Fresh context and fresh output folder |
| Always-on | Compact harness from task start | Fresh context and fresh output folder |
| Situational | Routing trigger plus relevant modules | Fresh context and fresh output folder |

## Required Outputs

| Artifact | Location | Format |
|----------|----------|--------|
| Control output | `evals/runs/{{SLUG}}/control/` | Project artifact |
| Always-on output | `evals/runs/{{SLUG}}/always-on/` | Project artifact |
| Situational output | `evals/runs/{{SLUG}}/situational/` | Project artifact |
| Review notes | `evals/runs/{{SLUG}}/review.md` | Markdown |

## Verification

- [ ] Artifact runs or opens.
- [ ] Required files exist.
- [ ] User-facing result is inspectable.
- [ ] Rubric completed blind where practical.
- [ ] Repeated corrections are routed back to source files.
