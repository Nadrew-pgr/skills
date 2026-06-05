---
name: vault-capture
description: Captures decisions, learning notes, project briefs, and review outputs into a minimal Obsidian-friendly note structure with wikilinks. Use when the user asks to save, update, organize, or connect notes in their vault.
disable-model-invocation: true
license: MIT
author: Matt Pocock (mattpocock/skills)
---

# Vault Capture

Use this only when the user explicitly wants to write or update notes.

## Mission

Capture useful knowledge without bloating the vault.

## Rules

1. Prefer updating an existing note over creating a new one.
2. Create a new note only if it has a clear future use.
3. Use Obsidian wikilinks: `[[Note Title]]`.
4. Keep notes atomic but not tiny.
5. Add links at the bottom.
6. Capture decisions separately from general notes.
7. Do not save sensitive client or employer information.

## Note Types

### Project Brief

```md
# [Project Name]

## Goal
## Constraints
## Decisions
## Next Actions
## Links
```

### Learning Note

```md
# [Concept]

## À retenir
## Questions active recall
## Exercices
## Pièges
## Flashcards
## Links
```

### Decision Note

```md
# Decision — [Title]

## Decision
## Reason
## Alternatives rejected
## Consequence
## Revisit if
## Links
```

## Output

After writing or proposing the note, summarize:

```md
Saved/updated:
- [Note]

Linked to:
- [[Related Note]]

Next:
- [One next action]
```
