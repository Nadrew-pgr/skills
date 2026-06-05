#!/usr/bin/env python3
from pathlib import Path
import os
import sys

root = Path(__file__).resolve().parents[2]
target = root / 'speech' / 'scripts' / 'tts.py'
os.execvp('python3', ['python3', str(target), *sys.argv[1:]])
