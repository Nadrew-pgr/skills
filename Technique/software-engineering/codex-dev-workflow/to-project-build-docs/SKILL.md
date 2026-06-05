---
name: to-project-build-docs
description: Generate or update the full agent-executable build-document pack for a development project: README, AGENT, PRD, QUALITY_GATES, ISSUES, build log, glossary, public/internal docs layout, and optional visual-check or learning-log scaffolding. Use instead of a standalone to-prd skill when the project needs docs detailed enough for weaker agents to execute.
license: MIT
author: Andrew (Nadrew-pgr)
---

# To Project Build Docs

## Mission

Create the complete build-doc pack, not only a PRD.

The output should let a weaker model or fresh agent understand the project, choose the current issue, implement one slice, verify it, review it, and stop cleanly without relying on hidden conversation context.

## Default Docs

Use these unless the project has stronger conventions:

- `README.md` — public entrypoint, status, quickstart, doc map.
- `AGENT.md` — mandatory agent protocol, reading order, fresh issue rule, stop conditions.
- `docs/internal/PRD.md` — product requirements and vision.
- `docs/internal/QUALITY_GATES.md` — blocking gates and proof requirements.
- `docs/internal/ISSUES.md` — self-contained implementation issues.
- `docs/internal/build-log.md` — append-only progress and proof log.
- `docs/public/GLOSSARY.md` — shared vocabulary when domain language matters.
- `docs/internal/visual-checks/` — visual evidence when UI exists.
- `.learnings/` — optional errors/learnings/features/ideas if the project wants self-improvement logs.

Separate publishable docs from internal planning docs.

## Context Budget Rule

If context is tight or the model is weaker, split the work:

1. create/update `README.md`, `AGENT.md`, and PRD;
2. create/update `QUALITY_GATES.md`;
3. create/update `ISSUES.md`;
4. create/update build log and glossary.

Never produce shallow docs just to fit all files in one turn. Prefer a staged plan with clear handoff.

## PRD Contents

Include:

- problem;
- users and surfaces;
- product value;
- goals and non-goals;
- core workflows;
- architecture boundaries;
- data/persistence/security policy;
- UI/UX/visual requirements when relevant;
- adapters/integrations;
- acceptance definition;
- backlog/future candidates.

## AGENT Contents

Include:

- mandatory reading order;
- fresh issue agent rule;
- sequential implementation rule;
- Slice Start Brief requirement;
- test-first rule;
- no false done/no toy implementation;
- visual impact reporting;
- visual verification gate for UI;
- reviewer/subagent policy;
- build-log update requirement;
- stop conditions.

## Build Log Contents

Initialize or maintain:

- timestamped entries;
- issue status;
- files changed;
- tests/checks run;
- manual/visual evidence;
- reviewer result;
- visual impact;
- next issue.

## Output

If writing files:

- list created/updated docs;
- list assumptions;
- list checks to run;
- recommend next skill: `to-quality-gates` or `to-implementation-issues`.

If not writing files:

- produce a file-by-file plan with enough detail for another agent to write them.
