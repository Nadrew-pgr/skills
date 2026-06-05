---
name: grill-with-docs
description: Challenges a plan against existing notes, documents, vault entries, project context, and prior decisions. Use when the user mentions Obsidian, vault, roadmap, mémoire notes, course notes, specs, context files, ADRs, or existing documentation.
license: MIT
author: Matt Pocock (mattpocock/skills)
---

# Grill With Docs

Use this when the truth is likely already in the user's documents, vault, project notes, or previous decisions.

## Mission

Do not restart from zero. Read the available context, extract the user's existing language and decisions, then challenge the plan.

## Workflow

1. Locate relevant docs or notes.
2. Extract existing terms, constraints, deadlines, decisions, and unresolved questions.
3. Identify contradictions between the user's current request and existing notes.
4. Ask one question at a time with your recommended answer.
5. Capture resolved decisions into a short decision log.
6. If the user uses vague terms, propose precise canonical terms.

## Context Checks

Look for:

- Existing roadmap or plan.
- Existing constraints and deadlines.
- Existing glossary or vocabulary.
- Prior rejected ideas.
- Notes that contradict the current direction.
- Tasks that are already done or already decided.

## Question Format

```md
Question — [single decision]

What I found in your docs — [relevant evidence or "nothing found"]

Recommended answer — [opinionated recommendation]

Why — [short reason]

Your call — [wait]
```

## Capture Format

When a decision is made:

```md
## Decision
- Decision:
- Reason:
- Consequence:
- Revisit if:
```

## Rules

- Ask one question at a time.
- Do not create massive summaries unless asked.
- If docs are missing, say so and continue with assumptions.
- Prefer updating one useful note over creating many notes.
- For Obsidian, use wikilinks when writing notes.

## Natural Next Steps

This skill is the **alignment against existing knowledge** step.

Use this routing after it:

- If the result needs to become a stable non-dev reference → `to-project-brief`
- If the result is a dev feature/design that now needs a formal implementation spec → `to-prd`
- If the result is already clear enough and the user just needs execution steps → `to-action-plan`
- If research gaps remain external/current → `grill-with-research`

Default recommendation:
- non-dev: `grill-with-docs` → `to-project-brief` → `to-action-plan`
- dev: `grill-with-docs` → `to-prd` → `to-issues`
