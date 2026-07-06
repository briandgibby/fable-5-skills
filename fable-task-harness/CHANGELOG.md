# Changelog

## 0.2.4 - 2026-07-06

Regression run `evals/runs/undocumented-local-tool-v0.2.3/` (harness arm, 3 runs) verified the 0.2.3 hygiene fix: all three runs preserved the tool's `usage.log` with a logged OK build and produced byte-identical reports; no over-cautious side effects from the new wording were observed.

Changed:

- The verification-playbook reporting rule now requires naming any generated files deliberately left in place beyond the requested artifact, with one line on why. In the regression, two of three runs correctly preserved the audit log but never mentioned it, leaving a reviewer unable to distinguish deliberate preservation from luck. The prior wording only required a mention "when unsure".

## 0.2.3 - 2026-07-06

Source improvements from the undocumented-local-tool trap battery (`evals/runs/undocumented-local-tool/`, 3 runs x 3 arms). The core trap saturated — zero invented flags or failed invocations in any arm — but the battery caught a harness-induced defect: the 0.2.2 verification-hygiene rule ("clean up anything else your checks generate") led 3 of 6 harness-family runs to delete the tool's own audit log as cleanup, destroying evaluation evidence. Control runs, which never read the rule, preserved the log 3/3.

Fixed:

- Scoped the verification-hygiene rule to artifacts the verification itself created, and added an explicit prohibition: logs, audit trails, state files, receipts, and history produced by a tool or system during normal operation are records, never cleanup targets. When unsure, leave the file and note it.

Changed:

- `side-effect-boundaries.md`: deleting a file you did not create is classified as external mutation requiring justification, not cleanup.
- `tool-contracts.md` follow-through: when a tool's interface was undocumented, notes must state the discovery method (help output, source read, or both) and the exact working command.

## 0.2.2 - 2026-07-05

Source improvements from the decoy-config-repo trap battery (`evals/runs/decoy-config-repo/`, 3 runs x 3 arms), the first evaluation with ground truth. No arm fell for the decoy, but harness arms documented the decoy discrepancy 6/6 versus control's 1/3 — the harness's first measured win. Cost stayed modest: roughly +2 tool calls and +7 file reads over control, versus full-load's much larger overhead for identical outcomes.

Changed:

- The verification-playbook reporting rule now requires naming any stale doc, config, or reference that contradicts the live source of truth. All nine runs edited the right file, but zero flagged the stale README specifically; readers of most control notes would never learn the docs mislead.
- Added a verification-hygiene rule: checks must not leave generated artifacts in the deliverable (all nine runs left Python bytecode in `app/`; `PYTHONDONTWRITEBYTECODE=1` named as the fix).
- Added a fast path note to the trigger table: small single-file edits usually need only intake-and-routing plus verification-playbook. All three harness runs loaded the same six references for a one-line edit; the fast path keeps the two references that produced the measured win.

## 0.2.1 - 2026-07-05

Source improvements from the static-focus-board v0.2 rerun (`evals/runs/static-focus-board-v0.2/`), where the harness arm reached real-browser verification and reported its rung — but overbuilt the app and paid roughly double control's wall time.

Changed:

- The anti-overbuild rule now names the failure concretely: no management controls (reset, sort, bulk actions, filters, export, analytics) unless requested. The rerun's harness arm shipped a sort toggle, "Clear done", and "Reset today" against a prompt that asked for none of them.
- Narrowed the `side-effect-boundaries.md` trigger from any file mutation to changing existing files, external systems, or user-facing state. Creating the requested artifact in its designated output location no longer triggers the reference. Six of ten references fired on a simple greenfield build; this was the least justified.

## 0.2.0 - 2026-07-05

Restructure driven by the first A/B/C evaluation (`evals/runs/static-focus-board/`), which showed the harness tying control on artifact quality while costing more, with verification as the weakest pillar.

Fixed:

- `SKILL.md` frontmatter was invalid YAML: the unquoted description contained a `: ` sequence, which strict loaders reject with "mapping values are not allowed here". The description is now quoted.

Changed:

- `SKILL.md` is now only the always-loaded spine: operating loop, observable reference triggers, and operating rules. The always-on/situational/control "Modes" section was removed — those were evaluation arms, not product behavior, and leaked factory content into the shipped artifact. Loading depth is now architectural: the spine is small, and references load per trigger.
- Reference triggers changed from judgment-based ("when the task shape warrants") to observable task-shape predicates.
- Consolidated overlapping references. `tool-sequencing.md`, `parameter-hygiene.md`, and `tool-schema-discovery.md` merged into `tool-contracts.md`. `environment-contract.md` and `structured-output-and-parsing.md` merged into `runtime-and-state-contracts.md`. `tool-card-template.md` guidance moved into `templates/tool-card.md`. Thirteen references became ten, with each rule now having one canonical home.
- Removed roadmap references to unbuilt future skills (`deep-research`, `trust-boundary-filter`) from shipped references.

Added:

- `references/verification-playbook.md`: per-artifact-type verification depth ladders with an explicit fallback order and a reporting rule that the depth reached, blocked rungs, and unverified remainder must be stated.
- Anti-overbuild operating rule: build the smallest artifact that satisfies the request; name omitted extras instead of building them.
- A worked wrong-versus-right example in every operational reference.
- `version` field in frontmatter and this changelog. Evaluation runs must record the harness version they tested.

## 0.1.0 - 2026-07-05

- Initial package: compact SKILL.md with always-on/situational modes, thirteen references, six templates, and an OpenAI-facing loader hint.
