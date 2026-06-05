---
name: to-quality-gates
description: Create or update project quality gates that make implementation slices honestly verifiable: test-first, architecture, persistence, visual QA, reviewers, build logs, human review, implicit user/app requirements, and no-false-done rules. Use when gates are missing, too generic, badly numbered, or not aligned with the project vision.
license: MIT
author: Andrew (Nadrew-pgr)
---

# To Quality Gates

## Mission

Turn project expectations into explicit gates that block false completion.

Gates must include both explicit requirements and implicit requirements inferred from:

- user statements and corrections;
- product/app category expectations;
- target users and surfaces;
- safety, privacy, persistence, and legal risks;
- visual/UX quality bar;
- comparable products or accepted references;
- host/platform constraints.

Do not limit gates to a fixed list of 8 categories. Use stable IDs so ordering can change without breaking references.

## Gate ID Pattern

Use stable IDs:

- `QG-CONTEXT` — docs, reading order, fresh agent context.
- `QG-SCOPE` — issue scope, no toy implementation, no false done.
- `QG-TEST-FIRST` — TDD/test-first/manual check first.
- `QG-ARCH` — boundaries, dependencies, host/core separation.
- `QG-DATA` — persistence, save truth, fixtures, policy, privacy.
- `QG-UI-VISUAL` — UI/UX, visual evidence, screenshots, responsive checks.
- `QG-REVIEW` — reviewer/subagent/human review rules.
- `QG-DOCS` — build log, README, PRD, issue status.
- `QG-HANDOFF` — clean git status, next issue, stop conditions.
- Add project-specific IDs such as `QG-AI`, `QG-PAYMENTS`, `QG-MOBILE`, `QG-CONTENT`, `QG-ACCESSIBILITY`, `QG-LICENSE`.

## Required Gate Shape

```md
## QG-ID — Name

### Applies when

[When this gate is active.]

### Requirement

[What must be true.]

### Proof

- Automated:
- Manual:
- Visual:
- Reviewer:

### Blocks progress when

- [Blocking condition]

### Notes

- [Implicit user/app requirement or reference]
```

## Rules

- Gates must be actionable, not slogans.
- A gate must say how it is proven.
- Manual checks do not replace automated tests for core behavior.
- UI gates require visual evidence unless explicitly impossible.
- Human review must be explicit when taste, product direction, or trust is involved.
- Document what happens when tooling fails: e.g. `code-complete, visual verification pending`.

## Output

List changed gates, new IDs, deprecated IDs, and docs/issues that must be updated.
