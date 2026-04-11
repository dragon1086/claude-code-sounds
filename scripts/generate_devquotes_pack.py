#!/usr/bin/env python3
"""
generate_devquotes_pack.py
실제 개발자 명언을 ElevenLabs TTS로 생성하는 사운드팩 스크립트
팩: devquotes-en (영어), devquotes-ko (한국어)

Usage:
    python3 scripts/generate_devquotes_pack.py --lang en
    python3 scripts/generate_devquotes_pack.py --lang ko
    python3 scripts/generate_devquotes_pack.py --lang all
    python3 scripts/generate_devquotes_pack.py --lang en --dry-run
"""

import os
import json
import time
import argparse
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent

# ──────────────────────────────────────────────
# ElevenLabs Voice IDs
# ──────────────────────────────────────────────
VOICE_EN = "onwK4e9ZLuTAKqWW03F9"   # Daniel — Steady Broadcaster
VOICE_KO = "Xb7hH8MSUJpSbSDYk0k2"  # Alice  — Clear, Engaging Educator

# ──────────────────────────────────────────────
# 영어 이벤트 → (명언, 출처)
# ──────────────────────────────────────────────
EVENTS_EN = {
    # 세션 시작 — 리누스 토르발즈의 시그니처 명언
    "sessionstart":       ("Talk is cheap. Show me the code.", "Linus Torvalds"),
    # 초기 설정 — 준비의 중요성
    "setup":              ("Measure twice, cut once.", "Proverb"),
    # 도구 사용 전 — 켄트 벡의 TDD 원칙
    "pretooluse":         ("Make it work, make it right, make it fast.", "Kent Beck"),
    # 도구 사용 후 성공 — 문제 우선 사고
    "posttooluse":        ("First, solve the problem. Then, write the code.", "John Johnson"),
    # 도구 사용 후 실패 — 개발자 유머
    "posttoolusefailure": ("It's not a bug. It's an undocumented feature.", "Anonymous"),
    # 사용자 프롬프트 수락 — 마틴 파울러
    "userpromptsubmit":   ("Any fool can write code that a computer can understand.", "Martin Fowler"),
    # 작업 완료 — 저커버그
    "stop":               ("Done is better than perfect.", "Mark Zuckerberg"),
    # 작업 실패 종료 — 성장 마인드셋
    "stopfailure":        ("Every expert was once a beginner.", "Helen Hayes"),
    # 알림 — 도널드 크누스
    "notification":       ("Premature optimization is the root of all evil.", "Donald Knuth"),
    # 권한 요청 — 스탠 리
    "permissionrequest":  ("With great power comes great responsibility.", "Stan Lee"),
    # 권한 거부 — KISS 원칙
    "permissiondenied":   ("Keep it simple, stupid.", "Kelly Johnson"),
    # 세션 종료 — 앨런 케이
    "sessionend":         ("The best way to predict the future is to invent it.", "Alan Kay"),
    # 서브에이전트 시작 — 협업
    "subagentstart":      ("Two heads are better than one.", "Proverb"),
    # 서브에이전트 종료 — 팀워크
    "subagentstop":       ("Many hands make light work.", "Proverb"),
    # 작업 생성 — 생텍쥐페리
    "taskcreated":        ("A goal without a plan is just a wish.", "Antoine de Saint-Exupéry"),
    # 작업 완료 — 실리콘밸리 문화
    "taskcompleted":      ("Ship it!", "Silicon Valley"),
    # 팀원 대기 — 인내
    "teammateidle":       ("Patience is a virtue.", "Proverb"),
    # 디렉토리 변경 — 헤라클레이토스
    "cwdchanged":         ("Change is the only constant.", "Heraclitus"),
    # 파일 변경 — 로버트 마틴
    "filechanged":        ("The only way to go fast is to go well.", "Robert C. Martin"),
    # 워크트리 생성 — 시작의 중요성
    "worktreecreate":     ("To begin, begin.", "William Wordsworth"),
    # 워크트리 제거 — 레오나르도 다빈치
    "worktreeremove":     ("Simplicity is the ultimate sophistication.", "Leonardo da Vinci"),
    # 컴팩트 전 — 집중
    "precompact":         ("Less is more.", "Ludwig Mies van der Rohe"),
    # 컴팩트 후 — 로버트 마틴
    "postcompact":        ("Clean code reads like well-written prose.", "Robert C. Martin"),
    # 설정 변경 — 적응
    "configchange":       ("Adapt or perish.", "H.G. Wells"),
    # 입력 요청 — 소통
    "elicitation":        ("Ask, and it shall be given to you.", "Matthew 7:7"),
    # 입력 결과 수신 — 프랜시스 베이컨
    "elicitationresult":  ("Knowledge is power.", "Francis Bacon"),
    # 지시 로드
    "instructionsloaded": ("Instructions received. Let's build something great.", ""),
}

# ──────────────────────────────────────────────
# 한국어 이벤트 → (명언, 출처) — 자연스러운 한국어 번역
# ──────────────────────────────────────────────
EVENTS_KO = {
    "sessionstart":       ("코드로 증명해라. 말은 필요 없어.", "리누스 토르발즈"),
    "setup":              ("두 번 재고, 한 번에 잘라라.", "속담"),
    "pretooluse":         ("작동하게, 올바르게, 그리고 빠르게.", "켄트 벡"),
    "posttooluse":        ("먼저 문제를 풀어라. 그다음에 코드를 써라.", "존 존슨"),
    "posttoolusefailure": ("버그가 아니야. 문서화 안 된 기능이지.", "익명"),
    "userpromptsubmit":   ("어떤 바보도 컴퓨터가 이해하는 코드를 쓸 수 있다.", "마틴 파울러"),
    "stop":               ("완벽함보다 완성이 낫다.", "마크 저커버그"),
    "stopfailure":        ("모든 전문가는 한때 초보자였다.", "헬렌 헤이스"),
    "notification":       ("조기 최적화는 모든 악의 근원이다.", "도널드 크누스"),
    "permissionrequest":  ("큰 힘에는 큰 책임이 따른다.", "스탠 리"),
    "permissiondenied":   ("단순하게, 바보야.", "켈리 존슨"),
    "sessionend":         ("미래를 예측하는 최선의 방법은 미래를 발명하는 것이다.", "앨런 케이"),
    "subagentstart":      ("백지장도 맞들면 낫다.", "속담"),
    "subagentstop":       ("여럿이 하면 짐도 가벼워진다.", "속담"),
    "taskcreated":        ("계획 없는 목표는 그냥 소원이다.", "생텍쥐페리"),
    "taskcompleted":      ("배포해!", "실리콘밸리"),
    "teammateidle":       ("인내는 미덕이다.", "속담"),
    "cwdchanged":         ("변화만이 유일한 상수다.", "헤라클레이토스"),
    "filechanged":        ("빠르게 가려면 올바르게 가야 한다.", "로버트 마틴"),
    "worktreecreate":     ("시작하려면, 시작해라.", "윌리엄 워즈워스"),
    "worktreeremove":     ("단순함이 궁극의 세련됨이다.", "레오나르도 다빈치"),
    "precompact":         ("적을수록 풍요롭다.", "미스 반 데어 로에"),
    "postcompact":        ("좋은 코드는 잘 쓰인 산문처럼 읽힌다.", "로버트 마틴"),
    "configchange":       ("적응하거나 소멸하라.", "H.G. 웰스"),
    "elicitation":        ("구하라, 그러면 얻을 것이다.", "마태복음"),
    "elicitationresult":  ("아는 것이 힘이다.", "프랜시스 베이컨"),
    "instructionsloaded": ("지시 수신 완료. 멋진 것을 만들어보자.", ""),
}

LANG_CONFIG = {
    "en": {
        "pack_name":   "devquotes-en",
        "voice_id":    VOICE_EN,
        "events":      EVENTS_EN,
        "description": "Developer motivational quotes (English) — real wisdom from Torvalds, Knuth, Beck, and more",
        "model":       "eleven_multilingual_v2",
    },
    "ko": {
        "pack_name":   "devquotes-ko",
        "voice_id":    VOICE_KO,
        "events":      EVENTS_KO,
        "description": "개발자 동기부여 명언 (한국어) — 토르발즈, 크누스, 벡 등 실제 명언 모음",
        "model":       "eleven_multilingual_v2",
    },
}


def load_env():
    env_path = ROOT_DIR / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())


def create_pack_json(pack_dir: Path, cfg: dict):
    pack = {
        "name":        cfg["pack_name"],
        "author":      "claude-code-sounds",
        "description": cfg["description"],
        "license":     "MIT",
        "preview_url": "",
    }
    path = pack_dir / "pack.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(pack, indent=2, ensure_ascii=False) + "\n")
    print(f"  pack.json 생성됨")


def generate_audio(client, pack_dir: Path, cfg: dict, dry_run=False):
    sounds_dir = pack_dir / "sounds"
    events = cfg["events"]
    voice_id = cfg["voice_id"]
    model_id = cfg["model"]
    skipped = 0

    for event, (text, source) in events.items():
        out_dir  = sounds_dir / event
        out_dir.mkdir(parents=True, exist_ok=True)
        out_file = out_dir / f"{event}.mp3"

        if out_file.exists():
            skipped += 1
            continue

        attribution = f" [{source}]" if source else ""
        print(f"  → {event}: {text}{attribution}")

        if dry_run:
            out_file.write_bytes(b"")
            print(f"    [DRY RUN] {out_file.name}")
            continue

        try:
            audio = b"".join(client.text_to_speech.convert(
                text=text,
                voice_id=voice_id,
                model_id=model_id,
                output_format="mp3_44100_128",
            ))
            out_file.write_bytes(audio)
            print(f"    저장됨: {len(audio):,} bytes")
            time.sleep(0.5)   # API rate limit 여유
        except Exception as e:
            print(f"    ✗ 실패: {e}")

    if skipped:
        print(f"  ✓ {skipped}개 이미 존재, 건너뜀")


def print_quote_table(cfg: dict):
    print(f"\n  {'이벤트':<25} {'명언':<55} 출처")
    print(f"  {'-'*25} {'-'*55} {'-'*20}")
    for event, (text, source) in cfg["events"].items():
        short_text = text[:52] + "..." if len(text) > 55 else text
        print(f"  {event:<25} {short_text:<55} {source}")


def run_pack(lang: str, client, dry_run=False):
    cfg = LANG_CONFIG[lang]
    pack_dir = ROOT_DIR / "packs" / cfg["pack_name"]

    print(f"\n{'='*60}")
    print(f"  [{lang.upper()}] {cfg['pack_name']}")
    print(f"  Voice: {cfg['voice_id']}")
    print(f"{'='*60}")

    if dry_run:
        print_quote_table(cfg)

    pack_dir.mkdir(parents=True, exist_ok=True)
    create_pack_json(pack_dir, cfg)

    print(f"\n[오디오 생성 — {len(cfg['events'])}개 이벤트]")
    generate_audio(client, pack_dir, cfg, dry_run=dry_run)

    print(f"\n✅ {cfg['pack_name']} 완료")
    print(f"   위치: {pack_dir}")
    print(f"   적용: ./claude-sounds.sh use {cfg['pack_name']} && ./install.sh --force")


def main():
    parser = argparse.ArgumentParser(description="개발자 명언 사운드팩 생성기")
    parser.add_argument("--lang",    choices=["en", "ko", "all"], default="all",
                        help="생성할 언어 (기본: all)")
    parser.add_argument("--dry-run", action="store_true",
                        help="API 호출 없이 파일 구조만 생성")
    args = parser.parse_args()

    load_env()

    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key and not args.dry_run:
        print("❌ ELEVENLABS_API_KEY 없음 (.env 파일 확인)")
        return

    if args.dry_run:
        client = None
        print("🔍 DRY RUN 모드 — API 호출 없음")
    else:
        from elevenlabs.client import ElevenLabs
        client = ElevenLabs(api_key=api_key)

    langs = ["en", "ko"] if args.lang == "all" else [args.lang]

    for lang in langs:
        run_pack(lang, client, dry_run=args.dry_run)

    print(f"\n🎉 전체 완료! {len(langs)}개 팩 생성됨")


if __name__ == "__main__":
    main()
