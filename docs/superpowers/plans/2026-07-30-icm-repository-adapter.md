# ICM Repository Adapter Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (- [ ]) syntax for tracking.

**Goal:** Add a verified repository-specific ICM adapter that routes nontrivial work through the separately maintained central kernel without changing the shipped harness.

**Architecture:** A thin icm/ control plane records repository facts, checks, and task-package routes while the existing five-layer project structure remains canonical content. A local Python checker validates only that adapter boundary; central planning, approval, build, review, and run validation stay in ICM-agentic-system.

**Tech Stack:** Markdown, JSON, Python 3 standard library, unittest, PowerShell verification commands.

## Global Constraints

- Consume the separately maintained central ICM kernel; do not copy its contracts, policies, skills, templates, or validators.
- Preserve CONTEXT.md, workspaces/, knowledge/, docs/, evals/, and fable-task-harness/ as current canonical sources and products.
- Require explicit $plan-task, separate approval, and explicit $build-task for nontrivial skill, architecture, script, evaluation-protocol, tracked-case, and grader changes.
- Keep the existing minimal workflow for small documentation and routing corrections that do not alter behavior or contracts.
- Do not change fable-task-harness behavior or version.
- Add no dependency; the checker uses only the Python 3 standard library.
- Preserve unrelated user changes and stage explicit paths only.
- Commit the checker, adapter, and root routing as separate verified milestones.

---

## File Map

**Create:**

- scripts/check-icm-repository.py — deterministic validation of the local adapter boundary.
- scripts/tests/test_check_icm_repository.py — subprocess-level checker tests using temporary repository fixtures.
- icm/CONTEXT.md — repository ICM router and central-kernel boundary.
- icm/profile.json — verified commands, paths, risk triggers, and review-rubric configuration.
- icm/knowledge/CONTEXT.md — routes ICM roles to existing canonical repository facts.
- icm/checks/CONTEXT.md — reusable command contracts.
- icm/tasks/CONTEXT.md — task-package and evidence-storage rules.

**Modify:**

- AGENTS.md — route nontrivial changes into ICM and retain the small-correction exception.
- CONTEXT.md — expose the ICM adapter in the task router and outputs.
- _core/CONVENTIONS.md — define how the ICM control plane relates to the five-layer content model.
- README.md — explain the operator-facing ICM lifecycle and prerequisite.

**Explicitly unchanged:**

- fable-task-harness/**
- evals/**
- workspaces/**
- Central ICM source in the sibling ICM-agentic-system repository.

---

### Task 1: Test-Driven Repository Adapter Checker

**Files:**

- Create: scripts/tests/test_check_icm_repository.py
- Create: scripts/check-icm-repository.py

**Interfaces:**

- Consumes: a repository root passed as --repo-root PATH; defaults to the parent of scripts/.
- Produces: validate_repository(repo_root: Path) -> list[str] and a CLI that returns 0 with "icm repository adapter: all checks passed" or 1 with one ERROR line per violation.
- Enforces: local adapter structure, repository-profile shape, relative existing paths, command strings, resolved placeholders, and absence of vendored central-only directories.

- [ ] **Step 1: Write the checker tests**

Create scripts/tests/test_check_icm_repository.py with:

~~~python
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
CHECKER = REPO_ROOT / "scripts" / "check-icm-repository.py"
REQUIRED_ADAPTER_FILES = (
    "icm/CONTEXT.md",
    "icm/profile.json",
    "icm/knowledge/CONTEXT.md",
    "icm/checks/CONTEXT.md",
    "icm/tasks/CONTEXT.md",
)


def valid_profile() -> dict[str, object]:
    return {
        "profile_version": 1,
        "repository_name": "fixture-repository",
        "commands": {
            "test": ["python -m unittest"],
            "lint": [],
            "typecheck": [],
            "build": [],
        },
        "paths": {"source": ["src/"], "tests": ["tests/"]},
        "task_profile_triggers": {"high_risk": ["security"]},
        "domain_review_rubrics": [],
    }


def write_profile(repo_root: Path, profile: dict[str, object]) -> None:
    (repo_root / "icm" / "profile.json").write_text(
        json.dumps(profile, indent=2) + "\n",
        encoding="utf-8",
    )


def write_valid_repository(repo_root: Path) -> None:
    for relative in REQUIRED_ADAPTER_FILES:
        path = repo_root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.suffix == ".md":
            path.write_text("# Context\n", encoding="utf-8")
    (repo_root / "src").mkdir()
    (repo_root / "tests").mkdir()
    write_profile(repo_root, valid_profile())


class CheckIcmRepositoryTests(unittest.TestCase):
    def run_checker(self, repo_root: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(CHECKER), "--repo-root", str(repo_root)],
            text=True,
            capture_output=True,
            check=False,
        )

    def test_valid_adapter_passes(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            write_valid_repository(repo_root)

            result = self.run_checker(repo_root)

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("icm repository adapter: all checks passed", result.stdout)

    def test_required_adapter_files_must_exist(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            write_valid_repository(repo_root)
            (repo_root / "icm" / "checks" / "CONTEXT.md").unlink()

            result = self.run_checker(repo_root)

        self.assertEqual(result.returncode, 1)
        self.assertIn(
            "required adapter file is missing: icm/checks/CONTEXT.md",
            result.stderr,
        )

    def test_profile_fields_must_match_the_central_shape(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            write_valid_repository(repo_root)
            profile = valid_profile()
            del profile["commands"]["build"]
            write_profile(repo_root, profile)

            result = self.run_checker(repo_root)

        self.assertEqual(result.returncode, 1)
        self.assertIn(
            "commands fields must be exactly: build, lint, test, typecheck",
            result.stderr,
        )

    def test_profile_paths_must_be_relative_and_exist(self):
        mutations = (
            ("../outside", "must be a relative path inside the repository"),
            ("missing/", "does not exist"),
        )
        for value, message in mutations:
            with self.subTest(value=value), tempfile.TemporaryDirectory() as temp_dir:
                repo_root = Path(temp_dir)
                write_valid_repository(repo_root)
                profile = valid_profile()
                profile["paths"]["source"] = [value]
                write_profile(repo_root, profile)

                result = self.run_checker(repo_root)

            self.assertEqual(result.returncode, 1)
            self.assertIn(message, result.stderr)

    def test_profile_commands_must_be_nonempty_strings(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            write_valid_repository(repo_root)
            profile = valid_profile()
            profile["commands"]["test"] = [""]
            write_profile(repo_root, profile)

            result = self.run_checker(repo_root)

        self.assertEqual(result.returncode, 1)
        self.assertIn("commands.test[0] must be a nonempty string", result.stderr)

    def test_adapter_files_must_not_contain_template_placeholders(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            write_valid_repository(repo_root)
            placeholder = "__" + "MISSING_VALUE" + "__"
            (repo_root / "icm" / "CONTEXT.md").write_text(
                f"# {placeholder}\n",
                encoding="utf-8",
            )

            result = self.run_checker(repo_root)

        self.assertEqual(result.returncode, 1)
        self.assertIn("contains unresolved template placeholder", result.stderr)

    def test_central_only_directories_must_not_be_vendored(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            write_valid_repository(repo_root)
            (repo_root / "icm" / "contracts").mkdir()

            result = self.run_checker(repo_root)

        self.assertEqual(result.returncode, 1)
        self.assertIn(
            "central-only path must not be vendored: icm/contracts",
            result.stderr,
        )


if __name__ == "__main__":
    unittest.main()
~~~

- [ ] **Step 2: Run the tests to verify the red state**

Run:

~~~powershell
python -m unittest scripts.tests.test_check_icm_repository -v
~~~

Expected: 7 failures because scripts/check-icm-repository.py does not exist.

- [ ] **Step 3: Implement the minimal checker**

Create scripts/check-icm-repository.py with:

~~~python
#!/usr/bin/env python3
"""Validate this repository's thin adapter to the central ICM kernel."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path, PureWindowsPath


REQUIRED_ADAPTER_FILES = (
    "icm/CONTEXT.md",
    "icm/profile.json",
    "icm/knowledge/CONTEXT.md",
    "icm/checks/CONTEXT.md",
    "icm/tasks/CONTEXT.md",
)
FORBIDDEN_CENTRAL_PATHS = (
    "icm/contracts",
    "icm/policies",
    "icm/validators",
)
PROFILE_FIELDS = {
    "profile_version",
    "repository_name",
    "commands",
    "paths",
    "task_profile_triggers",
    "domain_review_rubrics",
}
COMMAND_FIELDS = {"test", "lint", "typecheck", "build"}
PATH_FIELDS = {"source", "tests"}
TRIGGER_FIELDS = {"high_risk"}
PLACEHOLDER_PATTERN = re.compile(r"__[A-Z][A-Z0-9_]*__")


def exact_fields(value: object, expected: set[str], label: str) -> list[str]:
    if not isinstance(value, dict):
        return [f"{label} must be a JSON object"]
    actual = set(value)
    if actual != expected:
        return [f"{label} fields must be exactly: {', '.join(sorted(expected))}"]
    return []


def string_list(
    value: object,
    label: str,
    *,
    require_nonempty: bool = False,
) -> list[str]:
    if not isinstance(value, list):
        return [f"{label} must be a list"]
    errors = []
    if require_nonempty and not value:
        errors.append(f"{label} must not be empty")
    for index, item in enumerate(value):
        if not isinstance(item, str) or not item.strip():
            errors.append(f"{label}[{index}] must be a nonempty string")
    return errors


def relative_existing_path(repo_root: Path, value: object, label: str) -> list[str]:
    if not isinstance(value, str) or not value.strip():
        return [f"{label} must be a nonempty string"]
    candidate = Path(value)
    if (
        candidate.is_absolute()
        or candidate.drive
        or PureWindowsPath(value).drive
        or ".." in candidate.parts
    ):
        return [f"{label} must be a relative path inside the repository"]
    resolved_root = repo_root.resolve()
    resolved = (repo_root / candidate).resolve()
    try:
        resolved.relative_to(resolved_root)
    except ValueError:
        return [f"{label} must be a relative path inside the repository"]
    if not resolved.exists():
        return [f"{label} does not exist: {value}"]
    return []


def validate_profile(repo_root: Path, profile: object) -> list[str]:
    errors = exact_fields(profile, PROFILE_FIELDS, "profile")
    if not isinstance(profile, dict):
        return errors

    if profile.get("profile_version") != 1:
        errors.append("profile_version must be 1")
    name = profile.get("repository_name")
    if not isinstance(name, str) or not name.strip():
        errors.append("repository_name must be a nonempty string")

    commands = profile.get("commands")
    errors.extend(exact_fields(commands, COMMAND_FIELDS, "commands"))
    if isinstance(commands, dict):
        for field in sorted(COMMAND_FIELDS):
            errors.extend(
                string_list(
                    commands.get(field),
                    f"commands.{field}",
                    require_nonempty=field == "test",
                )
            )

    paths = profile.get("paths")
    errors.extend(exact_fields(paths, PATH_FIELDS, "paths"))
    if isinstance(paths, dict):
        for field in sorted(PATH_FIELDS):
            values = paths.get(field)
            errors.extend(string_list(values, f"paths.{field}", require_nonempty=True))
            if isinstance(values, list):
                for index, value in enumerate(values):
                    errors.extend(
                        relative_existing_path(
                            repo_root,
                            value,
                            f"paths.{field}[{index}]",
                        )
                    )

    triggers = profile.get("task_profile_triggers")
    errors.extend(exact_fields(triggers, TRIGGER_FIELDS, "task_profile_triggers"))
    if isinstance(triggers, dict):
        errors.extend(
            string_list(
                triggers.get("high_risk"),
                "task_profile_triggers.high_risk",
                require_nonempty=True,
            )
        )

    errors.extend(
        string_list(profile.get("domain_review_rubrics"), "domain_review_rubrics")
    )
    return errors


def load_profile(path: Path) -> tuple[object | None, list[str]]:
    try:
        return json.loads(path.read_text(encoding="utf-8")), []
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return None, [f"cannot read icm/profile.json: {exc}"]


def validate_placeholders(repo_root: Path) -> list[str]:
    errors = []
    for relative in REQUIRED_ADAPTER_FILES:
        path = repo_root / relative
        if not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            errors.append(f"cannot read {relative}: {exc}")
            continue
        if PLACEHOLDER_PATTERN.search(text):
            errors.append(f"{relative} contains unresolved template placeholder")
    return errors


def validate_repository(repo_root: Path) -> list[str]:
    repo_root = repo_root.resolve()
    errors = []
    for relative in REQUIRED_ADAPTER_FILES:
        if not (repo_root / relative).is_file():
            errors.append(f"required adapter file is missing: {relative}")
    for relative in FORBIDDEN_CENTRAL_PATHS:
        if (repo_root / relative).exists():
            errors.append(f"central-only path must not be vendored: {relative}")

    profile_path = repo_root / "icm" / "profile.json"
    if profile_path.is_file():
        profile, profile_errors = load_profile(profile_path)
        errors.extend(profile_errors)
        if not profile_errors:
            errors.extend(validate_profile(repo_root, profile))
    errors.extend(validate_placeholders(repo_root))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate the repository's thin ICM adapter"
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
    )
    args = parser.parse_args()

    errors = validate_repository(args.repo_root)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"\n{len(errors)} error(s) in ICM repository adapter", file=sys.stderr)
        return 1
    print("icm repository adapter: all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
~~~

- [ ] **Step 4: Run the checker tests to verify the green state**

Run:

~~~powershell
python -m unittest scripts.tests.test_check_icm_repository -v
~~~

Expected: 7 tests run and OK.

- [ ] **Step 5: Verify and commit the checker slice**

Run:

~~~powershell
git diff --check
git status --short
git add -- scripts/check-icm-repository.py scripts/tests/test_check_icm_repository.py
git diff --cached --check
git commit -m "feat: validate ICM repository adapter"
~~~

Expected: the staged diff contains exactly the checker and its test; the commit succeeds.

---

### Task 2: Repository-Specific ICM Adapter

**Files:**

- Modify: scripts/tests/test_check_icm_repository.py
- Create: icm/CONTEXT.md
- Create: icm/profile.json
- Create: icm/knowledge/CONTEXT.md
- Create: icm/checks/CONTEXT.md
- Create: icm/tasks/CONTEXT.md

**Interfaces:**

- Consumes: the checker CLI and central repository-template field names established in Task 1.
- Produces: a complete local adapter that the central $plan-task and $build-task skills can consume.
- Routes: to existing canonical project files rather than creating replacement architecture, domain, convention, or safety documents.

- [ ] **Step 1: Add a failing checked-in integration test**

Insert this method at the end of CheckIcmRepositoryTests, before the final if __name__ block in scripts/tests/test_check_icm_repository.py:

~~~python
    def test_checked_in_repository_passes(self):
        result = self.run_checker(REPO_ROOT)

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("icm repository adapter: all checks passed", result.stdout)
~~~

- [ ] **Step 2: Run the integration test to verify the red state**

Run:

~~~powershell
python -m unittest scripts.tests.test_check_icm_repository.CheckIcmRepositoryTests.test_checked_in_repository_passes -v
~~~

Expected: FAIL with a missing required adapter file such as icm/CONTEXT.md.

- [ ] **Step 3: Create the repository ICM router**

Create icm/CONTEXT.md with:

~~~markdown
# Repository ICM Context

This directory is the repository-specific adapter to the separately maintained central ICM kernel. Central policy governs orchestration and external-action boundaries. Existing project files remain authoritative for repository facts.

## Routes

| Need | Source |
|---|---|
| Verified commands and repository paths | profile.json |
| Existing project task routing | ../CONTEXT.md |
| Architecture, domain, convention, and safety facts | knowledge/CONTEXT.md |
| Reusable repository checks | checks/CONTEXT.md |
| Task packages and execution evidence | tasks/<task-id>/ |

Load only the central stage contract, this adapter, and the existing sources named for the task. Do not copy central contracts, policies, skills, templates, or validators into this repository.

Task discoveries remain candidates until a human promotes them into an existing canonical repository source.
~~~

- [ ] **Step 4: Create the verified repository profile**

Create icm/profile.json with:

~~~json
{
  "profile_version": 1,
  "repository_name": "fable-5-skills",
  "commands": {
    "test": [
      "python scripts/check-icm-repository.py",
      "python scripts/check-skill-package.py",
      "python scripts/check-eval-cases.py",
      "python -m unittest discover -s scripts/tests -v"
    ],
    "lint": [],
    "typecheck": [],
    "build": []
  },
  "paths": {
    "source": [
      "AGENTS.md",
      "CONTEXT.md",
      "README.md",
      "_core/",
      "docs/",
      "evals/",
      "fable-task-harness/",
      "knowledge/",
      "scripts/",
      "workspaces/"
    ],
    "tests": [
      "scripts/tests/",
      "evals/cases/"
    ]
  },
  "task_profile_triggers": {
    "high_risk": [
      "security",
      "authentication",
      "authorization",
      "migration",
      "destructive",
      "financial",
      "irreversible",
      "external-side-effect"
    ]
  },
  "domain_review_rubrics": []
}
~~~

- [ ] **Step 5: Create the knowledge router**

Create icm/knowledge/CONTEXT.md with:

~~~markdown
# Repository Knowledge

Use existing canonical files as repository knowledge. This router does not restate their durable content.

| Need | Canonical source | Section or scope |
|---|---|---|
| Project architecture and folder model | ../../_core/CONVENTIONS.md | Five-Layer Context Model and Routing Rules |
| Accepted harness decisions | ../../docs/fable-pseudo-harness-master.md | Current Position through Immediate Next Steps |
| Current harness behavior | ../../fable-task-harness/SKILL.md | Full file |
| Project task routing | ../../CONTEXT.md | Task Routing |
| Repository operating and safety rules | ../../AGENTS.md | Operating Rules |
| Evaluation methodology and scoring | ../../evals/protocol.md, ../../evals/rubric.md | Full files |
| Tracked evaluation-case contract | ../../evals/cases/README.md | Full file |
| Knowledge and source-integrity rules | ../../_core/CONVENTIONS.md | Knowledge Rules and Source Integrity |

Only evidence-backed facts belong in canonical sources. Task observations remain in their task package until a human approves promotion.
~~~

- [ ] **Step 6: Create the reusable check router**

Create icm/checks/CONTEXT.md with:

~~~markdown
# Repository Checks

Run commands from the repository root with Python 3. Record raw output and exit status in the active ICM task package.

| Change or claim | Command | Prerequisite | Success signal |
|---|---|---|---|
| ICM adapter structure or routing | python scripts/check-icm-repository.py | None beyond Python 3 | Exit 0 and "icm repository adapter: all checks passed" |
| Installable harness package | python scripts/check-skill-package.py | PyYAML available | Exit 0 and "fable-task-harness: all checks passed" |
| Tracked evaluation cases or graders | python scripts/check-eval-cases.py | Declared case grader tests are runnable | Exit 0 and one "<case-id>: valid" line per tracked case |
| Repository Python checks | python -m unittest discover -s scripts/tests -v | None beyond Python 3 | Exit 0 and final "OK" |

Task plans copy the exact commands relevant to their approved write paths. Do not claim an unrun command passed.
~~~

- [ ] **Step 7: Create the task-package router**

Create icm/tasks/CONTEXT.md with:

~~~markdown
# Task Packages

Each child directory is one durable task audit surface. Planning owns request.md, spec.md, plan.md, context-manifest.json, and approval.json. Building owns build/ and its run ledger, evidence, reviews, verification, and knowledge candidates.

Never reuse an approved package for another task or committed base. Historical task evidence records what happened; it is not current repository policy.

Task observations remain local knowledge candidates until the final user gate promotes them into an existing canonical repository source.
~~~

- [ ] **Step 8: Run the adapter checks to verify the green state**

Run:

~~~powershell
python -m unittest scripts.tests.test_check_icm_repository -v
python scripts/check-icm-repository.py
~~~

Expected: 8 checker tests run and OK; the checked-in adapter command exits 0 with "icm repository adapter: all checks passed".

- [ ] **Step 9: Verify and commit the adapter slice**

Run:

~~~powershell
git diff --check
git status --short
git add -- icm/CONTEXT.md icm/profile.json icm/knowledge/CONTEXT.md icm/checks/CONTEXT.md icm/tasks/CONTEXT.md scripts/tests/test_check_icm_repository.py
git diff --cached --check
git commit -m "feat: add central ICM repository adapter"
~~~

Expected: the staged diff contains exactly the five adapter files and the checked-in integration test; the commit succeeds.

---

### Task 3: Root Routing, Conventions, and Operator Documentation

**Files:**

- Modify: AGENTS.md:5-43
- Modify: CONTEXT.md:5-41
- Modify: _core/CONVENTIONS.md:5-18
- Modify: README.md:20-90

**Interfaces:**

- Consumes: icm/CONTEXT.md and the explicit central $plan-task and $build-task entrypoints.
- Produces: discoverable root routing, a canonical control-plane distinction, and an operator-facing lifecycle.
- Preserves: every existing task route, stage contract, install instruction, and lightweight correction path.

- [ ] **Step 1: Add ICM to the root map and routing gate**

In the AGENTS.md Folder Map, insert this line after CONTEXT.md:

~~~text
icm/                              Repository adapter for the central ICM lifecycle
~~~

In the AGENTS.md Routing table, insert this row before "Understand project structure":

~~~markdown
| Plan or build a nontrivial repository change | icm/CONTEXT.md, then explicit $plan-task or $build-task |
~~~

Append these operating rules before the existing Git-record rule:

~~~markdown
- Changes to the skill package, project architecture, scripts, evaluation protocols, tracked cases, or graders are nontrivial. Planning requires explicit $plan-task; implementation requires separate package approval and explicit $build-task.
- Small documentation and routing corrections that do not alter behavior or contracts may use the existing minimal workflow.
- Central ICM policy governs orchestration and external-action boundaries. Keep repository facts in their existing canonical files and do not vendor the central kernel.
~~~

- [ ] **Step 2: Route ICM work from the project context**

In the CONTEXT.md Task Routing table, insert this row before "Project conventions":

~~~markdown
| ICM planning and building | icm/CONTEXT.md | Full file | Route nontrivial changes through the central ICM lifecycle |
~~~

Replace the CONTEXT.md Process list with:

~~~markdown
1. Classify whether the request is a nontrivial repository change or a small non-behavioral documentation or routing correction.
2. For nontrivial work, read icm/CONTEXT.md and require the explicit central ICM planning, approval, and build gates.
3. Otherwise, read the routing row that matches the user request.
4. Load only the referenced sections or files.
5. Follow the relevant stage contract if the task changes files.
6. Verify changed artifacts before final response.
~~~

Add this row to the CONTEXT.md Outputs table:

~~~markdown
| ICM repository adapter and task packages | icm/ | Markdown, JSON, and task evidence |
~~~

- [ ] **Step 3: Define the control-plane relationship canonically**

Insert this section in _core/CONVENTIONS.md after the Five-Layer Context Model section and before Stage Contracts:

~~~markdown
## ICM Control Plane

The five-layer model controls what project context an agent reads. The repository icm/ adapter controls how nontrivial changes are planned, approved, built, evidenced, and reviewed through the separately maintained central ICM kernel.

Changes to the skill package, project architecture, scripts, evaluation protocols, tracked cases, or graders require explicit $plan-task, separate task-package approval, and explicit $build-task. Small documentation and routing corrections that do not alter behavior or contracts retain the minimal workflow.

Repository facts keep their existing canonical homes. The icm/ layer routes to those facts and stores task packages; it does not duplicate project knowledge or central kernel policy.
~~~

- [ ] **Step 4: Document the operator lifecycle**

In the README.md Repository Map, insert this line after CONTEXT.md:

~~~text
icm/                              Repository adapter and task records for central ICM
~~~

Insert this section before Development Workflow:

~~~markdown
## ICM Workflow

Nontrivial repository changes use the separately installed central ICM kernel. This repository contains only its repository-specific adapter; central contracts, policies, skills, templates, and validators remain in ICM-agentic-system.

Changes to the skill package, project architecture, scripts, evaluation protocols, tracked cases, or graders follow this lifecycle:

1. Explicitly invoke $plan-task with one change request.
2. Review the generated icm/tasks/<task-id>/ request, specification, plan, and context manifest.
3. In a later explicit $plan-task invocation, approve that unchanged task package.
4. Explicitly invoke $build-task with the approved task directory.
5. Inspect the resulting local commits, verification evidence, and independent review before separately deciding whether to integrate them.

Small documentation and routing corrections that do not alter behavior or contracts continue through the lightweight development workflow below. If the central kernel is unavailable or task approval is stale, stop rather than creating a repository-local fallback.
~~~

- [ ] **Step 5: Verify routing visibility and unchanged product scope**

Run:

~~~powershell
rg -n 'ICM|\$plan-task|\$build-task' AGENTS.md CONTEXT.md _core/CONVENTIONS.md README.md
git diff -- fable-task-harness evals workspaces
~~~

Expected: every root control surface exposes the ICM boundary; the second command prints no diff.

- [ ] **Step 6: Run the full acceptance suite**

Run:

~~~powershell
python scripts/check-icm-repository.py
python scripts/check-skill-package.py
python scripts/check-eval-cases.py
python -m unittest discover -s scripts/tests -v
git diff --check
~~~

Expected:

- ICM adapter checker exits 0.
- Skill package checker prints "fable-task-harness: all checks passed".
- Evaluation checker prints "decoy-config-repo: valid".
- unittest runs 32 tests and prints OK.
- Git whitespace check exits 0.

- [ ] **Step 7: Review scope and commit the routing slice**

Run:

~~~powershell
git status --short
git diff --stat
git diff -- AGENTS.md CONTEXT.md _core/CONVENTIONS.md README.md
git add -- AGENTS.md CONTEXT.md _core/CONVENTIONS.md README.md
git diff --cached --check
git commit -m "docs: route nontrivial work through ICM"
git status --short
~~~

Expected: the staged diff contains exactly the four root documentation files; after commit, the working tree is clean.

---

## Final Review Checklist

- [ ] The three implementation commits are narrowly scoped and ordered checker, adapter, then routing.
- [ ] icm/ contains only CONTEXT.md routers and profile.json; no contracts, policies, skills, templates, or validators were vendored.
- [ ] Existing project sources remain canonical and are routed by exact path.
- [ ] Nontrivial work requires explicit planning, approval, and building.
- [ ] Small non-behavioral documentation and routing corrections retain the minimal workflow.
- [ ] fable-task-harness version and contents are unchanged.
- [ ] evals/ and workspaces/ contents are unchanged.
- [ ] All four acceptance commands have fresh zero-exit evidence.
- [ ] The final working tree is clean.
