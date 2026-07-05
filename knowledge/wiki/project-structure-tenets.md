# Project Structure Tenets

This synthesis applies the folder-based agent research to this repo.

## What Already Existed

The original stage docs already contained several strong Fable-derived tenets:

- Context sufficiency before action.
- Context recovery from workspace, docs, memory, and tools.
- Skill preflight before specialized work.
- Output surface routing to prevent fake deliverables.
- Tool cards, parameter hygiene, and side-effect boundaries.
- Runtime state preservation and structured parsing.
- Source-backed research as a situational module.

## What The Research Adds

### 1. Make The Filesystem The Control Surface

Jake Van Clief's ICM/MWP method argues that sequential, human-reviewed workflows can often replace orchestration code with folders, markdown stage contracts, and local scripts. For this repo, that means the project should not only contain skill files. It should contain a small workspace protocol that tells agents where to go, what to load, what to produce, and how to verify.

Project adoption:

- `AGENTS.md` is the root map.
- `CONTEXT.md` is the task router.
- `workspaces/fable-task-harness-build/` owns the build workflow.
- `fable-task-harness/` remains the installable artifact.

### 2. Route By Layer And Section

The highest-leverage ICM pattern is selective loading. Agents should not read every doc or reference file for every task. Routing files should point to exact files and sections, then stop.

Project adoption:

- Keep `CONTEXT.md` files short.
- Put actual knowledge in `docs/`, `knowledge/wiki/`, and skill references.
- Use Inputs tables to say which file or section matters.

### 3. Separate Factory From Product

Stable references are the factory. Per-run outputs are the product. Old outputs should not silently become standards because early outputs are often lower quality.

Project adoption:

- Store durable rules in `_core/CONVENTIONS.md` and skill references.
- Store external source metadata in `knowledge/sources/`.
- Store synthesized, updateable knowledge in `knowledge/wiki/`.
- Keep stage `output/` folders for per-run artifacts, not canonical rules.

### 4. Treat Context As Code

Karpathy's Software 3.0 framing makes prompts, examples, tool definitions, and context windows part of the program. This fits the Fable harness directly: the important software is not only scripts, it is the instruction architecture that shapes agent behavior.

Project adoption:

- Review `AGENTS.md`, `CONTEXT.md`, `SKILL.md`, references, and templates like source code.
- Prefer explicit schemas, examples, and checklists over vague prose.
- Use local scripts only where deterministic mechanics beat model judgment.

### 5. Build Partial Autonomy First

Karpathy's pragmatic stance is not "let the agent do everything." It is small chunks, concrete prompts, fast generation-verification loops, and human review where judgment matters.

Project adoption:

- Add audits to creative or architectural stages.
- Keep A/B/C tests blind and rubric-driven.
- Make every output inspectable before it informs the next stage.
- Use checkpoints before long autonomous runs.

### 6. Improve The Source, Not Only The Output

ICM's source-integrity principle is the missing long-term learning loop. If the same output correction happens repeatedly, the fix belongs upstream in a stage contract, reference, template, or skill instruction.

Project adoption:

- Track repeated corrections during evaluation.
- Convert recurring output edits into source-level updates.
- Keep research findings in the knowledge layer so they survive beyond one conversation.

## Recommended Repo Shape

```text
AGENTS.md
CONTEXT.md
_core/
  CONVENTIONS.md
docs/
  fable-pseudo-harness-master.md
  stages/
knowledge/
  sources/
  wiki/
workspaces/
  fable-task-harness-build/
    CONTEXT.md
    stages/
      01-research-and-tenets/
      02-architecture/
      03-skill-package/
      04-evaluation/
fable-task-harness/
  SKILL.md
  references/
  templates/
  agents/
```

## Deferred

- A full workspace builder.
- Automated `setup` and `status` commands.
- Deep research as a separate skill.
- Trust-boundary filtering as a separate skill.
- Scripts for validating placeholders, line counts, and stage status.

## Sources

- Van Clief and McDermott, "Interpretable Context Methodology: Folder Structure as Agent Architecture": https://arxiv.org/abs/2603.16021
- RinDig ICM repository: https://github.com/RinDig/Interpreted-Context-Methdology
- RinDig routing promptbase: https://github.com/RinDig/Content-Agent-Routing-Promptbase
- Karpathy LLM Wiki: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
- Karpathy, "Software Is Changing (Again)": https://www.youtube.com/watch?v=LCEmiRjPEtQ
