# Harness Evaluation Rubric

Score each dimension from 1 to 5.

| Score | Meaning |
|-------|---------|
| 1 | Fails or misses the point |
| 2 | Partially works but has major gaps |
| 3 | Works with noticeable rough edges |
| 4 | Solid and usable |
| 5 | Excellent for the task size |

## Dimensions

| Dimension | What to look for |
|-----------|------------------|
| Correctness | Required behavior works |
| Completeness | All requested outputs are present |
| Simplicity | Solution avoids unnecessary machinery |
| Maintainability | Files are readable, organized, and easy to change |
| UX or reader polish | User-facing result feels coherent and usable |
| Appropriate tool use | Tools match the task and are not overused |
| Context recovery | Agent found and used the right source of truth |
| Output routing | Agent created or edited the right artifact |
| Verification | Agent ran or described meaningful checks |
| Speed and cost | Agent avoided avoidable work and context bloat |
| User intervention | Agent needed little clarification for recoverable context |

## Review Notes Template

```md
# Review: {{RUN_NAME}}

## Scores

| Dimension | Control | Always-on | Situational | Notes |
|-----------|---------|-----------|-------------|-------|
| Correctness | | | | |
| Completeness | | | | |
| Simplicity | | | | |
| Maintainability | | | | |
| UX or reader polish | | | | |
| Appropriate tool use | | | | |
| Context recovery | | | | |
| Output routing | | | | |
| Verification | | | | |
| Speed and cost | | | | |
| User intervention | | | | |

## Winner

- Winner:
- Reason:

## Source Improvements

- Recurring issue:
- Upstream file to update:
```
