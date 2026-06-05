---
name: to-implementation-issues
description: Convert build docs, PRD sections, quality gates, backlog, review findings, or feature plans into self-contained implementation issues that a weaker/fresh agent can execute one at a time with tests, visual checks, reviewers, build-log requirements, and stop conditions.
license: MIT
author: Andrew (Nadrew-pgr)
---

# To Implementation Issues

## Mission

Create issues that are executable without hidden context.

Each issue should be narrow enough for one agent/conversation and complete enough that a less capable model can still implement it safely.

## Issue Template

```md
## ISSUE-ID — Title

### Goal

One concrete outcome.

### Context

Why this exists and what previous issue/status it depends on.

### Scope

- In scope.
- Out of scope.

### Acceptance criteria

- Observable behavior.
- Required docs/log changes.
- Visual impact statement.

### Test-first / Verification plan

- RED: automated test, manual check, fixture, or visual scenario to define first.
- GREEN: smallest serious implementation.
- REFACTOR: cleanup boundaries.

### Manual verification

Required scenario, or `Not required` with reason.

### Visual verification

Screenshot/artifact path and viewport requirements when visible UI/content changes.

### Expected files/packages

Likely areas to inspect or change. Keep this non-binding unless exact paths are required.

### Execution model

- Implementation: sequential only.
- Fresh agent required: yes/no.
- Reviewer subagents: allowed reviewers.
- Parallel implementation: forbidden unless human-approved.
- Human review required: yes/no and why.

### Stop conditions

- [When to stop and ask.]

### Reviewer

Architecture / Test / UX / Security / DX / Visual / Content / License.
```

## Rules

- Prefer vertical slices over horizontal layers.
- Every code issue needs test-first or explicit manual-first proof.
- Every UI/content visual issue needs visual impact and visual evidence.
- Do not bundle unrelated backlog ideas into an implementation issue.
- Do not hide hard decisions inside vague acceptance criteria.
- Include previous status and next issue when sequencing matters.

## Output

If the user wants a proposal, list issue titles, dependencies, HITL/AFK, and why.

If writing `ISSUES.md`, update dependencies, numbering, and next issue references.
