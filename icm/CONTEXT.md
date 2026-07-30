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
