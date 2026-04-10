#!/usr/bin/env python3
"""
generate_faker_pack.py
ElevenLabs IVC 클로닝 보이스로 페이커(이상혁) 사운드팩 자동 생성

Usage:
    python3 scripts/generate_faker_pack.py
    python3 scripts/generate_faker_pack.py --dry-run
"""

import os
import json
import time
import argparse
from pathlib import Path

PACK_DIR       = Path(__file__).parent.parent / "packs" / "faker"
VOICE_IDS_FILE = PACK_DIR / ".voice_ids.json"

# ──────────────────────────────────────────────
# 이벤트 → 대사 매핑
# 실제 페이커 말투 기반: 짧고 절제되고 겸손함
# ──────────────────────────────────────────────
EVENTS = {
    # 세션 시작 — 공식 자기소개
    "sessionstart":       "안녕하세요, 저는 T1 페이커입니다.",
    # 초기 설정 — 준비 완료
    "setup":              "준비됐습니다. 열심히 하겠습니다.",
    # 도구 사용 전 — 짧은 집중 선언
    "pretooluse":         "해볼게요.",
    # 도구 사용 후 성공 — 담담한 완료
    "posttooluse":        "됐네요.",
    # 도구 사용 후 실패 — 특유의 짧은 탄식
    "posttoolusefailure": "아...",
    # 사용자 프롬프트 수락 — 성실한 수락
    "userpromptsubmit":   "알겠습니다, 해볼게요.",
    # 작업 완료 — 우승 후 담담한 반응
    "stop":               "수고하셨습니다.",
    # 작업 실패 종료 — 겸손한 패배 인정
    "stopfailure":        "아직 많이 부족합니다.",
    # 알림 — 간결한 확인
    "notification":       "확인했습니다.",
    # 권한 요청 — 정중한 부탁
    "permissionrequest":  "잘 부탁드립니다.",
    # 권한 거부 — 담담한 수용
    "permissiondenied":   "그렇군요, 알겠습니다.",
    # 세션 종료 — 경기 후 인사
    "sessionend":         "오늘도 수고하셨습니다. T1 화이팅.",
    # 서브에이전트 시작 — 팀 협력
    "subagentstart":      "같이 해봅시다.",
    # 서브에이전트 종료 — 팀원 격려
    "subagentstop":       "수고하셨습니다.",
    # 작업 생성 — 새 목표
    "taskcreated":        "새 임무가 생겼습니다.",
    # 작업 완료 — 간결한 완료
    "taskcompleted":      "완료됐습니다.",
    # 팀원 대기 — 여유로운 대기
    "teammateidle":       "조금만 기다려주세요.",
    # 디렉토리 이동 — 짧은 이동 선언
    "cwdchanged":         "이동합니다.",
    # 파일 변경 감지
    "filechanged":        "변경사항이 있네요.",
    # 워크트리 생성 — 새 시작
    "worktreecreate":     "새로 시작합니다.",
    # 워크트리 제거 — 정리
    "worktreeremove":     "정리됐습니다.",
    # 컴팩트 전 — 집중
    "precompact":         "집중하겠습니다.",
    # 컴팩트 후 — 재정비
    "postcompact":        "다시 정리됐습니다.",
    # 설정 변경
    "configchange":       "설정이 바뀌었네요.",
    # 입력 요청 — 정중한 질문
    "elicitation":        "혹시 여쭤봐도 될까요?",
    # 입력 결과 수신
    "elicitationresult":  "감사합니다, 알겠습니다.",
    # 지시 로드 — 성실하게 확인
    "instructionsloaded": "확인했습니다, 열심히 하겠습니다.",
}


def load_voice_id() -> str:
    if not VOICE_IDS_FILE.exists():
        raise FileNotFoundError(f"{VOICE_IDS_FILE} 없음. 먼저 clone_faker_voice.py 실행하세요.")
    data = json.loads(VOICE_IDS_FILE.read_text())
    return data["faker"]


def create_pack_json():
    pack = {
        "name": "faker",
        "author": "claude-code-sounds",
        "description": "T1 Faker (이상혁) voice pack — IVC cloned from real voice samples via ElevenLabs",
        "license": "MIT",
        "preview_url": "",
    }
    path = PACK_DIR / "pack.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(pack, indent=2, ensure_ascii=False) + "\n")
    print("  pack.json 생성됨")


def generate_audio(client, voice_id: str, dry_run=False):
    sounds_dir = PACK_DIR / "sounds"

    for event, text in EVENTS.items():
        out_dir  = sounds_dir / event
        out_dir.mkdir(parents=True, exist_ok=True)
        out_file = out_dir / f"{event}.mp3"

        if out_file.exists():
            print(f"  ✓ {event}: 이미 존재")
            continue

        print(f"  → {event}: {text}")
        if dry_run:
            out_file.write_bytes(b"")
            print(f"    [DRY RUN] {out_file}")
            continue

        try:
            audio = b"".join(client.text_to_speech.convert(
                text=text,
                voice_id=voice_id,
                model_id="eleven_multilingual_v2",
                output_format="mp3_44100_128",
            ))
            out_file.write_bytes(audio)
            print(f"    저장됨: {len(audio):,} bytes")
            time.sleep(0.4)
        except Exception as e:
            print(f"    ✗ 실패: {e}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    # .env 로드
    env_path = Path(__file__).parent.parent / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())

    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key and not args.dry_run:
        print("❌ ELEVENLABS_API_KEY 없음")
        return

    if args.dry_run:
        client = None
    else:
        from elevenlabs.client import ElevenLabs
        client = ElevenLabs(api_key=api_key)

    voice_id = load_voice_id()
    print(f"\n🎮 페이커 사운드팩 생성 시작 (voice_id: {voice_id})\n")

    create_pack_json()

    print("\n[오디오 생성]")
    generate_audio(client, voice_id, dry_run=args.dry_run)

    print(f"\n✅ 완료!")
    print(f"   팩 위치: {PACK_DIR}")
    print(f"   적용: ./claude-sounds.sh use faker && ./install.sh --force")


if __name__ == "__main__":
    main()
