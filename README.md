<div align="center">
  <img src="docs/assets/banner.png" alt="claude-code-sounds" width="600" />
</div>

<div align="center">

[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Validate](https://github.com/dragon1086/claude-code-sounds/actions/workflows/validate.yml/badge.svg)](https://github.com/dragon1086/claude-code-sounds/actions/workflows/validate.yml)
![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Linux%20%7C%20Windows-lightgrey)
![Hook Coverage](https://img.shields.io/badge/hooks-27%20events%20covered-7c3aed)

</div>

<div align="center">

**[한국어](README.ko.md) · [中文](README.zh.md) · [Español](README.es.md) · [日本語](README.ja.md)**

</div>

Audio feedback for every Claude Code lifecycle event — powered by the native hooks system. Ships with real ElevenLabs-generated voice files. Swap any sound by replacing one file.

## How it works

<div align="center">
  <img src="docs/assets/flow.png" alt="How claude-code-sounds works" width="700" />
</div>

## Install

### Option A — Plugin marketplace (recommended)

```
/plugin marketplace add https://github.com/dragon1086/claude-code-sounds
/plugin install claude-code-sounds
```

When prompted for scope:

| Choice | What happens |
|--------|-------------|
| **user (global)** ✅ | Sounds play in every project automatically |
| project | Sounds silent — run `setup-project` once per project (see below) |
| local | Same as project, but excluded from git (personal config) — also needs `setup-project` |

> **After install:** Restart Claude Code for hooks to activate.

#### Project-scope fix

If you chose project scope (or want per-project opt-in), run once inside the project:

```bash
bash "$(find ~/.claude/plugins/cache/claude-code-sounds -name "claude-sounds.sh" | head -1)" setup-project
```

Then restart Claude Code. This copies hooks into `.claude/hooks/` and registers them in `.claude/settings.json`.

---

### Option B — curl (project scope)

Installs into the current project's `.claude/hooks/`. Run from inside a project directory. Repeat for each project you want sounds in.

```bash
curl -fsSL https://raw.githubusercontent.com/dragon1086/claude-code-sounds/main/install.sh | bash
```

### Option C — Manual clone (project scope)

Same as Option B — installs into the current project only.

```bash
git clone https://github.com/dragon1086/claude-code-sounds
cd claude-code-sounds && ./install.sh
```

> **After install:** Restart Claude Code for hooks to activate.

## Requirements

- Python 3
- macOS (`afplay`), Linux (`paplay` / `aplay` / `ffplay`), or Windows (built-in `winsound`)

## Hook Coverage

All 27 Claude Code hook events are wired, plus 6 agent-scoped events:

| Category | Events |
|----------|--------|
| Session | `SessionStart`, `SessionEnd`, `Setup` |
| Tool | `PreToolUse`, `PostToolUse`, `PostToolUseFailure`, `PermissionRequest`, `PermissionDenied` |
| Turn | `UserPromptSubmit`, `Stop`, `StopFailure`, `Notification` |
| Subagent | `SubagentStart`, `SubagentStop`, `TeammateIdle`, `TaskCreated`, `TaskCompleted` |
| Context | `PreCompact`, `PostCompact`, `InstructionsLoaded`, `ConfigChange` |
| Environment | `CwdChanged`, `FileChanged`, `WorktreeCreate`, `WorktreeRemove` |
| MCP | `Elicitation`, `ElicitationResult` |

## Sound Packs

Switch all sounds at once using the `claude-sounds.sh use` command. This is the only way to switch packs — `activePack` in `hooks-config.json` is a tracking label only and does not affect which sounds are played.

### Available packs

| Pack | Description |
|------|-------------|
| `onepiece` | Real One Piece anime voices — Luffy, Zoro, Robin and more |
| `best-practice` | ElevenLabs "Samara X" voice — ported from claude-code-best-practice |
| `silent` | 100ms silence — disables all sounds without removing hooks |
| `default` | Minimal default sound set |

### Switching packs

**Plugin marketplace (user scope) — most common:**

```bash
bash "$(find ~/.claude/plugins/cache/claude-code-sounds -name "claude-sounds.sh" | sort -V | tail -1)" use onepiece
```

No reinstall needed. The change takes effect immediately.

**install.sh / manual clone:**

```bash
# Step 1: switch the pack in the repo
./claude-sounds.sh use onepiece

# Step 2: re-apply to your project
./install.sh --force
```

To see which pack is currently active: `./claude-sounds.sh current`

To list all available packs: `./claude-sounds.sh list`

### Community packs

See [PACKS.md](PACKS.md) for community-contributed packs. To contribute your own, see [packs/README.md](packs/README.md).

## Customize Sounds

Replace any file in `.claude/hooks/sounds/{event}/`:

```
.claude/hooks/sounds/stop/
└── stop.wav   ← replace this with your own sound
```

File name must match the folder name. Both `.wav` and `.mp3` are supported (`.wav` tried first).

### Special: Bash command patterns

Certain bash commands trigger dedicated sounds. For example, `git commit` plays `pretooluse-git-committing.wav` instead of the generic `pretooluse.wav`.

Add your own patterns in `hooks.py`:

```python
BASH_PATTERNS = [
    (r'git commit', "pretooluse-git-committing"),  # included by default
    (r'npm test',   "pretooluse-npm-testing"),      # add your own
    (r'rm -rf',     "pretooluse-danger"),
    (r'git push',   "pretooluse-git-pushing"),
]
```

Each pattern needs a matching file in `sounds/pretooluse/pretooluse-{name}.wav`.

## Disable Hooks

To disable individual hooks without uninstalling, create `.claude/hooks/config/hooks-config.local.json` (git-ignored):

```json
{
  "disablePostToolUseHook": true,
  "disableLogging": true
}
```

See `hooks/config/hooks-config.local.json.example` for all available options.

## Agent Sounds

Subagent sessions can play different sounds. Wire hooks in your agent frontmatter:

```yaml
---
name: my-agent
hooks:
  PreToolUse:
    - type: command
      command: python3 $CLAUDE_PROJECT_DIR/.claude/hooks/scripts/hooks.py --agent=my-agent
      async: true
      timeout: 5000
  Stop:
    - type: command
      command: python3 $CLAUDE_PROJECT_DIR/.claude/hooks/scripts/hooks.py --agent=my-agent
      async: true
      timeout: 5000
---
```

Sound files go in `agent_pretooluse/`, `agent_stop/`, etc.

## Uninstall

```bash
./uninstall.sh
```

## Credits

Inspired by [shanraisshan/claude-code-best-practice](https://github.com/shanraisshan/claude-code-best-practice), which first demonstrated wiring audio feedback into Claude Code hooks. This project extracts and generalizes that idea into a standalone, installable plugin with full hook coverage, sound packs, and cross-platform support.

## License

MIT
