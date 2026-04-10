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

Claude Code が作業するたびに音で知らせてくれるプラグインです。セッション開始・ファイル変更・タスク完了など 27 種類のイベントに効果音が設定されています。デフォルトはワンピースのアニメ音声で、設定ファイルを一つ変えるだけで別のサウンドパックに切り替えられます。

## 仕組み

<div align="center">
  <img src="docs/assets/flow.png" alt="How claude-code-sounds works" width="700" />
</div>

Claude Code のフック（hook）システムを利用して、特定のイベントが発生するたびに Python スクリプトが実行され、音が鳴ります。別途デーモンやバックグラウンドプロセスは不要です。

## インストール

### 方法 A — プラグインマーケットプレイス（推奨）

Claude Code のチャット欄に以下を入力してください：

```
/plugin marketplace add https://github.com/dragon1086/claude-code-sounds
/plugin install claude-code-sounds
```

スコープ選択画面が表示されたら：

| 選択肢 | 動作 |
|--------|------|
| **user (global)** ✅ | すべてのプロジェクトで自動的に音が鳴ります — こちらがおすすめ |
| project | このプロジェクトのみで使用 — 追加設定が必要（下記参照） |
| local | project と同じですが git 除外（個人設定用）— 追加設定が必要 |

> **インストール後：** フックを有効にするため Claude Code を再起動してください。

#### project/local スコープでインストールした場合

プロジェクトフォルダ内で一度だけ以下を実行してください：

```bash
bash "$(find ~/.claude/plugins/cache/claude-code-sounds -name "claude-sounds.sh" | head -1)" setup-project
```

Claude Code を再起動すると音が鳴るようになります。このコマンドはフックを `.claude/hooks/` にコピーし、`.claude/settings.json` に登録します。

---

### 方法 B — curl で一発インストール（project スコープ）

現在のプロジェクトの `.claude/hooks/` にインストールされます。プロジェクトディレクトリ内で実行してください。音を使いたいプロジェクトごとに繰り返し実行が必要です。

```bash
curl -fsSL https://raw.githubusercontent.com/dragon1086/claude-code-sounds/main/install.sh | bash
```

### 方法 C — 手動クローン（project スコープ）

方法 B と同じく、現在のプロジェクトにのみインストールされます。

```bash
git clone https://github.com/dragon1086/claude-code-sounds
cd claude-code-sounds && ./install.sh
```

> **インストール後：** フックを有効にするため Claude Code を再起動してください。

## 必要要件

- Python 3
- macOS（`afplay`）、Linux（`paplay` / `aplay` / `ffplay`）、または Windows（組み込みの `winsound`）

追加ライブラリのインストールは不要です。

## サウンドパックの切り替え

`claude-sounds.sh use` コマンドですべての音を一括で切り替えられます。パックを切り替える方法はこれだけです — `hooks-config.json` の `activePack` は最後に適用したパックを表示するラベルにすぎず、実際に再生される音には影響しません。

### 組み込みパック一覧

| パック名 | 説明 |
|----------|------|
| `onepiece` | ワンピースの実際のアニメ音声 — ルフィ・ゾロ・ロビンなどの名場面 |
| `best-practice` | ElevenLabs "Samara X" 音声 — claude-code-best-practice プロジェクトから移植 |
| `silent` | 100ms の無音 — フックを削除せずに音だけ消したいときに |
| `default` | 基本デフォルト効果音セット |

### 切り替え方法

**プラグインマーケットプレイス（user スコープ）— 最もよくある使い方：**

```bash
bash "$(find ~/.claude/plugins/cache/claude-code-sounds -name "claude-sounds.sh" | sort -V | tail -1)" use onepiece
```

再インストール不要です。すぐに反映されます。

**install.sh / 手動クローンの場合：**

```bash
# ステップ 1: リポジトリでパックを切り替える
./claude-sounds.sh use onepiece

# ステップ 2: プロジェクトに再適用する
./install.sh --force
```

現在のパックを確認: `./claude-sounds.sh current`

利用可能なパック一覧を表示: `./claude-sounds.sh list`

### コミュニティパック

他のユーザーが作成したパックは [PACKS.md](PACKS.md) で確認できます。自分のパックを作って共有したい場合は [packs/README.md](packs/README.md) を参照してください。

## 個別の音を変える

特定イベントの音だけ変えたい場合は、`.claude/hooks/sounds/{イベント名}/` フォルダのファイルを差し替えます：

```
.claude/hooks/sounds/stop/
└── stop.wav   ← これを好きな音に差し替える
```

ファイル名はフォルダ名と一致させてください。`.wav` と `.mp3` の両方に対応しています（`.wav` が優先されます）。

### 特別機能：Bash コマンドごとの専用音

特定の bash コマンドに専用の音を割り当てることができます。たとえば `git commit` を実行すると、汎用の `pretooluse.wav` の代わりに `pretooluse-git-committing.wav` が再生されます。

`hooks.py` に独自パターンを追加してください：

```python
BASH_PATTERNS = [
    (r'git commit', "pretooluse-git-committing"),  # デフォルトで含まれています
    (r'npm test',   "pretooluse-npm-testing"),      # 自分で追加
    (r'rm -rf',     "pretooluse-danger"),
    (r'git push',   "pretooluse-git-pushing"),
]
```

各パターンに対応する `sounds/pretooluse/pretooluse-{名前}.wav` ファイルが必要です。

## 特定フックを無効にする

アンインストールせずに一部のフックだけ無効にしたい場合は、`.claude/hooks/config/hooks-config.local.json` を作成してください（git に自動的に無視されます）：

```json
{
  "disablePostToolUseHook": true,
  "disableLogging": true
}
```

利用可能なすべてのオプションは `hooks/config/hooks-config.local.json.example` を参照してください。

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

## エージェント専用サウンド

サブエージェントセッションで別の音を鳴らすことができます。エージェントのフロントマターにフックを追加してください：

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

エージェント専用のサウンドファイルは `agent_pretooluse/`、`agent_stop/` などに置いてください。

## アンインストール

```bash
./uninstall.sh
```

## クレジット

Claude Code のフックに音声フィードバックを組み込むというアイデアは [shanraisshan/claude-code-best-practice](https://github.com/shanraisshan/claude-code-best-practice) からインスパイアされています。このプロジェクトはそのアイデアを独立したプラグインとして発展させ、全フックイベント対応・サウンドパック・クロスプラットフォーム対応を追加したものです。

## ライセンス

MIT
