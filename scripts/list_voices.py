#!/usr/bin/env python3
import os, sys
from pathlib import Path

env_path = Path(__file__).parent.parent / ".env"
if env_path.exists():
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())

from elevenlabs.client import ElevenLabs
client = ElevenLabs(api_key=os.environ["ELEVENLABS_API_KEY"])

voices = client.voices.get_all()
print(f"현재 보이스 ({len(voices.voices)}개):\n")
for v in voices.voices:
    category = getattr(v, 'category', 'unknown')
    print(f"  [{category}] {v.name}")
    print(f"         ID: {v.voice_id}")
