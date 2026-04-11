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

<div align="center">
<br>

*"当所有人都拥有相同的 AI，品味才是真正的差异化。"*  
<sub>— Kira Klaas</sub>

<br>

## **✦ 让你的 AI，听起来像你。✦**

<br>
</div>

Claude Code 每次执行操作时都会有声音提示的插件。会话开始、文件修改、任务完成等 27 种事件都有对应的音效。本项目的代表音效包采用海贼王动漫真实语音，只需修改一个配置文件即可切换到其他音效包。

## 演示视频

点击缩略图播放演示：

<div align="center">

[![海贼王音效包 — 演示视频](https://img.youtube.com/vi/wIA4PilUQpo/maxresdefault.jpg)](https://youtu.be/wIA4PilUQpo)

</div>

## ⚙️ 工作原理

<div align="center">
  <img src="docs/assets/flow.png" alt="How claude-code-sounds works" width="700" />
</div>

利用 Claude Code 的钩子（hook）系统，在特定事件触发时运行 Python 脚本播放声音。无需额外的守护进程或后台服务。

## 🚀 安装

### 方式 A — 插件市场（推荐）

在 Claude Code 聊天窗口中输入以下命令：

```
/plugin marketplace add https://github.com/dragon1086/claude-code-sounds
/plugin install claude-code-sounds
```

选择范围时：

| 选项 | 效果 |
|------|------|
| **user (global)** ✅ | 所有项目自动播放声音 — 推荐选这个 |
| project | 仅在此项目中使用 — 需要额外设置（见下文） |
| local | 与 project 相同，但不纳入 git（个人配置用）— 同样需要额外设置 |

> [!IMPORTANT]
> 安装后请重启 Claude Code 以激活钩子。

#### 选择 project/local 范围后的额外设置

在项目目录内运行一次：

```bash
bash "$(find ~/.claude/plugins/cache/claude-code-sounds -name "claude-sounds.sh" | head -1)" setup-project
```

重启 Claude Code 后即可播放声音。该命令会将钩子文件复制到 `.claude/hooks/` 并注册到 `.claude/settings.json`。

---

### 方式 B — curl 一键安装（project 范围）

安装到当前项目的 `.claude/hooks/` 目录。请在项目目录内运行。每个需要声音的项目都需要单独安装。

```bash
curl -fsSL https://raw.githubusercontent.com/dragon1086/claude-code-sounds/main/install.sh | bash
```

### 方式 C — 手动克隆（project 范围）

与方式 B 相同，仅安装到当前项目。

```bash
git clone https://github.com/dragon1086/claude-code-sounds
cd claude-code-sounds && ./install.sh
```

> [!IMPORTANT]
> 安装后请重启 Claude Code 以激活钩子。

## 📋 环境要求

- Python 3
- macOS（`afplay`）、Linux（`paplay` / `aplay` / `ffplay`）或 Windows（内置 `winsound`）

无需安装额外的第三方库。

## 🎵 音效包

使用 `claude-sounds.sh use` 命令一次性切换所有音效。这是切换音效包的唯一方式 — `hooks-config.json` 中的 `activePack` 只是显示上次应用了哪个包的标签，不影响实际播放的音效。

### 内置音效包

| 包名 | 说明 | 来源 |
|------|------|------|
| 🏴‍☠️ **`onepiece`** | **[代表作]** 海贼王真实动漫语音 — 路飞、索隆、罗宾、弗兰奇、布鲁克等 | 原版动漫 |
| 🎮 **`faker`** | T1 Faker（이상혁）— ElevenLabs IVC 声音克隆 | ElevenLabs IVC |
| ⚔️ **`kimetsu`** | 鬼灭之刃 — 炭治郎、炎柱、善逸、伊之助等 | ElevenLabs TTS |
| 🔊 **`best-practice`** | ElevenLabs "Samara X" — 来自 [claude-code-best-practice](https://github.com/shanraisshan/claude-code-best-practice) | ElevenLabs TTS |
| 🔇 **`silent`** | 100ms 静音 — 不删除钩子的情况下关闭所有声音 | — |
| ⚙️ **`default`** | 默认基础音效 | — |

### 社区音效包

> [!TIP]
> **欢迎投稿！** 任何主题、任何作品、任何语言 — 大约 15 分钟即可完成。详见 **[packs/README.md](packs/README.md)**。

| 包名 | 作者 | 说明 |
|------|------|------|
| _(成为第一个贡献者！)_ | | |

### 代表音效包 — 海贼王

本项目的起源与代表音效包。路飞、索隆、娜美、罗宾、弗兰奇、布鲁克等角色的真实动漫语音，与 Claude Code 生命周期事件一一对应。

完整曲目列表请参见 [packs/onepiece/](packs/onepiece/)。

### 切换方法

**插件市场（user 范围）— 最常见的情况：**

```bash
bash "$(find ~/.claude/plugins/cache/claude-code-sounds -name "claude-sounds.sh" | sort -V | tail -1)" use onepiece
```

无需重新安装，立即生效。

**install.sh / 手动克隆的情况：**

```bash
# 第一步：在仓库中切换音效包
./claude-sounds.sh use onepiece

# 第二步：重新应用到项目
./install.sh --force
```

查看当前使用的音效包：`./claude-sounds.sh current`

列出所有可用音效包：`./claude-sounds.sh list`

## ✏️ 自定义单个音效

如果只想修改某个事件的声音，替换 `.claude/hooks/sounds/{事件名}/` 目录下的文件即可：

```
.claude/hooks/sounds/stop/
└── stop.wav   ← 用你的音效文件替换这个
```

文件名必须与文件夹名一致。支持 `.wav` 和 `.mp3` 格式（优先使用 `.wav`）。

### 特殊功能：Bash 命令专属音效

可以为特定 bash 命令指定专属音效。例如执行 `git commit` 时，会播放 `pretooluse-git-committing.wav` 而不是通用的 `pretooluse.wav`。

在 `hooks.py` 中添加自定义模式：

```python
BASH_PATTERNS = [
    (r'git commit', "pretooluse-git-committing"),  # 默认包含
    (r'npm test',   "pretooluse-npm-testing"),      # 自定义添加
    (r'rm -rf',     "pretooluse-danger"),
    (r'git push',   "pretooluse-git-pushing"),
]
```

每个模式需要在 `sounds/pretooluse/pretooluse-{名称}.wav` 中有对应文件。

## 🔕 禁用特定钩子

无需卸载，只想关闭部分钩子时，创建 `.claude/hooks/config/hooks-config.local.json` 文件（git 自动忽略）：

```json
{
  "disablePostToolUseHook": true,
  "disableLogging": true
}
```

所有可用选项请参见 `hooks/config/hooks-config.local.json.example`。

## 🪝 钩子覆盖范围

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

## 🤖 Agent 专属音效

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

## 🗑️ 卸载

```bash
./uninstall.sh
```

## 🙏 致谢

本项目受 [shanraisshan/claude-code-best-practice](https://github.com/shanraisshan/claude-code-best-practice) 启发，该项目首次展示了将音频反馈集成到 Claude Code hooks 的方法。本项目将这一想法提炼为独立的可安装插件，支持全量 hook 事件、音效包和跨平台运行。

## 许可证

MIT
