#!/usr/bin/env python3
"""Normalize audio volume across all sound files using ffmpeg loudnorm filter.

Target: -20 LUFS, True Peak -1.5 dBTP
Usage:
  python3 normalize_audio.py                  # normalize all packs in this repo
  python3 normalize_audio.py path/to/sounds/  # normalize a specific directory
"""

import subprocess
import shutil
from pathlib import Path

TARGET_LUFS = -20
TRUE_PEAK = -1.5
LRA = 11

REPO_ROOT = Path(__file__).parent.parent


def get_loudness_stats(path: Path) -> dict:
    """Run first-pass loudnorm to measure current loudness."""
    result = subprocess.run(
        [
            "ffmpeg", "-i", str(path),
            "-af", f"loudnorm=I={TARGET_LUFS}:TP={TRUE_PEAK}:LRA={LRA}:print_format=json",
            "-f", "null", "-"
        ],
        capture_output=True, text=True
    )
    # Parse JSON from stderr
    stderr = result.stderr
    start = stderr.rfind("{")
    end = stderr.rfind("}") + 1
    if start == -1:
        return {}
    import json
    return json.loads(stderr[start:end])


def normalize_file(path: Path) -> bool:
    """Normalize a single audio file in-place. Returns True on success."""
    tmp = path.with_suffix(".tmp" + path.suffix)

    # Two-pass loudnorm for accuracy
    stats = get_loudness_stats(path)
    if not stats:
        print(f"  [SKIP] Could not measure {path.name}")
        return False

    measured_i = stats.get("input_i", "-70")
    measured_lra = stats.get("input_lra", "0")
    measured_tp = stats.get("input_tp", "-inf")
    measured_thresh = stats.get("input_thresh", "-70")
    offset = stats.get("target_offset", "0")

    af = (
        f"loudnorm=I={TARGET_LUFS}:TP={TRUE_PEAK}:LRA={LRA}"
        f":measured_I={measured_i}"
        f":measured_LRA={measured_lra}"
        f":measured_TP={measured_tp}"
        f":measured_thresh={measured_thresh}"
        f":offset={offset}"
        f":linear=true:print_format=summary"
    )

    ext = path.suffix.lower()
    if ext == ".mp3":
        codec_args = ["-c:a", "libmp3lame", "-q:a", "2"]
    else:  # .wav
        codec_args = ["-c:a", "pcm_s16le"]

    result = subprocess.run(
        ["ffmpeg", "-y", "-i", str(path), "-af", af] + codec_args + [str(tmp)],
        capture_output=True, text=True
    )

    if result.returncode != 0:
        print(f"  [ERROR] {path.name}: {result.stderr[-300:]}")
        if tmp.exists():
            tmp.unlink()
        return False

    shutil.move(str(tmp), str(path))
    return True


def process_directory(base_dir: Path, label: str):
    files = sorted(base_dir.rglob("*.mp3")) + sorted(base_dir.rglob("*.wav"))
    print(f"\n=== {label} ({len(files)} files) ===")
    ok = fail = 0
    for f in files:
        print(f"  Normalizing {f.relative_to(base_dir)} ...", end=" ", flush=True)
        if normalize_file(f):
            print("OK")
            ok += 1
        else:
            fail += 1
    print(f"  Done: {ok} OK, {fail} failed")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        # Normalize a specific directory passed as argument
        for arg in sys.argv[1:]:
            d = Path(arg).expanduser().resolve()
            process_directory(d, str(d))
    else:
        # Default: normalize all packs in this repo
        packs_dir = REPO_ROOT / "packs"
        for pack_sounds in sorted(packs_dir.glob("*/sounds")):
            label = str(pack_sounds.relative_to(REPO_ROOT))
            process_directory(pack_sounds, label)
    print("\nAll done.")
