#!/usr/bin/env python3
"""
generate_onepiece_pack.py
ElevenLabs API로 One Piece 사운드팩 자동 생성

Usage:
    pip install elevenlabs
    export ELEVENLABS_API_KEY="your_api_key_here"
    python scripts/generate_onepiece_pack.py

Options:
    --voices-only   보이스 생성만 (오디오 생성 건너뜀)
    --audio-only    오디오 생성만 (보이스 이미 있을 때)
    --dry-run       실제 API 호출 없이 파일 구조만 출력
"""

import os
import json
import time
import argparse
from pathlib import Path

# ──────────────────────────────────────────────
# 설정
# ──────────────────────────────────────────────

PACK_DIR = Path(__file__).parent.parent / "packs" / "onepiece"
VOICE_IDS_FILE = PACK_DIR / ".voice_ids.json"   # 생성된 Voice ID 캐시 (git-ignored)

# 캐릭터별 ElevenLabs Voice Design 프롬프트
CHARACTER_VOICES = {
    "luffy": {
        "description": "Energetic young male voice, rough and carefree tone, enthusiastic shounen anime protagonist, slightly hoarse, Japanese-style speech patterns, loud and expressive",
        "name": "OP-Luffy",
    },
    "zoro": {
        "description": "Stoic deep calm male voice, serious and reserved, samurai-like, minimal words, low pitch, speaks rarely but with conviction",
        "name": "OP-Zoro",
    },
    "franky": {
        "description": "Loud boisterous energetic male voice, robot-cyborg-like, over-enthusiastic, dramatic, loves exclamation",
        "name": "OP-Franky",
    },
    "robin": {
        "description": "Calm intelligent mature female voice, soft-spoken, scholarly and slightly mysterious, elegant and composed",
        "name": "OP-Robin",
    },
    "shanks": {
        "description": "Warm confident mature male voice, legendary aura, gentle but powerful, wise and composed",
        "name": "OP-Shanks",
    },
    "sanji": {
        "description": "Cool suave male voice, dramatic and chivalrous, slightly over-the-top, charming and passionate",
        "name": "OP-Sanji",
    },
    "usopp": {
        "description": "Cowardly but brave young male voice, over-dramatic storyteller, panicky at first then heroic, comedic timing",
        "name": "OP-Usopp",
    },
    "brook": {
        "description": "Old theatrical male voice, ghostly eccentric skeleton musician, laughs with Yohoho, dramatic and whimsical",
        "name": "OP-Brook",
    },
    "chopper": {
        "description": "Cute high-pitched innocent voice, small earnest and sweet character, slightly squeaky, kind and gentle tone",
        "name": "OP-Chopper",
    },
    "nami": {
        "description": "Sharp assertive young female voice, practical navigator, slightly bossy and confident, direct",
        "name": "OP-Nami",
    },
    "whitebeard": {
        "description": "Massive deep booming male voice, legendary elder pirate king, powerful and commanding, gravelly",
        "name": "OP-Whitebeard",
    },
    "roger": {
        "description": "Legendary charismatic male voice, the original pirate king, adventurous and magnetic, historically grand",
        "name": "OP-Roger",
    },
}

# 이벤트별 (캐릭터, 대사) 매핑
EVENTS = {
    "sessionstart":       ("luffy",      "海賊王に俺はなる！"),
    "setup":              ("roger",      "おれの財宝か？欲しけりゃくれてやるぜ、探してみろ！"),
    "stop":               ("franky",     "スーパー！"),
    "stopfailure":        ("robin",      "生きていたい！"),
    "pretooluse":         ("luffy",      "ゴムゴムの…！"),
    "posttooluse":        ("franky",     "改造完了！スーパー！"),
    "posttoolusefailure": ("zoro",       "背中の傷は剣士の恥だ"),
    "userpromptsubmit":   ("luffy",      "おれは助けてもらわねェと生きていけねェ自信がある！"),
    "notification":       ("usopp",      "今からおれが伝説のヒーローになってやる！"),
    "permissionrequest":  ("sanji",      "たとえ死んでもおれは女は蹴らん！"),
    "permissiondenied":   ("luffy",      "この海で一番自由な奴が海賊王だ！"),
    "sessionend":         ("shanks",     "この帽子をお前に預ける…立派な海賊になってな"),
    "subagentstart":      ("luffy",      "俺の仲間になれ！！"),
    "subagentstop":       ("zoro",       "ルフィは海賊王になる男だ！！！"),
    "taskcreated":        ("robin",      "また新しい謎が…！"),
    "taskcompleted":      ("zoro",       "…終わったか"),
    "teammateidle":       ("zoro",       "ちょっと寝てていいか？"),
    "cwdchanged":         ("zoro",       "また迷子か…"),
    "filechanged":        ("franky",     "改造完了！"),
    "worktreecreate":     ("luffy",      "新しい島だ！"),
    "worktreeremove":     ("brook",      "さらばじゃ…ヨホホ"),
    "precompact":         ("robin",      "歴史を整理しましょう"),
    "postcompact":        ("robin",      "準備ができました"),
    "instructionsloaded": ("whitebeard", "ワンピースは実在する！"),
    "configchange":       ("nami",       "航路を変更したわ"),
    "elicitation":        ("chopper",    "教えてもらえますか？"),
    "elicitationresult":  ("luffy",      "そうか！わかった！"),
}


# ──────────────────────────────────────────────
# 헬퍼
# ──────────────────────────────────────────────

def load_voice_ids() -> dict:
    if VOICE_IDS_FILE.exists():
        return json.loads(VOICE_IDS_FILE.read_text())
    return {}


def save_voice_ids(ids: dict):
    VOICE_IDS_FILE.parent.mkdir(parents=True, exist_ok=True)
    VOICE_IDS_FILE.write_text(json.dumps(ids, indent=2, ensure_ascii=False))
    print(f"  Voice IDs 저장됨: {VOICE_IDS_FILE}")


def create_pack_json():
    pack_json = {
        "name": "onepiece",
        "author": "claude-code-sounds",
        "description": "One Piece character voice pack — iconic quotes from Luffy, Zoro, Robin, Franky and more",
        "license": "MIT",
        "preview_url": ""
    }
    pack_path = PACK_DIR / "pack.json"
    pack_path.parent.mkdir(parents=True, exist_ok=True)
    pack_path.write_text(json.dumps(pack_json, indent=2, ensure_ascii=False) + "\n")
    print(f"  pack.json 생성됨")


# ──────────────────────────────────────────────
# Phase 1: 보이스 생성
# ──────────────────────────────────────────────

def create_voices(client, dry_run=False) -> dict:
    """캐릭터별 Voice Design으로 보이스 생성, Voice ID 반환"""
    voice_ids = load_voice_ids()

    for char, cfg in CHARACTER_VOICES.items():
        if char in voice_ids:
            print(f"  ✓ {char}: 이미 존재 ({voice_ids[char]})")
            continue

        print(f"  → {char} 보이스 생성 중...")
        if dry_run:
            voice_ids[char] = f"DRY_RUN_{char.upper()}"
            print(f"    [DRY RUN] voice_id = {voice_ids[char]}")
            continue

        try:
            # Step 1: 프리뷰 생성
            previews = client.text_to_voice.create_previews(
                voice_description=cfg["description"],
                auto_generate_text=True,
            )
            generated_voice_id = previews.previews[0].generated_voice_id

            # Step 2: 프리뷰 → 영구 보이스 저장
            voice = client.text_to_voice.create(
                voice_name=cfg["name"],
                voice_description=cfg["description"],
                generated_voice_id=generated_voice_id,
            )
            voice_ids[char] = voice.voice_id
            print(f"    voice_id = {voice.voice_id}")

            # API rate limit 방지
            time.sleep(1)

        except Exception as e:
            print(f"    ✗ 실패: {e}")
            continue

    save_voice_ids(voice_ids)
    return voice_ids


# ──────────────────────────────────────────────
# Phase 2: 오디오 생성
# ──────────────────────────────────────────────

def generate_audio(client, voice_ids: dict, dry_run=False):
    """이벤트별 대사를 TTS로 생성, 파일 저장"""
    sounds_dir = PACK_DIR / "sounds"

    for event, (char, text) in EVENTS.items():
        out_dir = sounds_dir / event
        out_dir.mkdir(parents=True, exist_ok=True)
        out_file = out_dir / f"{event}.mp3"

        if out_file.exists():
            print(f"  ✓ {event}: 이미 존재")
            continue

        voice_id = voice_ids.get(char)
        if not voice_id:
            print(f"  ✗ {event}: {char} voice_id 없음 — 건너뜀")
            continue

        print(f"  → [{char}] {event}: {text[:30]}...")
        if dry_run:
            out_file.write_bytes(b"")  # 빈 파일로 구조 확인
            print(f"    [DRY RUN] {out_file}")
            continue

        try:
            audio_generator = client.text_to_speech.convert(
                text=text,
                voice_id=voice_id,
                model_id="eleven_multilingual_v2",
                output_format="mp3_44100_128",
            )
            audio_bytes = b"".join(audio_generator)
            out_file.write_bytes(audio_bytes)
            print(f"    저장됨: {out_file} ({len(audio_bytes):,} bytes)")

            time.sleep(0.5)  # rate limit

        except Exception as e:
            print(f"    ✗ 실패: {e}")


# ──────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="One Piece 사운드팩 자동 생성")
    parser.add_argument("--voices-only", action="store_true", help="보이스 생성만")
    parser.add_argument("--audio-only",  action="store_true", help="오디오 생성만")
    parser.add_argument("--dry-run",     action="store_true", help="API 호출 없이 구조만 출력")
    args = parser.parse_args()

    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key and not args.dry_run:
        print("❌ ELEVENLABS_API_KEY 환경 변수를 설정하세요.")
        print("   export ELEVENLABS_API_KEY='your_key_here'")
        return

    if args.dry_run:
        client = None
    else:
        try:
            from elevenlabs.client import ElevenLabs
            client = ElevenLabs(api_key=api_key)
        except ImportError:
            print("❌ elevenlabs 패키지가 없습니다. 설치하세요:")
            print("   pip install elevenlabs")
            return

    print("\n🏴‍☠️ One Piece 사운드팩 생성 시작\n")
    create_pack_json()

    if not args.audio_only:
        print("\n[Phase 1] 캐릭터 보이스 생성")
        voice_ids = create_voices(client, dry_run=args.dry_run)
    else:
        voice_ids = load_voice_ids()
        if not voice_ids:
            print("❌ .voice_ids.json 없음. --voices-only 먼저 실행하세요.")
            return

    if not args.voices_only:
        print("\n[Phase 2] 이벤트 오디오 생성")
        generate_audio(client, voice_ids, dry_run=args.dry_run)

    print("\n✅ 완료!")
    print(f"   팩 위치: {PACK_DIR}")
    print(f"   적용 명령어: claude-sounds use onepiece")


if __name__ == "__main__":
    main()
