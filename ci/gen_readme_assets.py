#!/usr/bin/env python3
"""
Generate README visual assets (logo, diagrams) using Gemini image generation.
Model: gemini-2.0-flash-preview-image-generation
"""

import os
import base64
import json
import urllib.request
import urllib.error
from pathlib import Path

API_KEY = os.environ.get("GEMINI_API_KEY", "")
if not API_KEY:
    raise SystemExit("GEMINI_API_KEY not set")

ASSETS_DIR = Path(__file__).parent.parent / "docs" / "assets"
ASSETS_DIR.mkdir(parents=True, exist_ok=True)

BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models"


def generate_image(prompt: str, model: str = "gemini-3.1-flash-image-preview") -> bytes:
    url = f"{BASE_URL}/{model}:generateContent?key={API_KEY}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "responseModalities": ["TEXT", "IMAGE"],
            "thinkingConfig": {"thinkingBudget": 1024},
        },
    }
    data = json.dumps(payload).encode()
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        result = json.loads(resp.read())

    for candidate in result.get("candidates", []):
        for part in candidate.get("content", {}).get("parts", []):
            if "inlineData" in part:
                b64 = part["inlineData"]["data"]
                return base64.b64decode(b64)

    raise ValueError(f"No image in response: {json.dumps(result, indent=2)[:500]}")


def save(name: str, data: bytes) -> Path:
    path = ASSETS_DIR / name
    path.write_bytes(data)
    print(f"  saved → {path.relative_to(Path(__file__).parent.parent)}")
    return path


# ── 1. Main logo ───────────────────────────────────────────────────────────────
print("Generating logo...")
logo_prompt = """
Create a clean, modern open-source project logo for "claude-code-sounds".

Design specs:
- Dark background (#0d1117, GitHub dark style)
- Central icon: a stylized audio waveform or sound wave in a rounded square badge
- Waveform color: gradient from #7c3aed (violet) to #06b6d4 (cyan), glowing neon effect
- Small Claude Code terminal cursor or prompt symbol (▸ or >) subtly integrated
- Project name "claude-code-sounds" in clean monospace font below the icon
- Tagline: "Your Claude sessions, now with a soundtrack" in smaller muted gray text
- Resolution: 1200×630 (OpenGraph banner format)
- Style: minimal, developer-aesthetic, no gradients in background, dark mode
- NO busy backgrounds, NO photorealistic elements
"""
save("banner.png", generate_image(logo_prompt))

# ── 2. Hook event flow diagram ─────────────────────────────────────────────────
print("Generating hook flow diagram...")
flow_prompt = """
Create a clean developer-style diagram showing how claude-code-sounds works.

Layout: horizontal flow, dark background (#0d1117)
Flow steps (left to right, connected by arrows):
  1. Box: "Claude Code" (purple, with Claude logo-style triangle)
     ↓ fires hook event
  2. Box: "hooks.py" (dark card, monospace code font)
     → detects event type
  3. Box: "Sound Router" (cyan accent)
     → matches HOOK_SOUND_MAP
  4. Box: "sounds/{event}/" (folder icon, green)
     → plays .wav file
  5. Icon: speaker / audio waves (teal glow)

Style:
- Clean card-based diagram, rounded corners
- Dark mode (#0d1117 background, #161b22 cards)
- Accent colors: violet for Claude, cyan for logic, green for files
- Small code labels on arrows (e.g., "SessionStart", "PreToolUse", "git commit →")
- Monospace font throughout
- Resolution: 1200x500
- Minimal, clean, no 3D effects
"""
save("flow.png", generate_image(flow_prompt))

print("\nDone. Assets saved to docs/assets/")
