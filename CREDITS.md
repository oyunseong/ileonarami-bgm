# CREDITS

이 저장소의 모든 음원은 **CC0 1.0 (퍼블릭 도메인)** 으로 배포된 원본을 재인코딩한 것이다.
CC0는 저작자 표시 의무가 없지만, 출처 추적과 재검증을 위해 아래에 원본을 기록해 둔다.

| 파일 | 원본 트랙 | 저작자 | 출처 | 라이선스 |
|---|---|---|---|---|
| `sounds/pixel_morning.ogg` | Retro Game Music Pack — Level 1 | Juhani Junkala (SubspaceAudio) | https://opengameart.org/content/5-chiptunes-action | CC0 1.0 |
| `sounds/pixel_rush.ogg` | Retro Game Music Pack — Level 2 | Juhani Junkala (SubspaceAudio) | https://opengameart.org/content/5-chiptunes-action | CC0 1.0 |
| `sounds/pixel_boss.ogg` | Retro Game Music Pack — Level 3 | Juhani Junkala (SubspaceAudio) | https://opengameart.org/content/5-chiptunes-action | CC0 1.0 |
| `sounds/starlight_city.ogg` | Starlight City (LOOP) | Zane Little Music | https://opengameart.org/content/starlight-city-loop-included | CC0 1.0 |
| `sounds/nes_mercury.ogg` | NES Shooter Music — Mercury | SketchyLogic | https://opengameart.org/content/nes-shooter-music-5-tracks-3-jingles | CC0 1.0 |
| `sounds/nes_venus.ogg` | NES Shooter Music — Venus | SketchyLogic | https://opengameart.org/content/nes-shooter-music-5-tracks-3-jingles | CC0 1.0 |

Juhani Junkala 팩에 동봉된 `INFO.txt` 원문:

> These music tracks have been released under CC0 creative commons license.
> You can do anything you want with these tunes.

SketchyLogic 원본 페이지 표기: "Attribution is completely optional."

## 가공 내용

원본 WAV → Opus/Ogg. 적용한 처리는 두 가지뿐이다.

- 라우드니스 정규화: `loudnorm=I=-14:TP=-1.0:LRA=11` (트랙 간 음량 편차 제거)
- 인코딩: `libopus -b:a 96k -vbr on -ar 48000 -ac 2` (실측 약 107kbps)

**페이드인/아웃은 넣지 않았다.** 원본이 seamless loop이고 알람은 반복 재생이라,
페이드를 넣으면 루프가 돌 때마다 소리가 사라졌다 커진다.
