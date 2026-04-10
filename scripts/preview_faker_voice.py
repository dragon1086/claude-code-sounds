#!/usr/bin/env python3
"""
이미 생성된 generated_voice_id로 샘플 오디오를 로컬에 저장
"""
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

GENERATED_VOICE_ID = "US8NdfNVAnmfkW1SEysr"

SAMPLE_TEXTS = [
    "안녕하세요, 저는 T1 페이커입니다.",
    "열심히 하겠습니다. 잘 부탁드립니다.",
    "아직 부족한 점이 많습니다.",
]

out_dir = Path(__file__).parent.parent / "packs" / "faker" / "preview"
out_dir.mkdir(parents=True, exist_ok=True)

print("🎮 페이커 보이스 샘플 생성 중...\n")

for i, text in enumerate(SAMPLE_TEXTS):
    out_file = out_dir / f"sample_{i+1}.mp3"
    print(f"  [{i+1}] {text}")
    try:
        audio = client.text_to_speech.convert(
            text=text,
            voice_id=GENERATED_VOICE_ID,
            model_id="eleven_multilingual_v2",
            output_format="mp3_44100_128",
        )
        audio_bytes = b"".join(audio)
        out_file.write_bytes(audio_bytes)
        print(f"      → {out_file} ({len(audio_bytes):,} bytes)")
    except Exception as e:
        print(f"      ✗ 실패: {e}")

print(f"\n✅ 저장 완료: {out_dir}")
print("   afplay 명령으로 들어보세요:")
for i in range(len(SAMPLE_TEXTS)):
    print(f"   afplay packs/faker/preview/sample_{i+1}.mp3")
