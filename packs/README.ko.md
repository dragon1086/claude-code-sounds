# 사운드팩

사운드팩은 기본 사운드를 덮어쓰는 오디오 파일 모음 폴더입니다.

## 팩 형식

```
my-pack/
├── pack.json          # 필수 메타데이터
└── sounds/            # hooks/sounds/와 동일한 폴더 구조
    ├── sessionstart/
    │   └── sessionstart.wav
    ├── stop/
    │   └── stop.wav
    └── ...
```

**부분 팩도 지원됩니다.** 덮어쓰고 싶은 사운드만 포함하면 됩니다.  
없는 슬롯은 자동으로 `default` 팩을 사용합니다.

## pack.json 필드

```json
{
  "name": "my-pack",
  "author": "your-github-username",
  "description": "팩에 대한 간단한 설명",
  "license": "MIT",
  "preview_url": "https://..."
}
```

## 내장 팩

| 팩 | 설명 |
|----|------|
| `onepiece` | 원피스 애니메이션 실제 음성 — 루피, 조로, 로빈 등의 명장면. **기본 팩.** |
| `best-practice` | ElevenLabs "Samara X" 음성 — claude-code-best-practice에서 이식 |
| `silent` | 100ms 무음 — 훅을 제거하지 않고 소리를 비활성화 |

## 내 음성으로 교체하기

원하는 파일로 직접 교체할 수 있어요:

```
.claude/hooks/sounds/stop/
└── stop.wav   ← 원하는 파일로 교체
```

파일 이름은 폴더 이름과 일치해야 합니다. `.wav`와 `.mp3` 모두 지원됩니다 (`.wav`를 먼저 시도합니다).

## 오디오 가이드라인

팩 간 볼륨을 일정하게 유지하려면 모든 오디오 파일을 **-20 LUFS** 통합 라우드니스로 정규화한 후 제출해 주세요.

ffmpeg으로 정규화하는 방법 (2패스, 정확도 높음):

```bash
# 1패스 — 라우드니스 측정
stats=$(ffmpeg -i input.wav -af "loudnorm=I=-20:TP=-1.5:LRA=11:print_format=json" -f null - 2>&1)

# 측정값을 적용해 2패스 인코딩
ffmpeg -i input.wav \
  -af "loudnorm=I=-20:TP=-1.5:LRA=11:measured_I=<input_i>:measured_TP=<input_tp>:measured_LRA=<input_lra>:measured_thresh=<input_thresh>:offset=<target_offset>:linear=true" \
  -ar 44100 output.wav
```

볼륨이 비슷한 파일이라면 간단한 1패스도 충분합니다:

```bash
ffmpeg -i input.wav -af loudnorm=I=-20:TP=-1.5:LRA=11 output.wav
```

## 커뮤니티 팩

커뮤니티 기여 팩은 [PACKS.md](../PACKS.md)를 참고하세요.

팩을 제출하려면 `PACKS.md`에 항목을 추가하는 PR을 열어주세요.
