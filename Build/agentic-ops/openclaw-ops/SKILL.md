---
name: openclaw-ops
description: Configure, maintain, and troubleshoot a personal OpenClaw setup. Use for agents, skills, workspaces, openclaw.json, channels, routing, sessions, gateway diagnostics, and runtime hygiene.
license: MIT
author: OpenClaw / ClawHub
---

# OpenClaw Ops

## Goal

Make OpenClaw reliable with the smallest safe documented change.

## Rules

1. Start from real config, current files, and local docs.
2. Prefer documented OpenClaw mechanisms over patches or parallel systems.
3. Keep routing and agent topology simple.
4. Make compact, reviewable edits.
5. Validate syntax and state whether restart is needed.
6. Do not restart gateway or make destructive changes without explicit user approval.
7. Push back on agent sprawl and overbuilt config.

## Output

Return:
- changed files or config keys
- current status
- required user action, if any
- next test to run
