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

    def test_profile_version_must_be_integer_one(self):
        for value in (True, 1.0):
            with self.subTest(value=value), tempfile.TemporaryDirectory() as temp_dir:
                repo_root = Path(temp_dir)
                write_valid_repository(repo_root)
                profile = valid_profile()
                profile["profile_version"] = value
                write_profile(repo_root, profile)

                result = self.run_checker(repo_root)

            self.assertEqual(result.returncode, 1)
            self.assertIn("profile_version must be 1", result.stderr)

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

    def test_checked_in_repository_passes(self):
        result = self.run_checker(REPO_ROOT)

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("icm repository adapter: all checks passed", result.stdout)


if __name__ == "__main__":
    unittest.main()
