#!/usr/bin/env python3
"""Validate tracked evaluation case modules."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path


REQUIRED_FIELDS = (
    "schema_version",
    "id",
    "version",
    "title",
    "kind",
    "goal",
    "prompt",
    "fixture",
    "grader",
    "golden",
    "receipts",
)
PLACEHOLDER_PATTERN = re.compile(r"\{([A-Z][A-Z0-9_]*)\}")
REQUIRED_GOLDEN_FIELDS = (
    "command",
    "cwd",
    "expected_exit_code",
    "expected_stdout",
    "expected_stderr",
    "required_run_files",
    "allowed_fixture_changes",
    "ignored_generated_paths",
    "ground_truth_paths",
    "decoy_paths",
)
REQUIRED_RUN_FILE_KEYS = {"verification_notes", "run_metadata"}


def validate_reference_path(
    case_dir: Path, label: str, value: object, *, directory: bool = False
) -> tuple[Path | None, list[str]]:
    if not isinstance(value, str) or not value:
        return None, [f"{label} must be a non-empty relative path"]
    relative = Path(value)
    if relative.is_absolute() or ".." in relative.parts:
        return None, [f"{label} must stay inside the case directory"]
    resolved = (case_dir / relative).resolve()
    try:
        resolved.relative_to(case_dir.resolve())
    except ValueError:
        return None, [f"{label} must stay inside the case directory"]
    exists = resolved.is_dir() if directory else resolved.is_file()
    if not exists:
        return None, [f"{label} does not exist"]
    return resolved, []


def file_sha256(path: Path, mode: object) -> tuple[str | None, str | None]:
    data = path.read_bytes()
    if mode == "raw":
        normalized = data
    elif mode == "text-lf":
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            return None, "is not valid UTF-8 for text-lf hashing"
        normalized = text.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")
    else:
        return None, "hash_mode must be raw or text-lf"
    return hashlib.sha256(normalized).hexdigest(), None


def is_safe_relative_path(value: object) -> bool:
    if not isinstance(value, str) or not value:
        return False
    path = Path(value)
    return not path.is_absolute() and ".." not in path.parts


def validate_case(case_file: Path, manifest: object) -> list[str]:
    if not isinstance(manifest, dict):
        return ["manifest must be a JSON object"]
    missing = [field for field in REQUIRED_FIELDS if field not in manifest]
    if missing:
        return [f"missing required field: {field}" for field in missing]
    errors = []
    if manifest["schema_version"] != 1:
        errors.append("schema_version must be 1")
    if manifest.get("id") != case_file.parent.name:
        errors.append("id must match directory name")
    if not isinstance(manifest["version"], str) or not manifest["version"].strip():
        errors.append("version must be a non-empty string")
    if not isinstance(manifest["kind"], str) or manifest["kind"] not in {
        "build",
        "trap",
    }:
        errors.append("kind must be build or trap")
    resolved_paths: dict[str, Path] = {}
    reference_sections = (("prompt", False), ("fixture", True), ("grader", False))
    for section_name, directory in reference_sections:
        section = manifest[section_name]
        if not isinstance(section, dict):
            errors.append(f"{section_name} must be an object")
            continue
        resolved, path_errors = validate_reference_path(
            case_file.parent,
            f"{section_name}.path",
            section.get("path"),
            directory=directory,
        )
        errors.extend(path_errors)
        if resolved is not None:
            resolved_paths[section_name] = resolved
    prompt = manifest["prompt"]
    if isinstance(prompt, dict) and "prompt" in resolved_paths:
        actual_hash, hash_error = file_sha256(
            resolved_paths["prompt"], prompt.get("hash_mode")
        )
        if hash_error:
            errors.append(f"prompt {hash_error}")
        elif prompt.get("sha256") != actual_hash:
            errors.append("prompt sha256 mismatch")
        declared_placeholders = prompt.get("placeholders")
        if not isinstance(declared_placeholders, list) or not all(
            isinstance(item, str) for item in declared_placeholders
        ):
            errors.append("prompt.placeholders must be a list of strings")
        else:
            try:
                prompt_text = resolved_paths["prompt"].read_text(encoding="utf-8")
            except UnicodeDecodeError:
                if hash_error is None:
                    errors.append("prompt is not valid UTF-8")
            else:
                actual_placeholders = sorted(
                    set(PLACEHOLDER_PATTERN.findall(prompt_text))
                )
                if sorted(set(declared_placeholders)) != actual_placeholders:
                    errors.append(
                        "prompt placeholders mismatch: "
                        f"declared={sorted(set(declared_placeholders))}, "
                        f"actual={actual_placeholders}"
                    )
    fixture = manifest["fixture"]
    fixture_inventory: set[str] = set()
    if isinstance(fixture, dict) and "fixture" in resolved_paths:
        expected_files = fixture.get("files")
        if not isinstance(expected_files, dict):
            errors.append("fixture.files must be an object")
        else:
            fixture_inventory = set(expected_files)
            actual_files = {
                path.relative_to(resolved_paths["fixture"]).as_posix(): path
                for path in resolved_paths["fixture"].rglob("*")
                if path.is_file()
            }
            expected_names = set(expected_files)
            actual_names = set(actual_files)
            if expected_names != actual_names:
                missing_files = sorted(expected_names - actual_names)
                unexpected_files = sorted(actual_names - expected_names)
                errors.append(
                    "fixture file inventory mismatch: "
                    f"missing={missing_files}, unexpected={unexpected_files}"
                )
            for relative in sorted(expected_names & actual_names):
                actual_hash, hash_error = file_sha256(
                    actual_files[relative], fixture.get("hash_mode")
                )
                if hash_error:
                    errors.append(f"fixture {relative} {hash_error}")
                elif expected_files[relative] != actual_hash:
                    errors.append(f"fixture sha256 mismatch: {relative}")
    grader = manifest["grader"]
    if isinstance(grader, dict):
        _, grader_test_errors = validate_reference_path(
            case_file.parent, "grader.tests", grader.get("tests")
        )
        errors.extend(grader_test_errors)
        grader_args = grader.get("args")
        if not isinstance(grader_args, list) or not all(
            isinstance(arg, str) for arg in grader_args
        ):
            errors.append("grader.args must be a list of strings")
        elif "{run_dir}" not in grader_args:
            errors.append("grader.args must contain {run_dir}")
    receipts = manifest["receipts"]
    if not isinstance(receipts, list):
        errors.append("receipts must be a list of relative paths")
    else:
        for index, receipt in enumerate(receipts):
            _, receipt_errors = validate_reference_path(
                case_file.parent, f"receipts[{index}]", receipt
            )
            errors.extend(receipt_errors)
    golden = manifest["golden"]
    if not isinstance(golden, dict):
        errors.append("golden must be an object")
    else:
        for field in REQUIRED_GOLDEN_FIELDS:
            if field not in golden:
                errors.append(f"golden missing required field: {field}")
        if "command" in golden:
            command = golden["command"]
            if (
                not isinstance(command, list)
                or not command
                or not all(isinstance(part, str) and part for part in command)
            ):
                errors.append("golden.command must be a non-empty list of strings")
        if "expected_exit_code" in golden and (
            not isinstance(golden["expected_exit_code"], int)
            or isinstance(golden["expected_exit_code"], bool)
        ):
            errors.append("golden.expected_exit_code must be an integer")
        for field in ("expected_stdout", "expected_stderr"):
            if field in golden and not isinstance(golden[field], str):
                errors.append(f"golden.{field} must be a string")
        if "cwd" in golden:
            cwd = golden["cwd"]
            if not is_safe_relative_path(cwd):
                errors.append(
                    "golden.cwd must be a safe relative directory inside fixture"
                )
            elif "fixture" in resolved_paths:
                fixture_root = resolved_paths["fixture"].resolve()
                resolved_cwd = (fixture_root / cwd).resolve()
                try:
                    resolved_cwd.relative_to(fixture_root)
                except ValueError:
                    errors.append(
                        "golden.cwd must be a safe relative directory inside fixture"
                    )
                else:
                    if not resolved_cwd.exists():
                        errors.append("golden.cwd does not exist inside fixture")
                    elif not resolved_cwd.is_dir():
                        errors.append("golden.cwd is not a directory inside fixture")
        required_run_files = golden.get("required_run_files")
        if required_run_files is not None:
            if not isinstance(required_run_files, dict):
                errors.append(
                    "golden.required_run_files must be an object"
                )
            elif set(required_run_files) != REQUIRED_RUN_FILE_KEYS:
                errors.append(
                    "golden.required_run_files must contain exactly "
                    "verification_notes and run_metadata"
                )
            else:
                for name, value in required_run_files.items():
                    if not is_safe_relative_path(value):
                        errors.append(
                            f"golden.required_run_files.{name} "
                            "must be a safe relative path"
                        )
        ignored_patterns = golden.get("ignored_generated_paths")
        if ignored_patterns is not None:
            if not isinstance(ignored_patterns, list) or not all(
                isinstance(value, str) for value in ignored_patterns
            ):
                errors.append(
                    "golden.ignored_generated_paths must be a list of relative patterns"
                )
            else:
                for index, value in enumerate(ignored_patterns):
                    if not is_safe_relative_path(value):
                        errors.append(
                            "golden.ignored_generated_paths"
                            f"[{index}] must be a safe relative pattern"
                        )
        for field in ("ground_truth_paths", "decoy_paths"):
            values = golden.get(field)
            if values is None:
                continue
            if not isinstance(values, list) or not all(
                isinstance(value, str) for value in values
            ):
                errors.append(f"golden.{field} must be a list of relative paths")
                continue
            for index, value in enumerate(values):
                if not is_safe_relative_path(value):
                    errors.append(
                        f"golden.{field}[{index}] must be a safe relative path"
                    )
                elif value not in fixture_inventory:
                    errors.append(f"golden.{field}[{index}] is not in fixture.files")
        allowed_changes = golden.get("allowed_fixture_changes")
        if allowed_changes is not None:
            if not isinstance(allowed_changes, list):
                errors.append("golden.allowed_fixture_changes must be a list")
            else:
                for index, change in enumerate(allowed_changes):
                    label = f"golden.allowed_fixture_changes[{index}]"
                    if not isinstance(change, dict):
                        errors.append(f"{label} must be an object")
                        continue
                    path = change.get("path")
                    status = change.get("status")
                    if not is_safe_relative_path(path):
                        errors.append(f"{label}.path must be a safe relative path")
                    if not isinstance(status, str) or status not in {
                        "added",
                        "modified",
                        "removed",
                    }:
                        errors.append(
                            f"{label}.status must be added, modified, or removed"
                        )
                    elif (
                        status in {"modified", "removed"}
                        and path not in fixture_inventory
                    ):
                        errors.append(f"{label}.path is not in fixture.files")
    return errors


def run_grader_tests(case_dir: Path, test_file: str) -> subprocess.CompletedProcess[str]:
    case_dir = case_dir.resolve()
    test_path = (case_dir / test_file).resolve()
    return subprocess.run(
        [
            sys.executable,
            "-m",
            "unittest",
            "discover",
            "-s",
            str(test_path.parent),
            "-p",
            test_path.name,
            "-v",
        ],
        cwd=case_dir,
        text=True,
        capture_output=True,
        check=False,
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    default_cases = Path(__file__).resolve().parents[1] / "evals" / "cases"
    parser.add_argument("--cases-dir", type=Path, default=default_cases)
    args = parser.parse_args()

    case_files = sorted(args.cases_dir.glob("*/case.json"))
    if not case_files:
        print(f"ERROR: no case.json files found under {args.cases_dir}", file=sys.stderr)
        return 1

    failed = False
    for case_file in case_files:
        try:
            manifest = json.loads(case_file.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            print(f"ERROR: {case_file}: {exc}", file=sys.stderr)
            failed = True
            continue
        errors = validate_case(case_file, manifest)
        if errors:
            failed = True
            for error in errors:
                print(f"ERROR: {case_file.parent.name}: {error}", file=sys.stderr)
            continue
        test_result = run_grader_tests(case_file.parent, manifest["grader"]["tests"])
        test_output = f"{test_result.stdout}\n{test_result.stderr}"
        no_tests = bool(
            re.search(r"\bRan 0 tests?\b|\bNO TESTS RAN\b", test_output)
        )
        if test_result.returncode != 0 or no_tests:
            failed = True
            print(
                f"ERROR: {case_file.parent.name}: grader tests failed",
                file=sys.stderr,
            )
            if no_tests:
                print(
                    f"ERROR: {case_file.parent.name}: no grader tests discovered",
                    file=sys.stderr,
                )
            if test_result.stdout:
                print(test_result.stdout.rstrip(), file=sys.stderr)
            if test_result.stderr:
                print(test_result.stderr.rstrip(), file=sys.stderr)
            continue
        print(f"{manifest.get('id', case_file.parent.name)}: valid")

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
