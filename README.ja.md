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

**[English](README.md) · [한국어](README.ko.md) · [中文](README.zh.md) · [Español](README.es.md)**

</div>

Claude Code のすべてのライフサイクルイベントに音声フィードバックを提供します — ネイティブのフックシステムで動作します。ElevenLabs で生成された本物の音声ファイルが同梱されています。ファイルを一つ差し替えるだけで任意のサウンドに変更できます。

## 仕組み

<div align="center">
  <img src="docs/assets/flow.png" alt="How claude-code-sounds works" width="700" />
</div>

## インストール

### Claude Code プラグインマーケットプレイス経由（推奨）

```
/plugin marketplace add https://github.com/dragon1086/claude-code-sounds
/plugin install claude-code-sounds
```

### curl 経由

```bash
curl -fsSL https://raw.githubusercontent.com/dragon1086/claude-code-sounds/main/install.sh | bash
```

### クローン経由

```bash
git clone https://github.com/dragon1086/claude-code-sounds
cd claude-code-sounds && ./install.sh
```

> **インストール後：** Claude Code を終了して再起動するか、新しいセッションを開始してください。インストーラーが `.claude/settings.json` にフックを登録し、次回セッション開始時に有効になります。

## 必要要件

- Python 3
- macOS（`afplay`）、Linux（`paplay` / `aplay` / `ffplay`）、または Windows（組み込みの `winsound`）

## フックのカバレッジ

Claude Code の 27 すべてのフックイベントに加え、エージェントスコープの 6 イベントが対応しています：

| カテゴリ | イベント |
|----------|--------|
| セッション | `SessionStart`, `SessionEnd`, `Setup` |
| ツール | `PreToolUse`, `PostToolUse`, `PostToolUseFailure`, `PermissionRequest`, `PermissionDenied` |
| ターン | `UserPromptSubmit`, `Stop`, `StopFailure`, `Notification` |
| サブエージェント | `SubagentStart`, `SubagentStop`, `TeammateIdle`, `TaskCreated`, `TaskCompleted` |
| コンテキスト | `PreCompact`, `PostCompact`, `InstructionsLoaded`, `ConfigChange` |
| 環境 | `CwdChanged`, `FileChanged`, `WorktreeCreate`, `WorktreeRemove` |
| MCP | `Elicitation`, `ElicitationResult` |

## サウンドのカスタマイズ

`.claude/hooks/sounds/{event}/` 内の任意のファイルを差し替えます：

```
.claude/hooks/sounds/stop/
└── stop.wav   ← これを自分のサウンドに差し替える
```

ファイル名はフォルダ名と一致している必要があります。`.wav` と `.mp3` の両方がサポートされています（`.wav` が優先されます）。

### 特別機能: Bash コマンドパターン

特定の bash コマンドは専用のサウンドをトリガーします。たとえば、`git commit` を実行すると汎用の `pretooluse.wav` の代わりに `pretooluse-git-committing.wav` が再生されます。

`hooks.py` に独自のパターンを追加できます：

```python
BASH_PATTERNS = [
    (r'git commit', "pretooluse-git-committing"),  # included by default
    (r'npm test',   "pretooluse-npm-testing"),      # add your own
    (r'rm -rf',     "pretooluse-danger"),
    (r'git push',   "pretooluse-git-pushing"),
]
```

各パターンには `sounds/pretooluse/pretooluse-{name}.wav` に対応するファイルが必要です。

## フックの無効化

`.claude/hooks/config/hooks-config.local.json` を作成します（git で無視されます）：

```json
{
  "disablePostToolUseHook": true,
  "disableLogging": true
}
```

すべてのオプションについては `hooks/config/hooks-config.local.json.example` を参照してください。

## サウンドパック

すべてのサウンドを一度に切り替えます：

```bash
# 組み込みパック
claude-sounds use silent    # フックを削除せずにすべてのサウンドを無効化

# コミュニティパック（外部の GitHub リポジトリ）
claude-sounds use https://github.com/someone/star-trek-sounds
```

コミュニティパックについては [PACKS.md](PACKS.md) を参照してください。パックを提供する場合は [packs/README.md](packs/README.md) を参照してください。

## エージェントサウンド

サブエージェントセッションでは異なるサウンドを再生できます。エージェントのフロントマターにフックを設定します：

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

サウンドファイルは `agent_pretooluse/`、`agent_stop/` などに配置します。

## アンインストール

```bash
./uninstall.sh
```

## クレジット

[shanraisshan/claude-code-best-practice](https://github.com/shanraisshan/claude-code-best-practice) にインスパイアされて作成されました。このプロジェクトは、Claude Code のオーディオフィードバックのアイデアを独立したインストール可能なプラグインとして発展させたものです。

## ライセンス

MIT
