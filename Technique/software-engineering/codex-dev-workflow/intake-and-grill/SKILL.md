---
name: intake-and-grill
description: Clarify a fuzzy product or development idea into decisions that can feed project build docs. Use when the user starts with rough intent, many ideas, uncertainty, or wants to be grilled before generating docs/issues.
license: MIT
author: Matt Pocock (mattpocock/skills)
---

# Intake And Grill

## Mission

Turn a fuzzy idea into a decision-ready brief without overwhelming the user.

Ask one question at a time when needed. If an answer can be inferred from files, docs, prior context, or code, infer it and state the assumption.

## Clarify

1. Outcome: what should exist when done?
2. Users: who uses it, who integrates it, who reviews it?
3. Surfaces: web, mobile, desktop, CLI, API, IDE, agent workflow, docs.
4. Constraints: tech, time, budget, legal, license, privacy, visual quality, accessibility.
5. Non-goals: what must not be built now?
6. Success criteria: how acceptance will be proven.
7. Risks: unclear product, hidden integration, visual quality, data loss, security.
8. Existing assets: docs, repo, designs, screenshots, examples, references.

## Output

```md
## Build Brief

- Goal:
- Users:
- Surfaces:
- In scope:
- Out of scope:
- Constraints:
- Decisions:
- Assumptions:
- Risks:
- Success criteria:
- Open questions:
- Recommended next skill: to-project-build-docs / to-quality-gates / to-implementation-issues
```

## Guardrails

- Do not create build docs yet unless the user asks or the brief is stable.
- Do not ask long questionnaires.
- Do not hide assumptions.
- If the user asks for execution immediately but requirements are unstable, state the risk and recommend `to-project-build-docs`.
