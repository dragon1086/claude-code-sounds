# 사운드팩 기여 가이드

**팩 기여를 환영합니다** — 어떤 테마, 팬덤, 언어든 좋아요.  
15분 정도면 만들 수 있어요.

바로가기: [빠른 시작](#빠른-시작) · [팩 형식](#팩-형식) · [오디오 가이드라인](#오디오-가이드라인) · [제출하기](#제출하기)

---

## 빠른 시작

아이디어부터 PR 머지까지 다섯 단계:

1. `packs/<팩이름>/` 폴더를 만들고 `sounds/` 서브폴더 생성
2. 오디오 파일(`.wav` 또는 `.mp3`) 추가
3. `pack.json` 작성
4. 오디오를 -20 LUFS로 정규화
5. PR 열기 — [PACKS.md](../PACKS.md)에 항목 추가

**부분 팩도 지원됩니다.** 덮어쓰고 싶은 이벤트만 포함하면 돼요. 없는 슬롯은 자동으로 `default` 팩을 사용합니다.

---

## 팩 형식

```
my-pack/
├── pack.json          # 필수 메타데이터
└── sounds/            # hooks/sounds/와 동일한 구조
    ├── sessionstart/
    │   └── sessionstart.wav
    ├── stop/
    │   └── stop.wav
    └── ...            # 덮어쓸 이벤트만 포함
```

### pack.json

```json
{
  "name": "my-pack",
  "author": "your-github-username",
  "description": "팩에 대한 한 줄 설명",
  "license": "MIT",
  "preview_url": "https://youtube.com/..."
}
```

| 필드 | 필수 | 비고 |
|------|------|------|
| `name` | ✅ | 폴더 이름과 일치 |
| `author` | ✅ | GitHub 사용자명 |
| `description` | ✅ | 한 문장 |
| `license` | ✅ | 예: `MIT`, `CC BY 4.0` |
| `preview_url` | — | 유튜브 데모 링크 권장 |

---

## 훅 이벤트 목록

소리를 지정할 수 있는 27개 이벤트:

| 이벤트 | 발생 시점 |
|--------|----------|
| `sessionstart` | 새 Claude Code 세션 시작 |
| `sessionend` | 세션 종료 |
| `setup` | 프로젝트 초기화 |
| `userpromptsubmit` | 사용자 메시지 전송 |
| `pretooluse` | 도구 실행 직전 |
| `posttooluse` | 도구 실행 완료 |
| `posttoolusefailure` | 도구 실행 실패 |
| `stop` | Claude 응답 완료 |
| `stopfailure` | 응답 오류 종료 |
| `notification` | 알림 이벤트 |
| `permissionrequest` | 권한 요청 |
| `permissiondenied` | 권한 거부 |
| `subagentstart` | 서브에이전트 시작 |
| `subagentstop` | 서브에이전트 종료 |
| `taskcreated` | 태스크 생성 |
| `taskcompleted` | 태스크 완료 |
| `teammateidle` | 에이전트 대기 중 |
| `cwdchanged` | 작업 디렉토리 변경 |
| `filechanged` | 파일 변경 감지 |
| `worktreecreate` | Git 워크트리 생성 |
| `worktreeremove` | Git 워크트리 삭제 |
| `precompact` | 컨텍스트 압축 시작 직전 |
| `postcompact` | 컨텍스트 압축 완료 |
| `configchange` | 설정 변경 |
| `elicitation` | 사용자 입력 요청 |
| `elicitationresult` | 사용자 입력 수신 |
| `instructionsloaded` | 커스텀 지시 로드 |

---

## 오디오 가이드라인

### -20 LUFS로 정규화

팩 간 볼륨을 일정하게 유지하기 위해 모든 파일을 **-20 LUFS**로 정규화해 주세요.

```bash
ffmpeg -i input.wav -af "loudnorm=I=-20:TP=-1.5:LRA=11" output.wav
```

팩 전체 일괄 변환:

```bash
for dir in packs/my-pack/sounds/*/; do
  event=$(basename "$dir")
  mp3="$dir${event}.mp3"
  wav="$dir${event}.wav"
  [ -f "$mp3" ] && ffmpeg -y -i "$mp3" -af "loudnorm=I=-20:TP=-1.5:LRA=11" "$wav"
done
```

### 포맷

- `.wav` 또는 `.mp3` (`.wav`를 먼저 시도)
- 권장: 44100 Hz, 스테레오 또는 모노
- 클립 길이: 1~5초가 이상적

### 라이선스

배포 권한이 있는 오디오만 제출해 주세요. MIT, CC BY, CC BY-SA, CC0 등 호환 라이선스 허용.

---

## 내장 팩

| 팩 | 설명 |
|----|------|
| `onepiece` | **[대표 팩]** 원피스 애니메이션 실제 음성 — 루피, 조로, 로빈, 프랑키, 브룩 등 |
| `faker` | T1 페이커(이상혁) 보이스팩 — ElevenLabs IVC |
| `kimetsu` | 귀멸의 칼날(鬼滅の刃) — 탄지로, 렌고쿠, 젠이츠, 이노스케 등 (ElevenLabs TTS) |
| `best-practice` | ElevenLabs "Samara X" 음성 — claude-code-best-practice에서 이식 |
| `silent` | 100ms 무음 — 훅 제거 없이 소리만 비활성화 |
| `default` | 기본 최소 효과음 세트 |

---

## 제출하기

1. 이 저장소를 포크
2. `packs/<이름>/` 폴더에 팩 추가
3. [PACKS.md의 커뮤니티 팩 표](../PACKS.md#커뮤니티-팩)에 행 추가 후 PR 열기
4. `pack.json`의 `preview_url`에 유튜브 데모 링크 포함 권장

PR은 빠르게 리뷰하고 머지합니다. 팩이 많을수록 좋아요. 🎉
