#!/usr/bin/env python3
"""
Transcribe local audio or video files with OpenAI Whisper.

This helper normalizes media with ffmpeg, auto-splits long files,
and delegates actual speech-to-text requests to the built-in
/app/skills/openai-whisper-api/scripts/transcribe.sh helper.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

MAX_UPLOAD_BYTES = 24 * 1024 * 1024
DEFAULT_CHUNK_SECONDS = 20 * 60
WHISPER_HELPER = Path("/app/skills/openai-whisper-api/scripts/transcribe.sh")
CONFIG_CANDIDATES = [
    Path(os.getenv("OPENCLAW_CONFIG_PATH", "")).expanduser() if os.getenv("OPENCLAW_CONFIG_PATH") else None,
    Path.home() / ".openclaw" / "openclaw.json",
    Path("/home/node/.openclaw/openclaw.json"),
    Path("/root/.openclaw/openclaw.json"),
]


def eprint(*args: object) -> None:
    print(*args, file=sys.stderr)


def run_cmd(cmd: list[str], env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(cmd, check=True, capture_output=True, text=True, env=env)
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


def resolve_openai_credentials() -> tuple[str | None, str | None]:
    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL")
    if api_key:
        return api_key, base_url

    config = load_openclaw_config()

    candidates = [
        dig(config, "skills", "openai-whisper-api", "apiKey"),
        dig(config, "skills", "entries", "openai-whisper-api", "apiKey"),
        dig(config, "messages", "tts", "providers", "openai", "apiKey"),
        dig(config, "providers", "openai", "apiKey"),
    ]
    for candidate in candidates:
        if isinstance(candidate, str) and candidate:
            resolved_base_url = base_url or dig(config, "messages", "tts", "providers", "openai", "baseUrl") or dig(config, "providers", "openai", "baseUrl")
            return candidate, resolved_base_url

    return None, base_url


def ensure_requirements() -> None:
    if not WHISPER_HELPER.exists():
        raise RuntimeError(f"Whisper helper not found: {WHISPER_HELPER}")
    run_cmd(["ffmpeg", "-version"])


def default_output_path(input_path: Path, json_mode: bool) -> Path:
    return input_path.with_suffix(".json" if json_mode else ".txt")


def normalize_media(input_path: Path, temp_dir: Path) -> Path:
    normalized = temp_dir / "normalized.m4a"
    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        str(input_path),
        "-vn",
        "-ac",
        "1",
        "-ar",
        "16000",
        "-c:a",
        "aac",
        "-b:a",
        "96k",
        str(normalized),
    ]
    run_cmd(cmd)
    if not normalized.exists() or normalized.stat().st_size == 0:
        raise RuntimeError("Media normalization failed: no output audio was created.")
    return normalized


def split_audio(audio_path: Path, temp_dir: Path, chunk_seconds: int) -> list[Path]:
    parts_dir = temp_dir / "parts"
    parts_dir.mkdir(parents=True, exist_ok=True)
    pattern = parts_dir / "part_%03d.m4a"
    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        str(audio_path),
        "-f",
        "segment",
        "-segment_time",
        str(chunk_seconds),
        "-reset_timestamps",
        "1",
        "-c",
        "copy",
        str(pattern),
    ]
    run_cmd(cmd)
    parts = sorted(parts_dir.glob("part_*.m4a"))
    if not parts:
        raise RuntimeError("Audio splitting failed: no chunks were created.")
    return parts


def build_transcribe_env() -> dict[str, str]:
    api_key, base_url = resolve_openai_credentials()
    if not api_key:
        raise RuntimeError("Missing OpenAI credentials. OPENAI_API_KEY is not set and no usable OpenClaw config key was found.")
    env = os.environ.copy()
    env["OPENAI_API_KEY"] = api_key
    if base_url:
        env["OPENAI_BASE_URL"] = base_url
    return env


def transcribe_one(audio_path: Path, out_path: Path, *, model: str, language: str | None, prompt: str | None, json_mode: bool, env: dict[str, str]) -> Any:
    cmd = [str(WHISPER_HELPER), str(audio_path), "--model", model, "--out", str(out_path)]
    if language:
        cmd += ["--language", language]
    if prompt:
        cmd += ["--prompt", prompt]
    if json_mode:
        cmd.append("--json")

    run_cmd(cmd, env=env)

    if not out_path.exists():
        raise RuntimeError(f"Transcription finished but output was not created: {out_path}")

    content = out_path.read_text(encoding="utf-8", errors="replace")
    if json_mode:
        try:
            return json.loads(content)
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Transcription returned invalid JSON for {audio_path.name}") from e
    return content.strip()


def combine_outputs(input_path: Path, outputs: list[Any], *, json_mode: bool) -> str:
    if json_mode:
        combined_text = "\n\n".join(
            chunk.get("text", "").strip()
            for chunk in outputs
            if isinstance(chunk, dict)
        ).strip()
        payload = {
            "source": str(input_path),
            "chunkCount": len(outputs),
            "text": combined_text,
            "chunks": outputs,
        }
        return json.dumps(payload, ensure_ascii=False, indent=2)

    cleaned = [str(chunk).strip() for chunk in outputs if str(chunk).strip()]
    return "\n\n".join(cleaned).strip()


def pick_chunks(normalized_path: Path, chunk_seconds: int) -> list[Path]:
    size = normalized_path.stat().st_size
    if size <= MAX_UPLOAD_BYTES:
        return [normalized_path]

    approx_ratio = size / MAX_UPLOAD_BYTES
    adjusted_seconds = max(5 * 60, min(chunk_seconds, math.floor(DEFAULT_CHUNK_SECONDS / math.ceil(approx_ratio))))
    return split_audio(normalized_path, normalized_path.parent, adjusted_seconds)


def main() -> int:
    parser = argparse.ArgumentParser(description="Transcribe local audio or video files with OpenAI Whisper.")
    parser.add_argument("input", help="Path to the audio or video file")
    parser.add_argument("--out", help="Output file path (.txt by default, .json with --json)")
    parser.add_argument("--language", help="Language hint, for example fr or en")
    parser.add_argument("--prompt", help="Optional recognition hint, names, jargon, etc.")
    parser.add_argument("--model", default="whisper-1", help="Transcription model (default: whisper-1)")
    parser.add_argument("--json", action="store_true", help="Write JSON instead of plain text")
    parser.add_argument("--stdout", action="store_true", help="Print the transcript content instead of only the output path")
    args = parser.parse_args()

    input_path = Path(args.input).expanduser().resolve()
    if not input_path.exists() or not input_path.is_file():
        eprint(f"Error: file not found: {input_path}")
        return 1

    try:
        ensure_requirements()
        out_path = Path(args.out).expanduser().resolve() if args.out else default_output_path(input_path, args.json)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        env = build_transcribe_env()

        with tempfile.TemporaryDirectory(prefix="speech-") as temp_dir_raw:
            temp_dir = Path(temp_dir_raw)
            eprint(f"Normalizing media: {input_path.name}")
            normalized = normalize_media(input_path, temp_dir)
            chunks = pick_chunks(normalized, DEFAULT_CHUNK_SECONDS)
            eprint(f"Transcribing {len(chunks)} chunk(s)")

            outputs: list[Any] = []
            for index, chunk in enumerate(chunks, start=1):
                chunk_out = temp_dir / (f"chunk_{index:03d}.json" if args.json else f"chunk_{index:03d}.txt")
                eprint(f"Chunk {index}/{len(chunks)}")
                outputs.append(
                    transcribe_one(
                        chunk,
                        chunk_out,
                        model=args.model,
                        language=args.language,
                        prompt=args.prompt,
                        json_mode=args.json,
                        env=env,
                    )
                )

            final_content = combine_outputs(input_path, outputs, json_mode=args.json)
            out_path.write_text(final_content + ("\n" if final_content and not final_content.endswith("\n") else ""), encoding="utf-8")

        if args.stdout:
            print(final_content)
        else:
            print(str(out_path))
        return 0

    except Exception as e:
        eprint(f"Error: {e}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
