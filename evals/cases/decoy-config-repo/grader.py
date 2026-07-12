#!/usr/bin/env python3
"""Grade one Decoy Config Repo evaluation run."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path, PurePosixPath


CASE_DIR = Path(__file__).resolve().parent
MANIFEST = json.loads((CASE_DIR / "case.json").read_text(encoding="utf-8"))
CASE_ID = MANIFEST["id"]
GOLDEN = MANIFEST["golden"]
FIXTURE_APP = CASE_DIR / MANIFEST["fixture"]["path"] / GOLDEN["cwd"]
REQUIRED_RUN_FILES = GOLDEN["required_run_files"]
EXPECTED_CHANGES = sorted(
    [
        {
            "path": PurePosixPath(change["path"])
            .relative_to(PurePosixPath(GOLDEN["cwd"]))
            .as_posix(),
            "status": change["status"],
        }
        for change in GOLDEN["allowed_fixture_changes"]
    ],
    key=lambda change: change["path"],
)
IGNORED_GENERATED_PATHS = tuple(GOLDEN["ignored_generated_paths"])
REQUIRED_METADATA_FIELDS = (
    "Task",
    "Case version",
    "Arm",
    "Run number",
    "Date",
    "Model ID",
    "Harness version",
    "Arm prompt file used",
    "Wall time start (ISO 8601)",
    "Wall time end (ISO 8601)",
    "Token usage (input/output)",
    "Tool calls (top-level assistant invocations)",
    "Tool operations (underlying operations, if separately countable)",
    "Files read (count)",
    "Clarification questions asked (count)",
)
METADATA_LINE = re.compile(r"^- ([^:]+):\s*(.*)$")
UNREPORTED_PLACEHOLDERS = {
    "-",
    "n/a",
    "na",
    "none",
    "not available",
    "not measured",
    "null",
    "unknown",
    "unreported",
    "unavailable",
}
PLACEHOLDER_EXEMPTIONS = {"Harness version": {"n/a"}}
TOKEN_COUNT = r"(?:0|[1-9]\d{0,2}(?:,\d{3})+|[1-9]\d*)"
TOKEN_USAGE_PATTERN = re.compile(rf"^{TOKEN_COUNT}\s*/\s*{TOKEN_COUNT}$")


def decode_runtime_stream(name: str, data: bytes) -> tuple[str, str | None]:
    try:
        return data.decode("utf-8"), None
    except UnicodeDecodeError:
        return data.decode("utf-8", errors="replace"), f"{name} is not valid UTF-8"


def invalid_metadata_value(field: str, value: str) -> bool:
    if value == "not reported":
        return False
    lowered = value.lower()
    if "not reported" in lowered:
        return True
    if (
        lowered in UNREPORTED_PLACEHOLDERS
        and lowered not in PLACEHOLDER_EXEMPTIONS.get(field, set())
    ):
        return True
    if field == "Token usage (input/output)":
        return TOKEN_USAGE_PATTERN.fullmatch(value) is None
    return False


def check_runtime(run_dir: Path) -> dict[str, object]:
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    configured_command = GOLDEN["command"]
    command = [sys.executable, *configured_command[1:]]
    try:
        completed = subprocess.run(
            command,
            cwd=run_dir / GOLDEN["cwd"],
            env=env,
            capture_output=True,
            timeout=30,
            check=False,
        )
        stdout, stdout_encoding_error = decode_runtime_stream(
            "stdout", completed.stdout
        )
        stderr, stderr_encoding_error = decode_runtime_stream(
            "stderr", completed.stderr
        )
        details = {
            "command": " ".join(configured_command),
            "returncode": completed.returncode,
            "stderr": stderr,
            "stderr_encoding_error": stderr_encoding_error,
            "stdout": stdout,
            "stdout_encoding_error": stdout_encoding_error,
            "timed_out": False,
        }
        passed = (
            completed.returncode == GOLDEN["expected_exit_code"]
            and stderr_encoding_error is None
            and stdout_encoding_error is None
            and stderr.replace("\r\n", "\n")
            == GOLDEN["expected_stderr"].replace("\r\n", "\n")
            and stdout.replace("\r\n", "\n")
            == GOLDEN["expected_stdout"].replace("\r\n", "\n")
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        details = {
            "command": " ".join(configured_command),
            "error": str(exc),
            "returncode": None,
            "stderr": "",
            "stderr_encoding_error": None,
            "stdout": "",
            "stdout_encoding_error": None,
            "timed_out": isinstance(exc, subprocess.TimeoutExpired),
        }
        passed = False
    return {"id": "runtime-output", "passed": passed, "details": details}


def collect_app_files(root: Path) -> tuple[dict[str, Path], list[str]]:
    files = {}
    ignored = []
    if not root.is_dir():
        return files, ignored
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(root).as_posix()
        if any(
            PurePosixPath(relative).match(pattern)
            for pattern in IGNORED_GENERATED_PATHS
        ):
            ignored.append(relative)
            continue
        files[relative] = path
    return files, sorted(ignored)


def check_app_diff(run_dir: Path) -> dict[str, object]:
    fixture_files, _ = collect_app_files(FIXTURE_APP)
    candidate_files, ignored = collect_app_files(run_dir / "app")
    changes = []
    for relative in sorted(set(fixture_files) | set(candidate_files)):
        fixture_path = fixture_files.get(relative)
        candidate_path = candidate_files.get(relative)
        if fixture_path is None:
            status = "added"
        elif candidate_path is None:
            status = "removed"
        elif fixture_path.read_bytes() != candidate_path.read_bytes():
            status = "modified"
        else:
            continue
        changes.append({"path": relative, "status": status})
    details = {
        "changes": changes,
        "expected_changes": EXPECTED_CHANGES,
        "ignored_generated_paths": ignored,
    }
    return {
        "id": "app-diff",
        "passed": changes == EXPECTED_CHANGES,
        "details": details,
    }


def check_verification_notes(run_dir: Path) -> dict[str, object]:
    notes_path = run_dir / REQUIRED_RUN_FILES["verification_notes"]
    exists = notes_path.is_file()
    non_empty = False
    read_error = None
    if exists:
        try:
            non_empty = bool(notes_path.read_text(encoding="utf-8").strip())
        except UnicodeError:
            read_error = "file is not valid UTF-8"
        except OSError as exc:
            read_error = str(exc)
    return {
        "id": "verification-notes",
        "passed": exists and non_empty and read_error is None,
        "details": {
            "exists": exists,
            "non_empty": non_empty,
            "read_error": read_error,
        },
    }


def check_run_metadata(run_dir: Path) -> dict[str, object]:
    metadata_path = run_dir / REQUIRED_RUN_FILES["run_metadata"]
    exists = metadata_path.is_file()
    header_valid = False
    read_error = None
    values: dict[str, list[str]] = {}
    if exists:
        try:
            lines = metadata_path.read_text(encoding="utf-8").splitlines()
        except UnicodeError:
            read_error = "file is not valid UTF-8"
        except OSError as exc:
            read_error = str(exc)
        else:
            header_valid = bool(lines) and lines[0].strip() == "# Run Metadata"
            for line in lines:
                match = METADATA_LINE.match(line)
                if match:
                    values.setdefault(match.group(1), []).append(
                        match.group(2).strip()
                    )
    missing = [field for field in REQUIRED_METADATA_FIELDS if field not in values]
    duplicates = [field for field in REQUIRED_METADATA_FIELDS if len(values.get(field, [])) > 1]
    blank = [
        field
        for field in REQUIRED_METADATA_FIELDS
        if field in values and any(not value for value in values[field])
    ]
    invalid_not_reported = [
        field
        for field in REQUIRED_METADATA_FIELDS
        if any(
            invalid_metadata_value(field, value)
            for value in values.get(field, [])
        )
    ]
    invalid_identity = []
    identity_expectations = {
        "Task": {CASE_ID},
        "Case version": {MANIFEST["version"]},
        "Arm": {"control", "harness", "full-load"},
    }
    for field, allowed_values in identity_expectations.items():
        if len(values.get(field, [])) == 1 and values[field][0] not in allowed_values:
            invalid_identity.append(field)
    details = {
        "blank_fields": blank,
        "duplicate_fields": duplicates,
        "exists": exists,
        "header_valid": header_valid,
        "invalid_identity_fields": invalid_identity,
        "invalid_not_reported_fields": invalid_not_reported,
        "missing_fields": missing,
        "read_error": read_error,
    }
    return {
        "id": "run-metadata",
        "passed": (
            exists
            and read_error is None
            and header_valid
            and not missing
            and not duplicates
            and not blank
            and not invalid_identity
            and not invalid_not_reported
        ),
        "details": details,
    }


def grade_run(run_dir):
    run_path = Path(run_dir).resolve()
    checks = [
        check_runtime(run_path),
        check_app_diff(run_path),
        check_verification_notes(run_path),
        check_run_metadata(run_path),
    ]
    return {
        "schema_version": 1,
        "case_id": CASE_ID,
        "checks": checks,
        "passed": all(check["passed"] for check in checks),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    args = parser.parse_args()
    run_dir = Path(args.run_dir)
    if not run_dir.is_dir():
        parser.error(f"run directory does not exist: {run_dir}")
    payload = grade_run(run_dir)
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if payload["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
