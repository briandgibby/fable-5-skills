# Source Ledger: Folder-Based Agent Systems

Accessed: 2026-07-05

## Primary And Near-Primary Sources

| Source | Link | Used for |
|--------|------|----------|
| Van Clief and McDermott, "Interpretable Context Methodology: Folder Structure as Agent Architecture" | https://arxiv.org/abs/2603.16021 | MWP thesis, stage folders, markdown contracts, local scripts, human review, source integrity |
| RinDig, Interpreted-Context-Methdology README | https://github.com/RinDig/Interpreted-Context-Methdology | Practical ICM principles, workspace contribution rules, output as edit surface |
| RinDig, `_core/CONVENTIONS.md` | https://github.com/RinDig/Interpreted-Context-Methdology/blob/main/_core/CONVENTIONS.md | Five-layer routing, stage contracts, one-way dependencies, selective section loading |
| RinDig, Content-Agent-Routing-Promptbase README | https://github.com/RinDig/Content-Agent-Routing-Promptbase | Separation of concerns for context windows, canonical sources, context as working memory |
| Andrej Karpathy, "LLM Wiki" gist | https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f | Raw sources versus generated wiki, compounding markdown knowledge, schema file as maintainer contract |
| Andrej Karpathy, "Software Is Changing (Again)" | https://www.youtube.com/watch?v=LCEmiRjPEtQ | Software 3.0, LLMs as operating systems, partial autonomy, verification loops |
| Transcript mirror for "Software Is Changing (Again)" | https://singjupost.com/andrej-karpathy-software-is-changing-again/ | Searchable reference for Software 3.0 and pragmatic agent workflow claims |
| Anthropic, "Equipping agents for the real world with Agent Skills" | https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills | Folder-packaged skills, dynamic loading, instructions plus resources |

## Extracted Claims

| Claim | Source support | Project implication |
|-------|----------------|---------------------|
| Sequential human-reviewed agent work often does not need a heavy orchestration framework. | Van Clief paper and ICM README | Keep this repo markdown-first, stage-based, and inspectable. |
| Numbered folders can encode workflow stages. | Van Clief paper and ICM conventions | Use `workspaces/*/stages/01-*` contracts. |
| Stage contracts should specify inputs, process, and outputs. | ICM conventions | Make every build/eval step a readable `CONTEXT.md`. |
| Agents should load only the relevant layer and section. | ICM conventions and routing promptbase | Use routing tables with exact sections, not broad "read everything" instructions. |
| Plain markdown files are good agent interfaces because humans can inspect and edit them. | Van Clief paper and ICM README | Preserve markdown as the main project medium. |
| Raw sources and synthesized wiki should be distinct. | Karpathy LLM Wiki | Store source ledgers separately from `knowledge/wiki/` synthesis. |
| The LLM should handle bookkeeping while humans curate sources and steer judgment. | Karpathy LLM Wiki | Let agents maintain cross-links and summaries, but keep source choice human-visible. |
| Prompts and context are a Software 3.0 program. | Karpathy Software 3.0 talk | Treat `AGENTS.md`, `CONTEXT.md`, skill files, and templates as source code. |
| Small chunks and fast verification improve AI-assisted coding. | Karpathy Software 3.0 talk | Keep harness changes narrow and verify each artifact. |
| Current agents should be partial-autonomy products with human review loops. | Karpathy Software 3.0 talk | Build review gates and audits before autonomous execution. |
| Skills can package reusable instructions and resources in folders that agents load when relevant. | Anthropic Agent Skills engineering note | Keep `fable-task-harness/` as a portable folder artifact with a concise `SKILL.md` entrypoint. |
