---
name: grill-with-research
description: Researches current or external information first, then grills the user one question at a time with cited findings and recommended answers. Use for travel, mémoire topics, market research, legal/regulatory context, tools, prices, schedules, or any plan that depends on up-to-date facts.
license: MIT
author: Matt Pocock (mattpocock/skills)
---

# Grill With Research

Use this when the user needs to make a decision and the facts may be external, current, niche, or changeable.

## Mission

Do a short evidence pass before challenging the plan. Never grill from outdated assumptions.

## Workflow

1. Define the research question in one sentence.
2. Identify the minimum facts needed to challenge the decision.
3. Search or inspect sources.
4. Summarize only the facts that change the decision.
5. State uncertainties and conflicts.
6. Start the grilling loop: one question at a time, with your recommended answer.

## Research Ledger

Maintain a compact ledger:

```md
## Evidence Ledger
- Fact:
  Source:
  Confidence:
  Why it matters:
- Unknown:
  How to resolve:
```

## Grilling Loop

For each question:

```md
Question — [single decision to resolve]

Recommended answer — [your opinion, based on evidence]

Why it matters — [risk/opportunity]

User decision — [wait for the user]
```

## Rules

- Use current sources for prices, laws, schedules, tools, APIs, travel, academic requirements, or market facts.
- Cite sources when research is used.
- Do not ask the user for facts that can be researched.
- Do not over-research. Stop as soon as enough evidence exists to ask the next decision question.
- For travel, prioritize dates, departure city, budget, constraints, transport, lodging area, weather/season, and non-negotiables.
- For mémoire/research, prioritize academic framing, source quality, methodology, problem statement, and supervisor expectations.

## Final Output

End with:

```md
# Decision Brief

## Recommendation
[Your recommendation]

## Evidence
- [Key fact + source]

## Decisions locked
- [Decision]

## Open risks
- [Risk]

## Next three actions
1. [Action]
2. [Action]
3. [Action]
```

## Natural Next Steps

This skill is the **research + alignment** step.

Use this routing after it:

- If the researched decision now needs to become a stable non-dev reference → `to-project-brief`
- If the user is clear enough and only needs an execution plan → `to-action-plan`
- If the topic has become largely about existing vault docs or prior decisions → `grill-with-docs`
- If the topic is a dev feature and the research has clarified the shape of the build → `to-prd`

Default recommendation:
`grill-with-research` → `to-project-brief` → `to-action-plan`
