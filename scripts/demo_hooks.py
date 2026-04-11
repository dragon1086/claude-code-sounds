#!/usr/bin/env python3
"""Demo: play each hook sound with description. For video recording."""

import subprocess
import time
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from rich import box
import pyfiglet

console = Console()

SOUNDS_DIR = Path("/Users/aerok/Desktop/rocky/claude-code-sounds/packs/onepiece/sounds")
IMAGES_DIR = Path("/Users/aerok/Desktop/rocky/claude-code-sounds/packs/onepiece/images/norm")

RAINBOW = ["bold red", "bold orange1", "bold yellow", "bold green", "bold cyan", "bold blue1", "bold magenta"]

# (event, label, character, ko_desc, en_desc, color)
HOOKS = [
    ("sessionstart",       "Session Start",            "Luffy",          "나는 몽키D.루피, 해적왕이 될 사나이다!",              "I'm Monkey D. Luffy — I will be King of the Pirates!",     "bold red"),
    ("setup",              "Project Setup",             "Shanks",         "패기(覇気) 방출 — 압도적인 존재감",                  "Haki release — overwhelming presence",                     "bold yellow"),
    ("userpromptsubmit",   "User Prompt Submit",        "Luffy",          "고무고무의~! — 기술 준비",                           "Gum-Gum~! — attack ready",                                 "bold red"),
    ("pretooluse",         "Pre Tool Use",              "Zoro",           "사자의 노래 기술 시전 — 칼을 뽑는 순간",              "Rashomon — blade drawn",                                   "bold green"),
    ("posttooluse",        "Post Tool Use",             "Franky",         "수퍼(SUPER)!",                                       "SUPER!",                                                   "bold blue"),
    ("posttoolusefailure", "Post Tool Use Failure",     "Robin",          "살고싶어!! — 엔이스 섬 절규",                        "I want to live!! — Enies Lobby cry",                       "bold magenta"),
    ("stop",               "Stop",                      "Robin",          "로빈 웃음소리",                                      "Robin's laugh",                                            "bold magenta"),
    ("stopfailure",        "Stop Failure",              "Luffy",          "에이스를 부르는 절규 — 극한의 절망",                  "Crying out for Ace — peak despair",                        "bold red"),
    ("notification",       "Notification",              "Franky",         "와우(AWWW)! — 감탄",                                 "AWWW! — Franky's amazement",                               "bold blue"),
    ("permissionrequest",  "Permission Request",        "Nami",           "울면서 '루피 도와줘!'",                              "Crying 'Luffy, help me!'",                                 "bold yellow"),
    ("permissiondenied",   "Permission Denied",         "Nami / Sanji",   "상디 나미상~~ 달려들다 → 나미 펀치",                  "Sanji swoops in for Nami → gets punched",                  "bold yellow"),
    ("subagentstart",      "Subagent Start",            "Zoro",           "'롤로노아 조로' — 자기소개",                         "'Roronoa Zoro' — self-introduction",                       "bold green"),
    ("subagentstop",       "Subagent Stop",             "Zoro",           "삼도류 오의·삼천세계(三千世界) — 임무 완료",          "Santoryu Ogi: Sanzen Sekai — mission complete",            "bold green"),
    ("taskcreated",        "Task Created",              "Usopp",          "우솝 망치 소리 — 새 작업 착수",                      "Usopp Hammer — starting a new task",                       "bold yellow"),
    ("taskcompleted",      "Task Completed",            "Zoro",           "삼도류 오의·삼천세계 — 완료",                        "Santoryu Ogi: Sanzen Sekai — complete",                    "bold green"),
    ("teammateidle",       "Teammate Idle",             "Zoro",           "'아무일도 없었다' — 피투성이로 희생하고 안 아픈 척",   "'Nothing happened.' — stoic after sacrifice",              "bold green"),
    ("cwdchanged",         "CWD Changed",               "—",              "원피스 애니 장면전환 인트로",                         "One Piece mid-episode scene transition",                   "bold cyan"),
    ("filechanged",        "File Changed",              "Luffy",          "느려 — 견문색 패기로 이미 감지",                     "'Too slow.' — Kenbunshoku Haki sensed it first",           "bold red"),
    ("worktreecreate",     "Worktree Create",           "Luffy",          "루피 웃음소리 — 새 모험 시작!",                      "Luffy's laugh — new adventure begins!",                    "bold red"),
    ("worktreeremove",     "Worktree Remove",           "Brook",          "요호호호(Yohohoho) — 작별",                          "Yohohoho — farewell",                                      "bold white"),
    ("precompact",         "Pre Compact",               "Dr. Hiluluk",    "'사람이 언제 죽는다고 생각하나?'",                   "'When do you think a man dies?'",                          "bold magenta"),
    ("postcompact",        "Post Compact",              "Robin",          "로빈 웃음소리 — 상쾌한 재출발",                      "Robin's laugh — fresh restart",                            "bold magenta"),
    ("configchange",       "Config Change",             "Usopp",          "'나는 원래부터 비관주의자다!!' — 상황이 반전됐다",    "'I was always a pessimist!!' — things have changed",       "bold yellow"),
    ("elicitation",        "Elicitation",               "Chopper",        "귀여운 초퍼 부끄러움 — 조심스럽게 물어보는 중",       "Embarrassed Chopper — asking shyly",                       "bold cyan"),
    ("elicitationresult",  "Elicitation Result",        "Sanji",          "'멜로린(Mellorine)~!' — 완전 홀려버림",              "'Mellorine~!' — completely smitten",                       "bold yellow"),
    ("instructionsloaded", "Instructions Loaded",       "Whitebeard",     "'원피스는 실재한다!!'",                              "'ONE PIECE IS REAL!!'",                                    "bold white"),
    ("sessionend",         "Session End",               "Sanji",          "'더럽게 신세 많이 졌습니다' — 제프 선생 작별",        "'I'm deeply grateful.' — farewell to master Jeff",         "bold yellow"),
]

PAUSE_AFTER = 1.2

# ── Image window subprocess ──────────────────────────────────────────────────

_IMG_SCRIPT = """
import os, sys, time
os.environ["SDL_VIDEO_WINDOW_POS"] = sys.argv[2]
import pygame
pygame.init()
img = pygame.image.load(sys.argv[1])
w, h = img.get_size()
screen = pygame.display.set_mode((w, h), pygame.NOFRAME)
screen.blit(img, (0, 0))
pygame.display.flip()
clock = pygame.time.Clock()
while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            sys.exit()
    clock.tick(30)
"""

# Image window position: right side of screen (adjust X if needed)
_IMG_POS = "700,300"

_img_proc = None

def show_image(event: str):
    global _img_proc
    if _img_proc and _img_proc.poll() is None:
        _img_proc.terminate()
        _img_proc.wait()
    img_path = IMAGES_DIR / f"{event}.png"
    if not img_path.exists():
        _img_proc = None
        return
    _img_proc = subprocess.Popen(
        ["/Users/aerok/.pyenv/versions/3.12.10/bin/python", "-c", _IMG_SCRIPT,
         str(img_path), _IMG_POS],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    time.sleep(0.2)  # give window time to appear

def close_image():
    global _img_proc
    if _img_proc and _img_proc.poll() is None:
        _img_proc.terminate()
        _img_proc.wait()
    _img_proc = None

# ── Helpers ──────────────────────────────────────────────────────────────────

def pick_font(label: str) -> str:
    n = len(label)
    if n <= 11:
        return "big"
    if n <= 17:
        return "standard"
    return "small"


def rainbow_figlet(label: str) -> Text:
    font = pick_font(label)
    art = pyfiglet.figlet_format(label, font=font, width=90)
    lines = art.split("\n")
    result = Text()
    for i, line in enumerate(lines):
        result.append(line + "\n", style=RAINBOW[i % len(RAINBOW)])
    return result


def play(path: Path):
    subprocess.run(["afplay", str(path)], check=False)


def show_card(i, total, label, char, ko_desc, en_desc, color):
    console.clear()

    # ── Header ──────────────────────────────────────────────────────────────
    header = Text(justify="center")
    header.append("  ★ ONE PIECE SOUND PACK ★  ", style="bold white on dark_red")
    header.append(f"  {i} / {total}  ", style="bold yellow on grey23")
    console.print(Align.center(header))
    console.print()

    # ── Rainbow ASCII tool name ──────────────────────────────────────────────
    console.print(Align.center(rainbow_figlet(label)))

    # ── Character + scene panel ─────────────────────────────────────────────
    info = Text(justify="center")
    info.append(f"  {char}  ", style=f"{color} reverse")
    info.append(f"\n\n{ko_desc}", style="italic bright_white")
    info.append(f"\n{en_desc}", style="italic grey70")

    panel = Panel(
        Align.center(info, vertical="middle"),
        box=box.HEAVY,
        border_style=color,
        padding=(1, 6),
    )
    console.print(panel)
    console.print()


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    total = len(HOOKS)
    console.clear()
    console.print(Align.center(rainbow_figlet("One Piece")))
    console.print(Align.center(Text("Sound Pack  ·  All Hooks Demo\n", style="bold white")))
    console.print(Align.center(Text("▶  Starting in 3 seconds...\n", style="bold yellow")))
    time.sleep(3)

    for i, (event, label, char, ko_desc, en_desc, color) in enumerate(HOOKS, 1):
        wav = SOUNDS_DIR / event / f"{event}.wav"
        mp3 = SOUNDS_DIR / event / f"{event}.mp3"
        audio = wav if wav.exists() else mp3

        show_image(event)
        show_card(i, total, label, char, ko_desc, en_desc, color)
        play(audio)
        time.sleep(PAUSE_AFTER)

    close_image()
    console.clear()
    console.print(Align.center(rainbow_figlet("All Done!")))
    console.print(Align.center(Text("All hook sounds demonstrated  ·  One Piece Sound Pack\n", style="bold white")))


if __name__ == "__main__":
    main()
