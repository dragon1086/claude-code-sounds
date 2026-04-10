# 귀멸의 칼날 사운드팩 (鬼滅の刃)

*귀멸의 칼날* 일본어 원작 명대사를 Claude Code 훅 이벤트에 매핑한 사운드팩입니다.

## 등장인물

| 캐릭터 | 역할 | 목소리 스타일 |
|--------|------|--------------|
| 竈門炭治郎 탄지로 | 주인공, 수의 호흡 | 진심 어린 소년, 감동적이고 결의에 찬 목소리 |
| 煉獄杏寿郎 렌고쿠 | 염주, 불꽃의 호흡 | 폭발적인 열정, 따뜻하고 우렁찬 목소리 |
| 我妻善逸 젠이쓰 | 뇌의 호흡 | 겁쟁이와 용자 사이를 오가는 극적인 목소리 |
| 嘴平伊之助 이노스케 | 수수의 호흡 | 멧돼지에게 자란 야생 소년, 실내용 없음 |
| 胡蝶しのぶ 시노부 | 충주, 충의 호흡 | 달콤한 목소리 속 날카로운 독침 |
| 富岡義勇 기유 | 수주, 수의 호흡 | 과묵하고 단조롭지만 깊은 감정 |
| 鬼舞辻無惨 무잔 | 귀신 왕 | 조용하지만 압도적인 공포, 귀족적 냉담함 |
| 竈門禰豆子 네즈코 | 귀신(탄지로의 여동생) | 대나무 재갈로 막힌 귀여운 소리 |

## 이벤트-소리 매핑

| 이벤트 | 캐릭터 | 대사 | 설명 |
|--------|--------|------|------|
| `sessionstart` | 렌고쿠 | 心を燃やせ！ | *마음에 불을 질러라!* — 시작의 동기부여 |
| `setup` | 렌고쿠 | 生まれた時から、炎の呼吸は俺の全てだ！ | *태어날 때부터 불꽃의 호흡은 내 전부!* — 초기 설정 |
| `stop` | 렌고쿠 | うまい！！ | *맛있어!!* — 도시락 먹는 명장면. 작업 완료의 만족감 |
| `stopfailure` | 무잔 | 失望した | *실망이다.* — 냉혹한 실패 선고 |
| `pretooluse` | 탄지로 | 全集中！水の呼吸！ | *전집중! 수의 호흡!* — 기술 시작 전 |
| `posttooluse` | 탄지로 | やった！！ | *해냈어!!* — 성공 |
| `posttoolusefailure` | 젠이쓰 | もう死ぬ！絶対に死ぬ！！ | *죽겠어! 꼭 죽는다!!* — 실패 패닉 |
| `userpromptsubmit` | 탄지로 | わかりました！任せてください！ | *알겠습니다! 맡겨주세요!* — 지시 수락 |
| `notification` | 젠이쓰 | 鬼だ！鬼がいる！！ | *귀신이다! 귀신이 있어!!* — 경보 감지 |
| `permissionrequest` | 탄지로 | お願いします！やらせてください！！ | *부탁드립니다! 하게 해주세요!!* — 권한 요청 |
| `permissiondenied` | 시노부 | お断りします | *사양하겠습니다.* — 미소 지으며 거절하는 명장면 |
| `sessionend` | 렌고쿠 | 胸を張って生きろ | *가슴을 펴고 살아라.* — 탄지로에게 남긴 마지막 말 |
| `subagentstart` | 이노스케 | 俺様が来たぞ！！ | *이노스케님이 오셨다!!* — 서브에이전트 등장 |
| `subagentstop` | 탄지로 | ありがとうございました！ | *감사했습니다!* — 서브에이전트 완료 |
| `taskcreated` | 탄지로 | 新しい任務です！ | *새 임무입니다!* — 작업 생성 |
| `taskcompleted` | 기유 | …終わった | *…끝났다.* — 과묵한 완료 선언 |
| `teammateidle` | 젠이쓰 | 眠い…もう少し休ませてください… | *졸려… 조금만 더 쉬게 해주세요…* — 대기 중 |
| `cwdchanged` | 탄지로 | 次の場所へ向かいます | *다음 장소로 향합니다.* — 디렉토리 이동 |
| `filechanged` | 이노스케 | 何かが変わったぞ！！ | *뭔가 변했다!!* — 파일 변경 감지 |
| `worktreecreate` | 탄지로 | 新しい道を切り開きます！ | *새 길을 개척합니다!* — 워크트리 생성 |
| `worktreeremove` | 기유 | もう必要ない | *더 이상 필요 없다.* — 워크트리 삭제 |
| `precompact` | 탄지로 | 全集中の呼吸、常中 | *전집중의 호흡, 상중.* — 컴팩트 준비 |
| `postcompact` | 탄지로 | 準備できました | *준비됐습니다.* — 컴팩트 완료 |
| `instructionsloaded` | 렌고쿠 | 師匠の教えを、胸に刻め！ | *스승의 가르침을 가슴에 새겨라!* — 지시 로드 |
| `configchange` | 시노부 | 少し変えてみましょうか | *조금 바꿔볼까요.* — 설정 변경 |
| `elicitation` | 탄지로 | 一つ教えていただけますか？ | *한 가지 가르쳐 주시겠습니까?* — 입력 요청 |
| `elicitationresult` | 탄지로 | そうか！わかりました！ | *그렇구나! 알겠습니다!* — 답변 수신 |

## 오디오 소스

팬 사운드보드 및 커뮤니티 리소스에서 수집:

- [101soundboards.com — Demon Slayer](https://www.101soundboards.com/boards/76341-demon-slayer-kimetsu-no-yaiba-soundboard)
- [Voicy.network — Demon Slayer](https://www.voicy.network/official-soundboards/anime/demon-slayer)
- [SoundboardMax — Demon Slayer](https://soundboardmax.com/demon-slayer-soundboard/)
- [MyInstants — Demon Slayer](https://www.myinstants.com/en/search/?name=demon+slayer)

## ElevenLabs로 생성하는 방법 (대안)

실제 오디오 대신 AI 생성 음성을 원한다면:

```bash
pip install elevenlabs
export ELEVENLABS_API_KEY="your_key_here"
python scripts/generate_kimetsu_pack.py
```

각 캐릭터의 원작 성우 스타일을 참고한 일본어 특화 Voice Design 프롬프트가 포함되어 있습니다.

## 팩 적용 방법

```bash
./claude-sounds.sh use kimetsu
./install.sh --force
```

## 라이선스

오디오 클립은 팬 소스 수집본입니다. *귀멸의 칼날* © 吾峠呼世晴 / 集英社 / アニプレックス / ufotable
