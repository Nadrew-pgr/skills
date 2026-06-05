---
name: inbox-writer
description: Write user-provided captures into the Obsidian inbox as clean, traceable notes. Use for raw ideas, links, snippets, multi-item captures, or anything that must not be lost before later triage. Prefer conservative inbox capture over aggressive routing.
license: MIT
author: Matt Pocock (mattpocock/skills)
---

# Inbox Writer

## Goal

Save useful inputs without losing context. When unsure, write a clear inbox note instead of over-routing.

## Target

Default target:
- `/home/node/.openclaw/workspace/main/obsidian-vault/01 Inbox/`

Special direct target:
- Grocery / shopping items with no broader context go directly into `/home/node/.openclaw/workspace/main/obsidian-vault/07 Perso/courses.md`, not into the inbox.

## Naming

File name and H1 must match:
- `[STAT] PREF - Clear title.md` (STAT is optional)
- `# [STAT] PREF - Clear title`

**Statuts (Optionnels, 3-4 lettres avant le préfixe) :**
- `URG` (Urgent), `TODO` (À faire), `BKLG` (Backlog), `PARK` (Parking)

**Préfixes autorisés (3-4 lettres) :**
- `AGT` (Agent), `AGTC` (Agent-Content)
- `VID` (Video), `ART` (Article), `SITE` (Site), `PAGE` (Page), `PAPR` (Paper)
- `DOC` (Doc), `IDEE` (Idee), `CAPT` (Capture), `DBG` (Debug)
- `POST` (Post), `THRD` (Thread), `POD` (Podcast), `MAIL` (Email), `NOTE` (Note)

- *Règle Multi-domaines :* Pour les inputs qui touchent plusieurs domaines, accoler les deux préfixes avec un tiret (ex: `VID-AGT`).

Use `NOTE` only as fallback. Name by source/content type, not by future destination.

## Rules

1. Preserve the raw input.
2. Keep source traceability.
3. Separate raw capture from light synthesis.
4. Stay small and useful.
5. Split clearly distinct items into separate notes.
6. Default to writing in inbox, except for direct-target cases below.
7. Grocery / shopping articles with no broader context, especially short captures like “bouteille d’eau”, “lessive hypoallergénique prio”, “crème liquide”, “mouchoirs”, “fruits”, “lait”, “viande”, “légumes”, “pâtes”, or “ail et oignons”, should be applied directly to `/home/node/.openclaw/workspace/main/obsidian-vault/07 Perso/courses.md`. Do not create an inbox note for these unless Andrew adds broader context.
8. Before adding a grocery item, check whether it already exists in `courses.md` using singular/plural and close variants. If it exists, do not duplicate it.
9. If an existing grocery item is checked and Andrew asks for it again, uncheck it instead of adding a duplicate.
10. If Andrew says he already bought/took an item (e.g. “j’ai pris la lessive”, “j’ai acheté le lait”), mark the matching item checked instead of adding it.
11. Respect explicit priority words like “prio” by placing a new item under `## Priorité haute` when appropriate; if the item already exists elsewhere, move it only if needed to reflect priority without duplicating.
12. Do not invent certainty.
13. If the input is a reference or link, do lookup/enrichment first, then capture.
14. Only skip lookup/enrichment when Andrew explicitly asks for a raw ultra-fast capture.

## Template

```md
---
status: inbox
type_guess: article
source_channel: discord
source_sender: Andrew
source_at: 2026-04-13 10:54 UTC
source_url: https://example.com
agent_written: true
agent_name: Ines
---

# ARTICLE - Clear title

## Capture
Raw or near-raw text.

## Source
- Channel: Discord
- Sender: Andrew
- Date: 2026-04-13 10:54 UTC
- URL: https://example.com

## Use
Why this may matter.

## Note
To triage later.
```

## Boundary

This skill writes inbox notes only. It does not do full routing, task management, or calendar planning.
