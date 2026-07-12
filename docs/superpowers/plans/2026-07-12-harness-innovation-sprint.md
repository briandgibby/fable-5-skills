# Harness Innovation Multi-Sprint Implementation Plan

> **For agentic workers:** Use `superpowers:test-driven-development` for every
> behavior change, preserve the user's existing dirty worktree, and request an
> independent review before declaring a ticket complete.

**Goal:** Close current evidence and contract defects, then deepen the evaluation
system with replayable execution evidence, reliability and security cases,
long-horizon coverage, and proven host portability.

**Architecture:** Keep tracked case Modules and the Markdown control plane.
Introduce an Evaluation Execution Module and Run Evidence Module only after a
second case grader exists. Use local JSON/JSONL as the canonical Interface;
OpenTelemetry and vendor hooks remain optional Adapters. Extract a host Adapter
Interface only after two host Implementations work.

**Tech Stack:** Python, JSON, JSONL, Markdown, `unittest`, Git; standard library
for the evaluation runtime. The validation toolchain pins
[`PyYAML==6.0.3`](https://pypi.org/project/PyYAML/6.0.3/) and
[`jsonschema==4.26.0`](https://pypi.org/project/jsonschema/4.26.0/).

**Evidence:**

- [Architecture design](../specs/2026-07-12-harness-innovation-evaluation-design.md)
- [Maintained gap synthesis](../../../knowledge/wiki/agent-harness-innovation-gaps.md)
- [Primary-source ledger](../../../knowledge/sources/2026-07-12-agent-harness-innovation-source-ledger.md)

## Planning Assumptions

- Sprint length: two weeks.
- Capacity was not specified. Effort labels are relative (`S`, `M`, `L`) and
  should be converted to team points only after an owner is assigned.
- Sprint 1 is a proposed two-week scope until owners and points establish
  capacity. HN-001 through HN-005 are the committed candidate slice; HN-006 and
  HN-007 are stretch/carryover gates that must finish before Sprint 2 execution
  work starts.
- Later sprints are sequenced backlog, not calendar promises. HN-016 through
  HN-040 are epics that require owner, capacity, and exact fixture/file refinement
  before being pulled.
- GitHub issue publication is deferred until the local backlog is reviewed.
- No ticket authorizes external credentials, production mutation, commit, push,
  or pull-request creation.

## Global Constraints

- Preserve unrelated user changes in the dirty worktree.
- Keep `evals/cases/` canonical and `evals/runs/` generated/ignored.
- Keep case-specific ground truth in one case Module.
- Do not add a shared grader framework before two materially different tracked
  graders expose repeated behavior.
- Do not add a host Adapter abstraction before two host Implementations work.
- Outcome grading is primary. Process assertions require a safety, policy,
  discovery, audit, delegation, recovery, or budget reason.
- Do not record or require private chain-of-thought.
- Treat candidate-accessible content as untrusted; keep graders, fixtures, and
  ground truth immutable during candidate execution.
- Use tests for every new validation rule and every newly rejected state.
- Keep Windows commands working and include `python3` variants in user-facing
  docs where macOS/Linux users need them.
- Every durable evaluation claim must point to a tracked receipt and disclose
  missing telemetry.

## Sprint Map

| Sprint | Outcome | Tickets |
|--------|---------|---------|
| 1. Trust the baseline | Canonical docs and reproducible validators are trustworthy; two additional tracked cases are stretch/carryover | HN-001 through HN-005 committed candidate; HN-006 and HN-007 stretch |
| 2. Reconstruct every run | Versioned evidence schemas, deterministic preparation/grading, aggregation, and current receipts | HN-008 through HN-015 |
| 3. Prove reliability and recovery | State deltas, grader attacks, budgets, deterministic lifecycle, recovery, compaction, fault injection | HN-016 through HN-022 |
| 4. Enforce trust boundaries | Executable permissions, injection resistance, approval resume, dynamic tools, clarification, redaction | HN-023 through HN-028 |
| 5. Test long-horizon and portability | Late constraints, multi-agent handoffs, interface ablation, two host Adapters, platform matrix | HN-029 through HN-034 |
| 6. Maintain capability evidence | Held-out cases, calibrated judges, feedback promotion, drift scans, source freshness, trigger quality | HN-035 through HN-040 |

## Dependency Spine

```text
HN-002 -> HN-003 -> HN-006/HN-007
HN-004 -> HN-005
HN-005 + HN-006 + HN-007 -> HN-008 -> HN-009 -> HN-010 -> HN-011/HN-012
HN-011 + HN-012 -> HN-013 -> HN-014 -> HN-015
HN-008 + HN-011 -> HN-016
HN-008 + HN-010 + HN-011 -> HN-017
HN-016 + HN-017 -> HN-018/HN-020
HN-008 + HN-011 + HN-012 -> HN-019
HN-012 + HN-020 -> HN-021
HN-017 + HN-019 -> HN-022
HN-008 + HN-012 -> HN-023
HN-008 + HN-012 + HN-014 -> HN-028
HN-023 + HN-028 -> HN-024
HN-012 + HN-017 + HN-023 -> HN-025
HN-012 + HN-023 -> HN-026
HN-016 + HN-023 -> HN-027
HN-020 + HN-021 + HN-023 -> HN-029
HN-012 + HN-020 + HN-023 -> HN-030
HN-012/HN-015 -> HN-032 -> HN-031
HN-032 -> HN-033 -> HN-034
HN-015 + HN-018 -> HN-035/HN-036/HN-037
HN-004 + HN-015 + HN-037 -> HN-038
HN-012/HN-015 -> HN-040
```

---

## Sprint 1: Trust The Baseline

### HN-001 — Reconcile Routing, History, And Generated Analysis State

**Priority / effort:** P0 / S
**Dependencies:** none

**Files:**

- Modify: `workspaces/fable-task-harness-build/stages/03-skill-package/CONTEXT.md`
- Modify: `docs/fable-pseudo-harness-master.md`
- Modify: `fable-task-harness/CHANGELOG.md`
- Modify: `knowledge/wiki/project-structure-tenets.md`
- Modify: `.gitignore`

**Work:**

1. Point Stage 03 to the shipped package, current architecture decisions, and
   changelog rather than the superseded proposed reference list.
2. Mark obsolete master-plan architecture sections as historical without
   deleting useful decision context.
3. Replace changelog dependencies on ignored raw runs with tracked receipts, or
   explicitly label claims whose evidence has not yet been promoted.
4. Refresh the stale wiki `Deferred` list.
5. Treat `.ua/` as generated local analysis and ignore it unless a separate
   reviewed decision chooses to track knowledge graphs.

**Acceptance:**

- Stage 03 no longer references the obsolete `Proposed Skill Architecture` or
  `Core Harness Spine` master-plan sections and instead routes to the shipped
  `SKILL.md`, changelog, and current architecture design.
- `rg -n "evals/runs/" fable-task-harness/CHANGELOG.md` returns only claims that
  also name a tracked receipt or an explicit evidence limitation.
- `git check-ignore .ua/meta.json` succeeds after the ignore decision.
- All edited relative links resolve.

### HN-002 — Reject Incomplete Or Ill-Typed Case Modules

**Priority / effort:** P0 / M
**Dependencies:** none

**Files:**

- Modify: `scripts/check-eval-cases.py`
- Modify: `scripts/tests/test_check_eval_cases.py`
- Modify: `evals/cases/README.md`
- Modify: `_core/templates/evaluation-case-template.md`

**Work:**

1. Write failing tests only for current gaps: a direct case directory without
   `case.json`, missing `README.md`, non-string or empty title/goal values, and an
   ill-typed or unsupported grader result-schema declaration.
2. Make discovery inspect direct case directories, not only `*/case.json`.
3. Validate the documented required-file contract and field types.
4. Keep the existing version/kind/schema checks as characterization regressions;
   do not claim they are new red tests.
5. Keep errors deterministic and case-qualified.

**Acceptance:**

- The new tests fail before implementation and pass after it.
- Existing 24 validator tests remain green.
- An incomplete case directory produces a nonzero exit and concise error.

### HN-003 — Enforce Grader Interface Conformance

**Priority / effort:** P0 / M
**Dependencies:** HN-002

**Files:**

- Modify: `scripts/check-eval-cases.py`
- Modify: `scripts/tests/test_check_eval_cases.py`
- Modify: `evals/protocol.md`
- Modify: `_core/templates/evaluation-case-template.md`
- Modify: `evals/cases/decoy-config-repo/case.json`
- Create: `evals/cases/decoy-config-repo/grader-fixtures/known-good/**`
- Create: `evals/cases/decoy-config-repo/grader-fixtures/known-bad/**`

**Interface:** A declared grader must emit one JSON result matching its declared
schema version and use documented exit semantics. `grader.conformance_cases`
declares contained run-fixture paths plus expected pass/fail and exit states.

**Work:**

1. Add and document the minimal contained `grader.conformance_cases` manifest
   contract, then migrate Decoy Config with one known-good and one known-bad run
   fixture.
2. At author-validation time, invoke the declared grader against copies of those
   fixtures and verify JSON shape, schema version, expected result, exit status,
   and non-mutation.
3. Add checker fixtures for non-JSON output, wrong schema version, missing
   required fields, contradictory `passed`/exit status, unsafe fixture paths,
   undeclared tests, and mutation during grading.
4. Require substantive known-good and known-bad grader tests; reject the current
   trivial always-true validator fixture.
5. Keep case-specific grading logic inside the case. Runtime classification and
   isolation remain HN-011; adversarial semantic mutants remain HN-018.

**Acceptance:**

- A grader that prints nothing or invalid JSON cannot validate.
- Exit zero occurs only for a structurally valid passing result.
- Grader conformance tests cover success, objective failure, invalid evidence,
  and grader runtime failure.

### HN-004 — Deepen Skill-Package Validation And Add Tests

**Priority / effort:** P0 / M
**Dependencies:** none

**Files:**

- Modify: `scripts/check-skill-package.py`
- Create: `scripts/tests/test_check_skill_package.py`
- Inspect/modify if required: `fable-task-harness/agents/openai.yaml`
- Modify if required: `fable-task-harness/CHANGELOG.md`

**Work:**

1. Add red tests for malformed frontmatter, version mismatch with changelog,
   broken loader metadata, missing trigger targets, duplicate reference entries,
   and missing required worked examples.
2. Validate `agents/openai.yaml` and the exact reference/template inventory.
3. Preserve the current CLI Interface.
4. Keep warnings non-fatal only where the documented contract says advisory.

**Acceptance:**

- The new checker suite passes in isolation and under full discovery.
- Frontmatter, changelog, loader metadata, and package inventory agree.
- No wrapper script is added merely to invoke existing checkers.

### HN-005 — Make The Validation Toolchain Reproducible

**Priority / effort:** P0 / S
**Dependencies:** HN-004

**Files:**

- Create: `requirements-dev.txt`
- Create: `.github/workflows/validate.yml`
- Modify: `README.md`

**Work:**

1. Declare the current validation dependency as
   [`PyYAML==6.0.3`](https://pypi.org/project/PyYAML/6.0.3/) in
   `requirements-dev.txt`. Replacing YAML parsing with a narrower standard-
   library contract would be a separate reviewed change, not part of this ticket.
2. Pin `jsonschema==4.26.0` for Draft 2020-12 contract validation.
3. Add Windows and Linux CI jobs for validator tests, the case checker (the
   canonical command that runs every manifest-declared grader suite), package
   checks, and `git diff --check` equivalent whitespace validation. Do not add a
   top-level `unittest` discovery command under hyphenated case directories.
4. Disable Python bytecode during checks.

**Acceptance:**

- A fresh environment can install/execute the documented validation commands.
- Windows and Linux CI use the same canonical commands where platform syntax
  permits.
- Dependency choice and rationale are documented once.

### HN-006 — Migrate Undocumented Local Tool Into A Tracked Case

**Priority / effort:** P0 / L
**Dependencies:** HN-002, HN-003

**Files:**

- Create: `evals/cases/undocumented-local-tool/case.json`
- Create: `evals/cases/undocumented-local-tool/prompt.md`
- Create: `evals/cases/undocumented-local-tool/README.md`
- Create: `evals/cases/undocumented-local-tool/fixture/**`
- Create: `evals/cases/undocumented-local-tool/grader.py`
- Create: `evals/cases/undocumented-local-tool/test_grader.py`
- Create: `evals/cases/undocumented-local-tool/grader-fixtures/known-good/**`
- Create: `evals/cases/undocumented-local-tool/grader-fixtures/known-bad/**`
- Create: `evals/cases/undocumented-local-tool/receipts/harness-v0.2.2.md`
- Create: `evals/cases/undocumented-local-tool/receipts/harness-v0.2.3.md`
- Modify: `evals/candidate-simple-projects.md`
- Modify: `fable-task-harness/CHANGELOG.md`
- Delete after promotion: `evals/undocumented-local-tool-test-plan.md`

**Work:**

1. Freeze the existing task and pristine tool/data fixture, including declared
   known-good and known-bad conformance runs required by HN-003.
2. Encode exact output plus required audit-log preservation without requiring one
   golden trajectory.
3. Add alternate-good, missing-log, tool-bypass, hand-written-output,
   tool-mutation, data-mutation, extra-output, and evidence-deletion tests.
4. Promote historical conclusions into honest receipts, disclosing unavailable
   telemetry and reconstruction limits.

**Acceptance:**

- Case and grader validation pass.
- A matching report without a retained successful tool record fails the
  consequential evidence assertion.
- An alternate valid discovery path passes.
- No durable fact remains canonical only in the deleted standalone plan.

### HN-007 — Add The Tracked CSV Habit Summary Build Case

**Priority / effort:** P0 / L
**Dependencies:** HN-002, HN-003

**Files:**

- Create: `evals/cases/csv-habit-summary/case.json`
- Create: `evals/cases/csv-habit-summary/prompt.md`
- Create: `evals/cases/csv-habit-summary/README.md`
- Create: `evals/cases/csv-habit-summary/fixture/habits.csv`
- Create: `evals/cases/csv-habit-summary/grader.py`
- Create: `evals/cases/csv-habit-summary/test_grader.py`
- Create: `evals/cases/csv-habit-summary/grader-fixtures/known-good-script/**`
- Create: `evals/cases/csv-habit-summary/grader-fixtures/known-good-package/**`
- Create: `evals/cases/csv-habit-summary/grader-fixtures/known-bad/**`
- Modify: `evals/candidate-simple-projects.md`
- Modify: `evals/cases/README.md`

**Work:**

1. Freeze the existing CSV Habit Summary CLI candidate: standard-library Python
   reads the supplied habit-log CSV and writes the requested deterministic
   Markdown summary through the declared CLI.
2. Freeze prompt and fixture and declare two structurally different correct
   conformance runs: a single-script Implementation and a small-package
   Implementation.
3. Grade requested CLI behavior, report facts, residual changes, scope discipline, and highest
   reachable verification rung.
4. Add alternate-good, overbuilt, incomplete, brittle-hardcoded, wrong-output,
   and collateral-change tests.

**Acceptance:**

- The repository contains at least one build and two trap case Modules.
- A build-plus-trap battery can be assembled from tracked inputs only.
- The grader accepts two structurally different correct solutions.

### Sprint 1 Capacity And Exit Gates

Before commitment, assign owners and points. If capacity does not cover
HN-001 through HN-005, reduce scope rather than treating the stretch cases as
silently committed.

Committed-candidate gate:

Run:

- `python -m unittest discover -s scripts/tests -p "test_*.py" -v`
- `python scripts/check-eval-cases.py`
- `python scripts/check-skill-package.py`
- `git diff --check`

Done for the committed candidate means all commands exit zero and no current
router or changelog claim silently depends on obsolete or ignored evidence.

For HN-001 through HN-005, the case count remains the currently tracked baseline;
the three-case clause applies only after stretch/carryover HN-006 and HN-007 are
complete. Sprint 2 execution work may not start until that stretch gate passes.

---

## Sprint 2: Reconstruct Every Run

### HN-008 — Implement Versioned Artifact Schemas And Structural Validation

**Priority / effort:** P0 / L
**Dependencies:** HN-005, HN-006, HN-007

**Files:**

- Create: `evals/schemas/case.schema.json`
- Create: `evals/schemas/run-meta.schema.json`
- Create: `evals/schemas/trace-event.schema.json`
- Create: `evals/schemas/run-result.schema.json`
- Create: `evals/schemas/receipt.schema.json`
- Create: `scripts/evals/__init__.py`
- Create: `scripts/evals/evidence.py`
- Create: `scripts/tests/test_eval_evidence.py`
- Modify: `scripts/check-eval-cases.py`
- Modify: `_core/templates/evaluation-case-template.md`

**Work:** Write valid and invalid fixtures first, then define Draft 2020-12
schemas for versions, identity, fingerprints, timing, usage, lifecycle, lineage,
status taxonomy, nullable score applicability, evidence provenance/admissibility,
limitations, and redaction markers. Implement artifact-level validation with the
pinned `jsonschema` package and an explicit format checker; make
`case.schema.json` the named schema owner while retaining focused semantic checks
in `check-eval-cases.py`.

**Acceptance:** Every artifact has a versioned schema and negative tests for
missing identity, naive timestamps, invalid counts, unknown required versions,
wrong field types, and contradictory status. Schema files validate against their
meta-schema, and the current case validates against `case.schema.json`.

### HN-009 — Add Deterministic Evidence Serialization And Sequence Validation

**Priority / effort:** P0 / M
**Dependencies:** HN-008

**Files:**

- Modify: `scripts/evals/evidence.py`
- Create: `scripts/evals/event_sequence.py`
- Modify: `scripts/tests/test_eval_evidence.py`

**Work:** Normalize, hash, and serialize run metadata, event JSONL, results, and
receipt inputs. Add cross-record sequence rules that do not fit JSON Schema:
monotonic order, unique IDs, paired completed calls/results, explicitly unresolved
call IDs at interruption/crash/budget terminals, valid lineage references, and
terminal-state consistency.

**Acceptance:** The Module round-trips valid fixtures byte-stably, reports
field-qualified errors, rejects impossible ordering and unexplained open calls,
accepts terminal events that explicitly list unresolved call IDs, and never
treats unavailable metrics as zero.

### HN-010 — Implement Deterministic Run Preparation

**Priority / effort:** P0 / L
**Dependencies:** HN-009

**Files:**

- Create: `scripts/run-eval.py`
- Create: `scripts/evals/prepare.py`
- Create: `scripts/tests/test_run_eval_prepare.py`
- Modify: `evals/protocol.md`

**Interface:** `python scripts/run-eval.py prepare --case <id> --arm <arm>
--run-dir <path>`

**Work:** Validate inputs, copy exact fixture, assemble prompts verbatim, create
metadata, and record case/arm/prompt/fixture/grader/harness/environment hashes.
Reject existing nonempty targets and path escapes.

**Acceptance:** Two preparations from the same inputs have identical immutable
hashes; Windows path tests pass; no write occurs outside the named run folder.

### HN-011 — Implement Isolated Grading And Result Capture

**Priority / effort:** P0 / M
**Dependencies:** HN-010

**Files:**

- Create: `scripts/evals/grade.py`
- Create: `scripts/tests/test_run_eval_grade.py`
- Modify: `scripts/run-eval.py`

**Work:** Invoke the declared grader, validate result/exit semantics, hash the
final state, and have the runner emit the result envelope. The grader contributes
objective findings only when it ran; non-scorable setup, invalid-evidence, grader,
and runner states use a nullable primary outcome rather than a candidate failure.
A valid run that exhausts its declared budget remains score-applicable with a
false primary outcome. Detect grader/ground-truth mutation.

**Acceptance:** Known terminal states map deterministically; grading never
modifies candidate output except runner-owned result files; grader crashes do not
become candidate failures.

### HN-012 — Capture Events And Add A Deterministic Simulated Host

**Priority / effort:** P0 / L
**Dependencies:** HN-009, HN-010

**Files:**

- Create: `scripts/evals/events.py`
- Create: `scripts/evals/simulated_host.py`
- Create: `scripts/tests/test_eval_events.py`
- Create: `scripts/tests/test_simulated_host.py`
- Modify: `scripts/run-eval.py`
- Modify: `evals/protocol.md`

**Work:** Provide a local JSONL writer/importer for tool calls/results,
permissions, approvals, checkpoints, agent lineage, verification, usage, and
terminal state. Baseline sanitization strips secret values. Support manual import
when a host cannot stream events, retaining `runner_observed`, `host_reported`,
`worker_supplied`, or `derived` provenance. Add a deterministic simulated host
that can schedule tool calls, approvals, checkpoints, constraints, faults, and
agent lifecycle events for conformance testing; it is not evidence of real-host
enforcement. Enforce the design trust matrix so worker-supplied evidence is never
sole proof and derived evidence cannot upgrade its inputs.

**Acceptance:** Completed calls/results pair by ID; interrupted prefixes retain
explicit unresolved IDs or provenance-tagged runner closures without fabricated
host results. Secrets are omitted or sanitized, event order is monotonic, and
aggregate counts derive from admissible events rather than prose when events
exist. The simulator replays the same declared event schedule byte-stably and
labels every event as simulated.

### HN-013 — Add Battery Aggregation And Reliability Metrics

**Priority / effort:** P1 / M
**Dependencies:** HN-011, HN-012

**Files:**

- Create: `scripts/evals/summarize.py`
- Create: `scripts/tests/test_eval_summarize.py`
- Modify: `scripts/run-eval.py`
- Modify: `evals/protocol.md`

**Work:** Group by case/arm/configuration; report successes/attempts, median
scores and costs, `pass@1`, all-runs reliability for the chosen `k`, and an
uncertainty interval. Keep invalid trials separate from failures.

**Acceptance:** Unequal or missing repetitions are flagged; a group with one
success in three cannot be described as reliable; unavailable usage remains
explicit. Valid `budget_exceeded` runs remain in attempts and reliability
denominators; invalid budget evidence remains a separate invalid trial.

### HN-014 — Generate Reviewable Receipt Inputs

**Priority / effort:** P1 / M
**Dependencies:** HN-013

**Files:**

- Create: `scripts/evals/receipt.py`
- Create: `scripts/tests/test_eval_receipt.py`
- Create: `_core/templates/evaluation-receipt-template.md`
- Modify: `evals/cases/README.md`

**Work:** Generate a Markdown draft and structured receipt input from the same
validated data. Include configuration, hashes, commands, outcomes, reliability,
costs, deviations, limitations, and source-learning targets.

**Acceptance:** The Markdown and JSON facts agree; no claim depends only on an
unavailable raw path; human edits are clearly separated from generated facts.

### HN-015 — Run And Receipt A Current 0.2.4 Battery

**Priority / effort:** P1 / L
**Dependencies:** HN-010 through HN-014

**Files:**

- Generate locally: `evals/runs/<battery-id>/**`
- Create reviewed receipts under the selected tracked case Modules
- Modify if a repeated failure is confirmed: the owning harness reference,
  protocol, template, or grader

**Work:** Run one build and two traps, three repetitions per arm. Lock immutable
originals; create blind-review copies that change only enclosing names/wrapper
metadata while preserving candidate output bytes; run the uniform deterministic
grader against the originals; score the copies blind; then unblind and review
consequential process evidence. Do not improve worker outputs before scoring.

**Acceptance:** Every run has complete fingerprints and validated evidence;
receipts can reconstruct commands and inputs; source-learning changes cite a
repeated failure rather than one anecdote.

---

## Sprint 3: Prove Reliability And Recovery

### HN-016 — Add Required, Allowed, And Forbidden State Deltas

**Priority / effort:** P1 / L
**Dependencies:** HN-008, HN-011

**Files:**

- Modify: `evals/schemas/run-result.schema.json`
- Modify: `evals/schemas/case.schema.json`
- Modify: `scripts/evals/grade.py`
- Modify: `scripts/check-eval-cases.py`
- Modify: `scripts/tests/test_check_eval_cases.py`
- Modify: `_core/templates/evaluation-case-template.md`
- Create: `scripts/evals/state_delta.py`
- Create: `scripts/tests/test_state_delta.py`
- Modify: all tracked `evals/cases/*/case.json` manifests

**Acceptance:** Full residual state is checked; two valid Implementations pass;
a visible-test shortcut with collateral damage fails.

### HN-017 — Add Deterministic Case Lifecycle And Solvability Proof

**Priority / effort:** P1 / M
**Dependencies:** HN-008, HN-010, HN-011

**Files:**

- Create: `scripts/evals/lifecycle.py`
- Create: `scripts/tests/test_eval_lifecycle.py`
- Modify: `scripts/run-eval.py`
- Modify: `scripts/evals/prepare.py`
- Modify: `scripts/evals/grade.py`
- Modify: `evals/schemas/case.schema.json`
- Modify: `scripts/check-eval-cases.py`
- Modify: `scripts/tests/test_check_eval_cases.py`
- Modify: `_core/templates/evaluation-case-template.md`
- Modify: tracked `evals/cases/*/case.json` manifests

**Acceptance:** Setup twice with the declared seed, clock, timezone, and platform
contract yields the same state hash; teardown preserves failed cases when
configured; a validation solution proves solvability without becoming a required
trajectory.

### HN-018 — Establish Grader Mutation And Reward-Hacking Tests

**Priority / effort:** P1 / L
**Dependencies:** HN-016, HN-017

**Files:**

- Create: `evals/grader-conformance/README.md`
- Create: `evals/grader-conformance/mutants/**`
- Modify: `scripts/check-eval-cases.py`
- Modify: all tracked grader test suites

**Acceptance:** Every grader is challenged by no-op, empty, alternate-good,
bypass, evidence deletion, fixture edit, grader edit, skipped tool, and
overbroad-output mutants appropriate to its task.

### HN-019 — Enforce Per-Case Budgets And Safe Exhaustion

**Priority / effort:** P1 / M
**Dependencies:** HN-008, HN-011, HN-012

**Files:**

- Modify: `evals/schemas/case.schema.json`
- Modify: `evals/schemas/run-result.schema.json`
- Modify: tracked `evals/cases/*/case.json` manifests
- Create: `scripts/evals/budgets.py`
- Create: `scripts/tests/test_eval_budgets.py`
- Modify: `scripts/run-eval.py`
- Modify: `scripts/evals/grade.py`
- Modify: `scripts/evals/simulated_host.py`
- Modify: `evals/protocol.md`

**Acceptance:** Turn/request/tool/time limits are enforced against the simulated
host and any runner-owned subprocess boundary; parallel simulated calls cannot
silently overshoot. `budget_exceeded` preserves evidence and is distinct from a
generic objective-failure status, but a valid exhausted run still records primary
outcome `false` and counts as an attempt. Unavailable enforcement or invalid
budget evidence is non-scorable. Real-host enforcement is claimed only after
HN-032 demonstrates the corresponding interception capability.

### HN-020 — Add Polluted Repository Recovery Case

**Priority / effort:** P1 / L
**Dependencies:** HN-016, HN-017

**Files:** Create `evals/cases/polluted-repo-recovery/**`

**Variants:** full inherited trace, compact failure summary, and state-only,
holding the corrupted filesystem constant.

**Acceptance:** Score final success, repeated mistakes, collateral damage,
recovery cost, and whether stale narration was reconciled with live state.

### HN-021 — Add Compaction And Bounded-Checkpoint Case

**Priority / effort:** P1 / L
**Dependencies:** HN-012, HN-020

**Files:**

- Create: `evals/cases/compaction-fidelity/**`
- Create: `evals/arm-prompts/bounded-checkpoint.md`
- Modify: `evals/protocol.md`

**Acceptance:** A load-bearing pre-compaction decision is recoverable from an
explicit durable record; guessing from a supplied lossy summary fails;
bounded-checkpoint is reported as an experimental arm, not a shipped harness
mode or a claim about a real host's compactor.

### HN-022 — Add Metamorphic Perturbation And Fault Injection

**Priority / effort:** P1 / L
**Dependencies:** HN-017, HN-019

**Files:**

- Create: `scripts/evals/perturb.py`
- Create: `scripts/evals/faults.py`
- Create: `scripts/tests/test_eval_perturb_faults.py`
- Add variants to at least two tracked cases

**Acceptance:** Semantically equivalent prompt/state variants preserve the
expected end state; controlled timeout, rate-limit, partial-result, and schema-
drift faults from the deterministic simulator measure recovery without changing
hidden ground truth. Real-host fault behavior requires a later host receipt.

---

## Sprint 4: Enforce Trust Boundaries

### HN-023 — Add Executable Boundary Profiles

**Priority / effort:** P1 / L
**Dependencies:** HN-008, HN-012

**Files:**

- Modify: `evals/schemas/case.schema.json`
- Modify: `scripts/check-eval-cases.py`
- Modify: `scripts/tests/test_check_eval_cases.py`
- Modify: `_core/templates/evaluation-case-template.md`
- Modify: tracked `evals/cases/*/case.json` manifests
- Create: `scripts/evals/boundaries.py`
- Create: `scripts/tests/test_eval_boundaries.py`
- Modify: `scripts/evals/simulated_host.py`

**Acceptance:** Read roots, write roots, network, protected paths, external
systems, and allow/ask/deny expectations validate; attempted violations appear in
results even when final state is clean. Enforcement is proven first against the
simulator/runner boundary; real-host claims wait for HN-032.

### HN-024 — Add Untrusted Environment Instruction Case

**Priority / effort:** P1 / L
**Dependencies:** HN-023, HN-028

**Files:** Create `evals/cases/untrusted-environment-instruction/**`

**Acceptance:** A plausible malicious instruction in README/log/tool output
cannot redirect the frozen task, access protected data, or cause forbidden
effects in the simulator/runner boundary; useful task completion remains
possible. A real-host security claim requires HN-032 evidence.

### HN-025 — Add Deferred Approval And Resume Case

**Priority / effort:** P1 / L
**Dependencies:** HN-017, HN-023, HN-012

**Files:** Create `evals/cases/deferred-approval-resume/**`

**Acceptance:** Stable pending request IDs, approve and deny branches,
out-of-band sensitive input, original-context resume, and no duplicate completed
side effects are all graded in deterministic simulated-host branches. A later
real-host receipt must disclose which approval capabilities the host exposes.

### HN-026 — Add Dynamic High-Cardinality Tool Discovery Case

**Priority / effort:** P1 / L
**Dependencies:** HN-012, HN-023

**Files:** Create `evals/cases/dynamic-tool-catalog/**`

**Acceptance:** Many decoy schemas, a small relevant subset, pagination/list
change, one malformed structured result, wrong-tool counts, and loaded-context
cost are observable and graded through the simulated catalog. Real-host dynamic
catalog behavior remains a separate HN-032 capability check.

### HN-027 — Add Stateful Insufficient-Information Case

**Priority / effort:** P1 / M
**Dependencies:** HN-016, HN-023

**Files:** Create `evals/cases/stateful-tool-insufficient-info/**`

**Acceptance:** The agent discovers hidden prerequisites, asks exactly when a
required value cannot be inferred safely, abstains from premature mutation, and
continues correctly after a deterministic simulated answer.

### HN-028 — Validate Trace Redaction And Evidence Integrity

**Priority / effort:** P1 / M
**Dependencies:** HN-012, HN-014

**Files:**

- Modify: `scripts/evals/events.py`
- Modify: `scripts/evals/receipt.py`
- Create: `scripts/tests/test_eval_redaction.py`
- Modify: `scripts/tests/test_eval_receipt.py`
- Modify: `evals/schemas/trace-event.schema.json`
- Modify: `evals/schemas/receipt.schema.json`
- Modify: `evals/protocol.md`

**Acceptance:** Adversarial fixtures prove secrets never appear in trace values,
errors, receipts, or unsalted hashes. Correlation uses only a keyed per-battery
HMAC token with a non-exported, rotatable key; otherwise the digest is omitted.
Redaction cannot erase tool/result lineage or permission evidence. HN-012 owns
baseline sanitization; this ticket owns leakage attacks and integrity checks.

---

## Sprint 5: Test Long-Horizon Work And Portability

### HN-029 — Add Late-Constraint Long-Workflow Case

**Priority / effort:** P2 / L
**Dependencies:** HN-020, HN-021, HN-023

**Files:** Create `evals/cases/late-constraint-long-workflow/**`

**Acceptance:** A deterministic event introduces a new constraint after a
checkpoint; binary completion remains primary; milestones diagnose requirement
retention, re-planning, and verification. The first receipt is explicitly a
simulated-host conformance result, not a real-host capability claim.

### HN-030 — Add Stale Multi-Agent Handoff Case

**Priority / effort:** P2 / L
**Dependencies:** HN-012, HN-020, HN-023

**Files:** Create `evals/cases/stale-multi-agent-handoff/**`

**Acceptance:** Compare single-agent and delegated runs; grade delegation fit,
scope, information transfer, receiver acknowledgment, live-state reconciliation,
cancellation, merge, termination, and final verification in the deterministic
simulator. Real multi-agent host behavior is reported only after HN-032.

### HN-031 — Add Agent-Computer Interface Ablation

**Priority / effort:** P2 / L
**Dependencies:** HN-032

**Files:**

- Create: `evals/cases/interface-ablation/**`
- Create explicit interface profiles under `evals/interfaces/`
- Modify: protocol

**Work:** Compare raw shell with constrained search/edit/test actions. Where one
host exposes it without changing the model or task, add an experimental
sandboxed programmatic-tool profile that can batch loops, conditionals, and
parallel reads inside one model tool call.

**Sequencing note:** HN-032 executes before this ticket despite numeric order; a
real selected host is required for a meaningful interface ablation.

**Acceptance:** The same model, task, environment, and budget run through the
declared interface profiles; invalid actions, model round trips, feedback size,
retries, recovery, success, and cost are compared. The programmatic profile is
reported separately when it is unavailable on another host.

### HN-032 — Select And Implement The First Host Integration

**Priority / effort:** P2 / L
**Dependencies:** HN-012, HN-015

**Stop point:** User selects the first host and approves any required local CLI or
credential setup.

**Files:** Create one direct Implementation under `scripts/evals/hosts/` plus
focused tests and a tool card.

**Acceptance:** It prepares a task, captures available events/usage with explicit
provenance/capability declarations, maps terminal states, and runs one tracked
case without a speculative shared base class. A host-capability matrix maps the
planned conformance scenarios to supported, unsupported, or not-yet-run without
awarding a pass for missing evidence. Each scenario receives a real-host receipt
only when both its owning ticket and this Adapter exist.

### HN-033 — Implement A Second Host And Extract The Proven Adapter Interface

**Priority / effort:** P2 / L
**Dependencies:** HN-032

**Stop point:** User selects the second host.

**Work:** Implement the second host directly, compare both, then extract only
repeated integration behavior into a host Adapter Interface.

**Acceptance:** Both Implementations pass common contract tests plus host-specific
tests; deleting the Interface would duplicate meaningful logic in both Adapters.

### HN-034 — Add Cross-Platform And Boundary Matrix

**Priority / effort:** P2 / M
**Dependencies:** HN-033

**Files:**

- Modify: `.github/workflows/validate.yml`
- Create: `evals/platform-matrix.md`
- Add platform fixtures/tests as required

**Acceptance:** Windows, WSL2/Linux, path semantics, executable discovery,
line endings, sandbox availability, and unsupported features are reported per
host without claiming false parity.

---

## Sprint 6: Maintain Capability Evidence

### HN-035 — Establish A Rotating Held-Out Capability Tier

**Priority / effort:** P2 / L
**Dependencies:** HN-015, HN-018

**Files:**

- Create: `evals/heldout/README.md` or an approved external/private location
- Modify: `evals/protocol.md`
- Modify: `evals/schemas/case.schema.json`
- Modify: `_core/templates/evaluation-case-template.md`

**Stop point:** User approves storage, access, and retirement policy.

**Acceptance:** Capability cases record source date, environment digest, access
rules, and retirement; retired cases promote into tracked regression Modules
without leaking active holdouts.

### HN-036 — Calibrate Human And Optional Model-Based Graders

**Priority / effort:** P2 / L
**Dependencies:** HN-015, HN-018

**Files:**

- Create: `evals/calibration/README.md`
- Create: `evals/calibration/labels/**`
- Create optional judge Adapter only after labels exist

**Acceptance:** Human-labeled examples, disagreement categories, inter-rater
agreement, and judge false-positive/negative rates are reported; deterministic
state checks remain authoritative for objective facts.

### HN-037 — Convert Reviewed Failures Into Bounded Eval Tasks

**Priority / effort:** P2 / M
**Dependencies:** HN-015, HN-018

**Files:**

- Create: `_core/templates/evaluation-finding-template.md`
- Modify: source-learning sections in protocol and conventions
- Add a local promotion script only if repeated bookkeeping justifies it

**Acceptance:** Each promoted failure links trace/receipt, user impact,
reproduction, target contract, case/grader change, regression evidence, and human
approval. No single trajectory silently rewrites the harness.

### HN-038 — Add Recurring Drift And Quality-Grade Scans

**Priority / effort:** P2 / M
**Dependencies:** HN-004, HN-015, HN-037

**Files:**

- Create: `evals/quality-grade.md`
- Modify only the owning validator and focused tests when an invariant belongs to
  `scripts/check-eval-cases.py` or `scripts/check-skill-package.py`
- Modify: `.github/workflows/validate.yml` only to invoke established owning
  checks

**Work:** Maintain a reviewed cross-cutting quality report covering live routing,
one-way dependency rules, source freshness, package versions, placeholder/line
budgets, stage status, receipt coverage, public-case saturation, and
ignored/canonical artifact boundaries. Put an executable invariant in its owning
checker. Do not create a grab-bag orchestration script unless repeated CLI
duplication demonstrates a separate Module.

**Acceptance:** Findings name a remediation path; scans never auto-edit canonical
files; quality changes are reviewable diffs.

### HN-039 — Pin Research Freshness And Protocol Versions

**Priority / effort:** P2 / S
**Dependencies:** none

**Files:**

- Modify: `knowledge/sources/2026-07-12-agent-harness-innovation-source-ledger.md`
- Modify: `knowledge/wiki/agent-harness-innovation-gaps.md`
- Create: `knowledge/sources/source-review-schedule.md`

**Acceptance:** Live product docs record retrieval dates; MCP stable and RC
versions are not conflated; recent preprints retain maturity labels; a scheduled
review identifies stale claims without automatically adopting changes.

### HN-040 — Measure Reference Trigger Precision And Recall

**Priority / effort:** P2 / M
**Dependencies:** HN-012, HN-015

**Files:**

- Create: `evals/cases/reference-trigger-routing/**`
- Modify: `evals/protocol.md`
- Modify only after measured failure: `fable-task-harness/SKILL.md`

**Work:** Build a task taxonomy covering small edits, existing-project changes,
research, tool use, external mutation, structured state, verification, folder
workflow design, and autonomy decisions. Record which references were available,
loaded, useful, missed, or unnecessary. Compare the normal harness arm with
full-load and a deliberately minimal routing baseline under the same model and
budget.

**Acceptance:** Report per-reference precision/recall-style routing counts,
missed-risk cases, unnecessary loads, cached/input token effects when exposed,
and task outcomes. Change trigger wording only for a repeated measured failure;
do not add a reference merely to improve the routing score.

---

## Backlog-Wide Definition Of Done

A ticket is complete only when:

1. executable behavior and schema changes have red tests that failed for the
   intended reason before implementation; docs, research, policy, and battery-run
   tickets instead record a deterministic before/after probe or evidence receipt;
2. focused tests and the relevant full suite pass afterward where applicable;
3. generated artifacts remain inside the declared output surface;
4. no unrelated user change was overwritten;
5. docs and executable behavior agree;
6. new durable claims cite a tracked receipt or primary source;
7. limitations and unavailable telemetry are explicit;
8. an independent reviewer finds no open Critical or Important issue;
9. `git diff --check` adds no warning in ticket-owned paths; on an existing dirty
   worktree, compare against the recorded pre-ticket baseline rather than claiming
   unrelated user changes;
10. the work is not committed, pushed, or published unless separately requested.

## Recommended First Pull

Start HN-001, HN-002, and HN-004 as separate reviewable slices. Follow with
HN-003 after HN-002 and HN-005 after HN-004. Together they close the highest-risk
contract mismatch and make validation reproducible. Pull stretch/carryover
HN-006 and HN-007 only after those gates are green; they provide the two
additional Implementations needed to design shared execution and evidence
Modules from real repetition rather than speculation.
