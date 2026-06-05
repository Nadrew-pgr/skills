---
name: youtube-watcher
description: Fetch readable transcripts from YouTube videos for summarization, QA, and content extraction. Use before summarizing a YouTube video when a transcript is needed.
author: michael gathara
version: 1.0.0
triggers:
  - "watch youtube"
  - "summarize video"
  - "video transcript"
  - "youtube summary"
  - "analyze video"
metadata: {"clawdbot":{"emoji":"📺","requires":{"bins":["yt-dlp"]},"install":[{"id":"brew","kind":"brew","formula":"yt-dlp","bins":["yt-dlp"],"label":"Install yt-dlp (brew)"},{"id":"pip","kind":"pip","package":"yt-dlp","bins":["yt-dlp"],"label":"Install yt-dlp (pip)"}]}}
license: MIT
---

# YouTube Watcher

## Command

```bash
python3 {baseDir}/scripts/get_transcript.py "https://www.youtube.com/watch?v=VIDEO_ID"
python3 {baseDir}/scripts/get_transcript.py --json --device-payload-file /path/to/openclaw-youtube-payload.json
```

## Behavior

1. When a browser-extension payload file is provided, normalize that already-captured transcript first and return it as a standard watcher result.
2. Otherwise try YouTube subtitles / auto-subtitles first.
3. If subtitles fail or are unavailable, download the audio with `yt-dlp`.
4. Transcribe the downloaded audio through the OpenAI Whisper API helper when credentials are available.

## Rules

- Requires `yt-dlp` in PATH.
- Audio fallback requires a usable ASR backend, currently via `/app/skills/openai-whisper-api/scripts/transcribe.sh` plus `OPENAI_API_KEY` or equivalent OpenClaw config.
- If a trusted local device payload already contains transcript text, do not force a new remote fetch just to satisfy the helper path.
- If extraction fails, report the limitation instead of inventing transcript content.
