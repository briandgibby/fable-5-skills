import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
CHECKER = REPO_ROOT / "scripts" / "check-eval-cases.py"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write_valid_case(cases_dir: Path) -> Path:
    case_dir = cases_dir / "sample-case"
    fixture_dir = case_dir / "fixture"
    fixture_dir.mkdir(parents=True)

    prompt = b"Do the sample task.\n"
    fixture = b"fixture content\n"
    (case_dir / "prompt.md").write_bytes(prompt)
    (case_dir / "grader.py").write_text("raise SystemExit(0)\n", encoding="utf-8")
    (case_dir / "test_grader.py").write_text(
        "import unittest\n\n"
        "class GraderTests(unittest.TestCase):\n"
        "    def test_grader(self):\n"
        "        self.assertTrue(True)\n",
        encoding="utf-8",
    )
    (fixture_dir / "input.txt").write_bytes(fixture)

    manifest = {
        "schema_version": 1,
        "id": "sample-case",
        "version": "1.0.0",
        "title": "Sample Case",
        "kind": "trap",
        "goal": "Exercise the tracked case contract.",
        "description": "A minimal valid case.",
        "prompt": {
            "path": "prompt.md",
            "hash_mode": "text-lf",
            "sha256": sha256_bytes(prompt),
            "placeholders": [],
        },
        "fixture": {
            "path": "fixture",
            "hash_mode": "text-lf",
            "files": {"input.txt": sha256_bytes(fixture)},
        },
        "grader": {
            "path": "grader.py",
            "tests": "test_grader.py",
            "args": ["--run-dir", "{run_dir}"],
            "result_schema_version": 1,
        },
        "golden": {
            "command": ["python", "sample.py"],
            "cwd": ".",
            "expected_exit_code": 0,
            "expected_stdout": "",
            "expected_stderr": "",
            "required_run_files": {
                "verification_notes": "verification.md",
                "run_metadata": "run-meta.md",
            },
            "allowed_fixture_changes": [],
            "ignored_generated_paths": [],
            "ground_truth_paths": [],
            "decoy_paths": [],
        },
        "receipts": [],
    }
    (case_dir / "case.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    return case_dir


class CheckEvalCasesTests(unittest.TestCase):
    def run_checker(
        self, cases_dir: Path, *, cwd: Path | None = None
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(CHECKER), "--cases-dir", str(cases_dir)],
            cwd=cwd,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_valid_case_passes(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            cases_dir = Path(temp_dir) / "cases"
            write_valid_case(cases_dir)

            result = self.run_checker(cases_dir)

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("sample-case: valid", result.stdout)

    def test_relative_cases_directory_runs_declared_grader_tests(self):
        with tempfile.TemporaryDirectory(dir=REPO_ROOT) as temp_dir:
            cases_dir = Path(temp_dir) / "cases"
            write_valid_case(cases_dir)
            relative_cases_dir = cases_dir.relative_to(REPO_ROOT)

            result = self.run_checker(relative_cases_dir, cwd=REPO_ROOT)

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("sample-case: valid", result.stdout)

    def test_manifest_id_must_match_directory(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            cases_dir = Path(temp_dir) / "cases"
            case_dir = write_valid_case(cases_dir)
            manifest_path = case_dir / "case.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["id"] = "different-id"
            manifest_path.write_text(
                json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
            )

            result = self.run_checker(cases_dir)

        self.assertEqual(result.returncode, 1)
        self.assertIn("id must match directory name", result.stderr)

    def test_required_manifest_fields_are_enforced(self):
        required_fields = (
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
        for field in required_fields:
            with self.subTest(field=field), tempfile.TemporaryDirectory() as temp_dir:
                cases_dir = Path(temp_dir) / "cases"
                case_dir = write_valid_case(cases_dir)
                manifest_path = case_dir / "case.json"
                manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
                del manifest[field]
                manifest_path.write_text(
                    json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
                )

                result = self.run_checker(cases_dir)

            self.assertEqual(result.returncode, 1)
            self.assertIn(f"missing required field: {field}", result.stderr)

    def test_schema_version_and_kind_are_constrained(self):
        mutations = (
            ("schema_version", 2, "schema_version must be 1"),
            ("kind", "unknown", "kind must be build or trap"),
            ("kind", [], "kind must be build or trap"),
            ("version", "", "version must be a non-empty string"),
        )
        for field, value, message in mutations:
            with self.subTest(field=field), tempfile.TemporaryDirectory() as temp_dir:
                cases_dir = Path(temp_dir) / "cases"
                case_dir = write_valid_case(cases_dir)
                manifest_path = case_dir / "case.json"
                manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
                manifest[field] = value
                manifest_path.write_text(
                    json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
                )

                result = self.run_checker(cases_dir)

            self.assertEqual(result.returncode, 1)
            self.assertIn(message, result.stderr)

    def test_referenced_paths_must_stay_inside_case_directory(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            cases_dir = Path(temp_dir) / "cases"
            case_dir = write_valid_case(cases_dir)
            outside_prompt = cases_dir / "outside.md"
            outside_prompt.write_text("outside\n", encoding="utf-8")
            manifest_path = case_dir / "case.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["prompt"]["path"] = "../outside.md"
            manifest_path.write_text(
                json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
            )

            result = self.run_checker(cases_dir)

        self.assertEqual(result.returncode, 1)
        self.assertIn("prompt.path must stay inside the case directory", result.stderr)

    def test_referenced_files_must_exist(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            cases_dir = Path(temp_dir) / "cases"
            case_dir = write_valid_case(cases_dir)
            (case_dir / "grader.py").unlink()

            result = self.run_checker(cases_dir)

        self.assertEqual(result.returncode, 1)
        self.assertIn("grader.path does not exist", result.stderr)

    def test_prompt_hash_must_match_normalized_text(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            cases_dir = Path(temp_dir) / "cases"
            case_dir = write_valid_case(cases_dir)
            (case_dir / "prompt.md").write_bytes(b"changed\r\nprompt\r\n")

            result = self.run_checker(cases_dir)

        self.assertEqual(result.returncode, 1)
        self.assertIn("prompt sha256 mismatch", result.stderr)

    def test_non_utf8_prompt_is_reported_without_a_traceback(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            cases_dir = Path(temp_dir) / "cases"
            case_dir = write_valid_case(cases_dir)
            (case_dir / "prompt.md").write_bytes(b"\xff\xfe")

            result = self.run_checker(cases_dir)

        self.assertEqual(result.returncode, 1)
        self.assertIn(
            "prompt is not valid UTF-8 for text-lf hashing", result.stderr
        )
        self.assertNotIn("Traceback", result.stderr)

    def test_fixture_inventory_rejects_unexpected_files(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            cases_dir = Path(temp_dir) / "cases"
            case_dir = write_valid_case(cases_dir)
            (case_dir / "fixture" / "unexpected.txt").write_text(
                "unexpected\n", encoding="utf-8"
            )

            result = self.run_checker(cases_dir)

        self.assertEqual(result.returncode, 1)
        self.assertIn("fixture file inventory mismatch", result.stderr)
        self.assertIn("unexpected.txt", result.stderr)

    def test_fixture_hashes_must_match(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            cases_dir = Path(temp_dir) / "cases"
            case_dir = write_valid_case(cases_dir)
            (case_dir / "fixture" / "input.txt").write_bytes(b"changed\r\n")

            result = self.run_checker(cases_dir)

        self.assertEqual(result.returncode, 1)
        self.assertIn("fixture sha256 mismatch: input.txt", result.stderr)

    def test_grader_args_must_include_run_dir_placeholder(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            cases_dir = Path(temp_dir) / "cases"
            case_dir = write_valid_case(cases_dir)
            manifest_path = case_dir / "case.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["grader"]["args"] = ["--run-dir", "fixed-path"]
            manifest_path.write_text(
                json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
            )

            result = self.run_checker(cases_dir)

        self.assertEqual(result.returncode, 1)
        self.assertIn("grader.args must contain {run_dir}", result.stderr)

    def test_receipt_paths_must_exist_inside_case_directory(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            cases_dir = Path(temp_dir) / "cases"
            case_dir = write_valid_case(cases_dir)
            manifest_path = case_dir / "case.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["receipts"] = ["receipts/missing.md"]
            manifest_path.write_text(
                json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
            )

            result = self.run_checker(cases_dir)

        self.assertEqual(result.returncode, 1)
        self.assertIn("receipts[0] does not exist", result.stderr)

    def test_declared_prompt_placeholders_must_match_prompt(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            cases_dir = Path(temp_dir) / "cases"
            case_dir = write_valid_case(cases_dir)
            manifest_path = case_dir / "case.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["prompt"]["placeholders"] = ["MISSING_PLACEHOLDER"]
            manifest_path.write_text(
                json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
            )

            result = self.run_checker(cases_dir)

        self.assertEqual(result.returncode, 1)
        self.assertIn("prompt placeholders mismatch", result.stderr)

    def test_golden_contract_requires_all_fields(self):
        required_golden_fields = (
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
        for field in required_golden_fields:
            with self.subTest(field=field), tempfile.TemporaryDirectory() as temp_dir:
                cases_dir = Path(temp_dir) / "cases"
                case_dir = write_valid_case(cases_dir)
                manifest_path = case_dir / "case.json"
                manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
                del manifest["golden"][field]
                manifest_path.write_text(
                    json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
                )

                result = self.run_checker(cases_dir)

            self.assertEqual(result.returncode, 1)
            self.assertIn(f"golden missing required field: {field}", result.stderr)

    def test_golden_cwd_must_be_a_contained_fixture_directory(self):
        mutations = (
            ("..", "must be a safe relative directory inside fixture"),
            ("missing", "does not exist inside fixture"),
            ("input.txt", "is not a directory inside fixture"),
        )
        for value, message in mutations:
            with self.subTest(value=value), tempfile.TemporaryDirectory() as temp_dir:
                cases_dir = Path(temp_dir) / "cases"
                case_dir = write_valid_case(cases_dir)
                manifest_path = case_dir / "case.json"
                manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
                manifest["golden"]["cwd"] = value
                manifest_path.write_text(
                    json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
                )

                result = self.run_checker(cases_dir)

            self.assertEqual(result.returncode, 1)
            self.assertIn(message, result.stderr)

    def test_golden_command_must_be_a_non_empty_string_list(self):
        mutations = ("python sample.py", [], ["python", 3])
        for value in mutations:
            with self.subTest(value=value), tempfile.TemporaryDirectory() as temp_dir:
                cases_dir = Path(temp_dir) / "cases"
                case_dir = write_valid_case(cases_dir)
                manifest_path = case_dir / "case.json"
                manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
                manifest["golden"]["command"] = value
                manifest_path.write_text(
                    json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
                )

                result = self.run_checker(cases_dir)

            self.assertEqual(result.returncode, 1)
            self.assertIn(
                "golden.command must be a non-empty list of strings", result.stderr
            )

    def test_golden_expected_results_have_runtime_types(self):
        mutations = (
            (
                "expected_exit_code",
                "0",
                "golden.expected_exit_code must be an integer",
            ),
            (
                "expected_exit_code",
                True,
                "golden.expected_exit_code must be an integer",
            ),
            ("expected_stdout", 3, "golden.expected_stdout must be a string"),
            ("expected_stderr", [], "golden.expected_stderr must be a string"),
        )
        for field, value, message in mutations:
            with self.subTest(field=field, value=value), tempfile.TemporaryDirectory() as temp_dir:
                cases_dir = Path(temp_dir) / "cases"
                case_dir = write_valid_case(cases_dir)
                manifest_path = case_dir / "case.json"
                manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
                manifest["golden"][field] = value
                manifest_path.write_text(
                    json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
                )

                result = self.run_checker(cases_dir)

            self.assertEqual(result.returncode, 1)
            self.assertIn(message, result.stderr)

    def test_golden_run_paths_and_ignore_patterns_must_be_safe(self):
        mutations = (
            (
                "required_run_files",
                {
                    "verification_notes": "../verification.md",
                    "run_metadata": "run-meta.md",
                },
                "golden.required_run_files.verification_notes must be a safe relative path",
            ),
            (
                "required_run_files",
                {"verification_notes": "verification.md"},
                "golden.required_run_files must contain exactly verification_notes and run_metadata",
            ),
            (
                "ignored_generated_paths",
                ["../**/*.pyc"],
                "golden.ignored_generated_paths[0] must be a safe relative pattern",
            ),
            (
                "ignored_generated_paths",
                "**/*.pyc",
                "golden.ignored_generated_paths must be a list of relative patterns",
            ),
        )
        for field, value, message in mutations:
            with self.subTest(field=field, value=value), tempfile.TemporaryDirectory() as temp_dir:
                cases_dir = Path(temp_dir) / "cases"
                case_dir = write_valid_case(cases_dir)
                manifest_path = case_dir / "case.json"
                manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
                manifest["golden"][field] = value
                manifest_path.write_text(
                    json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
                )

                result = self.run_checker(cases_dir)

            self.assertEqual(result.returncode, 1)
            self.assertIn(message, result.stderr)

    def test_ground_truth_and_decoy_paths_must_name_fixture_files(self):
        mutations = (
            ("ground_truth_paths", ["../escape.py"], "must be a safe relative path"),
            ("decoy_paths", ["missing.txt"], "is not in fixture.files"),
        )
        for field, value, message in mutations:
            with self.subTest(field=field), tempfile.TemporaryDirectory() as temp_dir:
                cases_dir = Path(temp_dir) / "cases"
                case_dir = write_valid_case(cases_dir)
                manifest_path = case_dir / "case.json"
                manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
                manifest["golden"][field] = value
                manifest_path.write_text(
                    json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
                )

                result = self.run_checker(cases_dir)

            self.assertEqual(result.returncode, 1)
            self.assertIn(message, result.stderr)

    def test_case_grader_tests_must_pass(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            cases_dir = Path(temp_dir) / "cases"
            case_dir = write_valid_case(cases_dir)
            (case_dir / "test_grader.py").write_text(
                "import unittest\n\n"
                "class GraderTests(unittest.TestCase):\n"
                "    def test_grader(self):\n"
                "        self.fail('known failure')\n",
                encoding="utf-8",
            )

            result = self.run_checker(cases_dir)

        self.assertEqual(result.returncode, 1)
        self.assertIn("grader tests failed", result.stderr)

    def test_declared_grader_test_file_must_discover_a_test(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            cases_dir = Path(temp_dir) / "cases"
            case_dir = write_valid_case(cases_dir)
            (case_dir / "test_grader.py").write_text(
                "# Intentionally contains no tests.\n", encoding="utf-8"
            )

            result = self.run_checker(cases_dir)

        self.assertEqual(result.returncode, 1)
        self.assertIn("no grader tests discovered", result.stderr)

    def test_declared_nested_grader_test_cannot_be_shadowed_by_root_test(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            cases_dir = Path(temp_dir) / "cases"
            case_dir = write_valid_case(cases_dir)
            nested_tests = case_dir / "tests"
            nested_tests.mkdir()
            (nested_tests / "test_grader.py").write_text(
                "import unittest\n\n"
                "class GraderTests(unittest.TestCase):\n"
                "    def test_grader(self):\n"
                "        self.fail('declared nested failure')\n",
                encoding="utf-8",
            )
            manifest_path = case_dir / "case.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["grader"]["tests"] = "tests/test_grader.py"
            manifest_path.write_text(
                json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
            )

            result = self.run_checker(cases_dir)

        self.assertEqual(result.returncode, 1)
        self.assertIn("grader tests failed", result.stderr)
        self.assertIn("declared nested failure", result.stderr)

    def test_allowed_fixture_changes_require_known_paths_and_statuses(self):
        mutations = (
            (
                [{"path": "input.txt", "status": "changed"}],
                "status must be added, modified, or removed",
            ),
            (
                [{"path": "input.txt", "status": []}],
                "status must be added, modified, or removed",
            ),
            (
                [{"path": "missing.txt", "status": "modified"}],
                "path is not in fixture.files",
            ),
        )
        for value, message in mutations:
            with self.subTest(value=value), tempfile.TemporaryDirectory() as temp_dir:
                cases_dir = Path(temp_dir) / "cases"
                case_dir = write_valid_case(cases_dir)
                manifest_path = case_dir / "case.json"
                manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
                manifest["golden"]["allowed_fixture_changes"] = value
                manifest_path.write_text(
                    json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
                )

                result = self.run_checker(cases_dir)

            self.assertEqual(result.returncode, 1)
            self.assertIn(message, result.stderr)


if __name__ == "__main__":
    unittest.main()
