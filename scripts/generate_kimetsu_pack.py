#!/usr/bin/env python3
"""
generate_kimetsu_pack.py
ElevenLabs API로 鬼滅の刃 (귀멸의 칼날) 사운드팩 자동 생성

Usage:
    pip install elevenlabs
    export ELEVENLABS_API_KEY="your_api_key_here"
    python scripts/generate_kimetsu_pack.py

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

PACK_DIR = Path(__file__).parent.parent / "packs" / "kimetsu"
VOICE_IDS_FILE = PACK_DIR / ".voice_ids.json"   # 생성된 Voice ID 캐시 (git-ignored)

# 캐릭터별 ElevenLabs Voice Design 프롬프트
# 원작 성우 스타일을 최대한 재현하는 일본어 특화 프롬프트
CHARACTER_VOICES = {
    "tanjiro": {
        # 花江夏樹 스타일: 진심 어린 소년 목소리, 눈물을 머금은 결의, 따뜻하고 성실함
        "description": "Sincere earnest teenage boy voice in Japanese anime style, warm and emotionally expressive, voice cracks slightly with intense emotion, deeply determined and compassionate, cries easily but pushes through, gentle but firm conviction, the voice of someone who finds the good in everyone including monsters, breathing technique energy when shouting technique names",
        "name": "KM-Tanjiro",
    },
    "rengoku": {
        # 日野聡 스타일: 화염처럼 폭발적인 열정, 엄청난 볼륨, 따뜻한 호탕함
        "description": "Extremely loud and passionate adult male voice in Japanese anime style, volcanic enthusiasm and energy, booming laugh that fills the room, fire-pillar warrior spirit, deeply warm and encouraging despite the overwhelming intensity, shouts with genuine joy especially about food, voice of someone who burns with conviction and wants everyone around them to burn just as brightly",
        "name": "KM-Rengoku",
    },
    "zenitsu": {
        # 下野紘 스타일: 패닉-용기 스펙트럼을 오가는 과장된 표현, 높은 음조
        "description": "Young male voice with extreme dynamic range in Japanese anime style, oscillates between high-pitched terror and sudden cool confidence, whines and wails when frightened, voice climbs several octaves when panicking, unexpectedly drops to calm cool tone for brief moments of genuine bravery, cowardly boy who is secretly lightning-fast, the emotional whiplash is the character",
        "name": "KM-Zenitsu",
    },
    "inosuke": {
        # 岡本信彦 스타일: 야생적이고 공격적인 남성 목소리, 실내용이 없음
        "description": "Wild feral young male voice in Japanese anime style, raised by boars in mountains, absolutely no indoor volume, every statement sounds like a battle cry, aggressively confident even when completely wrong, mispronounces names on purpose out of dominance, rough and untamed texture, the voice of someone who has never had a single social skill but is proud of it",
        "name": "KM-Inosuke",
    },
    "shinobu": {
        # 早見沙織 스타일: 달콤하고 부드러운 목소리로 날카로운 말을 하는 반전 매력
        "description": "Soft sweet feminine voice in Japanese anime style with a permanent gentle smile, liltingly pleasant and warm on the surface, passive-aggressive undertone that makes flattery feel threatening, says cutting remarks in the kindest possible tone, insect pillar elegance, the contrast between the beautiful voice and the actual content is the character's entire personality",
        "name": "KM-Shinobu",
    },
    "giyu": {
        # 櫻井孝宏 스타일: 극도로 말이 없고 단조로운 목소리, 감정을 숨김
        "description": "Extremely sparse adult male voice in Japanese anime style, delivers maximum meaning in minimum words, monotone delivery that occasionally cracks with deeply buried emotion, stoic water pillar energy, uncomfortable with conversation, each word costs visible effort, the kind of person who says one sentence that others spend weeks thinking about",
        "name": "KM-Giyu",
    },
    "muzan": {
        # 関俊彦 스타일: 냉정하고 귀족적인 악당, 속삭이는 듯 하지만 압도적인 위압감
        "description": "Cold aristocratic adult male voice in Japanese anime style, soft-spoken but radiating absolute terror, dismissive and contemptuous of all life, speaks at a near-whisper that somehow carries more menace than shouting, the original demon king, every sentence is a quiet death threat delivered over dinner, effortless dominance without ever raising his voice",
        "name": "KM-Muzan",
    },
    "nezuko": {
        # 鬼頭明里 스타일: 대나무 재갈로 막힌 귀여운 목소리, 비언어적 표현
        "description": "Very high-pitched cute young female voice muffled by a bamboo gag, mostly non-verbal cute sounds and determined murmurs, tiny squeaks of effort and emotion, demon girl who retained her humanity, gentle and protective despite monstrous power, expressive without words, the sounds of someone communicating entirely through adorable determination",
        "name": "KM-Nezuko",
    },
}

# 이벤트별 (캐릭터, 대사, 설명) 매핑
EVENTS = {
    # 세션 시작 — 렌고쿠의 "마음에 불을 질러라!"
    "sessionstart":       ("rengoku",  "心を燃やせ！"),
    # 초기 설정 — 렌고쿠의 불꽃 결의
    "setup":              ("rengoku",  "生まれた時から、炎の呼吸は俺の全てだ！"),
    # 완료 — 렌고쿠의 "우마이!!" (밥 먹는 명장면, 작업 완료의 만족감)
    "stop":               ("rengoku",  "うまい！！"),
    # 실패 종료 — 무잔의 냉혹한 실망
    "stopfailure":        ("muzan",    "失望した"),
    # 도구 사용 전 — 탄지로의 전집중 호흡
    "pretooluse":         ("tanjiro",  "全集中！水の呼吸！"),
    # 도구 사용 후 (성공) — 탄지로의 기쁨
    "posttooluse":        ("tanjiro",  "やった！！"),
    # 도구 사용 후 (실패) — 젠이쓰의 패닉
    "posttoolusefailure": ("zenitsu",  "もう死ぬ！絶対に死ぬ！！"),
    # 사용자 프롬프트 제출 — 탄지로의 성실한 수락
    "userpromptsubmit":   ("tanjiro",  "わかりました！任せてください！"),
    # 알림 — 젠이쓰의 귀신 탐지 경보
    "notification":       ("zenitsu",  "鬼だ！鬼がいる！！"),
    # 권한 요청 — 탄지로의 진심 어린 부탁
    "permissionrequest":  ("tanjiro",  "お願いします！やらせてください！！"),
    # 권한 거부 — 시노부의 미소 거절 (명장면)
    "permissiondenied":   ("shinobu",  "お断りします"),
    # 세션 종료 — 렌고쿠의 마지막 유언 (탄지로에게)
    "sessionend":         ("rengoku",  "胸を張って生きろ"),
    # 서브에이전트 시작 — 이노스케의 등장
    "subagentstart":      ("inosuke",  "俺様が来たぞ！！"),
    # 서브에이전트 종료 — 탄지로의 감사
    "subagentstop":       ("tanjiro",  "ありがとうございました！"),
    # 작업 생성 — 탄지로의 새 임무
    "taskcreated":        ("tanjiro",  "新しい任務です！"),
    # 작업 완료 — 기유의 과묵한 완료 선언
    "taskcompleted":      ("giyu",     "…終わった"),
    # 팀원 대기 — 젠이쓰의 졸음
    "teammateidle":       ("zenitsu",  "眠い…もう少し休ませてください…"),
    # 디렉토리 이동 — 탄지로의 이동
    "cwdchanged":         ("tanjiro",  "次の場所へ向かいます"),
    # 파일 변경 — 이노스케의 감지
    "filechanged":        ("inosuke",  "何かが変わったぞ！！"),
    # 워크트리 생성 — 탄지로의 새 길 개척
    "worktreecreate":     ("tanjiro",  "新しい道を切り開きます！"),
    # 워크트리 제거 — 기유의 냉정한 판단
    "worktreeremove":     ("giyu",     "もう必要ない"),
    # 컴팩트 전 — 탄지로의 전집중 상중
    "precompact":         ("tanjiro",  "全集中の呼吸、常中"),
    # 컴팩트 후 — 탄지로의 준비 완료
    "postcompact":        ("tanjiro",  "準備できました"),
    # 지시 로드 — 렌고쿠의 사제 정신
    "instructionsloaded": ("rengoku",  "師匠の教えを、胸に刻め！"),
    # 설정 변경 — 시노부의 유쾌한 조정
    "configchange":       ("shinobu",  "少し変えてみましょうか"),
    # 입력 요청 — 탄지로의 정중한 질문
    "elicitation":        ("tanjiro",  "一つ教えていただけますか？"),
    # 입력 결과 — 탄지로의 이해
    "elicitationresult":  ("tanjiro",  "そうか！わかりました！"),
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
        "name": "kimetsu",
        "author": "claude-code-sounds",
        "description": "Demon Slayer (鬼滅の刃) voice pack — iconic quotes from Tanjiro, Rengoku, Zenitsu, Inosuke and more",
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

            time.sleep(1)  # API rate limit 방지

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
            out_file.write_bytes(b"")
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
    parser = argparse.ArgumentParser(description="鬼滅の刃 사운드팩 자동 생성")
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

    print("\n🗡️  鬼滅の刃 사운드팩 생성 시작\n")
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
    print(f"   적용 명령어: ./claude-sounds.sh use kimetsu && ./install.sh --force")


if __name__ == "__main__":
    main()
