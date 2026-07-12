# Tracked Evaluation Cases

Each folder under `evals/cases/` is a versioned evaluation-case module. It is
source material, not generated output, and must be committed with the repo.

A case owns:

- `case.json`: machine-readable identity, hashes, grader interface, and ground truth.
- `README.md`: the human-readable test plan and interpretation notes.
- `prompt.md`: the frozen task prompt.
- `fixture/`: pristine inputs copied into each isolated run.
- `grader.py`: a deterministic single-run objective grader.
- `test_grader.py`: known-good and known-bad grader tests.
- `receipts/`: compact, curated records of historical batteries worth preserving.

Generated worker artifacts remain under `evals/runs/` and stay ignored by Git.
The tracked case is the canonical source; raw runs are disposable execution
evidence unless a curated receipt promotes their durable findings.

## Validation

Run:

```powershell
python scripts/check-eval-cases.py
```

On macOS or Linux, use `python3 scripts/check-eval-cases.py`.

The repository-level check validates manifests, contained paths, normalized
hashes, exact fixture inventories, grader arguments, and receipt links, then runs
the grader test file declared by every case manifest.

## Hashing

`text-lf` hashes decode UTF-8 and normalize CRLF or CR line endings to LF before
SHA-256. Use `raw` only for byte-sensitive or binary fixtures. This keeps tracked
case hashes portable across Windows and Unix checkouts.
