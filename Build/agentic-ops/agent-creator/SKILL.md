---
name: agent-creator
description: Create or update a real OpenClaw agent using the documented runtime path. Use for agent creation, workspaces, identity, bindings, bootstrap files, and agent setup runbooks.
license: MIT
author: OpenClaw / ClawHub
---

# Agent Creator

## Goal

Create a **real OpenClaw agent** that exists in runtime, not just a persona file or idea stub.

## Use This Skill When

- the user asks to create a new OpenClaw agent
- the user wants a new workspace + routing + identity
- the user wants a runbook for agent creation
- the user wants to bind a Discord/Telegram/etc. surface to an agent
- the user is unsure whether they need an agent, a skill, a prompt, or just a channel-specific behavior

## Core Rule

Do **not** invent agent setup from memory alone.

Always start from:
1. the real config in `~/.openclaw/openclaw.json`
2. local OpenClaw docs
3. current agent/workspace patterns already present on the machine

## Canonical Sources

Read these first when needed:
- `/app/docs/cli/agents.md`
- `/app/docs/gateway/config-agents.md`
- `/app/docs/concepts/agent-workspace.md`
- `~/.openclaw/openclaw.json`

## Critical Distinction

Before acting, determine which of these the user actually wants:

1. **Real runtime agent**
   - needs `agents.list[]`
   - may need `bindings[]`
   - has its own workspace

2. **Skill**
   - lives in `skills/<name>/SKILL.md`
   - teaches behavior/tooling
   - does not create a routable agent by itself

3. **Persona / skin / prompt overlay**
   - changes identity, tone, or instructions
   - may not require a new agent at all

4. **Project note / agent spec**
   - documentation only
   - no runtime effect by itself

If the user says "create an agent", prefer the **real runtime agent** interpretation unless context clearly says otherwise.

## Runbook

### 1) Clarify the target shape

Extract or ask for the minimum missing facts:
- agent id
- purpose / mission
- workspace path if specific
- whether routing/binding is needed
- whether it should inherit common baseline rules

Do not ask unnecessary questions when a safe default exists.

### 2) Inspect the current state

Check:
- existing agents in `~/.openclaw/openclaw.json`
- existing workspaces under `~/.openclaw/`
- existing bindings
- relevant local docs

### 3) Create the runtime agent first

Prefer the documented command path:

```bash
openclaw agents add <id> --workspace <path> --non-interactive
```

This is preferred over hand-editing config from scratch because it creates the runtime entry and workspace skeleton in the standard shape.

### 4) Treat files as the second layer, not the first

After the runtime agent exists, adjust the workspace files:
- `AGENTS.md`
- `SOUL.md`
- `USER.md`
- `IDENTITY.md`
- `HEARTBEAT.md`
- `TOOLS.md`

Do **not** confuse "workspace files exist" with "agent exists in runtime".

### 5) Set identity explicitly

If the agent needs a name/theme/emoji/avatar, use:

```bash
openclaw agents set-identity --agent <id> ...
```

Or load from the workspace `IDENTITY.md` when that path is known to resolve correctly.

### 6) Add skills deliberately

If the setup uses skill allowlists:
- check `agents.defaults.skills`
- check `agents.list[].skills`
- add the needed skill visibility intentionally

Do not assume a newly created skill is automatically visible when allowlists are active.

### 7) Bind channels only when needed

If the user wants a channel/thread/topic/surface routed to the agent, add or update `bindings[]`.

Typical binding pattern:
- `match.channel`
- optional `match.peer`
- `agentId`

Keep routing simple.

### 8) Verify before claiming success

Minimum verification:
- inspect resulting `~/.openclaw/openclaw.json`
- run `openclaw agents list --bindings --json`
- confirm the workspace exists
- confirm the expected binding exists if routing was requested

### 9) Do not overdo the rollout

Unless the user asked for it:
- do not restart the gateway
- do not create extra agents "for later"
- do not add speculative bindings
- do not add parallel config systems

## Baseline Checklist For New Agents

When relevant, apply the common shared setup layer:
- timezone rules
- vault / Obsidian rules
- memory conventions
- safety boundaries
- messaging / routing conventions
- any shared "coffre" rules

If these baseline elements are not yet formalized, note the gap instead of inventing hidden defaults.

## Anti-Patterns

Avoid these mistakes:
- creating only files and calling it a real agent
- inventing config keys without checking docs
- copying old shapes blindly when docs/current config disagree
- hiding routing complexity inside vague language
- assuming skill visibility without checking allowlists
- restarting services without user approval

## Output Contract

When you finish, report:
- created/changed files
- changed config keys
- whether the agent now exists in runtime
- whether routing/binding exists
- whether any restart is still required
- the next concrete test to run

## Short Diagnostic Heuristic

If a user says the agent "exists" but cannot be focused or routed, suspect one of these first:
- missing `agents.list[]` entry
- missing or wrong `bindings[]`
- wrong workspace path
- skills not visible because of allowlist config
