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

**[English](README.md) · [中文](README.zh.md) · [Español](README.es.md) · [日本語](README.ja.md)**

</div>

네이티브 훅 시스템으로 구동되는 Claude Code 라이프사이클 이벤트별 오디오 피드백 — 실제 ElevenLabs로 생성된 음성 파일과 함께 제공됩니다. 파일 하나를 교체하는 것만으로 원하는 소리로 바꿀 수 있습니다.

## 동작 방식

<div align="center">
  <img src="docs/assets/flow.png" alt="How claude-code-sounds works" width="700" />
</div>

## 설치

### 방법 A — 플러그인 마켓플레이스 (권장)

```
/plugin marketplace add https://github.com/dragon1086/claude-code-sounds
/plugin install claude-code-sounds
```

스콥 선택 시:

| 선택 | 동작 |
|------|------|
| **user (global)** ✅ | 모든 프로젝트에서 자동으로 소리 남 |
| project | 소리 안 남 — 프로젝트마다 `setup-project` 한 번 실행 필요 (아래 참조) |

> **설치 후:** 훅 활성화를 위해 Claude Code를 재시작하세요.

#### project 스콥 설치 시 추가 설정

project 스콥으로 설치한 경우, 해당 프로젝트 안에서 한 번 실행:

```bash
bash "$(find ~/.claude/plugins/cache/claude-code-sounds -name "claude-sounds.sh" | head -1)" setup-project
```

Claude Code 재시작 후 소리가 납니다. 이 명령어는 hooks를 `.claude/hooks/`에 복사하고 `.claude/settings.json`에 등록해요.

---

### 방법 B — curl

```bash
curl -fsSL https://raw.githubusercontent.com/dragon1086/claude-code-sounds/main/install.sh | bash
```

### 방법 C — 직접 클론

```bash
git clone https://github.com/dragon1086/claude-code-sounds
cd claude-code-sounds && ./install.sh
```

> **설치 후:** 훅 활성화를 위해 Claude Code를 재시작하세요.

## 요구 사항

- Python 3
- macOS (`afplay`), Linux (`paplay` / `aplay` / `ffplay`), 또는 Windows (내장 `winsound`)

## 훅 커버리지

27개의 Claude Code 훅 이벤트 전체와 에이전트 전용 이벤트 6개가 연결되어 있습니다:

| 카테고리 | 이벤트 |
|----------|--------|
| 세션 | `SessionStart`, `SessionEnd`, `Setup` |
| 도구 | `PreToolUse`, `PostToolUse`, `PostToolUseFailure`, `PermissionRequest`, `PermissionDenied` |
| 턴 | `UserPromptSubmit`, `Stop`, `StopFailure`, `Notification` |
| 서브에이전트 | `SubagentStart`, `SubagentStop`, `TeammateIdle`, `TaskCreated`, `TaskCompleted` |
| 컨텍스트 | `PreCompact`, `PostCompact`, `InstructionsLoaded`, `ConfigChange` |
| 환경 | `CwdChanged`, `FileChanged`, `WorktreeCreate`, `WorktreeRemove` |
| MCP | `Elicitation`, `ElicitationResult` |

## 소리 커스터마이즈

`.claude/hooks/sounds/{event}/` 내의 파일을 교체하세요:

```
.claude/hooks/sounds/stop/
└── stop.wav   ← 이 파일을 원하는 소리로 교체하세요
```

파일 이름은 폴더 이름과 일치해야 합니다. `.wav`와 `.mp3` 모두 지원됩니다 (`.wav`를 먼저 시도합니다).

### 특수 기능: Bash 명령 패턴

특정 bash 명령은 전용 소리를 재생합니다. 예를 들어, `git commit`은 일반적인 `pretooluse.wav` 대신 `pretooluse-git-committing.wav`를 재생합니다.

`hooks.py`에서 직접 패턴을 추가할 수 있습니다:

```python
BASH_PATTERNS = [
    (r'git commit', "pretooluse-git-committing"),  # 기본 포함
    (r'npm test',   "pretooluse-npm-testing"),      # 직접 추가
    (r'rm -rf',     "pretooluse-danger"),
    (r'git push',   "pretooluse-git-pushing"),
]
```

각 패턴에는 `sounds/pretooluse/pretooluse-{name}.wav`에 대응하는 파일이 필요합니다.

## 훅 비활성화

`.claude/hooks/config/hooks-config.local.json` 파일을 생성하세요 (git에서 무시됨):

```json
{
  "disablePostToolUseHook": true,
  "disableLogging": true
}
```

모든 옵션은 `hooks/config/hooks-config.local.json.example`을 참고하세요.

## 사운드 팩

모든 소리를 한 번에 교체합니다:

```bash
# 내장 팩
claude-sounds use silent    # 훅을 제거하지 않고 모든 소리를 비활성화

# 커뮤니티 팩 (외부 GitHub 저장소)
claude-sounds use https://github.com/someone/star-trek-sounds
```

커뮤니티 팩은 [PACKS.md](PACKS.md)를 참고하세요. 팩을 기여하려면 [packs/README.md](packs/README.md)를 참고하세요.

## 에이전트 소리

서브에이전트 세션은 다른 소리를 재생할 수 있습니다. 에이전트 프론트매터에 훅을 연결하세요:

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

사운드 파일은 `agent_pretooluse/`, `agent_stop/` 등에 저장합니다.

## 제거

```bash
./uninstall.sh
```

## 크레딧

[shanraisshan/claude-code-best-practice](https://github.com/shanraisshan/claude-code-best-practice)에서 영감을 받아 제작되었습니다. 이 프로젝트는 Claude Code hooks에 오디오 피드백을 연결하는 아이디어를 독립적인 플러그인으로 발전시킨 것입니다.

## 라이선스

MIT
