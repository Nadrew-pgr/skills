---
name: review-slice
description: Review a completed implementation slice against build docs, issue acceptance criteria, quality gates, code, tests, visual evidence, reviewer logs, product vision, and build-log truthfulness. Use before accepting a slice or when the user asks for review/subagent review.
license: MIT
author: Andrew (Nadrew-pgr)
---

# Review Slice

## Mission

Decide whether a slice is accepted, pending, or blocked.

Review evidence first. Do not implement fixes unless explicitly asked.

## Review Axes

- Acceptance criteria proof.
- Tests and test-first honesty.
- Architecture boundaries.
- UI/UX/visual evidence.
- Data/persistence/security/policy truthfulness.
- Docs/build-log status.
- Product vision and implicit user/app requirements.
- Regression risk.

## Reviewer Passes

Use subagents when available. Otherwise label as fallback self-review.

- Architecture Reviewer
- Test Reviewer
- UX/Visual Reviewer
- Security/Policy Reviewer
- DX/Docs Reviewer
- Content/Brand Reviewer when visual/content work exists
- License Reviewer when references/assets/plugins are involved

## Finding Shape

```md
### [P1] Finding

- Evidence:
- Source of truth:
- Impact:
- Required action:
- Suggested issue/fix:
```

## Decision Labels

- `accepted`
- `accepted with follow-ups`
- `code-complete, visual verification pending`
- `code-complete, human review pending`
- `not accepted`
- `blocked`

## Output

```md
## Verdict

## Evidence Reviewed

## Findings

## Reviewer Passes

## Acceptance Decision

## Follow-up Issues / Backlog
```

## Guardrails

- Do not accept without proof.
- Do not hide reviewer findings.
- Separate verified gaps from hypotheses.
- If visual tooling failed, mark visual verification pending.
