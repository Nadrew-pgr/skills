#!/usr/bin/env bash
set -euo pipefail
base_dir="$(cd -- "$(dirname -- "$0")" && pwd)"
exec python3 "$base_dir/tts.py" "$@"
