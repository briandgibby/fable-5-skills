import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


CASE_DIR = Path(__file__).resolve().parent
FIXTURE_APP = CASE_DIR / "fixture" / "app"
GRADER = CASE_DIR / "grader.py"
CHECK_IDS = ("runtime-output", "app-diff", "verification-notes", "run-metadata")


VALID_METADATA = """# Run Metadata

- Task: decoy-config-repo
- Case version: 1.0.0
- Arm: control
- Run number: 1
- Date: 2026-07-10
- Model ID: test-model
- Harness version: n/a
- Arm prompt file used: evals/arm-prompts/control.md
- Wall time start (ISO 8601): 2026-07-10T12:00:00-04:00
- Wall time end (ISO 8601): 2026-07-10T12:01:00-04:00
- Token usage (input/output): not reported
- Tool calls (top-level assistant invocations): 3
- Tool operations (underlying operations, if separately countable): 4
- Files read (count): 2
- Clarification questions asked (count): 0
"""


class DecoyConfigGraderTests(unittest.TestCase):
    def make_valid_run(self) -> Path:
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)
        run_dir = Path(temp_dir.name) / "run"
        shutil.copytree(FIXTURE_APP, run_dir / "app")
        defaults = run_dir / "app" / "src" / "defaults.py"
        defaults.write_text(
            defaults.read_text(encoding="utf-8").replace(
                '"request_timeout_seconds": 10', '"request_timeout_seconds": 30'
            ),
            encoding="utf-8",
        )
        (run_dir / "verification.md").write_text(
            "Verified the live client reports a 30-second timeout.\n", encoding="utf-8"
        )
        (run_dir / "run-meta.md").write_text(VALID_METADATA, encoding="utf-8")
        return run_dir

    def run_grader(
        self, run_dir: Path, grader: Path = GRADER
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(grader), "--run-dir", str(run_dir)],
            text=True,
            capture_output=True,
            check=False,
        )

    def test_valid_run_exits_zero_and_reports_all_checks_passed(self):
        result = self.run_grader(self.make_valid_run())

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, "")
        payload = json.loads(result.stdout)
        self.assertEqual(payload["schema_version"], 1)
        self.assertEqual(payload["case_id"], "decoy-config-repo")
        self.assertTrue(payload["passed"])
        self.assertEqual(tuple(check["id"] for check in payload["checks"]), CHECK_IDS)
        self.assertTrue(all(check["passed"] for check in payload["checks"]))

    def test_runtime_output_must_match_the_entire_expected_line(self):
        run_dir = self.make_valid_run()
        defaults = run_dir / "app" / "src" / "defaults.py"
        defaults.write_text(
            defaults.read_text(encoding="utf-8").replace('"retries": 2', '"retries": 99'),
            encoding="utf-8",
        )

        result = self.run_grader(run_dir)
        payload = json.loads(result.stdout)
        checks = {check["id"]: check for check in payload["checks"]}

        self.assertEqual(result.returncode, 1)
        self.assertFalse(payload["passed"])
        self.assertFalse(checks["runtime-output"]["passed"])
        self.assertTrue(checks["app-diff"]["passed"])
        self.assertIn("timeout=30s", checks["runtime-output"]["details"]["stdout"])

    def test_non_utf8_runtime_output_returns_a_structured_failure(self):
        run_dir = self.make_valid_run()
        client = run_dir / "app" / "src" / "client.py"
        client.write_text(
            "import sys\nsys.stdout.buffer.write(bytes([255]))\n", encoding="utf-8"
        )

        result = self.run_grader(run_dir)
        payload = json.loads(result.stdout)
        check = next(
            item for item in payload["checks"] if item["id"] == "runtime-output"
        )

        self.assertEqual(result.returncode, 1)
        self.assertFalse(check["passed"])
        self.assertEqual(
            check["details"]["stdout_encoding_error"],
            "stdout is not valid UTF-8",
        )

    def test_app_diff_requires_only_src_defaults_modified(self):
        run_dir = self.make_valid_run()
        settings = run_dir / "app" / "config" / "settings.json"
        settings.write_text(
            settings.read_text(encoding="utf-8").replace(
                '"request_timeout_seconds": 10', '"request_timeout_seconds": 30'
            ),
            encoding="utf-8",
        )

        result = self.run_grader(run_dir)
        payload = json.loads(result.stdout)
        checks = {check["id"]: check for check in payload["checks"]}

        self.assertEqual(result.returncode, 1)
        self.assertTrue(checks["runtime-output"]["passed"])
        self.assertFalse(checks["app-diff"]["passed"])
        self.assertEqual(
            checks["app-diff"]["details"]["changes"],
            [
                {"path": "config/settings.json", "status": "modified"},
                {"path": "src/defaults.py", "status": "modified"},
            ],
        )

    def test_verification_notes_must_exist_at_run_root_and_be_nonblank(self):
        for mode in ("missing", "blank"):
            with self.subTest(mode=mode):
                run_dir = self.make_valid_run()
                notes = run_dir / "verification.md"
                if mode == "missing":
                    notes.unlink()
                else:
                    notes.write_text("  \n", encoding="utf-8")

                result = self.run_grader(run_dir)
                payload = json.loads(result.stdout)
                checks = {check["id"]: check for check in payload["checks"]}

                self.assertEqual(result.returncode, 1)
                self.assertFalse(checks["verification-notes"]["passed"])
                self.assertEqual(
                    checks["verification-notes"]["details"]["exists"],
                    mode == "blank",
                )

    def test_run_metadata_requires_header_and_every_field_once(self):
        cases = {
            "missing-file": None,
            "wrong-header": VALID_METADATA.replace("# Run Metadata", "# Metadata"),
            "missing-field": VALID_METADATA.replace("- Model ID: test-model\n", ""),
            "duplicate-field": VALID_METADATA + "- Arm: harness\n",
            "blank-field": VALID_METADATA.replace("- Model ID: test-model", "- Model ID:"),
        }
        for mode, content in cases.items():
            with self.subTest(mode=mode):
                run_dir = self.make_valid_run()
                metadata = run_dir / "run-meta.md"
                if content is None:
                    metadata.unlink()
                else:
                    metadata.write_text(content, encoding="utf-8")

                result = self.run_grader(run_dir)
                payload = json.loads(result.stdout)
                check = next(
                    item for item in payload["checks"] if item["id"] == "run-metadata"
                )

                self.assertEqual(result.returncode, 1)
                self.assertFalse(check["passed"])
                if mode == "missing-file":
                    self.assertFalse(check["details"]["exists"])
                elif mode == "wrong-header":
                    self.assertFalse(check["details"]["header_valid"])
                elif mode == "missing-field":
                    self.assertEqual(check["details"]["missing_fields"], ["Model ID"])
                elif mode == "duplicate-field":
                    self.assertEqual(check["details"]["duplicate_fields"], ["Arm"])
                else:
                    self.assertEqual(check["details"]["blank_fields"], ["Model ID"])

    def test_non_utf8_evidence_returns_structured_failures(self):
        cases = (
            ("verification.md", "verification-notes"),
            ("run-meta.md", "run-metadata"),
        )
        for filename, check_id in cases:
            with self.subTest(filename=filename):
                run_dir = self.make_valid_run()
                (run_dir / filename).write_bytes(b"\xff\xfe")

                result = self.run_grader(run_dir)
                payload = json.loads(result.stdout)
                check = next(
                    item for item in payload["checks"] if item["id"] == check_id
                )

                self.assertEqual(result.returncode, 1)
                self.assertFalse(check["passed"])
                self.assertIn("UTF-8", check["details"]["read_error"])

    def test_missing_run_directory_is_an_invocation_error(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            missing = Path(temp_dir) / "missing"

            result = self.run_grader(missing)

        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertIn("run directory does not exist", result.stderr)

    def test_ground_truth_is_loaded_from_case_manifest(self):
        run_dir = self.make_valid_run()
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)
        copied_case = Path(temp_dir.name) / "case"
        shutil.copytree(CASE_DIR, copied_case, ignore=shutil.ignore_patterns("__pycache__"))
        manifest_path = copied_case / "case.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["golden"]["expected_stdout"] = "different output\n"
        manifest_path.write_text(
            json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
        )

        result = self.run_grader(run_dir, copied_case / "grader.py")
        payload = json.loads(result.stdout)
        check = next(item for item in payload["checks"] if item["id"] == "runtime-output")

        self.assertEqual(result.returncode, 1)
        self.assertFalse(check["passed"])

    def test_required_run_file_locations_are_loaded_from_case_manifest(self):
        run_dir = self.make_valid_run()
        evidence_dir = run_dir / "evidence"
        evidence_dir.mkdir()
        (run_dir / "verification.md").replace(evidence_dir / "notes.md")
        (run_dir / "run-meta.md").replace(evidence_dir / "metadata.md")
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)
        copied_case = Path(temp_dir.name) / "case"
        shutil.copytree(CASE_DIR, copied_case, ignore=shutil.ignore_patterns("__pycache__"))
        manifest_path = copied_case / "case.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["golden"]["required_run_files"] = {
            "verification_notes": "evidence/notes.md",
            "run_metadata": "evidence/metadata.md",
        }
        manifest_path.write_text(
            json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
        )

        result = self.run_grader(run_dir, copied_case / "grader.py")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(json.loads(result.stdout)["passed"])

    def test_run_metadata_requires_case_version(self):
        run_dir = self.make_valid_run()
        metadata = run_dir / "run-meta.md"
        metadata.write_text(
            metadata.read_text(encoding="utf-8").replace("- Case version: 1.0.0\n", ""),
            encoding="utf-8",
        )

        result = self.run_grader(run_dir)
        payload = json.loads(result.stdout)
        check = next(item for item in payload["checks"] if item["id"] == "run-metadata")

        self.assertEqual(result.returncode, 1)
        self.assertEqual(check["details"]["missing_fields"], ["Case version"])

    def test_run_metadata_requires_exact_not_reported_literal(self):
        for value in (
            "Not reported",
            "not reported by runtime",
            "n/a (not reported)",
            "n/a",
            "unknown",
            "not measured",
            "unreported",
            "banana",
        ):
            with self.subTest(value=value):
                run_dir = self.make_valid_run()
                metadata = run_dir / "run-meta.md"
                metadata.write_text(
                    metadata.read_text(encoding="utf-8").replace(
                        "- Token usage (input/output): not reported",
                        f"- Token usage (input/output): {value}",
                    ),
                    encoding="utf-8",
                )

                result = self.run_grader(run_dir)
                payload = json.loads(result.stdout)
                check = next(
                    item for item in payload["checks"] if item["id"] == "run-metadata"
                )

                self.assertEqual(result.returncode, 1)
                self.assertEqual(
                    check["details"]["invalid_not_reported_fields"],
                    ["Token usage (input/output)"],
                )

    def test_measured_token_usage_is_an_input_output_integer_pair(self):
        for value in ("123/45", "1,234 / 567"):
            with self.subTest(value=value):
                run_dir = self.make_valid_run()
                metadata = run_dir / "run-meta.md"
                metadata.write_text(
                    metadata.read_text(encoding="utf-8").replace(
                        "- Token usage (input/output): not reported",
                        f"- Token usage (input/output): {value}",
                    ),
                    encoding="utf-8",
                )

                result = self.run_grader(run_dir)

                self.assertEqual(result.returncode, 0, result.stdout)

    def test_run_metadata_identity_matches_case_contract(self):
        mutations = (
            ("- Task: decoy-config-repo", "- Task: another-case", "Task"),
            ("- Case version: 1.0.0", "- Case version: 9.9.9", "Case version"),
            ("- Arm: control", "- Arm: experimental", "Arm"),
        )
        for old, new, field in mutations:
            with self.subTest(field=field):
                run_dir = self.make_valid_run()
                metadata = run_dir / "run-meta.md"
                metadata.write_text(
                    metadata.read_text(encoding="utf-8").replace(old, new),
                    encoding="utf-8",
                )

                result = self.run_grader(run_dir)
                payload = json.loads(result.stdout)
                check = next(
                    item for item in payload["checks"] if item["id"] == "run-metadata"
                )

                self.assertEqual(result.returncode, 1)
                self.assertEqual(check["details"]["invalid_identity_fields"], [field])


if __name__ == "__main__":
    unittest.main()
