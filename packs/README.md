# Sound Pack Contribution Guide

**Contributions are very welcome.** Any theme, any language, any fandom — if it sounds good, we want it.

Jump to: [Quick Start](#quick-start) · [Pack Format](#pack-format) · [Audio Guidelines](#audio-guidelines) · [Submitting](#submitting)

---

## Quick Start

Five steps from idea to merged PR:

1. Create `packs/<your-pack>/` with a `sounds/` subfolder
2. Drop in your audio files (`.wav` or `.mp3`)
3. Add a `pack.json`
4. Normalize audio to -20 LUFS
5. Open a PR — add your entry to [PACKS.md](../PACKS.md)

**Partial packs are supported.** You only need to include the events you want to override. Missing slots fall back to the `default` pack automatically.

---

## Pack Format

```
my-pack/
├── pack.json          # required metadata
└── sounds/            # same structure as hooks/sounds/
    ├── sessionstart/
    │   └── sessionstart.wav
    ├── stop/
    │   └── stop.wav
    └── ...            # only include what you want to override
```

### pack.json

```json
{
  "name": "my-pack",
  "author": "your-github-username",
  "description": "Short description of your pack",
  "license": "MIT",
  "preview_url": "https://youtube.com/..."
}
```

| Field | Required | Notes |
|-------|----------|-------|
| `name` | ✅ | Matches the folder name |
| `author` | ✅ | Your GitHub username |
| `description` | ✅ | One sentence |
| `license` | ✅ | e.g. `MIT`, `CC BY 4.0` |
| `preview_url` | — | YouTube demo link recommended |

---

## Hook Events

All 27 Claude Code hook events you can assign sounds to:

| Event | When it fires |
|-------|--------------|
| `sessionstart` | New Claude Code session begins |
| `sessionend` | Session ends |
| `setup` | Project initialized |
| `userpromptsubmit` | User sends a message |
| `pretooluse` | Just before a tool runs |
| `posttooluse` | Tool completed successfully |
| `posttoolusefailure` | Tool failed |
| `stop` | Claude finishes responding |
| `stopfailure` | Response ended with error |
| `notification` | Notification event |
| `permissionrequest` | Claude asks for permission |
| `permissiondenied` | Permission was denied |
| `subagentstart` | Subagent session begins |
| `subagentstop` | Subagent session ends |
| `taskcreated` | A task is created |
| `taskcompleted` | A task is completed |
| `teammateidle` | Agent is waiting |
| `cwdchanged` | Working directory changed |
| `filechanged` | File change detected |
| `worktreecreate` | Git worktree created |
| `worktreeremove` | Git worktree removed |
| `precompact` | Context compaction about to start |
| `postcompact` | Context compaction finished |
| `configchange` | Configuration changed |
| `elicitation` | Claude is asking for user input |
| `elicitationresult` | User input received |
| `instructionsloaded` | Custom instructions loaded |

---

## Audio Guidelines

### Normalize to -20 LUFS

All submissions must be normalized to **-20 LUFS** integrated loudness so volume is consistent across packs.

```bash
ffmpeg -i input.wav -af "loudnorm=I=-20:TP=-1.5:LRA=11" output.wav
```

Batch convert a whole pack:

```bash
for dir in packs/my-pack/sounds/*/; do
  event=$(basename "$dir")
  mp3="$dir${event}.mp3"
  wav="$dir${event}.wav"
  [ -f "$mp3" ] && ffmpeg -y -i "$mp3" -af "loudnorm=I=-20:TP=-1.5:LRA=11" "$wav"
done
```

### Format

- `.wav` or `.mp3` — both work (`.wav` is tried first)
- Recommended: 44100 Hz, stereo or mono
- Keep clips short: 1–5 seconds is ideal

### Licensing

Only submit audio you have the right to distribute. Accepted licenses: MIT, CC BY, CC BY-SA, CC0, or equivalent. Add the license to `pack.json`.

---

## Built-in Packs

| Pack | Description |
|------|-------------|
| `onepiece` | **[Flagship]** Real One Piece anime voices — Luffy, Zoro, Robin, Franky, Brook and more |
| `faker` | T1 Faker (이상혁) voice pack — ElevenLabs IVC |
| `kimetsu` | Demon Slayer (鬼滅の刃) — Tanjiro, Rengoku, Zenitsu, Inosuke and more |
| `best-practice` | ElevenLabs "Samara X" — ported from claude-code-best-practice |
| `silent` | 100ms silence — disables sounds without removing hooks |
| `default` | Minimal default sound set |

---

## Submitting

1. Fork this repo
2. Add your pack under `packs/<name>/`
3. Open a PR with a row added to the [Community Packs table in PACKS.md](../PACKS.md#community-packs)
4. Include a short demo (YouTube link in `pack.json` → `preview_url`)

We review and merge pack PRs promptly. The more packs, the better. 🎉
