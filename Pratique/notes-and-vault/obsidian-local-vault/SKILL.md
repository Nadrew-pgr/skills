---
name: obsidian-local-vault
description: Work inside the Momentarise Obsidian plugin using the real local vault, IDE-like context, structured questions, and local diff approval.
license: MIT
author: OpenClaw / ClawHub
---

# Obsidian Local Vault

Use this skill when the user asks to work on their Obsidian vault, the current note, a selection, Momentarise notes, tasks, projects, or local Markdown files from the Momentarise/Obsidian plugin.

## Core Rule

The real source of truth is the Obsidian vault opened by the local plugin.

The OpenClaw workspace copy may be useful as cache, scratch, fallback, or background context, but do not treat it as the final local vault when Obsidian is connected.

## How To Behave

- Inspect before concluding when the task depends on vault content.
- Inspect automatically when the user refers to the current note, this file, a named note/topic, a folder, a file status, or whether something is a Moment, Task, Project, or normal note.
- Do not claim you read the local vault until a local vault result is present.
- Do not claim a change is done, applied, written, fixed, or created unless a local vault result, accepted `momentarise-edit`, or explicit tool result confirms it.
- If you only proposed a patch, preview, or plan, say it is proposed or previewed. Do not say it is done.
- Do not ask the user to paste JSON, copy a path placeholder, or manually run shell commands for simple vault reads.
- Distinguish clearly between:
  - conversation memory;
  - local vault tool results;
  - OpenClaw workspace files.
- Ask a concise structured question only when a user decision changes the next step.
- When asking a structured question, provide two or three choices, mark one as recommended, and allow an `Other` free-form answer.

## Ambiguous Targets

Style, UI, interface, theme, layout, "rounding", "dashboard", "homepage", or "global" requests are ambiguous unless the user names a concrete file, path, note, plugin surface, or app.

When the target is ambiguous, ask a structured question before editing. Recommended choices:

- `Le plugin Obsidian actuel`
- `La note/page active du vault`
- `Une app/page web du projet`

Use `Other` for free-form clarification.

Do not infer paths like `/home/node/.openclaw/workspace/OaaS/styles.css`, `OaaS/styles.css`, or any workspace/project source file unless the user explicitly named that file or asked to edit that project source.

If Obsidian is connected, workspace edits are not proof that the local Obsidian vault or plugin UI changed.

## Local Vault Tools

Request local Obsidian context with fenced blocks. The plugin renders or auto-runs these tools.

Active note:

```momentarise-vault-tool
{"tool":"vault.getActiveFile"}
```

Current selection:

```momentarise-vault-tool
{"tool":"vault.getSelection"}
```

Open documents:

```momentarise-vault-tool
{"tool":"vault.getOpenDocuments"}
```

Search the real local vault:

```momentarise-vault-tool
{"tool":"vault.search","query":"search terms"}
```

List a concrete vault folder:

```momentarise-vault-tool
{"tool":"vault.listFolder","path":"Folder/Subfolder"}
```

Read a concrete file path returned by a prior local result:

```momentarise-vault-tool
{"tool":"vault.read","path":"Folder/Note.md","startLine":1,"endLine":80}
```

Never use placeholder paths such as `path/in/vault.md`, `<colle-ici-le-path>`, `file.md`, or `the path returned above`.

If `vault.getActiveDocument` returns no active local document, use `vault.getOpenDocuments` when the user refers to an open document, or `vault.search` / `vault.listFolder` when the user named a target or folder. Ask the user for a path only after those local tools fail.

## Edit Flow

For modifications, propose a local diff. The plugin applies only after user `Accept`.

```momentarise-edit
{"file":"Folder/Note.md","operation":"replace","oldText":"exact text currently in the local Obsidian vault","newText":"replacement text","reason":"why this edit is useful"}
```

Rules:

- Use exact, small replacements.
- Read the local file first unless the exact current text is already in a local vault result.
- Do not write directly into the OpenClaw workspace copy when the user expects a local Obsidian edit.
- Do not say the edit is applied until the plugin reports that the preview was accepted or a local tool result proves the final file content changed.
- If the edit is ambiguous, ask a structured question instead of guessing.

## Structured Questions

Use this format when a choice matters:

```momentarise-question
{"question":"Question text","choices":[{"label":"Recommended option","value":"Answer text","recommended":true},{"label":"Second option","value":"Answer text"}],"other":true}
```

The plugin renders the question above the composer. Do not explain the JSON to the user.
