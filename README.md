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

### Via Claude Code plugin marketplace (recommended)

```
/plugin marketplace add https://github.com/dragon1086/claude-code-sounds
/plugin install claude-code-sounds
```

> **Important — select User scope:** When prompted, choose **"user (global)"** scope, not "project".
> Plugin hooks only fire when installed at user scope. Project-scope installs will enable the plugin
> entry but sounds will not play.

### Via curl

```bash
curl -fsSL https://raw.githubusercontent.com/dragon1086/claude-code-sounds/main/install.sh | bash
```

### Via clone

```bash
git clone https://github.com/dragon1086/claude-code-sounds
cd claude-code-sounds && ./install.sh
```

> **After install:** Quit and relaunch Claude Code (or start a new session) for the hooks to take effect.

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

Create `.claude/hooks/config/hooks-config.local.json` (git-ignored):

```json
{
  "disablePostToolUseHook": true,
  "disableLogging": true
}
```

See `hooks/config/hooks-config.local.json.example` for all options.

## Sound Packs

Switch all sounds at once:

```bash
# built-in packs
claude-sounds use silent    # disables all sounds without removing hooks

# community packs (external GitHub repos)
claude-sounds use https://github.com/someone/star-trek-sounds
```

See [PACKS.md](PACKS.md) for community packs. To contribute a pack, see [packs/README.md](packs/README.md).

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
