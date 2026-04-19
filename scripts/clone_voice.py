#!/usr/bin/env python3
"""
YouTube 영상에서 오디오를 추출하고 ElevenLabs로 보이스 클론을 생성합니다.
Usage: python3 scripts/clone_voice.py <youtube_url> <voice_name>
"""

import os
import sys
import tempfile
from pathlib import Path

# .env 로드
env_path = Path(__file__).parent.parent / ".env"
if env_path.exists():
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())

import yt_dlp
from elevenlabs.client import ElevenLabs

def download_audio(url: str, output_path: str) -> str:
    """YouTube URL에서 오디오를 추출합니다."""
    print(f"[1/3] 유튜브 오디오 다운로드 중: {url}")
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_path,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
        "quiet": False,
        "no_warnings": False,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        title = info.get("title", "unknown")
        print(f"    제목: {title}")
    return output_path + ".mp3"


def clone_voice(audio_path: str, voice_name: str, description: str = "") -> str:
    """ElevenLabs Instant Voice Clone으로 보이스를 생성합니다."""
    print(f"[2/3] ElevenLabs에 보이스 클론 생성 중: {voice_name}")
    client = ElevenLabs(api_key=os.environ["ELEVENLABS_API_KEY"])

    with open(audio_path, "rb") as f:
        voice = client.voices.ivc.create(
            name=voice_name,
            description=description or f"{voice_name} - cloned from YouTube",
            files=[f],
        )

    print(f"    보이스 ID: {voice.voice_id}")
    return voice.voice_id


def main():
    if len(sys.argv) < 3:
        print("Usage: python3 scripts/clone_voice.py <youtube_url> <voice_name>")
        print("Example: python3 scripts/clone_voice.py 'https://www.youtube.com/shorts/JZp4s6cRkFU' '하츄핑'")
        sys.exit(1)

    url = sys.argv[1]
    voice_name = sys.argv[2]
    description = sys.argv[3] if len(sys.argv) > 3 else ""

    with tempfile.TemporaryDirectory() as tmpdir:
        audio_base = os.path.join(tmpdir, "voice_sample")
        audio_path = download_audio(url, audio_base)

        print(f"    오디오 파일: {audio_path} ({os.path.getsize(audio_path) / 1024:.1f} KB)")

        voice_id = clone_voice(audio_path, voice_name, description)

    print(f"\n[3/3] 완료!")
    print(f"  보이스 이름: {voice_name}")
    print(f"  보이스 ID:   {voice_id}")
    print(f"\n  이 ID를 scripts/generate_*.py 에서 VOICE_ID로 사용하세요.")


if __name__ == "__main__":
    main()
