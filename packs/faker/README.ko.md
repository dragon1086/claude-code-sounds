# 페이커(이상혁) 사운드팩

T1 페이커(이상혁)의 실제 음성 샘플을 ElevenLabs IVC(Instant Voice Cloning)로 클로닝한 사운드팩.

## 이벤트-소리 매핑

| 이벤트 | 대사 | 설명 |
|--------|------|------|
| `sessionstart` | 안녕하세요, 저는 T1 페이커입니다. | 공식 자기소개 |
| `setup` | 준비됐습니다. 열심히 하겠습니다. | 초기 설정 완료 |
| `pretooluse` | 해볼게요. | 도구 사용 전 짧은 집중 선언 |
| `posttooluse` | 됐네요. | 담담한 성공 확인 |
| `posttoolusefailure` | 아... | 특유의 짧은 탄식 |
| `userpromptsubmit` | 알겠습니다, 해볼게요. | 지시 성실하게 수락 |
| `stop` | 수고하셨습니다. | 작업 완료 — 우승 후에도 담담함 |
| `stopfailure` | 아직 많이 부족합니다. | 겸손한 패배 인정 |
| `notification` | 확인했습니다. | 간결한 알림 확인 |
| `permissionrequest` | 잘 부탁드립니다. | 정중한 권한 요청 |
| `permissiondenied` | 그렇군요, 알겠습니다. | 담담한 거절 수용 |
| `sessionend` | 오늘도 수고하셨습니다. T1 화이팅. | 경기 후 인사 |
| `subagentstart` | 같이 해봅시다. | 서브에이전트 등장 |
| `subagentstop` | 수고하셨습니다. | 서브에이전트 완료 |
| `taskcreated` | 새 임무가 생겼습니다. | 새 작업 생성 |
| `taskcompleted` | 완료됐습니다. | 간결한 완료 선언 |
| `teammateidle` | 조금만 기다려주세요. | 팀원 대기 중 |
| `cwdchanged` | 이동합니다. | 디렉토리 이동 |
| `filechanged` | 변경사항이 있네요. | 파일 변경 감지 |
| `worktreecreate` | 새로 시작합니다. | 워크트리 생성 |
| `worktreeremove` | 정리됐습니다. | 워크트리 삭제 |
| `precompact` | 집중하겠습니다. | 컴팩트 전 집중 |
| `postcompact` | 다시 정리됐습니다. | 컴팩트 후 재정비 |
| `configchange` | 설정이 바뀌었네요. | 설정 변경 감지 |
| `elicitation` | 혹시 여쭤봐도 될까요? | 입력 요청 |
| `elicitationresult` | 감사합니다, 알겠습니다. | 답변 수신 |
| `instructionsloaded` | 확인했습니다, 열심히 하겠습니다. | 지시 로드 완료 |

## 오디오 생성 방법

실제 페이커 음성 샘플(YouTube Shorts 클립)을 ElevenLabs IVC로 클로닝한 후 TTS 생성.

```bash
# 1. 음성 샘플 다운로드 및 클로닝
python3 scripts/clone_faker_voice.py

# 2. 전체 사운드팩 생성
python3 scripts/generate_faker_pack.py
```

## 팩 적용 방법

```bash
./claude-sounds.sh use faker
./install.sh --force
```

## 라이선스

오디오는 ElevenLabs IVC로 생성된 AI 음성입니다.  
원본 음성 © T1 / 이상혁. 개인 사용 전용 — 재배포 금지.
