# Source Ledger: Agent Harness Innovation And Evaluation

Accessed: 2026-07-12

## Scope And Reading Rules

This ledger supports the end-to-end evaluation of `fable-5-skills` and the
companion sprint plan. It prioritizes first-party product documentation and
primary research. Product behavior is treated as time-sensitive. Academic
results are labeled by publication status so a recent preprint is not presented
as settled consensus.

The evidence is used for design principles and evaluation methods, not for
copying another vendor's orchestration stack. The project remains a local,
Markdown-first, human-reviewed harness unless repeated implementation pressure
justifies a deeper runtime Module.

## Official Product And Protocol Sources

| ID | Source | Status at cutoff | Used for |
|----|--------|------------------|----------|
| OAI-1 | OpenAI, [Harness engineering: leveraging Codex in an agent-first world](https://openai.com/index/harness-engineering/) | Official article, 2026-02-11 | Small repository map, mechanically enforced architecture, observability, recurring cleanup |
| OAI-2 | OpenAI, [Unrolling the Codex agent loop](https://openai.com/index/unrolling-the-codex-agent-loop/) | Official article, 2026-01-23 | Compaction, prompt caching, dynamic MCP tools, structured sandbox and approval context |
| OAI-3 | OpenAI, [Unlocking the Codex harness: how we built App Server](https://openai.com/index/unlocking-the-codex-harness/) | Official article, 2026-02-04 | Stable event protocol, long-lived process, approvals, persistence |
| OAI-4 | OpenAI, [Running Codex safely at OpenAI](https://openai.com/index/running-codex-safely/) | Official article, 2026-05-08 | Bounded execution, risk-based approvals, agent-native telemetry |
| OAI-5 | OpenAI, [A shared playbook for trustworthy third-party evaluations](https://openai.com/index/trustworthy-third-party-evaluations-foundations/) | Official article, 2026-05-29 | Harness disclosure, common floors, budgets, validity checks |
| OAI-6 | OpenAI, [Building self-improving tax agents with Codex](https://openai.com/index/building-self-improving-tax-agents-with-codex/) | Official article, 2026-05-27 | Production traces to bounded eval tasks and regression suites |
| OAI-7 | OpenAI, [Evaluate agent workflows](https://developers.openai.com/api/docs/guides/agent-evals) | Live official docs | Trace grading first; repeatable datasets and eval runs after behavior is understood |
| OAI-8 | OpenAI, [Skills](https://developers.openai.com/api/docs/guides/tools-skills) | Live official docs | Skill validation, version pointers, network and prompt-injection risk |
| OAI-9 | OpenAI, [Tool search](https://developers.openai.com/api/docs/guides/tools-tool-search) | Live official docs | Deferred tool loading, namespaces, concise discovery descriptions |
| OAI-10 | OpenAI, [Compaction](https://developers.openai.com/api/docs/guides/compaction) | Live official docs | Canonical continuation window and opaque compaction state |
| OAI-11 | OpenAI, [Multi-agent](https://developers.openai.com/api/docs/guides/responses-multi-agent) | Live official docs, beta feature at cutoff | Bounded parallel work, focused context, shared-state cautions |
| OAI-12 | OpenAI, [Sandbox Agents](https://developers.openai.com/api/docs/guides/agents/sandboxes) | Live official docs, beta at cutoff | Snapshots, resumable sessions, persistent memory layouts |
| OAI-13 | OpenAI, [Prompt caching](https://developers.openai.com/api/docs/guides/prompt-caching) | Live official docs | Exact-prefix cache behavior and cached-token measurement |
| ANT-1 | Anthropic, [Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps) | Official article, 2026-03-24 | Planner-generator-evaluator separation, context reset versus compaction, skeptical evaluation |
| ANT-2 | Anthropic, [Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) | Official article, 2026-01-09 | Task/trial/trace/outcome distinction, mixed graders, capability versus regression suites, `pass^k` |
| ANT-3 | Anthropic, [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) | Official article, 2025-11-26 | Feature ledger, progress file, clean checkpoints, end-to-end testing |
| ANT-4 | Anthropic, [Scaling Managed Agents: Decoupling the brain from the hands](https://www.anthropic.com/engineering/managed-agents) | Official article, 2026-04-08 | Append-only session log, replaceable harness, sandbox separation, crash recovery |
| ANT-5 | Anthropic, [Extend Claude Code](https://code.claude.com/docs/en/features-overview) | Live official docs | Demand-loaded skills and schemas, isolated subagents, lifecycle hooks |
| ANT-6 | Anthropic, [Create custom subagents](https://code.claude.com/docs/en/sub-agents) | Live official docs | Scoped tools, permissions, resumable transcripts, bounded nesting |
| ANT-7 | Anthropic, [Hooks reference](https://code.claude.com/docs/en/hooks) | Live official docs | Pre/post tool, permission, subagent, worktree, compaction, and elicitation hooks |
| ANT-8 | Anthropic, [Sandboxing](https://code.claude.com/docs/en/sandboxing) | Live official docs | Filesystem/network isolation plus permission policy; WSL2 but not native Windows at cutoff |
| CUR-1 | Cursor, [Dynamic context discovery](https://cursor.com/blog/dynamic-context-discovery) | Official article, 2026-01-06 | File-backed searchable context and demand-loaded tools; reported MCP-run token reduction |
| CUR-2 | Cursor, [Best practices for coding with agents](https://cursor.com/blog/agent-best-practices) | Official article, 2026-01-09 | Focused rules, dynamic skills, fresh conversations, reusable correction loop |
| CUR-3 | Cursor, [Plugins, Sandbox Access Controls, and Async Subagents](https://cursor.com/changelog/2-5) | Official changelog, 2026-02-17 | Granular boundaries, asynchronous subagents, cancellation, bounded nesting |
| CUR-4 | Cursor, [Continually improving our agent harness](https://cursor.com/blog/continually-improving-agent-harness) | Official article, 2026-04-30 | Offline and online signals, error taxonomy, token/tool/cache metrics |
| CUR-5 | Cursor, [What we've learned building cloud agents](https://cursor.com/blog/cloud-agent-lessons) | Official article, 2026-06-02 | Separate agent loop, machine state, conversation storage, checkpoint/fork |
| CUR-6 | Cursor, [3.11 changelog](https://cursor.com/changelog) | Official changelog, 2026-07-10 | Conversation, subagent, compaction, and turn-completion hooks |
| OC-1 | OpenCode, [Agent Skills](https://opencode.ai/docs/skills) | Official docs, updated 2026-07-10 | Catalog-first skill discovery and allow/ask/deny visibility |
| OC-2 | OpenCode, [Agents](https://opencode.ai/docs/agents/) | Official docs, updated 2026-07-10 | Per-agent prompts, models, tools, and permissions |
| OC-3 | OpenCode, [Permissions](https://opencode.ai/docs/permissions/) | Official docs, updated 2026-07-10 | Input/path-pattern policy, external-directory guard, duplicate-call guard |
| OC-4 | OpenCode, [Plugins](https://opencode.ai/docs/plugins/) | Official docs, updated 2026-07-10 | Permission, session, compaction, lifecycle, and tool events |
| PYD-1 | Pydantic, [What makes a good harness](https://pydantic.dev/articles/what-makes-a-good-harness) | Official article, 2026-06-26 | Progressive disclosure, steering, scoped execution, observability |
| PYD-2 | Pydantic AI, [Deferred Tools](https://pydantic.dev/docs/ai/tools-toolsets/deferred-tools/) | Live official docs | Typed approval/external-work pause and resume |
| PYD-3 | Pydantic AI, [Durable Execution overview](https://pydantic.dev/docs/ai/integrations/durable_execution/overview/) | Live official docs | Progress preservation across failure and restart |
| PYD-4 | Pydantic Evals, [Span-Based Evaluation](https://pydantic.dev/docs/ai/evals/evaluators/span-based/) | Live official docs | Tool, sequence, failure, latency, safety, and delegation assertions |
| PYD-5 | Pydantic Evals, [Multi-Run Evaluation](https://pydantic.dev/docs/ai/evals/how-to/multi-run/) | Live official docs | Repeated stochastic trials and two-level aggregation |
| PYD-6 | Pydantic Evals, [Case Lifecycle Hooks](https://pydantic.dev/docs/ai/evals/how-to/lifecycle/) | Live official docs | Per-case setup, context preparation, teardown, and failure retention |
| PYD-7 | Pydantic Evals, [Dataset Serialization](https://pydantic.dev/docs/ai/evals/how-to/dataset-serialization/) | Live official docs | Version-controlled data plus generated JSON Schema |
| PYD-8 | Pydantic AI Harness, [Code Mode](https://pydantic.dev/docs/ai/harness/code-mode/) | Live official docs | Sandboxed programmatic tool batching and reduced model round trips |
| PYD-9 | Pydantic AI, [Agents](https://pydantic.dev/docs/ai/core-concepts/agent/) | Live official docs | Request, token, and tool-call usage limits |
| PYD-10 | Pydantic AI, [Output](https://pydantic.dev/docs/ai/core-concepts/output/) | Live official docs | Typed output schemas, validators, and correction retries |
| MCP-1 | MCP, [Tools specification](https://modelcontextprotocol.io/specification/2025-11-25/server/tools) | Latest stable specification at cutoff: 2025-11-25 | Paginated discovery, list-change notifications, input/output schemas |
| MCP-2 | MCP, [Elicitation](https://modelcontextprotocol.io/specification/2025-11-25/client/elicitation) | Stable specification 2025-11-25 | Consent, decline/cancel, structured versus sensitive out-of-band input |
| MCP-3 | MCP, [Authorization](https://modelcontextprotocol.io/specification/2025-11-25/basic/authorization) | Stable specification 2025-11-25 | Resource binding, least privilege, no token passthrough |
| MCP-4 | MCP, [Tasks](https://modelcontextprotocol.io/specification/2025-11-25/basic/utilities/tasks) | Explicitly experimental in stable spec | Durable task-state vocabulary; not a canonical dependency |
| MCP-5 | MCP, [2026-07-28 Specification Release Candidate](https://blog.modelcontextprotocol.io/posts/2026-07-28-release-candidate/) | Pre-release RC labeled `2026-07-28`, locked 2026-05-21; final scheduled after cutoff | Future stateless core and Tasks extension; version-pinning warning |

## Primary Academic Sources

| ID | Source | Publication status | Used for |
|----|--------|--------------------|----------|
| A-1 | Zhu et al., [Establishing Best Practices in Building Rigorous Agentic Benchmarks](https://papers.nips.cc/paper_files/paper/2025/hash/f316275b44ee2de533102913828a8107-Abstract-Datasets_and_Benchmarks_Track.html) | NeurIPS 2025 Datasets and Benchmarks | Benchmark checklist, grader defects, trivial baselines, contamination |
| A-2 | Yang et al., [SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering](https://proceedings.neurips.cc/paper_files/paper/2024/hash/5a7c947568c1b1328ccc5230172e1e7c-Abstract-Conference.html) | NeurIPS 2024 | Interface ablation, concise feedback, constrained actions |
| A-3 | Bahdanau et al., [TapeAgents](https://arxiv.org/abs/2412.08445) | arXiv technical report, 2024-12-11 (v1) | Append-only event tape as audit and resumable state |
| A-4 | Liu et al., [Context as a Tool](https://aclanthology.org/2026.findings-acl.1032/) | Findings of ACL 2026 | Stable semantics, condensed memory, recent high-fidelity evidence, proactive checkpoints |
| A-5 | Yao et al., [tau-bench](https://proceedings.iclr.cc/paper_files/paper/2025/hash/1b126cc38b8638e07bef37e7b2bb72bf-Abstract-Conference.html) | ICLR 2025 | Final-state grading and all-trials reliability with `pass^k` |
| A-6 | Lu et al., [ToolSandbox](https://aclanthology.org/2025.findings-naacl.65/) | Findings of NAACL 2025 | Stateful tools, hidden prerequisites, milestones, insufficient information |
| A-7 | Trivedi et al., [AppWorld](https://aclanthology.org/2024.acl-long.850/) | ACL 2024 Best Resource Paper | Required/allowed/forbidden state deltas and validation solutions |
| A-8 | Lu et al., [AgentRewardBench](https://openreview.net/forum?id=fQcUZMPIvu) | COLM 2025 | Judge calibration, alternate valid paths, self-report unreliability |
| A-9 | Zhang et al., [SWE-bench Goes Live!](https://papers.nips.cc/paper_files/paper/2025/hash/d83c4a745789690f82e86d0ef752ae7c-Abstract-Datasets_and_Benchmarks_Track.html) | NeurIPS 2025 Datasets and Benchmarks | Fresh held-out capability tier and static-case contamination |
| A-10 | Merrill et al., [Terminal-Bench](https://openreview.net/forum?id=a7Qa4CcHak) | ICLR 2026 | Realistic multi-command terminal tasks and comprehensive verification |
| A-11 | Yuan et al., [OSWorld 2.0](https://arxiv.org/abs/2606.29537) | arXiv preprint, 2026-06-28 | Late information, long workflows, hidden-state recovery, milestone diagnosis |
| A-12 | Tan et al., [Recovery-Bench](https://openreview.net/forum?id=8FZRnDgDxq) | NeurIPS 2025 LLM Evaluation Workshop | Recovery from inherited mistakes and polluted state |
| A-13 | Wijk et al., [RE-Bench](https://proceedings.mlr.press/v267/wijk25a.html) | ICML 2025 | Explicit time budgets, retries, and performance-versus-budget curves |
| A-14 | Debenedetti et al., [AgentDojo](https://proceedings.neurips.cc/paper_files/paper/2024/hash/97091a5177d8dc64b1da8bf3e1f6fb54-Abstract-Datasets_and_Benchmarks_Track.html) | NeurIPS 2024 Datasets and Benchmarks | Joint task utility and prompt-injection resistance |
| A-15 | Cemri et al., [Why Do Multi-Agent LLM Systems Fail?](https://proceedings.neurips.cc/paper_files/paper/2025/hash/b1041e52d3be19f0a9bc491657488e4a-Abstract-Datasets_and_Benchmarks_Track.html) | NeurIPS 2025 Datasets and Benchmarks | Handoff, role, information-flow, verification, and termination failures |
| A-16 | Yao et al., [Harness-Bench](https://arxiv.org/abs/2605.27922) | arXiv preprint, 2026-05-27 | Model-harness configuration as evaluated object; traces, budgets, execution alignment |
| A-17 | Gupta, [ReliabilityBench](https://arxiv.org/abs/2601.06112) | arXiv preprint, 2026-01-03 | Repetition, semantic perturbation, and tool/API fault injection |
| A-18 | Xu et al., [RoadmapBench](https://arxiv.org/abs/2605.15846) | arXiv preprint, 2026-05-15 | Multi-target long-horizon tasks and partial completion diagnostics |
| A-19 | Zhong and Zhu, [AI Harness Engineering](https://arxiv.org/abs/2605.13357) | arXiv preprint, 2026-05-13 | Auditable episode packages, failure attribution, intervention recording |
| A-20 | Schmotz et al., [Agent Skills Enable a New Class of Realistic and Trivially Simple Prompt Injections](https://arxiv.org/abs/2510.26328) | arXiv preprint, 2025-10-30 | Skill-file injection and approval carryover risk |

## Extracted Claims

| Claim | Source support | Project implication |
|-------|----------------|---------------------|
| The evaluated object is the model-harness-environment configuration, not the model alone. | OAI-5, ANT-2, A-16, A-19 | Pin model, harness, prompts, tools, permissions, environment, budgets, and grader in every receipt. |
| A compact always-loaded map plus demand-loaded detail is a recurring pattern across the reviewed product sources. | OAI-1, OAI-9, ANT-5, CUR-1, OC-1, PYD-1 | Preserve the current `SKILL.md` spine and trigger-gated references; measure trigger behavior instead of expanding the spine. |
| Durable state must live outside a lossy conversation summary. | OAI-10, ANT-3, ANT-4, CUR-5, PYD-3, A-3, A-4 | Add structured checkpoints, event lineage, and recovery cases; treat compaction and handoff as separate concerns. |
| Final outcomes and execution traces answer different questions. | OAI-7, ANT-2, PYD-4, A-7, A-8, A-19 | Keep outcome grading primary; assert trajectory only for discovery, safety, policy, efficiency, or auditability. |
| Agent reliability requires repeated trials, not one successful run. | ANT-2, PYD-5, A-5, A-17 | Retain three runs as a floor and report success counts, `pass^k`, variability, and uncertainty. |
| The grader is part of the benchmark attack surface. | ANT-2, A-1, A-7, A-8 | Require alternate-good, no-op, bypass, evidence-deletion, fixture-mutation, and reward-hacking tests. |
| Reproducible cases need deterministic setup and controlled state deltas. | PYD-6, A-6, A-7, A-10 | Add environment provenance and required/allowed/forbidden deltas; prove reset determinism and solvability. |
| Costs and budgets materially change results. | OAI-5, OAI-13, CUR-4, PYD-9, A-13, A-16 | Enforce turn/tool/time budgets and record tokens, cache use, retries, latency, and cost when available. |
| Machine-readable outputs need versioned schemas and validation before use. | OAI-7, PYD-7, PYD-10, MCP-1 | Validate run metadata, events, results, and receipt inputs; reject malformed artifacts before aggregation. |
| Long-horizon work exposes recovery and integration failures hidden by small bug-fix tasks. | ANT-1, ANT-3, A-11, A-12, A-18 | Add polluted-state recovery, late-constraint, and multi-target workflow cases. |
| Tool discovery and interface design are capability variables. | OAI-9, CUR-1, OC-1, MCP-1, A-2 | Add high-cardinality discovery and interface-ablation cases with the same model, task, and budget. |
| Approval, permission, and sandbox behavior must be executable contracts. | OAI-4, ANT-7, ANT-8, CUR-3, OC-3, PYD-2, MCP-2, MCP-3 | Add boundary profiles and approve/deny/resume cases; grade attempted forbidden effects, not only final files. |
| Skills and retrieved content are prompt-injection surfaces. | OAI-8, ANT-8, A-14, A-20 | Add untrusted README/log/tool-output cases and verify both useful completion and protected-state integrity. |
| Multi-agent systems add organizational failure modes and should earn their cost. | OAI-11, ANT-1, CUR-3, OC-2, PYD-4, A-15 | Compare against a single-agent baseline; grade delegation fit, scope, handoff, cancellation, merge, and verification. |
| Public static cases become regression assets rather than permanent capability evidence. | ANT-2, A-9 | Maintain tracked public regression cases and a rotating held-out capability tier with delayed promotion. |
| Lifecycle hooks are useful integration points but are vendor-specific. | ANT-7, CUR-6, OC-4, PYD-6 | Define a local event Interface and keep OpenTelemetry/vendor hooks as optional Adapters. |
| Repeated corrections should feed a bounded improvement loop. | OAI-1, OAI-6, CUR-2, CUR-4 | Add recurring drift scans and promote repeated failures into cases, contracts, graders, or references through review. |

## Version And Interpretation Warnings

- MCP stable remained `2025-11-25` at this research cutoff. The pre-release RC
  available since 2026-05-21 was labeled for the scheduled `2026-07-28` final;
  Tasks remained experimental in the stable specification.
- OpenAI, Anthropic, Cursor, OpenCode, and Pydantic documentation changes
  quickly. Any implementation issue derived from live docs should record its
  retrieval date and recheck the named surface before coding.
- Recent 2026 preprints strengthen the direction of this backlog but do not
  override peer-reviewed evidence or repository-local constraints.
- Vendor-reported product metrics are directional evidence, not neutral
  cross-vendor benchmarks.
- None of the reviewed sources requires replacing this repository's folder-based
  workflow with a mandatory orchestration framework. Recurring themes across the
  reviewed sources are explicit contracts, constrained execution, durable state,
  observable events, and verified outcomes.
