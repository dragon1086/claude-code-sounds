# Sound Packs

## 🎁 Want to contribute a pack?

**We'd love your pack.** Any theme, any language, any fandom.  
It takes about 15 minutes — see [How to Contribute](#how-to-contribute-a-pack) below.

---

## Built-in Packs

These packs are included with claude-code-sounds and ready to use immediately.

| Pack | Description | Source |
|------|-------------|--------|
| `onepiece` | **[Flagship]** Real One Piece anime voices — Luffy, Zoro, Robin, Franky, Brook and more | Original anime audio |
| `faker` | T1 Faker (이상혁) voice pack — IVC cloned via ElevenLabs | ElevenLabs IVC |
| `kimetsu` | Demon Slayer (鬼滅の刃) — Tanjiro, Rengoku, Zenitsu, Inosuke and more | ElevenLabs TTS |
| `best-practice` | ElevenLabs "Samara X" voice — ported from [claude-code-best-practice](https://github.com/shanraisshan/claude-code-best-practice) | ElevenLabs TTS |
| `silent` | 100ms silence — disables all sounds without removing hooks | — |
| `default` | Minimal default sound set | — |

---

## Community Packs

Packs created by the community. Open a PR to add yours!

**Requirements:** original or properly licensed audio only. No NSFW content.

| Pack | Author | Description | Install |
|------|--------|-------------|---------|
| _(be the first!)_ | | | |

---

## How to Contribute a Pack

Contributing a pack is straightforward. Here's all you need:

### 1. Create your pack folder

```
packs/
└── my-pack/
    ├── pack.json
    └── sounds/
        ├── sessionstart/
        │   └── sessionstart.wav
        ├── stop/
        │   └── stop.wav
        └── ...
```

**Partial packs are fine.** You only need to include the events you want to override — missing ones fall back to the `default` pack automatically.

### 2. Write pack.json

```json
{
  "name": "my-pack",
  "author": "your-github-username",
  "description": "Short description",
  "license": "MIT",
  "preview_url": "https://youtube.com/..."
}
```

### 3. Normalize audio to -20 LUFS

```bash
ffmpeg -i input.wav -af "loudnorm=I=-20:TP=-1.5:LRA=11" output.wav
```

Both `.wav` and `.mp3` are supported (`.wav` is tried first).

### 4. Test your pack

```bash
./claude-sounds.sh use my-pack
./install.sh --force
# restart Claude Code and verify sounds play
```

### 5. Open a PR

Add a row to the [Community Packs](#community-packs) table above and open a pull request.  
That's it — we'll review and merge promptly. 🎉

---

> See [packs/README.md](packs/README.md) for the full technical reference.
