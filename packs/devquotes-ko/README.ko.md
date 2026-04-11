# 개발자 명언 사운드팩 (한국어)

전설적인 개발자와 사상가들의 동기부여 명언 모음. ElevenLabs TTS(Alice — Clear Educator) 목소리로 생성.

## 이벤트 → 명언 매핑

| 이벤트 | 명언 | 출처 |
|--------|------|------|
| `sessionstart` | "코드로 증명해라. 말은 필요 없어." | 리누스 토르발즈 |
| `setup` | "두 번 재고, 한 번에 잘라라." | 속담 |
| `pretooluse` | "작동하게, 올바르게, 그리고 빠르게." | 켄트 벡 |
| `posttooluse` | "먼저 문제를 풀어라. 그다음에 코드를 써라." | 존 존슨 |
| `posttoolusefailure` | "버그가 아니야. 문서화 안 된 기능이지." | 익명 |
| `userpromptsubmit` | "어떤 바보도 컴퓨터가 이해하는 코드를 쓸 수 있다." | 마틴 파울러 |
| `stop` | "완벽함보다 완성이 낫다." | 마크 저커버그 |
| `stopfailure` | "모든 전문가는 한때 초보자였다." | 헬렌 헤이스 |
| `notification` | "조기 최적화는 모든 악의 근원이다." | 도널드 크누스 |
| `permissionrequest` | "큰 힘에는 큰 책임이 따른다." | 스탠 리 |
| `permissiondenied` | "단순하게, 바보야." | 켈리 존슨 |
| `sessionend` | "미래를 예측하는 최선의 방법은 미래를 발명하는 것이다." | 앨런 케이 |
| `subagentstart` | "백지장도 맞들면 낫다." | 속담 |
| `subagentstop` | "여럿이 하면 짐도 가벼워진다." | 속담 |
| `taskcreated` | "계획 없는 목표는 그냥 소원이다." | 생텍쥐페리 |
| `taskcompleted` | "배포해!" | 실리콘밸리 |
| `teammateidle` | "인내는 미덕이다." | 속담 |
| `cwdchanged` | "변화만이 유일한 상수다." | 헤라클레이토스 |
| `filechanged` | "빠르게 가려면 올바르게 가야 한다." | 로버트 마틴 |
| `worktreecreate` | "시작하려면, 시작해라." | 윌리엄 워즈워스 |
| `worktreeremove` | "단순함이 궁극의 세련됨이다." | 레오나르도 다빈치 |
| `precompact` | "적을수록 풍요롭다." | 미스 반 데어 로에 |
| `postcompact` | "좋은 코드는 잘 쓰인 산문처럼 읽힌다." | 로버트 마틴 |
| `configchange` | "적응하거나 소멸하라." | H.G. 웰스 |
| `elicitation` | "구하라, 그러면 얻을 것이다." | 마태복음 |
| `elicitationresult` | "아는 것이 힘이다." | 프랜시스 베이컨 |
| `instructionsloaded` | "지시 수신 완료. 멋진 것을 만들어보자." | — |

## 사용 방법

```bash
./claude-sounds.sh use devquotes-ko
./install.sh --force
```

## 오디오 생성 방법

ElevenLabs `eleven_multilingual_v2` 모델과 Alice(Clear Educator) 목소리로 생성.

```bash
python3 scripts/generate_devquotes_pack.py --lang ko
```

## 라이선스

오디오는 ElevenLabs TTS로 생성된 AI 음성입니다.
인용된 명언은 공공 도메인 또는 공정 이용에 해당합니다.
개인 사용 전용 — 재배포 금지.
