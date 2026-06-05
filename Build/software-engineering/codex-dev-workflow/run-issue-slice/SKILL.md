---
name: run-issue-slice
description: Execute one implementation issue end-to-end using fresh context, Slice Start Brief, test-first workflow, narrow implementation, verification, reviewer pass, build-log update, visual impact report, and clean handoff. Use when the user says to start/continue the next issue or implement a slice.
license: MIT
author: Andrew (Nadrew-pgr)
---

# Run Issue Slice

## Mission

Implement exactly one issue.

Do not start the next issue unless the human explicitly asks after this slice is complete.

## Required Reading Order

Use project docs if present:

1. `AGENT.md`
2. `README.md`
3. PRD/build docs
4. `QUALITY_GATES.md`
5. `ISSUES.md`
6. latest relevant `build-log.md`
7. `git status`
8. files related to the issue

## Slice Start Brief

Before coding, output:

- issue ID and goal;
- previous issue status;
- acceptance criteria;
- gates that apply;
- expected files/packages;
- test/manual/visual check to create first;
- reviewer plan;
- out of scope;
- stop conditions;
- visual impact expected.

If the brief is incomplete, do not code.

## Execution

1. Define or update failing proof first.
2. Implement the smallest serious solution.
3. Run targeted checks.
4. Run broader checks appropriate to blast radius.
5. Run manual/visual verification when relevant.
6. Use reviewer/subagent passes when available.
7. Update build log.
8. Report visual impact.
9. End with status, tests, remaining risk, next issue.

## Status Labels

- `completed`
- `code-complete, visual verification pending`
- `code-complete, human review pending`
- `blocked`
- `not accepted`

## Guardrails

- No toy implementations.
- No false done.
- No unrelated refactors.
- No silent docs drift.
- Do not revert user changes.
- If UI changed, say exactly what changed visually.
