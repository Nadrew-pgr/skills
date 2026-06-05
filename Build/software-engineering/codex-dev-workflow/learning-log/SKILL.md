---
name: learning-log
description: Log project errors, user corrections, process learnings, feature requests, and ideas into .learnings with concise templates and IDs. Use during development when a command fails, review finds a repeated issue, the user corrects the agent, a best practice emerges, or a product idea should be retained.
license: MIT
author: Andrew (Nadrew-pgr)
---

# Learning Log

## Mission

Capture useful failures and ideas without polluting build docs.

Log in the same turn when possible.

## Files

Create if missing:

- `.learnings/ERRORS.md`
- `.learnings/LEARNINGS.md`
- `.learnings/FEATURE_REQUESTS.md`
- `.learnings/IDEAS.md`

## Event Types

- `error`: command failure, crash, timeout, broken integration.
- `learning`: user correction, process gap, best practice, recurring mistake.
- `feature`: explicit feature request.
- `idea`: rough product or technical idea not yet scoped.

## IDs

- `ERR-YYYYMMDD-XXX`
- `LRN-YYYYMMDD-XXX`
- `FEAT-YYYYMMDD-XXX`
- `IDEA-YYYYMMDD-XXX`

Increment `XXX` per file/day.

## Entry

```md
## ID — Short title

- Date:
- Type:
- Status: open/resolved
- Context:
- Evidence:
- Lesson:
- Action:
- See also:
```

## Rules

- Never log secrets, tokens, private keys, or credentialed URLs.
- Keep entries searchable and operational.
- Deduplicate: update existing entries or add `See also`.
- Close the loop when resolved with date and commit/PR if available.
