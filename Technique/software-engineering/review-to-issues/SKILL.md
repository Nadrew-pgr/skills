---
name: review-to-issues
description: Review a codebase, product slice, PR, implementation log, or project against its docs, acceptance criteria, quality gates, and product vision, then turn verified gaps into prioritized implementation issues. Use when the user asks for a review pass, alignment gate, docs-vs-code audit, reviewer/subagent critique, "ecarts", "to issue", or wants feedback converted into actionable issues/backlog without silently coding.
license: MIT
author: Matt Pocock (mattpocock/skills)
---

# Review To Issues

## Purpose

Use this skill to perform an evidence-first review and convert the result into issues. It is not a general brainstorming mode.

The goal is to separate:

- verified gaps between docs, code, tests, UX, and build logs;
- risks that are likely but not yet proven;
- product/UX/architecture hypotheses that need human decision;
- backlog ideas that should not block the current slice.

Project instructions always win. If the repo has `AGENT.md`, `QUALITY_GATES.md`, `ISSUES.md`, build logs, PRD docs, or reviewer rules, read and follow them before applying this skill.

## Start Context

Before reviewing, identify the review target:

- current issue, PR, commit range, feature area, or user-reported behavior;
- canonical docs and gates;
- latest build log or implementation report;
- relevant tests and visual artifacts;
- current `git status`;
- known user feedback from the active conversation.

If the target is unclear, do a small discovery pass first. Do not write code during review unless the user explicitly asks for fixes.

## Review Passes

Run only the passes that fit the request, but name which ones were used.

- **Docs/code alignment**: what the docs promise vs what the code actually does.
- **Acceptance criteria proof**: each criterion must map to a test, manual check, screenshot, fixture, build-log evidence, or reviewer statement.
- **Behavior and tests**: missing tests, shallow tests, false positives, regressions, fragile assumptions.
- **Architecture**: dependency boundaries, host/core separation, adapter responsibilities, shared contracts.
- **UX and visual behavior**: visible state, flow, responsive behavior, affordances, copy, screenshot evidence.
- **Security/privacy/policy**: secrets, local files, BYOK, policy gates, persistence truthfulness.
- **DX/process**: build logs, issue status, reviewer provenance, stale README/docs, flaky tooling.
- **Vision hypotheses**: likely product expectations not yet stated explicitly.

## Priority Model

Use priorities consistently:

- `P0`: stop immediately; data loss, security leak, broken build, impossible acceptance gate, or severe user-facing regression.
- `P1`: must fix before dependent feature or next major slice.
- `P2`: should fix soon; quality/process/UX debt that can be scheduled.
- `P3`: backlog, polish, optional extension, or needs product decision.

Do not inflate hypotheses into P1 unless a source document or observed behavior makes them blocking.

## Finding Format

Lead with findings. For each verified issue:

```md
### [P1] Short finding title

- Source of truth: file/section, issue acceptance criterion, user report, or gate.
- Observed implementation: code/test/UI/build-log evidence.
- Impact: what breaks, becomes misleading, or blocks later work.
- Proof gap: missing test/manual check/screenshot/reviewer evidence, if applicable.
- Recommended decision: fix now, create issue, update docs, or mark pending human review.
- Issue candidate: proposed issue title and scope.
```

For code reviews, include file and line references when available. For visual reviews, include screenshot paths or state that visual evidence is unavailable.

## Hypotheses Section

Keep hypotheses separate from verified gaps.

```md
## Hypotheses / Vision Opportunities

### [H2] Short hypothesis title

- Hypothesis: what the product likely should do.
- Why it seems plausible: user feedback, comparable product, workflow expectation, or architecture direction.
- Risk if ignored: UX confusion, future refactor, missing market expectation.
- Decision needed: accept into backlog, reject, or ask human.
- Issue/backlog candidate: optional.
```

Examples of hypotheses:

- frontmatter should become editable in a property UI;
- rich mode should behave closer to Obsidian Live Preview;
- a host adapter should expose file watching if the environment supports it;
- AI writing should use a backend gateway in managed production apps.

## Convert Findings To Issues

When asked to make issues, convert only accepted or clearly actionable findings. Each issue should include:

- ID or placeholder;
- goal;
- scope;
- non-goals;
- acceptance criteria;
- test-first plan;
- manual UI or visual verification, when relevant;
- fixtures or real files;
- execution model;
- reviewer plan;
- human review requirement;
- stop conditions.

Use this template:

```md
## ISSUE-ID — Title

### Goal

One concrete outcome.

### Scope

- What changes.
- What stays out.

### Acceptance Criteria

- Proven behavior, not implementation vibes.

### Test-First / Verification Plan

- Automated test that should fail first.
- Manual UI scenario if automation is not realistic.
- Fixture or real file.
- Screenshot/visual artifact if visible UI changes.

### Execution Model

- Implementation: sequential only, unless project says otherwise.
- Reviewer subagents: allowed for review only.
- Human review required: yes/no and why.

### Reviewer

Who should review: architecture, tests, UX, security, DX.
```

## Reviewer/Subagent Rules

Use independent reviewers when available, but keep responsibilities clear.

- Implementation agent owns changes.
- Reviewer agents inspect and report.
- Reviewers do not modify production code unless the human explicitly asks.
- If no subagent/tool is available, label the pass as fallback self-review.
- Do not hide reviewer feedback. Either implement it, reject it with reason, or turn it into an issue/backlog item.

Recommended reviewer prompts:

- Architecture Reviewer: check boundaries, dependencies, abstractions, host/core split.
- Test Reviewer: check whether tests prove the acceptance criteria and fail honestly first.
- UX Reviewer: inspect screenshots/UI flow and compare to stated visual goals.
- Security Reviewer: inspect secrets, policy, file access, persistence, BYOK, external calls.
- DX Reviewer: inspect docs, setup, commands, logs, stale status, reproducibility.

## Output Shape

For a review-only answer:

```md
## Verified Gaps

### [P1] ...

## Hypotheses / Vision Opportunities

### [H2] ...

## Recommended Next Issues

- ISSUE-ID or title — reason.

## Review Provenance

- Docs read:
- Tests inspected/run:
- Visual evidence:
- Reviewer model:
```

For a fix-after-review task:

1. Review and list findings first.
2. Confirm which findings are in scope.
3. Implement only scoped fixes.
4. Run proof checks.
5. Update issue/build log/docs.
6. Report visual impact when UI changed.

## Guardrails

- Do not mark an issue done because it builds.
- Do not accept toy implementations that pass shallow checks but violate the product goal.
- Do not merge verified gaps and speculative ideas in one severity list.
- Do not create duplicate issues when an existing issue/backlog entry already covers the work.
- Do not silently change docs to match weak code unless that is the explicit decision.
- Do not start the next feature while an alignment gate is unresolved.
- If visual verification is required but unavailable, mark `code-complete, visual verification pending`.
