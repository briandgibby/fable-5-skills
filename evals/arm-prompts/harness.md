# Arm Prompt: Harness

Use this setup text verbatim, followed by the frozen task prompt. This arm tests the product as shipped: the spine loads first, references load only when the spine's trigger table says so.

```text
You are completing an isolated evaluation run. Work only inside the output folder
named in the task prompt. Do not read other evaluation runs or their outputs.

Before starting, read fable-task-harness/SKILL.md and follow it. Load files under
fable-task-harness/references/ only when a row in the Reference Triggers table
matches the task. Do not preload references whose triggers do not match. In your
verification notes, list which references you loaded and which trigger justified
each one.
```
