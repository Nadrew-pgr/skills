---
name: deliberate-practice-scaffolder
description: Creates progressive practice exercises with explanations, corrections, traps, and review loops. Use when the user wants to learn, revise, train for exams, prepare an oral defense, or scaffold exercises for DSCG, mémoire, AI, business, or writing.
license: MIT
author: Andrew (Nadrew-pgr)
---

# Deliberate Practice Scaffolder

Use this to transform a topic into exercises that build skill, not passive notes.

## Mission

Create a progression from recall to real-world/exam simulation.

## Exercise Ladder

1. Recall — definitions, formulas, facts.
2. Understanding — explain in plain language.
3. Application — small cases.
4. Trap detection — common mistakes and edge cases.
5. Exam or real-world simulation — full scenario.
6. Feedback loop — correction, score, next weakness.

## Output Template

```md
# Practice Pack — [Topic]

## Goal
By the end, the learner can [capability].

## Level 1 — Recall
1. Question:
   Expected answer:

## Level 2 — Explain
1. Prompt:
   Good answer should include:

## Level 3 — Apply
### Case
[Scenario]

### Task
[What to produce]

### Correction
[Reference answer]

## Level 4 — Traps
- Trap:
  Why it is tempting:
  Correct reasoning:

## Level 5 — Simulation
[Exam/oral/real-world scenario]

## Feedback
- Score:
- Weakness:
- Next exercise:
```

## Rules

- Start easier than the user thinks necessary.
- Make mistakes visible.
- Always include correction.
- If the user is revising DSCG, prefer active recall and cases over summaries.
- If the user asks for flashcards, generate compact question/answer pairs after exercises.
