#!/usr/bin/env python3
"""Demo: play each hook sound with description. For video recording."""

import subprocess
import time
from pathlib import Path

SOUNDS_DIR = Path("/Users/aerok/Desktop/rocky/claude-code-sounds/packs/onepiece/sounds")

HOOKS = [
    ("sessionstart",       "세션 시작",              "루피",        "나는 몽키D.루피, 해적왕이 될 사나이다!"),
    ("setup",              "프로젝트 초기화",          "샹크스",      "패기(覇気) 방출 — 압도적인 존재감"),
    ("userpromptsubmit",   "메시지 전송",             "루피",        "고무고무의~! — 기술 준비"),
    ("pretooluse",         "도구 실행 직전",           "조로",        "나생문(羅生門) 기술 시전 — 칼을 뽑는 순간"),
    ("posttooluse",        "도구 실행 완료",           "프랑키",      "수퍼(SUPER)!"),
    ("posttoolusefailure", "도구 실행 실패",           "로빈",        "살고싶어!! — 엔이스 섬 절규"),
    ("stop",               "응답 완료",               "프랑키",      "수퍼(SUPER)!"),
    ("stopfailure",        "응답 실패",               "루피",        "에이스를 부르는 절규 — 극한의 절망"),
    ("notification",       "알림",                   "프랑키",      "와우(AWWW)! — 감탄"),
    ("permissionrequest",  "권한 요청",               "나미",        "울면서 '루피 도와줘!'"),
    ("permissiondenied",   "권한 거부",               "나미 / 상디", "상디 나미상~~ 달려들다 → 나미 펀치"),
    ("subagentstart",      "서브에이전트 시작",        "조로",        "'롤로노아 조로' — 자기소개"),
    ("subagentstop",       "서브에이전트 완료",        "조로",        "삼도류 오의·삼천세계(三千世界) — 임무 완료"),
    ("taskcreated",        "태스크 생성",             "우솝",        "우솝 망치 소리 — 새 작업 착수"),
    ("taskcompleted",      "태스크 완료",             "조로",        "삼도류 오의·삼천세계 — 완료"),
    ("teammateidle",       "팀메이트 대기 중",         "조로",        "'아무일도 없었다' — 피투성이로 희생하고 안 아픈 척"),
    ("cwdchanged",         "작업 디렉토리 변경",       "—",           "원피스 애니 장면전환 인트로"),
    ("filechanged",        "파일 변경 감지",           "우솝",        "우솝 망치 소리 — 파일 수정"),
    ("worktreecreate",     "워크트리 생성",            "루피",        "루피 웃음소리 — 새 모험 시작!"),
    ("worktreeremove",     "워크트리 삭제",            "브룩",        "요호호호(Yohohoho) — 작별"),
    ("precompact",         "컨텍스트 압축 직전",       "닥터 히루루크", "'사람이 언제 죽는다고 생각하나?'"),
    ("postcompact",        "컨텍스트 압축 완료",       "로빈",        "로빈 웃음소리 — 상쾌한 재출발"),
    ("configchange",       "설정 변경",               "우솝",        "'나는 원래부터 비관주의자다!!' — 상황이 반전됐다"),
    ("elicitation",        "사용자 입력 요청",         "초퍼",        "귀여운 초퍼 부끄러움 — 조심스럽게 물어보는 중"),
    ("elicitationresult",  "입력 결과 수신",           "상디",        "'멜로린(Mellorine)~!' — 완전 홀려버림"),
    ("instructionsloaded", "커스텀 지시 로드",         "흰수염",      "'원피스는 실재한다!!'"),
    ("sessionend",         "세션 종료",               "상디",        "'더럽게 신세 많이 졌습니다, 은혜를 잊지 않겠습니다' — 제프 선생 작별"),
]

PAUSE_AFTER = 1.2  # seconds after sound finishes before next

def play(path: Path):
    subprocess.run(["afplay", str(path)], check=False)

def clear():
    print("\033[2J\033[H", end="", flush=True)

def show_card(i, total, event, func, char, desc):
    clear()
    print("=" * 56)
    print(f"  🎵  One Piece Sound Pack  —  {i}/{total}")
    print("=" * 56)
    print(f"  훅 이름   :  {event}")
    print(f"  기능      :  {func}")
    print(f"  캐릭터    :  {char}")
    print(f"  장면/대사 :  {desc}")
    print("=" * 56)
    print()

def main():
    total = len(HOOKS)
    print("▶  3초 후 시작합니다...")
    time.sleep(3)

    for i, (event, func, char, desc) in enumerate(HOOKS, 1):
        wav = SOUNDS_DIR / event / f"{event}.wav"
        mp3 = SOUNDS_DIR / event / f"{event}.mp3"
        audio = wav if wav.exists() else mp3

        show_card(i, total, event, func, char, desc)
        play(audio)
        time.sleep(PAUSE_AFTER)

    clear()
    print("=" * 56)
    print("  모든 훅 사운드 시연 완료!")
    print("=" * 56)

if __name__ == "__main__":
    main()
