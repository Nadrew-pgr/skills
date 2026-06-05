---
name: speech
description: Convert text into spoken audio with OpenAI TTS. Use for voice notes, spoken drafts, narrated documents, and MP3 generation from plain text or markdown.
license: MIT
author: Matt Pocock (mattpocock/skills)
---

# Speech

Use this skill when you need **text-to-speech**.

## What it does

- takes text and turns it into audio
- accepts direct text, stdin, or a text file
- uses the existing OpenAI credentials already present in OpenClaw config or env
- uses the OpenAI speech endpoint configured for TTS
- auto-splits long text and merges the result into one MP3

## Command

```bash
python3 {baseDir}/scripts/tts.py --text "Bonjour Andrew" --out /tmp/bonjour.mp3
```

## Useful examples

```bash
python3 {baseDir}/scripts/tts.py --text "Bonjour Andrew" --out /tmp/bonjour.mp3
python3 {baseDir}/scripts/tts.py --file /path/to/note.md --out /tmp/note.mp3
cat /path/to/script.txt | python3 {baseDir}/scripts/tts.py --stdin --out /tmp/script.mp3
python3 {baseDir}/scripts/tts.py --file /path/to/script.md --voice alloy --out /tmp/script.mp3
```

## Notes

- This is text-to-speech, not speech-to-text.
- Output format is MP3.
- Long texts are chunked automatically, then merged into one final file.
- Defaults come from `messages.tts.providers.openai` in OpenClaw config when available.
