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

<div align="center">

[![원피스 사운드팩 — 데모 영상](https://img.youtube.com/vi/wIA4PilUQpo/maxresdefault.jpg)](https://youtu.be/wIA4PilUQpo)

</div>

Claude Code가 작업할 때마다 소리로 알려주는 플러그인입니다. 세션 시작, 파일 수정, 작업 완료 등 27가지 이벤트에 효과음이 연결되어 있어요. 기본 팩은 원피스 애니메이션 음성으로 구성되어 있고, 설정 파일 하나만 바꾸면 다른 팩으로 전환할 수 있습니다.

## 동작 방식

<div align="center">
  <img src="docs/assets/flow.png" alt="How claude-code-sounds works" width="700" />
</div>

Claude Code의 훅(hook) 시스템을 이용해서, 특정 이벤트가 발생할 때마다 Python 스크립트가 실행되어 소리를 재생합니다. 별도 데몬이나 백그라운드 프로세스 없이 동작해요.

## 설치

### 방법 A — 플러그인 마켓플레이스 (권장)

Claude Code 채팅창에서 아래 명령어를 입력하세요:

```
/plugin marketplace add https://github.com/dragon1086/claude-code-sounds
/plugin install claude-code-sounds
```

스콥 선택 화면이 나타나면:

| 선택 | 동작 |
|------|------|
| **user (global)** ✅ | 모든 프로젝트에서 자동으로 소리가 납니다 — 이걸 추천해요 |
| project | 이 프로젝트에서만 사용 — 아래 추가 설정 필요 |
| local | project와 같지만 git에 포함되지 않음 (개인 설정용) — 추가 설정 필요 |

> **설치 후:** Claude Code를 재시작해야 훅이 활성화됩니다.

#### project/local 스콥으로 설치한 경우

프로젝트 폴더 안에서 아래 명령어를 한 번 실행하세요:

```bash
bash "$(find ~/.claude/plugins/cache/claude-code-sounds -name "claude-sounds.sh" | head -1)" setup-project
```

그 후 Claude Code를 재시작하면 소리가 납니다. 이 명령어는 훅 파일을 `.claude/hooks/`에 복사하고 `.claude/settings.json`에 등록해줍니다.

---

### 방법 B — curl 한 줄 설치 (project 스콥)

현재 프로젝트의 `.claude/hooks/`에 설치됩니다. 프로젝트 디렉토리 안에서 실행하세요. 소리를 사용하고 싶은 프로젝트마다 반복 실행이 필요합니다.

터미널에서 바로 실행할 수 있어요:

```bash
curl -fsSL https://raw.githubusercontent.com/dragon1086/claude-code-sounds/main/install.sh | bash
```

### 방법 C — 직접 클론 (project 스콥)

방법 B와 동일하게 현재 프로젝트에만 설치됩니다.

```bash
git clone https://github.com/dragon1086/claude-code-sounds
cd claude-code-sounds && ./install.sh
```

> **설치 후:** Claude Code를 재시작해야 훅이 활성화됩니다.

## 요구 사항

- Python 3
- macOS (`afplay`), Linux (`paplay` / `aplay` / `ffplay`), 또는 Windows (내장 `winsound`)

별도 라이브러리 설치는 필요 없어요.

## 사운드 팩 전환

`claude-sounds.sh use` 명령어로 모든 소리를 한 번에 바꿀 수 있어요. 팩을 바꾸는 방법은 이것뿐입니다. `hooks-config.json`의 `activePack`은 마지막으로 적용된 팩을 표시해주는 레이블일 뿐이고, 실제로 어떤 소리가 재생될지에는 영향을 주지 않아요.

### 기본 제공 팩

| 팩 이름 | 설명 |
|---------|------|
| `onepiece` | 원피스 애니메이션 실제 음성 — 루피, 조로, 로빈 등의 명장면 |
| `best-practice` | ElevenLabs "Samara X" 음성 — claude-code-best-practice 프로젝트에서 가져온 팩 |
| `silent` | 100ms 무음 — 훅을 제거하지 않고 소리만 끄고 싶을 때 |
| `default` | 기본 효과음 세트 |

### 팩 바꾸는 방법

**플러그인 마켓플레이스 (user 스콥) — 가장 일반적인 경우:**

```bash
bash "$(find ~/.claude/plugins/cache/claude-code-sounds -name "claude-sounds.sh" | sort -V | tail -1)" use onepiece
```

재설치 없이 바로 적용됩니다.

**install.sh / 직접 클론한 경우:**

```bash
# 1단계: 리포지토리에서 팩 전환
./claude-sounds.sh use onepiece

# 2단계: 프로젝트에 다시 적용
./install.sh --force
```

현재 적용된 팩 확인: `./claude-sounds.sh current`

사용 가능한 팩 목록 보기: `./claude-sounds.sh list`

### 커뮤니티 팩

다른 사용자들이 만든 팩은 [PACKS.md](PACKS.md)에서 확인할 수 있어요. 직접 팩을 만들어 기여하고 싶다면 [packs/README.md](packs/README.md)를 참고하세요.

## 소리 직접 바꾸기

특정 이벤트의 소리만 바꾸고 싶다면 `.claude/hooks/sounds/{이벤트명}/` 폴더의 파일을 교체하면 됩니다:

```
.claude/hooks/sounds/stop/
└── stop.wav   ← 이 파일을 원하는 소리로 교체하세요
```

파일 이름은 반드시 폴더 이름과 같아야 합니다. `.wav`와 `.mp3` 모두 지원되며, `.wav`를 먼저 찾습니다.

### 특수 기능: Bash 명령어별 소리

특정 bash 명령어에 전용 소리를 지정할 수 있어요. 예를 들어 `git commit` 실행 시 일반 `pretooluse.wav` 대신 `pretooluse-git-committing.wav`를 재생합니다.

`hooks.py`에서 패턴을 추가하세요:

```python
BASH_PATTERNS = [
    (r'git commit', "pretooluse-git-committing"),  # 기본 포함
    (r'npm test',   "pretooluse-npm-testing"),      # 직접 추가
    (r'rm -rf',     "pretooluse-danger"),
    (r'git push',   "pretooluse-git-pushing"),
]
```

각 패턴에는 `sounds/pretooluse/pretooluse-{이름}.wav` 파일이 필요합니다.

## 특정 훅 끄기

전체 제거 없이 일부 훅만 끄고 싶다면 `.claude/hooks/config/hooks-config.local.json` 파일을 만드세요 (git에서 자동으로 무시됩니다):

```json
{
  "disablePostToolUseHook": true,
  "disableLogging": true
}
```

사용 가능한 모든 옵션은 `hooks/config/hooks-config.local.json.example` 파일을 참고하세요.

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

## 에이전트별 소리 설정

서브에이전트 세션에 다른 소리를 지정할 수 있습니다. 에이전트 프론트매터에 훅을 추가하세요:

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

에이전트 전용 사운드 파일은 `agent_pretooluse/`, `agent_stop/` 등의 폴더에 저장합니다.

## 제거

```bash
./uninstall.sh
```

## 크레딧

Claude Code hooks에 오디오 피드백을 연결한다는 아이디어는 [shanraisshan/claude-code-best-practice](https://github.com/shanraisshan/claude-code-best-practice)에서 영감을 받았습니다. 이 프로젝트는 그 아이디어를 독립적인 플러그인으로 발전시켜, 전체 훅 커버리지와 사운드 팩, 크로스 플랫폼 지원을 추가한 버전입니다.

## 라이선스

MIT
