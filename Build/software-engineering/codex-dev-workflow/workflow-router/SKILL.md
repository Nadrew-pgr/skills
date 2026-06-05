---
name: workflow-router
description: Route a development request through the Codex Dev Workflow pack from fuzzy idea to build docs, quality gates, implementation issues, slice execution, review, docs sync, and learning logs. Use when the user asks what workflow/skill to use, wants a full agent-executable dev process, or needs a repo made executable by weaker agents.
license: MIT
author: Andrew (Nadrew-pgr)
---

# Workflow Router

## Mission

Choose the next skill in the independent Codex Dev Workflow pack.

Do not assume separate `to-prd` or Matt Pocock skills exist. This pack owns the flow.

## Routing

```txt
Fuzzy idea
-> intake-and-grill
Clear enough project direction
-> to-project-build-docs
Build docs need gates
-> to-quality-gates
Build docs ready
-> to-implementation-issues
Issue ready
-> run-issue-slice
Slice complete
-> review-slice
Review found gaps
-> to-implementation-issues or review-to-issues-style output
Docs/numbering drift
-> sync-docs-and-renumber
Error/correction/idea/feature request appears
-> learning-log
```

## Decision Rules

- If the user is still exploring, use `intake-and-grill`.
- If the build needs repo docs, use `to-project-build-docs`.
- If gates are missing, vague, or numbered badly, use `to-quality-gates`.
- If docs exist but work is not executable, use `to-implementation-issues`.
- If an issue is current and accepted, use `run-issue-slice`.
- If a slice is complete or contested, use `review-slice`.
- If issue numbers, next issue, PRD, README, gates, and build log disagree, use `sync-docs-and-renumber`.
- Log recurring mistakes, user corrections, and product ideas with `learning-log`.

## Output

State:

- selected skill;
- why;
- inputs needed;
- next visible action;
- stop condition.
