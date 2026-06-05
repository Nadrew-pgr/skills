---
name: intake-and-grill
description: Turns vague goals into a clear brief through a one-question-at-a-time interview with recommended answers. Use when the user starts from fuzzy intent such as "I need to do my mémoire", "I need to plan a trip", "I need to revise", or "I need to do this".
license: MIT
author: Matt Pocock (mattpocock/skills)
---

# Intake and Grill

Use this when the user starts from a vague obligation, goal, or pressure rather than a concrete plan.

## Mission

Transform fog into a decision-ready brief without overwhelming the user.

## Rules

1. Ask only one question at a time.
2. For every question, provide your recommended answer first.
3. Do not dump long lists of questions.
4. If the answer can be inferred from available docs, prior notes, project files, or conversation context, infer it and say your assumption.
5. If current external facts matter, route to or invoke `grill-with-research`.
6. If existing notes/docs matter, route to or invoke `grill-with-docs`.
7. If the topic is learning/revision, route to or invoke `dscg-learning-loop` or `deliberate-practice-scaffolder`.
8. End with a small brief and at most three next actions.

## Intake Map

Clarify in this order:

1. Outcome — what would "done" look like?
2. Deadline — when does this need to be done?
3. Constraints — rules, format, budget, tools, energy, available time.
4. Current assets — docs, notes, sources, prior decisions, drafts.
5. Unknowns — what must be researched or decided.
6. Success criteria — how we know this worked.
7. Next action — the smallest action the user can take now.

## Output Format

When enough is clear, produce:

```md
# Brief

## Goal
[One sentence]

## Constraints
- [Constraint]

## Decisions made
- [Decision]

## Open questions
- [Question]

## Recommended path
1. [Step]
2. [Step]
3. [Step]

## Next visible action
[Action doable in 10 minutes]
```

## ADHD Mode

Keep the working set small. Prefer one decision, one action, one visible checkpoint. If the plan grows beyond five items, compress it into three phases: Now, Next, Later.

## Natural Next Steps

This skill is the **draft + first alignment** step for non-dev work.

Use this routing after it:

- If existing vault notes, docs, specs, or prior decisions now matter → `grill-with-docs`
- If current external facts now matter → `grill-with-research`
- If enough is clear and the user needs a stable reference doc → `to-project-brief`
- If enough is clear and the user needs immediate movement, not more synthesis → `to-action-plan`

Default recommendation:
`intake-and-grill` → `to-project-brief` → `to-action-plan`
