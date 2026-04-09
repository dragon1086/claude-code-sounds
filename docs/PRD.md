# PRD: claude-code-sounds

> **Status**: Draft  
> **Type**: Open-source Claude Code plugin  
> **Repo name**: `claude-code-sounds`  
> **License**: MIT  
> **Source**: extracted from `claude-code-best-practice` (`.claude/hooks/`)

---

## 1. Problem

Claude Code's hooks system supports 27 lifecycle events — but there is no standalone, installable plugin that maps all 27 events to audio files out of the box. Existing solutions (claudio, cc-hooks, etc.) either:

- Cover only 3 hook events (PreToolUse, PostToolUse, UserPromptSubmit)
- Require TTS providers or external dependencies
- Don't ship real audio files users can swap

Developers who want rich audio feedback for every Claude Code lifecycle moment have to wire everything from scratch.

---

## 2. Goal

A Claude Code plugin that:

1. **Installs in one command** via the native Claude Code plugin marketplace
2. **Ships real audio files** (ElevenLabs-generated voice) for all 27 hook events out of the box
3. **Requires zero configuration** to hear the first sound after install
4. **Lets users swap any sound** by replacing a single file in the sounds folder
5. **Supports sound packs** — wholesale swap of all sounds at once

---

## 3. Non-Goals

- No TTS generation at runtime (generate offline with ElevenLabs/gTTS, then drop in)
- No GUI / dashboard
- No global `~/.claude` install (project-scoped, respects per-project isolation)
- No audio format conversion (ship `.wav` + `.mp3`; user provides their own in either)
- No hook decision/blocking logic — sounds only, all hooks are `async: true`

---

## 4. Core Design Principles

| Principle | Rationale |
|-----------|-----------|
| **Zero external dependencies** | `hooks.py` uses only Python stdlib (`subprocess`, `json`, `pathlib`, `re`, `argparse`) |
| **Cross-platform** | macOS: `afplay` (built-in) · Linux: `paplay`/`aplay`/`ffplay`/`mpg123` auto-detect · Windows: `winsound` (built-in) |
| **Fail silently** | Sound errors never block Claude — always `sys.exit(0)` |
| **Local override** | `hooks-config.local.json` overrides `hooks-config.json` — personal prefs stay git-ignored |
| **Drop-in swap** | Replace one file in `sounds/{event}/` → done. No config editing required |
| **Extensible patterns** | Bash command patterns let you add new sounds for specific commands (see §7) |

---

## 5. Installation

### Primary: Claude Code Plugin Marketplace (recommended)

```bash
/plugin marketplace add https://github.com/<org>/claude-code-sounds
/plugin install claude-code-sounds
```

This is the same pattern used by oh-my-claudecode and other first-class Claude Code plugins. Claude Code's plugin system copies the plugin into `.claude/` and wires hooks automatically.

### Alternative: curl one-liner

```bash
curl -fsSL https://raw.githubusercontent.com/<org>/claude-code-sounds/main/install.sh | bash
```

### Alternative: clone and run

```bash
git clone https://github.com/<org>/claude-code-sounds
cd claude-code-sounds && ./install.sh
```

### What install does

1. Detects project root (walks up from `$PWD` looking for `.claude/`, fails loudly if not found)
2. Copies `hooks/` tree → `.claude/hooks/` (skips if exists; `--force` to overwrite)
3. Patches `.claude/settings.json` — adds all 27 hook entries pointing to `hooks.py`
4. Prints a summary of wired hooks and path to sounds folder

### Generated settings.json patch (abbreviated)

```json
{
  "hooks": {
    "SessionStart":       [{ "type": "command", "command": "python3 $CLAUDE_PROJECT_DIR/.claude/hooks/scripts/hooks.py", "async": true, "timeout": 5000, "once": true, "statusMessage": "SessionStart" }],
    "PreToolUse":         [{ "type": "command", "command": "python3 $CLAUDE_PROJECT_DIR/.claude/hooks/scripts/hooks.py", "async": true, "timeout": 5000, "statusMessage": "PreToolUse" }],
    "PostToolUse":        [{ "type": "command", "command": "python3 $CLAUDE_PROJECT_DIR/.claude/hooks/scripts/hooks.py", "async": true, "timeout": 5000, "statusMessage": "PostToolUse" }],
    "Stop":               [{ "type": "command", "command": "python3 $CLAUDE_PROJECT_DIR/.claude/hooks/scripts/hooks.py", "async": true, "timeout": 5000, "statusMessage": "Stop" }]
  }
}
```

*(All 27 events written by installer — abbreviated above for readability)*

---

## 6. Repository Structure

```
claude-code-sounds/
├── README.md
├── install.sh                          # Primary installer
├── install.py                          # Python fallback
├── uninstall.sh
│
├── hooks/                              # Payload — copied into user's .claude/hooks/
│   ├── scripts/
│   │   └── hooks.py                    # Core handler (zero deps, cross-platform)
│   ├── config/
│   │   ├── hooks-config.json           # Default: all hooks enabled
│   │   └── hooks-config.local.json.example
│   └── sounds/                         # Default sound pack (ships with real audio)
│       ├── sessionstart/
│       │   ├── sessionstart.wav
│       │   └── sessionstart.mp3
│       ├── pretooluse/
│       │   ├── pretooluse.wav
│       │   └── pretooluse-git-committing.wav   ← special pattern sound (see §7)
│       ├── posttooluse/
│       ├── posttoolusefailure/
│       ├── stop/
│       ├── ...                         # all 27 events
│       ├── agent_pretooluse/           # agent-scoped sounds (6 events)
│       ├── agent_posttooluse/
│       └── ...
│
└── packs/                              # Built-in community sound packs
    ├── README.md                       # Pack format spec + contribution guide
    ├── default/                        # Symlink or copy of hooks/sounds/ (ElevenLabs voice)
    ├── silent/                         # All 100ms silence — useful for disabling
    ├── retro-8bit/                     # Community contributed
    │   ├── pack.json
    │   └── sounds/                     # Same folder structure as hooks/sounds/
    └── ...
```

**Total audio slots**: 27 main events + 1 special (`pretooluse-git-committing`) + 6 agent events = **34 slots**

---

## 7. Bash Command Pattern System (Key Extensibility Feature)

The most powerful extensibility feature is **Bash command pattern matching**. When `PreToolUse` fires with the `Bash` tool, `hooks.py` inspects the actual command and can play a *different* sound based on what Claude is running.

### How it works

```python
# In hooks.py — BASH_PATTERNS list
BASH_PATTERNS = [
    (r'git commit', "pretooluse-git-committing"),   # plays pretooluse-git-committing.wav
]
```

When Claude runs `git commit -m "fix bug"`, instead of the generic `pretooluse.wav`, a dedicated `pretooluse-git-committing.wav` plays. This is a **regex → sound name** mapping.

### Why `pretooluse-git-committing` exists

Git commits are a moment of significance — code is being saved to history. A distinct sound makes this feel like a ceremony rather than a generic tool call. The source repo uses ElevenLabs to generate a voice that says something specific for this moment.

### Adding your own patterns

Users can extend `BASH_PATTERNS` in `hooks.py` with any regex:

```python
BASH_PATTERNS = [
    (r'git commit',   "pretooluse-git-committing"),   # already included
    (r'npm test',     "pretooluse-npm-testing"),       # add: tests running
    (r'docker build', "pretooluse-docker-building"),   # add: docker build starting
    (r'rm -rf',       "pretooluse-danger"),            # add: ⚠️ destructive command
    (r'git push',     "pretooluse-git-pushing"),       # add: code going to remote
]
```

Each pattern needs a corresponding sound file in `sounds/pretooluse/pretooluse-{name}.wav`. This is the recommended way to give your workflow a unique audio personality — one specific sound per meaningful command.

---

## 8. Hook Event Coverage

All 27 official Claude Code hooks are wired, grouped by category:

### Session Lifecycle
| Event | Sound folder | Fires when |
|-------|-------------|-----------|
| `SessionStart` | `sessionstart/` | Session opens or resumes |
| `SessionEnd` | `sessionend/` | Session closes |
| `Setup` | `setup/` | `/setup` command runs |

### Tool Execution
| Event | Sound folder | Fires when |
|-------|-------------|-----------|
| `PreToolUse` | `pretooluse/` | Before any tool call |
| `PreToolUse` (git commit) | `pretooluse/pretooluse-git-committing` | Specifically before `git commit` |
| `PostToolUse` | `posttooluse/` | After tool succeeds |
| `PostToolUseFailure` | `posttoolusefailure/` | After tool fails |
| `PermissionRequest` | `permissionrequest/` | Claude asks for permission |
| `PermissionDenied` | `permissiondenied/` | Auto-mode denies a tool call |

### Turn Lifecycle
| Event | Sound folder | Fires when |
|-------|-------------|-----------|
| `UserPromptSubmit` | `userpromptsubmit/` | User sends a message |
| `Stop` | `stop/` | Claude finishes responding |
| `StopFailure` | `stopfailure/` | Turn ends due to API error |
| `Notification` | `notification/` | Claude sends a notification |

### Subagent / Team
| Event | Sound folder | Fires when |
|-------|-------------|-----------|
| `SubagentStart` | `subagentstart/` | Subagent task begins |
| `SubagentStop` | `subagentstop/` | Subagent task completes |
| `TeammateIdle` | `teammateidle/` | Team agent goes idle |
| `TaskCreated` | `taskcreated/` | Task is created |
| `TaskCompleted` | `taskcompleted/` | Task completes |

### Context Management
| Event | Sound folder | Fires when |
|-------|-------------|-----------|
| `PreCompact` | `precompact/` | Before context compaction |
| `PostCompact` | `postcompact/` | After context compaction |
| `InstructionsLoaded` | `instructionsloaded/` | CLAUDE.md / rules loaded |
| `ConfigChange` | `configchange/` | Settings file changes |

### Environment
| Event | Sound folder | Fires when |
|-------|-------------|-----------|
| `CwdChanged` | `cwdchanged/` | Working directory changes |
| `FileChanged` | `filechanged/` | Watched file changes |
| `WorktreeCreate` | `worktreecreate/` | Git worktree created |
| `WorktreeRemove` | `worktreeremove/` | Git worktree removed |

### MCP
| Event | Sound folder | Fires when |
|-------|-------------|-----------|
| `Elicitation` | `elicitation/` | MCP server requests user input |
| `ElicitationResult` | `elicitationresult/` | User responds to MCP elicitation |

---

## 9. User Sound Customization

This is the entire UX for customization:

```
.claude/hooks/sounds/stop/
├── stop.wav   ← replace with your sound
└── stop.mp3   ← or this (.wav tried first)
```

**Rules:**
- File name must match the folder name (`stop/stop.wav`, `sessionstart/sessionstart.wav`)
- Supported formats: `.wav` tried first, then `.mp3`
- Special sounds: `pretooluse/pretooluse-git-committing.wav` — or add your own patterns (§7)
- Agent sounds: `agent_stop/agent_stop.wav` — only fire inside subagent sessions

**Disabling individual hooks** (no script editing needed):

```jsonc
// .claude/hooks/config/hooks-config.local.json  (git-ignored)
{
  "disablePostToolUseHook": true,   // too noisy during heavy tool use
  "disableLogging": true            // stop writing hooks-log.jsonl
}
```

---

## 10. Sound Pack System

### Pattern: oh-my-zsh style

Inspired by how oh-my-zsh handles themes and plugins:

- **Built-in packs** live in `packs/` inside this repo — maintained by the core team
- **External packs** are their own GitHub repos — listed in `PACKS.md` (curated wiki)
- **No central registry** — GitHub is the registry (URL = identity)

### Switching packs

```bash
# Switch to a built-in pack
claude-sounds use retro-8bit

# Switch to an external pack (GitHub URL)
claude-sounds use https://github.com/someone/star-trek-sounds

# List installed packs
claude-sounds list

# Preview what a pack contains
claude-sounds preview retro-8bit
```

### Pack format

A pack is a folder with:

```
my-pack/
├── pack.json          # { "name", "author", "description", "license", "preview_url" }
└── sounds/            # Identical structure to hooks/sounds/
    ├── sessionstart/sessionstart.wav
    ├── stop/stop.wav
    └── ...            # partial packs OK — missing slots fall back to default
```

**Partial packs are supported**: a pack only needs to include the sounds it wants to override. Missing slots fall back to the `default` pack. This means a `git-ceremony` pack could ship only `pretooluse-git-committing.wav` and leave everything else as-is.

### Built-in packs (shipped with repo)

| Pack | Description |
|------|-------------|
| `default` | ElevenLabs "Samara X" voice — the sounds from the source repo |
| `silent` | 100ms silence for all slots — effectively disables sounds without removing hooks |

### Community packs (external, listed in PACKS.md)

External packs are separate GitHub repos. Contribution = open a PR to add your repo URL to `PACKS.md`. No gatekeeping beyond basic content checks (no NSFW, no copyrighted audio).

```markdown
<!-- PACKS.md -->
## Community Sound Packs

| Pack | Author | Description | Install |
|------|--------|-------------|---------|
| [star-trek-bridge](https://github.com/...) | @someone | LCARS sounds | `claude-sounds use https://...` |
| [retro-8bit](https://github.com/...) | @someone | Chiptune beeps | `claude-sounds use https://...` |
```

---

## 11. Default Audio Files

The repo ships **real audio files** from the source repo, generated with ElevenLabs TTS (voice: "Samara X"). These are the sounds currently in `claude-code-best-practice/.claude/hooks/sounds/`.

This means: **install → sounds immediately work** with personality, not silence.

Users who want silence can switch to the `silent` pack: `claude-sounds use silent`

---

## 12. Agent Hook Support

Six events fire inside subagent sessions. Users wire them via agent frontmatter:

```yaml
# .claude/agents/my-agent.md
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

Agent sounds live in `agent_pretooluse/`, `agent_stop/`, etc. — separate from main session sounds so the "voice" of subagents can differ from the main session.

---

## 13. Platform Support Matrix

| Platform | Audio player | WAV | MP3 |
|----------|-------------|-----|-----|
| macOS | `afplay` (built-in) | ✅ | ✅ |
| Linux (PulseAudio) | `paplay` | ✅ | ❌ |
| Linux (ALSA) | `aplay` | ✅ | ❌ |
| Linux (FFmpeg) | `ffplay` | ✅ | ✅ |
| Linux (mpg123) | `mpg123` | ❌ | ✅ |
| Windows | `winsound` (built-in) | ✅ | ❌ |

> **Linux recommendation**: ship `.wav` files for maximum compatibility. The installer warns if no supported audio player is found.

---

## 14. Logging

Hook events logged to `.claude/hooks/logs/hooks-log.jsonl` by default:

```jsonc
{
  "hook_event_name": "PreToolUse",
  "tool_name": "Bash",
  "tool_input": { "command": "git commit -m 'fix'" },
  "session_id": "abc123"
}
```

Disable: `"disableLogging": true` in `hooks-config.local.json`.

---

## 15. Open Questions

| Question | Current decision |
|----------|-----------------|
| CLI tool name | `claude-sounds` (the management CLI shipped with the plugin) |
| Plugin manifest format | Follow Claude Code plugin spec (same as oh-my-claudecode) |
| Pack switching UX | `claude-sounds use <pack>` CLI vs manual file copy |
| CI | GitHub Actions: validate `HOOK_SOUND_MAP` keys match `sounds/` folder names, lint `hooks.py` |
| Sound generation guide | Document ElevenLabs workflow for contributors creating new packs |

---

## 16. Success Metrics

- User installs in under 60 seconds via `/plugin marketplace add`
- Sounds play immediately after install with no config
- Swapping one sound = replacing one file
- Switching an entire pack = one CLI command
- Works on macOS, Ubuntu, Windows without any installs beyond Python 3
