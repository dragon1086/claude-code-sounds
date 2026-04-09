#!/usr/bin/env python3
"""
CI check: all .wav and .mp3 files under hooks/sounds/ must have lowercase filenames.
"""
import sys
from pathlib import Path

sounds_dir = Path(__file__).parent.parent / "hooks" / "sounds"
errors = []

for f in sounds_dir.rglob("*"):
    if f.is_file() and f.suffix in (".wav", ".mp3"):
        if f.name != f.name.lower():
            errors.append(str(f.relative_to(sounds_dir.parent.parent)))

if errors:
    print("FAIL: non-lowercase audio filenames found:")
    for e in errors:
        print(f"  {e}")
    sys.exit(1)

print("OK: all audio filenames are lowercase")
