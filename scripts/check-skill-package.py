#!/usr/bin/env python3
"""Deterministic checks for a skill package.

Usage: python scripts/check-skill-package.py [skill-dir]

Defaults to fable-task-harness/. Exits non-zero on errors.

Errors:
- SKILL.md missing or missing frontmatter.
- Frontmatter does not parse as YAML (catches unquoted-colon descriptions).
- Missing required frontmatter fields: name, description, version.
- Frontmatter name does not match the skill folder name.
- Description over 1024 characters.
- A relative markdown link in any .md file does not resolve to a real file.

Warnings (reported, non-fatal):
- SKILL.md over 100 lines; reference or template files over 200 lines.
"""

import re
import sys
from pathlib import Path

REQUIRED_FIELDS = ("name", "description", "version")
MAX_DESCRIPTION = 1024
MAX_SKILL_LINES = 100
MAX_REFERENCE_LINES = 200
LINK_PATTERN = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")


def fail(msg: str) -> None:
    print(f"ERROR: {msg}")
    fail.count += 1


fail.count = 0


def warn(msg: str) -> None:
    print(f"warning: {msg}")


def check_frontmatter(skill_dir: Path) -> None:
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        fail(f"{skill_md} does not exist")
        return

    text = skill_md.read_text(encoding="utf-8")
    if not text.startswith("---"):
        fail("SKILL.md does not start with YAML frontmatter")
        return
    parts = text.split("---", 2)
    if len(parts) < 3:
        fail("SKILL.md frontmatter is not closed with ---")
        return

    try:
        import yaml
    except ImportError:
        fail("PyYAML is required: pip install pyyaml")
        return

    try:
        meta = yaml.safe_load(parts[1])
    except yaml.YAMLError as exc:
        fail(f"SKILL.md frontmatter is not valid YAML: {exc}")
        return

    if not isinstance(meta, dict):
        fail("SKILL.md frontmatter did not parse to a mapping")
        return

    for field in REQUIRED_FIELDS:
        if not meta.get(field):
            fail(f"SKILL.md frontmatter is missing required field: {field}")

    name = meta.get("name")
    if name and name != skill_dir.name:
        fail(f"frontmatter name {name!r} does not match folder name {skill_dir.name!r}")

    description = meta.get("description") or ""
    if len(description) > MAX_DESCRIPTION:
        fail(f"description is {len(description)} chars; max {MAX_DESCRIPTION}")


def check_links(skill_dir: Path) -> None:
    for md_file in sorted(skill_dir.rglob("*.md")):
        for match in LINK_PATTERN.finditer(md_file.read_text(encoding="utf-8")):
            target = match.group(1)
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            resolved = (md_file.parent / target.split("#")[0]).resolve()
            if not resolved.exists():
                rel = md_file.relative_to(skill_dir)
                fail(f"{rel}: broken relative link -> {target}")


def check_line_counts(skill_dir: Path) -> None:
    for md_file in sorted(skill_dir.rglob("*.md")):
        lines = len(md_file.read_text(encoding="utf-8").splitlines())
        rel = md_file.relative_to(skill_dir)
        if md_file.name == "SKILL.md" and lines > MAX_SKILL_LINES:
            warn(f"{rel} is {lines} lines; guidance is {MAX_SKILL_LINES}")
        elif md_file.name != "SKILL.md" and lines > MAX_REFERENCE_LINES:
            warn(f"{rel} is {lines} lines; guidance is {MAX_REFERENCE_LINES}")


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    skill_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else repo_root / "fable-task-harness"
    if not skill_dir.is_dir():
        print(f"ERROR: skill directory not found: {skill_dir}")
        return 1

    check_frontmatter(skill_dir)
    check_links(skill_dir)
    check_line_counts(skill_dir)

    if fail.count:
        print(f"\n{fail.count} error(s) in {skill_dir.name}")
        return 1
    print(f"\n{skill_dir.name}: all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
