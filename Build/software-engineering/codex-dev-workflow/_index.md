---
type: skills_category_index
status: active
category: codex-dev-workflow
rag: include
---

## Codex Dev Workflow

Pack autonome pour transformer une idee floue en repo executable par agents: build docs, quality gates, issues autosuffisantes, execution slice par slice, reviews, build logs, sync documentaire et learnings.

## Flow

```txt
Fuzzy idea
-> intake-and-grill
-> to-project-build-docs
-> to-quality-gates
-> to-implementation-issues
-> run-issue-slice
-> review-slice
-> review-to-issues or to-implementation-issues for gaps
-> sync-docs-and-renumber when docs drift
-> learning-log throughout
```

## Skills

- [[workflow-router/SKILL|workflow-router]] — route to the right workflow skill and keep the pack independent.
- [[intake-and-grill/SKILL|intake-and-grill]] — clarify fuzzy goals without overwhelming the user.
- [[to-project-build-docs/SKILL|to-project-build-docs]] — create the full build-doc pack, including PRD, gates, issues, agent rules, glossary, and build log.
- [[to-quality-gates/SKILL|to-quality-gates]] — create/update explicit quality gates, including user/app implicit requirements.
- [[to-implementation-issues/SKILL|to-implementation-issues]] — create self-contained implementation issues for weaker agents.
- [[run-issue-slice/SKILL|run-issue-slice]] — execute one issue with fresh context, test-first, reviews, and build-log discipline.
- [[review-slice/SKILL|review-slice]] — review a completed slice against docs, tests, visual evidence, and product vision.
- [[sync-docs-and-renumber/SKILL|sync-docs-and-renumber]] — keep docs, issue numbering, next issue, and statuses aligned.
- [[learning-log/SKILL|learning-log]] — log errors, corrections, ideas, and feature requests into `.learnings/`.

## Rule

This pack is independent. Do not rely on separate `to-prd` or Matt Pocock skills being installed. Use external skills only as optional inspiration when available.
