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
        # 田中真弓 스타일: 여성 성우가 연기하는 소년 목소리, 거칠고 에너지 넘침
        "description": "Young boy voice performed by a female voice actress in classic Japanese anime style, very rough and raspy texture, extremely energetic and carefree, shouts with wild enthusiasm, slightly hoarse from constant yelling, rubbery loose quality, exaggerated vowels, zero hesitation, pure raw passion like a shounen protagonist screaming attack names",
        "name": "OP-Luffy",
    },
    "zoro": {
        # 中井和哉 스타일: 낮고 거친 남성 목소리, 과묵하고 결연함
        "description": "Deep gruff adult male voice, extremely low pitch, rough gravelly texture, samurai warrior energy, speaks only when necessary with absolute conviction, stoic and unyielding, no warmth or humor, heavy deliberate pacing, the voice of someone who has survived countless near-death battles",
        "name": "OP-Zoro",
    },
    "franky": {
        # 矢尾一樹 스타일: 매우 크고 과장된, 사이보그 느낌
        "description": "Extremely loud boisterous adult male voice, over-the-top exaggerated anime style, bombastic and theatrical, cyborg robot-like metallic edge, shouts SUPER with explosive enthusiasm, very wide dynamic range from normal speech to sudden yelling, flamboyant and dramatic, American-delinquent-turned-cyborg energy",
        "name": "OP-Franky",
    },
    "robin": {
        # 山口由里子 스타일: 차분하고 성숙한 여성, 약간 어두운 저음
        "description": "Calm sophisticated adult female voice, low and slightly husky for a woman, measured and deliberate speech, scholarly and mysterious undertone, emotionally restrained but with hidden depth, elegant and composed, the kind of voice that says terrifying things in a gentle matter-of-fact tone",
        "name": "OP-Robin",
    },
    "shanks": {
        # 池田秀一 스타일: 따뜻하고 카리스마 있는 성숙한 남성
        "description": "Warm charismatic adult male voice, mid-to-low pitch with natural authority, legendary pirate captain energy, deeply reassuring yet powerful, speaks with unhurried confidence, gentle smile in the voice, the kind of person whose calm words carry the weight of mountains",
        "name": "OP-Shanks",
    },
    "sanji": {
        # 平田広明 스타일: 쿨하고 세련된 남성, 로맨틱하고 극적
        "description": "Cool suave adult male voice, smooth and slightly smoky texture, chivalrous and dramatic, passionate intensity when speaking of women or cooking, effortlessly stylish, slight French-inspired flair, can shift instantly from composed to fiery, the voice of a chef who is also a deadly martial artist",
        "name": "OP-Sanji",
    },
    "usopp": {
        # 山口勝平 스타일: 극적이고 코믹한 젊은 남성, 겁쟁이이지만 영웅적
        "description": "Young adult male voice, highly expressive and comedic, starts sentences with exaggerated fear and panic then pivots to dramatic heroic proclamations, storyteller energy, slightly nasally, wide pitch range for comedic effect, the voice of someone who is terrified but forces himself to be brave anyway",
        "name": "OP-Usopp",
    },
    "brook": {
        # チョー 스타일: 나이 든 연극적인 남성, 유령 같고 기이함
        "description": "Elderly theatrical male voice, slightly ghostly and hollow quality, old-fashioned formal Japanese speech patterns, dramatic pauses before punchlines, whimsical and eccentric, warm despite the eerie undertone, the voice of a skeleton musician who has been alone for fifty years and now laughs at his own death jokes",
        "name": "OP-Brook",
    },
    "chopper": {
        # 大谷育江 스타일: 매우 높은 여성 목소리로 연기하는 어린 캐릭터
        "description": "Very high-pitched childlike voice performed by a female voice actress, tiny and innocent, earnest and sincere, easily flustered and excited, squeaky when surprised, gentle and kind-hearted, the voice of a small fluffy creature who is secretly a genius doctor but still acts like a child getting praised",
        "name": "OP-Chopper",
    },
    "nami": {
        # 岡村明美 스타일: 날카롭고 자신감 있는 젊은 여성
        "description": "Sharp assertive young adult female voice, bright and clear tone, practical and no-nonsense delivery, can shift instantly from friendly to scolding, slightly whiny when complaining about money, confident navigator energy, the voice of someone who is both the brains of the crew and perfectly willing to hit everyone when they're being idiots",
        "name": "OP-Nami",
    },
    "whitebeard": {
        # 内海賢二 스타일: 매우 낮고 거대한 목소리, 황제의 위엄
        "description": "Massively deep booming elderly male voice, the lowest possible pitch range, enormous gravelly resonance that feels like the earth shaking, slow powerful cadence, absolute authority with no need to raise his voice, the legendary voice of someone called the strongest man in the world, speaks with finality",
        "name": "OP-Whitebeard",
    },
    "roger": {
        # 키타무라 에리코 / 오가타 켄이치 스타일: 카리스마 넘치는 전설의 해적왕
        "description": "Charismatic legendary adult male voice, adventurous and magnetic, bold and fearless, laughs easily with genuine joy, the voice of someone who conquered the entire world and finds it all a grand adventure, historically grand and mythic quality, speaks as if every word is an invitation to the greatest journey imaginable",
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
    "userpromptsubmit":   ("luffy",      "仲間がいるよ！！！"),
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
