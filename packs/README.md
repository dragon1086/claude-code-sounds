# Sound Packs

A sound pack is a folder containing audio files that override the default sounds.

## Pack Format

```
my-pack/
├── pack.json          # required metadata
└── sounds/            # same folder structure as hooks/sounds/
    ├── sessionstart/
    │   └── sessionstart.wav
    ├── stop/
    │   └── stop.wav
    └── ...
```

**Partial packs are supported.** You only need to include the sounds you want to override.
Missing slots fall back to the `default` pack automatically.

## pack.json Fields

```json
{
  "name": "my-pack",
  "author": "your-github-username",
  "description": "Short description of your pack",
  "license": "MIT",
  "preview_url": "https://..."
}
```

## Built-in Packs

| Pack | Description |
|------|-------------|
| `onepiece` | Real One Piece anime voices — iconic scenes from Luffy, Zoro, Robin and more. **Default pack.** |
| `best-practice` | ElevenLabs "Samara X" voice — ported from the claude-code-best-practice repo |
| `silent` | 100ms silence — disables sounds without removing hooks |

## Bring Your Own Voices

You can replace any sound file with your own clips:

```
.claude/hooks/sounds/stop/
└── stop.wav   ← replace with your own file
```

File name must match the folder name. Both `.wav` and `.mp3` are supported (`.wav` tried first).

## Audio Guidelines

To ensure consistent volume across packs, normalize all audio files to **-20 LUFS** integrated loudness before submitting.

Using ffmpeg (two-pass for accuracy):

```bash
# First pass — measure loudness
stats=$(ffmpeg -i input.wav -af "loudnorm=I=-20:TP=-1.5:LRA=11:print_format=json" -f null - 2>&1)

# Extract values and apply (second pass)
ffmpeg -i input.wav \
  -af "loudnorm=I=-20:TP=-1.5:LRA=11:measured_I=<input_i>:measured_TP=<input_tp>:measured_LRA=<input_lra>:measured_thresh=<input_thresh>:offset=<target_offset>:linear=true" \
  -ar 44100 output.wav
```

Or use a simple one-liner if your files are roughly similar in loudness:

```bash
ffmpeg -i input.wav -af loudnorm=I=-20:TP=-1.5:LRA=11 output.wav
```

## Community Packs

See [PACKS.md](../PACKS.md) for community-contributed packs.

To submit your pack, open a PR adding your entry to `PACKS.md`.
