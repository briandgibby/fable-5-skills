# Fable 5 Skills

Fable 5 Skills is a small, markdown-first project for turning useful agent-workflow ideas into installable skills and human-reviewed workspace patterns.

The main artifact is `fable-task-harness/`, a compact skill that helps an agent route nontrivial work before acting: check context, recover missing information, choose the right source of truth, load relevant skills or references, respect tool contracts, and verify the result.

The surrounding repo is the factory for that artifact. It keeps research notes, stage contracts, templates, and evaluation plans close enough for review without requiring a heavy orchestration framework.

## Credits And Influences

This project is derived from several lines of work and should be read as synthesis, not invention from scratch:

- Jake Van Clief and collaborators, especially the [Interpretable Context Methodology / Markdown Workflow Processing](https://arxiv.org/abs/2603.16021) idea that folders, routing files, and stage contracts can be agent architecture.
- Andrej Karpathy's [Software 3.0](https://www.youtube.com/watch?v=LCEmiRjPEtQ) and [LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) framing: prompts, context, schemas, examples, and markdown knowledge bases are part of the software.
- Anthropic's Claude team for [Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills): the practical pattern of packaging instructions, scripts, and resources as discoverable folders that agents load when relevant.
- The Fable-derived harness idea that context sufficiency, skill preflight, tool literacy, and verification should be explicit operating habits rather than vibes.

Source notes live in `knowledge/sources/`, and the current project synthesis lives in `knowledge/wiki/`.

## Repository Map

```text
AGENTS.md                         Root map and routing hints
CONTEXT.md                        Task routing table
icm/                              Repository adapter and task records for central ICM
_core/                            Canonical conventions and templates
docs/                             Source design notes from stage analysis
knowledge/sources/                Source ledgers for external research
knowledge/wiki/                   Maintained synthesis and project tenets
workspaces/fable-task-harness-build/
                                  Stage contracts for building the harness
evals/cases/                      Tracked prompts, fixtures, graders, and result receipts
evals/runs/                       Generated local evaluation artifacts
evals/                            Shared protocol, arm prompts, rubric, and case catalog
fable-task-harness/               Installable skill package artifact (versioned; see its CHANGELOG.md)
scripts/                          Deterministic repo checks
```

## Install

The install procedure is folder-based. Copy the skill package folder, not the whole repo, into your agent's skills directory.

Codex:

```powershell
$source = (Resolve-Path ".\fable-task-harness").Path
$dest = "$env:USERPROFILE\.codex\skills\fable-task-harness"

if (Test-Path -LiteralPath $dest) {
  throw "Destination already exists: $dest"
}

Copy-Item -Recurse -LiteralPath $source -Destination $dest
```

Claude Code: use the same command with `$dest = "$env:USERPROFILE\.claude\skills\fable-task-harness"` (or `.claude\skills\` inside a single project).

Then restart or reload the agent so the skill registry can pick it up. The skill entrypoint is `fable-task-harness/SKILL.md`; `fable-task-harness/agents/openai.yaml` provides the compact OpenAI-facing loader hint.

Before shipping changes to the package, run the deterministic checks:

```powershell
python scripts\check-skill-package.py
```

On macOS or Linux, use `python3 scripts/check-skill-package.py`.

They validate frontmatter YAML, required fields (`name`, `description`, `version`), relative link integrity, and line-count guidance.

Before using or changing tracked evaluation cases, validate their manifests,
fixtures, graders, and grader tests:

```powershell
python scripts\check-eval-cases.py
```

On macOS or Linux, use `python3 scripts/check-eval-cases.py`.

## ICM Workflow

Nontrivial repository changes use the separately installed central ICM kernel. This repository contains only its repository-specific adapter; central contracts, policies, skills, templates, and validators remain in ICM-agentic-system.

Changes to the skill package, project architecture, scripts, evaluation protocols, tracked cases, or graders follow this lifecycle:

1. Explicitly invoke $plan-task with one change request.
2. Review the generated icm/tasks/<task-id>/ request, specification, plan, and context manifest.
3. In a later explicit $plan-task invocation, approve that unchanged task package.
4. Explicitly invoke $build-task with the approved task directory.
5. Inspect the resulting local commits, verification evidence, and independent review before separately deciding whether to integrate them.

Small documentation and routing corrections that do not alter behavior or contracts continue through the lightweight development workflow below. If the central kernel is unavailable or task approval is stale, stop rather than creating a repository-local fallback.

## Development Workflow

Use the routing files as control surfaces:

1. Start at `AGENTS.md` for the root map.
2. Use `CONTEXT.md` to choose the relevant workspace, stage, or artifact.
3. Follow the relevant stage `CONTEXT.md` when changing the harness, architecture, research layer, or evaluation case.
4. Keep durable rules in `_core/`, `knowledge/wiki/`, `fable-task-harness/references/`, or tracked `evals/cases/` modules.
5. Keep generated outputs in `evals/runs/` or stage `output/` folders.

Generated run outputs are ignored by default. Commit case manifests, prompts, fixtures, graders, curated receipts, references, templates, rubrics, and source-level fixes.

## License

MIT. See `LICENSE`.
