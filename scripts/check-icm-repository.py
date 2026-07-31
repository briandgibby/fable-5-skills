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

    version = profile.get("profile_version")
    if not (type(version) is int and version == 1):
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
