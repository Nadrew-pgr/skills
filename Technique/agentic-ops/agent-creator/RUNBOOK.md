# Agent Creator Runbook

## Purpose

This runbook exists to create OpenClaw agents cleanly and repeatably.

## Standard Order

1. Confirm whether the request is for:
   - a real runtime agent
   - a skill
   - a persona/skin
   - or just documentation
2. Read local docs and current config.
3. Create the runtime agent with `openclaw agents add`.
4. Fill the workspace bootstrap files.
5. Apply identity.
6. Add skills visibility if needed.
7. Add channel bindings if needed.
8. Verify with config inspection + `openclaw agents list --bindings --json`.
9. Report exactly what changed.

## Canonical Files

- Runtime config: `~/.openclaw/openclaw.json`
- Runtime state dirs: `~/.openclaw/agents/`
- Workspaces: `~/.openclaw/workspace*`
- Docs:
  - `/app/docs/cli/agents.md`
  - `/app/docs/gateway/config-agents.md`
  - `/app/docs/concepts/agent-workspace.md`

## Future Shared Baseline

This runbook is designed to later absorb a common baseline for every agent, including:
- timezone
- coffre rules
- Obsidian/vault rules
- memory rules
- safety defaults
- shared operational conventions

Until that baseline is formalized, do not pretend it exists.