# Repository Checks

Run commands from the repository root with Python 3. Record raw output and exit status in the active ICM task package.

| Change or claim | Command | Prerequisite | Success signal |
|---|---|---|---|
| ICM adapter structure or routing | python scripts/check-icm-repository.py | None beyond Python 3 | Exit 0 and "icm repository adapter: all checks passed" |
| Installable harness package | python scripts/check-skill-package.py | PyYAML available | Exit 0 and "fable-task-harness: all checks passed" |
| Tracked evaluation cases or graders | python scripts/check-eval-cases.py | Declared case grader tests are runnable | Exit 0 and one "<case-id>: valid" line per tracked case |
| Repository Python checks | python -m unittest discover -s scripts/tests -v | None beyond Python 3 | Exit 0 and final "OK" |

Task plans copy the exact commands relevant to their approved write paths. Do not claim an unrun command passed.
