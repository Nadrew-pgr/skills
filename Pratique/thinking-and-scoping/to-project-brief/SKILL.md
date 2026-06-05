---
name: to-project-brief
description: Converts a clarified conversation into a concise project brief without re-interviewing the user. Use after intake, grill, research, or docs review when the user needs a stable brief for a mémoire, trip, personal project, business offer, or dev feature.
license: MIT
author: Matt Pocock (mattpocock/skills)
---

# To Project Brief

Use this after enough context has been gathered. Do not restart the interview.

## Mission

Synthesize the current conversation into a stable, reusable brief.

## Rules

- Do not ask new questions unless a blocker makes the brief impossible.
- Use the user's existing words where possible.
- Separate facts, decisions, assumptions, and open questions.
- Keep it short enough to be read in 3 minutes.
- Include a "next visible action" for momentum.

## Template

```md
# Project Brief — [Name]

## Goal
[One sentence]

## Why this matters
[Business, academic, personal, or operational reason]

## Current situation
[What exists today]

## Scope
### In scope
- [Item]

### Out of scope
- [Item]

## Constraints
- Deadline:
- Budget:
- Tools:
- Energy/time:
- Rules:

## Decisions already made
- [Decision + reason]

## Assumptions
- [Assumption to verify]

## Risks
- [Risk + mitigation]

## Success criteria
- [Observable result]

## Plan
### Now
- [Action]

### Next
- [Action]

### Later
- [Action]

## Next visible action
[10-minute action]
```

## Natural Next Steps

This skill is the **crystallization** step for non-dev work.

Use this routing after it:

- If the user now needs a tiny execution sequence → `to-action-plan`
- If the brief is actually for a dev build and is stable enough to formalize further → `to-prd`
- If major ambiguity remains, go back to `intake-and-grill`, `grill-with-docs`, or `grill-with-research` depending on the blocker

Default recommendation:
`to-project-brief` → `to-action-plan`
