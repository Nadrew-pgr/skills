---
name: sync-docs-and-renumber
description: Keep project build docs aligned after inserting, renaming, renumbering, completing, or reordering issues/gates. Use when issue numbers drift, next issue is wrong, README/PRD/ISSUES/QUALITY_GATES/build-log disagree, or process docs need synchronization.
license: MIT
author: Andrew (Nadrew-pgr)
---

# Sync Docs And Renumber

## Mission

Prevent agent confusion from stale docs.

Use this after:

- inserting a new issue;
- renumbering issues;
- renaming gates;
- changing canonical build-log paths;
- changing current/next issue;
- adding human-review status;
- moving items into backlog.

## Check Files

Inspect relevant files:

- `README.md`
- `AGENT.md`
- PRD/build docs
- `QUALITY_GATES.md`
- `ISSUES.md`
- `build-log.md`
- visual-check READMEs
- public glossary/docs when terms changed

## Sync Matrix

For each change, record:

```md
- Change:
- Files updated:
- Old reference:
- New reference:
- Proof/check:
```

## Rules

- Do not rewrite history casually. Build logs may keep historical references, but add a superseding note.
- Current docs must point to the correct next issue.
- Issue IDs and gate IDs must be stable and searchable.
- If old numbering remains in historical log, explain it.
- Run grep checks for old names/IDs.

## Output

- Updated references.
- Remaining historical references and why they remain.
- Checks run.
- Next issue.
