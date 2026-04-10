#!/usr/bin/env python3
"""
기존 Voice Design 보이스를 삭제하고, 실제 페이커 음성 샘플로 IVC 클로닝
"""
import os, json
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

VOICE_IDS_FILE = Path(__file__).parent.parent / "packs" / "faker" / ".voice_ids.json"
SAMPLE_FILE    = Path(__file__).parent.parent / "packs" / "faker" / "sample_voice.mp3"
VOICE_NAME     = "Faker-LEE-Sang-hyeok"

# 기존 Voice Design ID 로드
existing = json.loads(VOICE_IDS_FILE.read_text()) if VOICE_IDS_FILE.exists() else {}
old_voice_id = existing.get("faker")

# Step 1: 기존 보이스 삭제
if old_voice_id:
    print(f"Step 1. 기존 Voice Design 삭제: {old_voice_id}")
    try:
        client.voices.delete(old_voice_id)
        print("  삭제 완료")
    except Exception as e:
        print(f"  삭제 실패 (이미 없을 수도): {e}")
else:
    print("Step 1. 삭제할 기존 보이스 없음")

# Step 2: IVC 클로닝
print(f"\nStep 2. IVC 클로닝 — {SAMPLE_FILE.name}")
with open(SAMPLE_FILE, "rb") as f:
    voice = client.voices.ivc.create(
        name=VOICE_NAME,
        description="페이커(이상혁) T1 실제 음성 샘플 기반 클로닝",
        files=[f],
    )

voice_id = voice.voice_id
print(f"  voice_id: {voice_id}")

# Step 3: ID 저장
VOICE_IDS_FILE.write_text(json.dumps({"faker": voice_id}, indent=2))
print(f"  ID 저장됨: {VOICE_IDS_FILE}")

print(f"""
✅ IVC 클로닝 완료!

🔗 ElevenLabs에서 들어보기:
   https://elevenlabs.io/app/voice-lab/{voice_id}

Voice ID: {voice_id}
""")
