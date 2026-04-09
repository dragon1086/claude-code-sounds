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
| `default` | ElevenLabs "Samara X" voice — ships with the repo |
| `silent` | 100ms silence — disables sounds without removing hooks |

## Community Packs

See [PACKS.md](../PACKS.md) for community-contributed packs.

To submit your pack, open a PR adding your entry to `PACKS.md`.
