#!/usr/bin/env python3
import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path


def clean_vtt(content: str) -> str:
    lines = content.splitlines()
    text_lines = []
    timestamp_pattern = re.compile(r'\d{2}:\d{2}:\d{2}\.\d{3}\s-->\s\d{2}:\d{2}:\d{2}\.\d{3}')

    for line in lines:
        line = line.strip()
        if not line or line == 'WEBVTT' or line.isdigit():
            continue
        if timestamp_pattern.match(line):
            continue
        if line.startswith('NOTE') or line.startswith('STYLE'):
            continue
        if text_lines and text_lines[-1] == line:
            continue
        line = re.sub(r'<[^>]+>', '', line)
        text_lines.append(line)

    return '\n'.join(text_lines)


def run_cmd(cmd: list[str], cwd: str | None = None) -> subprocess.CompletedProcess:
    try:
        return subprocess.run(cmd, cwd=cwd, check=True, capture_output=True, text=True)
    except FileNotFoundError as e:
        raise RuntimeError(f"Missing required binary: {cmd[0]}") from e
    except subprocess.CalledProcessError as e:
        stderr = (e.stderr or '').strip()
        stdout = (e.stdout or '').strip()
        detail = stderr or stdout or str(e)
        raise RuntimeError(detail) from e


def try_ytdlp_subtitles(url: str, temp_dir: str) -> str | None:
    cmd = [
        'yt-dlp',
        '--no-playlist',
        '--write-subs',
        '--write-auto-subs',
        '--skip-download',
        '--sub-langs', 'en.*,en',
        '--convert-subs', 'vtt',
        '--output', 'subs',
        url,
    ]
    run_cmd(cmd, cwd=temp_dir)

    temp_path = Path(temp_dir)
    vtt_files = sorted(temp_path.glob('*.vtt'))
    if not vtt_files:
        return None

    content = vtt_files[0].read_text(encoding='utf-8', errors='replace')
    clean_text = clean_vtt(content).strip()
    return clean_text or None


def download_audio(url: str, temp_dir: str) -> Path:
    cmd = [
        'yt-dlp',
        '--no-playlist',
        '-f', 'bestaudio/best',
        '--output', 'audio.%(ext)s',
        url,
    ]
    run_cmd(cmd, cwd=temp_dir)

    temp_path = Path(temp_dir)
    audio_files = [
        p for p in temp_path.glob('audio.*')
        if p.is_file() and p.suffix.lower() not in {'.part', '.tmp', '.json', '.vtt', '.srt'}
    ]
    if not audio_files:
        raise RuntimeError('Audio download finished but no audio file was found.')
    return sorted(audio_files)[0]


def load_openclaw_config() -> dict:
    candidates = []
    env_path = os.getenv('OPENCLAW_CONFIG_PATH')
    if env_path:
        candidates.append(Path(env_path).expanduser())
    candidates.extend([
        Path.home() / '.openclaw' / 'openclaw.json',
        Path('/root/.openclaw/openclaw.json'),
        Path('/home/node/.openclaw/openclaw.json'),
    ])

    for path in candidates:
        if path.exists():
            try:
                return json.loads(path.read_text(encoding='utf-8'))
            except Exception:
                continue
    return {}


def resolve_openai_credentials() -> tuple[str | None, str | None]:
    api_key = os.getenv('OPENAI_API_KEY')
    base_url = os.getenv('OPENAI_BASE_URL')
    if api_key:
        return api_key, base_url

    config = load_openclaw_config()

    skill_api_key = (
        config.get('skills', {})
        .get('entries', {})
        .get('openai-whisper-api', {})
        .get('apiKey')
    )
    if isinstance(skill_api_key, str) and skill_api_key:
        return skill_api_key, base_url

    tts_openai = (
        config.get('messages', {})
        .get('tts', {})
        .get('providers', {})
        .get('openai', {})
    )
    tts_api_key = tts_openai.get('apiKey')
    tts_base_url = tts_openai.get('baseUrl')
    if isinstance(tts_api_key, str) and tts_api_key:
        return tts_api_key, tts_base_url or base_url

    return None, base_url


def transcribe_audio(audio_path: Path, temp_dir: str, language: str = 'en') -> str:
    whisper_script = Path('/app/skills/openai-whisper-api/scripts/transcribe.sh')
    if not whisper_script.exists():
        raise RuntimeError('Whisper API helper script not found at /app/skills/openai-whisper-api/scripts/transcribe.sh')

    api_key, base_url = resolve_openai_credentials()
    if not api_key:
        raise RuntimeError('No ASR backend credentials found. Set OPENAI_API_KEY or configure openai-whisper-api.')

    out_path = Path(temp_dir) / 'transcript.txt'
    env = os.environ.copy()
    env['OPENAI_API_KEY'] = api_key
    if base_url:
        env['OPENAI_BASE_URL'] = base_url

    cmd = [str(whisper_script), str(audio_path), '--out', str(out_path), '--language', language]
    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True, env=env)
    except subprocess.CalledProcessError as e:
        stderr = (e.stderr or '').strip()
        stdout = (e.stdout or '').strip()
        detail = stderr or stdout or str(e)
        raise RuntimeError(f'Audio transcription failed: {detail}') from e

    if not out_path.exists():
        raise RuntimeError('ASR command finished but transcript output file was not created.')

    text = out_path.read_text(encoding='utf-8', errors='replace').strip()
    if not text:
        raise RuntimeError('ASR produced an empty transcript.')
    return text


def get_transcript(url: str, language: str = 'en'):
    with tempfile.TemporaryDirectory() as temp_dir:
        subtitle_error = None
        try:
            subtitle_text = try_ytdlp_subtitles(url, temp_dir)
            if subtitle_text:
                print(subtitle_text)
                return
        except Exception as e:
            subtitle_error = str(e)

        try:
            audio_path = download_audio(url, temp_dir)
            transcript = transcribe_audio(audio_path, temp_dir=temp_dir, language=language)
            print(transcript)
            return
        except Exception as audio_error:
            parts = ['Transcript retrieval failed.']
            if subtitle_error:
                parts.append(f'Subtitles path error: {subtitle_error}')
            parts.append(f'Audio fallback error: {audio_error}')
            raise RuntimeError(' '.join(parts)) from audio_error


def main():
    parser = argparse.ArgumentParser(description='Fetch YouTube transcript, with audio fallback.')
    parser.add_argument('url', help='YouTube video URL')
    parser.add_argument('--language', default='en', help='Preferred transcription language (default: en)')
    args = parser.parse_args()

    try:
        get_transcript(args.url, language=args.language)
    except Exception as e:
        print(f'Error: {e}', file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
