---
name: to-action-plan
description: Turns a brief, goal, or messy discussion into a tiny ADHD-friendly execution plan with immediate next actions. Use when the user needs to act, feels overwhelmed, has too many ideas, or asks what to do next.
license: MIT
author: Matt Pocock (mattpocock/skills)
---

# To Action Plan

Use this when the user needs movement, not more thinking.

## Mission

Compress complexity into a small plan the user can start today.

## Rules

1. Never output more than three main actions unless asked.
2. Always include a 10-minute starter action.
3. Use visible checkpoints.
4. Separate "Now", "Next", and "Later".
5. If there are more than five tasks, hide them under phases.
6. Prefer momentum over perfect planning.

## Output

```md
# Action Plan

## Objective
[One sentence]

## Now — next 10 minutes
- [Small action]

## Next — next focused block
- [One meaningful action]

## Later — after first checkpoint
- [One follow-up action]

## Checkpoint
At [time/date], verify:
- [Observable criterion]

## Do not do yet
- [Distraction or premature task]
```

## Overwhelm Recovery

If the user seems stuck, use:

```md
Minimum viable move:
1. Open [thing].
2. Do [one tiny action].
3. Send/save [visible output].
```

## Natural Next Steps

This skill is the **immediate execution** step.

Use this routing after it:

- If the user completes the first move and needs a more stable reference → `to-project-brief`
- If the plan exposes missing ambiguity → `intake-and-grill`
- If the plan depends on missing docs or current facts → `grill-with-docs` or `grill-with-research`
- If the action plan is for a dev build and is ready to become tracked work → `to-prd` or `to-issues`

Default recommendation:
This is usually the last synthesis skill before real execution.
