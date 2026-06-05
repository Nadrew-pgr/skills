---
name: tts
description: Convert text into spoken MP3 audio with OpenAI TTS. Use when you want text read aloud as an audio file.
license: MIT
author: Matt Pocock (mattpocock/skills)
---

# TTS

Alias explicite pour le helper text-to-speech.

## Command

```bash
python3 {baseDir}/scripts/tts.py --text "Bonjour Andrew" --out /tmp/bonjour.mp3
```

## Exemples

```bash
python3 {baseDir}/scripts/tts.py --text "Bonjour Andrew" --out /tmp/bonjour.mp3
python3 {baseDir}/scripts/tts.py --file /path/to/note.md --out /tmp/note.mp3
cat /path/to/script.txt | python3 {baseDir}/scripts/tts.py --stdin --out /tmp/script.mp3
```

## Note

Ce skill appelle le même helper que `speech`, mais avec un nom non ambigu: ici, on fait bien du text-to-speech.
