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

**[English](README.md) · [한국어](README.ko.md) · [Español](README.es.md) · [日本語](README.ja.md)**

</div>

为每一个 Claude Code 生命周期事件提供音频反馈 —— 由原生钩子系统驱动。内置真实的 ElevenLabs 生成语音文件。替换一个文件即可自定义任意音效。

## 工作原理

<div align="center">
  <img src="docs/assets/flow.png" alt="How claude-code-sounds works" width="700" />
</div>

## 安装

### 方式 A — 插件市场（推荐）

```
/plugin marketplace add https://github.com/dragon1086/claude-code-sounds
/plugin install claude-code-sounds
```

选择范围时：

| 选项 | 效果 |
|------|------|
| **user (global)** ✅ | 所有项目自动播放声音 |
| project | 无声音 — 需在每个项目中运行一次 `setup-project`（见下文） |

> **安装后：** 重启 Claude Code 以激活钩子。

#### project 范围修复

若已选择 project 范围，在项目目录内运行一次：

```bash
bash "$(find ~/.claude/plugins/cache/claude-code-sounds -name "claude-sounds.sh" | head -1)" setup-project
```

重启 Claude Code 后即可播放声音。

---

### 方式 B — curl

```bash
curl -fsSL https://raw.githubusercontent.com/dragon1086/claude-code-sounds/main/install.sh | bash
```

### 方式 C — 手动克隆

```bash
git clone https://github.com/dragon1086/claude-code-sounds
cd claude-code-sounds && ./install.sh
```

> **安装后：** 重启 Claude Code 以激活钩子。

## 环境要求

- Python 3
- macOS（`afplay`）、Linux（`paplay` / `aplay` / `ffplay`）或 Windows（内置 `winsound`）

## 钩子覆盖范围

所有 27 个 Claude Code 钩子事件均已接入，另加 6 个 agent 作用域事件：

| 类别 | 事件 |
|------|------|
| 会话 | `SessionStart`, `SessionEnd`, `Setup` |
| 工具 | `PreToolUse`, `PostToolUse`, `PostToolUseFailure`, `PermissionRequest`, `PermissionDenied` |
| 轮次 | `UserPromptSubmit`, `Stop`, `StopFailure`, `Notification` |
| 子 Agent | `SubagentStart`, `SubagentStop`, `TeammateIdle`, `TaskCreated`, `TaskCompleted` |
| 上下文 | `PreCompact`, `PostCompact`, `InstructionsLoaded`, `ConfigChange` |
| 环境 | `CwdChanged`, `FileChanged`, `WorktreeCreate`, `WorktreeRemove` |
| MCP | `Elicitation`, `ElicitationResult` |

## 自定义音效

替换 `.claude/hooks/sounds/{event}/` 中的任意文件：

```
.claude/hooks/sounds/stop/
└── stop.wav   ← 用你自己的音效替换这个文件
```

文件名必须与文件夹名一致。支持 `.wav` 和 `.mp3` 格式（优先尝试 `.wav`）。

### 特殊：Bash 命令模式

特定 bash 命令会触发专属音效。例如，`git commit` 会播放 `pretooluse-git-committing.wav` 而不是通用的 `pretooluse.wav`。

在 `hooks.py` 中添加自定义模式：

```python
BASH_PATTERNS = [
    (r'git commit', "pretooluse-git-committing"),  # 默认包含
    (r'npm test',   "pretooluse-npm-testing"),      # 添加自定义
    (r'rm -rf',     "pretooluse-danger"),
    (r'git push',   "pretooluse-git-pushing"),
]
```

每个模式需要在 `sounds/pretooluse/pretooluse-{name}.wav` 中有对应的文件。

## 禁用钩子

创建 `.claude/hooks/config/hooks-config.local.json`（已加入 git 忽略列表）：

```json
{
  "disablePostToolUseHook": true,
  "disableLogging": true
}
```

所有可用选项请参见 `hooks/config/hooks-config.local.json.example`。

## 音效包

一键切换所有音效：

```bash
# 内置音效包
claude-sounds use silent    # 在不移除钩子的情况下禁用所有音效

# 社区音效包（外部 GitHub 仓库）
claude-sounds use https://github.com/someone/star-trek-sounds
```

社区音效包请参见 [PACKS.md](PACKS.md)。如需贡献音效包，请参见 [packs/README.md](packs/README.md)。

## Agent 音效

子 Agent 会话可以播放不同的音效。在 agent frontmatter 中接入钩子：

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

音效文件存放于 `agent_pretooluse/`、`agent_stop/` 等目录中。

## 卸载

```bash
./uninstall.sh
```

## 致谢

本项目受 [shanraisshan/claude-code-best-practice](https://github.com/shanraisshan/claude-code-best-practice) 启发，该项目首次展示了将音频反馈集成到 Claude Code hooks 的方法。本项目将这一想法提炼为独立的可安装插件，支持全量 hook 事件、音效包和跨平台。

## 许可证

MIT
