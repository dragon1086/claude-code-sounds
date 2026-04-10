# Faker (Lee Sang-hyeok) Sound Pack

A sound pack featuring AI-cloned voice lines from T1's Faker (이상혁), created via ElevenLabs Instant Voice Cloning from real audio samples.

## Sound Map

| Event | Line | Context |
|-------|------|---------|
| `sessionstart` | 안녕하세요, 저는 T1 페이커입니다. | *Hello, I'm T1 Faker.* — Official self-introduction |
| `setup` | 준비됐습니다. 열심히 하겠습니다. | *I'm ready. I'll do my best.* — Initialization complete |
| `pretooluse` | 해볼게요. | *I'll try it.* — Short focused declaration before action |
| `posttooluse` | 됐네요. | *Done.* — Understated success confirmation |
| `posttoolusefailure` | 아... | *Ah...* — His signature brief sigh |
| `userpromptsubmit` | 알겠습니다, 해볼게요. | *Understood, I'll try it.* — Accepting instructions earnestly |
| `stop` | 수고하셨습니다. | *Good work.* — Calm task-complete, even after a win |
| `stopfailure` | 아직 많이 부족합니다. | *I'm still lacking a lot.* — Humble loss acknowledgment |
| `notification` | 확인했습니다. | *Confirmed.* — Concise alert acknowledgment |
| `permissionrequest` | 잘 부탁드립니다. | *I'm counting on you.* — Polite permission request |
| `permissiondenied` | 그렇군요, 알겠습니다. | *I see, understood.* — Calm acceptance of refusal |
| `sessionend` | 오늘도 수고하셨습니다. T1 화이팅. | *Good work today. T1 fighting.* — Post-match sign-off |
| `subagentstart` | 같이 해봅시다. | *Let's do it together.* — Subagent enters |
| `subagentstop` | 수고하셨습니다. | *Good work.* — Subagent done |
| `taskcreated` | 새 임무가 생겼습니다. | *A new task has arrived.* — Task assigned |
| `taskcompleted` | 완료됐습니다. | *Completed.* — Concise completion |
| `teammateidle` | 조금만 기다려주세요. | *Please wait a moment.* — Idle teammate |
| `cwdchanged` | 이동합니다. | *Moving.* — Directory change |
| `filechanged` | 변경사항이 있네요. | *There's a change.* — File modification detected |
| `worktreecreate` | 새로 시작합니다. | *Starting fresh.* — New branch created |
| `worktreeremove` | 정리됐습니다. | *Cleaned up.* — Branch removed |
| `precompact` | 집중하겠습니다. | *I'll focus.* — Before compaction |
| `postcompact` | 다시 정리됐습니다. | *Reorganized.* — After compaction |
| `configchange` | 설정이 바뀌었네요. | *The settings changed.* — Config modified |
| `elicitation` | 혹시 여쭤봐도 될까요? | *May I ask something?* — Asking for input |
| `elicitationresult` | 감사합니다, 알겠습니다. | *Thank you, understood.* — Got the answer |
| `instructionsloaded` | 확인했습니다, 열심히 하겠습니다. | *Confirmed, I'll work hard.* — Instructions loaded |

## Generating the pack

Real Faker voice samples (YouTube Shorts clips) cloned via ElevenLabs IVC, then TTS-generated for each event.

```bash
# 1. Clone the voice from sample
python3 scripts/clone_faker_voice.py

# 2. Generate the full sound pack
python3 scripts/generate_faker_pack.py
```

## Applying this pack

```bash
./claude-sounds.sh use faker
./install.sh --force
```

## License

Audio is AI-generated via ElevenLabs IVC.  
Original voice © T1 / Lee Sang-hyeok. Personal use only — do not redistribute.
