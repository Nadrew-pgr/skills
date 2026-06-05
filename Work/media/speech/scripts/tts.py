#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any
from urllib import request

CONFIG_CANDIDATES = [
    Path(os.getenv("OPENCLAW_CONFIG_PATH", "")).expanduser() if os.getenv("OPENCLAW_CONFIG_PATH") else None,
    Path.home() / ".openclaw" / "openclaw.json",
    Path("/home/node/.openclaw/openclaw.json"),
    Path("/root/.openclaw/openclaw.json"),
]
DEFAULT_MODEL = "gpt-4o-mini-tts"
DEFAULT_VOICE = "alloy"
DEFAULT_FORMAT = "mp3"
DEFAULT_MAX_CHARS = 3500


def eprint(*args: object) -> None:
    print(*args, file=sys.stderr)


def run_cmd(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(cmd, check=True, capture_output=True, text=True)
    except FileNotFoundError as e:
        raise RuntimeError(f"Missing required binary: {cmd[0]}") from e
    except subprocess.CalledProcessError as e:
        stderr = (e.stderr or "").strip()
        stdout = (e.stdout or "").strip()
        detail = stderr or stdout or str(e)
        raise RuntimeError(detail) from e


def load_openclaw_config() -> dict[str, Any]:
    for candidate in CONFIG_CANDIDATES:
        if not candidate or not candidate.exists():
            continue
        try:
            return json.loads(candidate.read_text(encoding="utf-8"))
        except Exception:
            continue
    return {}


def dig(data: dict[str, Any], *keys: str) -> Any:
    cur: Any = data
    for key in keys:
        if not isinstance(cur, dict):
            return None
        cur = cur.get(key)
    return cur


def resolve_tts_config() -> tuple[str | None, str | None, str, str]:
    env_api_key = os.getenv("OPENAI_API_KEY")
    env_base_url = os.getenv("OPENAI_BASE_URL")
    config = load_openclaw_config()

    provider = dig(config, "messages", "tts", "providers", "openai") or {}
    provider_api_key = provider.get("apiKey") if isinstance(provider, dict) else None
    provider_base_url = provider.get("baseUrl") if isinstance(provider, dict) else None
    provider_model = provider.get("model") if isinstance(provider, dict) else None
    provider_voice = provider.get("voice") if isinstance(provider, dict) else None

    generic_provider = dig(config, "providers", "openai") or {}
    generic_api_key = generic_provider.get("apiKey") if isinstance(generic_provider, dict) else None
    generic_base_url = generic_provider.get("baseUrl") if isinstance(generic_provider, dict) else None

    api_key = env_api_key or provider_api_key or generic_api_key
    base_url = env_base_url or provider_base_url or generic_base_url or "https://api.openai.com/v1"
    model = provider_model or DEFAULT_MODEL
    voice = provider_voice or DEFAULT_VOICE
    return api_key, base_url, model, voice


def read_input_text(args: argparse.Namespace) -> str:
    if args.text:
        return args.text.strip()
    if args.file:
        return Path(args.file).expanduser().read_text(encoding="utf-8").strip()
    if args.stdin:
        return sys.stdin.read().strip()
    raise RuntimeError("Provide one of --text, --file, or --stdin")


def normalize_text(text: str) -> str:
    text = text.replace("\r\n", "\n")
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def chunk_text(text: str, max_chars: int) -> list[str]:
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks: list[str] = []
    current = ""

    for para in paragraphs:
        candidate = para if not current else current + "\n\n" + para
        if len(candidate) <= max_chars:
            current = candidate
            continue

        if current:
            chunks.append(current)
            current = ""

        if len(para) <= max_chars:
            current = para
            continue

        sentences = re.split(r"(?<=[\.!?])\s+", para)
        for sent in sentences:
            sent = sent.strip()
            if not sent:
                continue
            candidate = sent if not current else current + " " + sent
            if len(candidate) <= max_chars:
                current = candidate
            else:
                if current:
                    chunks.append(current)
                current = sent

    if current:
        chunks.append(current)
    return chunks


def synthesize_chunk(text: str, out_path: Path, *, api_key: str, base_url: str, model: str, voice: str, audio_format: str) -> None:
    payload = {
        "model": model,
        "voice": voice,
        "input": text,
        "format": audio_format,
    }
    data = json.dumps(payload).encode("utf-8")
    req = request.Request(
        base_url.rstrip("/") + "/audio/speech",
        data=data,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with request.urlopen(req, timeout=300) as resp:
        out_path.write_bytes(resp.read())


def concat_mp3s(parts: list[Path], out_path: Path) -> None:
    with tempfile.TemporaryDirectory(prefix="tts-concat-") as td:
        list_file = Path(td) / "inputs.txt"
        list_file.write_text("".join(f"file '{p.as_posix()}'\n" for p in parts), encoding="utf-8")
        run_cmd([
            "ffmpeg",
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(list_file),
            "-c",
            "copy",
            str(out_path),
        ])


def default_output_path(source_file: str | None) -> Path:
    if source_file:
        return Path(source_file).expanduser().with_suffix(".mp3")
    return Path.cwd() / "speech.mp3"


def main() -> int:
    parser = argparse.ArgumentParser(description="Convert text into spoken MP3 audio with OpenAI TTS.")
    parser.add_argument("--text", help="Direct text to synthesize")
    parser.add_argument("--file", help="Path to a text or markdown file")
    parser.add_argument("--stdin", action="store_true", help="Read text from stdin")
    parser.add_argument("--out", help="Output MP3 path")
    parser.add_argument("--voice", help="Override voice")
    parser.add_argument("--model", help="Override TTS model")
    parser.add_argument("--max-chars", type=int, default=DEFAULT_MAX_CHARS, help="Max chars per API chunk")
    args = parser.parse_args()

    try:
        api_key, base_url, default_model, default_voice = resolve_tts_config()
        if not api_key:
            raise RuntimeError("Missing OpenAI API key for TTS")

        input_text = normalize_text(read_input_text(args))
        if not input_text:
            raise RuntimeError("Input text is empty")

        model = args.model or default_model
        voice = args.voice or default_voice
        out_path = Path(args.out).expanduser().resolve() if args.out else default_output_path(args.file)
        out_path.parent.mkdir(parents=True, exist_ok=True)

        chunks = chunk_text(input_text, max_chars=max(500, args.max_chars))
        eprint(f"Synthesizing {len(chunks)} chunk(s)")

        with tempfile.TemporaryDirectory(prefix="tts-") as td:
            td_path = Path(td)
            parts: list[Path] = []
            for i, chunk in enumerate(chunks, start=1):
                part = td_path / f"part_{i:03d}.{DEFAULT_FORMAT}"
                eprint(f"Chunk {i}/{len(chunks)}")
                synthesize_chunk(
                    chunk,
                    part,
                    api_key=api_key,
                    base_url=base_url,
                    model=model,
                    voice=voice,
                    audio_format=DEFAULT_FORMAT,
                )
                parts.append(part)

            if len(parts) == 1:
                out_path.write_bytes(parts[0].read_bytes())
            else:
                concat_mp3s(parts, out_path)

        print(str(out_path))
        return 0

    except Exception as e:
        eprint(f"Error: {e}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
