# Demon Slayer Sound Pack (鬼滅の刃)

Iconic Japanese voice lines from *Kimetsu no Yaiba*, matched to every Claude Code hook event.

## Characters

| Character | Role | Voice style |
|-----------|------|-------------|
| 竈門炭治郎 Tanjiro | Main protagonist, Water Breathing | Sincere, earnest, emotional depth |
| 煉獄杏寿郎 Rengoku | Flame Pillar | Explosive passion, warm and booming |
| 我妻善逸 Zenitsu | Thunder Breathing | Panic-to-bravado whiplash, high-pitched |
| 嘴平伊之助 Inosuke | Beast Breathing | Feral, no indoor voice, raised by boars |
| 胡蝶しのぶ Shinobu | Insect Pillar | Sweet voice, passive-aggressive edge |
| 富岡義勇 Giyu | Water Pillar | Stoic, maximum meaning in minimum words |
| 鬼舞辻無惨 Muzan | Demon King | Soft-spoken, aristocratic terror |
| 竈門禰豆子 Nezuko | Demon (Tanjiro's sister) | Muffled cute murmurs, bamboo-gagged |

## Sound Map

| Event | Character | Line (Japanese) | Context |
|-------|-----------|-----------------|---------|
| `sessionstart` | 煉獄 Rengoku | 心を燃やせ！ | *Set your heart ablaze!* — Starting motivation |
| `setup` | 煉獄 Rengoku | 生まれた時から、炎の呼吸は俺の全てだ！ | *Flame Breathing has been my everything since birth!* — Initialization |
| `stop` | 煉獄 Rengoku | うまい！！ | *Delicious!!* — His iconic food reaction; perfect task-complete satisfaction |
| `stopfailure` | 無惨 Muzan | 失望した | *I am disappointed.* — Cold dismissal on failure |
| `pretooluse` | 炭治郎 Tanjiro | 全集中！水の呼吸！ | *Total Concentration! Water Breathing!* — Technique start |
| `posttooluse` | 炭治郎 Tanjiro | やった！！ | *I did it!!* — Success |
| `posttoolusefailure` | 善逸 Zenitsu | もう死ぬ！絶対に死ぬ！！ | *I'm gonna die! I'm definitely gonna die!!* — Panic on tool failure |
| `userpromptsubmit` | 炭治郎 Tanjiro | わかりました！任せてください！ | *Understood! Leave it to me!* — Accepting a request |
| `notification` | 善逸 Zenitsu | 鬼だ！鬼がいる！！ | *A demon! There's a demon!!* — Alert detection |
| `permissionrequest` | 炭治郎 Tanjiro | お願いします！やらせてください！！ | *Please! Let me do this!!* — Earnest permission request |
| `permissiondenied` | しのぶ Shinobu | お断りします | *I must decline.* — Iconic smile-refusal |
| `sessionend` | 煉獄 Rengoku | 胸を張って生きろ | *Live with your chest held high.* — Rengoku's final words to Tanjiro |
| `subagentstart` | 伊之助 Inosuke | 俺様が来たぞ！！ | *The great Inosuke has arrived!!* — Subagent enters |
| `subagentstop` | 炭治郎 Tanjiro | ありがとうございました！ | *Thank you very much!* — Subagent done |
| `taskcreated` | 炭治郎 Tanjiro | 新しい任務です！ | *A new mission!* — Task assigned |
| `taskcompleted` | 義勇 Giyu | …終わった | *…It's over.* — Stoic completion |
| `teammateidle` | 善逸 Zenitsu | 眠い…もう少し休ませてください… | *Sleepy… let me rest a little more…* — Idle waiting |
| `cwdchanged` | 炭治郎 Tanjiro | 次の場所へ向かいます | *Heading to the next location.* — Directory change |
| `filechanged` | 伊之助 Inosuke | 何かが変わったぞ！！ | *Something changed!!* — File modification detected |
| `worktreecreate` | 炭治郎 Tanjiro | 新しい道を切り開きます！ | *I'll carve open a new path!* — New branch created |
| `worktreeremove` | 義勇 Giyu | もう必要ない | *No longer needed.* — Branch removed |
| `precompact` | 炭治郎 Tanjiro | 全集中の呼吸、常中 | *Total Concentration Breathing, constant.* — Before compaction |
| `postcompact` | 炭治郎 Tanjiro | 準備できました | *Ready.* — After compaction |
| `instructionsloaded` | 煉獄 Rengoku | 師匠の教えを、胸に刻め！ | *Engrave your master's teachings in your heart!* — Instructions loaded |
| `configchange` | しのぶ Shinobu | 少し変えてみましょうか | *Shall we change things up a little?* — Config modified |
| `elicitation` | 炭治郎 Tanjiro | 一つ教えていただけますか？ | *Could you teach me one thing?* — Asking for input |
| `elicitationresult` | 炭治郎 Tanjiro | そうか！わかりました！ | *I see! Understood!* — Got the answer |

## Audio Sources

Audio clips sourced from fan soundboards and community resources:

- [101soundboards.com — Demon Slayer](https://www.101soundboards.com/boards/76341-demon-slayer-kimetsu-no-yaiba-soundboard)
- [Voicy.network — Demon Slayer](https://www.voicy.network/official-soundboards/anime/demon-slayer)
- [SoundboardMax — Demon Slayer](https://soundboardmax.com/demon-slayer-soundboard/)
- [MyInstants — Demon Slayer](https://www.myinstants.com/en/search/?name=demon+slayer)

## Generating with ElevenLabs (alternative)

If you prefer AI-generated voices instead of sourced clips:

```bash
pip install elevenlabs
export ELEVENLABS_API_KEY="your_key_here"
python scripts/generate_kimetsu_pack.py
```

The script uses `eleven_multilingual_v2` with Japanese-optimized voice descriptions modeled after each character's original voice actor style.

## Applying this pack

```bash
./claude-sounds.sh use kimetsu
./install.sh --force
```

## License

Audio clips are fan-sourced. *Kimetsu no Yaiba* is © Koyoharu Gotouge / Shueisha / Aniplex / Ufotable.
