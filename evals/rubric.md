# Harness Evaluation Rubric

Score blind (see `protocol.md`), compute totals, and record process metrics from transcripts. Subjective scores without computed totals and measured metrics are not a complete review.

## Artifact And Process Scores

Score each dimension from 1 to 5.

| Score | Meaning |
|-------|---------|
| 1 | Fails or misses the point |
| 2 | Partially works but has major gaps |
| 3 | Works with noticeable rough edges |
| 4 | Solid and usable |
| 5 | Excellent for the task size |

| Dimension | What to look for |
|-----------|------------------|
| Correctness | Required behavior works under the uniform objective checks |
| Completeness | All requested outputs are present |
| Simplicity | Nothing built beyond the request; no unnecessary machinery |
| Maintainability | Files are readable, organized, and easy to change |
| UX or reader polish | User-facing result feels coherent and usable |
| Appropriate tool use | Tools match the task and are not overused |
| Context recovery | Agent found and used the right source of truth (trap tasks have ground truth) |
| Output routing | Agent created or edited the right artifact in the right place |
| Verification | Depth ladder rung reached, honestly reported, blocked rungs named |
| User intervention | Agent needed little clarification for recoverable context |

Speed and cost are no longer a 1-5 dimension. They are measured, not felt — see process metrics.

## Process Metrics

Record per run from metadata and transcripts. These are counts and measurements, not scores.

| Metric | Source |
|--------|--------|
| Input/output tokens | `run-meta.md` |
| Wall time | `run-meta.md` |
| Tool calls | `run-meta.md` |
| Files read | `run-meta.md` |
| Clarification questions | `run-meta.md` |
| Guessed parameters (IDs, paths, flags used without discovery) | transcript |
| Wrong-file reads or edits | transcript |
| Verification depth rung reached | verification notes vs playbook ladder |
| Unrequested features shipped | artifact vs frozen prompt |
| References loaded and trigger cited (harness arm only) | verification notes |

## Review Notes Template

```md
# Review: {{RUN_NAME}}

Harness version tested:
Runs per arm:
Blind scoring mapping attached: yes/no

## Scores (median across runs)

| Dimension | Control | Harness | Full-load | Notes |
|-----------|---------|---------|-----------|-------|
| Correctness | | | | |
| Completeness | | | | |
| Simplicity | | | | |
| Maintainability | | | | |
| UX or reader polish | | | | |
| Appropriate tool use | | | | |
| Context recovery | | | | |
| Output routing | | | | |
| Verification | | | | |
| User intervention | | | | |
| **Total (computed)** | | | | |

## Process Metrics (median across runs)

| Metric | Control | Harness | Full-load |
|--------|---------|---------|-----------|
| Tokens (in/out) | | | |
| Wall time | | | |
| Tool calls | | | |
| Clarifications | | | |
| Guessed parameters | | | |
| Wrong-file edits | | | |
| Verification rung | | | |
| Unrequested features | | | |

## Winner

- Winner:
- Totals support the winner: yes/no
- Tie-break applied (lower cost wins): yes/no
- Reason:

## Source Improvements

- Recurring issue:
- Upstream file to update:
- Suggested change:
```
