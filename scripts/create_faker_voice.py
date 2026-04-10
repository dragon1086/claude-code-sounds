#!/usr/bin/env python3
"""
create_faker_voice.py
ElevenLabs Voice Design으로 페이커(이상혁) 캐릭터 보이스 생성

Usage:
    pip install elevenlabs python-dotenv
    python scripts/create_faker_voice.py
"""

import os
import sys
from pathlib import Path

# .env 로드
env_path = Path(__file__).parent.parent / ".env"
if env_path.exists():
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())

try:
    from elevenlabs.client import ElevenLabs
except ImportError:
    print("❌ elevenlabs 패키지가 없습니다.")
    print("   pip install elevenlabs")
    sys.exit(1)

api_key = os.environ.get("ELEVENLABS_API_KEY")
if not api_key:
    print("❌ ELEVENLABS_API_KEY가 없습니다.")
    sys.exit(1)

# ──────────────────────────────────────────────
# 페이커 Voice Design 프롬프트
# ──────────────────────────────────────────────
# 리서치 기반:
# - 28세 한국 남성, 서울 표준어
# - 침착하고 절제된 목소리 — 절대 흥분하지 않음
# - 겸손하고 진중한 톤, 과장 없음
# - 말 수가 적고 핵심만 전달, 자연스러운 정지(pause)
# - 인게임: 냉철하고 전략적, 짧은 콜
# - 인터뷰: 더 차분하고 성실함
# - 건조한 유머가 가끔 섞임 (표정 없이 농담)
FAKER_VOICE_DESCRIPTION = (
    "Korean male voice, 28 years old, Seoul standard dialect. "
    "Extremely calm and composed — the voice of someone who has been the world's best at their craft for over a decade. "
    "Speaks with deliberate, measured pacing and natural thoughtful pauses. "
    "Minimal emotional inflection; stoic but warm underneath. "
    "Humble and understated — never boastful, never rushed. "
    "Precise and clear articulation, as if every word is chosen carefully. "
    "Slight dry humor delivered completely deadpan. "
    "The composed authority of an elite esports legend who lets performance speak louder than words."
)

FAKER_VOICE_NAME = "Faker-LEE-Sang-hyeok"

def main():
    client = ElevenLabs(api_key=api_key)

    print("🎮 페이커(이상혁) 보이스 생성 중...\n")
    print(f"Voice Description:\n  {FAKER_VOICE_DESCRIPTION}\n")

    # Step 1: 프리뷰 생성
    print("Step 1. Voice Design 프리뷰 생성...")
    try:
        previews = client.text_to_voice.create_previews(
            voice_description=FAKER_VOICE_DESCRIPTION,
            auto_generate_text=True,
        )
    except Exception as e:
        print(f"❌ 프리뷰 생성 실패: {e}")
        sys.exit(1)

    generated_voice_id = previews.previews[0].generated_voice_id
    print(f"  generated_voice_id: {generated_voice_id}")

    # Step 2: 영구 보이스로 저장
    print(f"\nStep 2. '{FAKER_VOICE_NAME}' 보이스로 저장...")
    try:
        voice = client.text_to_voice.create(
            voice_name=FAKER_VOICE_NAME,
            voice_description=FAKER_VOICE_DESCRIPTION,
            generated_voice_id=generated_voice_id,
        )
    except Exception as e:
        print(f"❌ 보이스 저장 실패: {e}")
        sys.exit(1)

    voice_id = voice.voice_id
    print(f"  voice_id: {voice_id}")

    # voice_id 저장
    voice_ids_path = Path(__file__).parent.parent / "packs" / "faker" / ".voice_ids.json"
    voice_ids_path.parent.mkdir(parents=True, exist_ok=True)
    import json
    voice_ids_path.write_text(json.dumps({"faker": voice_id}, indent=2))
    print(f"  ID 저장됨: {voice_ids_path}")

    print(f"""
✅ 페이커 보이스 생성 완료!

🔗 ElevenLabs에서 들어보기:
   https://elevenlabs.io/app/voice-lab/{voice_id}

   또는 Voice Library 전체:
   https://elevenlabs.io/app/voice-lab

Voice ID: {voice_id}
""")


if __name__ == "__main__":
    main()
