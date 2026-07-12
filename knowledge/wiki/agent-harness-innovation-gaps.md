# Agent Harness Innovation Tenets And Gap Map

Status: maintained synthesis
Evidence cutoff: 2026-07-12
Source ledger: [2026-07-12-agent-harness-innovation-source-ledger.md](../sources/2026-07-12-agent-harness-innovation-source-ledger.md)

## Thesis

`fable-5-skills` does not need a larger instruction surface. Its current
strength is a compact harness spine, demand-loaded references, explicit folder
contracts, tracked evaluation cases, deterministic graders, and human review.

The missing Depth is in the evaluation lifecycle. The repository can validate
the shape and hashes of one tracked case, but it cannot yet assemble a complete
battery, capture provenance-tagged process evidence, enforce budgets and
boundaries, recover interrupted work, or generate a reconstructable receipt. The next
investment should therefore deepen execution evidence and case coverage while
preserving the Markdown-first control plane.

## Current Strengths To Preserve

1. **Compact progressive disclosure.**
   `fable-task-harness/SKILL.md` is a small always-loaded Interface. Its
   reference trigger table exposes deeper Implementations only for observable
   task shapes. This matches current OpenAI, Anthropic, Cursor, OpenCode, and
   Pydantic guidance.

2. **Folder contracts with clear Locality.**
   Root routing, stage `CONTEXT.md` files, the knowledge split, and installable
   package boundaries keep decisions near the work they govern.

3. **Canonical tracked case Modules.**
   `evals/cases/<case-id>/` owns prompt, fixture, manifest, grader, grader tests,
   and curated receipts. `evals/runs/` remains generated execution evidence.

4. **Blind artifact review plus process review.**
   The A/B/C protocol correctly separates artifact facts from process facts and
   avoids letting missing telemetry automatically falsify a correct artifact.

5. **Source-learning loop.**
   Recurring output failures are routed upstream to the contract, reference,
   template, or grader that can prevent them in later runs.

## Confirmed Repository Gaps

| Gap | Local evidence | Consequence | Priority |
|-----|----------------|-------------|----------|
| Only one tracked case, and it is a trap | `evals/cases/decoy-config-repo/case.json`; Stage 04 requires a build plus a trap | The documented minimum battery cannot be assembled from canonical inputs | P0 |
| Current battery is not reconstructable | Decoy receipt says prompt, fixture, grader, harness, model, and environment fingerprints were not captured automatically | Historical conclusions cannot be independently replayed | P0 |
| Grader conformance is not enforced | `check-eval-cases.py` runs declared tests but does not validate result JSON and exit semantics | A trivial or non-JSON grader can be declared valid | P0 |
| Case template exceeds validator behavior | Required README, alternate-valid tests, receipt semantics, and incomplete case directories are not fully checked | The documented Interface and executable Implementation can drift | P0 |
| Durable claims still cite ignored runs | Several changelog entries cite `evals/runs/` although `evals/README.md` requires tracked receipts | Canonical history depends on local-only evidence | P0 |
| Run metadata is duplicated and manual | Protocol owns fields; the Decoy grader reimplements parsing; workers self-report counts | Aggregation is fragile and process claims are weak | P0 |
| Stage routing points to superseded design | Stage 03 names the master's obsolete architecture section | A future agent can load deleted reference names as current guidance | P0 |
| No current-harness receipt | Existing receipt covers harness 0.2.1; shipped harness is 0.2.4 | The tracked-case model itself has not been exercised end to end | P1 |
| No trace/event contract | `run-meta.md` contains aggregates and prose, not authoritative call/result events | Tool sequence, retries, denials, delegation, and recovery cannot be graded reliably | P1 |
| No deterministic lifecycle contract | Fixtures are hashed, but setup/reset, clock, platform, dependency, and network state are not declared | Repeated trials can differ for environmental reasons | P1 |
| No state-delta model | Cases list allowed changes but do not distinguish required, optional-allowed, and forbidden residual changes | Alternate valid paths and collateral damage are hard to express together | P1 |
| No reliability statistics | Protocol uses three runs and medians but does not report `pass^k`, intervals, or perturbation sensitivity | A single success can conceal inconsistent behavior | P1 |
| No recovery or compaction case | Continuation remains a candidate, not a tracked Module | Durable-state and context-recovery claims are untested | P1 |
| No executable permission profile | Side-effect rules are prose; cases do not declare read/write/network/approval expectations | Attempted unsafe behavior may disappear from final-state grading | P1 |
| No held-out capability tier | All canonical cases are public and static | Improvement on tracked cases can become overfitting rather than frontier evidence | P2 |
| No cross-harness Adapter comparison | Arms vary instructions, not host runtime | Results cannot isolate host-harness differences across Codex, Claude, Cursor, or OpenCode | P2 |

The former research-provenance gap is closed by this maintained synthesis and
its linked source ledger. Freshness review remains active work, but provenance is
no longer missing.

## Pydantic Opportunity Disposition

The earlier Pydantic review is retained as part of the broader evidence base, not
replaced by it:

| Pydantic surface | Project disposition | Backlog owner |
|------------------|---------------------|---------------|
| Typed outputs and dataset schemas (`PYD-7`, `PYD-10`) | Version case, event, result, and receipt contracts; reject malformed grader output before use | HN-002, HN-003, HN-008, HN-011 |
| Span-based evaluation (`PYD-4`) | Preserve outcome-first grading while asserting consequential tool, permission, recovery, and delegation events | HN-009, HN-012, HN-016, HN-023, HN-028 |
| Multi-run evaluation (`PYD-5`) | Aggregate repetitions at run and configuration levels; report reliability, variability, and missing telemetry | HN-013, HN-015 |
| Lifecycle hooks (`PYD-6`) | Declare deterministic setup/reset/teardown and retain failed environments when configured | HN-017 |
| Deferred tools (`PYD-2`) | Test approve, deny, out-of-band input, resume, and duplicate-effect prevention | HN-025 |
| Durable execution (`PYD-3`) | Keep durable state outside lossy conversation summaries and grade recovery | HN-020, HN-021 |
| Usage limits (`PYD-9`) | Enforce and report request, token, tool, and time budgets where the execution boundary exposes them | HN-019 |
| Sandboxed code mode (`PYD-8`) | Treat programmatic batching as an optional interface-ablation profile, not a core dependency | HN-031 |

## Adopted Tenets

### 1. Evaluate The Configuration

The unit of evaluation is:

```text
model + harness version + arm prompt + loaded capabilities + tools +
permissions + environment + budgets + case + grader
```

Receipts must pin that configuration. Model-only claims are out of scope.

### 2. Keep The Spine Small

Do not respond to new research by putting more policy in `SKILL.md`. New rules
belong in the smallest existing reference that owns the behavior, and only after
an evaluation or repeated failure demonstrates the need. Trigger precision and
recall should be measured before adding a new reference.

### 3. Record Observable Events, Not Self-Narration

Workers may write human-readable verification notes, but tool counts, paths,
durations, retries, approvals, and exit states should come from machine-captured
events when the host exposes them. Do not require private chain-of-thought.

The local Interface should be append-only JSONL. OpenTelemetry and vendor hook
formats are Adapters, not the canonical contract.

### 4. Separate Durable State From Conversation State

Source-tree state, environment state, event history, and continuation summary are
different artifacts. A compaction summary is not an authoritative progress
ledger. Recovery cases should test whether a fresh worker can reconcile durable
state without repeating side effects or trusting stale narration.

### 5. Grade Outcomes First, Paths When Consequential

Final state is the primary source of truth. Multiple valid trajectories should
pass. Process assertions are appropriate only when the path affects:

- safety or permission compliance;
- mandatory discovery or clarification;
- policy adherence;
- preservation of audit evidence;
- retry/loop behavior;
- delegation or handoff correctness;
- explicit efficiency budgets.

### 6. Treat The Grader As Production Code

Every nontrivial grader needs:

- a validation solution proving the case is solvable;
- at least one alternate-good outcome;
- known-bad mutations;
- no-op and empty-output baselines;
- evidence-deletion and bypass attempts;
- fixture and grader tampering checks;
- tests for unintended residual changes.

An agent's claim that it succeeded never substitutes for environment evidence.

### 7. Measure Reliability, Not Anecdotes

Three runs per arm remain the floor. Reports should include successes/attempts,
per-case and cross-case aggregates, an all-runs-success metric such as `pass^3`,
and uncertainty appropriate to the sample. Capability claims should also be
tested against semantically equivalent prompt or state perturbations.

### 8. Make Boundaries Executable

Cases should declare allowed read roots, write roots, network policy, protected
paths, external systems, and expected allow/ask/deny outcomes. Grade attempted
violations from events as well as residual filesystem changes.

### 9. Keep Regression And Capability Evidence Separate

Tracked public cases are regression assets. A rotating held-out tier provides
capability evidence. Retired held-out cases may be promoted into `evals/cases/`
with source date, environment digest, and a receipt explaining retirement.

### 10. Multi-Agent Must Earn Its Complexity

Delegation is useful only when independent bounded work or specialist context
outweighs its token, permission, and reconciliation cost. Multi-agent cases must
compare against a single-agent baseline and grade scope, information transfer,
acknowledgment, cancellation, merge quality, and final verification.

### 11. Improve Through Reviewed Promotion

Production-like traces, user corrections, failed cases, and review findings may
propose upstream changes. Promotion into a contract, reference, template,
grader, or regression case remains human-reviewed. No agent should silently
self-modify the canonical harness from one trajectory.

## Architecture Deepening Decisions

### Evaluation Execution Module: Justified

Create one narrow Interface for preparing a run, assembling prompts, copying the
fixture, recording fingerprints, ingesting events, invoking the grader, and
building receipt inputs.

Deletion test: without this Module, the same prompt assembly, hashing, fixture
copying, metadata, and receipt logic appears in every arm and case. The Module
therefore creates real Depth, Leverage, and Locality.

### Run Evidence Module: Justified

Create one parser/validator Interface for machine-readable run metadata and
events. The Implementation owns types, timestamps, lineage, counts, token syntax,
arm identity, and redaction.

Deletion test: these rules are already duplicated across the protocol, worker
notes, case grader, and parent reviews.

### Harness Adapter Seam: Real, But Later

The three arm prompts are already multiple Adapters over the same case. Host
runtime portability is not yet a real Seam because there are no two implemented
host Adapters. Implement the first host directly, implement a second, then
extract only their proven common Interface.

### Shared Grader Module: Not Yet

There is one tracked grader Adapter today. Extracting a shared grader framework
now would be speculative. Migrate Undocumented Local Tool and add a materially
different build case first; use those Implementations to reveal the true common
contract.

### Mandatory Orchestrator: Rejected

Temporal, DBOS, Prefect, Restate, and vendor cloud runtimes demonstrate useful
durability patterns, but this repository does not need one as a core dependency.
The local state and event contracts should be serializable enough for an Adapter
to map into a durable runtime later.

### Mandatory OpenTelemetry: Rejected

OpenTelemetry is a valuable Adapter and common vocabulary. Requiring it in the
core would add deployment and dependency cost to a local Markdown-first project.
Canonical JSONL events should be convertible to and from OTel spans where the
host supports them.

## Evaluation Portfolio

### Regression Cases To Track

1. `decoy-config-repo` — live source of truth versus stale decoys.
2. `undocumented-local-tool` — interface discovery, exact command, audit-log preservation.
3. A build case — full artifact construction plus objective behavior verification.
4. `polluted-repo-recovery` — inherited failure, stale notes, and recovery cost.
5. `stateful-tool-insufficient-info` — hidden prerequisite and required clarification.
6. Alternate-path/collateral-damage variants — applied across the build case and
   the state-delta migration rather than maintained as a duplicate standalone case.
7. `untrusted-environment-instruction` — useful completion under indirect injection.
8. `deferred-approval-resume` — approve/deny, stable request IDs, no duplicate effects.
9. `dynamic-tool-catalog` — high-cardinality discovery, list change, malformed result.
10. `late-constraint-long-workflow` — checkpoint, changed requirement, re-plan, verify.
11. `stale-multi-agent-handoff` — information transfer and live-state reconciliation.
12. `interface-ablation` — raw shell versus constrained repo operations.
13. `reference-trigger-routing` — trigger precision, missed risks, unnecessary loads, and full-load cost.

### Cross-Cutting Assertions

- deterministic setup/reset and frozen time where relevant;
- required, optional-allowed, and forbidden state deltas;
- complete residual diff;
- immutable prompt, fixture, grader, and ground truth during candidate execution;
- provenance-tagged tool/action events with secret redaction;
- explicit budgets and a safe `budget_exceeded` state;
- artifact blinding before process evidence is opened;
- capability-versus-regression classification and freshness metadata.

## Deferred Until Evidence Exists

- A generalized host Adapter Interface before two host Implementations exist.
- LLM judges as release gates before human calibration and disagreement analysis.
- Autonomous generation and acceptance of new regression cases.
- Mandatory vendor hooks, MCP Tasks, or cloud orchestration.
- A large benchmark suite before the runner, grader conformance, and three diverse
  tracked cases are trustworthy.

## Review Trigger

Revisit these tenets when any of the following occurs:

- two host Adapters expose repeated integration logic;
- five or more tracked cases repeat grader or lifecycle code;
- a new stable MCP specification supersedes `2025-11-25`;
- three consecutive batteries show the same harness failure;
- held-out capability results diverge materially from public regression results;
- the core JSONL event contract cannot express a required safety or recovery
  assertion without vendor-specific fields.
